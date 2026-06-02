"""ContextSmith runtime validator core.

Deterministic structural validators for universal artifact types.
Each validator checks required fields, status enumerations, and
domain-neutral structural rules. Returns:
    {"passed": bool, "violations": list[str], "warnings": list[str]}
"""

import json
from pathlib import Path


# --- Shared constants ---

_ARTIFACT_TYPES = frozenset([
    "requirements_chain", "phase_contract", "domain_pack",
    "evidence_ledger", "approval_record", "phase_closeout",
])

_REQUIREMENT_STATUSES = frozenset(["pending", "passed", "blocked", "waived_by_user"])
_PHASE_STATUSES = frozenset(["active", "completed", "blocked", "cancelled"])
_APPROVAL_STATUSES = frozenset(["not_required", "requested", "approved", "denied", "waived_by_user"])
_CLOSEOUT_STATUSES = frozenset(["passed", "failed", "blocked", "waived_by_user"])
_SIDE_EFFECT_TIERS = frozenset([
    "read_only", "local_write", "external_read", "external_write", "irreversible",
])
_VALIDATION_METHODS = frozenset([
    "command", "artifact_check", "evidence_review", "user_confirmation", "none",
])
_EVIDENCE_TYPES = frozenset([
    "file", "command_output", "artifact", "observation", "user_confirmation",
])
_CHECK_TYPES = frozenset([
    "field_presence", "value_check", "command", "artifact_check", "user_confirmation",
])
_BOUNDARY_VALUES = frozenset(["allowed", "requires_approval", "blocked"])

# --- Helpers ---


