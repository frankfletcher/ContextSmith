/contextsmith-run --run-mode phase --validation strict --self-audit true --ralph 3 --mode guided --target-profile generic-local --context-length 120k

You are implementing the Artifact Schema Standards project. Your job is to execute exactly one phase of the 11-phase plan — every sub-phase in it — then stop.

Read these files in order:

1. `.agent_work/sprints/artifact-schema-standards/tasks/2026-06-14-schema-registry/STATUS.md` — tells you which phase and sub-phase you're in
2. `.agent_work/sprints/artifact-schema-standards/tasks/2026-06-14-schema-registry/NEXT_PROMPT.md` — tells you exactly what to do for the current sub-phase
3. `.agent_work/sprints/artifact-schema-standards/tasks/2026-06-14-schema-registry/CONTEXT.md` — project constraints and file locations
4. `.agent_work/sprints/artifact-schema-standards/tasks/2026-06-14-schema-registry/PLAN.md` — the full 11-phase plan with sub-phases, context budgets, and tasks
5. `.agent_work/sprints/artifact-schema-standards/tasks/2026-06-14-schema-registry/CHECKLIST.md` — track what's done per task
6. `.agent_work/sprints/artifact-schema-standards/tasks/2026-06-14-schema-registry/ARTIFACTS.md` — artifact inventory

Do exactly what NEXT_PROMPT.md says for the current sub-phase. Then advance to the next sub-phase and repeat until all sub-phases in the current phase are done.

For every sub-phase:

1. Read NEXT_PROMPT.md — it describes the sub-phase's task, input files, output requirements, and constraints
2. Execute all tasks for that sub-phase
3. Run Ralph loop (3 iterations: critique → fix → recheck → fix → final check)
4. Run self-audit: goal satisfied, validation commands executed, side-effect boundaries respected, task state updated
5. Check off completed tasks in CHECKLIST.md (`[x]`)
6. Write an entry to `EDUCATIONAL_REPORT.md.new` with a `## Sub-phase N.M` section explaining what was done, what you learned, and why decisions were made — the orchestrator will merge this into the report automatically
7. Write an entry to `AUDIT_REPORT.md.new` with a `## Sub-phase N.M` section containing the full A-F rubric grade (Clarity, Atomicity, Safety, Testability, Domain Fit, Context Fit) and rationale — the orchestrator will merge this into the report automatically
8. Write an entry to `PHASE_LOG.md.new` with changes summary — the orchestrator will merge this into the report automatically
9. Update `STATUS.md` Current Sub-phase to the next sub-phase within the phase

When all sub-phases in the current phase are complete:

1. Run full validation suite:

    uv run python scripts/validate_skills.py
    uv run ruff check orchestrator/ --select E,F,W,I | uv run python scripts/lint_error_counter.py
    uv run ruff format orchestrator/ --check
    uv run pytest tests/ -v
    markdownlint . --ignore node_modules | uv run python scripts/lint_error_counter.py

2. Write `RESULT.json`: {"status": "pass"|"fail", "reason": "...", "phase_completed": "Phase N: Name", "artifacts": ["file1", "file2", ...]}
3. Update `STATUS.md`: set `## Current Phase` to the next phase, `## Current Sub-phase` to its first sub-phase, `## Current State` to "execute", increment phase counter
4. Write `NEXT_PROMPT.md` for the next agent — generate sub-phase tasks from PLAN.md, include Input Files, Output Requirements, Constraints, Ralph Loop, Self-Audit, and Hard Stop sections specific to the first sub-phase of the next phase
5. Write a phase-completion entry to `PHASE_LOG.md.new` — the orchestrator merges it into the log on next execution

### REPORT FILES: USE `.new` SEGMENTS — ORCHESTRATOR HANDLES MERGING

Do NOT write directly to these files. Write a `.new` segment instead — the orchestrator automatically merges `.new` files into the parent reports:

| Parent File | Write This Instead |
| --- | --- |
| `EDUCATIONAL_REPORT.md` | `EDUCATIONAL_REPORT.md.new` |
| `AUDIT_REPORT.md` | `AUDIT_REPORT.md.new` |
| `PHASE_LOG.md` | `PHASE_LOG.md.new` |
| `DECISIONS.md` | `DECISIONS.md.new` |

The `.new` file should contain ONLY the new entry content (e.g., `## Phase N` entry text). The orchestrator handles concatenation with existing history after execution. This removes the agent from the append operation entirely — no risk of overwrite, no file-existence guessing.

Never clobber EDUCATIONAL_REPORT.md, AUDIT_REPORT.md, PHASE_LOG.md, or DECISIONS.md — only append. Never proceed beyond the current phase. Do not skip the self-audit. Do not mark complete if files are missing or validation fails. Read every direction at every sub-phase and follow them to a T.

When auditing, never assume something has been done.  Never blindly assign an "A". Always check your work for each task in the rubric.
