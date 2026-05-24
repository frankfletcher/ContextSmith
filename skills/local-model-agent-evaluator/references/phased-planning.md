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
## Implementation Plan Audit Integration

For coding, migration, repo-porting, or long-running work, run the implementation plan audit from `implementation-plan-audit.md` before treating a plan as executable.

Phase count must scale with `targeted_context_length`. For `targeted_context_length <= 32k`, prefer more smaller phases over fewer broad phases. A large Windows/macOS-to-Linux port should usually be closer to 8-15 phases than 3 broad phases.

Every phase should end with phase compression/debrief and `Do Not Carry Forward` notes.
