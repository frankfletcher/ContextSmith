# Ralph Improvement Loop

The Ralph loop is an optional bounded improvement loop. It asks: “This passed minimum validation, but how can it be better for local/smaller models?”

## When to Use

Use when the artifact is reusable, high-risk, long-running, user-requested, or will guide file/tool operations.

Do not use for short one-off tasks unless requested.

## Iteration Limits

- Default maximum: 2 iterations.
- Hard maximum: 3 unless the user explicitly overrides.
- Stop if no material defect remains and next iteration would add bloat, semantic drift, or only cosmetic polishing.

## Per-Iteration Structure

All iterations use the same structure — there is no #1/#2/#3 role distinction. Each iteration does:

1. **Critique** — Identify material defects, gaps, edge cases, or spec violations.
2. **Strategic review** — Ask: "Beyond baseline, how can this be improved? What is the gap between 'done' and 'well done'? Is there a better approach?" Act on material insights.
3. **Cross-reference** — Before acting, check if the improvement is already planned in a downstream phase or task-state item. If yes, enrich that phase's detail instead of implementing early.
4. **Fix** — Apply material defect fixes and scoped improvements. For complex improvements not already planned, add a new phase to the plan rather than implementing inline.
5. **Record** — Log what was critiqued, fixed, and decided. If no material defect remains, record as no-op with reason.

No-op iterations are valid evidence. Do not invent changes to satisfy the iteration count.

## A-F End Evaluation

## A-F End Evaluation

At the end of each iteration, grade:

- Small-model atomicity
- Instruction clarity
- Output contract quality
- Context strategy
- Assumption control
- Domain fit
- Validation strength
- Loop safety
- Git/file safety, if applicable
- Bloat / cognitive load

Ask:

1. What is still too abstract for a smaller model?
2. What assumption should be explicit?
3. What loop, context, Git, or side-effect risk remains?
4. What can be made more atomic without bloating the artifact?
5. Is another iteration materially justified?

## Canonical Iteration Storage

Use `references/output-location.md`.

For project-based work, write iterations under:

```text
<project>/.agent_work/sprints/<sprint-or-subproject>/tasks/<YYYY-MM-DD-short-slug>/iterations/
```

Each iteration folder should contain:

- generated artifact
- `audit.md`
- `ralph-report.md`
- `changes.md`

Never leave canonical Ralph outputs only in `/tmp`.
