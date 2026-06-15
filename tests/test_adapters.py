"""Tests for harness adapters."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from orchestrator.adapters import discover_adapters
from orchestrator.adapters.base import (
    HarnessAdapter,
    HarnessExecutionError,
    HarnessNotFoundError,
    HarnessRegistry,
    HarnessResult,
    HarnessTimeoutError,
    StepContract,
)
from orchestrator.adapters.generic import GenericAdapter
from orchestrator.adapters.opencode import OpenCodeAdapter


@pytest.fixture
def sample_contract():
    """Create a sample StepContract for testing."""
    return StepContract(
        step_id="test-step-1",
        state="execute",
        agent_profile="test-agent",
        permissions="edit",
        inputs=["STATUS.md"],
        expected_outputs=["RESULT.json", "STATUS.md"],
        timeout_s=60,
        max_retries=3,
        ralph_max_cycles=0,
        validation_mode="strict",
        model_pin=None,
        checkpoint_before_run=False,
        prompt_template=None,
        workflow_id="test-workflow",
        task_state_dir="",
        extra={},
    )


@pytest.fixture
def temp_state_dir():
    """Create a temporary state directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestHarnessRegistry:
    """Tests for HarnessRegistry."""

    def test_register_adapter(self):
        """Test adapter registration."""
        # Save current state
        saved_adapters = HarnessRegistry._adapters.copy()

        try:
            # Clear registry for test
            HarnessRegistry._adapters.clear()

            class TestAdapter(HarnessAdapter):
                @property
                def name(self):
                    return "test"

                def validate_environment(self):
                    return []

                def execute(self, contract, state_dir):
                    pass

                def cancel(self, step_id):
                    return False

            HarnessRegistry.register(TestAdapter)
            assert "test" in HarnessRegistry.list_available()
        finally:
            # Restore original state
            HarnessRegistry._adapters.clear()
            HarnessRegistry._adapters.update(saved_adapters)

    def test_get_adapter(self):
        """Test getting adapter by name."""
        discover_adapters()
        adapter = HarnessRegistry.get("generic")
        assert adapter.name == "generic"

    def test_get_nonexistent_adapter(self):
        """Test getting non-existent adapter raises KeyError."""
        discover_adapters()
        with pytest.raises(KeyError):
            HarnessRegistry.get("nonexistent")

    def test_detect_auto(self):
        """Test auto-detection returns any available adapter."""
        discover_adapters()
        adapter = HarnessRegistry.get("auto")
        assert adapter.name in ("opencode", "generic")


