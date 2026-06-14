# NEXT_PROMPT.md

You are continuing work on the ContextSmith artifact schema standards task.

## Current Status
- Phase: 8 of 10
- Sub-phase: 8.1
- State: execute

## Sub-phase
Sub-phase 8.1: Sub-phase advancement test

## Sub-phase Tasks
- [ ] Add test for _try_advance_subphase with pending sub-phases
- [ ] Add test for _try_advance_subphase returns None on all done
- [ ] Add test for backward compat with flat plan

## Your Task
Add integration tests to verify the orchestrator's sub-phase advancement logic (`_try_advance_subphase`). Cover the three scenarios: advancing through pending sub-phases, returning None when all sub-phases are done, and backward compatibility with the flat plan format.

## Input Files
- STATUS.md: Current workflow state
- PLAN.md: Phase plan with all 10 phases
- CONTEXT.md: Project context
- CHECKLIST.md: Task tracking
- orchestrator/orchestrator.py: Main orchestrator with _try_advance_subphase
- tests/test_orchestrator_determinism.py: Existing orchestrator tests
- tests/fixtures/: Test fixture directory
- schemas/workflow_config.schema.json: Workflow config schema (now has artifact_schemas)

## Output Requirements
- Add tests to tests/test_orchestrator_determinism.py or a new test file
- All sub-phase advancement paths must be covered
- Tests must use existing test fixture patterns
- Update CHECKLIST.md
- Create or append to EDUCATIONAL_REPORT.md, AUDIT_REPORT.md, PHASE_LOG.md

## Constraints
- Context Budget: 32k
- Must not modify orchestrator/orchestrator.py logic (test only)
- Must follow existing test patterns (pytest, fixtures)
- Must pass full validation suite on completion

### REPORT FILES: USE `.new` SEGMENTS — ORCHESTRATOR HANDLES MERGING

Do NOT write directly to these files. Write a `.new` segment file instead with only the new entry content:

- `EDUCATIONAL_REPORT.md.new` — new sub-phase explanation entry
- `AUDIT_REPORT.md.new` — new audit rubric entry
- `PHASE_LOG.md.new` — new phase log entry
- `DECISIONS.md.new` — new decision entry

The orchestrator automatically merges `.new` files into the parent reports after execution. This removes the append operation from the agent entirely — no risk of overwrite history, no file-existence guessing.

## Ralph Loop Enforcement
3 iterations required. Each is critique+fix. Do not skip or collapse.
1. **Critique** — Review tests against contract, find material defects
2. **Re-check** — After fixes, if no new defects → no-op; else fix
3. **Final check** — If no defects → no-op; do not invent changes

## Self-Audit
Before closeout, verify:
- Original phase goal satisfied or blocker recorded
- All validation commands executed or blocker documented
- Side-effect boundaries respected
- Task state updated with compact facts

## Hard Stop
Current phase is Phase 8: Integration Tests.
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
