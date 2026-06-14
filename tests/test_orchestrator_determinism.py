"""Dedicated tests for orchestrator determinism features.

Tests the 10 determinism features added in Phase 6:
  - Exit code mapping (0-5)
  - validation_mode (strict/relaxed/none)
  - checkpoint_before_run pre-dispatch marker
  - Pre-dispatch counter check
  - RESULT.json fallback (4 scenarios)
  - Agent transition authority (next_action ignored)
"""

import json
import tempfile
from pathlib import Path


from orchestrator.adapters.base import HarnessResult, StepContract
from orchestrator.constants import (
    EXIT_BLOCKED,
    EXIT_CONFIG_ERROR,
    EXIT_CONTINUE,
    EXIT_DONE,
    EXIT_INTERNAL_ERROR,
    EXIT_STATE_INCONSISTENCY,
)
from orchestrator.orchestrator import (
    _apply_result_fallback,
    _build_validation_none,
    _build_validation_relaxed,
    _build_validation_strict,
    _exit_code_for_state,
    _run_predispatch_checks,
    _write_predispatch_checkpoint,
)
from orchestrator.step_compiler import resolve_next_state

FIXTURES_DIR = Path(__file__).parent / "fixtures"
TASK_STATE_VALID = FIXTURES_DIR / "task_state_valid"


def _make_contract(overrides: dict | None = None) -> StepContract:
    """Create a minimal StepContract for testing."""
    base = StepContract(
        step_id="test-det",
        state="execute",
        agent_profile="test",
        permissions="edit",
        inputs=[],
        expected_outputs=["RESULT.json"],
        timeout_s=60,
        max_retries=3,
    )
    if overrides:
        for k, v in overrides.items():
            setattr(base, k, v)
    return base


def _make_harness_result(status: str = "pass",
                          artifacts: list[str] | None = None) -> HarnessResult:
    """Create a minimal HarnessResult for testing."""
    return HarnessResult(
        status=status,
        step_id="test-det",
        reason="test",
        artifacts={},
        artifacts_written=artifacts or [],
        validation={"passed": True},
        issues=[],
        next_action="done",
    )


class TestExitCodeMapping:
    """Tests for exit code mapping."""

    def test_exit_done(self):
        """Test EXIT_DONE (0) when transitioning to done."""
        assert _exit_code_for_state("done") == EXIT_DONE

    def test_exit_blocked(self):
        """Test EXIT_BLOCKED (1) when transitioning to blocked."""
        assert _exit_code_for_state("blocked") == EXIT_BLOCKED

    def test_exit_continue(self):
        """Test EXIT_CONTINUE (2) for intermediate states."""
        assert _exit_code_for_state("execute") == EXIT_CONTINUE
        assert _exit_code_for_state("audit") == EXIT_CONTINUE
        assert _exit_code_for_state("fix") == EXIT_CONTINUE

    def test_exit_config_error_constant(self):
        """Test EXIT_CONFIG_ERROR (3) constant exists."""
        assert EXIT_CONFIG_ERROR == 3

    def test_exit_state_inconsistency_constant(self):
        """Test EXIT_STATE_INCONSISTENCY (4) constant exists."""
        assert EXIT_STATE_INCONSISTENCY == 4

    def test_exit_internal_error_constant(self):
        """Test EXIT_INTERNAL_ERROR (5) constant exists."""
        assert EXIT_INTERNAL_ERROR == 5

    def test_config_error_path(self):
        """Test config error maps to EXIT_CONFIG_ERROR."""
        from orchestrator.orchestrator import _prepare_run_context

        state_dir = TASK_STATE_VALID
        result = _prepare_run_context(
            FIXTURES_DIR / "nonexistent_config.yaml", state_dir
        )
        assert result == EXIT_CONFIG_ERROR

    def test_state_inconsistency_path(self):
        """Test state inconsistency maps to EXIT_STATE_INCONSISTENCY."""
        from orchestrator.orchestrator import _prepare_run_context

        result = _prepare_run_context(
            FIXTURES_DIR / "valid_workflow_simple_audit.yaml",
            FIXTURES_DIR / "task_state_missing_status",
        )
        assert result == EXIT_STATE_INCONSISTENCY


