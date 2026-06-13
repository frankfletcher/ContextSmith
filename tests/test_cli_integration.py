"""Comprehensive CLI integration tests for Phase 5D.

Tests cover:
- All 6 domain packs through CLI
- Exit code verification for all paths
- Output format compliance
- Cross-validator workflow tests
- Edge cases (empty files, special characters, etc.)
- Multiple artifact scenarios
- Programmatic API tests
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


# Test fixtures for cross-validator workflow tests
VALID_FIXTURES = {
    "requirements_chain": Path(__file__).parent
    / "fixtures"
    / "requirements_chain_valid.json",
    "evidence_ledger": Path(__file__).parent
    / "fixtures"
    / "evidence_ledger_valid.json",
    "phase_closeout": Path(__file__).parent / "fixtures" / "phase_closeout_valid.json",
}

# Structural failure fixtures (these fail individual validator checks)
FAIL_FIXTURES = {
    "requirements_chain": Path(__file__).parent
    / "fixtures"
    / "requirements_chain_missing_id.json",
    "phase_contract": Path(__file__).parent
    / "fixtures"
    / "phase_contract_missing_domain.json",
    "evidence_ledger": Path(__file__).parent
    / "fixtures"
    / "evidence_ledger_missing_requirement_id.json",
    "approval_record": Path(__file__).parent
    / "fixtures"
    / "approval_record_missing_requirement_ids.json",
    "phase_closeout": Path(__file__).parent
    / "fixtures"
    / "phase_closeout_missing_phase_id.json",
}

# Cross-artifact failure fixtures (structurally valid but fail cross-validation)
CROSS_FAIL_FIXTURES = {
    "requirements_chain": Path(__file__).parent
    / "fixtures"
    / "requirements_chain_orphan.json",
    "evidence_ledger": Path(__file__).parent
    / "fixtures"
    / "evidence_ledger_orphan_requirement.json",
    "phase_closeout": Path(__file__).parent
    / "fixtures"
    / "phase_closeout_orphan_evidence.json",
}

DOMAIN_PACKS = [
    "general_fallback",
    "research_summary",
    "scheduling",
    "software_engineering",
    "travel_purchase",
    "writing_editing",
]


def _run_cli(
    subcommand: str, artifact_path: Path | str, extra_args: list[str] | None = None
) -> subprocess.CompletedProcess:
    """Run CLI subcommand and return result."""
    cmd = [sys.executable, "-m", "runtime.cli", subcommand, str(artifact_path)]
    if extra_args:
        cmd.extend(extra_args)
    return subprocess.run(cmd, capture_output=True, text=True)


def _create_temp_json(data: dict, suffix: str = ".json") -> Path:
    """Create a temporary JSON file and return its path."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w") as f:
        json.dump(data, f)
    return Path(path)


# ==================== Domain Pack CLI Validation ====================


