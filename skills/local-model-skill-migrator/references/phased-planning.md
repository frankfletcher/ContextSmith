# Phased Planning

Use phased planning for complex, long-running, multi-file, migration, porting, refactor, or validation-heavy tasks.

## Granularity Rule

Phase count must scale with complexity. A three-phase plan is often too coarse for a large application port, repo migration, or multi-system refactor. Prefer 6–12 phases when the task has many unknowns, platforms, dependencies, or subsystems.

Each phase must include:

- goal
- inputs
- likely files/directories
- explicit tasks
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
