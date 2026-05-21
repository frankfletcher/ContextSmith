# Canonical Output Location

Use durable project-local output by default. Do not scatter Ralph reports, task plans, manifests, or validation reports across `/tmp`.

## Priority Order

1. If the user specifies an output directory, use it.
2. If the task is project/repo-based, use the project’s `.agent-work/` directory.
3. If the task is skill-package-based, use that skill/package’s `.agent-work/` or migration workspace.
4. If the task is not tied to a project, use a user-level workspace such as `~/.agent-work/`.
5. Use `/tmp` only for disposable scratch files, never for canonical reports or iteration history.

## Project-Based Task Layout

```text
<project>/.agent-work/
├── active-task
├── sprints/
│   └── <sprint-or-subproject>/
│       └── tasks/
│           └── <YYYY-MM-DD-short-slug>/
│               ├── TASK.md
│               ├── PLAN.md
│               ├── STATUS.md
│               ├── DECISIONS.md
│               ├── CONTEXT.md
│               ├── CHECKLIST.md
│               ├── ARTIFACTS.md
│               ├── PHASE_LOG.md
│               ├── NEXT_PROMPT.md
│               ├── iterations/
│               └── reports/
```

## Ralph Loop Output

For project-based work, write Ralph iterations under:

```text
<project>/.agent-work/sprints/<sprint-or-subproject>/tasks/<YYYY-MM-DD-short-slug>/iterations/
```

Each iteration must be written before the next iteration begins:

```text
iterations/
├── iteration-01/
│   ├── output.md
│   ├── audit.md
│   ├── ralph-report.md
│   └── changes.md
├── iteration-02/
└── FINAL/
```

## Migration Workspaces

- Installed user skills: `~/.agents/skill-migrations/<migration-id>/`
- Repo-local skill packages: `<project>/.agent-work/skill-migrations/<migration-id>/`

## `/tmp` Policy

`/tmp` is acceptable for temporary extraction, scratch output, and disposable previews. Never leave canonical plans, Ralph iterations, validation reports, manifests, or resume prompts only in `/tmp`.
