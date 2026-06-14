"""Tests for orchestrator step compiler."""

from orchestrator.adapters.base import StepContract
from orchestrator.step_compiler import (
    _matches_condition,
    compile_step_contract,
    resolve_next_state,
)


def _make_config(state: str, overrides: dict | None = None) -> dict:
    """Create a minimal workflow config for testing."""
    state_def = {
        "agent": "test-agent",
        "permissions": "edit",
        "max_retries": 3,
        "timeout_s": 300,
        "transitions": [
            {"condition": "pass", "target": "audit"},
            {"condition": "fail", "target": "fix"},
            {"condition": "max_retries", "target": "blocked"},
        ],
        "inputs": ["STATUS.md"],
        "expected_outputs": ["RESULT.json"],
    }
    if overrides:
        state_def.update(overrides)
    return {
        "workflow_id": "test-wf",
        "states": {state: state_def},
    }


def _make_plan() -> dict:
    """Create a minimal plan dict."""
    return {"phases": [], "dependencies": {}, "validation_gates": {}}


def _make_context() -> dict:
    """Create a minimal context dict."""
    return {"harness": "generic"}


class TestCompileStepContract:
    """Tests for compile_step_contract."""

    def test_basic_contract(self):
        """Test basic contract compilation."""
        config = _make_config("execute")
        contract = compile_step_contract("execute", config, _make_plan(), _make_context())
        assert isinstance(contract, StepContract)
        assert contract.state == "execute"
        assert contract.agent_profile == "test-agent"
        assert contract.step_id == "test-wf-execute"

    def test_default_values(self):
        """Test contract uses default values when config missing."""
        config = _make_config("execute", {})
        del config["states"]["execute"]["agent"]
        del config["states"]["execute"]["permissions"]
        del config["states"]["execute"]["timeout_s"]
        del config["states"]["execute"]["max_retries"]
        contract = compile_step_contract("execute", config, _make_plan(), _make_context())
        assert contract.agent_profile == "contextsmith-default"
        assert contract.permissions == "read-only"
        assert contract.timeout_s == 300
        assert contract.max_retries == 3

    def test_model_pin_resolution(self):
        """Test model_pin is read from state config."""
        config = _make_config("execute", {"model_pin": "qwen3:6b"})
        contract = compile_step_contract("execute", config, _make_plan(), _make_context())
        assert contract.model_pin == "qwen3:6b"

    def test_model_pin_absent(self):
        """Test model_pin is None when not in config."""
        config = _make_config("execute")
        contract = compile_step_contract("execute", config, _make_plan(), _make_context())
        assert contract.model_pin is None

    def test_ralph_max_cycles_resolution(self):
        """Test ralph_max_cycles is read from state config."""
        config = _make_config("execute", {"ralph_max_cycles": 5})
        contract = compile_step_contract("execute", config, _make_plan(), _make_context())
        assert contract.ralph_max_cycles == 5

    def test_ralph_max_cycles_default(self):
        """Test ralph_max_cycles defaults to 0."""
        config = _make_config("execute")
        contract = compile_step_contract("execute", config, _make_plan(), _make_context())
        assert contract.ralph_max_cycles == 0

    def test_ralph_max_cycles_zero(self):
        """Test ralph_max_cycles=0 disables Ralph loop."""
        config = _make_config("execute", {"ralph_max_cycles": 0})
        contract = compile_step_contract("execute", config, _make_plan(), _make_context())
        assert contract.ralph_max_cycles == 0

    def test_timeout_s_resolution(self):
        """Test timeout_s is read from state config."""
        config = _make_config("execute", {"timeout_s": 120})
        contract = compile_step_contract("execute", config, _make_plan(), _make_context())
        assert contract.timeout_s == 120

    def test_timeout_s_default(self):
        """Test timeout_s defaults to 300."""
        config = _make_config("execute", {})
        del config["states"]["execute"]["timeout_s"]
        contract = compile_step_contract("execute", config, _make_plan(), _make_context())
        assert contract.timeout_s == 300

    def test_validation_mode_resolution(self):
        """Test validation_mode is read from state config."""
        config = _make_config("execute", {"validation_mode": "relaxed"})
        contract = compile_step_contract("execute", config, _make_plan(), _make_context())
        assert contract.validation_mode == "relaxed"

    def test_checkpoint_before_run_resolution(self):
        """Test checkpoint_before_run is read from state config."""
        config = _make_config("execute", {"checkpoint_before_run": True})
        contract = compile_step_contract("execute", config, _make_plan(), _make_context())
        assert contract.checkpoint_before_run is True


