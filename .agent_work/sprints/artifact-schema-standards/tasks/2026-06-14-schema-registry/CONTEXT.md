# CONTEXT.md

## Project

ContextSmith orchestrator - artifact schema standards

## Task Directory

.agent_work/sprints/artifact-schema-standards/tasks/2026-06-14-schema-registry

## Key Files

- orchestrator/validators.py: Artifact validation functions
- orchestrator/step_compiler.py: StepContract compilation
- orchestrator/orchestrator.py: Main orchestrator loop
- orchestrator/state_reader.py: Markdown artifact parsing
- schemas/workflow_config.schema.json: Workflow config schema
- schemas/artifact_schemas.yaml: Artifact schema registry
- tests/test_validators.py: Validator tests
- tests/test_orchestrator_state.py: State reader tests
- scripts/lint_error_counter.py: Persistent lint error frequency counter
- shared/extra-audit.md: Strategic-lens review template
- shared/project-audit.md: Full project audit prompt
- shared/coding-standards.md: Markdown and Python coding standards
- .contextsmith/audit-with-extra.json: Workflow config chaining audit + extra_audit

## Known Constraints

- Must preserve append-only semantics for PHASE_LOG.md, EDUCATIONAL_REPORT.md, AUDIT_REPORT.md, DECISIONS.md
- Must not break existing workflows
- Must pass all validation commands
- **Orchestrator is the production runtime** (D15). `.new` file auto-merging is handled by `_merge_new_artifact_segments()` in orchestrator.run(). Agents must NOT merge `.new` files manually. Check for `D14_GATE_PASSED` sentinel in `.agent_work/` to confirm.
- Orchestrator CLI installed via `pip install -e .` or `pip install contextsmith`. Must be available before runtime-dependent workflows can run outside the repo.

## Technical Debt

- `orchestrator.orchestrator.run()` has cyclomatic complexity C (15) — scheduled for refactor in Phase 12.6. Extract sub-phase dispatch and checkpoint handling to reduce to ≤ B.

## Evidence Notes

- Current validation is shallow: existence + non-empty + section presence
- `section_requirements` is config-driven, not a fixed contract
- PHASE_LOG.md has 3 different formats in the wild
- JSON artifacts (runtime enforcement) have full schemas; markdown artifacts do not
- Sub-phases now have Context Budget, Dependency, and Validation metadata

## Skip Rules

- Do not modify `.gitignore` without approval
- Do not change existing workflow configs
- Do not remove existing validation functions (deprecate instead)

## Harness

opencode
