# Next Prompt: Phase 4a — Implement File Validators (Test-First)

You are implementing Phase 4a of the Deep Determinism project: implementing file validators using a test-first approach.

## Environment Setup

This project uses **uv** for Python dependency management. All Python commands must use `uv run`:

```bash
# If you haven't already, sync the environment
uv sync

# All Python commands use uv run
uv run python <script>
uv run pytest <tests>
uv run ruff check <files>
uv run ruff format <files>
```

## Current Status

- Phase: 4a of 6
- State: execute
- Completed: Phase 1 (all 4 sub-phases PASS), Phase 2 (all 6 sub-phases PASS + bugfix), Phase 3 (all 3 sub-phases PASS), Phase 3.5 (integration, bug fixes, ruff, uv)
- Retries remaining: 3

## Your Task

Implement file validation functions in `orchestrator/validators.py` using a **test-first approach**. Write tests before implementation.

## Files to Read

- `.agent_work/ideation/deep_determinism/state_artifact_strategy.md` (validation pseudocode)
- `.agent_work/ideation/deep_determinism/orchestrator_idea.md` (validation section)

## Implementation Requirements

### 1. Create `tests/test_validators.py` FIRST

Write comprehensive tests for all validators before implementing them. This is test-driven development.

#### Test Cases to Write

```python
# File existence tests
def test_validate_file_exists_success():
    """Test file exists returns [] when file exists."""
    
def test_validate_file_exists_failure():
    """Test file exists returns error when file missing."""

# File non-empty tests
def test_validate_file_nonempty_success():
    """Test file non-empty returns [] when file has content."""
    
def test_validate_file_nonempty_failure():
    """Test file non-empty returns error when file empty."""

# Section validation tests
def test_validate_required_sections_all_present():
    """Test all sections present returns []."""
    
def test_validate_required_sections_missing():
    """Test missing sections returns errors."""

# Artifact validation tests
def test_validate_artifact_all_checks_pass():
    """Test artifact passes all checks."""
    
def test_validate_artifact_missing_file():
    """Test artifact fails when file missing."""
    
def test_validate_artifact_empty_file():
    """Test artifact fails when file empty."""
    
def test_validate_artifact_missing_sections():
    """Test artifact fails when sections missing."""

# Batch validation tests
def test_validate_artifacts_all_pass():
    """Test all artifacts pass validation."""
    
def test_validate_artifacts_some_fail():
    """Test some artifacts fail validation."""
    
def test_validate_artifacts_with_config():
    """Test validation uses config for section requirements."""
```

### 2. Create `orchestrator/validators.py`

Implement these validation functions to make the tests pass:

#### File Validators
```python
def validate_file_exists(path: Path) -> list[str]:
    """Check if file exists. Returns [] if exists, [error] if not."""
    
def validate_file_nonempty(path: Path) -> list[str]:
    """Check if file is non-empty. Returns [] if non-empty, [error] if empty."""
    
def validate_required_sections(path: Path, sections: list[str]) -> list[str]:
    """Check if file contains required sections. Returns [] if all present, [errors] if missing."""
    
def validate_artifact(file_path: Path, required_sections: list[str] = None) -> list[str]:
    """Combine all checks: exists, non-empty, sections present. Returns list of errors."""
    
def validate_artifacts(state_dir: Path, expected_outputs: list[str], config: dict) -> dict:
    """Validate all expected artifacts from a step contract.
    
    Returns:
        {
            "passed": bool,
            "failures": list[str],
            "files_checked": int,
            "files_passed": int
        }
    """
```

### 3. Implementation Details

#### Error Message Format
All validators return lists of strings in this format:
```python
# Success
return []

# Failure
return ["Missing required file: STATUS.md"]
return ["Missing required section '## Current Phase' in STATUS.md"]
return ["File is empty: PLAN.md"]
```

Format: `"<error type>: <details>"`

Error types:
- `Missing required file`
- `Missing required section`
- `File is empty`

#### Section Detection
For Markdown files, detect sections by looking for ATX-style headings (`## Section Name`).

```python
def _extract_sections(content: str) -> list[str]:
    """Extract section names from Markdown content."""
    sections = []
    for line in content.splitlines():
        if line.startswith("## "):
            sections.append(line[3:].strip())
    return sections
```

#### Artifact Validation
The `validate_artifacts()` function should:
1. Iterate through `expected_outputs` from the step contract
2. For each artifact, call `validate_artifact()` with required sections from config
3. Collect all errors
4. Return summary dict with passed/failures/counts

### 4. Integration with Orchestrator