class TestResolveNextState:
    """Tests for resolve_next_state."""

    def test_pass_transition(self):
        """Test pass condition advances to target."""
        config = _make_config("execute")
        next_state = resolve_next_state(
            "execute", "phase_1",
            {"status": "pass"}, {"passed": True},
            config, {},
        )
        assert next_state == "audit"

    def test_fail_transition(self):
        """Test fail condition goes to fix target."""
        config = _make_config("execute")
        next_state = resolve_next_state(
            "execute", "phase_1",
            {"status": "fail"}, {"passed": False},
            config, {},
        )
        assert next_state == "fix"

    def test_max_retries_blocked(self):
        """Test max_retries reached transitions to blocked."""
        config = _make_config("execute", {
            "transitions": [
                {"condition": "pass", "target": "audit"},
                {"condition": "fail", "target": "execute"},
                {"condition": "max_retries", "target": "blocked"},
            ],
        })
        counters = {"phase_1": {"retries": 3, "ralph_cycles": 0}}
        next_state = resolve_next_state(
            "execute", "phase_1",
            {"status": "fail"}, {"passed": False},
            config, counters,
        )
        assert next_state == "blocked"

    def test_no_match_goes_blocked(self):
        """Test no matching condition transitions to blocked."""
        config = _make_config("execute", {
            "transitions": [{"condition": "never", "target": "done"}],
        })
        next_state = resolve_next_state(
            "execute", "phase_1",
            {"status": "pass"}, {"passed": True},
            config, {},
        )
        assert next_state == "blocked"

    def test_ralph_complete_condition(self):
        """Test ralph_complete condition when cycle count met."""
        config = _make_config("execute", {
            "ralph_max_cycles": 3,
            "transitions": [
                {"condition": "ralph_complete", "target": "done"},
            ],
        })
        counters = {"phase_1": {"retries": 0, "ralph_cycles": 3}}
        next_state = resolve_next_state(
            "execute", "phase_1",
            {"status": "pass"}, {"passed": True},
            config, counters,
        )
        assert next_state == "done"

    def test_output_valid_condition(self):
        """Test output_valid condition matches validation."""
        config = _make_config("execute", {
            "transitions": [
                {"condition": "output_valid", "target": "done"},
                {"condition": "output_invalid", "target": "fix"},
            ],
        })
        next_state = resolve_next_state(
            "execute", "phase_1",
            {"status": "pass"}, {"passed": True},
            config, {},
        )
        assert next_state == "done"

    def test_output_invalid_condition(self):
        """Test output_invalid condition matches validation fail."""
        config = _make_config("execute", {
            "transitions": [
                {"condition": "output_valid", "target": "done"},
                {"condition": "output_invalid", "target": "fix"},
            ],
        })
        next_state = resolve_next_state(
            "execute", "phase_1",
            {"status": "fail"}, {"passed": False},
            config, {},
        )
        assert next_state == "fix"


class TestMatchesCondition:
    """Tests for _matches_condition."""

    def test_pass_true(self):
        """Test 'pass' condition matches when status is pass."""
        assert _matches_condition(
            "pass", "execute", "phase_1",
            {"status": "pass"}, {"passed": True}, {}, {},
        )

    def test_pass_false(self):
        """Test 'pass' condition does not match when status is fail."""
        assert not _matches_condition(
            "pass", "execute", "phase_1",
            {"status": "fail"}, {"passed": False}, {}, {},
        )

    def test_fail_true(self):
        """Test 'fail' condition matches when status is fail."""
        assert _matches_condition(
            "fail", "execute", "phase_1",
            {"status": "fail"}, {"passed": False}, {}, {},
        )

    def test_always_true(self):
        """Test 'always' condition always matches."""
        assert _matches_condition(
            "always", "execute", "phase_1",
            {"status": "pass"}, {"passed": True}, {}, {},
        )

    def test_never_false(self):
        """Test 'never' condition never matches."""
        assert not _matches_condition(
            "never", "execute", "phase_1",
            {"status": "pass"}, {"passed": True}, {}, {},
        )

    def test_unknown_condition(self):
        """Test unknown condition returns False."""
        assert not _matches_condition(
            "unknown_condition", "execute", "phase_1",
            {"status": "pass"}, {"passed": True}, {}, {},
        )