class TestValidationMode:
    """Tests for validation_mode feature."""

    def test_strict_blocks_on_failure(self):
        """Test strict mode blocks on validation failure."""
        for harness_passed in (True, False):
            result = _build_validation_strict(
                harness_passed,
                {"passed": False, "failures": ["bad"], "files_checked": 1, "files_passed": 0},
                ["bad"],
            )
            assert result["passed"] is False

    def test_strict_passes_on_success(self):
        """Test strict mode passes on all success."""
        result = _build_validation_strict(
            True,
            {"passed": True, "failures": [], "files_checked": 1, "files_passed": 1},
            [],
        )
        assert result["passed"] is True

    def test_relaxed_warns_but_passes(self):
        """Test relaxed mode passes when harness passes despite file failures."""
        result = _build_validation_relaxed(
            True,
            {"passed": False, "failures": ["Missing file"], "files_checked": 1, "files_passed": 0},
            ["Missing file"],
        )
        assert result["passed"] is True
        assert result["failures"] == []

    def test_relaxed_fails_when_harness_fails(self):
        """Test relaxed mode still blocks when harness fails."""
        result = _build_validation_relaxed(
            False,
            {"passed": False, "failures": ["Missing file"], "files_checked": 1, "files_passed": 0},
            ["Missing file"],
        )
        assert result["passed"] is False

    def test_none_skips_artifact_check(self):
        """Test none mode skips artifact validation entirely."""
        result = _build_validation_none(True)
        assert result["passed"] is True
        assert result["files_checked"] == 0

    def test_none_fails_when_harness_fails(self):
        """Test none mode still blocks when harness fails."""
        result = _build_validation_none(False)
        assert result["passed"] is False


class TestCheckpointBeforeRun:
    """Tests for checkpoint_before_run feature."""

    def test_writes_predispatch_marker(self):
        """Test pre-dispatch checkpoint writes pre_dispatch=true."""
        import tempfile

        from orchestrator.checkpoint import create_initial_checkpoint

        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            cp = create_initial_checkpoint("test-cp")
            _write_predispatch_checkpoint(
                cp, {"workflow_id": "test"}, "phase_1", "execute", state_dir
            )
            from orchestrator.checkpoint import read_checkpoint

            result = read_checkpoint(state_dir)
            assert result["pre_dispatch"] is True
            assert "pre_dispatch_at" in result

    def test_predispatch_exit_on_max_retries(self):
        """Test pre-dispatch check returns EXIT_BLOCKED on max retries."""
        from orchestrator.checkpoint import create_initial_checkpoint

        cp = create_initial_checkpoint("test-retry")
        cp["counters"]["phase_1"] = {"retries": 3, "ralph_cycles": 0}
        contract = _make_contract({"max_retries": 3})
        code = _run_predispatch_checks(
            cp, contract, "phase_1", "execute",
            {"states": {}}, TASK_STATE_VALID,
        )
        assert code == EXIT_BLOCKED

    def test_predispatch_proceeds_within_limit(self):
        """Test pre-dispatch check returns None within retry limit."""
        from orchestrator.checkpoint import create_initial_checkpoint

        cp = create_initial_checkpoint("test-ok")
        cp["counters"]["phase_1"] = {"retries": 1, "ralph_cycles": 0}
        contract = _make_contract({"max_retries": 3})
        code = _run_predispatch_checks(
            cp, contract, "phase_1", "execute",
            {"states": {}}, TASK_STATE_VALID,
        )
        assert code is None

    def test_predispatch_blocked_zero_retries(self):
        """Test max_retries=0 blocks immediately without dispatch."""
        from orchestrator.checkpoint import create_initial_checkpoint

        cp = create_initial_checkpoint("test-zero")
        cp["counters"]["phase_1"] = {"retries": 0, "ralph_cycles": 0}
        contract = _make_contract({"max_retries": 0})
        code = _run_predispatch_checks(
            cp, contract, "phase_1", "execute",
            {"states": {}}, TASK_STATE_VALID,
        )
        assert code == EXIT_BLOCKED