class TestGenericAdapter:
    """Tests for GenericAdapter."""

    @staticmethod
    def _execute_generic(sample_contract, temp_state_dir):
        """Execute GenericAdapter with the given contract and state dir."""
        adapter = GenericAdapter()
        return adapter.execute(sample_contract, temp_state_dir)

    def test_name(self):
        """Test adapter name."""
        adapter = GenericAdapter()
        assert adapter.name == "generic"

    def test_validate_environment(self):
        """Test environment validation always passes."""
        adapter = GenericAdapter()
        assert adapter.validate_environment() == []

    def test_execute_writes_pending_prompt(self, sample_contract, temp_state_dir):
        """Test execute writes .pending_prompt.md."""
        sample_contract.task_state_dir = str(temp_state_dir)
        adapter = GenericAdapter()

        # Create NEXT_PROMPT.md
        prompt_file = temp_state_dir / "NEXT_PROMPT.md"
        prompt_file.write_text("# Test Prompt\n\nDo something.")

        adapter.execute(sample_contract, temp_state_dir)

        # Check pending prompt was written
        pending = temp_state_dir / ".pending_prompt.md"
        assert pending.exists()
        assert "Test Prompt" in pending.read_text()

    def test_execute_with_existing_artifacts(self, sample_contract, temp_state_dir):
        """Test execute collects existing artifacts."""
        sample_contract.task_state_dir = str(temp_state_dir)
        adapter = GenericAdapter()

        # Create expected artifacts
        result_path, status_path = sample_contract.expected_outputs
        (temp_state_dir / result_path).write_text(f"Content of {result_path}")
        (temp_state_dir / status_path).write_text(f"Content of {status_path}")

        result = adapter.execute(sample_contract, temp_state_dir)

        assert result.status == "pass"
        assert len(result.artifacts_written) == len(sample_contract.expected_outputs)

    def test_execute_malformed_result_json(self, sample_contract, temp_state_dir):
        """Test malformed RESULT.json does not crash."""
        sample_contract.task_state_dir = str(temp_state_dir)

        # Write malformed RESULT.json
        (temp_state_dir / "RESULT.json").write_text("{invalid json")

        adapter = GenericAdapter()
        result = adapter.execute(sample_contract, temp_state_dir)

        # Should not crash — falls back to artifact presence check
        assert isinstance(result, HarnessResult)
        assert result.status in ("pass", "fail")
        assert result.step_id == sample_contract.step_id

    def test_execute_malformed_fixture_no_crash(self, sample_contract, temp_state_dir):
        """Test malformed fixture file in test mode does not crash."""
        sample_contract.task_state_dir = str(temp_state_dir)
        sample_contract.extra["test_mode"] = True

        # Create malformed fixture file
        fixture_path = temp_state_dir / "fixture.json"
        fixture_path.write_text("{not valid json}")
        sample_contract.extra["fixture"] = str(fixture_path)

        adapter = GenericAdapter()
        result = adapter.execute(sample_contract, temp_state_dir)

        # Should not crash — falls back to "no fixture" result
        assert isinstance(result, HarnessResult)
        assert result.reason == "test mode: no fixture provided"

    def test_execute_test_mode_with_fixture(self, sample_contract, temp_state_dir):
        """Test test mode loads fixture and writes artifacts."""
        sample_contract.task_state_dir = str(temp_state_dir)
        sample_contract.extra["test_mode"] = True

        # Create fixture file
        fixture_data = {
            "status": "pass",
            "reason": "test fixture",
            "artifacts": ["RESULT.json"],
            "artifacts_content": {
                "RESULT.json": '{"status": "pass", "reason": "test"}'
            },
            "validation": {"passed": True},
            "issues": [],
            "next_action": "done",
        }
        fixture_file = temp_state_dir / "fixture.json"
        fixture_file.write_text(json.dumps(fixture_data))
        sample_contract.extra["fixture"] = str(fixture_file)

        result = self._execute_generic(sample_contract, temp_state_dir)

        assert result.status == "pass"
        assert "RESULT.json" in result.artifacts_written
        assert (temp_state_dir / "RESULT.json").exists()

    def test_execute_poll_human_no_response(self, sample_contract, temp_state_dir):
        """Test poll_human returns blocked when no response."""
        sample_contract.task_state_dir = str(temp_state_dir)
        sample_contract.extra["poll_human"] = True

        result = self._execute_generic(sample_contract, temp_state_dir)

        assert result.status == "blocked"
        assert "awaiting human response" in result.reason

    def test_execute_poll_human_with_response(self, sample_contract, temp_state_dir):
        """Test poll_human returns pass when response exists."""
        sample_contract.task_state_dir = str(temp_state_dir)
        sample_contract.extra["poll_human"] = True

        # Create human response
        (temp_state_dir / ".human_response.md").write_text("Human says yes")

        adapter = GenericAdapter()
        result = adapter.execute(sample_contract, temp_state_dir)

        assert result.status == "pass"
        assert result.artifacts["human_response"] == "Human says yes"

    def test_cancel(self):
        """Test cancel always returns False."""
        adapter = GenericAdapter()
        assert adapter.cancel("any-step") is False

    def test_get_capabilities(self):
        """Test capabilities declaration."""
        adapter = GenericAdapter()
        caps = adapter.get_capabilities()

        assert caps["supports_model_pinning"] is False
        assert caps["supports_structured_output"] is True
        assert caps["max_concurrent_steps"] == 1


