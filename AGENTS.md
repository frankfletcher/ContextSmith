# AGENTS.md

ContextSmith is a meta-skills package for model-aware agent instruction engineering. This AGENTS.md is for agents working on ContextSmith itself — editing skills, shared references, docs, and the validation script.

## Repository Map

```
ContextSmith/
├── skills/                          # 7 installable skill folders (SKILL.md + references/)
│   ├── contextsmith/
│   ├── contextsmith-prompt-engineer/
│   ├── contextsmith-skill-engineer/
│   ├── contextsmith-skill-migrator/
│   ├── contextsmith-instruction-engineer/
│   ├── contextsmith-agent-evaluator/
│   └── contextsmith-orchestrator/
├── shared/                          # Canonical agent references (54 files)
├── orchestrator/                    # Python orchestrator package (deterministic workflow execution)
│   ├── __init__.py
│   ├── orchestrator.py              # Main loop: run(), run_workflow()
│   ├── state_reader.py              # Parse task-state artifacts
│   ├── checkpoint.py                # Checkpoint management
│   ├── step_compiler.py             # StepContract compilation
│   ├── validators.py                # Artifact and schema validation
│   ├── cli.py                       # CLI interface
│   └── adapters/                    # Harness adapters
│       ├── base.py                  # StepContract, HarnessResult, HarnessAdapter ABC
│       ├── generic.py               # File-based fallback adapter
│       └── opencode.py              # OpenCode subprocess adapter
├── tests/                           # Python test suite
├── docs/                            # User-facing documentation
│   ├── workflows/
│   ├── concepts/
│   ├── reference/
│   └── contributing/
├── scripts/lint_error_counter.py    # Persistent lint error frequency counter
├── scripts/validate_skills.py       # Skill metadata validator
├── README.md                        # Project landing page
├── PACKAGE_SPEC.md                  # Design decisions and package spec
├── CHANGELOG.md                     # Version history
├── CONTEXTSMITH_LIVING_NOTES.md
└── .agent_work/                     # Persistent task state (gitignored)
```

## Setup and Validation Commands

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install markdownlint (required for Markdown validation)
npm install -g markdownlint-cli

# Sync dependencies and create .venv
rtk uv sync

# Run validation
rtk uv run python scripts/validate_skills.py
rtk uv run ruff check orchestrator/ --select E,F,W,I | uv run python scripts/lint_error_counter.py
rtk uv run ruff format orchestrator/ --check
rtk uvx radon cc orchestrator/ -s -a | grep -E " - [CDEF] "
rtk markdownlint .agent_work/ orchestrator/ docs/ --ignore node_modules | uv run python scripts/lint_error_counter.py
rtk uv run pytest tests/ -v

# View accumulated lint error frequencies (top 10 across all runs)
rtk python -c "import json; d=json.load(open('.agent_work/lint_error_counts.json')); [print(f'{v:4d} {k}') for k,v in sorted(d.items(), key=lambda x:-x[1])[:10]]"

