# Git Safety

Use this reference for coding agents, repo instruction files, skill migrations inside Git repos, and any workflow that edits project files.

## Hard Rule

Do not perform destructive or history-rewriting Git operations without explicit user approval.

## Requires Explicit Approval

- `git reset --hard`
- `git clean -fd` or `git clean -fdx`
- `git checkout -- .`
- `git restore .`
- `git restore --staged .`
- `git rebase`
- `git rebase --continue`
- `git rebase --abort`
- `git merge --abort`
- `git push --force`
- `git push --force-with-lease`
- deleting branches
- amending, squashing, or rewriting commits
- discarding uncommitted changes
- removing files outside the requested scope
- staging/committing/pushing unless the user asked for Git commit management

## Safe Inspection Commands

Allowed without approval:

- `git status`
- `git status --short`
- `git diff`
- `git diff --staged`
- `git log --oneline -n 20`
- `git branch --show-current`
- `git show`

## Working Tree Protection

Before editing files:

1. Run `git status --short` when inside a Git repo.
2. Identify uncommitted user changes.
3. Inspect relevant diffs for files you intend to edit.
4. Do not overwrite user changes without approval.
5. If editing a dirty file is required, preserve existing changes and explain the risk.

## Branching and Commits

For large tasks:

- Recommend creating a feature branch before major edits.
- Ask before creating or switching branches.
- Do not run `git add`, `git commit`, or `git push` unless the user explicitly asks.
- If asked to commit, stage only relevant files.
- Use concise commit messages describing user-visible changes.

## Rebase Policy

Do not start, continue, abort, or repair a rebase without explicit user approval.

If the repository is already in a rebase state:

1. Stop normal edits.
2. Use safe inspection commands only.
3. Report the rebase state to the user.
4. Ask whether to continue, abort, or pause.
5. Do not guess.

If conflicts exist, do not resolve them unless the user explicitly asks you to handle the conflicts.

## Git Loop Prevention

Do not repeat the same Git command after failure. If a Git command fails or reports a conflict:

1. Inspect `git status`.
2. Change strategy or ask for input.
3. Do not run the same Git command again unless the cause has been fixed.
4. If unsure, stop with `BLOCKED_GIT_STATE_REQUIRES_HUMAN_INPUT`.

## Compact AGENTS.md Block

```markdown
## Git Safety

Do not run destructive or history-rewriting Git commands without explicit user approval.

Requires approval:
- `git reset --hard`
- `git clean -fd` / `git clean -fdx`
- `git rebase`, `git rebase --continue`, `git rebase --abort`
- `git merge --abort`
- `git push --force` / `git push --force-with-lease`
- deleting branches
- amending, squashing, or rewriting commits
- discarding uncommitted changes

Safe inspection commands:
- `git status`
- `git diff`
- `git diff --staged`
- `git log --oneline -n 20`
- `git branch --show-current`

Before editing, check `git status --short`. Do not overwrite user changes. If a rebase or merge conflict is in progress, stop and ask for guidance.
```