The validators will be called by `orchestrator.py` after harness execution to validate artifacts before advancing to the next state.

```python
# In orchestrator.py run() function
from orchestrator.validators import validate_artifacts

validation_result = validate_artifacts(state_dir, step_contract.expected_outputs, config)
validation = {
    "passed": validation_result["passed"],
    "failures": validation_result["failures"],
}
```

## Expected Outputs

- `tests/test_validators.py` — comprehensive test suite (write FIRST)
- `orchestrator/validators.py` — all validation functions (write SECOND to make tests pass)

## Validation

After implementation:

1. `uv run pytest tests/test_validators.py -v` passes (all tests green)
2. `uv run python -c "from orchestrator.validators import validate_artifacts"` succeeds
3. Test with valid fixture: `validate_artifacts(tests/fixtures/task_state_valid, ["STATUS.md", "PLAN.md"], {})` returns `{"passed": True, ...}`
4. Test with missing file: `validate_artifacts(tests/fixtures/task_state_missing_status, ["STATUS.md"], {})` returns `{"passed": False, "failures": ["Missing required file: STATUS.md"], ...}`
5. `uv run ruff check orchestrator/validators.py --select E,F,W,I` passes
6. `uv run ruff format orchestrator/validators.py --check` passes

## Constraints

- Python 3.10+
- PEP 8 style (enforced by ruff)
- No new dependencies (use only stdlib: pathlib)
- All public functions must have docstrings
- Error messages follow the format: `"<error type>: <details>"`
- **Test-first**: Write tests before implementation
- **uv environment**: All commands must use `uv run`

## Self-Audit

Before writing RESULT.json:

1. All expected output files exist and are non-empty
2. All tests pass: `uv run pytest tests/test_validators.py -v`
3. Python imports work without errors: `uv run python -c "from orchestrator.validators import validate_artifacts"`
4. No TODOs, FIXMEs, or placeholders in written files
5. All public functions have docstrings
6. Code follows PEP 8 style: `uv run ruff check orchestrator/validators.py --select E,F,W,I`
7. Code is properly formatted: `uv run ruff format orchestrator/validators.py --check`
8. Error messages follow the correct format
9. Validators work with test fixtures

If all checks pass → write RESULT.json with status: "pass"
If any check fails → fix the issue, then re-audit

## Educational Report

After completing the phase, append to `EDUCATIONAL_REPORT.md` explaining what you did, why it matters, and how it works.

## Audit Report

Append to `AUDIT_REPORT.md` using the full A-F rubric (Completeness, Correctness, Consistency, Documentation, Validation, File Safety).

## Checklist

Check off the completed items in `CHECKLIST.md` under "Sub-phase 4a: Implement file validators".

## Context (from previous phases)

Phase 1 completed: schemas validated, test fixtures created.
Phase 2 completed: core orchestrator module with state machine, loop, checkpoint, CLI.
Phase 3 completed: harness adapters (generic, opencode) with StepContract, HarnessResult, HarnessAdapter ABC, HarnessRegistry.
Phase 3.5 completed: adapters wired into orchestrator, all bugs fixed, logging added, 28 adapter tests passing.

The orchestrator package now has:
- `orchestrator/__init__.py` — public API exports
- `orchestrator/constants.py` — exit codes, canonical states, terminal states
- `orchestrator/exceptions.py` — OrchestratorError hierarchy, re-exports HarnessTimeoutError, HarnessExecutionError, HarnessNotFoundError
- `orchestrator/state_reader.py` — parse task-state artifacts
- `orchestrator/checkpoint.py` — checkpoint management with atomic writes
- `orchestrator/step_compiler.py` — StepContract compilation and state transitions
- `orchestrator/orchestrator.py` — main loop with run(), run_workflow(), should_stop(), register_signal_handlers() — NOW WIRED TO ADAPTERS
- `orchestrator/cli.py` — CLI with init, validate, inspect, diff, resume subcommands
- `orchestrator/adapters/__init__.py` — adapter discovery and registry
- `orchestrator/adapters/base.py` — StepContract, HarnessResult, HarnessAdapter ABC, HarnessRegistry, error types
- `orchestrator/adapters/generic.py` — GenericAdapter for file-based fallback (test_mode writes artifacts, poll_human clarified)
- `orchestrator/adapters/opencode.py` — OpenCodeAdapter for subprocess-based execution (cancel() fixed with Popen)
- `tests/test_adapters.py` — 28 tests for adapters, all passing

Phase 4a is the first sub-phase of Phase 4 (Validators). Use test-first approach: write tests before implementation.
