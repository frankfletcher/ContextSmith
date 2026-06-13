# Persistent Task State

Use persistent task state for long-running, multi-phase, multi-file, crash-sensitive, or validation-heavy work.

## Directory Layout

```text
.agent_work/
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

All state files that accumulate history (DECISIONS.md, PHASE_LOG.md, ARTIFACTS.md, and any report) must be updated by appending new entries — never overwrite the file. Identify each file's purpose: if it maintains a record, append to preserve the full history.

## Downstream Prompt Requirements

When the requested prompt will make a downstream agent create an implementation plan for long-running, multi-file, migration, release, refactor, validation-heavy, or coding work, compile the downstream prompt as a plan-package initializer unless the user explicitly asks for a single-file plan. The downstream model must understand that the deliverable is not only a narrative plan. It is a reusable work package that a later execution session can resume without the original chat transcript.

The downstream prompt MUST require the agent to create or update a task-state directory at:

```text
<project>/.agent_work/sprints/<sprint-or-subproject>/tasks/<YYYY-MM-DD-short-slug>/
```

The downstream prompt MUST require these artifacts:

- `TASK.md`: objective, scope, constraints, success criteria
- `PLAN.md`: phase checklist with small-model-executable phases
- `STATUS.md`: current phase, last completed work, next action
- `DECISIONS.md`: durable decisions with reasons
- `CONTEXT.md`: file map, constraints, evidence notes, skip rules
- `CHECKLIST.md`: validation checklist
- `ARTIFACTS.md`: generated/changed files and commands to run
- `PHASE_LOG.md`: compact phase entries
- `NEXT_PROMPT.md`: short resume prompt for the next session or first execution phase

The downstream prompt MUST tell the agent to write these files, not merely mention them. A section named "Persistent Task State" may summarize the directory and file responsibilities, but it is not a substitute for creating the files. If planning-only mode forbids code changes, state that task-state files are allowed planning artifacts and source-code edits remain forbidden.

The downstream prompt MUST require each state file to stay compact. Do not paste raw logs, full source files, long transcripts, or hidden reasoning into state files. Store objective facts: paths, commands, validation results, decisions, constraints, skip rules, and the next actionable instruction. `NEXT_PROMPT.md` must be directly usable as the first prompt in a fresh session.

For each planned phase, require the fields from `phased-planning.md`: goal, inputs, likely files/directories, explicit tasks, testing/validation steps, unit and integration tests where relevant, outputs/artifacts, validation checks, stop condition, and handoff notes. Require phase closeout to update the state files and refresh `NEXT_PROMPT.md`.

## Phase Gate Convention

When a NEXT_PROMPT.md contains a `.phase_gate` guard, the downstream agent must NOT execute until `<task-dir>/.phase_gate` exists. To proceed, create the flag file:

```bash
touch .agent_work/sprints/<sprint>/tasks/<task>/.phase_gate
```

The `.phase_gate` file is a zero-byte flag or contains a brief `ready` marker. This gives the human operator a chance to review before side effects occur. If the file is missing, report "Phase gate not set. Awaiting human instruction to proceed."

## Canonical location

Use `references/output-location.md`. For project work, place task state under `<project>/.agent_work/`. Treat `.agent_work/` as local operational state and suggest gitignoring it using `references/git-hygiene.md`.