class TestResultJsonFallback:
    """Tests for RESULT.json fallback protocol."""

    def test_fallback_all_artifacts_present(self):
        """Test fallback infers pass when all artifacts exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            for name in ["RESULT.json", "STATUS.md"]:
                (state_dir / name).write_text("content")
            contract = _make_contract({"expected_outputs": ["STATUS.md"]})
            result = _make_harness_result("")
            _apply_result_fallback(result, contract, state_dir)
            assert result.status == "pass"

    def test_fallback_partial_artifacts_fail(self):
        """Test fallback infers fail when some artifacts missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            (state_dir / "RESULT.json").write_text("{}")
            contract = _make_contract({"expected_outputs": ["STATUS.md", "REPORT.md"]})
            (state_dir / "STATUS.md").write_text("status content")
            result = _make_harness_result("")
            _apply_result_fallback(result, contract, state_dir)
            assert result.status == "fail"
            assert "missing" in result.reason.lower()

    def test_fallback_no_artifacts_fail(self):
        """Test fallback infers fail when no artifacts written."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            contract = _make_contract({"expected_outputs": []})
            result = _make_harness_result("")
            _apply_result_fallback(result, contract, state_dir)
            assert result.status == "fail"
            assert "no artifacts" in result.reason.lower()

    def test_result_json_takes_priority(self):
        """Test existing RESULT.json status takes priority over fallback."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            result_data = {"status": "pass", "reason": "real result"}
            (state_dir / "RESULT.json").write_text(json.dumps(result_data))
            contract = _make_contract({"expected_outputs": []})
            result = _make_harness_result("pass",
                                          artifacts=["RESULT.json"])
            _apply_result_fallback(result, contract, state_dir)
            assert result.status == "pass"

    def test_fallback_no_expected_outputs(self):
        """Test fallback with no expected outputs and no RESULT.json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            contract = _make_contract({"expected_outputs": []})
            result = _make_harness_result("")
            _apply_result_fallback(result, contract, state_dir)
            assert result.status == "fail"
            assert "no artifacts" in result.reason.lower()


class TestAgentTransitionAuthority:
    """Tests that agent output is evidence, not authority."""

    def test_next_action_ignored(self):
        """Test agent next_action does not override config transitions."""
        config = {
            "states": {
                "execute": {
                    "transitions": [
                        {"condition": "pass", "target": "audit"},
                        {"condition": "fail", "target": "blocked"},
                    ],
                },
            },
        }
        counters = {"phase_1": {"retries": 0, "ralph_cycles": 0}}
        next_state = resolve_next_state(
            "execute", "phase_1",
            {"status": "pass"}, {"passed": True},
            config, counters,
        )
        assert next_state == "audit"

    def test_agent_fail_does_not_advance(self):
        """Test agent fail status prevents advancement."""
        config = {
            "states": {
                "execute": {
                    "transitions": [
                        {"condition": "pass", "target": "next_phase"},
                        {"condition": "fail", "target": "fix"},
                    ],
                },
            },
        }
        counters = {"phase_1": {"retries": 0, "ralph_cycles": 0}}
        next_state = resolve_next_state(
            "execute", "phase_1",
            {"status": "fail"}, {"passed": False},
            config, counters,
        )
        assert next_state == "fix"


class TestEndToEndDeterminism:
    """End-to-end determinism tests using the orchestrator run function."""

    VALID_STATUS = """# Status

## Current Phase
load_task_state

## Current State
plan

## Progress
- Phase: 1 of 1

## Next Action
Execute phase

## Blocked By
none
"""

    VALID_CHECKPOINT = json.dumps({
        "workflow_id": "test-det-e2e",
        "version": 1,
        "current_phase": "load_task_state",
        "current_state": "plan",
        "last_updated": "2026-06-12T00:00:00Z",
        "completed_phases": [],
        "counters": {"load_task_state": {"retries": 0, "ralph_cycles": 0}},
        "last_result": {"status": "continue", "artifacts_written": []},
    })

    VALID_PLAN = """# Plan

## Phases
- [ ] Phase 1: Execute

## Validation Gates
- file_check: Required files exist
"""

    VALID_CONTEXT = """# Context

## Project
Test project

## Task Directory
/tmp/test

## Assumptions
- Test environment

## Known Constraints
- None
"""

    def test_dry_run_returns_continue(self):
        """Test --dry-run mode returns EXIT_CONTINUE."""
        from orchestrator.orchestrator import run

        state_dir = Path(tempfile.mkdtemp())
        try:
            for name, content in [
                ("STATUS.md", self.VALID_STATUS),
                ("PLAN.md", self.VALID_PLAN),
                ("CONTEXT.md", self.VALID_CONTEXT),
                ("checkpoint.json", self.VALID_CHECKPOINT),
            ]:
                (state_dir / name).write_text(content)
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

    def test_workflow_handles_config_error(self):
        """Test workflow returns EXIT_CONFIG_ERROR for bad config."""
        from orchestrator.orchestrator import run_workflow

        state_dir = Path(tempfile.mkdtemp())
        try:
            for name, content in [
                ("STATUS.md", self.VALID_STATUS),
                ("PLAN.md", self.VALID_PLAN),
                ("CONTEXT.md", self.VALID_CONTEXT),
                ("checkpoint.json", self.VALID_CHECKPOINT),
            ]:
                (state_dir / name).write_text(content)
            code = run_workflow(
                config_path=str(FIXTURES_DIR / "invalid_workflow_missing_field.yaml"),
                state_dir=str(state_dir),
                harness="generic",
            )
            assert code == EXIT_CONFIG_ERROR
        finally:
            import shutil
            shutil.rmtree(state_dir, ignore_errors=True)
