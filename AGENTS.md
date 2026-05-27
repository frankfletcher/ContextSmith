# AGENTS.md

ContextSmith is a meta-skills package for model-aware agent instruction engineering. This AGENTS.md is for agents working on ContextSmith itself — editing skills, shared references, docs, and the validation script.

## Repository Map

```
ContextSmith/
├── skills/                          # 5 installable skill folders (SKILL.md + references/)
│   ├── local-model-prompt-engineer/
│   ├── local-model-skill-engineer/
│   ├── local-model-skill-migrator/
│   ├── local-model-instruction-engineer/
│   └── local-model-agent-evaluator/
├── shared/                          # Canonical agent references (42 files)
├── docs/                            # User-facing documentation
│   ├── workflows/
│   ├── concepts/
│   ├── reference/
│   └── contributing/
├── scripts/validate_skills.py       # Skill metadata validator
├── README.md                        # Project landing page
├── PACKAGE_SPEC.md                  # Design decisions and package spec
├── CHANGELOG.md                     # Version history
├── LOCAL_MODEL_AGENT_ENGINEERING_LIVING_NOTES.md
└── .agent_work/                     # Persistent task state (gitignored)
```

## Setup and Validation Commands

```bash
python scripts/validate_skills.py
```

No package manager, build system, or test framework. The validation script checks SKILL.md frontmatter, line counts, and reference directory presence.

Note: The validation script requires PyYAML. Install with `pip install pyyaml` if needed.

## Development Workflow

### Adding or editing a skill
1. Edit `skills/<skill>/SKILL.md` and/or `skills/<skill>/references/` files.
2. Run `python scripts/validate_skills.py`.
3. Update `CHANGELOG.md` if the change is user-facing.
4. Update `PACKAGE_SPEC.md` if design decisions change.

### Editing shared references
- `shared/` files are canonical. Skills may copy them to per-skill `references/` for standalone install. After editing a shared reference, decide whether per-skill copies need updating.

### Adding or editing docs
- User-facing docs go in `docs/`. Use the project voice from `.agent_work/contextsmith_mem.md` and `shared/documentation-quality.md`.

## Coding Standards

This repo has one Python file and many Markdown/YAML files.

### Python
- The single file is `scripts/validate_skills.py`. Keep it readable and self-contained.
- No new dependencies without approval.
- Follow PEP 8.

### Markdown / YAML
- SKILL.md frontmatter: YAML between `---` fences with `name`, `description`, and `metadata.version`.
- Avoid arbitrary top-level frontmatter keys. Use `metadata` for extra fields.
- Keep SKILL.md under 500 lines.
- Headings: use ATX-style (`##`), not setext-style.

## Git Safety

Do not run destructive or history-rewriting Git commands without explicit user approval.

Requires approval:
- `git reset --hard`, `git clean -fd` / `git clean -fdx`
- `git rebase`, `git rebase --continue`, `git rebase --abort`
- `git merge --abort`
- `git push --force` / `git push --force-with-lease`
- deleting branches, amending/squashing/rewriting commits
- discarding uncommitted changes

Safe inspection: `git status`, `git diff`, `git diff --staged`, `git log --oneline -n 20`, `git branch --show-current`.

Before editing, check `git status --short`. Do not overwrite user changes. If a rebase or merge conflict is in progress, stop and ask.

## Agentic Loop Safety

1. Do not execute identical consecutive tool calls.
2. If the same command, patch, or edit fails twice, stop repeating.
3. Before retrying, change the command, arguments, target, working directory, input, or strategy.
4. After a tool failure, inspect the error and make at most one targeted correction.
5. If no safe alternative exists, stop with `BREAK_LOOP_AWAITING_HUMAN_INPUT`.
6. Do not brainstorm repeatedly. After at most 3 options, choose one and act.
7. Do not rewrite the plan more than once per phase unless new evidence changes the task.
8. After an edit, verify that the file changed. Do not repeat no-op edits.
9. Keep working notes phase-local and brief.
10. Focus on the next atomic action: inspect, edit, validate, report, or ask.

## Context Management

- `shared/` contains 42 reference files. Do not load them all at once. Use glob/grep to find relevant files, then read selectively.
- The validation script output is the primary functional test. Run it before claiming work is complete.
- For reference-authoring tasks, prefer the index/query/verify pattern: grep for related content, read the best match, then edit.

## File and Directory Boundaries

- Do not edit files outside the workspace without explicit approval.
- `skills/` and `shared/` are the core package. Treat `docs/` as derivative (user-facing documentation derived from the reference content).
- `docs/contributing/documentation-style.md` and `docs/contributing/documentation-review-checklist.md` are the voice/style authority for user-facing docs.
- `shared/` files are the canonical source for agent-facing references. Skills must not redefine concepts that `shared/` already defines.

## Persistent Task State

For multi-phase work, use `.agent_work/sprints/<sprint>/tasks/<YYYY-MM-DD-slug>/`:

```
.agent_work/
└── sprints/<sprint>/tasks/<YYYY-MM-DD-slug>/
    ├── TASK.md          # objective, scope, constraints
    ├── PLAN.md          # phase checklist
    ├── STATUS.md        # current phase, next action
    ├── DECISIONS.md     # durable decisions with reasons
    ├── CONTEXT.md       # file map, constraints, skip rules
    ├── PHASE_LOG.md     # one compact entry per phase
    └── NEXT_PROMPT.md   # short resume prompt
```

Example: `.agent_work/sprints/contextsmith-1.0/tasks/2026-05-24-agents-md`

Keep state files short. Do not paste full files or raw output into state files.

## Documentation Standards

When editing README, docs, or CHANGELOG:
- Use a practical, warm, explanatory voice. Avoid generic AI-sounding contrast patterns ("not just X, but Y").
- Keep agent reference material (skills, shared/) imperative and precise.
- Run `python scripts/validate_skills.py` after skill changes.
- Refer to `shared/documentation-quality.md` and `docs/contributing/documentation-review-checklist.md` for full review criteria.

## Human Approval Required

- Git operations listed under Git Safety.
- Modifying `.gitignore`.
- Adding new dependencies.
- Editing `PACKAGE_SPEC.md` design decisions.
- Removing or renaming skills.
- Batch migration or mass file changes.