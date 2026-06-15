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
- Treat raw tool output as current-phase evidence, not next-phase memory.
- Preserve exact paths, commands, errors, schemas, and decisions when needed.
- Keep phase summaries short enough to load in tight context windows.
- If `targeted_context_length` is tiny/tight, prefer more phases and stronger phase debriefs.
- Update `STATUS.md`, `CONTEXT.md`, and `PHASE_LOG.md` at phase closeout.
- Maintain a compact tool ledger with searches, reads, commands, and validation results summarized as paths, commands, outcomes, and line anchors.

## Forecast-Exceeded Compaction

Compact or close the phase when:

- actual tool calls exceed the forecast by 50%
- raw tool output dominates useful context
- validation output is long enough that only summarized failures remain useful
- the phase needs new discovery after edits have started
- the stop condition cannot fit in the remaining context reserve
- more than one recovery strategy has failed
- the phase crosses its intended boundary

When forecast-exceeded compaction happens, write a short debrief with: completed work, exact evidence anchors, new findings, a revised next phase with a smaller context contract, and do-not-carry-forward notes. If the phase cannot safely finish after compaction, stop and hand off the revised next phase.

## Do-Not-Carry-Forward Notes

Use this section to prevent loops and repeated dead ends:

- failed approach and why it failed
- obsolete assumption replaced by evidence
- irrelevant files/directories to avoid
- validation paths that produced no signal

The next phase should read carry-forward notes, not the entire prior phase history.
