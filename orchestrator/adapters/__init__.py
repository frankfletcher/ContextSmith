"""Harness adapters for the orchestrator.

Adapters register themselves with HarnessRegistry at import time.
Call discover_adapters() to discover and import all registered adapters
via package entry points (contextsmith.adapters), falling back to the
hardcoded list if entry points are unavailable (e.g., in development
without pip install -e .).
"""

import importlib
import sys

from orchestrator.adapters.base import (
    HarnessAdapter,
    HarnessExecutionError,
    HarnessNotFoundError,
    HarnessRegistry,
    HarnessResult,
    HarnessTimeoutError,
    StepContract,
)

_FALLBACK_ADAPTERS = ["opencode", "generic"]


def discover_adapters() -> None:
    """Discover and import all registered adapters via entry points.

    Uses importlib.metadata.entry_points with group='contextsmith.adapters'.
    Falls back to a hardcoded list when entry points are unavailable
    (e.g., package not installed or in editable install without build metadata).
    """
    try:
        from importlib.metadata import entry_points

        eps = entry_points(group="contextsmith.adapters")
        discovered = list(eps)
    except (ImportError, TypeError):
        discovered = []

    if discovered:
        for ep in discovered:
            try:
                ep.load()
            except Exception as exc:
                print(
                    f"Warning: failed to load adapter '{ep.name}': {exc}",
                    file=sys.stderr,
                )
    else:
        for name in _FALLBACK_ADAPTERS:
            module_name = f"orchestrator.adapters.{name}"
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
            else:
                importlib.import_module(module_name)


__all__ = [
    "discover_adapters",
    "HarnessAdapter",
    "HarnessExecutionError",
    "HarnessNotFoundError",
    "HarnessRegistry",
    "HarnessResult",
    "HarnessTimeoutError",
    "StepContract",
]
