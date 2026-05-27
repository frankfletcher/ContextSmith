# Ralph Improvement Loop

The Ralph loop is an optional bounded improvement loop. It asks: “This passed minimum validation, but how can it be better for local/smaller models?”

## When to Use

Use when the artifact is reusable, high-risk, long-running, user-requested, or will guide file/tool operations.

Do not use for short one-off tasks unless requested.

## Iteration Limits

- Default maximum: 2 iterations.
- Hard maximum: 3 unless the user explicitly overrides.
- Stop if all categories are B or better and no high-risk issue remains.
- Stop if the next iteration would add bloat, semantic drift, or only cosmetic polishing.

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
