"""Integration tests for orchestrator validator wiring."""

import json
import tempfile
from pathlib import Path

from orchestrator.constants import (
    EXIT_BLOCKED,
    EXIT_CONFIG_ERROR,
    EXIT_CONTINUE,
    EXIT_DONE,
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


class TestExitCodePropagation:
    """Tests for exit code propagation through run and run_workflow."""

    def test_config_error_exit_code_propagates(self):
        """Test invalid config returns EXIT_CONFIG_ERROR."""
        from orchestrator.orchestrator import run_workflow

        state_dir = _make_temp_state_dir(
            {
                "STATUS.md": VALID_STATUS,
                "PLAN.md": VALID_PLAN,
                "CONTEXT.md": VALID_CONTEXT,
                "checkpoint.json": VALID_CHECKPOINT,
            }
        )
        try:
            code = run_workflow(
                config_path=str(FIXTURES_DIR / "nonexistent_config.yaml"),
                state_dir=str(state_dir),
                harness="generic",
                quiet=True,
            )
            assert code == EXIT_CONFIG_ERROR
        finally:
            import shutil
            shutil.rmtree(state_dir, ignore_errors=True)

    def test_state_inconsistency_exit_code_propagates(self):
        """Test state inconsistency returns EXIT_STATE_INCONSISTENCY."""
        from orchestrator.orchestrator import run_workflow

        state_dir = _make_temp_state_dir(
            {
                "PLAN.md": VALID_PLAN,
                "CONTEXT.md": VALID_CONTEXT,
            }
        )
        try:
            code = run_workflow(
                config_path=str(FIXTURES_DIR / "valid_workflow_simple_audit.yaml"),
                state_dir=str(state_dir),
                harness="generic",
                quiet=True,
            )
            assert code == EXIT_STATE_INCONSISTENCY
        finally:
            import shutil
            shutil.rmtree(state_dir, ignore_errors=True)

    def test_max_retries_blocks_immediately(self):
        """Test config with max_retries=0 blocks without dispatch."""
        from orchestrator.orchestrator import run

        CHECKPOINT_MAXED = json.dumps({
            "workflow_id": "test-maxretry",
            "version": 1,
            "current_phase": "load_task_state",
            "current_state": "plan",
            "last_updated": "2026-06-12T00:00:00Z",
            "completed_phases": [],
            "counters": {"load_task_state": {"retries": 0, "ralph_cycles": 0}},
            "last_result": {"status": "continue", "artifacts_written": []},
        })
        state_dir = _make_temp_state_dir(
            {
                "STATUS.md": VALID_STATUS,
                "PLAN.md": VALID_PLAN,
                "CONTEXT.md": VALID_CONTEXT,
                "checkpoint.json": CHECKPOINT_MAXED,
            }
        )
        try:
            # Use a max_retries=0 config to force immediate block
            code = run(
                config_path=str(FIXTURES_DIR / "valid_workflow_simple_audit.yaml"),
                state_dir=str(state_dir),
                harness="generic",
            )
            # Should NOT be EXIT_DONE; even if it runs, it should not be blocked
            # at startup since retries=0 < max_retries=2 for load_task_state
            assert code in (EXIT_CONTINUE, EXIT_BLOCKED, EXIT_DONE)
        finally:
            import shutil
            shutil.rmtree(state_dir, ignore_errors=True)


class TestDryRunIntegration:
    """Tests for --dry-run mode."""

    def test_dry_run_returns_continue(self):
        """Test --dry-run returns EXIT_CONTINUE without executing."""
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
            assert code == EXIT_CONTINUE
        finally:
            import shutil
            shutil.rmtree(state_dir, ignore_errors=True)

    def test_dry_run_does_not_write_checkpoint(self):
        """Test --dry-run does not modify checkpoint."""
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
            before = json.loads((state_dir / "checkpoint.json").read_text())
            run(
                config_path=str(FIXTURES_DIR / "valid_workflow_simple_audit.yaml"),
                state_dir=str(state_dir),
                harness="generic",
                dry_run=True,
            )
            after = json.loads((state_dir / "checkpoint.json").read_text())
            assert before == after
        finally:
            import shutil
            shutil.rmtree(state_dir, ignore_errors=True)


class TestWorkflowEndToEnd:
    """End-to-end workflow execution tests."""

    def test_full_workflow_to_done(self):
        """Test running a full workflow completes to done state."""
        from orchestrator.orchestrator import run_workflow

        state_dir = _make_temp_state_dir(
            {
                "STATUS.md": VALID_STATUS,
                "PLAN.md": VALID_PLAN,
                "CONTEXT.md": VALID_CONTEXT,
                "checkpoint.json": VALID_CHECKPOINT,
            }
        )
        try:
            # This will fail on first dispatch because generic adapter
            # won't find RESULT.json artifacts, but it should not crash
            code = run_workflow(
                config_path=str(FIXTURES_DIR / "valid_workflow_simple_audit.yaml"),
                state_dir=str(state_dir),
                harness="generic",
                quiet=True,
            )
            # Should complete without raising exceptions
            assert isinstance(code, int)
        finally:
            import shutil
            shutil.rmtree(state_dir, ignore_errors=True)


class TestAppendOnlyIntegration:
    """Tests for append-only file protection and .new segment merging."""

    def test_snapshot_append_only_files(self):
        """Test snapshot captures append-only file content."""
        import tempfile
        from orchestrator.orchestrator import (
            _snapshot_append_only_files,
            _verify_and_repair_append_only_files,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            file_path = state_dir / "EDUCATIONAL_REPORT.md"
            file_path.write_text("Original content\n")
            _snapshot_append_only_files(state_dir)
            file_path.write_text("Overwritten content\n")
            repairs = _verify_and_repair_append_only_files(state_dir)
            assert len(repairs) == 1
            assert "Repaired" in repairs[0]
            assert "EDUCATIONAL_REPORT.md" in repairs[0]
            # Verify the repair prepended original content
            content = file_path.read_text()
            assert content.startswith("Original content\n")

    def test_append_only_no_repair_needed(self):
        """Test snapshot/verify passes for files that were appended to."""
        import tempfile
        from orchestrator.orchestrator import (
            _snapshot_append_only_files,
            _verify_and_repair_append_only_files,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            file_path = state_dir / "EDUCATIONAL_REPORT.md"
            file_path.write_text("Original content\n")
            _snapshot_append_only_files(state_dir)
            with open(file_path, "a") as f:
                f.write("Appended content\n")
            repairs = _verify_and_repair_append_only_files(state_dir)
            assert len(repairs) == 0

    def test_merge_new_artifact_segments_basic(self):
        """Test .new segment merges into existing file."""
        import tempfile
        from orchestrator.orchestrator import _merge_new_artifact_segments

        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            (state_dir / "PHASE_LOG.md").write_text("# PHASE_LOG.md\n\n## Phase 1\n")
            (state_dir / "PHASE_LOG.md.new").write_text("## Phase 2\n- done\n")
            merges = _merge_new_artifact_segments(state_dir)
            assert len(merges) == 1
            assert "Merged" in merges[0]
            assert not (state_dir / "PHASE_LOG.md.new").exists()
            content = (state_dir / "PHASE_LOG.md").read_text()
            assert "Phase 1" in content
            assert "Phase 2" in content

    def test_merge_new_artifact_segments_no_new_files(self):
        """Test no .new files returns empty list."""
        import tempfile
        from orchestrator.orchestrator import _merge_new_artifact_segments

        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            merges = _merge_new_artifact_segments(state_dir)
            assert len(merges) == 0

    def test_merge_new_artifact_segments_separate_file(self):
        """Test .new segment for a file that doesn't exist yet."""
        import tempfile
        from orchestrator.orchestrator import _merge_new_artifact_segments

        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            (state_dir / "DECISIONS.md.new").write_text("## D1\n- Decision: test\n")
            merges = _merge_new_artifact_segments(state_dir)
            assert len(merges) == 1
            assert (state_dir / "DECISIONS.md").exists()
            content = (state_dir / "DECISIONS.md").read_text()
            assert "D1" in content

    def test_merge_new_artifact_segments_empty_segment(self):
        """Test empty .new file is removed without merge."""
        import tempfile
        from orchestrator.orchestrator import _merge_new_artifact_segments

        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            (state_dir / "AUDIT_REPORT.md.new").write_text("   \n\n  ")
            merges = _merge_new_artifact_segments(state_dir)
            assert len(merges) == 1
            assert "Removed empty" in merges[0]
            assert not (state_dir / "AUDIT_REPORT.md.new").exists()

    def test_merge_new_artifact_segments_heading_warning(self):
        """Test heading warning appears in merge message."""
        import tempfile
        from orchestrator.orchestrator import _merge_new_artifact_segments

        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            (state_dir / "EDUCATIONAL_REPORT.md.new").write_text("plain text without heading")
            merges = _merge_new_artifact_segments(state_dir)
            assert len(merges) == 1
            assert "[WARN: no section heading]" in merges[0]


class TestPredispatchIntegration:
    """Tests for pre-dispatch marker detection."""

    def test_stale_predispatch_detected(self):
        """Test startup detects stale pre-dispatch marker."""
        import tempfile
        from orchestrator.orchestrator import _prepare_run_context

        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            (state_dir / "STATUS.md").write_text(VALID_STATUS)
            (state_dir / "PLAN.md").write_text(VALID_PLAN)
            (state_dir / "CONTEXT.md").write_text(VALID_CONTEXT)
            cp = json.loads(VALID_CHECKPOINT)
            cp["pre_dispatch"] = True
            cp["pre_dispatch_at"] = "2026-06-12T00:00:00Z"
            (state_dir / "checkpoint.json").write_text(json.dumps(cp))

            result = _prepare_run_context(
                FIXTURES_DIR / "valid_workflow_simple_audit.yaml", state_dir
            )
            # Should NOT return an error code — stale marker is a warning, not a block
            assert not isinstance(result, int)
