"""Tests for orchestrator checkpoint manager."""

import tempfile
from pathlib import Path

import pytest

from orchestrator.checkpoint import (
    create_initial_checkpoint,
    read_checkpoint,
    update_checkpoint,
    validate_checkpoint,
    write_checkpoint,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestReadCheckpoint:
    """Tests for read_checkpoint."""

    def test_read_checkpoint_valid(self):
        """Test reading a valid checkpoint.json."""
        path = FIXTURES_DIR / "task_state_valid"
        cp = read_checkpoint(path)
        assert cp is not None
        assert cp["workflow_id"] is not None

    def test_read_checkpoint_required_missing(self):
        """Test reading missing checkpoint with required=True raises."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(FileNotFoundError):
                read_checkpoint(Path(tmpdir), required=True)

    def test_read_checkpoint_not_required_missing(self):
        """Test reading missing checkpoint with required=False returns None."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            assert read_checkpoint(Path(tmpdir), required=False) is None

    def test_read_checkpoint_invalid_json(self):
        """Test reading malformed checkpoint raises ValueError."""
        path = FIXTURES_DIR / "task_state_invalid_checkpoint"
        with pytest.raises(ValueError, match="Malformed JSON"):
            read_checkpoint(path)


class TestWriteCheckpoint:
    """Tests for write_checkpoint."""

    def test_write_and_read_roundtrip(self):
        """Test write then read returns same data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            data = create_initial_checkpoint("test-wf")
            write_checkpoint(state_dir, data)
            result = read_checkpoint(state_dir)
            assert result["workflow_id"] == "test-wf"
            assert result["current_state"] == "init"

    def test_write_adds_timestamp(self):
        """Test write adds last_updated if missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = Path(tmpdir)
            data = create_initial_checkpoint("test-ts")
            del data["last_updated"]
            write_checkpoint(state_dir, data)
            result = read_checkpoint(state_dir)
            assert "last_updated" in result


class TestUpdateCheckpoint:
    """Tests for update_checkpoint."""

    def test_update_transition(self):
        """Test updating checkpoint on state transition."""
        cp = create_initial_checkpoint("test-update")
        result = update_checkpoint(
            cp, "phase_1", "execute", "audit", {"status": "pass", "artifacts": []}
        )
        assert result["current_state"] == "audit"
        assert result["last_result"]["status"] == "pass"

    def test_update_increments_retry(self):
        """Test retry counter increments when staying in same state."""
        cp = create_initial_checkpoint("test-retry")
        result = update_checkpoint(
            cp, "phase_1", "execute", "execute", {"status": "fail"}
        )
        assert result["counters"]["phase_1"]["retries"] == 1

    def test_update_ralph_cycle_increment(self):
        """Test Ralph cycle counter increments on revise->critique."""
        cp = create_initial_checkpoint("test-ralph")
        result = update_checkpoint(
            cp, "phase_1", "ralph_revise", "ralph_critique", {"status": "pass"}
        )
        assert result["counters"]["phase_1"]["ralph_cycles"] == 1

    def test_update_records_completed_phase(self):
        """Test completed phase recorded on transition to done."""
        cp = create_initial_checkpoint("test-complete")
        result = update_checkpoint(
            cp, "phase_1", "execute", "done", {"status": "pass", "artifacts": []}
        )
        assert len(result["completed_phases"]) == 1
        assert result["completed_phases"][0]["phase"] == "phase_1"

    def test_update_does_not_mutate_input(self):
        """Test update_checkpoint does not mutate the input dict."""
        cp = create_initial_checkpoint("test-immutable")
        original_phase = cp.get("current_phase", "")
        update_checkpoint(cp, "phase_2", "execute", "audit", {"status": "pass"})
        assert cp["current_phase"] == original_phase


class TestValidateCheckpoint:
    """Tests for validate_checkpoint."""

    def test_valid_checkpoint(self):
        """Test valid checkpoint returns no errors."""
        cp = create_initial_checkpoint("test-valid")
        assert validate_checkpoint(cp, {}) == []

    def test_missing_required_field(self):
        """Test checkpoint missing required field returns error."""
        cp = create_initial_checkpoint("test-missing")
        del cp["workflow_id"]
        errors = validate_checkpoint(cp, {})
        assert any("Missing required field" in e for e in errors)

    def test_invalid_state(self):
        """Test checkpoint with invalid state returns error."""
        cp = create_initial_checkpoint("test-bad-state")
        cp["current_state"] = "nonexistent_state"
        errors = validate_checkpoint(cp, {})
        assert any("Invalid state" in e for e in errors)

    def test_negative_counter(self):
        """Test checkpoint with negative counter returns error."""
        cp = create_initial_checkpoint("test-neg")
        cp["counters"]["phase_1"] = {"retries": -1, "ralph_cycles": 0}
        errors = validate_checkpoint(cp, {})
        assert any("Negative retry" in e for e in errors)

    def test_missing_last_result_status(self):
        """Test checkpoint with missing last_result status returns error."""
        cp = create_initial_checkpoint("test-no-status")
        del cp["last_result"]["status"]
        errors = validate_checkpoint(cp, {})
        assert any("Missing 'status' in last_result" in e for e in errors)


class TestCreateInitialCheckpoint:
    """Tests for create_initial_checkpoint."""

    def test_creates_valid_structure(self):
        """Test initial checkpoint has all required fields."""
        cp = create_initial_checkpoint("test-init")
        assert cp["workflow_id"] == "test-init"
        assert cp["current_phase"] == "init"
        assert cp["current_state"] == "init"
        assert cp["version"] == 1
        assert cp["completed_phases"] == []
        assert cp["last_result"]["status"] == "pending"

    def test_custom_version(self):
        """Test initial checkpoint with custom version."""
        cp = create_initial_checkpoint("test-ver", version=2)
        assert cp["version"] == 2