def _load_json(path: str | Path) -> dict:
    """Load and parse a JSON file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Artifact file not found: {p}")
    if not p.is_file():
        raise ValueError(f"Not a file: {p}")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _result(*, passed: bool = True, violations: tuple[str, ...] = (),
            warnings: tuple[str, ...] = ()) -> dict:
    return {"passed": passed, "violations": list(violations), "warnings": list(warnings)}


def _check_required(data: dict, artifact_type: str, fields: list[str]) -> list[str]:
    """Return violations for missing required fields."""
    return [f"Missing required field: {f}" for f in fields if f not in data]


def _check_enum(value: str, allowed: frozenset[str], field: str) -> list[str]:
    """Return a violation if value is not in allowed set."""
    if value not in allowed:
        return [f"Invalid {field}: {value!r}. Must be one of {sorted(allowed)}"]
    return []


def _check_non_empty_string(data: dict, field: str) -> list[str]:
    if field not in data:
        return []
    value = data[field]
    if not isinstance(value, str) or not value.strip():
        return [f"Field '{field}' must be a non-empty string"]
    return []


def _check_string_list(data: dict, field: str, *, non_empty: bool = False) -> list[str]:
    if field not in data:
        return []
    value = data[field]
    if not isinstance(value, list):
        return [f"Field '{field}' must be a list of strings"]
    if non_empty and not value:
        return [f"Field '{field}' must be a non-empty list of strings"]
    if any(not isinstance(item, str) or not item.strip() for item in value):
        return [f"Field '{field}' must be a list of non-empty strings"]
    return []


def _check_bool(data: dict, field: str) -> list[str]:
    if field in data and not isinstance(data[field], bool):
        return [f"Field '{field}' must be a boolean"]
    return []


def _check_dict(data: dict, field: str) -> list[str]:
    if field in data and not isinstance(data[field], dict):
        return [f"Field '{field}' must be an object"]
    return []


# --- Validators ---


def validate_requirements_chain(path: str | Path) -> dict:
    """Validate a requirements_chain artifact."""
    data = _load_json(path)
    violations: list[str] = []

    violations.extend(_check_required(data, "requirements_chain", [
        "id", "source", "domain", "side_effect_tier", "validation_method",
        "phase_ids", "evidence_ids", "status",
    ]))

    if "artifact_type" in data and data["artifact_type"] != "requirements_chain":
        violations.append(f"Wrong artifact_type: {data['artifact_type']!r}")

    for field in ("id", "source", "domain"):
        violations.extend(_check_non_empty_string(data, field))

    violations.extend(_check_string_list(data, "phase_ids"))
    violations.extend(_check_string_list(data, "evidence_ids"))

    if "side_effect_tier" in data:
        violations.extend(_check_enum(data["side_effect_tier"], _SIDE_EFFECT_TIERS, "side_effect_tier"))

    if "validation_method" in data:
        violations.extend(_check_enum(data["validation_method"], _VALIDATION_METHODS, "validation_method"))

    if "status" in data:
        violations.extend(_check_enum(data["status"], _REQUIREMENT_STATUSES, "status"))

    # Rule 7: passed status requires at least one phase_id and one evidence_id
    if data.get("status") == "passed":
        if not data.get("phase_ids"):
            violations.append("Status 'passed' requires at least one phase_id")
        if not data.get("evidence_ids"):
            violations.append("Status 'passed' requires at least one evidence_id")

    warnings: list[str] = []
    if data.get("status") == "pending" and not data.get("phase_ids"):
        warnings.append("Requirement is 'pending' with no phases assigned yet")

    return _result(passed=len(violations) == 0, violations=violations, warnings=tuple(warnings))


def validate_phase_contract(path: str | Path) -> dict:
    """Validate a phase_contract artifact."""
    data = _load_json(path)
    violations: list[str] = []

    violations.extend(_check_required(data, "phase_contract", [
        "phase_id", "objective", "domain", "allowed_actions", "disallowed_actions",
        "validation_commands", "max_artifacts", "status",
    ]))

    if "artifact_type" in data and data["artifact_type"] != "phase_contract":
        violations.append(f"Wrong artifact_type: {data['artifact_type']!r}")

    for field in ("phase_id", "objective", "domain"):
        violations.extend(_check_non_empty_string(data, field))

    violations.extend(_check_string_list(data, "allowed_actions"))
    violations.extend(_check_string_list(data, "disallowed_actions"))
    violations.extend(_check_string_list(data, "validation_commands"))

    if "max_artifacts" in data and not isinstance(data["max_artifacts"], int):
        violations.append("Field 'max_artifacts' must be an integer")

    if "status" in data:
        violations.extend(_check_enum(data["status"], _PHASE_STATUSES, "status"))

    return _result(passed=len(violations) == 0, violations=violations)


def validate_evidence_ledger(path: str | Path) -> dict:
    """Validate an evidence_ledger artifact."""
    data = _load_json(path)
    violations: list[str] = []

    violations.extend(_check_required(data, "evidence_ledger", [
        "id", "requirement_id", "phase_id", "claim", "evidence",
        "evidence_type", "verified", "timestamp",
    ]))

    if "artifact_type" in data and data["artifact_type"] != "evidence_ledger":
        violations.append(f"Wrong artifact_type: {data['artifact_type']!r}")

    for field in ("id", "requirement_id", "phase_id", "claim", "evidence", "timestamp"):
        violations.extend(_check_non_empty_string(data, field))

    if "evidence_type" in data:
        violations.extend(_check_enum(data["evidence_type"], _EVIDENCE_TYPES, "evidence_type"))

    violations.extend(_check_bool(data, "verified"))

    return _result(passed=len(violations) == 0, violations=violations)


def validate_approval_record(path: str | Path) -> dict:
    """Validate an approval_record artifact."""
    data = _load_json(path)
    violations: list[str] = []

    violations.extend(_check_required(data, "approval_record", [
        "id", "requirement_ids", "action", "side_effect_tier", "requester",
        "approver", "status", "timestamp", "evidence_id", "residual_risk",
    ]))

    if "artifact_type" in data and data["artifact_type"] != "approval_record":
        violations.append(f"Wrong artifact_type: {data['artifact_type']!r}")

    for field in ("id", "action", "requester", "approver", "timestamp", "evidence_id", "residual_risk"):
        violations.extend(_check_non_empty_string(data, field))

    violations.extend(_check_string_list(data, "requirement_ids", non_empty=True))

    if "side_effect_tier" in data:
        violations.extend(_check_enum(data["side_effect_tier"], _SIDE_EFFECT_TIERS, "side_effect_tier"))

    if "status" in data:
        violations.extend(_check_enum(data["status"], _APPROVAL_STATUSES, "status"))

    # Status/approver/timestamp consistency rules
    status = data.get("status")
    approver = data.get("approver")
    timestamp = data.get("timestamp")

    if status in ("approved", "denied"):
        if approver == "not_yet_approved":
            violations.append(
                f"Status '{status}' requires an approver (cannot be 'not_yet_approved')")
        if timestamp == "pending":
            violations.append(
                f"Status '{status}' requires a timestamp (cannot be 'pending')")

    if status == "requested":
        if approver != "not_yet_approved":
            violations.append("Status 'requested' requires approver to be 'not_yet_approved'")
        if timestamp != "pending":
            violations.append("Status 'requested' requires timestamp to be 'pending'")

    # Rule 10: external_write or irreversible requires non-empty residual_risk
    if data.get("side_effect_tier") in ("external_write", "irreversible"):
        risk = data.get("residual_risk")
        if not risk or (isinstance(risk, str) and not risk.strip()):
            violations.append(
                "High-risk side_effect_tier requires non-empty 'residual_risk'")

    return _result(passed=len(violations) == 0, violations=violations)


def validate_phase_closeout(path: str | Path) -> dict:
    """Validate a phase_closeout artifact."""
    data = _load_json(path)
    violations: list[str] = []

    violations.extend(_check_required(data, "phase_closeout", [
        "phase_id", "objective_met", "artifacts_produced", "evidence_ids",
        "validation_results", "blockers", "carry_forward", "next_phase_id", "status",
    ]))

    if "artifact_type" in data and data["artifact_type"] != "phase_closeout":
        violations.append(f"Wrong artifact_type: {data['artifact_type']!r}")

    violations.extend(_check_non_empty_string(data, "phase_id"))
    violations.extend(_check_string_list(data, "artifacts_produced"))
    violations.extend(_check_string_list(data, "evidence_ids"))
    violations.extend(_check_string_list(data, "blockers"))
    violations.extend(_check_string_list(data, "carry_forward"))
    violations.extend(_check_non_empty_string(data, "next_phase_id"))

    if "validation_results" in data and not isinstance(data["validation_results"], list):
        violations.append("Field 'validation_results' must be a list")

    if "status" in data:
        violations.extend(_check_enum(data["status"], _CLOSEOUT_STATUSES, "status"))

    violations.extend(_check_bool(data, "objective_met"))

    return _result(passed=len(violations) == 0, violations=violations)


def validate_domain_pack(path: str | Path) -> dict:
    """Validate a domain_pack artifact."""
    data = _load_json(path)
    violations: list[str] = []

    violations.extend(_check_required(data, "domain_pack", [
        "domain", "triggers", "required_artifacts", "validation_gates",
        "approval_gates", "external_action_boundaries", "residual_risk",
    ]))

    if "artifact_type" in data and data["artifact_type"] != "domain_pack":
        violations.append(f"Wrong artifact_type: {data['artifact_type']!r}")

    # Domain name format
    domain = data.get("domain", "")
    if domain and (not isinstance(domain, str) or not domain.islower() or " " in domain):
        violations.append("Field 'domain' must be a non-empty lowercase string with underscores")

    violations.extend(_check_string_list(data, "triggers", non_empty=True))
    violations.extend(_check_string_list(data, "required_artifacts", non_empty=True))
    violations.extend(_check_string_list(data, "approval_gates"))
    violations.extend(_check_non_empty_string(data, "residual_risk"))
    violations.extend(_check_dict(data, "validation_gates"))
    violations.extend(_check_dict(data, "external_action_boundaries"))

    # Rule 3: required_artifacts must only contain vocabulary types
    ra = data.get("required_artifacts")
    if ra is not None and isinstance(ra, list):
        for art in ra:
            if art not in _ARTIFACT_TYPES:
                violations.append(
                    f"Invalid required_artifact: {art!r}. Must be one of {sorted(_ARTIFACT_TYPES)}")

    # validation_gates structure
    vg = data.get("validation_gates")
    if vg is not None and isinstance(vg, dict):
        for gate_name, gate in vg.items():
            if not isinstance(gate, dict):
                violations.append(f"validation_gates['{gate_name}'] must be an object")
                continue
            for req_field in ("description", "required", "check_type"):
                if req_field not in gate:
                    violations.append(
                        f"validation_gates['{gate_name}'] missing '{req_field}'")
            if "description" in gate and (
                not isinstance(gate["description"], str) or not gate["description"].strip()
            ):
                violations.append(
                    f"validation_gates['{gate_name}'].description must be a non-empty string")
            if "required" in gate and not isinstance(gate["required"], bool):
                violations.append(
                    f"validation_gates['{gate_name}'].required must be a boolean")
            if "check_type" in gate:
                violations.extend(
                    _check_enum(gate["check_type"], _CHECK_TYPES,
                                f"validation_gates['{gate_name}'].check_type"))

    # external_action_boundaries values
    eab = data.get("external_action_boundaries")
    if eab is not None and isinstance(eab, dict):
        for action, level in eab.items():
            violations.extend(
                _check_enum(level, _BOUNDARY_VALUES,
                            f"external_action_boundaries['{action}']"))

    # Rule 9: requires_approval actions must have approval_gates entries
    if eab is not None and isinstance(eab, dict) and "approval_gates" in data:
        approval_gates = data.get("approval_gates", [])
        for action, level in eab.items():
            if level == "requires_approval" and action not in approval_gates:
                violations.append(
                    f"Action '{action}' is 'requires_approval' but missing from approval_gates")

    # Rule 10: general_fallback must match unknown domains with wildcard trigger
    if data.get("domain") == "general_fallback" and data.get("triggers") != ["*"]:
        violations.append("general_fallback domain pack must have triggers: ['*']")

    return _result(passed=len(violations) == 0, violations=violations)


def validate_workflow(artifact_paths: dict[str, str | Path]) -> dict:
    """Validate cross-artifact consistency.

    artifact_paths maps artifact type names to file paths, e.g.:
        {
            "requirements_chain": "path/to/requirements.json",
            "evidence_ledger": "path/to/evidence.json",
            "phase_closeout": "path/to/closeout.json",
        }
    """
    violations: list[str] = []
    warnings: list[str] = []

    # First run structural validators so workflow gates cannot pass invalid artifacts.
    validators = {
        "requirements_chain": validate_requirements_chain,
        "phase_contract": validate_phase_contract,
        "evidence_ledger": validate_evidence_ledger,
        "approval_record": validate_approval_record,
        "phase_closeout": validate_phase_closeout,
        "domain_pack": validate_domain_pack,
    }

    for artifact_type, validator in validators.items():
        if artifact_type not in artifact_paths:
            continue
        try:
            result = validator(artifact_paths[artifact_type])
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            violations.append(f"{artifact_type}: {e}")
            continue
        violations.extend(f"{artifact_type}: {v}" for v in result["violations"])
        warnings.extend(f"{artifact_type}: {w}" for w in result["warnings"])

    # Load available artifacts for cross-reference checks.
    rc_data = None
    el_data = None
    pc_data = None

    if "requirements_chain" in artifact_paths:
        try:
            rc_data = _load_json(artifact_paths["requirements_chain"])
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            violations.append(f"requirements_chain: {e}")

    if "evidence_ledger" in artifact_paths:
        try:
            el_data = _load_json(artifact_paths["evidence_ledger"])
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            violations.append(f"evidence_ledger: {e}")

    if "phase_closeout" in artifact_paths:
        try:
            pc_data = _load_json(artifact_paths["phase_closeout"])
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            violations.append(f"phase_closeout: {e}")

    # Build evidence ID set from evidence_ledger
    el_ids = set()
    if el_data is not None:
        if isinstance(el_data, list):
            for entry in el_data:
                if "id" in entry:
                    el_ids.add(entry["id"])
        elif "id" in el_data:
            el_ids.add(el_data["id"])

    # Build requirement ID set from requirements_chain
    rc_ids = set()
    if rc_data is not None:
        if isinstance(rc_data, list):
            for entry in rc_data:
                if "id" in entry:
                    rc_ids.add(entry["id"])
        elif "id" in rc_data:
            rc_ids.add(rc_data["id"])

    # Check phase_closeout evidence_ids reference valid ledger entries
    if pc_data is not None and el_ids is not None:
        pc_evidence_ids = pc_data.get("evidence_ids", [])
        if isinstance(pc_evidence_ids, list):
            for eid in pc_evidence_ids:
                if eid not in el_ids:
                    violations.append(
                        f"phase_closeout references evidence_id '{eid}' not found in evidence_ledger")

    # Check evidence_ledger requirement_id references valid requirements
    if el_data is not None and rc_ids is not None:
        if isinstance(el_data, list):
            for entry in el_data:
                rid = entry.get("requirement_id")
                if rid and rid not in rc_ids:
                    violations.append(
                        f"evidence_ledger '{entry.get('id', '?')}' references "
                        f"requirement_id '{rid}' not found in requirements_chain")
        elif "requirement_id" in el_data:
            rid = el_data["requirement_id"]
            if rid not in rc_ids:
                violations.append(
                    f"evidence_ledger '{el_data.get('id', '?')}' references "
                    f"requirement_id '{rid}' not found in requirements_chain")

    return _result(passed=len(violations) == 0, violations=violations, warnings=tuple(warnings))
