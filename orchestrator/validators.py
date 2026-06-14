"""File and state validators for orchestrator artifacts."""

from pathlib import Path

import yaml


def _extract_sections(content: str) -> list[str]:
    """Extract ATX-style section names from Markdown content.

    Returns section names without the "## " prefix.
    """
    sections = []
    for line in content.splitlines():
        if line.startswith("## "):
            sections.append(line[3:].strip())
    return sections


def validate_file_exists(path: Path) -> list[str]:
    """Check if file exists. Returns [] if exists, [error] if not."""
    if not path.exists():
        return [f"Missing required file: {path.name}"]
    return []


def validate_file_nonempty(path: Path) -> list[str]:
    """Check if file is non-empty. Returns [] if non-empty, [error] otherwise."""
    if not path.exists():
        return [f"Missing required file: {path.name}"]
    if path.stat().st_size == 0:
        return [f"File is empty: {path.name}"]
    return []


def validate_required_sections(path: Path, sections: list[str]) -> list[str]:
    """Check file has required sections. Returns [] if all present, [errors] if missing.

    Section detection uses ATX-style headings (## Section Name).
    """
    if not path.exists():
        return [f"Missing required file: {path.name}"]

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        return [f"File is empty: {path.name}"]

    found = _extract_sections(content)
    errors = []
    for section in sections:
        if section not in found:
            errors.append(f"Missing required section '{section}' in {path.name}")
    return errors


def validate_artifact(
    file_path: Path, required_sections: list[str] | None = None
) -> list[str]:
    """Check exists, non-empty, and sections. Returns list of errors."""
    if required_sections is None:
        required_sections = []

    errors = validate_file_nonempty(file_path)
    if errors:
        return errors

    if required_sections:
        section_errors = validate_required_sections(file_path, required_sections)
        errors.extend(section_errors)

    return errors


def validate_artifacts(
    state_dir: Path, expected_outputs: list[str], config: dict
) -> dict:
    """Validate all expected artifacts from a step contract.

    Args:
        state_dir: Directory containing task state files.
        expected_outputs: List of filenames to validate.
        config: Configuration dict, may contain "section_requirements"
                mapping filenames to lists of required section names.

    Returns:
        Dict with "passed", "failures", "files_checked", "files_passed".
    """
    section_requirements = config.get("section_requirements", {})

    failures = []
    files_checked = 0
    files_passed = 0

    for filename in expected_outputs:
        file_path = state_dir / filename
        required_sections = section_requirements.get(filename, [])
        errors = validate_artifact(file_path, required_sections)
        files_checked += 1
        if errors:
            failures.extend(errors)
        else:
            files_passed += 1

    return {
        "passed": len(failures) == 0,
        "failures": failures,
        "files_checked": files_checked,
        "files_passed": files_passed,
    }


_SCHEMAS_DIR = Path(__file__).parent.parent / "schemas"


def validate_schema(data: dict, schema_path: Path) -> list[str]:
    """Validate data against a JSON schema. Returns [] if valid, [errors] if not."""
    import json

    from jsonschema import SchemaError, ValidationError, validate

    if not schema_path.exists():
        return [f"Schema validation failed: schema file not found: {schema_path}"]

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"Schema validation failed: invalid schema JSON: {e}"]

    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        return [f"Schema validation failed: {e.message}"]
    except SchemaError as e:
        return [f"Schema validation failed: schema error: {e}"]

    return []


def validate_workflow_config(config_path: Path) -> list[str]:
    """Validate a workflow config YAML file against workflow_config.schema.json."""
    import yaml

    if not config_path.exists():
        return [f"Schema validation failed: config file not found: {config_path}"]

    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"Schema validation failed: invalid YAML: {e}"]

    if config is None:
        return ["Schema validation failed: empty config file"]

    schema_path = _SCHEMAS_DIR / "workflow_config.schema.json"
    return validate_schema(config, schema_path)