# Reset the lint error counter (clears accumulated frequencies)
echo '{}' > .agent_work/lint_error_counts.json
```

The validation script checks SKILL.md frontmatter, line counts, and reference directory presence. Ruff handles Python linting, formatting, and import sorting. Radon checks cyclomatic complexity (no C/D/E/F allowed). Markdownlint validates all Markdown files. Pytest runs the test suite. The lint error counter (`scripts/lint_error_counter.py`) pipes through ruff and markdownlint output to accumulate error code frequencies across runs, surfacing the most common issues for targeted standards improvement.

Note: All Python commands should be run with `uv run` to use the project's virtual environment. Dependencies are managed in `pyproject.toml` and locked in `uv.lock`.

## Extra-Audit Step

The orchestrator supports an optional `extra_audit` state that runs after the baseline audit. It applies `shared/extra-audit.md` — strategic-lens review for trajectory, scope pressure, dependency surface, blind spots, and exit-condition honesty.

To enable, add `extra_audit` to a workflow config's `states` and `phase_order` after the baseline audit state. The step produces `EXTRA_AUDIT.md`, an append-only persistent artifact. See `shared/extra-audit.md` for the full schema and config template.

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
- Agent workflow artifacts, including Superpowers specs and plans, must go under `.agent_work/`, not `docs/`. This overrides any external skill default that suggests `docs/superpowers/...`. The `docs/` tree is only for user-facing package documentation.

## Coding Standards

This repo has Python files in `orchestrator/` and `scripts/`, plus many Markdown/YAML files.

### Python
- All Python code must pass `rtk ruff check --select E,F,W,I` and `rtk ruff format --check`.
- Run `rtk ruff check --fix` and `rtk ruff format` before committing.
- The orchestrator package is in `orchestrator/`. Tests are in `tests/`.
- Ask for approval before adding new dependencies.
- Follow PEP 8 (enforced by ruff).

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

## Temporary Files

Never use `/tmp` for temporary files or scratch directories. Always use `<project root>/.agent_work/tmp/`. This directory is gitignored and scoped to the project — no cross-project contamination, no cleanup needed. Create it if it doesn't exist:

```bash
mkdir -p .agent_work/tmp
```

Use this for any scratch files, diff patches, intermediate artifacts, or staged content that doesn't belong in task state.

## File Operation Safety

Always read before writing:

1. To check if a file exists, use `test -f <path>` or the `read` tool. Do NOT use `ls` for existence checks — `ls` can produce false negatives.
2. Before creating or overwriting any file, read it first. If the read succeeds (returns content), use `edit` to modify it or `>>` to append — never use `write` on a file whose current content you haven't verified.
3. **PREFERRED: write `.new` segment files instead of appending.** For `*_REPORT.md`, `PHASE_LOG.md`, and `DECISIONS.md`, write a `.new` file with only the new entry content (e.g., `EDUCATIONAL_REPORT.md.new`). The orchestrator merges `.new` segments into the parent report automatically after execution — this removes the agent from the append operation entirely. If `.new` files are not feasible (e.g., the orchestrator is not involved), use `cat >>` heredoc to append. **Never use `write` on parent report/log/decision files** — it destroys accumulated history. Do not `test -f` first; the agent cannot reliably determine which files exist in git vs. on disk.
4. When a `write` call is necessary (new file that is definitely NOT a report/log/decision file), first confirm with `test -f` that the path is clear.
5. After any file operation, verify the result: read the file or check with `test -f`/`stat` to confirm the expected content is there.

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
- Do not place transient plans, specs, scratch notes, or other agent workflow artifacts under `docs/`; use `.agent_work/` for those artifacts.
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

## Versioning Convention

ContextSmith uses project-level versioning. The canonical version lives in `PACKAGE_SPEC.md`. After the determinism sprint, all skills move to 2.0.0. Per-skill `metadata.version` in SKILL.md frontmatter mirrors the project version but is no longer independently meaningful — do not bump individual skills. See `docs/reference/VERSIONING.md` for the full policy.

## Human Approval Required

- Git operations listed under Git Safety.
- Modifying `.gitignore`.
- Adding new dependencies.
- Editing `PACKAGE_SPEC.md` design decisions.
- Removing or renaming skills.
- Batch migration or mass file changes.



## Agent-User interaction rules

* When advising, brainstorming, evaluating, or reviewing: be honest over agreeable. If my thinking has gaps or my approach has a flaw, say so directly and specifically, tell me what's wrong and what would be better. If it's solid, say so and move on. Don't invent objections, don't pad your response, and don't restate what I just said. If you're uncertain or speculating, flag it. Never fabricate data, sources, or examples.

## Write Simple Code First

Before writing any Python function, apply the patterns in `shared/coding-standards.md` (the **Write Simple Code First** section). These prevent complex code from being written at all — no if/elif chains of 3+, no boolean parameters, no functions whose name contains "and", no nesting deeper than 3 levels. Extract early, extract often.

**Measure, don't assume.** After writing, run:

```bash
rtk uvx radon cc orchestrator/ -s -a | grep -E " - [CDEF] "
rtk uvx radon mi orchestrator/ -s | grep -E " - [BCDEF] "
```

- `radon cc`: cyclomatic complexity per function. A (1-5) = low, B (6-10) = moderate, C+ = complex. **Target: all touched functions ≤ B.**
- `radon mi`: maintainability index per file. A (20-100) = high, B (10-19) = moderate, C (0-9) = difficult. **Target: all touched files ≥ A.**

**The gate is a backup.** Do not write code assuming you'll fix it after radon complains. Write it clean in one pass. If radon flags a function, do not just rename variables — extract, restructure, eliminate branches. Loop until the function is naturally ≤ B.

For the full complexity prevention reference, see `shared/coding-standards.md`. For the gate procedure, see `shared/complexity-gate.md`.



# RTK (Rust Token Killer) - Token-Optimized Commands

## Golden Rule

**Always prefix commands with `rtk`**. If RTK has a dedicated filter, it uses it. If not, it passes through unchanged. This means RTK is always safe to use.

**Important**: Even in command chains with `&&`, use `rtk`:

```bash
# ❌ Wrong
git add . && git commit -m "msg" && git push