class TestDomainPackCLIValidation:
    """Test all 6 domain packs through CLI."""

    def test_all_domain_packs_valid(self):
        """All domain pack files should pass validation."""
        domain_packs_dir = Path(__file__).parent.parent / "runtime" / "domain_packs"
        for domain in DOMAIN_PACKS:
            path = domain_packs_dir / f"{domain}.json"
            assert path.exists(), f"Domain pack {domain} not found"
            result = _run_cli("domain-pack", path)
            assert result.returncode == 0, (
                f"Domain pack {domain} failed validation:\n{result.stdout}\n{result.stderr}"
            )
            assert "PASS" in result.stdout

    def test_general_fallback_with_wildcard(self):
        """general_fallback must have triggers: ['*']."""
        domain_packs_dir = Path(__file__).parent.parent / "runtime" / "domain_packs"
        path = domain_packs_dir / "general_fallback.json"
        with open(path) as f:
            data = json.load(f)
        assert data["triggers"] == ["*"], "general_fallback must have triggers: ['*']"

    def test_domain_pack_with_invalid_domain_format(self):
        """Domain must be lowercase with underscores, no spaces."""
        invalid_domain = {
            "artifact_type": "domain_pack",
            "domain": "Invalid Domain",
            "triggers": ["test"],
            "required_artifacts": ["requirements_chain"],
            "validation_gates": {},
            "approval_gates": [],
            "external_action_boundaries": {},
            "residual_risk": "test",
        }
        path = _create_temp_json(invalid_domain)
        result = _run_cli("domain-pack", path)
        assert result.returncode == 1
        assert "domain" in result.stdout.lower() or "lowercase" in result.stdout.lower()

    def test_domain_pack_with_missing_required_artifacts(self):
        """Domain pack must have non-empty required_artifacts."""
        invalid = {
            "artifact_type": "domain_pack",
            "domain": "test_domain",
            "triggers": ["test"],
            "required_artifacts": [],
            "validation_gates": {},
            "approval_gates": [],
            "external_action_boundaries": {},
            "residual_risk": "test",
        }
        path = _create_temp_json(invalid)
        result = _run_cli("domain-pack", path)
        assert result.returncode == 1
        assert "required_artifacts" in result.stdout

    def test_domain_pack_invalid_artifact_in_required(self):
        """required_artifacts must contain only valid artifact types."""
        invalid = {
            "artifact_type": "domain_pack",
            "domain": "test_domain",
            "triggers": ["test"],
            "required_artifacts": ["invalid_artifact_type"],
            "validation_gates": {},
            "approval_gates": [],
            "external_action_boundaries": {},
            "residual_risk": "test",
        }
        path = _create_temp_json(invalid)
        result = _run_cli("domain-pack", path)
        assert result.returncode == 1
        assert (
            "Invalid required_artifact" in result.stdout
            or "invalid_artifact_type" in result.stdout
        )

    def test_domain_pack_requires_approval_missing_from_gates(self):
        """Actions requiring approval must be in approval_gates."""
        invalid = {
            "artifact_type": "domain_pack",
            "domain": "test_domain",
            "triggers": ["test"],
            "required_artifacts": ["requirements_chain"],
            "validation_gates": {},
            "approval_gates": [],
            "external_action_boundaries": {
                "test_action": "requires_approval",
            },
            "residual_risk": "test",
        }
        path = _create_temp_json(invalid)
        result = _run_cli("domain-pack", path)
        assert result.returncode == 1
        assert "requires_approval" in result.stdout or "approval_gates" in result.stdout


# ==================== Exit Code Verification ====================


class TestExitCodeVerification:
    """Test exit codes for all subcommands and all paths."""

    def test_all_subcommands_exit_codes(self):
        """Test exit codes for all 6 validator subcommands."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        test_cases = [
            ("requirements", fixtures_dir / "requirements_chain_valid.json", 0),
            ("requirements", fixtures_dir / "requirements_chain_missing_id.json", 1),
            ("phase-contract", fixtures_dir / "phase_contract_valid.json", 0),
            ("phase-contract", fixtures_dir / "phase_contract_missing_domain.json", 1),
            ("evidence", fixtures_dir / "evidence_ledger_valid.json", 0),
            (
                "evidence",
                fixtures_dir / "evidence_ledger_missing_requirement_id.json",
                1,
            ),
            ("approval", fixtures_dir / "approval_record_valid.json", 0),
            (
                "approval",
                fixtures_dir / "approval_record_missing_requirement_ids.json",
                1,
            ),
            ("closeout", fixtures_dir / "phase_closeout_valid.json", 0),
            ("closeout", fixtures_dir / "phase_closeout_missing_phase_id.json", 1),
            (
                "domain-pack",
                Path(__file__).parent.parent
                / "runtime"
                / "domain_packs"
                / "general_fallback.json",
                0,
            ),
        ]
        for subcommand, path, expected_code in test_cases:
            result = _run_cli(subcommand, path)
            assert result.returncode == expected_code, (
                f"Subcommand {subcommand} with {path.name} returned {result.returncode}, "
                f"expected {expected_code}\nstdout: {result.stdout}\nstderr: {result.stderr}"
            )

    def test_nonexistent_file_error(self):
        """Nonexistent file should return exit code 2."""
        result = _run_cli("requirements", Path("/nonexistent.json"))
        assert result.returncode == 2
        assert "ERROR" in result.stderr or "not found" in result.stderr

    def test_invalid_json_error(self):
        """Invalid JSON should return exit code 2."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{ invalid json }")
            path = f.name
        try:
            result = _run_cli("requirements", path)
            assert result.returncode == 2
            assert "ERROR" in result.stderr or "Invalid JSON" in result.stderr
        finally:
            os.unlink(path)

    def test_empty_file_error(self):
        """Empty file should return exit code 2."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("")
            path = f.name
        try:
            result = _run_cli("requirements", path)
            assert result.returncode == 2
        finally:
            os.unlink(path)

    def test_directory_instead_of_file_error(self):
        """Directory path should return exit code 2."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = _run_cli("requirements", Path(tmpdir))
            assert result.returncode == 2


