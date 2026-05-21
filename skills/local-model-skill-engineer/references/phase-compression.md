# Phase Compression and Debrief

Use phase compression for long-running, multi-phase, or context-sensitive work. It helps the next run resume without reloading full history.

## Required Phase Debrief

At the end of each phase, write a compact debrief:

```markdown
## Phase Debrief

### Completed
- ...

### Evidence
- files changed, commands run, tests observed, reports produced

### Blockers
- ...

### Decisions
- ...

### Carry Forward
- facts, paths, decisions, risks, and next-phase constraints that remain relevant

### Do Not Carry Forward
- failed approaches, obsolete assumptions, irrelevant files, outdated hypotheses

### Next Phase
- next atomic phase goal and stop condition
```

## Compression Rules

- Summarize; do not paste raw logs or full files.
- Preserve exact paths, commands, errors, schemas, and decisions when needed.
- Keep phase summaries short enough to load in tight context windows.
- If `targeted_context_length` is tiny/tight, prefer more phases and stronger phase debriefs.
- Update `STATUS.md`, `CONTEXT.md`, and `PHASE_LOG.md` at phase closeout.

## Do-Not-Carry-Forward Notes

Use this section to prevent loops and repeated dead ends:

- failed approach and why it failed
- obsolete assumption replaced by evidence
- irrelevant files/directories to avoid
- validation paths that produced no signal

The next phase should read carry-forward notes, not the entire prior phase history.
