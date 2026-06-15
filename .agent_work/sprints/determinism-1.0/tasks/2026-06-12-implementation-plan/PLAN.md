# Implementation Plan: Deep Determinism

## Phase Overview

This plan has 9 phases, each broken into sub-phases. Phases 3.5 and 5.5 are targeted fix/quality passes between major phases. Each phase follows:

1. Implement
2. Audit (pass/fail)
3. Ralph critique (3 cycles)
4. Ralph revise (3 cycles)
5. Validate

Total: 9 phases × ~5 sub-phases × (implement + audit + 3 Ralph cycles + validate) = ~225 steps
Phase 6 grew from 6 to 17 sub-phases during development (6a-6q) — the collapse phase
absorbs contextsmith-run patterns, then hardens determinism with 10 additional wiring sub-phases.

## Prerequisites

Before starting, set up the development environment:

```bash

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies and create .venv
uv sync

# Verify dependencies
uv run python -c "import jsonschema; print('jsonschema OK')"
uv run python -c "import yaml; print('PyYAML OK')"
uv run python -c "import pytest; print('pytest OK')"
uv run ruff --version
```

All Python commands should be run with `uv run` to use the project's virtual environment.

## Artifact Templates

### Checkpoint.json Template

```json
{
  "workflow_id": "determinism-implementation",
  "version": 1,
  "current_phase": "<phase-name>",
  "current_state": "<state-name>",
  "last_updated": "<ISO 8601>",
  "completed_phases": [],
  "counters": {
    "<phase-name>": {"retries": 0, "ralph_cycles": 0}
  },
  "last_result": {
    "state": "<state-name>",
    "status": "pass|fail",
    "artifacts_written": []
  }
}
```

### RESULT.json Template

```json
{
  "status": "pass|fail|blocked",
  "reason": "human-readable explanation",
  "artifacts": ["file1.md", "file2.py"],
  "issues": [],
  "next_action": "done|retry|fix|stop"
}
```

### AUDIT_REPORT.md (Append-Only)

Every phase must append its audit findings to `AUDIT_REPORT.md`. Never overwrite — this file accumulates rubric assessments across all phases.

**Append rule:** Read the existing file, then append a new section. Use the same two methods as the Educational Report (bash `>>` heredoc preferred; `edit` tool fallback). The `write` tool is **forbidden** for this file.

### AUDIT_REPORT.md Template

```markdown

# Audit Report: <Phase Name>

## Summary
<one-line conclusion>

## Findings

- <Severity>: <description>
  - Evidence: <where>
  - Fix: <how>

## Overall Verdict
pass / fail / conditional-pass
```

## Validation Commands

For each phase, run these commands to validate:

```bash

# Validate skills
uv run python scripts/validate_skills.py

# Lint and format Python code
uv run ruff check orchestrator/ --select E,F,W,I
uv run ruff format orchestrator/ --check

# Validate Markdown formatting
markdownlint .agent_work/ orchestrator/ docs/ --ignore node_modules

# Run tests
uv run pytest tests/ -v

# Validate orchestrator module
uv run python -c "from orchestrator import run; print('import OK')"

# Validate adapters
uv run python -c "from orchestrator.adapters.base import HarnessAdapter; print('adapters OK')"
```

All Python code must pass ruff linting and formatting checks. Run `uv run ruff check --fix` and `uv run ruff format` to auto-fix issues before committing.
All Markdown files must pass markdownlint with the project's `.markdownlint.jsonc` config.

## Import Pattern

Avoid circular imports. Use this import hierarchy:

```
orchestrator/__init__.py
  ← orchestrator/orchestrator.py
  ← orchestrator/cli.py

orchestrator/orchestrator.py
  ← orchestrator/state_reader.py
  ← orchestrator/checkpoint.py
  ← orchestrator/step_compiler.py
  ← orchestrator/validators.py
  ← orchestrator/adapters/base.py

orchestrator/step_compiler.py
  ← orchestrator/adapters/base.py (for StepContract, HarnessResult)

orchestrator/adapters/__init__.py
  ← orchestrator/adapters/base.py
  ← orchestrator/adapters/generic.py
  ← orchestrator/adapters/opencode.py
```

Rule: Never import from `orchestrator.orchestrator` in state_reader, checkpoint, or step_compiler.

## Test Patterns

Follow existing test conventions in `tests/`:

```python

# tests/test_orchestrator_state.py
import pytest
from pathlib import Path
from orchestrator.state_reader import read_status, read_plan

FIXTURES = Path(__file__).parent / "fixtures"

def test_read_status_valid():
    status = read_status(FIXTURES / "task_state_valid")
    assert status["current_phase"] is not None
    assert status["current_state"] is not None

def test_read_status_missing():
    with pytest.raises(FileNotFoundError):
        read_status(FIXTURES / "nonexistent")
```

Reference: `tests/test_validator.py` for patterns.

## Error Message Format

Validators return lists of strings in this format:

```python

# Success
return []

# Failure
return ["Missing required file: STATUS.md"]
return ["Missing required section '## Current Phase' in STATUS.md"]
return ["File is empty: PLAN.md"]
return ["Invalid state 'bad_state' in STATUS.md, not in config.states"]
```

Format: `"<error type>: <details>"`

Error types:

- `Missing required file`
- `Missing required section`
- `File is empty`
- `Invalid state`
- `Invalid transition`
- `Schema validation failed`
- `State inconsistency`

## Self-Audit Gate

After every implementation phase, before writing RESULT.json, the agent must self-audit:

### Self-Audit Checklist (per phase)

1. **Artifacts exist** — all expected_outputs are written to disk
2. **Artifacts non-empty** — no zero-byte files
3. **Code compiles** — `uv run python -c "import orchestrator.<module>"` succeeds (for Python phases)
4. **Tests pass** — `uv run pytest tests/test_<module>.py -v` succeeds (if tests exist)
5. **Ruff passes** — `uv run ruff check orchestrator/ --select E,F,W,I` and `uv run ruff format --check` succeed (for Python phases)
6. **No TODOs left** — grep for `TODO`, `FIXME`, `HACK` in written files
7. **No placeholder content** — no `...`, `TBD`, `PLACEHOLDER` in written files
8. **Imports resolve** — no circular imports, no missing dependencies
9. **Docstrings present** — all public functions have docstrings
10. **Consistent style** — matches existing code conventions in the project
11. **Spec alignment** — implementation matches the spec files in deep_determinism/
12. **Report files preserved** — verify `EDUCATIONAL_REPORT.md` and `AUDIT_REPORT.md` still contain all prior phase content (grep for earlier phase names). If any prior phase is missing, the file was clobbered — restore from git and re-append.

### Self-Audit Result

If all checks pass → write RESULT.json with `status: "pass"`
If any check fails → fix the issue, then re-audit
If cannot fix → write RESULT.json with `status: "fail"` and `reason: "<what failed>"`

### Self-Audit for Non-Code Phases

For phases that create YAML, Markdown, or config files:

1. **Format valid** — YAML parses, Markdown renders, JSON validates
2. **Required fields present** — all fields from the spec are included
3. **No duplication** — doesn't duplicate content from other files
4. **References valid** — all referenced files exist
5. **Consistent with spec** — matches the spec in deep_determinism/

## Educational Report (Append-Only)

After every implementation phase, **append to** `EDUCATIONAL_REPORT.md`. Never overwrite it — it accumulates history across all phases.

### Append Mechanics (Required)

Use one of these two methods:

**Method A (preferred — cannot clobber):** Use bash heredoc:

```bash
cat >> .agent_work/sprints/determinism-1.0/tasks/.../EDUCATIONAL_REPORT.md << 'REPORT'

---

# Educational Report: <Phase Name>

## What Was Done
...
REPORT
```

The `>>` operator appends. The `'REPORT'` heredoc delimiter (quoted) prevents variable expansion. This cannot clobber.

**Method B (fragile — verify file length before and after):** Use the `edit` tool with `oldString` matching the last unique paragraph of the existing file, and `newString` = `oldString + "\n\n---\n\n" + new_content`. If the edit tool errors (e.g., whitespace mismatch), fall back to Method A. Never fall back to `write`.

### What to Append Per Phase

#### What Was Done

- List every file created or modified
- Summarize the key functions/classes added
- Note any design decisions made

#### Why It Matters

- How this phase contributes to the overall system
- What problems this code solves
- How it fits with the other components

#### How It Works

- Explain the key algorithms or patterns used
- Describe the data flow
- Note any non-obvious implementation choices

#### For Small Models

- Keep explanations concrete and literal
- Use examples from the actual code
- Avoid abstract descriptions
- Include the actual function signatures

### Educational Report Template

````markdown

# Educational Report: <Phase Name>

## What Was Done

- Created `orchestrator/<file>.py` with <N> functions
- Key functions: `function1()`, `function2()`
- Design decision: <what and why>

## Why It Matters

- This component handles <responsibility>
- Without it, <what would break>
- It connects to <other components> by <how>

## How It Works

1. <Step 1 of the algorithm>
2. <Step 2 of the algorithm>
3. <Step 3 of the algorithm>

### Key Function Signatures
```python
def function1(arg1: str, arg2: int) -> dict:
    """What it does, what it returns."""
    
def function2(arg1: Path) -> list[str]:
    """What it does, what it returns."""
```

### Data Flow

```
<input> → <processing> → <output>
```

### For Small Models

- <Concrete example of how to use this code>
- <Common mistakes to avoid>
- <What to check if something goes wrong>
````

## Rollback Instructions

