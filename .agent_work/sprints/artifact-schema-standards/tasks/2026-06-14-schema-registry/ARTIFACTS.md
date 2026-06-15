# ARTIFACTS.md

## Files to Create

- `schemas/artifact_schemas.yaml` - artifact schema registry (PLAN.md with phase_tree, STATUS.md with Current Sub-phase)

## Files to Modify

- `orchestrator/state_reader.py` - added `_parse_phase_tree()`, `_parse_flat_phases()`, `_calc_completion()`; updated `read_plan()` and `read_status()`
- `orchestrator/validators.py` - added `validate_phase_tree_structure()`, `validate_plan_phase_order()`
- `orchestrator/step_compiler.py` - added `_extract_subphase_budget()`, `_name_matches()`; updated `compile_step_contract()` to accept current_subphase
- `orchestrator/adapters/base.py` - added subphase_name, subphase_context_budget to StepContract
- `orchestrator/orchestrator.py` - added `_try_advance_subphase()`, `_find_phase_in_plan()`, `_find_first_subphase()`, `_find_subphase_tasks()`; updated `_rewrite_status_content()`, `_update_status()`, `_persist_transition()`, `_generate_next_prompt()`, `_prepare_step_contract()`, `_complete_step_flow()`, `run()`
- `tests/test_orchestrator_state.py` - added TestParsePhaseTree
- `tests/test_validators.py` - added TestValidatePhaseTreeStructure, TestValidatePlanPhaseOrder
- `tests/test_step_compiler.py` - added TestExtractSubphaseBudget

## Files Pending (Phase 12)

- `.github/workflows/validate.yml` - CI/CD pipeline
- `pyproject.toml` - update with CLI entry point, version consolidation
- `scripts/test_release.sh` - fix contextsmith-run reference
- `scripts/build_release.py` - include orchestrator/ in bundle

## Files to Modify (Phase 12)

- `pyproject.toml` - add `[project.scripts]` entry point for orchestrator CLI
- `PACKAGE_SPEC.md` - consolidate version
- `skills/*/SKILL.md` - consolidate metadata.version
- `orchestrator/orchestrator.py` - refactor run() complexity (extract dispatch, checkpoint)

## Files Completed (all prior phases)

- All 11 phases (1-11) deliverables complete. See prior ARTIFACTS.md entries.
- `.contextsmith/audit-with-extra.json` - validated, dry-run passes
- `AGENTS.md` - lint counter integrated
- `CHANGELOG.md` - v2.2.0
- `DECISIONS.md` - D15 orchestrator commitment added
- `CONTEXT.md` - orchestrator gap note resolved

## Commands to Run

- `uv run python scripts/validate_skills.py`
- `uv run ruff check orchestrator/ --select E,F,W,I`
- `uv run ruff format orchestrator/ --check`
- `uv run pytest tests/ -v`
- `markdownlint . --ignore node_modules`
- `uvx radon cc orchestrator/ -s -a | grep -E " - [CDEF] "` (Phase 12.6 gate)
- `bash scripts/test_release.sh` (Phase 12.2 gate)
