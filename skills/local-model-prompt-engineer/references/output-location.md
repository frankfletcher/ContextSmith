# Canonical Output Locations

Use predictable durable output locations so reports, Ralph iterations, plans, and task state do not scatter across `/tmp` or harness-specific scratch directories.

## Priority Order

1. If the user specifies an output directory, use it.
2. For project/repo work, use `<project>/.agent-work/`.
3. For skill-package work inside a repo, use that package's `.agent-work/`.
4. For installed user skill migrations, use `~/.agents/skill-migrations/`.
5. For non-project work, use `~/.agent-work/`.
6. Use `/tmp` only for disposable scratch, never as the only location for canonical reports or iterations.

## Project Task Layout

```text
<project>/.agent-work/
├── active-task
└── sprints/<sprint-or-subproject>/tasks/<YYYY-MM-DD-short-slug>/
    ├── TASK.md
    ├── PLAN.md
    ├── STATUS.md
    ├── DECISIONS.md
    ├── CONTEXT.md
    ├── CHECKLIST.md
    ├── ARTIFACTS.md
    ├── PHASE_LOG.md
    ├── NEXT_PROMPT.md
    ├── iterations/
    └── reports/
```

## Ralph Iterations

For project-based work, write Ralph iterations under:

```text
<project>/.agent-work/sprints/<sprint-or-subproject>/tasks/<YYYY-MM-DD-short-slug>/iterations/
```

Use numbered folders:

- `iteration-01/`
- `iteration-02/`
- `iteration-03/`
- `FINAL/`

Each iteration should include the output artifact, `ralph-report.md`, `audit.md`, and `changes.md` when files are being written.

## Migration Workspaces

Installed user skills:

```text
~/.agents/skill-migrations/<migration-id>/
```

Repo-local skill packages:

```text
<project>/.agent-work/skill-migrations/<migration-id>/
```

## Git Hygiene

Treat `.agent-work/` as local operational state by default. Suggest adding it to `.gitignore`; do not modify `.gitignore` without approval.
