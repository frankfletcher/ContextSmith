## Gate: .phase_gate

This prompt is queued for the next run. Do NOT execute until
`.agent_work/sprints/determinism-1.0/tasks/2026-06-12-implementation-plan/.phase_gate` exists.
If the file is missing, stop and report "Phase gate not set. Awaiting human instruction to proceed."

# Next Prompt: Phase 7 — Integration and Testing

## Current Status

- Phase: 7 of 9 (3 sub-phases: 7a, 7b, 7c)
- State: init
- Completed: Phases 1-6 — all schemas, core module, adapters, validators, 2 skills, quality fixes, collapse + determinism hardening

## Pre-Flight: PLAN.md / CHECKLIST.md Sync

Before starting, check that all sub-phases listed in PLAN.md Phase 7 also exist in CHECKLIST.md. If PLAN.md has a sub-phase that CHECKLIST.md is missing, add it to CHECKLIST.md before proceeding.

## Your Task

Execute **all** of Phase 7 (sub-phases 7a, 7b, 7c). This is a full-phase execution. The phase is complete when all 3 sub-phases are done and validated.

See `PLAN.md` Phase 7 for full detail on each sub-phase. Key additions from Phase 6 review:

| Sub-phase | Task | Key files |
|-----------|------|-----------|
| **7a** | Extend unit tests — **must add dedicated tests for 10 determinism features** (exit codes 0-5, validation_mode, checkpoint_before_run, pre-dispatch counter, RESULT.json fallback, append validation, model_pin, agent-evidence rules). Create `tests/test_orchestrator_determinism.py`. | tests/ |
| **7b** | Extend integration tests — add exit code 3/4/5 propagation, append-only file snapshot+repair, pre-dispatch marker detection | tests/test_orchestrator_integration.py |
| **7c** | Update validation script, document SKILL.md file trim opportunity for Phase 8 | scripts/validate_skills.py |

## Execution Order

1. Run 7a → 7b → 7c in sequence (7c is last since it validates the final state)

## Per Sub-phase Cycle

Each sub-phase follows: Implement → Audit → Ralph (3 iterations) → Validate → Record.

### Validation Commands

For each sub-phase, run:
- `uv run ruff check orchestrator/ --select E,F,W,I`
- `uv run python scripts/validate_skills.py`
- `uv run pytest tests/ -q`
- `uv run ruff format orchestrator/ --check`

## Report Files — APPEND ONLY

- EDUCATIONAL_REPORT.md: use `>>` heredoc — never `write`
- AUDIT_REPORT.md: use `>>` heredoc — never `write`
- DECISIONS.md: append new decisions, never overwrite

## Stop Condition

Phase 7 is complete when all 3 sub-phases pass, test coverage is extended (including dedicated tests for 10 determinism features), validation script is current, and all existing tests still pass. Phase 8 (Documentation and Polish) and Phase 9 (Final Validation and Lock) are defined in PLAN.md.

When done, update STATUS.md to phase_7_complete and write NEXT_PROMPT.md for Phase 8.

## Context

Continue from previous phase. All Phase 6 artifacts are in place: exit codes 0-5, configurable validation modes, pre-dispatch checkpoints, per-state timeout_s/model_pin/ralph_max_cycles, RESULT.json fallback, append-only auto-repair, documented agent-evidence rules.
