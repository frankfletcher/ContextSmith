"""
Orchestrator module for ContextSmith workflow execution.

Provides deterministic state machine execution with validation gates,
checkpoint recovery, and harness-agnostic agent dispatch.
"""

from orchestrator.constants import (
    CANONICAL_STATES,
    EXIT_BLOCKED,
    EXIT_CONFIG_ERROR,
    EXIT_CONTINUE,
    EXIT_DONE,
    EXIT_INTERNAL_ERROR,
    EXIT_STATE_INCONSISTENCY,
    TERMINAL_STATES,
)
from orchestrator.exceptions import (
    ConfigError,
    HarnessError,
    HarnessExecutionError,
    HarnessNotFoundError,
    HarnessTimeoutError,
    OrchestratorError,
    StateInconsistency,
    ValidationError,
)
from orchestrator.orchestrator import run, run_workflow

__all__ = [
    "run",
    "run_workflow",
    "EXIT_BLOCKED",
    "EXIT_CONFIG_ERROR",
    "EXIT_CONTINUE",
    "EXIT_DONE",
    "EXIT_INTERNAL_ERROR",
    "EXIT_STATE_INCONSISTENCY",
    "CANONICAL_STATES",
    "TERMINAL_STATES",
    "ConfigError",
    "HarnessError",
    "HarnessExecutionError",
    "HarnessNotFoundError",
    "HarnessTimeoutError",
    "OrchestratorError",
    "StateInconsistency",
    "ValidationError",
]
