# Next Prompt

You are implementing Phase 2a of the Deep Determinism project: creating the orchestrator Python package structure.

## Current Status

- Phase: 2a of 6 (Create orchestrator package structure)
- State: execute
- Completed: Phase 1 (all 4 sub-phases PASS)
- Retries remaining: 3

## Your Task

Create the orchestrator Python package with __init__.py and basic structure.

### Step 1: Read the spec files

Read these files to understand the orchestrator structure:
- `.agent_work/ideation/deep_determinism/orchestrator_idea.md` (function reference section)
- `.agent_work/ideation/deep_determinism/implementation_guide.md` (if exists)

### Step 2: Create orchestrator directory

Create `orchestrator/` directory at the project root.

### Step 3: Create __init__.py

Create `orchestrator/__init__.py` with public API exports:

```python
"""
Orchestrator module for ContextSmith workflow execution.

Provides deterministic state machine execution with validation gates,
checkpoint recovery, and harness-agnostic agent dispatch.
"""

from orchestrator.orchestrator import run, run_workflow
from orchestrator.cli import init, validate, inspect

__all__ = ["run", "run_workflow", "init", "validate", "inspect"]
```

Note: The imports will fail initially because orchestrator.py and cli.py don't exist yet. That's expected — they'll be created in phases 2e and 2f. For now, create stub files or comment out the imports.

### Step 4: Create constants.py

Create `orchestrator/constants.py` with exit codes and canonical state names:

```python
"""Exit codes and canonical state names for the orchestrator."""

# Exit codes
EXIT_DONE = 0
EXIT_BLOCKED = 1
EXIT_CONTINUE = 2

# Canonical state names
STATE_INIT = "init"
STATE_PLAN = "plan"
STATE_EXECUTE = "execute"
STATE_AUDIT = "audit"
STATE_FIX = "fix"
STATE_VALIDATE = "validate"
STATE_RALPH_CRITIQUE = "ralph_critique"
STATE_RALPH_REVISE = "ralph_revise"
STATE_CLOSEOUT = "closeout"
STATE_DONE = "done"
STATE_BLOCKED = "blocked"

# All canonical states
CANONICAL_STATES = [
    STATE_INIT,
    STATE_PLAN,
    STATE_EXECUTE,
    STATE_AUDIT,
    STATE_FIX,
    STATE_VALIDATE,
    STATE_RALPH_CRITIQUE,
    STATE_RALPH_REVISE,
    STATE_CLOSEOUT,
    STATE_DONE,
    STATE_BLOCKED,
]
```

### Step 5: Create exceptions.py

Create `orchestrator/exceptions.py` with custom exceptions:

```python
"""Custom exceptions for the orchestrator module."""


class OrchestratorError(Exception):
    """Base exception for orchestrator errors."""
    pass


class StateInconsistency(OrchestratorError):
    """Raised when task state is inconsistent (e.g., STATUS.md doesn't match checkpoint.json)."""
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


class HarnessTimeoutError(HarnessError):
    """Raised when harness adapter times out."""
    pass
```

### Step 6: Verify import works

Test that the package can be imported:

```bash
python3 -c "from orchestrator.constants import EXIT_DONE, CANONICAL_STATES; print('constants OK')"
python3 -c "from orchestrator.exceptions import OrchestratorError, StateInconsistency; print('exceptions OK')"
```

Note: The `from orchestrator import run` import will fail until phases 2e and 2f are complete. That's expected.

## Input Files

- `.agent_work/ideation/deep_determinism/orchestrator_idea.md` — function reference
- `.agent_work/ideation/deep_determinism/implementation_guide.md` — implementation patterns (if exists)

## Output Requirements

- `orchestrator/__init__.py` — public API exports (may have commented imports initially)
- `orchestrator/constants.py` — exit codes and canonical state names
- `orchestrator/exceptions.py` — custom exception classes

## Constraints

- Python 3.10+
- PEP 8 style
- No new dependencies without approval
- Keep files small (see PLAN.md file size constraints)
- All public functions must have docstrings

## Validation

After completing this phase:
1. `orchestrator/` directory exists
2. All 3 files exist and are non-empty
3. `python3 -c "from orchestrator.constants import EXIT_DONE"` succeeds
4. `python3 -c "from orchestrator.exceptions import OrchestratorError"` succeeds

## Self-Audit

Before writing RESULT.json, check:
1. All expected output files exist and are non-empty
2. Python imports work without errors
3. No TODOs, FIXMEs, or placeholders in written files
4. All public functions have docstrings
5. Code follows PEP 8 style

If all checks pass → write RESULT.json with `status: "pass"`
If any check fails → fix the issue, then re-audit

## Educational Report

After completing the phase, append to `EDUCATIONAL_REPORT.md` explaining what you did, why it matters, and how it works.

## Audit Report

Write `AUDIT_REPORT.md` using the full A-F rubric (Completeness, Correctness, Consistency, Documentation, Validation, File Safety).

## Checklist

Check off the completed items in `CHECKLIST.md` under "Sub-phase 2a: Create orchestrator package structure".

## Context (from previous phases)

Phase 1 completed successfully:
- Phase 1a: workflow config schema validation — PASS
- Phase 1b: agent config schema validation — PASS
- Phase 1c: invalid fixtures created — PASS
- Phase 1d: task-state fixtures created — PASS

All test fixtures are in place for Phase 2 implementation.
