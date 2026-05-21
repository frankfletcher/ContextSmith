# Persistent Task State

Use persistent task state for long-running, multi-phase, multi-file, crash-sensitive, or validation-heavy work.

## Directory Layout

```text
.agent-work/
└── sprints/<sprint-or-subproject>/tasks/<YYYY-MM-DD-short-slug>/
    ├── TASK.md
    ├── PLAN.md
    ├── STATUS.md
    ├── DECISIONS.md
    ├── CONTEXT.md
    ├── CHECKLIST.md
    ├── ARTIFACTS.md
    ├── PHASE_LOG.md
    └── NEXT_PROMPT.md
```

## File Responsibilities

- `TASK.md`: objective, scope, constraints, success criteria. Update only when task changes.
- `PLAN.md`: phase checklist. Use enough phases for the model and task complexity.
- `STATUS.md`: current phase, completed work, in-progress work, next action. Keep short.
- `DECISIONS.md`: durable decisions only, with reason and impact.
- `CONTEXT.md`: relevant file map, constraints, evidence notes, skip rules. No raw dumps.
- `CHECKLIST.md`: testable validation items.
- `ARTIFACTS.md`: changed/generated files and commands run.
- `PHASE_LOG.md`: one compact entry per phase.
- `NEXT_PROMPT.md`: short resume prompt.

## Phase Granularity Rule

Scale phases to task complexity. A large port, migration, or refactor should usually have 8-12 smaller phases, not 3 broad phases.

Each phase must include:

- goal
- inputs
- likely files/directories
- explicit tasks
- output artifacts
- validation checks
- stop condition
- handoff notes

## State Hygiene

Do not paste full files, logs, transcripts, command output, or model reasoning into state files. Store summaries, paths, commands, evidence anchors, decisions, and validation results.

## Canonical location

Use `references/output-location.md`. For project work, place task state under `<project>/.agent-work/`. Treat `.agent-work/` as local operational state and suggest gitignoring it using `references/git-hygiene.md`.
