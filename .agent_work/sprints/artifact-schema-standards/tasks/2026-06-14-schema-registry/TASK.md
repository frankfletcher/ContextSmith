# TASK.md

## Objective

Create artifact schema standards for the ContextSmith orchestrator's markdown artifacts (STATUS.md, PLAN.md, CONTEXT.md, PHASE_LOG.md, EDUCATIONAL_REPORT.md, AUDIT_REPORT.md, DECISIONS.md, ARTIFACTS.md, CHECKLIST.md, TASK.md, NEXT_PROMPT.md).

## Scope

1. Define a declarative artifact schema registry (YAML) that specifies required/optional sections, ordering constraints, and content rules per artifact type
2. Refactor `orchestrator/validators.py` to load and enforce schemas from the registry
3. Add structural validation for all markdown artifacts beyond existence checks
4. Update `orchestrator/step_compiler.py` to pass artifact schemas through StepContract
5. Update `workflow_config.schema.json` to support schema extensions
6. Add comprehensive test coverage for schema validation
7. Document the schema registry in `docs/reference/ARTIFACT_SCHEMAS.md`

## Constraints

- Must not break existing workflows that use `section_requirements` in config
- Must preserve append-only semantics for PHASE_LOG.md, EDUCATIONAL_REPORT.md, AUDIT_REPORT.md, DECISIONS.md
- Must allow LLMs to add additional structure beyond required sections
- Must pass `ruff check --select E,F,W,I` and `ruff format --check`
- Must pass `uv run pytest tests/ -v`
- Must pass `uv run python scripts/validate_skills.py`
- Must pass `markdownlint . --ignore node_modules`
- Target context window: 120k (large tier)
- Ralph iterations: 3
- Audit and Ralph on every sub-phase

## Success Criteria

- All markdown artifacts have defined schemas with required sections
- Validators enforce schemas at runtime
- Existing tests pass
- New tests cover schema validation edge cases
- Documentation explains the schema registry and how to extend it
- Implementation plan audit passes all categories with grade A or B
