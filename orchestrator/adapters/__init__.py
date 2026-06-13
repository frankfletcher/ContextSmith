"""Harness adapters for the orchestrator.

Adapters register themselves with HarnessRegistry at import time.
Call discover_adapters() to import all registered adapter modules.
"""

import importlib

from orchestrator.adapters.base import (
    HarnessAdapter,
    HarnessExecutionError,
    HarnessNotFoundError,
    HarnessRegistry,
    HarnessResult,
    HarnessTimeoutError,
    StepContract,
)

ADAPTER_REGISTRY = [
    "opencode",
    "generic",
]


def discover_adapters() -> None:
    """Import all registered adapters to trigger registration."""
    for name in ADAPTER_REGISTRY:
        importlib.import_module(f"orchestrator.adapters.{name}")


__all__ = [
    "ADAPTER_REGISTRY",
    "discover_adapters",
    "HarnessAdapter",
    "HarnessExecutionError",
    "HarnessNotFoundError",
    "HarnessRegistry",
    "HarnessResult",
    "HarnessTimeoutError",
    "StepContract",
]
