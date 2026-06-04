"""Tests for the orchestrated runner skeleton."""

import json
import subprocess
import tempfile
from pathlib import Path

import pytest

from runtime.runner import plan_status, next_gate


@pytest.fixture
def temp_task_dir():
    """Create a temporary task directory with minimal task-state files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        task_dir = Path(tmpdir)
        
        # Create STATUS.md
        (task_dir / "STATUS.md").write_text("""# Status: Test Task

## Artifact Manifest
- artifact_type: status
- parent_task: TASK.md
- current_phase: Phase 5E
- next_required_action: Phase 5E (Runner Skeleton)
- validation_state: `python -m pytest tests/ -v` (PASS)

## Current Phase
Phase 5E (Runner Skeleton)

## Next Action
Phase 5E (Runner Skeleton)

## Blockers
- **ISSUE-1:** Packaging flattening breaks runtime module paths.

## Validation Commands
- `python scripts/validate_skills.py`
- `python -m pytest tests/ -v`
""")
        
        # Create PLAN.md with Phase 5E section
        (task_dir / "PLAN.md").write_text("""# Universal Runtime Enforcement Implementation Plan

## Phase 5E: Runner Skeleton
**Goal:** Implement the smallest CLI runner skeleton if Phase 5D is approved.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 35k-45k
```

**Actions:**
1. Implement read-only commands first (plan-status, next-gate)
2. Implement validation dispatch to CLI validator
3. Reuse Next Prompt Compiler
4. Do not automate model invocation

**Validation:**
- Good task-state fixture reports next gate
- Bad fixture reports exact missing artifacts
- Pytest covers pass/fail runner behavior
""")
        
        # Create CONTEXT.md
        (task_dir / "CONTEXT.md").write_text("""# Context: Runtime Enforcement

## Validation Commands
- `python scripts/validate_skills.py` after skill or shared-reference changes.
- `python scripts/token_budget.py --strict` after skill or shared-reference changes.
- `python -m pytest tests/ -v` after runtime validator, domain-pack, CLI, or runner test changes.
""")
        
        yield task_dir


def test_plan_status_basic(temp_task_dir):
    """Test plan_status returns basic phase information."""
    result = plan_status(temp_task_dir)
    
    assert result['phase'] == 'Phase 5E'
    assert result['status']['current_phase'] == 'Phase 5E'
    assert result['has_status'] is True
    assert result['has_plan'] is True
    assert result['has_context'] is True


def test_next_gate_basic(temp_task_dir):
    """Test next_gate returns validation commands and blockers."""
    result = next_gate(temp_task_dir)
    
    assert result['phase'] == 'Phase 5E'
    assert len(result['blockers']) > 0
    assert 'packaging flattening' in result['blockers'][0].lower()
    assert len(result['validation_commands']) > 0
    # Check that at least one validation command mentions pytest
    validation_text = ' '.join(result['validation_commands']).lower()
    assert 'pytest' in validation_text
    assert result['next_action'] == 'Run validation commands'


def test_plan_status_missing_files():
    """Test plan_status handles missing task-state files gracefully."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = plan_status(Path(tmpdir))
        
        assert result['phase'] is None
        assert result['has_status'] is False
        assert result['has_plan'] is False
        assert result['has_context'] is False


def test_next_gate_missing_files():
    """Test next_gate handles missing task-state files gracefully."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = next_gate(Path(tmpdir))
        
        assert result['phase'] is None
        assert result['blockers'] == []
        assert result['validation_commands'] == []


def test_runner_cli_plan_status(temp_task_dir):
    """Test runner CLI plan-status command via subprocess."""
    result = subprocess.run(
        ['python', '-m', 'runtime.cli', 'plan-status', str(temp_task_dir)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data['phase'] == 'Phase 5E'
    assert data['has_status'] is True
    assert data['has_plan'] is True


def test_runner_cli_next_gate(temp_task_dir):
    """Test runner CLI next-gate command via subprocess."""
    result = subprocess.run(
        ['python', '-m', 'runtime.cli', 'next-gate', str(temp_task_dir)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data['phase'] == 'Phase 5E'
    assert 'blockers' in data
    assert len(data['blockers']) > 0
    assert 'validation_commands' in data


def test_runner_cli_help():
    """Test runner CLI help output."""
    result = subprocess.run(
        ['python', '-m', 'runtime.cli', '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'plan-status' in result.stdout
    assert 'next-gate' in result.stdout


def test_runner_cli_subcommand_help():
    """Test runner CLI subcommand help output."""
    result = subprocess.run(
        ['python', '-m', 'runtime.cli', 'plan-status', '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'task_dir' in result.stdout


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