If a phase fails and retries:

1. Re-read STATUS.md to determine current phase
2. Re-read NEXT_PROMPT.md for the bounded task
3. Re-read CONTEXT.md for constraints
4. Check what artifacts were partially written
5. Fix the issues identified in the failure reason
6. Re-attempt the phase

Do NOT re-read PLAN.md unless the plan itself needs updating.

---

## Phase 1: Verify Schemas and Create Test Fixtures

**Goal:** Verify existing schemas work, create test fixtures for all artifact types.

### Sub-phase 1a: Verify workflow_config.schema.json

**Task:** Verify the schema validates both example configs from workflow_config_sketch.md.

**Files to read:**

- `schemas/workflow_config.schema.json`
- `.agent_work/ideation/deep_determinism/workflow_config_sketch.md` (lines 272-377, 383-557)

**Steps:**

1. Read the schema file
2. Read both example configs
3. Validate each against the schema using jsonschema library
4. Record results

**Expected outputs:**

- `tests/fixtures/valid_workflow_simple_audit.yaml` — copy of simple audit example
- `tests/fixtures/valid_workflow_engineering.yaml` — copy of engineering example
- `tests/fixtures/validation_results.md` — validation pass/fail for each

**Validation:** Both examples validate without errors.

### Sub-phase 1b: Verify agent_config.schema.json

**Task:** Verify the schema validates agent config examples.

**Files to read:**

- `schemas/agent_config.schema.json`
- `.agent_work/ideation/deep_determinism/system_components.md` (lines 179-204)

**Steps:**

1. Read the schema file
2. Read agent config examples
3. Validate each against the schema
4. Record results

**Expected outputs:**

- `tests/fixtures/valid_agent_auditor.yaml` — auditor agent config
- `tests/fixtures/valid_agent_builder.yaml` — builder agent config
- `tests/fixtures/validation_results_agent.md` — validation pass/fail

**Validation:** Both examples validate without errors.

### Sub-phase 1c: Create invalid test fixtures

**Task:** Create test fixtures that should fail validation.

**Files to read:**

- `schemas/workflow_config.schema.json`
- `schemas/agent_config.schema.json`

**Steps:**

1. Create workflow config with missing required field
2. Create workflow config with invalid state reference
3. Create workflow config with invalid transition target
4. Create agent config with missing permission
5. Create agent config with invalid mode

**Expected outputs:**

- `tests/fixtures/invalid_workflow_missing_field.yaml`
- `tests/fixtures/invalid_workflow_bad_state.yaml`
- `tests/fixtures/invalid_workflow_bad_transition.yaml`
- `tests/fixtures/invalid_agent_missing_permission.yaml`
- `tests/fixtures/invalid_agent_bad_mode.yaml`

**Validation:** All invalid fixtures fail validation with expected error messages.

### Sub-phase 1d: Create task-state test fixtures

**Task:** Create valid and invalid task-state directories for testing.

**Files to read:**

- `.agent_work/ideation/deep_determinism/state_artifact_strategy.md`
- `shared/persistent-task-state.md`

**Steps:**

1. Create valid task-state directory with all required files
2. Create task-state directory missing STATUS.md
3. Create task-state directory with empty PLAN.md
4. Create task-state directory with invalid checkpoint.json

**Expected outputs:**

- `tests/fixtures/task_state_valid/` — all files present and valid
- `tests/fixtures/task_state_missing_status/` — STATUS.md missing
- `tests/fixtures/task_state_empty_plan/` — PLAN.md empty
- `tests/fixtures/task_state_invalid_checkpoint/` — checkpoint.json malformed

**Validation:** Valid fixture passes all checks, invalid fixtures fail with specific errors.

---

## Phase 2: Core Orchestrator Module

**Goal:** Implement the Python orchestrator module with state machine, loop, and checkpoint management.

### Sub-phase 2a: Create orchestrator package structure

**Task:** Create the orchestrator Python package with **init**.py and basic structure.

**Files to read:**

- `.agent_work/ideation/deep_determinism/orchestrator_idea.md` (function reference section)
- `.agent_work/ideation/deep_determinism/implementation_guide.md`

**Steps:**

1. Create `orchestrator/` directory
2. Create `orchestrator/__init__.py` with public API
3. Create `orchestrator/constants.py` with exit codes and state names
4. Create `orchestrator/exceptions.py` with custom exceptions

**Expected outputs:**

- `orchestrator/__init__.py` — exports run, run_workflow, init, validate, inspect
- `orchestrator/constants.py` — EXIT_DONE, EXIT_BLOCKED, EXIT_CONTINUE, canonical states
- `orchestrator/exceptions.py` — OrchestratorError, StateInconsistency, ConfigError

**Validation:** `python -c "from orchestrator import run"` succeeds.

### Sub-phase 2b: Implement state reader

**Task:** Implement parsing of STATUS.md, PLAN.md, CONTEXT.md into structured dicts.

**Files to read:**

- `.agent_work/ideation/deep_determinism/state_artifact_strategy.md` (required sections)
- `.agent_work/ideation/deep_determinism/orchestrator_idea.md` (state reading)

**Steps:**

1. Create `orchestrator/state_reader.py`
2. Implement `read_status(dir) -> dict` — parse STATUS.md sections
3. Implement `read_plan(dir) -> dict` — parse PLAN.md checkboxes
4. Implement `read_context(dir) -> dict` — parse CONTEXT.md sections
5. Implement `read_checkpoint(dir) -> dict | None` — parse checkpoint.json
6. Add validation for each parser (required fields present)

**Expected outputs:**

- `orchestrator/state_reader.py` — all 4 parser functions

**Validation:** Parse `tests/fixtures/task_state_valid/` without errors, return correct structure.

### Sub-phase 2c: Implement checkpoint manager

**Task:** Implement checkpoint read/write with atomic writes.

**Files to read:**

- `.agent_work/ideation/deep_determinism/orchestrator_idea.md` (checkpoint format section)

**Steps:**

1. Create `orchestrator/checkpoint.py`
2. Implement `read_checkpoint(dir) -> dict` — read and validate checkpoint.json
3. Implement `write_checkpoint(dir, data) -> None` — atomic write (temp + rename)
4. Implement `update_checkpoint(checkpoint, current, next, result) -> dict` — update counters
5. Implement `validate_checkpoint(checkpoint, config) -> list[str]` — check consistency

**Expected outputs:**

- `orchestrator/checkpoint.py` — all 4 functions

**Validation:** Write checkpoint, read it back, verify content matches.

### Sub-phase 2d: Implement step compiler

**Task:** Compile StepContract from config + state + plan.

**Files to read:**

- `.agent_work/ideation/deep_determinism/orchestrator_and_harness.md` (StepContract dataclass)
- `.agent_work/ideation/deep_determinism/workflow_config_sketch.md` (state definitions)

**Steps:**

1. Create `orchestrator/step_compiler.py`
2. Import StepContract, HarnessResult from adapters (or define locally)
3. Implement `compile_step_contract(state, config, plan, context) -> StepContract`
4. Implement `resolve_next_state(current, result, validation, config, counters) -> str`
5. Implement `_matches_condition(condition, result, validation) -> bool`

**Expected outputs:**

- `orchestrator/step_compiler.py` — compile and resolve functions

**Validation:** Compile step contract from test fixture, verify all fields populated correctly.

### Sub-phase 2e: Implement main loop

**Task:** Implement the orchestrator main loop (run_workflow, run).

**Files to read:**

- `.agent_work/ideation/deep_determinism/orchestrator_idea.md` (main loop section)

**Steps:**

1. Create `orchestrator/orchestrator.py`
2. Implement `run(config_path, state_dir, ...) -> int` — single step execution
3. Implement `run_workflow(config_path, state_dir, ...) -> int` — outer loop
4. Implement `should_stop(state_dir) -> bool` — check for STOP file
5. Implement `register_signal_handlers(state_dir) -> None` — SIGINT handler
6. Wire together: load config → read state → compile step → dispatch → validate → transition → checkpoint

**Expected outputs:**

- `orchestrator/orchestrator.py` — run, run_workflow, should_stop, register_signal_handlers

**Validation:** Run with `--dry-run` flag, print next step without executing.

### Sub-phase 2f: Implement CLI interface

**Task:** Implement the CLI entry point.

**Files to read:**

- `.agent_work/ideation/deep_determinism/orchestrator_idea.md` (CLI section)

**Steps:**

1. Create `orchestrator/cli.py`
2. Implement argument parsing (config, state_dir, --harness, --single-step, --dry-run, --repair, --force, --test-mode, --verbose, --quiet)
3. Implement subcommands: run, init, validate, inspect, diff, resume
4. Wire to orchestrator functions

**Expected outputs:**

- `orchestrator/cli.py` — argument parsing and subcommand dispatch

**Validation:** `python -m orchestrator --help` shows usage.

---

## Phase 3: Harness Adapters

**Goal:** Implement the harness adapter base class and OpenCode/generic adapters.

### Sub-phase 3a: Create adapter base classes

**Task:** Implement HarnessAdapter ABC, HarnessResult, StepContract, error types.

**Files to read:**

- `.agent_work/ideation/deep_determinism/orchestrator_and_harness.md` (full file)

**Steps:**

1. Create `orchestrator/adapters/` directory
2. Create `orchestrator/adapters/__init__.py` with ADAPTER_REGISTRY
3. Create `orchestrator/adapters/base.py` with:
   - `StepContract` dataclass
   - `HarnessResult` dataclass
   - `HarnessAdapter` ABC (name, validate_environment, execute, cancel, get_capabilities)
   - `HarnessRegistry` class
   - `HarnessTimeoutError` exception
   - `HarnessExecutionError` exception

