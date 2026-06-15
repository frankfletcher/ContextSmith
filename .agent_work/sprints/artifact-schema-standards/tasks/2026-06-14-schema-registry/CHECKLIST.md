# CHECKLIST.md

## Schema Registry

- [x] YAML schema registry created at `schemas/artifact_schemas.yaml`
- [x] All 11 markdown artifact types have defined schemas
- [x] Required sections are specified for each artifact type
- [x] Optional sections are specified where applicable
- [x] Schema structure is extensible for future content rules
- [x] PLAN.md uses phase_tree content rule with 3-level hierarchy
- [x] STATUS.md includes Current Sub-phase optional section

## Phase Tree Parsing and Validation

- [x] `state_reader._parse_phase_tree()` handles ### phases, #### sub-phases, checkbox tasks
- [x] Flat checkbox format still supported (backward compat)
- [x] `read_status()` returns current_subphase
- [x] `validators.validate_phase_tree_structure()` validates hierarchy
- [x] `validators.validate_plan_phase_order()` cross-references plan with config

## StepContract and Step Compiler

- [x] `StepContract` has subphase_name and subphase_context_budget fields
- [x] `_extract_subphase_budget()` parses Context Budget from metadata
- [x] `compile_step_contract()` passes subphase data to StepContract

## Orchestrator Sub-phase Integration

- [x] `_rewrite_status_content()` supports Current Sub-phase
- [x] `_update_status()` accepts current_subphase parameter
- [x] `_generate_next_prompt()` includes sub-phase name and task list
- [x] `_try_advance_subphase()` advances through pending sub-phases
- [x] `_find_first_subphase()` auto-selects initial sub-phase on phase transition
- [x] `run()` inserts sub-phase advancement after successful execution
- [x] 403 tests pass, ruff lint and format clean

## Workflow Config Schema

- [x] Add artifact_schemas extension to workflow_config.schema.json
- [x] Define extension mechanism for workflow-specific overrides

## Integration Tests

- [x] Integration test for sub-phase advancement
- [x] Integration test for sub-phase budget extraction in dispatch (covered by unit tests in test_step_compiler.py::TestExtractSubphaseBudget)

## Documentation

- [x] `docs/reference/ARTIFACT_SCHEMAS.md` created
- [x] `CHANGELOG.md` updated
- [x] `markdownlint` passes on all docs (pre-existing issues in docs/ unaffected)

## Phase 10: Final Audit and Validation

- [x] Sub-phase 10.1: Run implementation plan audit — no must-fix items found
- [x] Sub-phase 10.2: Run full validation suite — all 5 commands pass

## Validation

- [x] `uv run python scripts/validate_skills.py` passes
- [x] `uv run ruff check orchestrator/ --select E,F,W,I` passes
- [x] `uv run ruff format orchestrator/ --check` passes
- [x] `uv run pytest tests/ -v` passes (423 tests)
- [x] `markdownlint . --ignore node_modules` passes on new files (pre-existing issues in docs/ unaffected)
