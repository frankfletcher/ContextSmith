"""Adapter base classes for orchestrator.

Defines StepContract, HarnessResult, HarnessAdapter ABC, HarnessRegistry,
and error types.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class StepContract:
    """Bounded step definition compiled by the orchestrator."""

    step_id: str
    state: str
    agent_profile: str
    permissions: str
    inputs: list[str]
    expected_outputs: list[str]
    timeout_s: int
    max_retries: int
    ralph_max_cycles: int = 0
    validation_mode: str = "strict"
    model_pin: Optional[str] = None
    checkpoint_before_run: bool = False
    prompt_template: Optional[str] = None
    workflow_id: str = ""
    task_state_dir: str = ""
    extra: dict = field(default_factory=dict)


@dataclass
class HarnessResult:
    """Structured result returned by the harness after execution."""

    status: str
    step_id: str
    reason: str
    artifacts: dict[str, str]
    artifacts_written: list[str]
    validation: dict
    issues: list[str]
    next_action: str
    extra: dict = field(default_factory=dict)


class HarnessTimeoutError(Exception):
    """Raised when the harness exceeds the step timeout."""

    def __init__(self, step_id: str, timeout_s: int):
        self.step_id = step_id
        self.timeout_s = timeout_s
        super().__init__(f"Step {step_id} timed out after {timeout_s}s")


class HarnessExecutionError(Exception):
    """Raised when the harness itself fails (not the agent)."""

    def __init__(self, step_id: str, reason: str):
        self.step_id = step_id
        self.reason = reason
        super().__init__(f"Harness execution error for {step_id}: {reason}")


class HarnessNotFoundError(Exception):
    """Raised when no harness adapter is available or can be auto-detected."""

    def __init__(self, message: str = "No harness adapter available"):
        self.message = message
        super().__init__(message)


class HarnessAdapter(ABC):
    """Base class for all harness adapters."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique harness identifier.

        Must match the 'harness' field in workflow config.
        """
        ...

    @abstractmethod
    def validate_environment(self) -> list[str]:
        """Check that the harness runtime is available.

        Returns a list of error messages. Empty list means the environment is ready.
        """
        ...

    @abstractmethod
    def execute(self, contract: StepContract, state_dir: Path) -> HarnessResult:
        """Execute one bounded step.

        Translates the StepContract into harness-native commands, launches the
        agent or runtime, waits for completion or timeout, reads RESULT.json
        from state_dir, collects artifacts, and returns a structured result.

        Must raise HarnessTimeoutError on timeout.
        Must raise HarnessExecutionError on harness-level failure.
        """
        ...

    @abstractmethod
    def cancel(self, step_id: str) -> bool:
        """Attempt to cancel a running step.

        Returns True if cancellation was confirmed, False otherwise.
        """
        ...

    def get_capabilities(self) -> dict:
        """Return what this harness supports. Used for capability negotiation."""
        return {
            "supports_model_pinning": False,
            "supports_step_caps": True,
            "supports_permission_levels": True,
            "max_concurrent_steps": 1,
            "supports_structured_output": False,
            "supports_cancellation": False,
        }


class HarnessRegistry:
    """Registry for harness adapters. Adapters register at import time."""

    _adapters: dict[str, HarnessAdapter] = {}

    @classmethod
    def register(cls, adapter_class: type[HarnessAdapter]) -> None:
        """Register a harness adapter class. Called at module import time."""
        instance = adapter_class()
        cls._adapters[instance.name] = instance

    @classmethod
    def get(cls, name: str) -> HarnessAdapter:
        """Get a registered adapter by name. Raises KeyError if not found."""
        if name == "auto":
            return cls._detect_auto()
        if name not in cls._adapters:
            raise KeyError(f"No harness adapter registered for '{name}'")
        return cls._adapters[name]

    @classmethod
    def list_available(cls) -> list[str]:
        """Return list of registered adapter names."""
        return list(cls._adapters.keys())

    @classmethod
    def _detect_auto(cls) -> HarnessAdapter:
        """Auto-detect: check environment for known harness runtimes."""
        for name, adapter in cls._adapters.items():
            errors = adapter.validate_environment()
            if not errors:
                return adapter
        raise HarnessNotFoundError("No harness adapter available for auto-detection")
