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
- [ ] Code compiles (for Python phases): `python -c "import orchestrator.<module>"`
- [ ] Tests pass (if tests exist): `pytest tests/test_<module>.py -v`
- [x] No TODOs, FIXMEs, or HACKs in written files
- [x] No placeholders (..., TBD, PLACEHOLDER) in written files
- [ ] Imports resolve (no circular imports)
- [ ] Docstrings present on all public functions
- [ ] Style matches existing code conventions
- [ ] Implementation matches spec in deep_determinism/

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
- [ ] Create orchestrator/ directory
- [ ] Create __init__.py with public API
- [ ] Create constants.py with exit codes and states
- [ ] Create exceptions.py with custom exceptions
- [ ] Verify import works

### Sub-phase 2b: Implement state reader
- [ ] Create state_reader.py
- [ ] Implement read_status()
- [ ] Implement read_plan()
- [ ] Implement read_context()
- [ ] Implement read_checkpoint()
- [ ] Add validation for each parser
- [ ] Test with valid fixture

### Sub-phase 2c: Implement checkpoint manager
- [ ] Create checkpoint.py
- [ ] Implement read_checkpoint()
- [ ] Implement write_checkpoint() with atomic writes
- [ ] Implement update_checkpoint() for counters
- [ ] Implement validate_checkpoint()
- [ ] Test round-trip write/read

### Sub-phase 2d: Implement step compiler
- [ ] Create step_compiler.py
- [ ] Define StepContract and HarnessResult (or import)
- [ ] Implement compile_step_contract()
- [ ] Implement resolve_next_state()
- [ ] Implement _matches_condition()
- [ ] Test with test fixture

### Sub-phase 2e: Implement main loop
- [ ] Create orchestrator.py
- [ ] Implement run() for single step
- [ ] Implement run_workflow() for outer loop
- [ ] Implement should_stop() for STOP file
- [ ] Implement register_signal_handlers()
- [ ] Wire together all components
- [ ] Test with --dry-run

### Sub-phase 2f: Implement CLI interface
- [ ] Create cli.py
- [ ] Implement argument parsing
- [ ] Implement subcommands (run, init, validate, inspect, diff, resume)
- [ ] Wire to orchestrator functions
- [ ] Test --help output

## Phase 3: Harness Adapters

### Sub-phase 3a: Create adapter base classes
- [ ] Create adapters/ directory
- [ ] Create __init__.py with ADAPTER_REGISTRY
- [ ] Create base.py with StepContract dataclass
- [ ] Create base.py with HarnessResult dataclass
- [ ] Create base.py with HarnessAdapter ABC
- [ ] Create base.py with HarnessRegistry
- [ ] Create base.py with error types
- [ ] Verify import works

### Sub-phase 3b: Implement generic adapter
- [ ] Create generic.py
- [ ] Implement GenericAdapter class
- [ ] Implement name, validate_environment, execute, cancel, get_capabilities
- [ ] Register with HarnessRegistry
- [ ] Test with test fixture

### Sub-phase 3c: Implement OpenCode adapter
- [ ] Create opencode.py
- [ ] Implement OpenCodeAdapter class
- [ ] Implement _build_command() with verified flags
- [ ] Implement _read_result() for RESULT.json
- [ ] Register with HarnessRegistry
- [ ] Test validate_environment()

## Phase 4: Validators

### Sub-phase 4a: Implement file validators
- [ ] Create validators.py
- [ ] Implement validate_file_exists()
- [ ] Implement validate_file_nonempty()
- [ ] Implement validate_required_sections()
- [ ] Implement validate_artifact()
- [ ] Implement validate_artifacts()
- [ ] Test with fixtures

### Sub-phase 4b: Implement schema validators
- [ ] Add validate_schema()
- [ ] Add validate_workflow_config()
- [ ] Add validate_agent_config()
- [ ] Add validate_checkpoint()
- [ ] Test with valid and invalid configs

### Sub-phase 4c: Implement state consistency validator
- [ ] Add validate_state_consistency()
- [ ] Test with consistent state
- [ ] Test with inconsistent state

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
