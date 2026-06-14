# ARTIFACTS.md

## Files to Create
- `schemas/artifact_schemas.yaml` - artifact schema registry (PLAN.md with phase_tree, STATUS.md with Current Sub-phase)

## Files to Modify
- `orchestrator/state_reader.py` - added _parse_phase_tree(), _parse_flat_phases(), _calc_completion(); updated read_plan() and read_status()
- `orchestrator/validators.py` - added validate_phase_tree_structure(), validate_plan_phase_order()
- `orchestrator/step_compiler.py` - added _extract_subphase_budget(), _name_matches(); updated compile_step_contract() to accept current_subphase
- `orchestrator/adapters/base.py` - added subphase_name, subphase_context_budget to StepContract
- `orchestrator/orchestrator.py` - added _try_advance_subphase(), _find_phase_in_plan(), _find_first_subphase(), _find_subphase_tasks(); updated _rewrite_status_content(), _update_status(), _persist_transition(), _generate_next_prompt(), _prepare_step_contract(), _complete_step_flow(), run()
- `tests/test_orchestrator_state.py` - added TestParsePhaseTree
- `tests/test_validators.py` - added TestValidatePhaseTreeStructure, TestValidatePlanPhaseOrder
- `tests/test_step_compiler.py` - added TestExtractSubphaseBudget

## Files Pending
- `docs/reference/ARTIFACT_SCHEMAS.md` - documentation

## Files Completed
- `schemas/workflow_config.schema.json` - added artifact_schemas extension with ArtifactSchemaOverride

## Commands to Run
- `uv run python scripts/validate_skills.py`
- `uv run ruff check orchestrator/ --select E,F,W,I`
- `uv run ruff format orchestrator/ --check`
- `uv run pytest tests/ -v`
- `markdownlint . --ignore node_modules`
