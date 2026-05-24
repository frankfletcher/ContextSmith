# AGENTS.md Guide

`AGENTS.md` is often the backbone of an agentic coding project. It shapes what the agent reads, how it edits, how it handles Git, how it validates work, and when it asks for help.

A good `AGENTS.md` is not a manifesto. It is a concise operating manual for this repo, this harness, this model, and this risk profile.

## Why it matters

Coding agents fail in predictable ways:

- they retry the same failing command
- they overwrite uncommitted work
- they run broad tests repeatedly without learning anything
- they write code that passes shallow tests
- they ignore project conventions
- they add dependencies without approval
- they treat a large repo as if it fits in one context window

`AGENTS.md` is where you can prevent many of those failures before they happen.

## Recommended workflow

When creating or improving `AGENTS.md`, ContextSmith should:

1. scan the repo structure
2. inspect existing instruction files
3. detect languages, frameworks, package managers, tests, and domain signals
4. identify which safeguards already exist
5. propose relevant instruction blocks
6. ask the user before making broad project-wide decisions
7. keep the final file concise

This is why `local-model-instruction-engineer` defaults to a more guided style for repo instruction work.

## Useful sections

A practical `AGENTS.md` often includes:

- project overview
- repository map
- setup commands
- build/test/lint commands
- coding standards
- testing expectations
- Git safety
- loop safety
- context management
- persistent task-state policy
- domain-specific guidance
- final validation checklist

Not every repo needs every section.

## What to avoid

Avoid:

- generic advice like “be careful”
- repeated near-duplicate rules
- long philosophical style guides
- outdated commands copied from old docs
- instructions that conflict with package scripts
- raw project dumps
- secrets or credentials
- model-specific runtime claims that the harness cannot control
- exposed chain-of-thought instructions

## Coding projects

For coding repos, useful defaults include:

- check `git status --short` before editing
- do not overwrite user changes
- do not run destructive Git commands without approval
- run narrow tests before broad tests
- report commands run and commands not run
- avoid unrelated refactors
- preserve public APIs unless asked
- do not add dependencies without approval
- keep changes small and cohesive

## Data science and ML projects

For data-science and ML repos, add guidance when relevant:

- inspect schema, shape, missing values, and target definitions
- do not modify raw data in place
- split before preprocessing
- fit preprocessing only on training data
- do not use test data for model selection
- define metrics before optimizing
- use baselines
- record seeds, data versions, features, model parameters, and environment details
- avoid committing large datasets, checkpoints, caches, and generated artifacts unless the repo intentionally tracks them

## Loop safety

A small but powerful block:

```markdown
## Agentic Loop Safety

Do not execute identical consecutive tool calls.

If the same command, patch, edit, or generated code block appears twice without progress, stop repeating it.

After a failure:
1. inspect the error
2. make at most one targeted correction
3. if the same failure repeats, change strategy
4. if no safe alternative exists, stop with `BREAK_LOOP_AWAITING_HUMAN_INPUT`
```

## Git safety

A useful compact block:

```markdown
## Git Safety

Before editing, run `git status --short`.

Do not run destructive or history-rewriting Git commands without explicit approval, including reset hard, clean, checkout/restore of the whole tree, rebase, merge abort, force push, branch deletion, commit amend, squash, or discarding uncommitted changes.

Do not run `git add`, `git commit`, or `git push` unless the user asks.
```

## Keep it compact

If `AGENTS.md` becomes too long, split detailed material into docs and keep `AGENTS.md` as the operating summary. For tight local models, a concise `AGENTS.md` plus good task-state files is usually better than one giant instruction file.
