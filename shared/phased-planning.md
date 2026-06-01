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

Implementation phases must also include a compact context contract:

<!-- CONTEXT_BUDGET: Override per-project. Default: 64k tokens -->
```yaml
context_contract:
  targeted_context_length: "{{CONTEXT_BUDGET}}"
  usable_phase_budget: 32k
  tool_output_reserve: 32k
  phase_type: edit-light
  expected_tool_calls:
    search: 2
    read: 4
    edit: 2
    bash: 2
  max_tool_calls_before_compaction: 10
  max_raw_output_lines_per_call: 200
  fresh_session_after_phase: true
  stop_if_forecast_exceeded: true
```

Use phase types to size the reserve: `read-only`, `discovery-heavy`, `edit-light`, `edit-heavy`, or `validation-heavy`. If a phase is both discovery-heavy and edit-heavy, split it. Discovery should produce an edit map; editing should consume that map without broad repo exploration.

Each tool-heavy phase must include a context fit estimate covering task-state load, search output, file reads, edit/patch attempts, validation output, recovery buffer, and expected active context. If the estimate does not fit the usable phase budget, split the phase before execution.

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

During execution, compact or close the phase early when actual tool calls exceed the forecast by 50%, raw tool output dominates useful context, validation output becomes long, new discovery is required after edits begin, or the stop condition cannot fit the remaining reserve. Record the reason and create a narrower next phase instead of silently expanding scope.

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

<!-- CONTEXT_BUDGET: Override per-project. Default: 64k tokens -->
For tool-heavy work under tight or moderate targets (`targeted_context_length <= {{CONTEXT_BUDGET}}`), prefer one fresh session per phase unless the previous phase used few tool calls and produced no large search or validation output. For larger targets, continuing in the same session is acceptable only while the tool ledger stays compact and raw tool output is not carried forward.