class TestOpenCodeAdapter:
    """Tests for OpenCodeAdapter."""

    def test_name(self):
        """Test adapter name."""
        adapter = OpenCodeAdapter()
        assert adapter.name == "opencode"

    def test_validate_environment_no_opencode(self):
        """Test validation fails when opencode not on PATH."""
        adapter = OpenCodeAdapter()
        with patch("shutil.which", return_value=None):
            errors = adapter.validate_environment()
            assert len(errors) > 0
            assert "not found" in errors[0]

    def test_validate_environment_with_opencode(self):
        """Test validation passes when opencode on PATH."""
        adapter = OpenCodeAdapter()
        with patch("shutil.which", return_value="/usr/bin/opencode"):
            errors = adapter.validate_environment()
            assert errors == []

    def test_build_command_basic(self, sample_contract):
        """Test command building with basic contract."""
        sample_contract.task_state_dir = "/tmp/test"
        adapter = OpenCodeAdapter()

        cmd = adapter._build_command(sample_contract)

        assert cmd[0] == "opencode"
        assert cmd[1] == "run"
        assert "--agent" in cmd
        assert "test-agent" in cmd
        assert "--format" in cmd
        assert "json" in cmd

    def test_build_command_with_model_pin(self, sample_contract):
        """Test command building with model pin."""
        sample_contract.model_pin = "ollama/qwen3:6b"
        sample_contract.task_state_dir = "/tmp/test"
        adapter = OpenCodeAdapter()

        cmd = adapter._build_command(sample_contract)

        assert "--model" in cmd
        assert "ollama/qwen3:6b" in cmd

    def test_build_command_with_prompt_template(self, sample_contract):
        """Test command building with prompt template."""
        sample_contract.prompt_template = "Do the thing"
        adapter = OpenCodeAdapter()

        cmd = adapter._build_command(sample_contract)

        assert "--prompt" in cmd
        assert "Do the thing" in cmd

    def test_cancel_no_process(self):
        """Test cancel returns False when no process running."""
        adapter = OpenCodeAdapter()
        assert adapter.cancel("nonexistent") is False

    def test_get_capabilities(self):
        """Test capabilities declaration."""
        adapter = OpenCodeAdapter()
        caps = adapter.get_capabilities()

        assert caps["supports_model_pinning"] is True
        assert caps["supports_cancellation"] is True
        assert caps["max_concurrent_steps"] == 1


class TestStepContract:
    """Tests for StepContract dataclass."""

    def test_creation(self, sample_contract):
        """Test StepContract creation."""
        assert sample_contract.step_id == "test-step-1"
        assert sample_contract.state == "execute"
        assert sample_contract.timeout_s == 60

    def test_defaults(self):
        """Test StepContract defaults."""
        contract = StepContract(
            step_id="test",
            state="execute",
            agent_profile="agent",
            permissions="edit",
            inputs=[],
            expected_outputs=[],
            timeout_s=60,
            max_retries=3,
        )

        assert contract.ralph_max_cycles == 0
        assert contract.validation_mode == "strict"
        assert contract.model_pin is None
        assert contract.extra == {}


class TestHarnessResult:
    """Tests for HarnessResult dataclass."""

    def test_creation(self):
        """Test HarnessResult creation."""
        result = HarnessResult(
            status="pass",
            step_id="test-1",
            reason="all good",
            artifacts={"file.txt": "content"},
            artifacts_written=["file.txt"],
            validation={"passed": True},
            issues=[],
            next_action="done",
        )

        assert result.status == "pass"
        assert result.step_id == "test-1"
        assert len(result.artifacts_written) == 1

    def test_defaults(self):
        """Test HarnessResult defaults."""
        result = HarnessResult(
            status="pass",
            step_id="test",
            reason="",
            artifacts={},
            artifacts_written=[],
            validation={},
            issues=[],
            next_action="done",
        )

        assert result.extra == {}


class TestExceptions:
    """Tests for harness exceptions."""

    def test_harness_timeout_error(self):
        """Test HarnessTimeoutError."""
        error = HarnessTimeoutError("step-1", 60)
        assert error.step_id == "step-1"
        assert error.timeout_s == 60
        assert "timed out" in str(error)

    def test_harness_execution_error(self):
        """Test HarnessExecutionError."""
        error = HarnessExecutionError("step-1", "subprocess failed")
        assert error.step_id == "step-1"
        assert error.reason == "subprocess failed"
        assert "execution error" in str(error)

    def test_harness_not_found_error(self):
        """Test HarnessNotFoundError."""
        error = HarnessNotFoundError("no adapter")
        assert "no adapter" in str(error)
