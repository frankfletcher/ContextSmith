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
- [x] Tests pass (if tests exist): `pytest tests/ -q` — 374 passed
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

- [x] Create skills/contextsmith-orchestrator/ directory
- [x] Create SKILL.md from draft
- [x] Create reference_manifest.yml
- [x] Add shared references
- [x] Run validate_skills.py

### Sub-phase 5b: Create workflow developer SKILL.md

- [x] Create skills/contextsmith-workflow-developer/ directory
- [x] Create SKILL.md
- [x] Create reference_manifest.yml
- [x] Copy domain templates
- [x] Run validate_skills.py

### Sub-phase 5c: Update router skill

- [x] Add contextsmith-orchestrator to routing table
- [x] Add contextsmith-workflow-developer to routing table
- [x] Update wizard Q1 options
- [x] Run validate_skills.py

## Phase 5.5: Targeted Quality Fixes

### Sub-phase 5.5a: Fix ruff line-too-long errors

- [x] Fix E501 in orchestrator/orchestrator.py:219
- [x] Fix E501 in orchestrator/orchestrator.py:244
- [x] Fix E501 in orchestrator/orchestrator.py:254
- [x] Fix E501 in orchestrator/orchestrator.py:267
- [x] Run ruff format --check

### Sub-phase 5.5b: Replace HARD STOP with .phase_gate

- [x] Document .phase_gate convention in NEXT_PROMPT.md template
- [x] Update orchestrator SKILL.md artifact templates
- [x] Remove any existing .phase_gate files

### Sub-phase 5.5c: Remove deep_determinism refs

- [x] Remove deep_determinism paths from orchestrator SKILL.md Reference Loading
- [x] Replace with inline format descriptions or shared refs

### Sub-phase 5.5d: Create shared/harness-generic.md

- [x] Create shared/harness-generic.md
- [x] Copy to orchestrator references/
- [x] Update orchestrator reference_manifest.yml

### Sub-phase 5.5e: Update versioning scheme (policy only)

- [x] Update PACKAGE_SPEC.md with project-level versioning decision
- [x] Update AGENTS.md with versioning convention
- [x] Do NOT bump versions yet — happens at end of Phase 6e

### Sub-phase 5.5f: Add meta-config detail to Phase 6

- [x] Expand Phase 6d in PLAN.md with concrete meta-config phase definitions

### Sub-phase 5.5g: Update Ralph rationale

- [x] Add note to PLAN.md Ralph section: no-op is valid evidence (already present)

## Phase 6: Collapse into Orchestrator-Only Execution

### Sub-phase 6a: Juice contextsmith-run (read-only)

- [x] Catalog contextsmith-run sections and patterns
- [x] Read 8 local-only references
- [x] Read reference_manifest.yml
- [x] Identify shared ref gap

### Sub-phase 6b: Enhance orchestrator SKILL.md

- [x] Add Supported Inputs, Control Parameters, Domain Routing
- [x] Add Interaction Modes, Execution Contract, Preflight Gate
- [x] Add Reference Selection, Execution Workflow, Task-State
- [x] Add Validation Gate, Self-Audit Gate, Evidence Ledger
- [x] Add Completion Criteria, Failure Handling, Required Output, Manifest

### Sub-phase 6c: Move references and update manifest

- [x] Copy 8 local refs from run to orchestrator
- [x] Update orchestrator reference_manifest.yml
- [x] Add missing shared refs to manifest

### Sub-phase 6d: Convert workflow-developer to meta-config

- [x] Create workflow_config.yaml with 6 phases
- [x] Reduce SKILL.md to thin delegator
- [x] Validate config against schema

### Sub-phase 6e: Delete contextsmith-run

- [x] Delete skills/contextsmith-run/
- [x] Remove from router routing table
- [x] Merge wizard Q1 execute options
- [x] Remove from cross-skill chains
- [x] Full repo grep for dangling refs (skills/, shared/, docs/, AGENTS.md, PACKAGE_SPEC.md)
- [x] Apply version 2.0.0 stamp to all surviving skills

### Sub-phase 6f: Create orchestrator __main__.py

- [x] Create __main__.py
- [x] Test python -m orchestrator --help

### Sub-phase 6g: Implement append validation

- [x] Add validate_append_only() to validators.py
- [x] Snapshot append-only files before agent dispatch
- [x] Verify append after agent returns, repair on overwrite
- [x] Add test cases for append validation (function implemented)

### Sub-phase 6h: Wire validation_mode into orchestrator

- [x] Read validation_mode from StepContract in validation branch
- [x] Implement strict/relaxed/none behavior
- [x] Add validation_mode to config schema

### Sub-phase 6i: Wire checkpoint_before_run write

- [x] Write pre-dispatch checkpoint with marker before agent execute
- [x] Post-execution checkpoint clears marker
- [x] Add startup warning for stale pre-dispatch checkpoint

### Sub-phase 6j: Add exit codes 3, 4, 5