**Expected outputs:**

- `orchestrator/adapters/base.py` — all types and classes

**Validation:** `from orchestrator.adapters.base import HarnessAdapter` succeeds.

### Sub-phase 3b: Implement generic adapter

**Task:** Implement the generic adapter (file-based, no agent runtime).

**Files to read:**

- `.agent_work/ideation/deep_determinism/harness_agnostic_distribution.md` (generic adapter section)

**Steps:**

1. Create `orchestrator/adapters/generic.py`
2. Implement `GenericAdapter(HarnessAdapter)`:
   - `name` → "generic"
   - `validate_environment()` → always returns []
   - `execute(contract, state_dir)` → write .pending_prompt.md, check RESULT.json, collect artifacts
   - `cancel(step_id)` → return False
   - `get_capabilities()` → basic capabilities
3. Register with HarnessRegistry

**Expected outputs:**

- `orchestrator/adapters/generic.py` — GenericAdapter class

**Validation:** Create GenericAdapter, call execute with test fixture, verify HarnessResult returned.

### Sub-phase 3c: Implement OpenCode adapter

**Task:** Implement the OpenCode adapter (subprocess-based).

**Files to read:**

- `.agent_work/ideation/deep_determinism/orchestrator_and_harness.md` (OpenCode adapter section)
- `.agent_work/ideation/deep_determinism/harness-opencode.md`

**Steps:**

1. Create `orchestrator/adapters/opencode.py`
2. Implement `OpenCodeAdapter(HarnessAdapter)`:
   - `name` → "opencode"
   - `validate_environment()` → check `opencode` command exists
   - `execute(contract, state_dir)` → build command, launch subprocess, collect RESULT.json, return HarnessResult
   - `_build_command(contract)` → opencode run --agent --model --file --format json
   - `_read_result(proc, contract, state_dir)` → read RESULT.json, fallback to artifacts
   - `cancel(step_id)` → kill subprocess
   - `get_capabilities()` → supports_model_pinning, supports_step_caps, etc.
3. Register with HarnessRegistry

**Expected outputs:**

- `orchestrator/adapters/opencode.py` — OpenCodeAdapter class

**Validation:** Create OpenCodeAdapter, call validate_environment, verify returns [] on system with opencode installed.

---

## Phase 4: Validators

**Goal:** Implement validation functions for artifacts and workflow state. **Test-first approach:** Write tests before implementation.

### Sub-phase 4a: Implement file validators

**Task:** Implement file existence, non-empty, and section presence checks. Write tests first.

**Files to read:**

- `.agent_work/ideation/deep_determinism/state_artifact_strategy.md` (validation pseudocode)

**Steps:**

1. Create `tests/test_validators.py` with test cases for all validators
2. Create `orchestrator/validators.py`
3. Implement `validate_file_exists(path) -> list[str]` — check file exists
4. Implement `validate_file_nonempty(path) -> list[str]` — check file not empty
5. Implement `validate_required_sections(path, sections) -> list[str]` — check sections present
6. Implement `validate_artifact(file_path, required_sections) -> list[str]` — combine all checks
7. Implement `validate_artifacts(state_dir, expected_outputs, config) -> ValidationResult`
8. Run tests, fix any failures

**Expected outputs:**

- `tests/test_validators.py` — comprehensive test suite
- `orchestrator/validators.py` — all validation functions

**Validation:** `pytest tests/test_validators.py` passes.

### Sub-phase 4b: Implement schema validators

**Task:** Implement JSON/YAML schema validation. Write tests first.

**Files to read:**

- `schemas/workflow_config.schema.json`
- `schemas/agent_config.schema.json`

**Steps:**

1. Add test cases to `tests/test_validators.py` for schema validation
2. Add `validate_schema(data, schema_path) -> list[str]` to validators.py
3. Add `validate_workflow_config(config_path) -> list[str]` — validate against schema
4. Add `validate_agent_config(agent_path) -> list[str]` — validate against schema
5. Add `validate_checkpoint(checkpoint_path, config) -> list[str]` — validate checkpoint
6. Run tests, fix any failures

**Expected outputs:**

- Updated `tests/test_validators.py` — schema validation tests
- Updated `orchestrator/validators.py` — schema validation functions

**Validation:** `pytest tests/test_validators.py` passes. Validate valid configs pass, invalid configs fail with specific errors.

### Sub-phase 4c: Implement state consistency validator

**Task:** Validate consistency between STATUS.md, checkpoint.json, and workflow config. Write tests first.

**Files to read:**

- `.agent_work/ideation/deep_determinism/orchestrator_idea.md` (error handling matrix)

**Steps:**

1. Add test cases to `tests/test_validators.py` for state consistency
2. Add `validate_state_consistency(status, checkpoint, config) -> list[str]`
3. Check: STATUS.md current_phase is valid state in config
4. Check: checkpoint.json current_phase matches STATUS.md
5. Check: checkpoint counters are within limits
6. Check: completed_phases exist in config phase_order
7. Run tests, fix any failures

**Expected outputs:**

- Updated `tests/test_validators.py` — state consistency tests
- Updated `orchestrator/validators.py` — state consistency check

**Validation:** `pytest tests/test_validators.py` passes. Test with consistent state (pass) and inconsistent state (fail with specific error).

### Sub-phase 4d: Wire validators into orchestrator

**Task:** Integrate validators into orchestrator execution flow.

**Steps:**

1. Import validators in orchestrator.py
2. Call validate_artifacts() after harness execution
3. Call validate_state_consistency() before state transitions
4. Call validate_workflow_config() at startup
5. Handle validation failures appropriately (retry, block, or error)
6. Write integration tests in `tests/test_orchestrator_integration.py`
7. Run all tests, fix any failures

**Expected outputs:**

- Updated `orchestrator/orchestrator.py` — validators integrated
- `tests/test_orchestrator_integration.py` — integration tests

**Validation:** `pytest tests/` passes. End-to-end workflow execution validates artifacts at each step.

---

## Phase 5: Orchestrator Skill and Workflow Developer

**Goal:** Create the SKILL.md files for skill-only path and workflow generation.

### Sub-phase 5a: Create orchestrator SKILL.md

**Task:** Create the orchestrator skill for skill-only execution.

**Files to read:**

- `.agent_work/ideation/deep_determinism/orchestrator_skill_draft.md`
- `.agent_work/ideation/deep_determinism/orchestrator_as_skill.md`

**Steps:**

1. Create `skills/contextsmith-orchestrator/` directory
2. Create `skills/contextsmith-orchestrator/SKILL.md` from draft
3. Create `skills/contextsmith-orchestrator/reference_manifest.yml`
4. Add to `skills/contextsmith-orchestrator/references/` shared references
5. Run `python scripts/validate_skills.py` to verify

**Expected outputs:**

- `skills/contextsmith-orchestrator/SKILL.md` — under 300 lines
- `skills/contextsmith-orchestrator/reference_manifest.yml` — manifest

**Validation:** `python scripts/validate_skills.py` passes for new skill.

### Sub-phase 5b: Create workflow developer SKILL.md

**Task:** Create the workflow developer skill for generating configs.

**Files to read:**

- `.agent_work/ideation/deep_determinism/workflow_developer_skill.md`
- `.agent_work/ideation/deep_determinism/domain-templates/`

**Steps:**

1. Create `skills/contextsmith-workflow-developer/` directory
2. Create `skills/contextsmith-workflow-developer/SKILL.md`
3. Create `skills/contextsmith-workflow-developer/reference_manifest.yml`
4. Copy domain templates to `skills/contextsmith-workflow-developer/references/domain-templates/`
5. Run `python scripts/validate_skills.py` to verify

**Expected outputs:**

- `skills/contextsmith-workflow-developer/SKILL.md` — under 250 lines
- `skills/contextsmith-workflow-developer/reference_manifest.yml` — manifest
- `skills/contextsmith-workflow-developer/references/domain-templates/` — 6 templates

**Validation:** `python scripts/validate_skills.py` passes for new skill.

### Sub-phase 5c: Update router skill

**Task:** Update the contextsmith router to dispatch to orchestrator and workflow-developer.

**Files to read:**

- `skills/contextsmith/SKILL.md`
- `.agent_work/ideation/deep_determinism/orchestrator_as_skill.md`

**Steps:**

1. Add `contextsmith-orchestrator` to routing table
2. Add `contextsmith-workflow-developer` to routing table
3. Update wizard Q1 options
4. Run `python scripts/validate_skills.py` to verify

**Expected outputs:**

- Updated `skills/contextsmith/SKILL.md` — new routes added

**Validation:** `python scripts/validate_skills.py` passes.

---

## Phase 5.5: Targeted Quality Fixes

**Goal:** Fix 7 audit findings before proceeding to the collapse phase. Each sub-phase is independent.

### Sub-phase 5.5a: Fix ruff line-too-long errors

**Task:** Fix 4 pre-existing E501 line-too-long errors in `orchestrator/orchestrator.py`.

**Steps:**

1. Read lines 219, 244, 254, 267
2. Break each long line at 88 chars using parentheses or intermediate variables
3. Run `ruff format` and `ruff check`

**Expected outputs:**

- Clean `ruff check orchestrator/ --select E,F,W,I`
- Clean `ruff format orchestrator/ --check`

### Sub-phase 5.5b: Replace HARD STOP with .phase_gate flag pattern

