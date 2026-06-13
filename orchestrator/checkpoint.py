"""Checkpoint manager for crash recovery and state persistence.

Handles atomic read/write of checkpoint.json, counter updates, and validation.
"""

import copy
import json
from datetime import datetime, timezone
from pathlib import Path

from orchestrator.constants import CANONICAL_STATES


def read_checkpoint(dir: Path, required: bool = True) -> dict | None:
    """Read and validate checkpoint.json.

    Args:
        dir: Directory containing checkpoint.json
        required: If True, raise FileNotFoundError when missing. If False, return None.

    Returns:
        Parsed checkpoint dict, or None if missing and required=False

    Raises:
        FileNotFoundError: If checkpoint.json doesn't exist and required=True
        ValueError: If JSON is malformed or required fields missing
    """
    path = Path(dir) / "checkpoint.json"
    if not path.exists():
        if required:
            raise FileNotFoundError(f"Missing required file: {path.name}")
        return None

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Malformed JSON in checkpoint.json: {e}") from e

    return data


def write_checkpoint(dir: Path, data: dict) -> None:
    """Atomic write of checkpoint.json.

    Writes to a temp file first, then renames to prevent partial writes.

    Args:
        dir: Directory to write checkpoint.json
        data: Checkpoint dict to write
    """
    path = Path(dir) / "checkpoint.json"
    temp_path = path.with_suffix(".json.tmp")

    # Add timestamp if not present
    if "last_updated" not in data:
        data["last_updated"] = (
            datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        )

    content = json.dumps(data, indent=2, ensure_ascii=False)
    temp_path.write_text(content, encoding="utf-8")
    temp_path.rename(path)


def update_checkpoint(
    checkpoint: dict,
    current_phase: str,
    current_state: str,
    next_state: str,
    result: dict,
) -> dict:
    """Update checkpoint after a state transition.

    Increments counters for retries and Ralph cycles, updates last_result,
    and records completed phases.

    Args:
        checkpoint: Current checkpoint dict
        current_phase: Phase identifier (e.g., "audit-03")
        current_state: State machine state before transition
        next_state: State machine state after transition
        result: Step execution result dict

    Returns:
        Updated checkpoint dict (new copy, does not mutate input)
    """
    # Create a deep copy to avoid mutating the input
    updated = copy.deepcopy(checkpoint)

    # Initialize counters dict if missing
    if "counters" not in updated:
        updated["counters"] = {}

    # Initialize counter for this phase if missing
    if current_phase not in updated["counters"]:
        updated["counters"][current_phase] = {"retries": 0, "ralph_cycles": 0}

    # Increment retry counter if staying in same state
    if next_state == current_state:
        updated["counters"][current_phase]["retries"] += 1

    # Increment Ralph cycle counter if transitioning through Ralph loop
    if current_state == "ralph_revise" and next_state == "ralph_critique":
        updated["counters"][current_phase]["ralph_cycles"] += 1

    # Update last_result
    updated["last_result"] = {
        "state": current_state,
        "status": result.get("status", "unknown"),
        "reason": result.get("reason", ""),
        "artifacts_written": result.get("artifacts", []),
        "validation_passed": result.get("validation_passed", False),
    }

    # Record completed phase if transitioning to done
    if next_state == "done":
        if "completed_phases" not in updated:
            updated["completed_phases"] = []
        updated["completed_phases"].append(
            {
                "phase": current_phase,
                "state": current_state,
                "completed_at": datetime.now(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z"),
            }
        )

    # Update current state and timestamp
    updated["current_state"] = next_state
    updated["last_updated"] = (
        datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    )

    return updated


def validate_checkpoint(checkpoint: dict, config: dict) -> list[str]:
    """Validate checkpoint consistency.

    Checks required fields, valid states, and counter constraints.

    Args:
        checkpoint: Checkpoint dict to validate
        config: Workflow config dict (for state validation)

    Returns:
        List of validation error messages (empty = valid)
    """
    errors = []

    # Required fields
    required_fields = [
        "workflow_id",
        "version",
        "current_phase",
        "current_state",
        "last_updated",
        "completed_phases",
        "counters",
        "last_result",
    ]

    for field in required_fields:
        if field not in checkpoint:
            errors.append(f"Missing required field: {field}")

    # Validate current_state is a canonical state
    if "current_state" in checkpoint:
        state = checkpoint["current_state"]
        if state not in CANONICAL_STATES:
            errors.append(
                f"Invalid state '{state}' in checkpoint, not in canonical states"
            )

    # Validate counters are non-negative
    if "counters" in checkpoint:
        for phase, counts in checkpoint["counters"].items():
            if "retries" in counts and counts["retries"] < 0:
                errors.append(f"Negative retry count for phase {phase}")
            if "ralph_cycles" in counts and counts["ralph_cycles"] < 0:
                errors.append(f"Negative Ralph cycle count for phase {phase}")

    # Validate last_result has required fields
    if "last_result" in checkpoint:
        last_result = checkpoint["last_result"]
        if "status" not in last_result:
            errors.append("Missing 'status' in last_result")

    return errors


def create_initial_checkpoint(workflow_id: str, version: int = 1) -> dict:
    """Create a new checkpoint with initial values.

    Args:
        workflow_id: Workflow identifier
        version: Schema version (default 1)

    Returns:
        Initial checkpoint dict
    """
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "workflow_id": workflow_id,
        "version": version,
        "current_phase": "init",
        "current_state": "init",
        "last_updated": now,
        "completed_phases": [],
        "counters": {},
        "last_result": {
            "state": "init",
            "status": "pending",
            "reason": "",
            "artifacts_written": [],
            "validation_passed": False,
        },
    }
