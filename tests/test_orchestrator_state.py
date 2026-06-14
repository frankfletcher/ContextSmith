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


_PHASE_TREE_CONTENT = """### Phase 1: Schema Registry
- Status: completed

#### Sub-phase 1.1: Core schema
- Status: completed
- Context Budget: 32k
- Validation: yaml_valid
- Tasks:
  - [x] Define structure
  - [x] Write YAML

#### Sub-phase 1.2: Validation
- Status: in_progress
- Context Budget: 48k
- Dependency: Sub-phase 1.1
- Tasks:
  - [x] Add load function
  - [ ] Add validate function

### Phase 2: Implementation
- Status: pending
- Agent: contextsmith-engineer

#### Sub-phase 2.1: Core functions
- Status: pending
- Context Budget: 64k
- Tasks:
  - [ ] Implement
  - [ ] Test
"""


class TestParsePhaseTree:
    """Tests for _parse_phase_tree."""

    def test_parse_hierarchical(self):
        """Test parsing hierarchical phase tree with sub-phases and tasks."""
        from orchestrator.state_reader import _parse_phase_tree

        phases = _parse_phase_tree(_PHASE_TREE_CONTENT)
        assert len(phases) == 2

        p1 = phases[0]
        assert "Phase 1" in p1["name"]
        assert p1["status"] == "completed"
        assert len(p1["subphases"]) == 2

        sp1 = p1["subphases"][0]
        assert "Sub-phase 1.1" in sp1["name"]
        assert sp1["status"] == "completed"
        assert sp1["metadata"].get("Context Budget") == "32k"
        assert len(sp1["tasks"]) == 2
        assert sp1["tasks"][0]["done"] is True
        assert sp1["tasks"][1]["done"] is True
        assert sp1["task_completion"] == 1.0

        sp2 = p1["subphases"][1]
        assert "Sub-phase 1.2" in sp2["name"]
        assert sp2["status"] == "in_progress"
        assert sp2["metadata"].get("Dependency") == "Sub-phase 1.1"
        assert len(sp2["tasks"]) == 2
        assert sp2["tasks"][0]["done"] is True
        assert sp2["tasks"][1]["done"] is False
        assert sp2["task_completion"] == 0.5

        p2 = phases[1]
        assert "Phase 2" in p2["name"]
        assert p2["status"] == "pending"
        assert p2["metadata"].get("Agent") == "contextsmith-engineer"
        assert len(p2["subphases"]) == 1

    def test_parse_flat_format(self):
        """Test parsing flat checkbox format (backward compat)."""
        from orchestrator.state_reader import _parse_phase_tree

        flat = "- [x] Phase 1: Init\n- [ ] Phase 2: Execute\n- [ ] Phase 3: Audit"
        phases = _parse_phase_tree(flat)
        assert len(phases) == 3
        assert phases[0]["status"] == "completed"
        assert phases[1]["status"] == "pending"
        assert phases[2]["status"] == "pending"
        assert all(len(p["subphases"]) == 0 for p in phases)

    def test_parse_empty(self):
        """Test parsing empty content returns empty list."""
        from orchestrator.state_reader import _parse_phase_tree

        assert _parse_phase_tree("") == []
        assert _parse_phase_tree("  ") == []

    def test_extract_context_budget(self):
        """Test parsing context budget from metadata."""
        from orchestrator.state_reader import _parse_phase_tree

        phases = _parse_phase_tree(_PHASE_TREE_CONTENT)
        p1_sp1 = phases[0]["subphases"][0]
        assert p1_sp1["metadata"].get("Context Budget") == "32k"
        p1_sp2 = phases[0]["subphases"][1]
        assert p1_sp2["metadata"].get("Context Budget") == "48k"
