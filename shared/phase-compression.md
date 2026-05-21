# Phase Compression and Debrief

Use this reference for long-running or multi-phase tasks.

## Phase Closeout

At the end of each phase, write a compact debrief:

```markdown
## Phase Closeout

Phase completed:
Evidence of completion:
Files changed:
Commands run:
Validation result:
Failed approaches:
Decisions made:
Carry forward:
Do not carry forward:
Next phase:
```

## Do Not Carry Forward

Record stale assumptions and failed approaches so the model does not repeat them.

Examples:

```markdown
## Do Not Carry Forward
- Failed approach: using the Windows-only packaging script.
- Obsolete assumption: app requires Electron 20.
- Irrelevant files: old build output under `dist/`.
```

## Active Context Manifest

For long tasks, keep a small manifest of what should be loaded next:

```markdown
# Active Context Manifest

Read these:
- TASK.md
- STATUS.md
- CHECKLIST.md
- DECISIONS.md

Do not read unless needed:
- archive/
- old iterations/
- raw logs/
```

## Compression Rule

Carry forward only what affects the next phase: constraints, decisions, blockers, relevant files, validation status, and next actions. Do not carry raw logs or obsolete context.
