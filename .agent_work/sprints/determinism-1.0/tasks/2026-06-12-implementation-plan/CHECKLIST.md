# Checklist

## Prerequisites

- [x] Verify jsonschema is installed
- [x] Verify PyYAML is installed
- [ ] Verify pytest is installed
- [x] Verify scripts/validate_skills.py exists
- [x] Verify schemas/workflow_config.schema.json exists
- [x] Verify schemas/agent_config.schema.json exists

## Self-Audit Gate (every phase)

After each implementation phase, before writing RESULT.json:

- [x] All expected output files exist
- [x] All expected output files are non-empty
- [x] Code compiles (for Python phases): `python -c "import orchestrator.<module>"`
- [ ] Tests pass (if tests exist): `pytest tests/test_<module>.py -v`
- [x] No TODOs, FIXMEs, or HACKs in written files
- [x] No placeholders (..., TBD, PLACEHOLDER) in written files
- [x] Imports resolve (no circular imports)
- [x] Docstrings present on all public functions
- [x] Style matches existing code conventions
- [x] Implementation matches spec in deep_determinism/

## Phase 1: Verify Schemas and Create Test Fixtures

### Sub-phase 1a: Verify workflow_config.schema.json

- [x] Read schema file
- [x] Read simple audit example
- [x] Read engineering example
- [x] Validate simple audit against schema
- [x] Validate engineering against schema
- [x] Save valid fixtures to tests/fixtures/
- [x] Record validation results

### Sub-phase 1b: Verify agent_config.schema.json

- [x] Read schema file
- [x] Read auditor agent example
- [x] Read builder agent example
- [x] Validate auditor against schema
- [x] Validate builder against schema
- [x] Save valid fixtures to tests/fixtures/
- [x] Record validation results

### Sub-phase 1c: Create invalid test fixtures

- [x] Create workflow with missing required field
- [x] Create workflow with invalid state reference
- [x] Create workflow with invalid transition target
- [x] Create agent with missing permission
- [x] Create agent with invalid mode
- [x] Verify all invalid fixtures fail validation

### Sub-phase 1d: Create task-state test fixtures

- [x] Create valid task-state directory
- [x] Create task-state missing STATUS.md
- [x] Create task-state with empty PLAN.md
- [x] Create task-state with invalid checkpoint.json
- [x] Verify valid fixture passes checks
- [x] Verify invalid fixtures fail with specific errors

## Phase 2: Core Orchestrator Module

### Sub-phase 2a: Create orchestrator package structure

- [x] Create orchestrator/ directory
- [x] Create __init__.py with public API
- [x] Create constants.py with exit codes and states
- [x] Create exceptions.py with custom exceptions
- [x] Verify import works

### Sub-phase 2b: Implement state reader

- [x] Create state_reader.py
- [x] Implement read_status()
- [x] Implement read_plan()
- [x] Implement read_context()
- [x] Implement read_checkpoint()
- [x] Add validation for each parser
- [x] Test with valid fixture

### Sub-phase 2c: Implement checkpoint manager

- [x] Create checkpoint.py
- [x] Implement read_checkpoint()
- [x] Implement write_checkpoint() with atomic writes
- [x] Implement update_checkpoint() for counters
- [x] Implement validate_checkpoint()
- [x] Test round-trip write/read

### Sub-phase 2d: Implement step compiler

- [x] Create step_compiler.py
- [x] Define StepContract and HarnessResult (or import)
- [x] Implement compile_step_contract()
- [x] Implement resolve_next_state()
- [x] Implement _matches_condition()
- [x] Test with test fixture

### Sub-phase 2e: Implement main loop

- [x] Create orchestrator.py
- [x] Implement run() for single step
- [x] Implement run_workflow() for outer loop
- [x] Implement should_stop() for STOP file
- [x] Implement register_signal_handlers()
- [x] Wire together all components
- [x] Test with --dry-run

### Sub-phase 2f: Implement CLI interface

- [x] Create cli.py
- [x] Implement argument parsing
- [x] Implement subcommands (run, init, validate, inspect, diff, resume)
- [x] Wire to orchestrator functions
- [x] Test --help output

### Bug Fix Pass

- [x] Fix _list() strip bug in state_reader.py
- [x] Fix max_retries condition in step_compiler.py
- [x] Fix _update_status destroying STATUS.md structure
- [x] Fix _update_status writing "unknown" for phase
- [x] Reconcile duplicate read_checkpoint functions
- [x] Add YAML config loading support
- [x] Fix datetime.utcnow() deprecation warnings
- [x] Fix update_checkpoint mutation bug
- [x] Fix CLI argparse conflicts
- [x] Fix run_workflow silently dropping flags
- [x] Add file locking for state directory
- [x] Add config validation against schemas
- [x] Add report file protection system
- [x] Test all fixes end-to-end

## Phase 3: Harness Adapters

### Sub-phase 3a: Create adapter base classes

- [x] Create adapters/ directory
- [x] Create __init__.py with ADAPTER_REGISTRY
- [x] Create base.py with StepContract dataclass
- [x] Create base.py with HarnessResult dataclass
- [x] Create base.py with HarnessAdapter ABC
- [x] Create base.py with HarnessRegistry
- [x] Create base.py with error types
- [x] Verify import works

### Sub-phase 3b: Implement generic adapter