**Task:** Replace the "HARD STOP — DO NOT EXECUTE IN CURRENT SESSION" text with a `.phase_gate` flag file mechanism. NEXT_PROMPT.md instead reads: "Wait for .phase_gate_ready at <task-dir>/.phase_gate before executing. Do NOT proceed without this file."

**Steps:**

1. Update the handoff pattern in `shared/persistent-task-state.md` or document the .phase_gate convention
2. Update NEXT_PROMPT.md template in orchestrator SKILL.md artifacts section
3. Remove `.agent_work/sprints/.../tasks/2026-06-12-implementation-plan/.phase_gate` if present (clean slate)
4. Create a brief convention doc in shared/ or document inline

**Expected outputs:**

- NEXT_PROMPT.md template updated to use .phase_gate
- Convention documented

### Sub-phase 5.5c: Remove deep_determinism spec file references from orchestrator SKILL.md

**Task:** The orchestrator SKILL.md Reference Loading table references `.agent_work/ideation/deep_determinism/` files. Replace with formats described inline or references that exist in standalone installations.

**Steps:**

1. Read orchestrator SKILL.md Reference Loading section
2. Replace deep_determinism spec file paths with inline format descriptions or shared/project references
3. Verify validation still passes

**Expected outputs:**

- Clean orchestrator SKILL.md with no deep_determinism path references

### Sub-phase 5.5d: Create shared/harness-generic.md

**Task:** Create the generic harness companion for the orchestrator skill. This is the fallback for unknown harnesses — skill-only mode, no optimizations, inline results.

**Steps:**

1. Read `shared/harness-opencode.md` for format reference
2. Create `shared/harness-generic.md` following the companion template from orchestrator_as_skill.md
3. Update orchestrator reference_manifest.yml to reference it
4. Verify validation

**Expected outputs:**

- `shared/harness-generic.md` — companion file
- `skills/contextsmith-orchestrator/references/harness-generic.md` — local copy
- Updated orchestrator reference_manifest.yml

### Sub-phase 5.5e: Update versioning scheme (policy only)

**Task:** Move to project-level versioning. After this sprint, all ContextSmith skills move to 2.0.0. Per-skill version metadata is deprecated in favor of the single project version in PACKAGE_SPEC.md. Document the decision here; the actual version stamp happens at the end of Phase 6 after the router is finalized.

**Steps:**

1. Update PACKAGE_SPEC.md with versioning decision (project-level version, deprecate per-skill)
2. Update AGENTS.md with versioning convention
3. Do NOT bump SKILL.md versions yet — that happens after Phase 6e when the final skill set is settled

**Expected outputs:**

- Updated PACKAGE_SPEC.md
- Updated AGENTS.md

### Sub-phase 5.5f: Add meta-config detail to Phase 6

**Task:** Add detail to Phase 6 sub-phases 6d (workflow-developer meta-config) so the meta-config phase definitions are concrete.

**Steps:**

1. Read current Phase 6d description in PLAN.md
2. Expand steps to include concrete phase definitions for the meta-config workflow_config.yaml
3. Add example config snippet

**Expected outputs:**

- Enhanced Phase 6d in PLAN.md

### Sub-phase 5.5g: Update Ralph rationale in PLAN.md

**Task:** Clarify that 3 Ralph iterations per sub-phase is intentional. No-op is valid evidence — it means no material defect was found. The Ralph Loop Configuration section should state this explicitly.

**Steps:**

1. Read current Ralph Loop Configuration section
2. Add explicit note: "No-op iterations are valid evidence. They mean no material defect was found. Do not invent changes to satisfy the iteration count."
3. Keep 3 iterations as-is

**Expected outputs:**

- Updated Ralph Loop Configuration section

---

## Phase 6: Collapse into Orchestrator-Only Execution

**Goal:** Remove contextsmith-run, upgrade orchestrator to absorb its contract/validation/evidence patterns, convert workflow-developer to use meta-config.

### Sub-phase 6a: Juice contextsmith-run (read-only)

**Task:** Catalog every concept in contextsmith-run SKILL.md and local references. No file changes.

**Steps:**

1. Read contextsmith-run SKILL.md sections — Runtime Contract, Supported Inputs, Control Parameters, Local-Model Execution Rules, Domain Routing, Interaction Modes, Execution Contract Compiler, Preflight Gate, Reference Selection, Execution Workflow, Task-State Execution, Validation Gate, Self-Audit Gate, Ralph Loop, Evidence Ledger, Completion Criteria, Failure Handling, Required Output, Artifact Manifest
2. Read 8 local-only references: execution-contract-core.md, execution-contract.md, evidence-ledger-core.md, evidence-ledger.md, domain-packs.md, interaction-refinement.md, task-state-execution.md, help.md
3. Read reference_manifest.yml for reference mapping
4. Identify shared refs run has but orchestrator doesn't

### Sub-phase 6b: Enhance contextsmith-orchestrator SKILL.md

**Task:** Absorb all patterns from contextsmith-run into the orchestrator skill.

**Steps:**

1. Rewrite orchestrator SKILL.md to include:
   - Supported Inputs (raw prompts, prompt files, NEXT_PROMPT.md, task-state dirs, plans, checklists)
   - Config auto-generation: no workflow_config.yaml → route through workflow-developer
   - Runtime Contract / parameter defaults table
   - Control Parameters / flag catalog
   - Local-Model Execution Rules
   - Domain Routing / task classification
   - Interaction Modes (silent/confirm/refine/collaborative/review-gate)
   - Execution Contract Compiler
   - Preflight Gate (verify input, domain, side effects, refs, validation)
   - Reference Selection (load by need)
   - Execution Workflow (full 14-step numbered workflow)
   - Task-State Execution (required state files, phase closeout)
   - Validation Gate (two-layer: runtime CLI + domain)
   - Self-Audit Gate
   - Ralph Loop Enforcement
   - Evidence Ledger
   - Completion Criteria
   - Failure Handling
   - Required Output format
   - Artifact Manifest
2. Keep existing orchestrator loop, state determination, artifact validation, templates, transition logic
3. Keep heavy reference content (domain-packs.md ~397 lines, execution-contract.md, evidence-ledger.md) as separate reference files — do NOT inline them. The SKILL.md should reference them, not contain them.
4. Update Quick Use to route through workflow-developer for auto-config
5. Target: ~400 lines of instruction content; heavy domain/contract detail stays in reference files

**Expected outputs:**

- `skills/contextsmith-orchestrator/SKILL.md` — rewritten

**Validation:** `python scripts/validate_skills.py` passes.

### Sub-phase 6c: Move references and update manifest

**Task:** Copy 8 local-only references from run to orchestrator; add missing shared refs to orchestrator manifest. Note: harness-generic.md was already created in sub-phase 5.5d — do NOT copy it again.

**Steps:**

1. Copy contextsmith-run's local references: execution-contract-core, execution-contract, evidence-ledger-core, evidence-ledger, domain-packs, interaction-refinement, task-state-execution, help
2. Verify they don't duplicate existing orchestrator references
3. Update orchestrator reference_manifest.yml
4. Add shared refs contextsmith-run had that orchestrator is missing
5. Verify harness-generic.md from 5.5d is still in orchestrator references/ and manifest

**Expected outputs:**

- `skills/contextsmith-orchestrator/references/` — updated with 8 new files
- `skills/contextsmith-orchestrator/reference_manifest.yml` — updated

**Validation:** `python scripts/validate_skills.py` passes.

### Sub-phase 6d: Convert workflow-developer to meta-config

**Task:** Create workflow_config.yaml for the config-generation process. Orchestrator runs this meta-config when invoked by the workflow-developer skill.

**Steps:**

1. Create `skills/contextsmith-workflow-developer/workflow_config.yaml`
2. Define phases with concrete state definitions for each:

   ```yaml
   states:
     gather_requirements:
       permissions: read-only
       max_retries: 2
       transitions:

         - condition: pass

           target: select_domain_template

         - condition: max_retries

           target: blocked
       expected_outputs:

         - requirements.md

       phase_prompt: |
         Ask 4 structured questions to gather workflow intent:

         1. What domain does this workflow cover? (software, data, ML, writing, research, ops)
         2. What is the top-level task or problem?
         3. What files or inputs are involved?
         4. What success criteria define "done"?

     select_domain_template:
       permissions: read-only
       max_retries: 1
       transitions:

         - condition: pass

           target: customize_config
       expected_outputs:

         - selected_template.yaml

       phase_prompt: |
         Based on requirements.md, select the best-matching domain template from
         references/domain-templates/. Copy it to selected_template.yaml.

     customize_config:
       permissions: edit
       max_retries: 3
       transitions:

         - condition: output_valid

           target: validate_config

         - condition: pass

           target: validate_config

         - condition: max_retries

           target: blocked
       expected_outputs:

         - workflow_config.yaml

       phase_prompt: |
         Customize selected_template.yaml with the gathered requirements:

         - Fill in workflow_id, domain, mode from requirements
         - Add/modify state definitions for the specific workflow
         - Set permissions, transitions, expected_outputs per state
         - Add any custom phases not covered by the template

     validate_config:
       permissions: read-only
       max_retries: 2
       transitions:

         - condition: pass

           target: confirm_config

         - condition: fail

           target: customize_config

         - condition: max_retries

           target: blocked
       expected_outputs:

         - validation_report.md

       phase_prompt: |
         Validate workflow_config.yaml against schemas/workflow_config.schema.json:

         - Check all required fields present
         - Verify state references in transitions are valid
         - Check permission values are valid
         - Generate validation_report.md with results

     confirm_config:
       permissions: read-only
       max_retries: 1
       transitions:

         - condition: pass

           target: output_config
       expected_outputs:

         - confirmed_config.yaml

       phase_prompt: |
         Show the config to the user for confirmation. Ask:
         "Is this workflow_config.yaml correct? (yes/no/modify)"
         If yes, copy to confirmed_config.yaml.
         If no or modify, go back to customize_config.

     output_config:
       permissions: edit
       max_retries: 1
       transitions:

         - condition: pass

           target: done
       expected_outputs:

         - workflow_config.yaml

       phase_prompt: |
         Finalize and write the workflow_config.yaml to the target location.
         Create companion task-state files (TASK.md, STATUS.md, PLAN.md) if needed.
   ```

