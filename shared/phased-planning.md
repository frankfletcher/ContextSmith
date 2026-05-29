# Phased Planning

Use phased planning for complex, long-running, multi-file, migration, porting, refactor, or validation-heavy tasks.

## Granularity Rule

Phase count must scale with complexity. A three-phase plan is often too coarse for a large application port, repo migration, or multi-system refactor. Prefer 6–20 phases when the task has many unknowns, platforms, dependencies, or subsystems. Implementation of each phase must fit within the context window, therefore more phases with narrower scope are usually better than fewer broad phases.

Each phase must include:

- goal
- inputs
- likely files/directories
- explicit tasks
- testing/validation steps
- unit and integration tests where relevant
- outputs/artifacts
- validation checks
- stop condition
- handoff notes

## Phase Memory

For long work, require persistent phase memory:

- `TASK.md`
- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `CONTEXT.md`
- `CHECKLIST.md`
- `ARTIFACTS.md`
- `PHASE_LOG.md`
- `NEXT_PROMPT.md`

Use `references/persistent-task-state.md`, `references/output-location.md`, and `references/phase-compression.md`.

## Phase Closeout

At the end of each phase:

1. Update `STATUS.md`.
2. Check off `PLAN.md` items.
3. Record durable decisions in `DECISIONS.md`.
4. Record changed files/commands in `ARTIFACTS.md`.
5. Add compact notes to `PHASE_LOG.md`.
6. Write carry-forward and do-not-carry-forward notes.
7. Update `NEXT_PROMPT.md`.
8. Run phase compression and update `CONTEXT.md` for the next phase.
9. Run validation checks. If any fail, update `STATUS.md` to "Blocked", add details to `DECISIONS.md`, and exit.
10. Run an audit of the implementation plan for the next phase using `implementation-plan-audit.md`. If it fails, update `STATUS.md` to "Blocked", add details to `DECISIONS.md`, and exit.
11. Include a test quality audit for coding-related work. If it fails, update `STATUS.md` to "Blocked", add details to `DECISIONS.md`, and exit. Use `test-quality-audit.md`
12. If the stop condition is met, update `STATUS.md` to "Completed" and exit.

## Ralph Evaluation for Plans

Grade phase plans on:

- phase granularity
- small-model suitability
- memory/documentation support
- stop conditions
- validation strength
- context-risk handling
- domain fit
- human approval gates
- safeguards for side effects, loops, Git, and coding when relevant
- implementation plan audit results when relevant
- overall plan quality and reliability

## Implementation Plan Audit Integration

For coding, migration, repo-porting, or long-running work, run the implementation plan audit from `implementation-plan-audit.md` before treating a plan as executable.

Phase count must scale with `targeted_context_length`. For `targeted_context_length <= 32k`, prefer more smaller phases over fewer broad phases. A large Windows/macOS-to-Linux port should usually be closer to 10-25 phases.

Every phase should end with phase compression/debrief and `Do Not Carry Forward` notes.
