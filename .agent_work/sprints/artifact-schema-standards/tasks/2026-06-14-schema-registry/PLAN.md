# PLAN.md

## Phases

### Phase 1: Schema Registry Design

- Status: completed

#### Sub-phase 1.1: YAML structure

- Status: completed
- Context Budget: 16k
- Validation: yaml_valid
- Tasks:
  - [x] Define YAML structure for artifact schemas
  - [x] Add metadata, descriptions, and examples

#### Sub-phase 1.2: All artifact schemas

- Status: completed
- Context Budget: 32k
- Tasks:
  - [x] Draft schemas for STATUS.md, PLAN.md, CONTEXT.md
  - [x] Draft schemas for PHASE_LOG.md, EDUCATIONAL_REPORT.md, AUDIT_REPORT.md
  - [x] Draft schemas for DECISIONS.md, ARTIFACTS.md, CHECKLIST.md
  - [x] Draft schemas for TASK.md, NEXT_PROMPT.md

### Phase 2: Validator Refactor

- Status: completed

#### Sub-phase 2.1: Schema loading

- Status: completed
- Context Budget: 24k
- Validation: |pytest tests/test_validators.py::TestLoadArtifactSchemas|
- Tasks:
  - [x] Add load_artifact_schemas()
  - [x] Add validate_artifact_schema()
  - [x] Add validate_artifacts_with_schemas()

#### Sub-phase 2.2: Phase tree validation

- Status: completed
- Context Budget: 24k
- Validation: |pytest tests/test_validators.py::TestValidatePhaseTreeStructure|
- Tasks:
  - [x] Add validate_phase_tree_structure()
  - [x] Add validate_plan_phase_order()

### Phase 3: State Reader Refactor

- Status: completed

#### Sub-phase 3.1: Hierarchical parsing

- Status: completed
- Context Budget: 24k
- Validation: |pytest tests/test_orchestrator_state.py::TestParsePhaseTree|
- Tasks:
  - [x] Add _parse_phase_tree() with 3-level hierarchy
  - [x] Preserve flat checkbox backward compatibility
  - [x] Add current_subphase to read_status()

### Phase 4: Step Compiler and StepContract

- Status: completed

#### Sub-phase 4.1: StepContract fields

- Status: completed
- Context Budget: 16k
- Tasks:
  - [x] Add subphase_name and subphase_context_budget to StepContract

#### Sub-phase 4.2: Sub-phase budget extraction

- Status: completed
- Context Budget: 16k
- Validation: |pytest tests/test_step_compiler.py::TestExtractSubphaseBudget|
- Tasks:
  - [x] Add _extract_subphase_budget() helper
  - [x] Pass current_subphase to compile_step_contract()

### Phase 5: Orchestrator Sub-phase Advancement

- Status: completed

#### Sub-phase 5.1: Status and prompt updates

- Status: completed
- Context Budget: 24k
- Tasks:
  - [x] Update _rewrite_status_content for Current Sub-phase
  - [x] Update _update_status for sub-phase parameter
  - [x] Update _generate_next_prompt with sub-phase task list

#### Sub-phase 5.2: Sub-phase dispatch loop

- Status: completed
- Context Budget: 24k
- Tasks:
  - [x] Add _try_advance_subphase()
  - [x] Add _find_phase_in_plan() and _find_first_subphase()
  - [x] Insert sub-phase advancement in run() after execution

### Phase 6: Unit Test Coverage

- Status: completed

#### Sub-phase 6.1: State reader tests

- Status: completed
- Context Budget: 16k
- Validation: |pytest tests/test_orchestrator_state.py::TestParsePhaseTree|
- Tasks:
  - [x] Test hierarchical parsing
  - [x] Test flat format backward compat
  - [x] Test context budget extraction

#### Sub-phase 6.2: Validator tests

- Status: completed
- Context Budget: 16k
- Validation: |pytest tests/test_validators.py::TestValidatePhaseTreeStructure tests/test_validators.py::TestValidatePlanPhaseOrder|
- Tasks:
  - [x] Test phase tree structure validation
  - [x] Test plan/config phase order cross-reference
  - [x] Test invalid status detection

#### Sub-phase 6.3: Step compiler tests

- Status: completed
- Context Budget: 16k
- Validation: |pytest tests/test_step_compiler.py::TestExtractSubphaseBudget|
- Tasks:
  - [x] Test budget extraction from metadata
  - [x] Test missing budget handling
  - [x] Test sub-phase not found

### Phase 7: Workflow Config Schema Update

- Status: completed

#### Sub-phase 7.1: artifact_schemas extension

- Status: completed
- Context Budget: 16k
- Tasks:
  - [x] Add artifact_schemas section to workflow_config.schema.json
  - [x] Define extension mechanism for workflow-specific overrides
  - [x] Validate JSON schema syntax

### Phase 8: Integration Tests

- Status: completed

#### Sub-phase 8.1: Sub-phase advancement test

- Status: completed
- Context Budget: 32k
- Tasks:
  - [x] Add test for _try_advance_subphase with pending sub-phases
  - [x] Add test for _try_advance_subphase returns None on all done
  - [x] Add test for backward compat with flat plan

### Phase 9: Documentation

- Status: completed

#### Sub-phase 9.1: Schema registry docs

- Status: completed
- Context Budget: 24k
- Tasks:
  - [x] Write docs/reference/ARTIFACT_SCHEMAS.md
  - [x] Document PLAN.md hierarchical format
  - [x] Add examples of sub-phase structure

#### Sub-phase 9.2: Changelog

- Status: completed
- Context Budget: 8k
- Tasks:
  - [x] Update CHANGELOG.md
  - [x] Run markdownlint on all docs

### Phase 10: Final Audit and Validation

- Status: completed

#### Sub-phase 10.1: Implementation plan audit

- Status: completed
- Context Budget: 16k
- Tasks:
  - [x] Run implementation plan audit
  - [x] Fix any must-fix items

#### Sub-phase 10.2: Full validation

- Status: completed
- Context Budget: 16k
- Tasks:
  - [x] uv run python scripts/validate_skills.py
  - [x] uv run ruff check orchestrator/ --select E,F,W,I | uv run python scripts/lint_error_counter.py
  - [x] uv run ruff format orchestrator/ --check
  - [x] uv run pytest tests/ -v
  - [x] markdownlint . --ignore node_modules | uv run python scripts/lint_error_counter.py

### Phase 11: Tooling and Audit Infrastructure

- Status: pending

#### Sub-phase 11.1: Extra-audit workflow config

- Status: pending
- Context Budget: 8k
- Tasks:
  - [ ] Create .contextsmith/audit-with-extra.json workflow config
  - [ ] Validate config against schema
  - [ ] Test with dry run

#### Sub-phase 11.2: Lint counter integration

- Status: pending
- Context Budget: 8k
- Tasks:
  - [ ] Document lint_error_counter.py usage
  - [ ] Verify AGENTS.md validation commands include counter piping
  - [ ] Add reset/view instructions

#### Sub-phase 11.3: Decision records backfill

- Status: pending
- Context Budget: 8k
- Tasks:
  - [ ] Add DECISIONS.md entries for .new merging, lint counter, PROTECTED_FILES cleanup
  - [ ] Update CONTEXT.md Key Files with new scripts/ and shared/ refs

#### Sub-phase 11.4: Documentation and cleanup

- Status: pending
- Context Budget: 16k
- Tasks:
  - [ ] Verify .agent_work/tmp/ exists and is gitignored
  - [ ] Run full validation suite
  - [ ] Update CHANGELOG.md