def validate_agent_config(config_path: Path) -> list[str]:
    """Validate an agent config YAML file against agent_config.schema.json."""
    import yaml

    if not config_path.exists():
        return [f"Schema validation failed: config file not found: {config_path}"]

    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"Schema validation failed: invalid YAML: {e}"]

    if config is None:
        return ["Schema validation failed: empty config file"]

    schema_path = _SCHEMAS_DIR / "agent_config.schema.json"
    return validate_schema(config, schema_path)


def _validate_checkpoint_version(data: dict) -> list[str]:
    """Check version field is a positive integer."""
    if "version" not in data:
        return []
    version = data["version"]
    if not isinstance(version, int) or version < 1:
        return [f"Invalid value for version: must be integer >= 1, got {version!r}"]
    return []


def _validate_checkpoint_config_ref(data: dict, config: dict) -> list[str]:
    """Cross-reference checkpoint phase/state against config phase_order and states."""
    errors = []
    states = config.get("states", {})
    phase_order = config.get("phase_order", [])
    current_phase = data.get("current_phase", "")
    current_state = data.get("current_state", "")

    if current_phase and phase_order and current_phase not in phase_order:
        errors.append(
            f"Invalid value for current_phase: '{current_phase}' not in phase_order"
        )
    if current_state and states:
        known_states = {s.get("state") for s in states.values() if isinstance(s, dict)}
        if current_state not in known_states:
            errors.append(
                f"Invalid value for current_state:"
                f" '{current_state}' not in known states"
            )
    return errors


def validate_checkpoint_file(
    checkpoint_path: Path, config: dict | None = None
) -> list[str]:
    """Validate a checkpoint JSON file against required structure.

    Reads the file from disk, parses JSON, checks required fields.

    Args:
        checkpoint_path: Path to checkpoint.json file.
        config: Optional workflow config dict. If provided with "states" or
                "phase_order", validates phase/state are known.

    Returns:
        List of error strings (empty = valid).
    """
    import json

    if not checkpoint_path.exists():
        return [
            f"Schema validation failed: checkpoint file not found: {checkpoint_path}"
        ]

    try:
        data = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"Schema validation failed: invalid checkpoint JSON: {e}"]

    _CHECKPOINT_REQUIRED = [
        "workflow_id",
        "version",
        "current_phase",
        "current_state",
        "last_updated",
    ]
    errors = [
        f"Missing required field: {f}" for f in _CHECKPOINT_REQUIRED if f not in data
    ]
    errors.extend(_validate_checkpoint_version(data))
    if config is not None:
        errors.extend(_validate_checkpoint_config_ref(data, config))
    return errors


def validate_append_only(
    file_path: Path, original_prefix: bytes, check_bytes: int = 512
) -> bool:
    """Check that a file starts with the same bytes as before modification.

    Used to verify that append-only files were appended to, not overwritten.
    Compares the first check_bytes of the current file against the snapshot.

    Args:
        file_path: Path to the file to check.
        original_prefix: The first N bytes of the file before modification.
        check_bytes: Number of bytes to compare (default 512).

    Returns:
        True if the file still starts with the original prefix, False if overwritten.
    """
    if not file_path.exists():
        return False
    current = file_path.read_bytes()[:check_bytes]
    return current.startswith(original_prefix[:check_bytes])


