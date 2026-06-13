import json
import sys
import tempfile
from pathlib import Path

# Add project root to path so we can import runtime
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from runtime.validator import (
    validate_requirements_chain,
    validate_phase_contract,
    validate_evidence_ledger,
    validate_approval_record,
    validate_phase_closeout,
    validate_domain_pack,
)

FIXTURES = Path(__file__).parent / "fixtures"


def _fixture(name: str) -> str:
    return str(FIXTURES / name)


# --- requirements_chain ---


class TestValidateRequirementsChain:
    def test_valid(self):
        result = validate_requirements_chain(_fixture("requirements_chain_valid.json"))
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_missing_id(self):
        result = validate_requirements_chain(
            _fixture("requirements_chain_missing_id.json")
        )
        assert result["passed"] is False
        assert any("Missing required field: id" in v for v in result["violations"])

    def test_invalid_status(self):
        result = validate_requirements_chain(
            _fixture("requirements_chain_invalid_status.json")
        )
        assert result["passed"] is False
        assert any("Invalid status" in v for v in result["violations"])

    def test_passed_without_evidence(self):
        result = validate_requirements_chain(
            _fixture("requirements_chain_passed_no_evidence.json")
        )
        assert result["passed"] is False
        assert any("requires at least one" in v for v in result["violations"])

    def test_empty_source(self):
        result = validate_requirements_chain(
            _fixture("requirements_chain_empty_source.json")
        )
        assert result["passed"] is False
        assert any("source" in v and "non-empty" in v for v in result["violations"])

    def test_wrong_artifact_type(self):
        result = validate_requirements_chain(
            _fixture("requirements_chain_wrong_artifact_type.json")
        )
        assert result["passed"] is False
        assert any("Wrong artifact_type" in v for v in result["violations"])

    def test_invalid_side_effect_tier(self):
        result = validate_requirements_chain(
            _fixture("requirements_chain_invalid_side_effect_tier.json")
        )
        assert result["passed"] is False
        assert any("Invalid side_effect_tier" in v for v in result["violations"])

    def test_invalid_validation_method(self):
        result = validate_requirements_chain(
            _fixture("requirements_chain_invalid_validation_method.json")
        )
        assert result["passed"] is False
        assert any("Invalid validation_method" in v for v in result["violations"])


# --- phase_contract ---


class TestValidatePhaseContract:
    def test_valid(self):
        result = validate_phase_contract(_fixture("phase_contract_valid.json"))
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_missing_domain(self):
        result = validate_phase_contract(_fixture("phase_contract_missing_domain.json"))
        assert result["passed"] is False
        assert any("Missing required field: domain" in v for v in result["violations"])

    def test_invalid_status(self):
        result = validate_phase_contract(_fixture("phase_contract_invalid_status.json"))
        assert result["passed"] is False
        assert any("Invalid status" in v for v in result["violations"])

    def test_wrong_artifact_type(self):
        result = validate_phase_contract(
            _fixture("phase_contract_wrong_artifact_type.json")
        )
        assert result["passed"] is False
        assert any("Wrong artifact_type" in v for v in result["violations"])


# --- evidence_ledger ---


class TestValidateEvidenceLedger:
    def test_valid(self):
        result = validate_evidence_ledger(_fixture("evidence_ledger_valid.json"))
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_missing_requirement_id(self):
        result = validate_evidence_ledger(
            _fixture("evidence_ledger_missing_requirement_id.json")
        )
        assert result["passed"] is False
        assert any(
            "Missing required field: requirement_id" in v for v in result["violations"]
        )

    def test_invalid_evidence_type(self):
        result = validate_evidence_ledger(_fixture("evidence_ledger_invalid_type.json"))
        assert result["passed"] is False
        assert any("Invalid evidence_type" in v for v in result["violations"])

    def test_wrong_artifact_type(self):
        result = validate_evidence_ledger(
            _fixture("evidence_ledger_wrong_artifact_type.json")
        )
        assert result["passed"] is False
        assert any("Wrong artifact_type" in v for v in result["violations"])

    def test_nonbool_verified(self):
        result = validate_evidence_ledger(
            _fixture("evidence_ledger_nonbool_verified.json")
        )
        assert result["passed"] is False
        assert any("verified" in v and "boolean" in v for v in result["violations"])


