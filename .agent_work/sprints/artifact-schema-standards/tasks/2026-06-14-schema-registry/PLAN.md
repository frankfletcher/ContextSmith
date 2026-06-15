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

- Status: completed

#### Sub-phase 11.1: Extra-audit workflow config

- Status: completed
- Context Budget: 8k
- Tasks:
  - [x] Create .contextsmith/audit-with-extra.json workflow config [PRE-EXISTING]
  - [x] Validate config against schema — PASS
  - [x] Test with dry run — PASS

#### Sub-phase 11.2: Lint counter integration

- Status: completed
- Context Budget: 8k
- Tasks:
  - [x] Document lint_error_counter.py usage — AGENTS.md Repository Map + description
  - [x] Verify AGENTS.md validation commands include counter piping — confirmed
  - [x] Add reset/view instructions — reset command added

#### Sub-phase 11.3: Decision records backfill

- Status: completed
- Context Budget: 8k
- Tasks:
  - [x] Add DECISIONS.md entries — D9/D10/D12/D14 all present
  - [x] Update CONTEXT.md Key Files — all present

#### Sub-phase 11.4: Documentation and cleanup

- Status: completed
- Context Budget: 16k
- Tasks:
  - [x] Verify .agent_work/tmp/ exists and is gitignored
  - [x] Run full validation suite — all 5 pass
  - [x] Update CHANGELOG.md — v2.2.0

### Phase 12: Packaging and Distribution

- Status: pending

#### Sub-phase 12.1: Orchestrator packaging

- Status: pending
- Context Budget: 16k
- Validation: |pip install -e . && python -m orchestrator.cli --help|
- Tasks:
  - [ ] Add pyproject.toml `[project.scripts]` entry point: `contextsmith-orchestrator = "orchestrator.cli:main"`
  - [ ] Ensure `pip install -e .` makes `python -m orchestrator` and `contextsmith-orchestrator` available
  - [ ] Verify CLI help output and subcommands work

#### Sub-phase 12.2: Release pipeline fix

- Status: pending
- Context Budget: 16k
- Validation: |bash scripts/test_release.sh|
- Tasks:
  - [ ] Fix test_release.sh: replace `contextsmith-run` with `contextsmith-workflow-developer`
  - [ ] Update build_release.py to include `orchestrator/` in release bundle
  - [ ] Run test_release.sh end-to-end and fix any failures
  - [ ] Run build_release.py --package --individual and verify dist/ output

#### Sub-phase 12.3: Version consolidation

- Status: pending
- Context Budget: 8k
- Validation: |grep -r '"version"' pyproject.toml|, check all skills match
- Tasks:
  - [ ] Set pyproject.toml `version` as canonical source
  - [ ] Update PACKAGE_SPEC.md version to match pyproject.toml
  - [ ] Update all skill metadata.version to match project version
  - [ ] Update CHANGELOG.md header if needed

#### Sub-phase 12.4: Orchestrator-as-runtime commitment

- Status: pending
- Context Budget: 16k
- Validation: |pytest tests/test_orchestrator_integration.py::TestMergeNewArtifactSegments|
- Tasks:
  - [ ] Evaluate D14 gate: condition 1 MET (5 end-to-end tests exist for _merge_new_artifact_segments)
  - [ ] Evaluate D14 gate: condition 2 MET (user commitment — orchestrator is production runtime)
  - [ ] Add D14_GATE_PASSED sentinel to .agent_work/ (checked by agents on session start)
  - [ ] Update AGENTS.md: stop manual .new merging, orchestrator handles it
  - [ ] Update CONTEXT.md: orchestrator gap note → orchestrator IS the runtime
  - [ ] Update DECISIONS.md: mark D12/D14 as resolved, add D15 commitment
  - [ ] Update _merge_new_artifact_segments invocation in orchestrator.run() — already present, verify it fires in production path

#### Sub-phase 12.5: CI/CD setup

- Status: pending
- Context Budget: 8k
- Tasks:
  - [ ] Add `.github/workflows/validate.yml` running full suite on push/PR
  - [ ] Commands: validate_skills, ruff check, ruff format --check, pytest, markdownlint (scoped)
  - [ ] Verify workflow syntax with `act` or manual review

#### Sub-phase 12.6: Orchestrator complexity refactor

- Status: pending
- Context Budget: 16k
- Validation: |uvx radon cc orchestrator/ -s -a | grep -E " - [CDEF] "| (must find none)
- Tasks:
  - [ ] Extract sub-phase dispatch from `orchestrator.run()` (lines ~940-960)
  - [ ] Extract checkpoint persistence from `orchestrator.run()` (lines ~713-745)
  - [ ] Verify cyclomatic complexity drops to ≤ B
  - [ ] Run full test suite — all pass
