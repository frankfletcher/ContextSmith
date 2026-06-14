## Gate: .phase_gate

This prompt is queued for the next run. Do NOT execute until
`.agent_work/sprints/determinism-1.0/tasks/2026-06-12-implementation-plan/.phase_gate` exists.
If the file is missing, stop and report "Phase gate not set. Awaiting human instruction to proceed."

# Next Prompt: Phase 9 — Final Validation and Lock

## Current Status

- Phase: 9 of 9 (3 sub-phases: 9a, 9b, 9c)
- State: init
- Completed: Phases 1-8 — schemas, core module, adapters, validators, 2 skills, quality fixes, collapse + determinism hardening, integration/testing (374 tests), documentation/polish

## Your Task

Execute **all** of Phase 9 (sub-phases 9a, 9b, 9c). This is the final phase of the Deep Determinism project. The project is complete when all 3 sub-phases are done and validated.

See `PLAN.md` Phase 9 for full detail on each sub-phase.

| Sub-phase | Task | Key files |
|-----------|------|-----------|
| **9a** | Full validation pass | Run full suite: ruff, format, validate_skills, pytest, markdownlint. Fix remaining issues. |
| **9b** | Final self-audit | Audit all phases 1-9 against A-F rubric. Verify every expected_output from every sub-phase exists and is non-empty. |
| **9c** | Project closeout | Verify git status is clean. Check staged_skills/ in .agent_work/ for stale artifacts. Write final DECISIONS.md entry. Tag release if applicable. |

## Execution Order

1. Run 9a → 9b → 9c in sequence

## Per Sub-phase Cycle

Each sub-phase follows: Implement → Audit → Ralph (3 iterations) → Validate → Record.

### Validation Commands

```bash
uv run ruff check orchestrator/ --select E,F,W,I
uv run ruff format orchestrator/ --check
uv run python scripts/validate_skills.py
uv run pytest tests/ -q
uvx radon cc orchestrator/ -s -a | grep -E " - [CDEF] "
uvx radon mi orchestrator/ -s | grep -E " - [BCDEF] "
markdownlint .agent_work/ orchestrator/ docs/ --ignore node_modules
```

## Report Files — APPEND ONLY

- EDUCATIONAL_REPORT.md: use `>>` heredoc — never `write`
- AUDIT_REPORT.md: use `>>` heredoc — never `write`
- DECISIONS.md: append new decisions, never overwrite

## Stop Condition

The Deep Determinism project is **complete** when Phase 9 passes all validations, the final audit covers all 9 phases, git status is clean, and the closeout decision is recorded.

When done, update STATUS.md to project_complete and write RESULT.json with status "pass". No NEXT_PROMPT.md is needed after Phase 9.

## Context

Continue from Phase 8. All 374 tests pass. SKILL.md is at 468 lines (under 500). Both schemas updated to 2020-12. MD060 issues in docs/ resolved. CHANGELOG v2.0.0 entry written. 