- [x] Create generic.py
- [x] Implement GenericAdapter class
- [x] Implement name, validate_environment, execute, cancel, get_capabilities
- [x] Register with HarnessRegistry
- [x] Test with test fixture

### Sub-phase 3c: Implement OpenCode adapter

- [x] Create opencode.py
- [x] Implement OpenCodeAdapter class
- [x] Implement _build_command() with verified flags
- [x] Implement _read_result() for RESULT.json
- [x] Register with HarnessRegistry
- [x] Test validate_environment()

## Phase 3.5: Integration and Bug Fixes

### Critical Integration

- [x] Wire adapters into orchestrator.py
- [x] Replace simulated execution with actual adapter calls
- [x] Add adapter discovery and environment validation
- [x] Wire HarnessResult into state transition logic

### Adapter Bug Fixes

- [x] Fix OpenCodeAdapter.cancel() — use Popen instead of run
- [x] Fix GenericAdapter test_mode — write artifacts to disk
- [x] Rename await_human to poll_human — clarify polling behavior
- [x] Fix OpenCodeAdapter exit code handling — prioritize RESULT.json

### Architectural Improvements

- [x] Add logging module — replace all print() statements
- [x] Add config validation — validate workflow config against schema
- [x] Fix unused imports — remove Path and Optional from step_compiler.py
- [x] Fix HarnessRegistry error handling — create HarnessNotFoundError

### Tests

- [x] Create tests/test_adapters.py
- [x] Test HarnessRegistry registration and discovery
- [x] Test GenericAdapter execute, test_mode, poll_human
- [x] Test OpenCodeAdapter command building, validation, capabilities
- [x] Test StepContract and HarnessResult dataclasses
- [x] Test exception types
- [x] All 28 tests passing

### Code Quality

- [x] Install ruff
- [x] Run ruff check --fix on all Python code
- [x] Run ruff format on all Python code
- [x] Fix all line-too-long errors manually
- [x] All ruff checks pass (E, F, W, I)
- [x] Update AGENTS.md with ruff commands
- [x] Update PLAN.md with ruff in validation pipeline

### Environment Setup

- [x] Install uv package manager
- [x] Initialize uv project (pyproject.toml already existed)
- [x] Add dependencies: ruff, pytest, pyyaml, jsonschema
- [x] Create .venv with uv venv
- [x] Sync dependencies with uv sync
- [x] Update AGENTS.md with uv workflow
- [x] Update PLAN.md with uv commands
- [x] Verify all commands work with uv run

## Phase 4: Validators

### Sub-phase 4a: Implement file validators

- [x] Create tests/test_validators.py (test-first — 29 tests)
- [x] Create validators.py
- [x] Implement validate_file_exists()
- [x] Implement validate_file_nonempty()
- [x] Implement validate_required_sections()
- [x] Implement validate_artifact()
- [x] Implement validate_artifacts()
- [x] Test with fixtures

### Sub-phase 4b: Implement schema validators

- [x] Add validate_schema()
- [x] Add validate_workflow_config()
- [x] Add validate_agent_config()
- [x] Add validate_checkpoint()
- [x] Test with valid and invalid configs

### Sub-phase 4c: Implement state consistency validator

- [x] Add validate_state_consistency()
- [x] Test with consistent state
- [x] Test with inconsistent state

### Sub-phase 4d: Wire validators into orchestrator

- [x] Import validators in orchestrator.py
- [x] Call validate_artifacts() after harness execution
- [x] Call validate_state_consistency() before state transitions
- [x] Call validate_workflow_config() at startup
- [x] Write integration tests
- [x] All tests pass

## Phase 5: Orchestrator Skill and Workflow Developer

### Sub-phase 5a: Create orchestrator SKILL.md

- [ ] Create skills/contextsmith-orchestrator/ directory
- [ ] Create SKILL.md from draft
- [ ] Create reference_manifest.yml
- [ ] Add shared references
- [ ] Run validate_skills.py

### Sub-phase 5b: Create workflow developer SKILL.md

- [ ] Create skills/contextsmith-workflow-developer/ directory
- [ ] Create SKILL.md
- [ ] Create reference_manifest.yml
- [ ] Copy domain templates
- [ ] Run validate_skills.py

### Sub-phase 5c: Update router skill

- [ ] Add contextsmith-orchestrator to routing table
- [ ] Add contextsmith-workflow-developer to routing table
- [ ] Update wizard Q1 options
- [ ] Run validate_skills.py

## Phase 6: Integration and Testing

### Sub-phase 6a: Create orchestrator __main__.py

- [ ] Create __main__.py
- [ ] Test python -m orchestrator --help

### Sub-phase 6b: Create unit tests

- [ ] Create test_orchestrator_state.py
- [ ] Create test_checkpoint.py
- [ ] Create test_step_compiler.py
- [ ] Create test_validators.py
- [ ] Create test_adapters.py
- [ ] Run pytest

### Sub-phase 6c: Create integration test

- [ ] Create test_orchestrator_integration.py
- [ ] Test end-to-end execution
- [ ] Test resume after crash
- [ ] Test max retries → blocked
- [ ] Test --dry-run mode
- [ ] Run pytest

### Sub-phase 6d: Update validation script

- [ ] Verify new skills detected
- [ ] Add missing validation rules
- [ ] Run full validation
