"""Tests for _try_advance_subphase sub-phase advancement logic."""

import tempfile
from pathlib import Path

from orchestrator.adapters.base import StepContract
from orchestrator.constants import EXIT_CONTINUE
from orchestrator.orchestrator import _try_advance_subphase


class TestSubphaseAdvancement:
    """Tests for _try_advance_subphase."""

    def _make_status_md(self, phase: str, subphase: str) -> str:
        subphase_line = f"\n## Current Sub-phase\n{subphase}" if subphase else ""
        return f"""# Status

## Current Phase
{phase}

## Current State
execute{subphase_line}

## Progress
- Phase: 8 of 10

## Next Action
Continue to execute

## Blocked By
none
"""

    def _make_minimal_contract(self) -> StepContract:
        return StepContract(
            step_id="test-advance",
            state="execute",
            agent_profile="test",
            permissions="read-only",
            inputs=[],
            expected_outputs=[],
            timeout_s=60,
            max_retries=3,
        )

    def test_advance_to_next_pending_subphase(self):
        """Advancing through pending sub-phases returns EXIT_CONTINUE."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            status_md = self._make_status_md(
                "Phase 8: Integration Tests",
                "Sub-phase 8.1: Sub-phase advancement test",
            )
            (state_dir / "STATUS.md").write_text(status_md)

            plan = {
                "phases": [
                    {
                        "name": "Phase 8: Integration Tests",
                        "status": "in_progress",
                        "metadata": {},
                        "subphases": [
                            {
                                "name": "Sub-phase 8.1: Sub-phase advancement test",
                                "status": "completed",
                                "metadata": {},
                                "tasks": [{"text": "Task A", "done": True}],
                                "task_completion": 1.0,
                            },
                            {
                                "name": "Sub-phase 8.2: Budget extraction test",
                                "status": "pending",
                                "metadata": {},
                                "tasks": [{"text": "Task B", "done": False}],
                                "task_completion": 0.0,
                            },
                        ],
                    }
                ]
            }
            status = {
                "current_phase": "Phase 8: Integration Tests",
                "current_state": "execute",
                "current_subphase": "Sub-phase 8.1: Sub-phase advancement test",
                "next_action": "Execute phase",
                "blocked_by": "none",
            }
            contract = self._make_minimal_contract()
            config = {"states": {}, "phases": []}
            context = {"project": "Test", "harness": "generic"}

            code = _try_advance_subphase(
                state_dir, plan, status, contract, config, context
            )

            assert code == EXIT_CONTINUE
            assert "Sub-phase 8.2" in contract.subphase_name

    def test_all_subphases_done_returns_none(self):
        """All sub-phases completed returns None (proceed with phase transition)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            status_md = self._make_status_md(
                "Phase 8: Integration Tests",
                "Sub-phase 8.2: Budget extraction test",
            )
            (state_dir / "STATUS.md").write_text(status_md)

            plan = {
                "phases": [
                    {
                        "name": "Phase 8: Integration Tests",
                        "status": "in_progress",
                        "metadata": {},
                        "subphases": [
                            {
                                "name": "Sub-phase 8.1: Sub-phase advancement test",
                                "status": "completed",
                                "metadata": {},
                                "tasks": [{"text": "Task A", "done": True}],
                                "task_completion": 1.0,
                            },
                            {
                                "name": "Sub-phase 8.2: Budget extraction test",
                                "status": "completed",
                                "metadata": {},
                                "tasks": [{"text": "Task B", "done": True}],
                                "task_completion": 1.0,
                            },
                        ],
                    }
                ]
            }
            status = {
                "current_phase": "Phase 8: Integration Tests",
                "current_state": "execute",
                "current_subphase": "Sub-phase 8.2: Budget extraction test",
                "next_action": "Execute phase",
                "blocked_by": "none",
            }
            contract = self._make_minimal_contract()
            config = {"states": {}, "phases": []}
            context = {"project": "Test", "harness": "generic"}

            code = _try_advance_subphase(
                state_dir, plan, status, contract, config, context
            )

            assert code is None

    def test_flat_plan_no_subphases_returns_none(self):
        """Flat plan (no sub-phases) returns None for backward compat."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            status_md = self._make_status_md("Phase 1: Execute", "")
            (state_dir / "STATUS.md").write_text(status_md)

            plan = {
                "phases": [
                    {
                        "name": "Phase 1: Execute",
                        "status": "pending",
                        "metadata": {},
                        "subphases": [],
                    }
                ]
            }
            status = {
                "current_phase": "Phase 1: Execute",
                "current_state": "execute",
                "current_subphase": "",
                "next_action": "Execute phase",
                "blocked_by": "none",
            }
            contract = self._make_minimal_contract()
            config = {"states": {}, "phases": []}
            context = {"project": "Test", "harness": "generic"}

            code = _try_advance_subphase(
                state_dir, plan, status, contract, config, context
            )

            assert code is None

    def test_advance_verifies_status_file_updated(self):
        """After advancing, STATUS.md should reflect the new sub-phase."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            status_md = self._make_status_md(
                "Phase 8: Integration Tests",
                "Sub-phase 8.1: Sub-phase advancement test",
            )
            (state_dir / "STATUS.md").write_text(status_md)

            plan = {
                "phases": [
                    {
                        "name": "Phase 8: Integration Tests",
                        "status": "in_progress",
                        "metadata": {},
                        "subphases": [
                            {
                                "name": "Sub-phase 8.1: Sub-phase advancement test",
                                "status": "completed",
                                "metadata": {},
                                "tasks": [],
                                "task_completion": 1.0,
                            },
                            {
                                "name": "Sub-phase 8.2: Budget extraction test",
                                "status": "pending",
                                "metadata": {},
                                "tasks": [],
                                "task_completion": 0.0,
                            },
                        ],
                    }
                ]
            }
            status = {
                "current_phase": "Phase 8: Integration Tests",
                "current_state": "execute",
                "current_subphase": "Sub-phase 8.1: Sub-phase advancement test",
                "next_action": "Execute phase",
                "blocked_by": "none",
            }
            contract = self._make_minimal_contract()
            config = {"states": {}, "phases": []}
            context = {"project": "Test", "harness": "generic"}

            _try_advance_subphase(
                state_dir, plan, status, contract, config, context
            )

            updated = (state_dir / "STATUS.md").read_text()
            assert "Sub-phase 8.2" in updated

    def test_no_current_subphase_starts_from_first_pending(self):
        """With empty current_subphase, advances to first pending sub-phase."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            status_md = self._make_status_md("Phase 8: Integration Tests", "")
            (state_dir / "STATUS.md").write_text(status_md)

            plan = {
                "phases": [
                    {
                        "name": "Phase 8: Integration Tests",
                        "status": "in_progress",
                        "metadata": {},
                        "subphases": [
                            {
                                "name": "Sub-phase 8.1: Sub-phase advancement test",
                                "status": "completed",
                                "metadata": {},
                                "tasks": [],
                                "task_completion": 1.0,
                            },
                            {
                                "name": "Sub-phase 8.2: Budget extraction test",
                                "status": "pending",
                                "metadata": {},
                                "tasks": [],
                                "task_completion": 0.0,
                            },
                        ],
                    }
                ]
            }
            status = {
                "current_phase": "Phase 8: Integration Tests",
                "current_state": "execute",
                "current_subphase": "",
                "next_action": "Execute phase",
                "blocked_by": "none",
            }
            contract = self._make_minimal_contract()
            config = {"states": {}, "phases": []}
            context = {"project": "Test", "harness": "generic"}

            code = _try_advance_subphase(
                state_dir, plan, status, contract, config, context
            )

            assert code == EXIT_CONTINUE
            assert "Sub-phase 8.2" in contract.subphase_name

    def test_skips_subphase_with_unmet_dependency(self):
        """Sub-phase with unmet Dependency is skipped, returns None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            status_md = self._make_status_md(
                "Phase 8: Integration Tests",
                "Sub-phase 8.1: Sub-phase advancement test",
            )
            (state_dir / "STATUS.md").write_text(status_md)

            plan = {
                "phases": [
                    {
                        "name": "Phase 8: Integration Tests",
                        "status": "in_progress",
                        "metadata": {},
                        "subphases": [
                            {
                                "name": "Sub-phase 8.1: Sub-phase advancement test",
                                "status": "completed",
                                "metadata": {},
                                "tasks": [],
                                "task_completion": 1.0,
                            },
                            {
                                "name": "Sub-phase 8.2: Budget extraction test",
                                "status": "pending",
                                "metadata": {"Dependency": "Sub-phase 8.3"},
                                "tasks": [],
                                "task_completion": 0.0,
                            },
                        ],
                    }
                ]
            }
            status = {
                "current_phase": "Phase 8: Integration Tests",
                "current_state": "execute",
                "current_subphase": "Sub-phase 8.1: Sub-phase advancement test",
                "next_action": "Execute phase",
                "blocked_by": "none",
            }
            contract = self._make_minimal_contract()
            config = {"states": {}, "phases": []}
            context = {"project": "Test", "harness": "generic"}

            code = _try_advance_subphase(
                state_dir, plan, status, contract, config, context
            )

            assert code is None
            assert contract.subphase_name == ""
