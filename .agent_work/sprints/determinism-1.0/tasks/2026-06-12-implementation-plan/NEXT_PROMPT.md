## Gate: .phase_gate

This prompt is queued for the next run. Do NOT execute until
`.agent_work/sprints/determinism-1.0/tasks/2026-06-12-implementation-plan/.phase_gate` exists.
If the file is missing, stop and report "Phase gate not set. Awaiting human instruction to proceed."

# Next Prompt: Phase 8 — Documentation and Polish

## Current Status

- Phase: 8 of 9 (4 sub-phases: 8a, 8b, 8c, 8d)
- State: init
- Completed: Phases 1-7 — all schemas, core module, adapters, validators, 2 skills, quality fixes, collapse + determinism hardening, integration/testing (374 tests)

## Your Task

Execute **all** of Phase 8 (sub-phases 8a, 8b, 8c, 8d). This is a full-phase execution. The phase is complete when all 4 sub-phases are done and validated.

See `PLAN.md` Phase 8 for full detail on each sub-phase.

| Sub-phase | Task | Key files |
|-----------|------|-----------|
| **8a** | Trim orchestrator SKILL.md — extract artifact templates to references/artifact-templates.md | skills/contextsmith-orchestrator/SKILL.md |
| **8b** | Fix schema deprecation — update $schema from draft-07 to 2020-12 | schemas/workflow_config.schema.json |
| **8c** | Update user-facing docs — run markdownlint, fix MD060 issues in docs/ | docs/ |
| **8d** | CHANGELOG entry — comprehensive entry covering Phase 5.5-6 changes | CHANGELOG.md |

## Execution Order

1. Run 8a → 8b → 8c → 8d in sequence

## Per Sub-phase Cycle

Each sub-phase follows: Implement → Audit → Ralph (3 iterations) → Validate → Record.

### Validation Commands

For each sub-phase, run:
- `uv run ruff check orchestrator/ --select E,F,W,I`
- `uv run python scripts/validate_skills.py`
- `uv run pytest tests/ -q`
- `uv run ruff format orchestrator/ --check`
- `uvx radon cc orchestrator/ -s -a | grep -E " - [CDEF] "`
- `uvx radon mi orchestrator/ -s | grep -E " - [BCDEF] "`

## Report Files — APPEND ONLY

- EDUCATIONAL_REPORT.md: use `>>` heredoc — never `write`
- AUDIT_REPORT.md: use `>>` heredoc — never `write`
- DECISIONS.md: append new decisions, never overwrite

## Stop Condition

Phase 8 is complete when all 4 sub-phases pass, SKILL.md is under 500 lines, schema deprecation warning is resolved, markdownlint issues in docs/ are fixed, and CHANGELOG.md is updated.

When done, update STATUS.md to phase_8_complete and write NEXT_PROMPT.md for Phase 9.

## Context

Continue from Phase 7. All 374 tests pass. The orchestrator SKILL.md is at 572 lines (needs trimming in 8a). Schema validation produces deprecation warnings for draft-07 (to be fixed in 8b).
