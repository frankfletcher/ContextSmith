# Implementation Plan: Deep Determinism

## Phase Overview

This plan has 6 major phases, each broken into sub-phases. Each phase follows:
1. Implement
2. Audit (pass/fail)
3. Ralph critique (3 cycles)
4. Ralph revise (3 cycles)
5. Validate

Total: 6 major phases × ~5 sub-phases × (implement + audit + 3 Ralph cycles + validate) = ~150 steps

## Prerequisites

Before starting, verify these are installed:

```bash
python -c "import jsonschema; print('jsonschema OK')"
python -c "import yaml; print('PyYAML OK')"
python -c "import pytest; print('pytest OK')"
```

If any fail, install with `pip install jsonschema pyyaml pytest`.

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

### AUDIT_REPORT.md Template

```markdown
# Audit Report

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
python scripts/validate_skills.py

# Run tests
pytest tests/ -v

# Validate orchestrator module
python -c "from orchestrator import run; print('import OK')"

# Validate adapters
python -c "from orchestrator.adapters.base import HarnessAdapter; print('adapters OK')"
```

## File Size Constraints

Keep files small for small models:

| File | Max Lines | Purpose |
|------|-----------|---------|
| `orchestrator/__init__.py` | 30 | Public API exports |
| `orchestrator/constants.py` | 40 | Exit codes, state names |
| `orchestrator/exceptions.py` | 30 | Custom exceptions |
| `orchestrator/state_reader.py` | 100 | Parse STATUS.md, PLAN.md, CONTEXT.md, checkpoint.json |
| `orchestrator/checkpoint.py` | 80 | Read/write checkpoint.json |
| `orchestrator/step_compiler.py` | 120 | Compile StepContract, resolve transitions |
| `orchestrator/orchestrator.py` | 150 | Main loop, run_workflow, run |
| `orchestrator/cli.py` | 100 | Argument parsing, subcommands |
| `orchestrator/validators.py` | 150 | File, schema, state validation |
| `orchestrator/adapters/base.py` | 120 | ABC, dataclasses, registry, errors |
| `orchestrator/adapters/generic.py` | 80 | Generic adapter |
| `orchestrator/adapters/opencode.py` | 120 | OpenCode adapter |

Total: ~1120 lines of Python code.

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
3. **Code compiles** — `python -c "import orchestrator.<module>"` succeeds (for Python phases)
4. **Tests pass** — `pytest tests/test_<module>.py -v` succeeds (if tests exist)
5. **No TODOs left** — grep for `TODO`, `FIXME`, `HACK` in written files
6. **No placeholder content** — no `...`, `TBD`, `PLACEHOLDER` in written files
7. **Imports resolve** — no circular imports, no missing dependencies
8. **Docstrings present** — all public functions have docstrings
9. **Consistent style** — matches existing code conventions in the project
10. **Spec alignment** — implementation matches the spec files in deep_determinism/

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

## Educational Report

After every implementation phase, write an `EDUCATIONAL_REPORT.md` that explains:

### What Was Done
- List every file created or modified
- Summarize the key functions/classes added
- Note any design decisions made

### Why It Matters
- How this phase contributes to the overall system
- What problems this code solves
- How it fits with the other components

### How It Works
- Explain the key algorithms or patterns used
- Describe the data flow
- Note any non-obvious implementation choices

### For Small Models
- Keep explanations concrete and literal
- Use examples from the actual code
- Avoid abstract descriptions
- Include the actual function signatures

### Educational Report Template

```markdown
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
<input> → <processing> → <output>

## For Small Models
- <Concrete example of how to use this code>
- <Common mistakes to avoid>
- <What to check if something goes wrong>
```

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

**Task:** Create the orchestrator Python package with __init__.py and basic structure.

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

**Goal:** Implement validation functions for artifacts and workflow state.

### Sub-phase 4a: Implement file validators

**Task:** Implement file existence, non-empty, and section presence checks.

**Files to read:**
- `.agent_work/ideation/deep_determinism/state_artifact_strategy.md` (validation pseudocode)

**Steps:**
1. Create `orchestrator/validators.py`
2. Implement `validate_file_exists(path) -> list[str]` — check file exists
3. Implement `validate_file_nonempty(path) -> list[str]` — check file not empty
4. Implement `validate_required_sections(path, sections) -> list[str]` — check sections present
5. Implement `validate_artifact(file_path, required_sections) -> list[str]` — combine all checks
6. Implement `validate_artifacts(state_dir, expected_outputs, config) -> ValidationResult`

