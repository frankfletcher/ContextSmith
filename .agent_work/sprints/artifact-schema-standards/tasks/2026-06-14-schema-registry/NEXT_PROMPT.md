# NEXT_PROMPT.md

You are continuing work on the ContextSmith artifact schema standards task.

## Current Status
- Phase: 7 of 10
- Sub-phase: 7.1
- State: execute

## Sub-phase
Sub-phase 7.1: artifact_schemas extension

## Sub-phase Tasks
  - [ ] Add artifact_schemas section to workflow_config.schema.json
  - [ ] Define extension mechanism for workflow-specific overrides
  - [ ] Validate JSON schema syntax

## Your Task
Update `schemas/workflow_config.schema.json` to support an `artifact_schemas` section
that allows workflows to declare custom section overrides on top of the base schemas.

## Input Files
- STATUS.md: Current workflow state
- PLAN.md: Phase plan with all 10 phases
- CONTEXT.md: Project context
- schemas/artifact_schemas.yaml: Artifact schema registry
- schemas/workflow_config.schema.json: Workflow config schema

## Output Requirements
- Update schemas/workflow_config.schema.json with artifact_schemas support
- Update STATUS.md with results
- Update CHECKLIST.md
- Update PHASE_LOG.md

## Constraints
- Must preserve backward compatibility with existing workflow configs
- Must pass JSON schema validation
- Must run `markdownlint . --ignore node_modules` on any changed Markdown files

## Ralph Loop Enforcement
3 iterations required. Each is critique+fix. Do not skip or collapse.
1. **Critique** — Review against contract, find material defects, fix them
2. **Re-check** — After fixes, if no new defects → no-op; else fix
3. **Final check** — If no defects → no-op; do not invent changes
Each iteration needs a compact log entry in Ralph Summary.
Ralph loops are critique/revision, not repeated tool calls.

## Self-Audit
Before closeout, verify:
- Original phase goal satisfied or blocker recorded
- All validation commands executed or blocker documented
- Side-effect boundaries respected
- Task state updated with compact facts

## Hard Stop
Current phase is Phase 7: Workflow Config Schema Update.
Do not proceed beyond it. Do not edit files outside this phase scope.

## Expected Output Format

```
## Result
[summary of changes]

## Evidence
[list of files modified]

## Validation
[validation checks performed and results]

## Risks / Next Action
[any risks or blockers, next sub-phase]
```
