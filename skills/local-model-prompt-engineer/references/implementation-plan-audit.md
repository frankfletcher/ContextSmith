# Implementation Plan Audit

Use this reference when creating, reviewing, or refining phased implementation plans for coding, migration, data-science, ML, documentation, or long-running agent work.

## Purpose

A plan can pass basic validation and still be too broad for a smaller model to execute. Audit the plan for **small-model executability**, not only completeness.

## A-F Rubric

Grade each category A-F.

- **Phase granularity**: Are phases small enough for the target model and `targeted_context_length`?
- **Atomicity**: Can each step be executed without hidden inference leaps?
- **Dependency ordering**: Are prerequisites completed before dependent work begins?
- **Context fit**: Can one phase fit in the stated context budget with tool results and output reserved?
- **Validation strength**: Does each phase define concrete pass/fail checks?
- **Task-state integration**: Does the plan update TASK, PLAN, STATUS, DECISIONS, CONTEXT, CHECKLIST, ARTIFACTS, PHASE_LOG, and NEXT_PROMPT when needed?
- **Handoff quality**: Does each phase end with a debrief and clear next prompt?
- **Rollback/recovery**: Does the plan preserve user work and define recovery steps for failures?
- **Test strategy**: Does the plan specify baseline, edge, regression, and integration tests when relevant?
- **Small-model carryout readiness**: Could a smaller local model execute the phase from task-state files without rereading the entire repo or prior chat?

## Audit Questions

1. Is the plan too coarse for the model/context budget?
2. Does each phase have a single primary objective?
3. Does each phase name likely files, inputs, outputs, and stop conditions?
4. Does each phase include narrow validation before broader validation?
5. Does the plan include phase compression/debrief?
6. Does the plan state what not to carry forward?
7. Does the plan avoid bundling unrelated subsystems into one phase?
8. Does the plan include code review/test-quality gates for coding work?
9. Does the plan identify user-approval points for risky actions?
10. Does the plan state what can be done in a fresh session?

## Output Format

```markdown
## Implementation Plan Audit

Overall recommendation: ship | refine before execution | split phases | needs user input

| Category | Grade | Notes |
|---|---:|---|
| Phase granularity |  |  |
| Atomicity |  |  |
| Context fit |  |  |
| Validation strength |  |  |
| Task-state integration |  |  |
| Handoff quality |  |  |
| Test strategy |  |  |

## Must Fix Before Execution
- ...

## Suggested Improvements
- ...

## Small-Model Execution Notes
- ...
```
