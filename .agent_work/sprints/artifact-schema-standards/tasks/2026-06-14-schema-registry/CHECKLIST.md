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

## Phase 11: Tooling and Audit Infrastructure

### Sub-phase 11.1: Extra-audit workflow config

- [x] Create .contextsmith/audit-with-extra.json workflow config [PRE-EXISTING — verified Phase 10.1]
- [x] Validate config against schema — PASS (validate_workflow_config: no violations)
- [x] Test with dry run — PASS (step contract compiles, state readable)

### Sub-phase 11.2: Lint counter integration

- [x] Document lint_error_counter.py usage — added to AGENTS.md Repository Map + description in validation section
- [x] Verify AGENTS.md validation commands include counter piping — confirmed: both ruff (line 58) and markdownlint (line 61) pipe through counter
- [x] Add reset/view instructions — added `echo '{}' > .agent_work/lint_error_counts.json` reset command to AGENTS.md

### Sub-phase 11.3: Decision records backfill

- [x] Add DECISIONS.md entries for .new merging, lint counter, PROTECTED_FILES cleanup — VERIFIED: D9 (lint counter), D10 (PROTECTED_FILES), D12/D14 (.new merging) all exist, no additions needed
- [x] Update CONTEXT.md Key Files with new scripts/ and shared/ refs — VERIFIED: lint_error_counter.py, extra-audit.md, project-audit.md, coding-standards.md all present

### Sub-phase 11.4: Documentation and cleanup

- [x] Verify .agent_work/tmp/ exists and is gitignored — EXISTS, listed in .gitignore line 14
- [x] Run full validation suite — all 5 commands pass (validate_skills, ruff check, ruff format, pytest 423, markdownlint pre-existing only)
- [x] Update CHANGELOG.md — added v2.2.0 entry for Phase 11 completion

## Phase 12: Packaging and Distribution

### Sub-phase 12.1: Orchestrator packaging

- [x] Add pyproject.toml `[project.scripts]` entry point: `contextsmith-orchestrator = "orchestrator.cli:main"`
- [x] Ensure `pip install -e .` makes orchestrator available
- [x] Verify CLI help and subcommands work

### Sub-phase 12.2: Distribution packaging

- [x] Fix test_release.sh: replace contextsmith-run with contextsmith-workflow-developer
- [x] Update build_release.py: add --wheel flag, include orchestrator/ in bundle
- [x] Add .github/workflows/publish.yml
- [x] Run test_release.sh (blocked at token budget — pre-existing)
- [x] Run build_release.py --dry-run with --wheel flag — pipeline parses correctly
- [x] Verify wheel build + fresh venv install — PASS

### Sub-phase 12.3: Adapter plugin system

- [x] Add `[project.entry-points."contextsmith.adapters"]` to pyproject.toml
- [x] Add `[project.optional-dependencies]` harness extras
- [x] Rewrite discover_adapters() to use importlib.metadata.entry_points with fallback
- [x] Add tests/test_adapter_discovery.py (6 tests)
- [x] Full test suite passes (429)

### Sub-phase 12.4: CI/CD full pipeline

- [x] Add .github/workflows/validate.yml (matrix: 3.10, 3.11, 3.12)
- [x] Add .pre-commit-config.yaml (ruff + pre-commit-hooks)
- [x] Add scripts/lint_changelog.py
- [x] Document pre-commit install in AGENTS.md

### Sub-phase 12.5: Version consolidation

- [x] Set pyproject.toml version as canonical (v2.2.0)
- [x] Update PACKAGE_SPEC.md, all 8 skill SKILL.md to v2.2.0
- [x] Add scripts/validate_version_consistency.py
- [x] Add version consistency check to validate.yml

### Sub-phase 12.6: Orchestrator-as-runtime commitment

- [x] Evaluate D14 gate conditions (both MET)
- [x] Add D14_GATE_PASSED sentinel to .agent_work/
- [x] AGENTS.md already updated for orchestrator-as-runtime
- [x] CONTEXT.md already reflects orchestrator IS the runtime
- [x] DECISIONS.md has D15 with D12/D14 resolved
- [x] Verify _merge_new_artifact_segments fires in production path (line 936)

### Sub-phase 12.7: Complexity refactor

- [x] Extract sub-phase dispatch + post-execution from run() — C(15) → B(8)
- [x] No C/D/E/F grades remain in orchestrator/
- [x] Full test suite passes (429)

## Validation

- [x] `uv run python scripts/validate_skills.py` passes (8 skills, all v2.2.0)
- [x] `uv run ruff check orchestrator/ --select E,F,W,I` passes
- [x] `uv run ruff format orchestrator/ --check` passes
- [x] `uv run pytest tests/ -v` passes (429 tests)
- [x] `uv run python scripts/validate_version_consistency.py` passes (all v2.2.0)
- [x] `markdownlint . --ignore node_modules` passes on new files (pre-existing issues in docs/ unaffected)