**Expected outputs:**
- `orchestrator/validators.py` — all validation functions

**Validation:** Validate test fixtures, verify pass/fail results match expectations.

### Sub-phase 4b: Implement schema validators

**Task:** Implement JSON/YAML schema validation.

**Files to read:**
- `schemas/workflow_config.schema.json`
- `schemas/agent_config.schema.json`

**Steps:**
1. Add `validate_schema(data, schema_path) -> list[str]` to validators.py
2. Add `validate_workflow_config(config_path) -> list[str]` — validate against schema
3. Add `validate_agent_config(agent_path) -> list[str]` — validate against schema
4. Add `validate_checkpoint(checkpoint_path, config) -> list[str]` — validate checkpoint

**Expected outputs:**
- Updated `orchestrator/validators.py` — schema validation functions

**Validation:** Validate valid configs pass, invalid configs fail with specific errors.

### Sub-phase 4c: Implement state consistency validator

**Task:** Validate consistency between STATUS.md, checkpoint.json, and workflow config.

**Files to read:**
- `.agent_work/ideation/deep_determinism/orchestrator_idea.md` (error handling matrix)

**Steps:**
1. Add `validate_state_consistency(status, checkpoint, config) -> list[str]`
2. Check: STATUS.md current_phase is valid state in config
3. Check: checkpoint.json current_phase matches STATUS.md
4. Check: checkpoint counters are within limits
5. Check: completed_phases exist in config phase_order

**Expected outputs:**
- Updated `orchestrator/validators.py` — state consistency check

**Validation:** Test with consistent state (pass) and inconsistent state (fail with specific error).

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

## Phase 6: Integration and Testing

**Goal:** Wire everything together and verify end-to-end.

### Sub-phase 6a: Create orchestrator __main__.py

**Task:** Make the orchestrator runnable as `python -m orchestrator`.

**Files to read:**
- `.agent_work/ideation/deep_determinism/orchestrator_idea.md` (CLI section)

**Steps:**
1. Create `orchestrator/__main__.py`
2. Import and call CLI main function
3. Test `python -m orchestrator --help`

**Expected outputs:**
- `orchestrator/__main__.py` — entry point

**Validation:** `python -m orchestrator --help` shows usage.

### Sub-phase 6b: Create unit tests

**Task:** Create unit tests for all orchestrator components.

**Files to read:**
- `tests/test_validator.py` (existing test patterns)

**Steps:**
1. Create `tests/test_orchestrator_state.py` — test state reader
2. Create `tests/test_checkpoint.py` — test checkpoint manager
3. Create `tests/test_step_compiler.py` — test step compiler
4. Create `tests/test_validators.py` — test validators
5. Create `tests/test_adapters.py` — test harness adapters

**Expected outputs:**
- 5 new test files with comprehensive coverage

**Validation:** `pytest tests/` passes.

### Sub-phase 6c: Create integration test

**Task:** Create end-to-end integration test.

**Files to read:**
- `tests/test_cli.py` (existing patterns)

**Steps:**
1. Create `tests/test_orchestrator_integration.py`
2. Test: load config → execute all phases → verify done state
3. Test: resume after simulated crash
4. Test: max retries → blocked state
5. Test: --dry-run mode

**Expected outputs:**
- `tests/test_orchestrator_integration.py` — integration tests

**Validation:** `pytest tests/test_orchestrator_integration.py` passes.

### Sub-phase 6d: Update validation script

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

Each major phase (2-6) will undergo 3 Ralph cycles:
- Ralph critique: identify defects, gaps, improvements
- Ralph revise: address critiques, improve quality

Ralph focuses on:
- Code quality (readability, maintainability)
- Test coverage (edge cases, error paths)
- Documentation (comments, docstrings)
- Consistency (with existing codebase conventions)
- Small-model friendliness (atomic instructions, clear structure)

---

## Dependency Graph

```
Phase 1 (Schemas) ──→ Phase 2 (Core) ──→ Phase 3 (Adapters) ──→ Phase 4 (Validators)
                                         ↓
                                    Phase 5 (Skills) ──→ Phase 6 (Integration)
```

Phases 3 and 4 can run in parallel after Phase 2.
Phase 5 depends on Phase 2 (needs orchestrator module).
Phase 6 depends on all previous phases.