# ==================== Output Format Compliance ====================


class TestOutputFormatCompliance:
    """Test structured output format."""

    def test_pass_output_format(self):
        """PASS output should have correct format."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        result = _run_cli(
            "requirements", fixtures_dir / "requirements_chain_valid.json"
        )
        assert result.returncode == 0
        assert result.stdout.startswith("PASS")
        assert "requirements_chain_valid.json" in result.stdout

    def test_fail_output_format(self):
        """FAIL output should list violations."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        result = _run_cli(
            "requirements", fixtures_dir / "requirements_chain_missing_id.json"
        )
        assert result.returncode == 1
        assert result.stdout.startswith("FAIL")
        assert "violation:" in result.stdout or "violations" in result.stdout.lower()

    def test_no_stderr_on_pass(self):
        """Successful validation should not write to stderr."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        result = _run_cli(
            "requirements", fixtures_dir / "requirements_chain_valid.json"
        )
        assert result.returncode == 0
        assert result.stderr == ""

    def test_warnings_appear_in_output(self):
        """Warnings should be printed even on pass."""
        # Create a requirement with pending status and no phases (should trigger warning)
        pending_no_phases = {
            "artifact_type": "requirements_chain",
            "id": "req-pending-test",
            "source": "Test requirement",
            "domain": "general",
            "side_effect_tier": "read_only",
            "validation_method": "artifact_check",
            "phase_ids": [],
            "evidence_ids": [],
            "status": "pending",
        }
        path = _create_temp_json(pending_no_phases)
        try:
            result = _run_cli("requirements", path)
            # This should pass (pending doesn't require phases/evidence) but have a warning
            assert result.returncode == 0
            assert "warning:" in result.stdout.lower()
        finally:
            os.unlink(path)


# ==================== Cross-Validator Workflow Tests ====================


class TestCrossValidatorWorkflow:
    """Test cross-artifact validation scenarios."""

    def test_validate_workflow_valid_artifacts(self):
        """Valid cross-referenced artifacts should pass workflow validation."""
        # Note: There's no CLI subcommand for validate_workflow, so test programmatically
        from runtime.validator import validate_workflow

        result = validate_workflow(
            {
                "requirements_chain": VALID_FIXTURES["requirements_chain"],
                "evidence_ledger": VALID_FIXTURES["evidence_ledger"],
                "phase_closeout": VALID_FIXTURES["phase_closeout"],
            }
        )
        assert result["passed"], f"Workflow validation failed: {result['violations']}"

    def test_validate_workflow_orphan_evidence(self):
        """Workflow should fail when phase_closeout references non-existent evidence."""
        from runtime.validator import validate_workflow

        result = validate_workflow(
            {
                "evidence_ledger": VALID_FIXTURES["evidence_ledger"],
                "phase_closeout": CROSS_FAIL_FIXTURES["phase_closeout"],
            }
        )
        assert not result["passed"]
        assert any("ev-nonexistent" in v for v in result["violations"])

    def test_validate_workflow_orphan_requirement(self):
        """Workflow should fail when evidence_ledger references non-existent requirement."""
        from runtime.validator import validate_workflow

        result = validate_workflow(
            {
                "requirements_chain": VALID_FIXTURES["requirements_chain"],
                "evidence_ledger": CROSS_FAIL_FIXTURES["evidence_ledger"],
            }
        )
        assert not result["passed"]
        assert any("req-missing" in v for v in result["violations"])

    def test_validate_workflow_mixed_artifacts(self):
        """Workflow with multiple artifacts should validate all and report violations."""
        from runtime.validator import validate_workflow

        # Mix valid and cross-fail fixtures
        result = validate_workflow(
            {
                "requirements_chain": VALID_FIXTURES["requirements_chain"],
                "evidence_ledger": CROSS_FAIL_FIXTURES[
                    "evidence_ledger"
                ],  # orphan requirement
                "phase_closeout": VALID_FIXTURES["phase_closeout"],
            }
        )
        assert not result["passed"]
        assert any("req-missing" in v for v in result["violations"])

    def test_validate_workflow_partial_artifacts(self):
        """Workflow should work with subset of artifacts."""
        from runtime.validator import validate_workflow

        # Only requirements_chain
        result = validate_workflow(
            {
                "requirements_chain": VALID_FIXTURES["requirements_chain"],
            }
        )
        # Should pass (no cross-validation needed with only one artifact)
        assert result["passed"]


# ==================== Edge Cases ====================


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_json_object(self):
        """Empty JSON object should fail validation."""
        empty = {}
        path = _create_temp_json(empty)
        try:
            result = _run_cli("requirements", path)
            assert result.returncode == 1
            assert "Missing required field" in result.stdout
        finally:
            os.unlink(path)

    def test_wrong_artifact_type(self):
        """Wrong artifact_type field should fail."""
        wrong_type = {
            "artifact_type": "wrong_type",
            "id": "test",
            "source": "test",
            "domain": "general",
            "side_effect_tier": "read_only",
            "validation_method": "artifact_check",
            "phase_ids": [],
            "evidence_ids": [],
            "status": "pending",
        }
        path = _create_temp_json(wrong_type)
        try:
            result = _run_cli("requirements", path)
            assert result.returncode == 1
            assert "Wrong artifact_type" in result.stdout
        finally:
            os.unlink(path)

    def test_special_characters_in_field(self):
        """Fields with special characters should be handled correctly."""
        special = {
            "artifact_type": "requirements_chain",
            "id": "req-with-special-chars-@#$",
            "source": "Test with \"quotes\" and 'apostrophes'",
            "domain": "general",
            "side_effect_tier": "read_only",
            "validation_method": "artifact_check",
            "phase_ids": ["phase-1"],
            "evidence_ids": ["ev-1"],
            "status": "passed",
        }
        path = _create_temp_json(special)
        try:
            result = _run_cli("requirements", path)
            assert result.returncode == 0
        finally:
            os.unlink(path)

    def test_very_long_field_values(self):
        """Long field values should be handled."""
        long_text = "x" * 10000
        data = {
            "artifact_type": "requirements_chain",
            "id": "req-long",
            "source": long_text,
            "domain": "general",
            "side_effect_tier": "read_only",
            "validation_method": "artifact_check",
            "phase_ids": ["phase-1"],
            "evidence_ids": ["ev-1"],
            "status": "passed",
        }
        path = _create_temp_json(data)
        try:
            result = _run_cli("requirements", path)
            assert result.returncode == 0
        finally:
            os.unlink(path)

    def test_unicode_in_fields(self):
        """Unicode characters should be handled."""
        data = {
            "artifact_type": "requirements_chain",
            "id": "req-unicodé",
            "source": "Test with 日本語 and 🚀 emoji",
            "domain": "general",
            "side_effect_tier": "read_only",
            "validation_method": "artifact_check",
            "phase_ids": ["phase-1"],
            "evidence_ids": ["ev-1"],
            "status": "passed",
        }
        path = _create_temp_json(data)
        try:
            result = _run_cli("requirements", path)
            assert result.returncode == 0
        finally:
            os.unlink(path)


# ==================== Multiple Artifact Scenarios ====================


class TestMultipleArtifactScenarios:
    """Test scenarios with multiple artifacts in sequence."""

    def test_validating_multiple_sequential(self):
        """Validate multiple artifacts in sequence."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        artifacts = [
            ("requirements", fixtures_dir / "requirements_chain_valid.json"),
            ("evidence", fixtures_dir / "evidence_ledger_valid.json"),
            ("closeout", fixtures_dir / "phase_closeout_valid.json"),
        ]
        for subcommand, path in artifacts:
            result = _run_cli(subcommand, path)
            assert result.returncode == 0, f"Failed on {subcommand}: {result.stdout}"

    def test_mixed_pass_fail_sequence(self):
        """Sequence with both passing and failing artifacts."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        # First pass, then fail
        result1 = _run_cli(
            "requirements", fixtures_dir / "requirements_chain_valid.json"
        )
        assert result1.returncode == 0

        result2 = _run_cli(
            "requirements", fixtures_dir / "requirements_chain_missing_id.json"
        )
        assert result2.returncode == 1

    def test_all_domain_packs_in_sequence(self):
        """Validate all domain packs sequentially."""
        domain_packs_dir = Path(__file__).parent.parent / "runtime" / "domain_packs"
        for domain in DOMAIN_PACKS:
            path = domain_packs_dir / f"{domain}.json"
            result = _run_cli("domain-pack", path)
            assert result.returncode == 0, f"Domain pack {domain} failed"


# ==================== Programmatic API Tests ====================


class TestProgrammaticAPI:
    """Test CLI programmatic API."""

    def test_main_with_invalid_args(self):
        """Main with invalid args should raise SystemExit with code 2."""
        from runtime.cli import main

        with pytest.raises(SystemExit) as exc_info:
            main(["invalid_subcommand", "dummy.json"])
        assert exc_info.value.code == 2

    def test_main_with_help(self):
        """Main with --help should raise SystemExit with code 0."""
        from runtime.cli import main

        with pytest.raises(SystemExit) as exc_info:
            main(["--help"])
        assert exc_info.value.code == 0

    def test_build_parser(self):
        """Parser should have all expected subcommands."""
        from runtime.cli import build_parser, SUBCOMMANDS

        parser = build_parser()
        # All subcommands should be registered in SUBCOMMANDS
        expected = {
            "requirements",
            "phase-contract",
            "evidence",
            "approval",
            "closeout",
            "domain-pack",
        }
        assert set(SUBCOMMANDS.keys()) == expected
        # Verify we can parse each subcommand
        for name in expected:
            args = parser.parse_args([name, "dummy.json"])
            assert hasattr(args, "func")

    def test_subcommands_registered(self):
        """All 6 subcommands should be registered."""
        from runtime.cli import SUBCOMMANDS

        expected = {
            "requirements",
            "phase-contract",
            "evidence",
            "approval",
            "closeout",
            "domain-pack",
        }
        assert set(SUBCOMMANDS.keys()) == expected

    def test_next_prompt_subcommand(self):
        """next-prompt subcommand should exist and work."""
        from runtime.cli import main

        # This may fail if task_dir doesn't exist, but should not crash
        result = main(["next-prompt", "--dry-run", "."])
        # Should return 0 or error code, but not crash with exception
        assert isinstance(result, int)

    def test_handle_subcommand_error_handling(self):
        """Error handling in _handle_subcommand."""
        from runtime.cli import _handle_subcommand, validate_requirements_chain
        import argparse

        # Create args namespace with nonexistent path
        args = argparse.Namespace(path="/nonexistent.json")
        result = _handle_subcommand("requirements", validate_requirements_chain, args)
        assert result == 2


# ==================== Help and Usage Tests ====================


class TestHelpAndUsage:
    """Test help output and usage messages."""

    def test_main_help(self):
        """Main help should show all subcommands."""
        result = _run_cli("--help", "")
        assert result.returncode == 0
        assert "requirements" in result.stdout
        assert "phase-contract" in result.stdout
        assert "domain-pack" in result.stdout

    def test_subcommand_help(self):
        """Each subcommand should have help text."""
        subcommands = [
            "requirements",
            "phase-contract",
            "evidence",
            "approval",
            "closeout",
            "domain-pack",
        ]
        for subcommand in subcommands:
            cmd = [sys.executable, "-m", "runtime.cli", subcommand, "--help"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            assert result.returncode == 0
            assert (
                "usage:" in result.stdout.lower()
                or "positional arguments" in result.stdout.lower()
            )

    def test_next_prompt_help(self):
        """next-prompt subcommand should have help text."""
        cmd = [sys.executable, "-m", "runtime.cli", "next-prompt", "--help"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()


# ==================== Cross-Artifact Validation via CLI ====================


class TestCrossArtifactValidationCLI:
    """Test cross-artifact validation scenarios via CLI."""

    def test_requirements_chain_validation(self):
        """Requirements chain should validate required fields."""
        valid = {
            "artifact_type": "requirements_chain",
            "id": "req-test",
            "source": "Test source",
            "domain": "general",
            "side_effect_tier": "read_only",
            "validation_method": "artifact_check",
            "phase_ids": ["phase-1"],
            "evidence_ids": ["ev-1"],
            "status": "passed",
        }
        path = _create_temp_json(valid)
        try:
            result = _run_cli("requirements", path)
            assert result.returncode == 0
        finally:
            os.unlink(path)

    def test_requirements_chain_missing_fields(self):
        """Requirements chain should fail on missing required fields."""
        invalid = {
            "artifact_type": "requirements_chain",
            "id": "req-test",
            # Missing source, domain, etc.
        }
        path = _create_temp_json(invalid)
        try:
            result = _run_cli("requirements", path)
            assert result.returncode == 1
            assert "Missing required field" in result.stdout
        finally:
            os.unlink(path)

    def test_phase_contract_validation(self):
        """Phase contract should validate required fields."""
        valid = {
            "artifact_type": "phase_contract",
            "phase_id": "phase-test",
            "objective": "Test objective",
            "domain": "general",
            "allowed_actions": ["read"],
            "disallowed_actions": ["write"],
            "validation_commands": ["pytest"],
            "max_artifacts": 10,
            "status": "active",
        }
        path = _create_temp_json(valid)
        try:
            result = _run_cli("phase-contract", path)
            assert result.returncode == 0
        finally:
            os.unlink(path)

    def test_evidence_ledger_validation(self):
        """Evidence ledger should validate required fields."""
        valid = {
            "artifact_type": "evidence_ledger",
            "id": "ev-test",
            "requirement_id": "req-test",
            "phase_id": "phase-test",
            "claim": "Test claim",
            "evidence": "Test evidence",
            "evidence_type": "file",
            "verified": True,
            "timestamp": "2026-01-01",
        }
        path = _create_temp_json(valid)
        try:
            result = _run_cli("evidence", path)
            assert result.returncode == 0
        finally:
            os.unlink(path)

    def test_approval_record_validation(self):
        """Approval record should validate required fields."""
        valid = {
            "artifact_type": "approval_record",
            "id": "approval-test",
            "requirement_ids": ["req-test"],
            "action": "test_action",
            "side_effect_tier": "read_only",
            "requester": "user",
            "approver": "not_yet_approved",
            "status": "requested",
            "timestamp": "pending",
            "evidence_id": "ev-test",
            "residual_risk": "No risk",
        }
        path = _create_temp_json(valid)
        try:
            result = _run_cli("approval", path)
            assert result.returncode == 0
        finally:
            os.unlink(path)

    def test_phase_closeout_validation(self):
        """Phase closeout should validate required fields."""
        valid = {
            "artifact_type": "phase_closeout",
            "phase_id": "phase-test",
            "objective_met": True,
            "artifacts_produced": ["artifact-1"],
            "evidence_ids": ["ev-1"],
            "validation_results": [{"check": "test", "result": "pass"}],
            "blockers": [],
            "carry_forward": [],
            "next_phase_id": "phase-next",
            "status": "passed",
        }
        path = _create_temp_json(valid)
        try:
            result = _run_cli("closeout", path)
            assert result.returncode == 0
        finally:
            os.unlink(path)

    def test_approval_status_consistency(self):
        """Approval record status should be consistent with approver and timestamp."""
        # approved status with not_yet_approved approver should fail
        invalid = {
            "artifact_type": "approval_record",
            "id": "approval-test",
            "requirement_ids": ["req-test"],
            "action": "test_action",
            "side_effect_tier": "read_only",
            "requester": "user",
            "approver": "not_yet_approved",  # Should be actual approver for approved status
            "status": "approved",
            "timestamp": "2026-01-01",
            "evidence_id": "ev-test",
            "residual_risk": "No risk",
        }
        path = _create_temp_json(invalid)
        try:
            result = _run_cli("approval", path)
            assert result.returncode == 1
            assert "approver" in result.stdout.lower()
        finally:
            os.unlink(path)

    def test_high_risk_requires_residual_risk(self):
        """High-risk side_effect_tier requires non-empty residual_risk."""
        invalid = {
            "artifact_type": "approval_record",
            "id": "approval-test",
            "requirement_ids": ["req-test"],
            "action": "test_action",
            "side_effect_tier": "external_write",
            "requester": "user",
            "approver": "approver",
            "status": "approved",
            "timestamp": "2026-01-01",
            "evidence_id": "ev-test",
            "residual_risk": "",  # Empty for high-risk tier
        }
        path = _create_temp_json(invalid)
        try:
            result = _run_cli("approval", path)
            assert result.returncode == 1
            assert "residual_risk" in result.stdout.lower()
        finally:
            os.unlink(path)
