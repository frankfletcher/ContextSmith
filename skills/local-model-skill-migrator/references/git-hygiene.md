# Git Hygiene for Agent Work Artifacts

Agent work artifacts are usually local operational state, not project source.

## Gitignore Suggestion

By default, suggest adding these paths to `.gitignore`:

```gitignore
# Agent work state
.agent-work/
.agent-task/
.agent-iterations/
.agent-reports/

# Local skill migration workspaces
.skill-migrations/
```

Do not modify `.gitignore` automatically unless the user explicitly approves repository edits.

## Commit-Worthiness Check

Usually commit:

- `AGENTS.md`
- edited source files
- edited docs
- finalized reusable prompt/skill/instruction files
- curated migration summaries
- human-reviewed architecture notes

Usually do not commit:

- `.agent-work/`
- Ralph iteration folders
- subagent scratch reports
- local task-state files
- raw command output
- temporary validation logs
- generated zips unless they are release artifacts

If unsure, recommend keeping the file local.
