# CONTEXT.md

## Project
ContextSmith orchestrator - artifact schema standards

## File Map
- `orchestrator/validators.py` - artifact validation functions
- `orchestrator/step_compiler.py` - StepContract compilation
- `orchestrator/orchestrator.py` - main orchestrator loop
- `orchestrator/state_reader.py` - markdown artifact parsing
- `schemas/workflow_config.schema.json` - workflow config schema
- `tests/test_validators.py` - validator tests
- `tests/test_orchestrator_state.py` - state reader tests
- `docs/reference/` - reference documentation

## Constraints
- Must preserve append-only semantics for PHASE_LOG.md, EDUCATIONAL_REPORT.md, AUDIT_REPORT.md, DECISIONS.md
- Must not break existing workflows
- Must pass all validation commands

## Evidence Notes
- Current validation is shallow: existence + non-empty + section presence
- `section_requirements` is config-driven, not a fixed contract
- PHASE_LOG.md has 3 different formats in the wild
- JSON artifacts (runtime enforcement) have full schemas; markdown artifacts do not

## Skip Rules
- Do not modify `.gitignore` without approval
- Do not change existing workflow configs
- Do not remove existing validation functions (deprecate instead)