3. Define state definitions, permissions, transitions, expected outputs for each phase as shown above
4. Reduce SKILL.md to: frontmatter + "this skill invokes orchestrator with its own config at workflow_config.yaml" + reference loading table + after-generation options
5. Keep domain templates in references/domain-templates/

**Expected outputs:**

- `skills/contextsmith-workflow-developer/workflow_config.yaml` — meta-config
- `skills/contextsmith-workflow-developer/SKILL.md` — slimmed

**Validation:** Config validates against `schemas/workflow_config.schema.json`. SKILL.md validates. Tests pass.

### Sub-phase 6e: Delete contextsmith-run

**Task:** Remove contextsmith-run skill and all references to it.

**Steps:**

1. Delete `skills/contextsmith-run/` directory
2. Remove contextsmith-run from router routing table
3. Merge wizard Q1 execute options into one: "Execute a task" → orchestrator
4. Remove contextsmith-run from cross-skill coordination chains
5. Update any cross-references in other skills:
   - `shared/harness-opencode.md` + all skill copies: replace "contextsmith-runner" agent reference with "contextsmith-orchestrator" or orchestrator-equivalent
   - `shared/run-configuration-preview.md`: remove or replace contextsmith-run row
   - `shared/structured-questioning.md`: remove or replace contextsmith-run mention
   - `AGENTS.md` repository map: remove contextsmith-run/ entry
6. Update orchestrator description to mention it handles all execution
7. Search for dangling references to contextsmith-run across the full codebase:
   - `grep -r "contextsmith-run" skills/` — other SKILL.md references
   - `grep -r "contextsmith-run" shared/` — shared reference mentions
   - `grep -r "contextsmith-run" docs/` — documentation
   - `grep -r "contextsmith-run" AGENTS.md CONTRIBUTING.md README.md CHANGELOG.md PACKAGE_SPEC.md`
   - `grep -r "contextsmith-run" .agent_work/` — spec files, old plans
8. Apply project-wide version stamp: update all surviving SKILL.md metadata.version to "2.0.0"

**Expected outputs:**

- `skills/contextsmith-run/` — deleted
- `skills/contextsmith/SKILL.md` — updated
- All surviving skills at version 2.0.0
- No dangling references anywhere in the repo

**Validation:** `python scripts/validate_skills.py` passes. Full repo grep for "contextsmith-run" returns nothing. Tests pass.

### Sub-phase 6f: Create orchestrator __main__.py

**Task:** Make the orchestrator runnable as `python -m orchestrator`. This completes the "Python always available" path — the code entry point alongside the skill entry point.

**Files to read:**

- `.agent_work/ideation/deep_determinism/orchestrator_idea.md` (CLI section)

**Steps:**

1. Create `orchestrator/__main__.py`
2. Import and call CLI main function
3. Test `python -m orchestrator --help`

**Expected outputs:**

- `orchestrator/__main__.py` — entry point

**Validation:** `python -m orchestrator --help` shows usage.

### Sub-phase 6g: Implement append validation

**Task:** When dispatching an agent to edit an append-only file (PHASE_LOG.md, EDUCATIONAL_REPORT.md, AUDIT_REPORT.md, DECISIONS.md, or any file declared append-only), validate the agent appended rather than overwrote. Automatically repair if the agent overwrites.

**Files to read:**

- `.agent_work/ideation/deep_determinism/state_artifact_strategy.md` (Append Validation section)

**Steps:**

1. In `orchestrator/validators.py`, add `validate_append_only(file_path: Path, original_prefix: bytes) -> bool` — checks that the file still starts with the same bytes as before the agent acted.
2. In `orchestrator/orchestrator.py`, before dispatching an agent to a state where an expected_output is declared append-only, snapshot the file content (or first N bytes).
3. After the agent returns and artifacts are validated, run `validate_append_only` on each append-only file.
4. If the check fails, prepend the snapshot content back to the file automatically (the orchestrator repairs directly — no re-dispatch).
5. Add test cases to `tests/test_validators.py`:
   - Appended file passes validation
   - Overwritten file fails validation
   - Empty new file fails validation
   - Repair via prepend restores original content
6. Add integration test in `tests/test_orchestrator_integration.py`:
   - Full phase execution with append-only file, verify snapshot + verify + repair

**Expected outputs:**

- Updated `orchestrator/validators.py` — `validate_append_only()` function
- Updated `orchestrator/orchestrator.py` — snapshot-before-dispatch and repair-on-overwrite logic
- Updated `tests/test_validators.py` — append validation tests
- Updated `tests/test_orchestrator_integration.py` — append validation integration test

**Validation:** `pytest tests/` passes. Append-only files survive agent execution correctly.

### Sub-phase 6h: Wire validation_mode into orchestrator

**Task:** `validation_mode` (strict/relaxed/none) already exists on `StepContract` but is never read by the orchestrator's validation branch. All validations are equally strict — cannot distinguish "warn on missing optional artifact" from "block on missing required."

**Files to read:**

- `orchestrator/orchestrator.py` (post-execution validation logic around `validate_artifacts`)
- `orchestrator/adapters/base.py` (StepContract dataclass — confirm `validation_mode` field)
- `orchestrator/validators.py` (current validate_artifacts return format)

**Steps:**

1. Read `validation_mode` from `step_contract.validation_mode` after harness execution.
2. In the validation branch of `_execute_and_validate_step()` or equivalent:
   - `strict` (default): Block on any validation failure. Current behavior.
   - `relaxed`: Log warnings for failures but set `validation["passed"] = True` if at least some artifacts exist.
   - `none`: Skip artifact validation entirely. Harness result status is the only check.
3. Add `validation_mode` to the state definition in `schemas/workflow_config.schema.json` as an optional enum (`strict`, `relaxed`, `none`, default `strict`).
4. Add test cases to `tests/test_validators.py`:
   - Strict mode fails on missing artifact
   - Relaxed mode warns on missing artifact but passes
   - None mode skips validation entirely

**Expected outputs:**

- Updated `orchestrator/orchestrator.py` — validation branch respects `validation_mode`
- Updated `schemas/workflow_config.schema.json` — optional `validation_mode` field in state definitions
- Updated `tests/test_validators.py` — validation mode tests

**Validation:** `pytest tests/` passes. A config with `validation_mode: none` on a state skips artifact checks.

### Sub-phase 6i: Wire checkpoint_before_run write

**Task:** `checkpoint_before_run` exists on `StepContract` but is never called. Without it, a crash during agent dispatch leaves no evidence of whether the agent was launched. Wire the write half only — this creates crash evidence on disk without building the full auto-recovery decision table.

**Files to read:**

- `orchestrator/orchestrator.py` (dispatch sequence: `_execute_and_validate_step` and the code around it)
- `orchestrator/checkpoint.py` (`write_checkpoint`, `update_checkpoint`)

**Steps:**

1. In the orchestrator dispatch path, before calling `adapter.execute()`, check `step_contract.checkpoint_before_run`.
2. If true, write a checkpoint with a `pre_dispatch: true` marker and the current timestamp. Use `write_checkpoint()`.
3. After the agent returns and artifacts are validated (in the normal checkpoint update), write a post-execution checkpoint without the `pre_dispatch` marker. The normal checkpoint write already happens — just add `pre_dispatch: false`.
4. On orchestrator startup (in `run()`), before dispatching any step, check if a `pre_dispatch: true` checkpoint exists without a matching `pre_dispatch: false` checkpoint. If so, log a warning: `"Pre-execution checkpoint found — possible crash during agent dispatch. Check artifacts manually."` Do NOT attempt auto-recovery.
5. Add test cases to `tests/test_checkpoint.py`:
   - `checkpoint_before_run` writes pre-dispatch marker
   - Post-execution checkpoint removes pre-dispatch marker
   - Startup detects stale pre-dispatch marker and warns
6. Write the limitation in a comment at the checkpoint write site: `# Crash recovery: pre-dispatch evidence only. Auto-recovery not implemented — operator checks artifacts if crash is suspected.`

**Expected outputs:**

- Updated `orchestrator/orchestrator.py` — pre-dispatch checkpoint write and startup warning
- Updated `tests/test_checkpoint.py` — pre-dispatch checkpoint tests

**Validation:** `pytest tests/` passes. A simulated crash (interrupt between checkpoint write and agent return) produces a warning on next orchestrator startup.

### Sub-phase 6j: Add exit codes 3, 4, 5

**Task:** Currently the orchestrator only distinguishes 0 (done), 1 (blocked), 2 (continue). Config errors, state inconsistencies, and internal crashes produce the same exit codes. Add distinct codes so callers can automate different responses.

**Files to read:**

- `orchestrator/constants.py` (current exit code definitions)
- `orchestrator/orchestrator.py` (each return/exit path)
- `orchestrator/cli.py` (all subcommand exit paths)