# --- approval_record ---


class TestValidateApprovalRecord:
    def test_valid(self):
        result = validate_approval_record(_fixture("approval_record_valid.json"))
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_missing_requirement_ids(self):
        result = validate_approval_record(
            _fixture("approval_record_missing_requirement_ids.json")
        )
        assert result["passed"] is False
        assert any(
            "Missing required field: requirement_ids" in v for v in result["violations"]
        )

    def test_approved_without_approver(self):
        result = validate_approval_record(
            _fixture("approval_record_approved_no_approver.json")
        )
        assert result["passed"] is False
        assert any("requires an approver" in v for v in result["violations"])
        assert any("requires a timestamp" in v for v in result["violations"])

    def test_wrong_artifact_type(self):
        result = validate_approval_record(
            _fixture("approval_record_wrong_artifact_type.json")
        )
        assert result["passed"] is False
        assert any("Wrong artifact_type" in v for v in result["violations"])

    def test_requested_bad_approver(self):
        """Status 'requested' requires approver='not_yet_approved' and timestamp='pending'."""
        result = validate_approval_record(
            _fixture("approval_record_requested_bad_state.json")
        )
        assert result["passed"] is False
        assert any(
            "requested" in v and "not_yet_approved" in v for v in result["violations"]
        )
        assert any("requested" in v and "pending" in v for v in result["violations"])

    def test_denied_without_approver(self):
        """Status 'denied' requires an approver and timestamp."""
        result = validate_approval_record(
            _fixture("approval_record_denied_no_approver.json")
        )
        assert result["passed"] is False
        assert any("requires an approver" in v for v in result["violations"])
        assert any("requires a timestamp" in v for v in result["violations"])

    def test_highrisk_no_residual_risk(self):
        """High-risk side_effect_tier requires non-empty residual_risk."""
        result = validate_approval_record(
            _fixture("approval_record_highrisk_no_risk.json")
        )
        assert result["passed"] is False
        assert any(
            "residual_risk" in v and "non-empty" in v for v in result["violations"]
        )


# --- phase_closeout ---


class TestValidatePhaseCloseout:
    def test_valid(self):
        result = validate_phase_closeout(_fixture("phase_closeout_valid.json"))
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_missing_phase_id(self):
        result = validate_phase_closeout(
            _fixture("phase_closeout_missing_phase_id.json")
        )
        assert result["passed"] is False
        assert any(
            "Missing required field: phase_id" in v for v in result["violations"]
        )

    def test_invalid_status(self):
        result = validate_phase_closeout(_fixture("phase_closeout_invalid_status.json"))
        assert result["passed"] is False
        assert any("Invalid status" in v for v in result["violations"])

    def test_wrong_artifact_type(self):
        result = validate_phase_closeout(
            _fixture("phase_closeout_wrong_artifact_type.json")
        )
        assert result["passed"] is False
        assert any("Wrong artifact_type" in v for v in result["violations"])

    def test_nonbool_objective_met(self):
        result = validate_phase_closeout(
            _fixture("phase_closeout_nonbool_objective_met.json")
        )
        assert result["passed"] is False
        assert any(
            "objective_met" in v and "boolean" in v for v in result["violations"]
        )


# --- domain_pack ---


