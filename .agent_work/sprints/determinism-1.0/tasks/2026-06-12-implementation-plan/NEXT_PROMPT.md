# Next Prompt: Phase 5a — Create Orchestrator SKILL.md

## HARD STOP — DO NOT EXECUTE IN CURRENT SESSION

This prompt is queued for the next run. Phase 4 is fully complete (all sub-phases a, b, c, d). Do not execute Phase 5 now.

## Current Status

- Phase: 5a of 6
- State: execute
- Completed: Phases 1-4 — 284 tests passing, full suite green, ruff clean
- Retries remaining: 3

## Pre-Flight: PLAN.md / CHECKLIST.md Sync

Before starting this phase, check that all sub-phases listed in PLAN.md also exist in CHECKLIST.md. If PLAN.md has a sub-phase that CHECKLIST.md is missing, add it to CHECKLIST.md before proceeding. This prevents task gaps like the Phase 4d omission.

## Your Task

Phase 5: Create SKILL.md files for the orchestrator skill-only path and workflow developer.
See `PLAN.md` lines 728-827.

### Sub-phase 5a: Create orchestrator SKILL.md

**Task:** Create the orchestrator skill for skill-only execution.

**Files to read:**

- `.agent_work/ideation/deep_determinism/orchestrator_skill_draft.md`
- `.agent_work/ideation/deep_determinism/orchestrator_as_skill.md`
- `PLAN.md` lines 728-754

**Steps:**

1. Create `skills/contextsmith-orchestrator/` directory
2. Create `skills/contextsmith-orchestrator/SKILL.md` from draft
3. Create `skills/contextsmith-orchestrator/reference_manifest.yml`
4. Add shared references to `skills/contextsmith-orchestrator/references/`
5. Run `python scripts/validate_skills.py` to verify

**Expected outputs:**

- `skills/contextsmith-orchestrator/SKILL.md` — under 300 lines
- `skills/contextsmith-orchestrator/reference_manifest.yml`

## Ralph Loop (Required — 3 Iterations)

Each iteration is one full critique+revise cycle. Do not skip iterations.

**Ralph #1:** Critique implementation. Check for defects, gaps, edge cases. Fix any material issue found. Record what was critiqued and what was fixed.

**Ralph #2:** Re-check after fixes. If no new material defects remain, record as no-op and move to #3.

**Ralph #3:** Final check. If no defects remain, record as no-op.

Each iteration must have a compact log entry in the final output. Do not invent changes to satisfy the loop — only fix material defects.

## Report Files — APPEND ONLY

- EDUCATIONAL_REPORT.md: use `cat >> file << 'REPORT'` — never `write`
- AUDIT_REPORT.md: use `cat >> file << 'AUDIT'` — never `write`
- Never overwrite, never use `>` single redirect. If using edit tool fails, fall back to bash `>>`.

## STOP

Phase 5a ready. Execute only when explicitly instructed.