**Steps:**

1. Add to `orchestrator/constants.py`:
   ```python
   EXIT_DONE = 0
   EXIT_BLOCKED = 1
   EXIT_CONTINUE = 2
   EXIT_CONFIG_ERROR = 3
   EXIT_STATE_INCONSISTENCY = 4
   EXIT_INTERNAL_ERROR = 5
   ```
2. In `orchestrator/orchestrator.py`, wire each error path to its distinct code:
   - Config load/schema validation failure → `EXIT_CONFIG_ERROR`
   - State consistency check failure (STATUS.md vs checkpoint mismatch) → `EXIT_STATE_INCONSISTENCY`
   - Unhandled exceptions → `EXIT_INTERNAL_ERROR`
3. In `orchestrator/cli.py`, ensure all subcommands (`run`, `validate`, `inspect`, `diff`, `resume`, `init`) return the correct exit codes for their error paths.
4. Update `_update_status()` to accept an exit code parameter so phase closeout logs which code was used.
5. Add test cases to `tests/test_cli.py`:
   - Run with invalid config → exit code 3
   - Run with corrupted checkpoint → exit code 4
   - Run with internal error → exit code 5
   - Valid run → exit code 0, 1, or 2 as appropriate

**Expected outputs:**

- Updated `orchestrator/constants.py` — 6 named exit codes
- Updated `orchestrator/orchestrator.py` — each error path returns distinct code
- Updated `tests/test_cli.py` — exit code verification tests

**Validation:** `pytest tests/` passes. `python -m orchestrator --bad-config` returns exit code 3.

### Sub-phase 6k: Add pre-dispatch counter check

**Task:** Currently counters are checked during transition resolution (after the agent ran). If a phase has reached `max_retries`, the orchestrator still dispatches the agent one more time before realizing it's blocked. This wastes an agent cycle and risks side effects.

**Files to read:**

- `orchestrator/orchestrator.py` (dispatch sequence before `adapter.execute()`)
- `orchestrator/step_compiler.py` (`resolve_next_state` — current counter check location)
- `orchestrator/checkpoint.py` (counter read/increment)

**Steps:**

1. In the orchestrator dispatch path, before `adapter.execute()` and after the contract is compiled, check `counters[current_state].retries >= max_retries`.
2. If exceeded, skip dispatch entirely. Log: `"[{state}] Max retries ({max_retries}) reached. Transitioning to blocked."` Return `EXIT_BLOCKED` immediately.
3. The dispatch path becomes: compile contract → validate counters → if exceeded, blocked → dispatch → collect result → resolve transition → update counters.
4. The transition resolver (`resolve_next_state`) still checks counters as a second layer — the pre-dispatch check is a fast-fail optimization, not a replacement.
5. Add test cases to `tests/test_orchestrator_integration.py`:
   - Phase at max_retries skips dispatch and goes to blocked
   - Phase within retry limit dispatches normally
   - Counter validation happens before dispatch, not after

**Expected outputs:**

- Updated `orchestrator/orchestrator.py` — pre-dispatch counter gate
- Updated `tests/test_orchestrator_integration.py` — counter gate tests

**Validation:** `pytest tests/` passes. A config with `max_retries: 0` blocks immediately without dispatching.

### Sub-phase 6l: Add timeout_s to workflow config schema

**Task:** Currently timeout is per-harness only. A single long-running state can hang the entire workflow with no per-state timeout enforcement. Add `timeout_s` to the workflow config state definitions and wire it into StepContract.

**Files to read:**

- `schemas/workflow_config.schema.json` (state definition properties)
- `orchestrator/step_compiler.py` (`compile_step_contract` — where StepContract fields are populated)
- `orchestrator/adapters/base.py` (StepContract dataclass — confirm `timeout_s` field)

**Steps:**

1. Add `timeout_s` to the workflow config schema's state definition as an optional integer (minimum 1, default 300 or harness default).
2. In `compile_step_contract()`, read `timeout_s` from the state definition. If absent, fall back to a config-level `default_timeout_s` field. If that's also absent, use 300 (5 minutes).
3. The value flows through StepContract to the harness adapter, which already enforces `timeout_s` — this just makes it configurable per-state.
4. Update existing test fixtures to include or handle the new optional field. Existing configs without `timeout_s` should default correctly.
5. Add test cases to `tests/test_step_compiler.py`:
   - State with explicit `timeout_s` uses it
   - State without `timeout_s` falls back to default
   - State with `timeout_s: 0` or negative is rejected

**Expected outputs:**

- Updated `schemas/workflow_config.schema.json` — optional `timeout_s` in state definitions
- Updated `orchestrator/step_compiler.py` — reads `timeout_s` from state definition
- Updated `tests/test_step_compiler.py` — timeout_s resolution tests

**Validation:** `python -c "import json, jsonschema; jsonschema.validate({'states': {'test': {'timeout_s': 60}}}, json.load(open('schemas/workflow_config.schema.json')))"` passes.

### Sub-phase 6m: Wire model_pin from config to StepContract

**Task:** `model_pin` exists on `StepContract` and the OpenCode adapter already reads it, but the workflow config schema has no field for it and the step compiler never reads it from the config. Complete the pipeline.

**Files to read:**

- `schemas/workflow_config.schema.json` (state definition properties)
- `orchestrator/step_compiler.py` (`compile_step_contract`)
- `.agent_work/ideation/deep_determinism/workflow_config_sketch.md` (model_pin usage examples)

**Steps:**

1. Add `model_pin` to the workflow config schema's state definition as an optional string.
2. In `compile_step_contract()`, read `model_pin` from the state definition. Pass it through to `StepContract.model_pin`.
3. The OpenCode adapter already has `_build_command()` logic that uses `contract.model_pin` when set — this completes the data pipeline without modifying the adapter.
4. Add test cases to `tests/test_step_compiler.py`:
   - State with `model_pin` sets it on StepContract
   - State without `model_pin` leaves it as None
   - State with empty string `model_pin` is treated as None

**Expected outputs:**

- Updated `schemas/workflow_config.schema.json` — optional `model_pin` in state definitions
- Updated `orchestrator/step_compiler.py` — reads `model_pin` from state definition
- Updated `tests/test_step_compiler.py` — model_pin tests

**Validation:** StepContract produced from a config with `model_pin: "qwen2.5:72b"` has `model_pin == "qwen2.5:72b"`.

### Sub-phase 6n: Wire ralph_max_cycles from config to StepContract

**Task:** `ralph_max_cycles` exists on `StepContract` but the workflow config schema has no field for it and the step compiler never reads it from config. The plan hardcodes 3 Ralph iterations uniformly — you can't say "this state gets 1 pass, that state gets 5."

**Files to read:**

- `schemas/workflow_config.schema.json` (state definition properties)
- `orchestrator/step_compiler.py` (`compile_step_contract`)
- `orchestrator/adapters/base.py` (StepContract dataclass — confirm `ralph_max_cycles` field)

**Steps:**

1. Add `ralph_max_cycles` to the workflow config schema's state definition as an optional integer (minimum 0, default 3).
2. In `compile_step_contract()`, read `ralph_max_cycles` from the state definition. Default to 3 if absent.
3. The value flows through StepContract to the orchestrator's transition resolver, which already checks `step_contract.ralph_max_cycles` when deciding whether to enter/exit the Ralph loop.
4. Add test cases to `tests/test_step_compiler.py`:
   - State with `ralph_max_cycles: 5` sets it on StepContract
   - State without `ralph_max_cycles` defaults to 3
   - State with `ralph_max_cycles: 0` disables Ralph (Ralph loop is skipped)

**Expected outputs:**

- Updated `schemas/workflow_config.schema.json` — optional `ralph_max_cycles` in state definitions
- Updated `orchestrator/step_compiler.py` — reads `ralph_max_cycles` from state definition
- Updated `tests/test_step_compiler.py` — ralph_max_cycles tests

**Validation:** StepContract produced from a config with `ralph_max_cycles: 1` has `ralph_max_cycles == 1`.

### Sub-phase 6p: Implement RESULT.json fallback protocol

**Task:** When the orchestrator replaces contextsmith-run, existing task-state directories may not have RESULT.json. The orchestrator must handle missing RESULT.json gracefully by falling back to artifact presence + exit code. This is the backward-compatibility layer for the run-to-orchestrator migration.

**Files to read:**

- `.agent_work/ideation/deep_determinism/migration_run_to_orchestrator.md` (lines 59-63, fallback protocol)
- `orchestrator/orchestrator.py` (post-execution result collection)
- `orchestrator/adapters/base.py` (HarnessResult — confirm all status values)

**Steps:**

1. In the post-execution result collection path in `orchestrator.py`, after harness execution:
   - If `harness_result.status` is already set from RESULT.json, use it as-is.
   - If `harness_result.status` is unknown/unset and no RESULT.json was found:
     - Check `harness_result.artifacts_written` length.
     - If > 0 and all expected outputs exist → `status = "pass"`.
     - If > 0 but some expected outputs missing → `status = "fail"` with issue: `"RESULT.json missing: fell back to artifact presence check. Missing: [files]"`.
     - If 0 → `status = "fail"` with issue: `"RESULT.json missing: no artifacts written."`.