def load_artifact_schemas() -> dict:
    """Load artifact schemas from schemas/artifact_schemas.yaml.

    Returns:
        Dict with artifact schemas, or empty dict if file not found/invalid.
    """
    schema_path = _SCHEMAS_DIR / "artifact_schemas.yaml"
    if not schema_path.exists():
        return {}

    try:
        with open(schema_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("artifacts", {}) if data else {}
    except yaml.YAMLError, OSError:
        return {}


def validate_artifact_schema(
    file_path: Path, schema: dict, config_overrides: dict | None = None
) -> list[str]:
    """Validate a markdown artifact against its schema.

    Args:
        file_path: Path to the artifact file.
        schema: Artifact schema dict with required_sections, optional_sections, etc.
        config_overrides: Optional dict with per-file required section overrides.
            Populated from both section_requirements and artifact_schemas config keys.

    Returns:
        List of error strings (empty = valid).
    """
    if not file_path.exists():
        return [f"Missing required file: {file_path.name}"]

    content = file_path.read_text(encoding="utf-8")
    if not content.strip():
        return [f"File is empty: {file_path.name}"]

    errors = []
    found_sections = _extract_sections(content)

    required_sections = schema.get("required_sections", [])
    if config_overrides and file_path.name in config_overrides:
        required_sections = config_overrides[file_path.name]

    for section in required_sections:
        if section not in found_sections:
            errors.append(f"Missing required section '{section}' in {file_path.name}")

    return errors


def _build_artifact_overrides(config: dict, schemas: dict) -> dict[str, list[str]]:
    """Build section_requirements from artifact_schemas config overrides.

    Reads the artifact_schemas config property and merges each override
    with its base schema, respecting extend_base and additional_sections.

    Args:
        config: Full workflow config dict.
        schemas: Loaded artifact schemas dict.

    Returns:
        Dict mapping filenames to lists of required sections.
    """
    artifact_overrides = config.get("artifact_schemas", {})
    if not artifact_overrides:
        return {}

    result = {}
    for filename, override in artifact_overrides.items():
        base = schemas.get(filename, {})
        extend_base = override.get("extend_base", True)

        required = list(base.get("required_sections", [])) if extend_base else []
        if "required_sections" in override:
            required = list(set(required) | set(override["required_sections"]))

        additional = override.get("additional_sections", [])
        required = list(set(required) | set(additional))

        if required:
            result[filename] = required

    return result


def validate_artifacts_with_schemas(
    state_dir: Path, expected_outputs: list[str], config: dict
) -> dict:
    """Validate all expected artifacts using schema registry and config overrides.

    Args:
        state_dir: Directory containing task state files.
        expected_outputs: List of filenames to validate.
        config: Configuration dict, may contain "section_requirements" and/or
                "artifact_schemas" for overrides.

    Returns:
        Dict with "passed", "failures", "files_checked", "files_passed".
    """
    schemas = load_artifact_schemas()
    section_requirements = dict(config.get("section_requirements", {}))
    artifact_overrides = _build_artifact_overrides(config, schemas)

    for filename, sections in artifact_overrides.items():
        section_requirements[filename] = sections

    failures = []
    files_checked = 0
    files_passed = 0

    for filename in expected_outputs:
        file_path = state_dir / filename
        schema = schemas.get(filename, {})

        if schema:
            errors = validate_artifact_schema(file_path, schema, section_requirements)
        else:
            required_sections = section_requirements.get(filename, [])
            errors = validate_artifact(file_path, required_sections)

        files_checked += 1
        if errors:
            failures.extend(errors)
        else:
            files_passed += 1

    return {
        "passed": len(failures) == 0,
        "failures": failures,
        "files_checked": files_checked,
        "files_passed": files_passed,
    }


def validate_phase_tree_structure(plan: dict) -> list[str]:
    """Validate PLAN.md phase tree structure.

    Checks:
      - At least one phase exists
      - Each phase has a status value
      - Each sub-phase has a status value and context budget
      - Task checkboxes are well-formed
      - Phase/sub-phase status values are valid

    Args:
        plan: Parsed plan dict from state_reader.read_plan.

    Returns:
        List of error strings (empty = valid).
    """
    VALID_STATUSES = {"pending", "in_progress", "completed", "blocked"}
    errors = []

    phases = plan.get("phases", [])
    if not phases:
        return ["PLAN.md: no phases defined in Phases section"]

    for phase in phases:
        name = phase.get("name", "unnamed")
        status = phase.get("status", "")
        if status and status not in VALID_STATUSES:
            errors.append(
                f"Phase '{name}': invalid status '{status}' "
                f"(must be one of: {', '.join(sorted(VALID_STATUSES))})"
            )

        for sp in phase.get("subphases", []):
            sp_name = sp.get("name", "unnamed")
            sp_status = sp.get("status", "")
            if sp_status and sp_status not in VALID_STATUSES:
                errors.append(
                    f"Sub-phase '{sp_name}' in '{name}': invalid status '{sp_status}'"
                )

            for task in sp.get("tasks", []):
                if not isinstance(task, dict):
                    errors.append(
                        f"Sub-phase '{sp_name}' in '{name}': malformed task entry"
                    )

    return errors


def validate_plan_phase_order(plan: dict, config: dict) -> list[str]:
    """Cross-reference plan phases against workflow config phase_order.

    Checks:
      - Every plan phase name (or prefix) appears in config phase_order
      - Every config phase_order entry has a matching phase in the plan

    Args:
        plan: Parsed plan dict from state_reader.read_plan.
        config: Workflow config dict with phase_order.

    Returns:
        List of error strings (empty = consistent).
    """
    errors = []
    phase_order = config.get("phase_order", [])
    if not phase_order:
        return errors

    plan_phase_names = [p.get("name", "") for p in plan.get("phases", [])]

    for config_phase in phase_order:
        found = any(config_phase in name for name in plan_phase_names)
        if not found:
            errors.append(
                f"Phase order mismatch: config phase '{config_phase}' "
                f"has no matching entry in PLAN.md"
            )

    for plan_name in plan_phase_names:
        found = any(
            config_p in plan_name or plan_name.startswith(config_p)
            for config_p in phase_order
        )
        if not found:
            errors.append(
                f"Phase order mismatch: PLAN.md phase '{plan_name}' "
                f"has no matching entry in config phase_order"
            )

    return errors


def _check_phase_consistency(
    status_phase: str, checkpoint_phase: str, phase_order: list, errors: list
) -> None:
    """Check STATUS.md / checkpoint phase consistency and validity."""
    if status_phase and status_phase != checkpoint_phase:
        errors.append(
            f"State inconsistency: STATUS.md current_phase "
            f"'{status_phase}' != checkpoint current_phase '{checkpoint_phase}'"
        )
    if checkpoint_phase and phase_order and checkpoint_phase not in phase_order:
        errors.append(
            f"State inconsistency: checkpoint current_phase "
            f"'{checkpoint_phase}' not in config phase_order"
        )


def _check_completed_phases(
    completed_phases: list, phase_order: list, errors: list
) -> None:
    """Check completed phases are in config phase_order."""
    if not completed_phases or not phase_order:
        return
    for cp in completed_phases:
        if cp not in phase_order:
            errors.append(
                f"State inconsistency: completed phase '{cp}' not in config phase_order"
            )


def _check_state_consistency(
    status_state: str, checkpoint_state: str, states: dict, errors: list
) -> None:
    """Check STATUS.md / checkpoint state consistency and validity."""
    if status_state and status_state != checkpoint_state:
        errors.append(
            f"State inconsistency: STATUS.md current_state "
            f"'{status_state}' != checkpoint current_state '{checkpoint_state}'"
        )
    if checkpoint_state and states:
        known_states = {s.get("state") for s in states.values() if isinstance(s, dict)}
        if checkpoint_state not in known_states:
            errors.append(
                f"State inconsistency: checkpoint current_state "
                f"'{checkpoint_state}' not a valid state in config"
            )


def validate_state_consistency(
    status: dict, checkpoint: dict, config: dict
) -> list[str]:
    """Validate consistency between STATUS.md, checkpoint.json, and workflow config.

    Args:
        status: Parsed STATUS.md dict (from state_reader.read_status).
        checkpoint: Parsed checkpoint.json dict.
        config: Workflow config dict with phase_order and states.

    Returns:
        List of error strings (empty = consistent).
    """
    errors: list[str] = []
    phase_order = config.get("phase_order", [])
    states = config.get("states", {})

    _check_phase_consistency(
        status.get("current_phase", ""),
        checkpoint.get("current_phase", ""),
        phase_order,
        errors,
    )
    _check_completed_phases(checkpoint.get("completed_phases", []), phase_order, errors)
    _check_state_consistency(
        status.get("current_state", ""),
        checkpoint.get("current_state", ""),
        states,
        errors,
    )
    return errors
