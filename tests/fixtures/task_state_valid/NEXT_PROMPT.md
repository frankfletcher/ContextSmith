# Next Prompt: Phase 1C

## Artifact Manifest
- artifact_type: next_prompt
- phase: Phase 1C
- target_profile: qwen36
- parent_plan: PLAN.md
- version: 1.0.0

## Mission

Implementation

**Hard boundary:** Do not proceed to Phase 1D. Do not invoke models or execute phases.

## Read Order

1. STATUS.md — current phase and next action
2. Phase 1C section in PLAN.md — goal, actions, validation
3. CONTEXT.md — constraints and validation commands
4. CHECKLIST.md — optional context

## Phase Contract

- usable_phase_budget: 3000
- expected_tool_calls: 15
- stop_rule: All tests passing and lint clean
- validation_output_reserve: 500

## Actions

1. Implement feature X
2. Write tests
3. Run linting

## Allowed and Disallowed Actions

| Allowed | Disallowed |
|---|---|
| Implement feature X | All tests passing and lint clean |
| Write tests | Editing files outside workspace |
| Run linting | Proceeding to the next phase |
|  | Invoking models |

## Validation Commands

- Run available project validation commands

## Closeout

Update `STATUS.md`, `PHASE_LOG.md`, `ARTIFACTS.md`, `CONTEXT.md`, `CHECKLIST.md`, and `NEXT_PROMPT.md` with compact facts only. Record changed files, commands run, validation result, blockers, carry-forward, do-not-carry-forward, and next action.

## Recovery

If validation fails or the phase cannot complete:
1. Stop. Do not widen scope or start the next phase.
2. Set `STATUS.md` to `Blocked` with the failed gate and exact reason.
3. Add a `PHASE_LOG.md` entry with attempted action and validation result.
4. Write `NEXT_PROMPT.md` for human/frontier review with at most three options: fix, narrow scope, or abandon.

## Self-Audit

Before closeout, verify:
- Original phase goal satisfied or blocker recorded
- All validation commands executed or blocker documented
- Side-effect boundaries respected
- Task state updated with compact facts
- No broad architecture decisions made without evidence

## Expected Output Format

```
## Result
## Evidence
## Self-Audit
## Ralph Summary
## Validation
## Declared vs Enforced
## Risks / Next Action
```

## Hard Stop

Do not proceed to Phase 1D.
Current phase is Phase 1C. Do not move beyond it.
Do not implement features outside this phase.
Do not invoke models or execute phases.
Do not edit files outside the current phase scope.

## Education Notes

Review the phase contract carefully. Focus on the stop_rule and validation commands before proceeding. Keep context budget in mind.