2. Log a warning whenever the fallback is triggered: `"[orchestrator] RESULT.json missing — using artifact presence fallback for step {step_id}"`.
3. Document the fallback protocol in the orchestrator SKILL.md under the Artifact Validation section: "If RESULT.json is absent, the orchestrator infers status from artifact presence. All expected outputs present → pass. Partial → fail with details. None → fail."
4. Add test cases to `tests/test_orchestrator_integration.py`:
   - No RESULT.json, all artifacts present → pass
   - No RESULT.json, partial artifacts → fail with specific issue message
   - No RESULT.json, no artifacts → fail
   - RESULT.json present takes priority over artifact presence

**Expected outputs:**

- Updated `orchestrator/orchestrator.py` — RESULT.json fallback logic
- Updated `skills/contextsmith-orchestrator/SKILL.md` — fallback documented
- Updated `tests/test_orchestrator_integration.py` — fallback tests

**Validation:** Run without RESULT.json in state dir → orchestrator infers status from artifact presence. All existing tests still pass.

### Sub-phase 6q: Document "agent output is evidence" rule

**Task:** Nowhere in the orchestrator code or SKILL.md does it explicitly state that the orchestrator owns state transitions — not the agent. An agent could claim "status: done, next_action: done" in RESULT.json and the orchestrator's current code would follow it. The orchestration loop should document and enforce this.

**Files to read:**

- `orchestrator/orchestrator.py` (`resolve_next_state` and transition logic)
- `skills/contextsmith-orchestrator/SKILL.md` (agent-facing instructions)
- `.agent_work/ideation/deep_determinism/audit_and_ralph_state_machine.md` (line 83: "The agent's output is only evidence; it does not define the state machine.")

**Steps:**

1. In `orchestrator/orchestrator.py`, above `resolve_next_state()`, add a docstring block:
   ```python
   def resolve_next_state(...):
       """Deterministic state transition.
       
       The orchestrator owns all state transitions. The agent's RESULT.json
       provides evidence of completion (status, artifacts), but the orchestrator
       alone decides the next state by matching transition conditions from the
       workflow config against that evidence.
       
       Rule: Agent output is evidence, not authority. The agent never chooses
       its next state. If no transition condition matches, the orchestrator
       transitions to 'blocked', not to whatever the agent requested.
       """
   ```
2. Verify the current `resolve_next_state()` implementation already follows this rule (it reads transitions from config, not from RESULT.json). If it references `result.next_action` for transition decisions, change it to only use the workflow config's transition list.
3. Add a paragraph to `skills/contextsmith-orchestrator/SKILL.md` under Transition Resolution:
   ```markdown
   **Agent output is evidence, not authority.** The RESULT.json status tells
   the orchestrator whether the phase completed, but the orchestrator alone
   decides what state comes next by matching transition conditions from the
   workflow config. The agent cannot override the state machine. If no
   transition condition matches the RESULT.json status and artifact state,
   the orchestrator transitions to `blocked`.
   ```
4. Add test case to `tests/test_orchestrator_integration.py`:
   - Agent returns RESULT.json with `next_action: "done"` but config has more phases → orchestrator continues to next phase, does not stop
   - Agent returns RESULT.json with `status: "fail"` but transition condition is `pass` for next state → orchestrator resolves based on config, not agent hint

**Expected outputs:**

- Updated `orchestrator/orchestrator.py` — docstring on `resolve_next_state` + code audit
- Updated `skills/contextsmith-orchestrator/SKILL.md` — "agent output is evidence" paragraph
- Updated `tests/test_orchestrator_integration.py` — transition authority tests

**Validation:** An agent RESULT.json claiming `next_action: "done"` does not terminate a workflow that has more phases defined.

---

## Phase 7: Integration and Testing

**Goal:** Wire everything together and verify end-to-end.

### Sub-phase 7a: Extend unit tests for orchestrator

**Task:** Extend existing test coverage for all orchestrator components. Some test files already exist from Phase 4; add missing tests.

**Files to read:**

- `tests/test_validators.py` (existing — extend, do not recreate)

**Steps:**

1. Check existing test files: `test_validators.py`, `test_adapters.py`, `test_orchestrator_integration.py` already exist
2. Create `tests/test_orchestrator_state.py` — test state reader (if missing)
3. Create `tests/test_checkpoint.py` — test checkpoint manager (if missing)
4. Create `tests/test_step_compiler.py` — test step compiler (if missing)
5. Extend `tests/test_validators.py` — add any missing test cases
6. Extend `tests/test_adapters.py` — add any missing test cases

**Expected outputs:**

- Coverage for all 5 component areas (state reader, checkpoint, step compiler, validators, adapters)

**Validation:** `pytest tests/` passes.

### Sub-phase 7b: Extend integration tests

**Task:** Extend existing integration test coverage. `tests/test_orchestrator_integration.py` already exists from Phase 4d — extend it, do not recreate.

**Files to read:**

- `tests/test_orchestrator_integration.py` (existing — extend)

**Steps:**

1. Extend `tests/test_orchestrator_integration.py` with:
   - Test: load config → execute all phases → verify done state
   - Test: resume after simulated crash
   - Test: max retries → blocked state
   - Test: --dry-run mode

**Expected outputs:**

- Extended `tests/test_orchestrator_integration.py`

**Validation:** `pytest tests/test_orchestrator_integration.py` passes.

### Sub-phase 7c: Update validation script

**Task:** Update validate_skills.py to recognize new skills.

**Files to read:**

- `scripts/validate_skills.py`

**Steps:**

1. Verify new skills are detected
2. Add any missing validation rules
3. Run full validation

**Expected outputs:**

- Updated `scripts/validate_skills.py` if needed

**Validation:** `python scripts/validate_skills.py` passes for all skills.

---

## Ralph Loop Configuration

Each sub-phase must undergo **3 Ralph iterations**. Each iteration is identical in structure — critique, identify improvements, fix, and record. Do not skip iterations or collapse them into a single pass.

No-op iterations are valid evidence. They mean no material defect was found at that iteration.
Do not invent changes to satisfy the iteration count. Record no-op with the reason
"no material defect found."

### Per-Iteration Structure

Each iteration does the same thing:

**1. Critique** — Review the implementation against the execution contract. Identify material defects, gaps, edge cases, or spec violations.

**2. Strategic review (mandatory):**

- Ask: "Does this work progress the goals of the sprint/task? How?"
- Ask: "Beyond baseline requirements, how can this be improved?"
- Ask: "What is the gap between 'done' and 'well done'?"
- Ask: "Is there a better approach, pattern, or design than what was implemented?"
- Act on any improvement insight that is material (not cosmetic)
- Record what strategic improvements were identified and applied

**3. Cross-reference with future phases:** Before acting on any improvement, check whether it is already covered by a future phase of the implementation plan. If already planned:

- Add concrete detail to that future phase's description in PLAN.md (steps, expected outputs, validation)
- Add any new checklist items to CHECKLIST.md under the correct future phase
- Record the decision in DECISIONS.md with reference to the phase where it will be implemented
- Do NOT implement it now — the future phase will handle it

**4. Fix material defects** — Apply fixes found in critique and strategic review. If an improvement is complex and not already planned, add it as a new sub-phase instead of implementing inline.

**5. Record** — Log what was critiqued, what was fixed, and what strategic improvements were identified. If no material defect remains, record as no-op.

### Handling Complex Improvements

If the strategic review identifies changes that are complex, multi-file, cross-cutting, would take longer than the current sub-phase allows, AND are NOT already covered by a future phase, do NOT try to implement them in one pass. Instead:

1. Add a new sub-phase or phase to PLAN.md documenting the improvement work
2. Update CHECKLIST.md with the new items
3. Update STATUS.md and NEXT_PROMPT.md to reflect the adjusted plan
4. Record the decision in DECISIONS.md with rationale
5. Complete the current sub-phase as-is (or with only the quick fixes from the critique)
6. The new sub-phases will be picked up by the next agent pass

This keeps Ralph loops bounded. The loop critiques the current sub-phase's work; it does not execute unbounded refactors. Architecturally significant improvements get planned, not forced into a single iteration. For improvements already in the plan, enrich the future phase instead of implementing early.

### Ralph Focus Areas

- Code quality (readability, maintainability)
- Test coverage (edge cases, error paths)
- Documentation (comments, docstrings)
- Consistency (with existing codebase conventions)
- Small-model friendliness (atomic instructions, clear structure)
- Sprint goal alignment: does this sub-phase advance the overall sprint objective?
- Improvement over baseline: not just "correct" but "well-considered"

### Ralph Enforcement

Each iteration must have a compact log entry in the final output under `## Ralph Summary`.
Ralph loops are critique/revision passes, not repeated blind tool calls.
Do not rerun commands or edits unless the critique identifies a concrete reason.
Strategic review questions must be answered explicitly — even if the answer is "no improvement needed, work is already well-executed for this phase."
If no material defect remains before iteration N, record remaining iterations as
no-op by evidence.

---

## Dependency Graph

```
Phase 1 (Schemas)
    ↓
Phase 2 (Core)
    ↓
Phase 3 (Adapters) ──→ Phase 3.5 (Bug Fixes)
    ↓
Phase 4 (Validators)
    ↓
Phase 5 (Skills)
    ↓
Phase 5.5 (Quality Fixes) ──→ addresses 7 audit findings before collapse
    ↓
Phase 6 (Collapse + Hardening) ──→ 17 sub-phases: remove contextsmith-run, unify on
                                      orchestrator, wire determinism features
    ↓
Phase 6.75 (Complexity Cleanup) ──→ add radon to validation pipeline, refactor
                                      C-ranked functions to ≤ B
    ↓
Phase 7 (Integration & Testing)
```

