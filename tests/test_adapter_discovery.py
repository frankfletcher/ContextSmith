"""Tests for adapter discovery via entry points."""

import importlib
from unittest.mock import patch, MagicMock

import pytest

from orchestrator.adapters import discover_adapters
from orchestrator.adapters.base import HarnessRegistry
from orchestrator.adapters.generic import GenericAdapter
from orchestrator.adapters.opencode import OpenCodeAdapter


def test_discover_via_entry_points():
    """discover_adapters() registers both built-in adapters via entry points."""
    HarnessRegistry._adapters.clear()

    mock_entry_point = MagicMock()
    mock_entry_point.name = "opencode"
    mock_entry_point.load.return_value = None

    opencode_module = MagicMock()
    opencode_adapter = OpenCodeAdapter()

    def load_opencode():
        HarnessRegistry.register(OpenCodeAdapter)
        return opencode_module

    mock_entry_point.load.side_effect = load_opencode

    mock_entry_point2 = MagicMock()
    mock_entry_point2.name = "generic"
    mock_entry_point2.load.return_value = None

    generic_adapter = GenericAdapter()

    def load_generic():
        HarnessRegistry.register(GenericAdapter)
        return MagicMock()

    mock_entry_point2.load.side_effect = load_generic

    with patch("importlib.metadata.entry_points", return_value=[mock_entry_point, mock_entry_point2]):
        discover_adapters()

    assert "opencode" in HarnessRegistry._adapters
    assert "generic" in HarnessRegistry._adapters
    assert isinstance(HarnessRegistry.get("opencode"), OpenCodeAdapter)
    assert isinstance(HarnessRegistry.get("generic"), GenericAdapter)


def test_discover_falls_back_to_hardcoded():
    """discover_adapters() falls back to hardcoded list when entry points unavailable."""
    HarnessRegistry._adapters.clear()

    with patch("importlib.metadata.entry_points", side_effect=ImportError):
        discover_adapters()

    registered = HarnessRegistry.list_available()
    assert "opencode" in registered
    assert "generic" in registered


def test_get_opencode():
    """HarnessRegistry.get('opencode') returns OpenCodeAdapter."""
    HarnessRegistry._adapters.clear()
    HarnessRegistry.register(OpenCodeAdapter)
    adapter = HarnessRegistry.get("opencode")
    assert isinstance(adapter, OpenCodeAdapter)
    assert adapter.name == "opencode"


def test_get_generic():
    """HarnessRegistry.get('generic') returns GenericAdapter."""
    HarnessRegistry._adapters.clear()
    HarnessRegistry.register(GenericAdapter)
    adapter = HarnessRegistry.get("generic")
    assert isinstance(adapter, GenericAdapter)
    assert adapter.name == "generic"


def test_get_unknown_harness_raises_key_error():
    """HarnessRegistry.get() raises KeyError for unknown harness name."""
    HarnessRegistry._adapters.clear()
    with pytest.raises(KeyError, match="No harness adapter registered for 'nonexistent'"):
        HarnessRegistry.get("nonexistent")


def test_discover_via_entry_points_registers_both():
    """Entry-point discovery registers opencode and generic."""
    HarnessRegistry._adapters.clear()

    mock_ep_open = MagicMock()
    mock_ep_open.name = "opencode"
    mock_ep_open.load.side_effect = lambda: HarnessRegistry.register(OpenCodeAdapter)

    mock_ep_gen = MagicMock()
    mock_ep_gen.name = "generic"
    mock_ep_gen.load.side_effect = lambda: HarnessRegistry.register(GenericAdapter)

    with patch("importlib.metadata.entry_points", return_value=[mock_ep_open, mock_ep_gen]):
        discover_adapters()

    assert "opencode" in HarnessRegistry._adapters
    assert "generic" in HarnessRegistry._adapters