# ✅ Correct
rtk git add . && rtk git commit -m "msg" && rtk git push
```

## RTK Commands by Workflow

### Build & Compile (80-90% savings)

```bash
rtk cargo build         # Cargo build output
rtk cargo check         # Cargo check output
rtk cargo clippy        # Clippy warnings grouped by file (80%)
rtk tsc                 # TypeScript errors grouped by file/code (83%)
rtk lint                # ESLint/Biome violations grouped (84%)
rtk prettier --check    # Files needing format only (70%)
rtk next build          # Next.js build with route metrics (87%)
```

### Test (60-99% savings)

```bash
rtk cargo test          # Cargo test failures only (90%)
rtk go test             # Go test failures only (90%)
rtk jest                # Jest failures only (99.5%)
rtk vitest              # Vitest failures only (99.5%)
rtk playwright test     # Playwright failures only (94%)
rtk pytest              # Python test failures only (90%)
rtk rake test           # Ruby test failures only (90%)
rtk rspec               # RSpec test failures only (60%)
rtk test <cmd>          # Generic test wrapper - failures only
```

### Git (59-80% savings)

```bash
rtk git status          # Compact status
rtk git log             # Compact log (works with all git flags)
rtk git diff            # Compact diff (80%)
rtk git show            # Compact show (80%)
rtk git add             # Ultra-compact confirmations (59%)
rtk git commit          # Ultra-compact confirmations (59%)
rtk git push            # Ultra-compact confirmations
rtk git pull            # Ultra-compact confirmations
rtk git branch          # Compact branch list
rtk git fetch           # Compact fetch
rtk git stash           # Compact stash
rtk git worktree        # Compact worktree
```

Note: Git passthrough works for ALL subcommands, even those not explicitly listed.

### GitHub (26-87% savings)

```bash
rtk gh pr view <num>    # Compact PR view (87%)
rtk gh pr checks        # Compact PR checks (79%)
rtk gh run list         # Compact workflow runs (82%)
rtk gh issue list       # Compact issue list (80%)
rtk gh api              # Compact API responses (26%)
```

### JavaScript/TypeScript Tooling (70-90% savings)

```bash
rtk pnpm list           # Compact dependency tree (70%)
rtk pnpm outdated       # Compact outdated packages (80%)
rtk pnpm install        # Compact install output (90%)
rtk npm run <script>    # Compact npm script output
rtk npx <cmd>           # Compact npx command output
rtk prisma              # Prisma without ASCII art (88%)
```

### Files & Search (60-75% savings)

```bash
rtk ls <path>           # Tree format, compact (65%)
rtk read <file>         # Code reading with filtering (60%)
rtk grep <pattern>      # Search grouped by file (75%). Format flags (-c, -l, -L, -o, -Z) run raw.
rtk find <pattern>      # Find grouped by directory (70%)
```

### Analysis & Debug (70-90% savings)

```bash
rtk err <cmd>           # Filter errors only from any command
rtk log <file>          # Deduplicated logs with counts
rtk json <file>         # JSON structure without values
rtk deps                # Dependency overview
rtk env                 # Environment variables compact
rtk summary <cmd>       # Smart summary of command output
rtk diff                # Ultra-compact diffs
```

### Infrastructure (85% savings)

```bash
rtk docker ps           # Compact container list
rtk docker images       # Compact image list
rtk docker logs <c>     # Deduplicated logs
rtk kubectl get         # Compact resource list
rtk kubectl logs        # Deduplicated pod logs
```

### Network (65-70% savings)

```bash
rtk curl <url>          # Compact HTTP responses (70%)
rtk wget <url>          # Compact download output (65%)
```

### Meta Commands

```bash
rtk gain                # View token savings statistics
rtk gain --history      # View command history with savings
rtk discover            # Analyze Claude Code sessions for missed RTK usage
rtk proxy <cmd>         # Run command without filtering (for debugging)
rtk init                # Add RTK instructions to CLAUDE.md
rtk init --global       # Add RTK to ~/.claude/CLAUDE.md
```

## 

@RTK.md