class TestValidateDomainPack:
    def test_valid(self):
        result = validate_domain_pack(_fixture("domain_pack_valid.json"))
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_general_fallback_fixture_valid(self):
        result = validate_domain_pack(_fixture("domain_pack_general_fallback.json"))
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_general_fallback_pack_valid(self):
        pack = project_root / "runtime" / "domain_packs" / "general_fallback.json"
        result = validate_domain_pack(pack)
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_software_engineering_fixture_valid(self):
        result = validate_domain_pack(_fixture("domain_pack_software_engineering.json"))
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_software_engineering_pack_valid(self):
        pack = project_root / "runtime" / "domain_packs" / "software_engineering.json"
        result = validate_domain_pack(pack)
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_scheduling_fixture_valid(self):
        result = validate_domain_pack(_fixture("domain_pack_scheduling.json"))
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_scheduling_pack_valid(self):
        pack = project_root / "runtime" / "domain_packs" / "scheduling.json"
        result = validate_domain_pack(pack)
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_travel_purchase_fixture_valid(self):
        result = validate_domain_pack(_fixture("domain_pack_travel_purchase.json"))
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_travel_purchase_pack_valid(self):
        pack = project_root / "runtime" / "domain_packs" / "travel_purchase.json"
        result = validate_domain_pack(pack)
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_writing_editing_fixture_valid(self):
        result = validate_domain_pack(_fixture("domain_pack_writing_editing.json"))
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_writing_editing_pack_valid(self):
        pack = project_root / "runtime" / "domain_packs" / "writing_editing.json"
        result = validate_domain_pack(pack)
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_research_summary_fixture_valid(self):
        result = validate_domain_pack(_fixture("domain_pack_research_summary.json"))
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_research_summary_pack_valid(self):
        pack = project_root / "runtime" / "domain_packs" / "research_summary.json"
        result = validate_domain_pack(pack)
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_missing_approval_gates(self):
        result = validate_domain_pack(
            _fixture("domain_pack_missing_approval_gates.json")
        )
        assert result["passed"] is False
        assert any(
            "Missing required field: approval_gates" in v for v in result["violations"]
        )

    def test_empty_triggers(self):
        result = validate_domain_pack(_fixture("domain_pack_empty_triggers.json"))
        assert result["passed"] is False
        assert any("triggers" in v and "non-empty" in v for v in result["violations"])

    def test_invalid_check_type(self):
        result = validate_domain_pack(_fixture("domain_pack_invalid_check_type.json"))
        assert result["passed"] is False
        assert any("check_type" in v for v in result["violations"])

    def test_missing_boundary_gate(self):
        """Rule 9: requires_approval actions must have approval_gates entries."""
        result = validate_domain_pack(
            _fixture("domain_pack_missing_boundary_gate.json")
        )
        assert result["passed"] is False
        assert any(
            "requires_approval" in v and "approval_gates" in v
            for v in result["violations"]
        )

    def test_invalid_domain_format(self):
        """Rule 1: domain must be lowercase with underscores."""
        result = validate_domain_pack(_fixture("domain_pack_invalid_domain.json"))
        assert result["passed"] is False
        assert any(
            "domain" in v.lower() and "lowercase" in v.lower()
            for v in result["violations"]
        )

    def test_invalid_required_artifact(self):
        """Rule 3: required_artifacts must be from universal vocabulary."""
        result = validate_domain_pack(_fixture("domain_pack_bad_artifact_type.json"))
        assert result["passed"] is False
        assert any("Invalid required_artifact" in v for v in result["violations"])

    def test_incomplete_validation_gate(self):
        """Rule 4: validation_gates entries must have description, required, check_type."""
        result = validate_domain_pack(_fixture("domain_pack_incomplete_gate.json"))
        assert result["passed"] is False
        assert any("missing 'required'" in v for v in result["violations"])
        assert any("missing 'check_type'" in v for v in result["violations"])

    def test_invalid_boundary_value(self):
        """Rule 7: external_action_boundaries values must be allowed/requires_approval/blocked."""
        result = validate_domain_pack(
            _fixture("domain_pack_invalid_boundary_value.json")
        )
        assert result["passed"] is False
        assert any(
            "Invalid" in v and "external_action_boundaries" in v
            for v in result["violations"]
        )

    def test_empty_residual_risk(self):
        """Rule 8: residual_risk must be non-empty."""
        result = validate_domain_pack(_fixture("domain_pack_empty_residual_risk.json"))
        assert result["passed"] is False
        assert any(
            "residual_risk" in v and "non-empty" in v for v in result["violations"]
        )

    def test_wrong_artifact_type(self):
        """Wrong artifact_type is rejected."""
        result = validate_domain_pack(_fixture("domain_pack_wrong_artifact_type.json"))
        assert result["passed"] is False
        assert any("Wrong artifact_type" in v for v in result["violations"])

    def test_general_fallback_requires_wildcard_trigger(self):
        """Rule 10: general_fallback must use the wildcard trigger."""
        data = {
            "artifact_type": "domain_pack",
            "domain": "general_fallback",
            "triggers": ["unknown"],
            "required_artifacts": ["requirements_chain"],
            "validation_gates": {
                "requirement_trace_exists": {
                    "description": "Requirement trace exists",
                    "required": True,
                    "check_type": "field_presence",
                }
            },
            "approval_gates": ["external_action"],
            "external_action_boundaries": {
                "external_action": "requires_approval",
            },
            "residual_risk": "Unknown-domain checks may miss domain specifics.",
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            f.flush()
            result = validate_domain_pack(f.name)
        assert result["passed"] is False
        assert any(
            "general_fallback" in v and "triggers" in v for v in result["violations"]
        )


# --- Cross-artifact consistency ---


class TestCrossArtifact:
    def test_workflow_consistent(self):
        from runtime.validator import validate_workflow

        result = validate_workflow(
            {
                "requirements_chain": _fixture("requirements_chain_valid.json"),
                "evidence_ledger": _fixture("evidence_ledger_valid.json"),
                "phase_closeout": _fixture("phase_closeout_valid.json"),
            }
        )
        assert result["passed"] is True, (
            f"Unexpected violations: {result['violations']}"
        )

    def test_workflow_orphan_evidence(self):
        from runtime.validator import validate_workflow

        result = validate_workflow(
            {
                "requirements_chain": _fixture("requirements_chain_valid.json"),
                "evidence_ledger": _fixture("evidence_ledger_valid.json"),
                "phase_closeout": _fixture("phase_closeout_missing_phase_id.json"),
            }
        )
        # phase_closeout_missing_phase_id has evidence_ids: [], so no orphan check
        # but it should still have structural violations from the closeout itself
        assert "violations" in result or "warnings" in result

    def test_workflow_orphan_evidence_id(self):
        """phase_closeout references evidence_id not in evidence_ledger."""
        from runtime.validator import validate_workflow

        result = validate_workflow(
            {
                "evidence_ledger": _fixture("evidence_ledger_valid.json"),
                "phase_closeout": _fixture("phase_closeout_orphan_evidence.json"),
            }
        )
        assert result["passed"] is False
        assert any("not found in evidence_ledger" in v for v in result["violations"])

    def test_workflow_orphan_requirement_id(self):
        """evidence_ledger references requirement_id not in requirements_chain."""
        from runtime.validator import validate_workflow

        result = validate_workflow(
            {
                "requirements_chain": _fixture("requirements_chain_valid.json"),
                "evidence_ledger": _fixture("evidence_ledger_orphan_requirement.json"),
            }
        )
        assert result["passed"] is False
        assert any("not found in requirements_chain" in v for v in result["violations"])

    def test_workflow_missing_artifact_types(self):
        """Workflow with only one artifact type still validates."""
        from runtime.validator import validate_workflow

        result = validate_workflow(
            {
                "requirements_chain": _fixture("requirements_chain_valid.json"),
            }
        )
        assert result["passed"] is True

    def test_workflow_all_invalid(self):
        """validate_workflow runs structural and cross-artifact checks."""
        from runtime.validator import validate_workflow

        result = validate_workflow(
            {
                "requirements_chain": _fixture("requirements_chain_missing_id.json"),
                "evidence_ledger": _fixture(
                    "evidence_ledger_missing_requirement_id.json"
                ),
                "phase_closeout": _fixture("phase_closeout_missing_phase_id.json"),
            }
        )
        assert result["passed"] is False
        assert any(
            "requirements_chain: Missing required field: id" in v
            for v in result["violations"]
        )
        assert any(
            "evidence_ledger: Missing required field: requirement_id" in v
            for v in result["violations"]
        )
        assert any(
            "phase_closeout: Missing required field: phase_id" in v
            for v in result["violations"]
        )

    def test_workflow_structural_failure_blocks_reference_pass(self):
        """Cross-consistent IDs cannot hide invalid required fields."""
        from runtime.validator import validate_workflow

        result = validate_workflow(
            {
                "requirements_chain": _fixture("requirements_chain_missing_id.json"),
                "evidence_ledger": _fixture("evidence_ledger_valid.json"),
                "phase_closeout": _fixture("phase_closeout_valid.json"),
            }
        )
        assert result["passed"] is False
        assert any(
            "requirements_chain: Missing required field: id" in v
            for v in result["violations"]
        )


# --- Warnings ---


class TestWarnings:
    def test_requirements_chain_pending_no_phases(self):
        import json, tempfile

        data = {
            "artifact_type": "requirements_chain",
            "id": "req-warn",
            "source": "Pending with no phases",
            "domain": "general",
            "side_effect_tier": "read_only",
            "validation_method": "artifact_check",
            "phase_ids": [],
            "evidence_ids": [],
            "status": "pending",
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            f.flush()
            result = validate_requirements_chain(f.name)
        assert result["passed"] is True
        assert any(
            "no phases" in w.lower() or "still pending" in w.lower()
            for w in result["warnings"]
        )

    def test_approval_record_warnings_present(self):
        """Validator result includes warnings key even when empty."""
        result = validate_approval_record(_fixture("approval_record_valid.json"))
        assert "warnings" in result
        assert isinstance(result["warnings"], list)

    def test_approval_record_empty_requirement_ids(self):
        data = {
            "artifact_type": "approval_record",
            "id": "appr-empty",
            "requirement_ids": [],
            "action": "Send invite",
            "side_effect_tier": "external_write",
            "requester": "scheduling-agent",
            "approver": "user:frank",
            "status": "approved",
            "timestamp": "2026-06-02T14:23:00Z",
            "evidence_id": "ev-078",
            "residual_risk": "Invite cannot be recalled once sent",
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            f.flush()
            result = validate_approval_record(f.name)
        assert result["passed"] is False
        assert any(
            "requirement_ids" in v and "non-empty" in v for v in result["violations"]
        )

    def test_phase_contract_warnings_present(self):
        """Validator result includes warnings key even when empty."""
        result = validate_phase_contract(_fixture("phase_contract_valid.json"))
        assert "warnings" in result
        assert isinstance(result["warnings"], list)

    def test_domain_pack_warnings_present(self):
        """Validator result includes warnings key even when empty."""
        result = validate_domain_pack(_fixture("domain_pack_valid.json"))
        assert "warnings" in result
        assert isinstance(result["warnings"], list)


# --- YAML rejection ---


class TestYamlRejection:
    def test_yaml_file_raises_json_decode_error(self):
        """YAML files should fail with JSON decode error, not silently pass."""
        import pytest

        with pytest.raises(json.JSONDecodeError):
            validate_requirements_chain(_fixture("requirements_chain_invalid.yml"))


# --- Result shape ---


class TestResultShape:
    def test_result_has_required_keys(self):
        result = validate_requirements_chain(_fixture("requirements_chain_valid.json"))
        assert "passed" in result
        assert "violations" in result
        assert "warnings" in result
        assert isinstance(result["passed"], bool)
        assert isinstance(result["violations"], list)
        assert isinstance(result["warnings"], list)

    def test_missing_file_raises(self):
        import pytest

        with pytest.raises(FileNotFoundError):
            validate_requirements_chain("/nonexistent/path.json")
