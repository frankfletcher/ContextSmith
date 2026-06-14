"""Tests for orchestrator state reader."""

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"
TASK_STATE_VALID = FIXTURES_DIR / "task_state_valid"


class TestReadStatus:
    """Tests for read_status."""

    def test_read_status_valid(self):
        """Test reading a valid STATUS.md."""
        from orchestrator.state_reader import read_status

        status = read_status(TASK_STATE_VALID)
        assert status["current_phase"] is not None
        assert status["current_state"] is not None
        assert "next_action" in status

    def test_read_status_missing_file(self):
        """Test reading STATUS.md that doesn't exist."""
        from orchestrator.state_reader import read_status

        with pytest.raises(FileNotFoundError):
            read_status(FIXTURES_DIR / "task_state_missing_status")

    def test_read_status_missing_sections(self):
        """Test reading STATUS.md with missing required sections."""
        import tempfile
        from pathlib import Path
        from orchestrator.state_reader import read_status

        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "STATUS.md"
            p.write_text("# Status\n\n## Some Section\ncontent\n")
            with pytest.raises(ValueError, match="Missing required section"):
                read_status(Path(tmpdir))


class TestReadPlan:
    """Tests for read_plan."""

    def test_read_plan_valid(self):
        """Test reading a valid PLAN.md."""
        from orchestrator.state_reader import read_plan

        plan = read_plan(TASK_STATE_VALID)
        assert isinstance(plan["phases"], list)
        assert isinstance(plan["validation_gates"], dict)

    def test_read_plan_missing_file(self):
        """Test reading PLAN.md that doesn't exist."""
        import tempfile
        from orchestrator.state_reader import read_plan

        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(FileNotFoundError):
                read_plan(Path(tmpdir))

    def test_read_plan_empty(self):
        """Test reading empty PLAN.md."""
        from orchestrator.state_reader import read_plan

        plan = read_plan(FIXTURES_DIR / "task_state_empty_plan")
        assert plan["phases"] == []


class TestReadContext:
    """Tests for read_context."""

    def test_read_context_valid(self):
        """Test reading a valid CONTEXT.md."""
        from orchestrator.state_reader import read_context

        context = read_context(TASK_STATE_VALID)
        assert "project" in context
        assert "constraints" in context
        assert "assumptions" in context

    def test_read_context_missing_file(self):
        """Test reading CONTEXT.md that doesn't exist."""
        import tempfile
        from orchestrator.state_reader import read_context

        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(FileNotFoundError):
                read_context(Path(tmpdir))
