"""File and state validators for orchestrator artifacts."""

from pathlib import Path


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

    required_fields = [
        "workflow_id",
        "version",
        "current_phase",
        "current_state",
        "last_updated",
    ]
    errors = []
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if "version" in data:
        version = data["version"]
        if not isinstance(version, int) or version < 1:
            errors.append(
                f"Invalid value for version: must be integer >= 1, got {version!r}"
            )

    if config is not None:
        states = config.get("states", {})
        phase_order = config.get("phase_order", [])
        current_phase = data.get("current_phase", "")
        current_state = data.get("current_state", "")

        if current_phase and phase_order and current_phase not in phase_order:
            errors.append(
                f"Invalid value for current_phase: '{current_phase}' not in phase_order"
            )

        if current_state and states:
            known_states = {
                s.get("state") for s in states.values() if isinstance(s, dict)
            }
            if current_state not in known_states:
                errors.append(
                    f"Invalid value for current_state:"
                    f" '{current_state}' not in known states"
                )

    return errors


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
    errors = []

    status_phase = status.get("current_phase", "")
    status_state = status.get("current_state", "")
    checkpoint_phase = checkpoint.get("current_phase", "")
    checkpoint_state = checkpoint.get("current_state", "")
    phase_order = config.get("phase_order", [])
    states = config.get("states", {})

    if status_phase != checkpoint_phase:
        errors.append(
            f"State inconsistency: STATUS.md current_phase "
            f"'{status_phase}' != checkpoint current_phase '{checkpoint_phase}'"
        )

    if checkpoint_phase and phase_order and checkpoint_phase not in phase_order:
        errors.append(
            f"State inconsistency: checkpoint current_phase "
            f"'{checkpoint_phase}' not in config phase_order"
        )

    completed_phases = checkpoint.get("completed_phases", [])
    if completed_phases and phase_order:
        for cp in completed_phases:
            if cp not in phase_order:
                errors.append(
                    f"State inconsistency: completed phase "
                    f"'{cp}' not in config phase_order"
                )

    if status_state != checkpoint_state:
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

    return errors