- [x] Add EXIT_CONFIG_ERROR, EXIT_STATE_INCONSISTENCY, EXIT_INTERNAL_ERROR to constants.py
- [x] Wire config error → exit 3
- [x] Wire state inconsistency → exit 4
- [x] Wire internal errors → exit 5
- [x] Update tests for new exit codes

### Sub-phase 6k: Add pre-dispatch counter check

- [x] Add retry counter check before adapter.execute()
- [x] Skip dispatch and go to blocked if max_retries exceeded

### Sub-phase 6l: Add timeout_s to workflow config schema

- [x] timeout_s already in schema (pre-existing)
- [x] Wire timeout_s into compile_step_contract() — already wired (pre-existing)

### Sub-phase 6m: Wire model_pin from config to StepContract

- [x] Add optional model_pin to schema state definitions
- [x] Wire model_pin into compile_step_contract() — already wired (pre-existing)

### Sub-phase 6n: Wire ralph_max_cycles from config to StepContract

- [x] ralph_max_cycles already in schema (pre-existing)
- [x] Wire into compile_step_contract() — already wired (pre-existing)

### Sub-phase 6p: Implement RESULT.json fallback protocol

- [x] Implement artifact-presence fallback when RESULT.json missing
- [x] Add warning log when fallback triggered
- [x] Document fallback in orchestrator SKILL.md (Artifact Validation section)

### Sub-phase 6q: Document "agent output is evidence" rule

- [x] Add docstring to resolve_next_state() asserting orchestrator transition authority
- [x] Audit resolve_next_state() — no next_action usage found ✓
- [x] Add "agent output is evidence" paragraph to orchestrator SKILL.md

## Phase 7: Integration and Testing

### Sub-phase 7a: Extend unit tests for orchestrator

- [x] Check existing tests (test_validators.py, test_adapters.py, test_orchestrator_integration.py)
- [x] Create test_orchestrator_state.py if missing
- [x] Create test_checkpoint.py if missing
- [x] Create test_step_compiler.py if missing
- [x] Extend test_validators.py with append validation tests
- [x] Extend test_adapters.py with missing cases
- [x] Create tests/test_orchestrator_determinism.py — dedicated tests for:
  - [x] Exit code mapping: 0-5 all tested
  - [x] validation_mode=strict blocks; relaxed warns+passes; none skips
  - [x] checkpoint_before_run writes pre-dispatch marker
  - [x] Pre-dispatch counter: max_retries=0 blocks without dispatch
  - [x] RESULT.json fallback: all 4 scenarios
  - [x] Agent transition authority: next_action ignored
- [x] Run pytest (374 passed)

### Sub-phase 7b: Extend integration tests

- [x] Extend test_orchestrator_integration.py with end-to-end tests
- [x] Test resume after crash (pre-dispatch marker detection)
- [x] Test max retries → blocked (pre-dispatch counter check)
- [x] Test --dry-run mode
- [x] Test exit code 3/4/5 propagation through run_workflow
- [x] Test append-only file snapshot + repair on overwrite
- [x] Run pytest (13 integration tests)

### Sub-phase 7c: Update validation script

- [x] Verify new skills detected (8/8 OK)
- [x] Add missing validation rules (current rules are sufficient)
- [x] Document orchestrator SKILL.md: consider extracting artifact templates to ref file (572 line WARN, Phase 8a planned)
- [x] Run full validation (ruff, format, validate_skills, radon, pytest all clean)

## Phase 8: Documentation and Polish

### Sub-phase 8a: Trim orchestrator SKILL.md
- [x] Extract artifact templates to references/artifact-templates.md
- [x] Update SKILL.md reference table
- [x] Verify under 500 lines (468 ✓)

### Sub-phase 8b: Fix schema deprecation
- [x] Update $schema from draft-07 to 2020-12 (both schemas updated)
- [x] Rename definitions to $defs for 2020-12 compliance
- [x] Test all fixtures still validate (valid pass, invalid fail correctly)

### Sub-phase 8c: Update user-facing docs
- [x] Run markdownlint across docs/ fix MD060 table-style issues (15 files fixed)
- [x] 0 remaining MD060 issues

### Sub-phase 8d: CHANGELOG entry
- [x] Write comprehensive entry covering Phase 5.5-8 changes
- [x] Version 1.7.1 → 2.0.0

## Phase 9: Final Validation and Lock

### Sub-phase 9a: Full validation pass
- [ ] Run ruff check, ruff format --check, validate_skills.py, pytest, markdownlint
- [ ] Fix remaining issues

### Sub-phase 9b: Final self-audit
- [ ] Audit all phases 1-9 against A-F rubric
- [ ] Verify every expected_output exists and is non-empty

### Sub-phase 9c: Project closeout
- [ ] Verify git status is clean
- [ ] Check staged_skills/ for stale artifacts
- [ ] Write final DECISIONS.md entry
