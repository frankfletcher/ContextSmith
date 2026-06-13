"""Custom exceptions for the orchestrator module."""

from orchestrator.adapters.base import (
    HarnessExecutionError,
    HarnessNotFoundError,
    HarnessTimeoutError,
)


class OrchestratorError(Exception):
    """Base exception for orchestrator errors."""

    pass


class StateInconsistency(OrchestratorError):
    """STATUS.md does not match checkpoint.json."""

    pass


class ConfigError(OrchestratorError):
    """Raised when workflow config is invalid or missing required fields."""

    pass


class ValidationError(OrchestratorError):
    """Raised when artifact validation fails."""

    pass


class HarnessError(OrchestratorError):
    """Raised when harness adapter encounters an error."""

    pass


__all__ = [
    "ConfigError",
    "HarnessError",
    "HarnessExecutionError",
    "HarnessNotFoundError",
    "HarnessTimeoutError",
    "OrchestratorError",
    "StateInconsistency",
    "ValidationError",
]
