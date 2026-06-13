"""Integration tests for orchestrator validator wiring."""

import json
import tempfile
from pathlib import Path

from orchestrator.constants import (
    EXIT_BLOCKED,
    EXIT_CONFIG_ERROR,
    EXIT_STATE_INCONSISTENCY,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _make_temp_state_dir(files: dict[str, str]) -> Path:
    """Create a temporary state directory with given files."""
    tmpdir = Path(tempfile.mkdtemp())
    for name, content in files.items():
        (tmpdir / name).write_text(content, encoding="utf-8")
    return tmpdir


VALID_STATUS = """# Status

## Current Phase
load_task_state

## Current State
plan

## Progress
- Phase: 1 of 1
- Checklist: 0/1 complete

## Next Action
Execute phase

## Blocked By
none
"""

VALID_CHECKPOINT = json.dumps(
    {
        "workflow_id": "test-integration",
        "version": 1,
        "current_phase": "load_task_state",
        "current_state": "plan",
        "last_updated": "2026-06-12T00:00:00Z",
        "completed_phases": [],
        "counters": {"load_task_state": {"retries": 0, "ralph_cycles": 0}},
        "last_result": {"status": "continue", "artifacts_written": []},
    }
)

VALID_PLAN = """# Plan

## Phases
- [ ] Phase 1: Execute

## Validation Gates
- file_check: Required files exist
"""

VALID_CONTEXT = """# Context

## File Map
- tests/: Test directory

## Assumptions
- Test environment

## Known Constraints
- New test

## Reference Links
- None

## Harness
generic
"""


class TestConfigValidationIntegration:
    """Tests that validate_workflow_config is wired into orchestrator startup."""

    def test_valid_config_allows_run(self):
        """Test that valid workflow config does not block execution."""
        from orchestrator.orchestrator import run

        state_dir = _make_temp_state_dir(
            {
                "STATUS.md": VALID_STATUS,
                "PLAN.md": VALID_PLAN,
                "CONTEXT.md": VALID_CONTEXT,
                "checkpoint.json": VALID_CHECKPOINT,
            }
        )

        try:
            code = run(
                config_path=str(FIXTURES_DIR / "valid_workflow_simple_audit.yaml"),
                state_dir=str(state_dir),
                harness="generic",
                dry_run=True,
            )
            assert code != EXIT_BLOCKED, "Valid config should not block"
        finally:
            import shutil

            shutil.rmtree(state_dir, ignore_errors=True)

    def test_invalid_config_blocks_run(self):
        """Test that invalid workflow config blocks execution at startup."""
        from orchestrator.orchestrator import run

        state_dir = _make_temp_state_dir(
            {
                "STATUS.md": VALID_STATUS,
                "PLAN.md": VALID_PLAN,
                "CONTEXT.md": VALID_CONTEXT,
                "checkpoint.json": VALID_CHECKPOINT,
            }
        )

        try:
            code = run(
                config_path=str(FIXTURES_DIR / "invalid_workflow_missing_field.yaml"),
                state_dir=str(state_dir),
                harness="generic",
                dry_run=True,
            )
            assert code == EXIT_CONFIG_ERROR, (
                "Invalid config should return config error"
            )
        finally:
            import shutil

            shutil.rmtree(state_dir, ignore_errors=True)

    def test_missing_config_blocks_run(self):
        """Test that non-existent config file blocks execution."""
        from orchestrator.orchestrator import run

        state_dir = _make_temp_state_dir(
            {
                "STATUS.md": VALID_STATUS,
                "PLAN.md": VALID_PLAN,
                "CONTEXT.md": VALID_CONTEXT,
                "checkpoint.json": VALID_CHECKPOINT,
            }
        )

        try:
            code = run(
                config_path=str(FIXTURES_DIR / "nonexistent_config.yaml"),
                state_dir=str(state_dir),
                harness="generic",
                dry_run=True,
            )
            assert code == EXIT_CONFIG_ERROR, (
                "Missing config should return config error"
            )
        finally:
            import shutil

            shutil.rmtree(state_dir, ignore_errors=True)


class TestValidatorImports:
    """Tests that all validators are importable through the orchestrator."""

    def test_validators_imported_by_orchestrator(self):
        """Test that orchestrator module imports the validator functions."""
        import orchestrator.orchestrator as orch_mod

        assert hasattr(orch_mod, "validate_artifacts")
        assert hasattr(orch_mod, "validate_workflow_config")
        assert hasattr(orch_mod, "validate_state_consistency")