Phases 3 and 4 ran in parallel after Phase 2.
Phase 5.5 fixes pre-conditions for Phase 6 (deep_determinism refs, ruff errors, missing harness companion, version scheme).
Phase 6 has 17 sub-phases: 6a-6g (collapse) + 6h-6q (determinism hardening). The hardening sub-phases wire features that exist in the data model but were never connected to the execution loop.
Phase 6h-6q must complete before Phase 7. They can run in any order as they touch different files, but 6q (agent-evidence rule) should be last since it documents behavior changes from the other sub-phases.
Phase 6.75 addresses complexity findings from Phase 6 review before integration testing.
Phase 7 depends on all previous phases.

---

## Phase 6.75: Complexity Cleanup

**Goal:** Add `uvx radon cc` and `uvx radon mi` to the validation toolkit. Refactor all C-ranked functions in the orchestrator to ≤ B complexity. Integrate the check into AGENTS.md, the orchestrator skill, and the shared validation pipeline.

### Findings: Current C-Ranked Functions

| File | Function | Complexity | Target |
| ------ | ---------- | ----------- | -------- |
| orchestrator/orchestrator.py | `_execute_and_validate_step` | C (19) | ≤ B (10) |
| orchestrator/orchestrator.py | `run` | C (18) | ≤ B (10) |
| orchestrator/orchestrator.py | `run_workflow` | C (13) | ≤ B (10) |
| orchestrator/validators.py | `validate_checkpoint_file` | C (17) | ≤ B (10) |
| orchestrator/validators.py | `validate_state_consistency` | C (15) | ≤ B (10) |
| orchestrator/cli.py | `cmd_validate` | C (13) | ≤ B (10) |
| orchestrator/cli.py | `cmd_diff` | C (12) | ≤ B (10) |
| orchestrator/cli.py | `cmd_resume` | C (11) | ≤ B (10) |
| orchestrator/checkpoint.py | `validate_checkpoint` | C (13) | ≤ B (10) |

### Sub-phase 6.75a: Add radon to pipeline docs

**Task:** Add radon complexity checks to AGENTS.md, orchestrator SKILL.md reference loading table, and shared validation references.

**Steps:**

1. Update AGENTS.md with complexity/maintainability section (done)
2. Add a `references/complexity-gate.md` to orchestrator and shared/ so the rule is loadable as a reference
3. Reference it from orchestrator SKILL.md reference loading table

**Expected outputs:**

- Updated AGENTS.md
- `shared/complexity-gate.md`
- `skills/contextsmith-orchestrator/references/complexity-gate.md`
- Updated orchestrator reference_manifest.yml

### Sub-phase 6.75b: Refactor orchestrator.py C-ranked functions

**Task:** Extract helper functions from `_execute_and_validate_step`, `run`, and `run_workflow` to bring each under B (10).

**Approach:**

- `_execute_and_validate_step` (C/19): Extract RESULT.json fallback into `_apply_result_fallback()` and validation-mode branches into private helpers.
- `run` (C/18): Extract pre-dispatch setup into `_run_predispatch_setup()`. Extract post-dispatch persistence into a cleaner flow.
- `run_workflow` (C/13): Already has clear structure — may need minimal changes.

### Sub-phase 6.75c: Refactor validators.py C-ranked functions

**Task:** Extract helper functions from `validate_checkpoint_file` (C/17) and `validate_state_consistency` (C/15).

**Approach:**

- `validate_checkpoint_file`: Extract required-field check and config-cross-reference check.
- `validate_state_consistency`: Break into section-based validators.

### Sub-phase 6.75d: Refactor cli.py and checkpoint.py C-ranked functions

**Task:** Extract helpers from `cmd_validate`, `cmd_diff`, `cmd_resume`, and `validate_checkpoint`.

### Validation Commands

```bash
uvx radon cc orchestrator/ -s -a | grep -E " - [CDEF] "  # no output = no C/D/E/F
uvx radon mi orchestrator/ -s | grep -E " - [BCDEF] "    # no output = all A
uv run ruff check orchestrator/ --select E,F,W,I
uv run ruff format orchestrator/ --check
uv run pytest tests/ -q
```

## Phase 7: Integration and Testing — Expanded Scope

**Goal:** Wire everything together and verify end-to-end. In addition to baseline testing, address findings from Phase 6 review.

### Findings from Phase 6 Review: Items for Phase 7

The following were identified during Phase 6 completion review and should be addressed in Phase 7:

| Finding | Priority | Where to Fix |
| --------- | ---------- | ------------- |
| Dedicated unit tests needed for 10 new determinism features (exit codes, validation_mode, checkpoint_before_run, pre-dispatch counter, RESULT.json fallback, append validation, model_pin, agent-evidence rules) | High | Phase 7a |
| Integration tests should exercise each new determinism feature end-to-end | High | Phase 7b |
| schema deprecation warning: draft-07 metaschema | Low | Phase 7c or standalone |
| orchestrator SKILL.md 571 lines > 500 target — extract artifact templates to reference file | Medium | Phase 7c |

### Sub-phase 7a: Extend unit tests for orchestrator

**Task:** Extend existing test coverage for all orchestrator components. **Must include** at minimum:

- `tests/test_orchestrator_state.py` — test state reader (if missing)
- `tests/test_checkpoint.py` — test checkpoint manager (if missing), including pre-dispatch marker lifecycle
- `tests/test_step_compiler.py` — test step compiler (if missing), including model_pin/timeout_s/ralph_max_cycles resolution
- `orchestrator/test_validators.py` — add test cases for `validate_append_only()`:
  - Appended file passes validation
  - Overwritten file fails validation
  - Empty new file fails validation
  - Repair via prepend restores original content
- New test file `tests/test_orchestrator_determinism.py` — dedicated unit tests for:
  - Exit code mapping: valid run → 0, blocked → 1, continue → 2, config error → 3, state inconsistency → 4, internal error → 5
  - validation_mode=strict blocks on missing artifact
  - validation_mode=relaxed warns but passes on missing artifact
  - validation_mode=none skips artifact validation
  - checkpoint_before_run writes pre-dispatch marker
  - Pre-dispatch counter: max_retries=0 blocks without dispatching
  - RESULT.json fallback: no RESULT.json + all artifacts → pass
  - RESULT.json fallback: no RESULT.json + partial artifacts → fail
  - RESULT.json fallback: no RESULT.json + no artifacts → fail
  - RESULT.json priority: present result takes precedence over fallback
  - Agent transition authority: agent next_action does not override config

**Expected outputs:**

- All test files extended with coverage for above scenarios

**Validation:** `pytest tests/` passes with expanded test count.

### Sub-phase 7b: Extend integration tests

**Task:** Extend `tests/test_orchestrator_integration.py` with end-to-end integration tests.

**Must include:**

- Test: load config → execute all phases → verify done state
- Test: resume after simulated crash (pre-dispatch marker detection)
- Test: max retries → blocked (pre-dispatch counter check)
- Test: `--dry-run` mode prints step without executing
- Test: exit code 3 (config error) propagates through run_workflow
- Test: exit code 4 (state inconsistency) propagates
- Test: exit code 5 (internal error) propagates
- Test: append-only file snapshot + repair on overwrite

**Validation:** `pytest tests/test_orchestrator_integration.py` passes.

### Sub-phase 7c: Update validation script

**Task:** Update validate_skills.py to recognize new skills. Also address:

- Verify orchestrator SKILL.md artifact templates could be extracted (document, don't necessarily do)
- Document markdownlint MD060 table-style issues in docs/workflows/ (pre-existing, not blocking)

**Validation:** `python scripts/validate_skills.py` passes for all skills.

---

## Phase 8: Documentation and Polish

**Goal:** Finalize user-facing docs, trim orchestrator SKILL.md, fix schema deprecation.

### Sub-phase 8a: Trim orchestrator SKILL.md
Move the full artifact templates (STATUS.md, PHASE_LOG.md, CHECKLIST.md, NEXT_PROMPT.md examples) to `references/artifact-templates.md`. Reference them from the SKILL.md with a short table. This should bring the SKILL.md under 500 lines.

### Sub-phase 8b: Fix schema deprecation
Update `$schema` in `schemas/workflow_config.schema.json` from `draft-07` to `https://json-schema.org/draft/2020-12/schema` if compatible. Update metaschema URI. Test all fixtures still validate.

### Sub-phase 8c: Update user-facing docs

- Update CONTRIBUTING.md if needed
- Run markdownlint across all docs/ and fix MD060 table-style issues
- Update EXAMPLES_LIBRARY.md with orchestrator examples (contextsmith-run → orchestrator migration notes)

### Sub-phase 8d: CHANGELOG entry
Write a comprehensive CHANGELOG.md entry covering:

- contextsmith-run removed, all execution via contextsmith-orchestrator
- Determinism hardening: exit codes 0-5, validation modes, pre-dispatch checkpoints, per-state parameters
- Append-only file protection with auto-repair
- Version bump 1.7.1 → 2.0.0

---

## Phase 9: Final Validation and Lock

**Goal:** Run full validation suite one final time, produce final status artifacts.

### Sub-phase 9a: Full validation pass
Run: `ruff check`, `ruff format --check`, `validate_skills.py`, `pytest`, `markdownlint`. Fix any remaining issues.

### Sub-phase 9b: Final self-audit
Audit all phases 1-9 against the A-F rubric. Verify every expected_output from every sub-phase exists and is non-empty.

### Sub-phase 9c: Project closeout

- Verify git status is clean
- Check staged_skills/ in .agent_work/ for stale artifacts
- Write final DECISIONS.md entry
- Tag release if applicable
