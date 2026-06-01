# ContextSmith v1.5.1 Audit Remediation - Implementation Plan

## Overview
Address 5 audit findings (2 medium, 3 low severity) from v1.5.1 audit report. Each phase is a single atomic action with explicit inputs, outputs, and validation.

## Context Budget
- Target model: Qwen3.6-27B (qwen36)
- Budget: 60k tokens per phase
- Mode: guided/deep, education: deep, Ralph loop: 2 iterations

## Phase 0: Baseline Validation
**Objective:** Confirm current state before changes.

**Inputs:**
- `scripts/validate_skills.py`
- `skills/local-model-prompt-engineer/SKILL.md` (291 lines)

**Actions:**
1. Run `python scripts/validate_skills.py` - capture output
2. Record current SKILL.md line count: `wc -l skills/local-model-prompt-engineer/SKILL.md`
3. Record current git status: `git status --short`

**Outputs:**
- Validation script output (must pass)
- Line count confirmation (291 lines)
- Clean git status

**Validation:** Validation script passes, line count matches 291.

**Context Contract:**
```yaml
context_contract:
  required_files:
    - scripts/validate_skills.py
    - skills/local-model-prompt-engineer/SKILL.md
  required_knowledge:
    - validation script expects passing output
    - SKILL.md is 291 lines
  estimated_tokens: 8000
```

**Phase Debrief Template:**
- What changed: baseline captured
- What didn't: N/A
- Next phase: Phase 1

---

## Phase 1: Extract Context Budget Section (Finding #1)
**Objective:** Extract lines 113-135 from SKILL.md into `shared/targeted-context-length.md`, reducing SKILL.md to ~269 lines.

**Inputs:**
- `skills/local-model-prompt-engineer/SKILL.md` lines 113-135 (23 lines)
- `shared/targeted-context-length.md`

**Actions:**
1. Read SKILL.md lines 113-135 to extract context budget section
2. Append extracted content to `shared/targeted-context-length.md` (add as new "Phase-Specific Budgets" subsection)
3. Replace lines 113-135 in SKILL.md with single reference line: `> Context budgets: see shared/targeted-context-length.md`
4. Run `python scripts/validate_skills.py`
5. Verify SKILL.md line count: `wc -l skills/local-model-prompt-engineer/SKILL.md` (expect ~269)
6. Commit: `git add -A && git commit -m "fix: extract context budget section to shared reference (finding #1)"`

**Outputs:**
- Updated `shared/targeted-context-length.md` with phase-specific budgets
- Updated SKILL.md with reference link (~269 lines)
- Passing validation
- Per-phase git commit

**Validation:** SKILL.md <= 269 lines, validation passes, git commit created.

**Context Contract:**
```yaml
context_contract:
  required_files:
    - skills/local-model-prompt-engineer/SKILL.md
    - shared/targeted-context-length.md
  required_knowledge:
    - Lines 113-135 contain context budget guidance
    - Target: 291 - 23 + 1 = 269 lines
  estimated_tokens: 12000
```

**Phase Debrief Template:**
- What changed: 23 lines extracted, 1 reference added
- What didn't: rest of SKILL.md unchanged
- Next phase: Phase 2

---

## Phase 2: Add ML-Heavy Phase Type (Finding #2)
**Objective:** Add "ml-heavy" phase type to `shared/targeted-context-length.md` with 80k token budget.

**Inputs:**
- `shared/targeted-context-length.md` (updated in Phase 1)

**Actions:**
1. Read `shared/targeted-context-length.md` to find phase types table
2. Add "ml-heavy" row: `| ml-heavy | 80k | Data loading, model training, evaluation |`
3. Run `python scripts/validate_skills.py`
4. Commit: `git add -A && git commit -m "fix: add ml-heavy phase type with 80k budget (finding #2)"`

**Outputs:**
- Updated `shared/targeted-context-length.md` with ml-heavy phase type
- Passing validation
- Per-phase git commit

**Validation:** ml-heavy row present in phase types table, validation passes.

**Context Contract:**
```yaml
context_contract:
  required_files:
    - shared/targeted-context-length.md
  required_knowledge:
    - Phase types table format: | name | budget | description |
    - ml-heavy budget: 80k tokens
  estimated_tokens: 6000
```

**Phase Debrief Template:**
- What changed: ml-heavy row added to phase types table
- What didn't: other phase types unchanged
- Next phase: Phase 3

---

## Phase 3: Create Minimal Behavioral Contracts (Finding #3)
**Objective:** Create `shared/minimal-behavioral-contracts.md` with model-specific behavioral guidance. DO NOT append to `shared/behavioral-contracts.md`.

**Inputs:**
- `shared/behavioral-contracts.md` (read-only, do not modify)

**Actions:**
1. Create `shared/minimal-behavioral-contracts.md` with model-specific behavioral guidance:
   - Qwen3.6: concise output, no preamble/postamble, direct answers
   - Llama 3.1: structured outputs, explicit formatting
   - Mistral: code-focused, minimal prose
2. Add cross-reference in `shared/behavioral-contracts.md`: `> Model-specific contracts: see shared/minimal-behavioral-contracts.md`
3. Run `python scripts/validate_skills.py`
4. Commit: `git add -A && git commit -m "fix: create minimal behavioral contracts for small models (finding #3)"`

**Outputs:**
- New `shared/minimal-behavioral-contracts.md`
- Updated `shared/behavioral-contracts.md` with cross-reference
- Passing validation
- Per-phase git commit

**Validation:** New file exists, cross-reference present, validation passes.

**Context Contract:**
```yaml
context_contract:
  required_files:
    - shared/behavioral-contracts.md
  required_knowledge:
    - Model-specific behavioral patterns for Qwen3.6, Llama 3.1, Mistral
    - behavioral-contracts.md is read-only; create separate file
  estimated_tokens: 10000
```

**Phase Debrief Template:**
- What changed: new minimal contracts file created
- What didn't: behavioral-contracts.md content unchanged (only cross-reference added)
- Next phase: Phase 4

---

## Phase 4: Parameterize Hardcoded Context Budget (Finding #4)
**Objective:** Replace hardcoded "64k" in `shared/phased-planning.md` with configurable `{{CONTEXT_BUDGET}}` variable.

**Inputs:**
- `shared/phased-planning.md`

**Actions:**
1. Read `shared/phased-planning.md` to find hardcoded "64k" references
2. Replace all instances with `{{CONTEXT_BUDGET}}` (default: 64k tokens)
3. Add comment before each replacement: `<!-- CONTEXT_BUDGET: Override per-project. Default: 64k tokens -->`
4. Run `python scripts/validate_skills.py`
5. Commit: `git add -A && git commit -m "fix: parameterize hardcoded context budget in phased planning (finding #4)"`

**Outputs:**
- Updated `shared/phased-planning.md` with `{{CONTEXT_BUDGET}}` variable
- Passing validation
- Per-phase git commit

**Validation:** No hardcoded "64k" remains, `{{CONTEXT_BUDGET}}` present with comment, validation passes.

**Context Contract:**
```yaml
context_contract:
  required_files:
    - shared/phased-planning.md
  required_knowledge:
    - Hardcoded "64k" appears in phased planning guidance
    - Replace with {{CONTEXT_BUDGET}} variable
  estimated_tokens: 8000
```

**Phase Debrief Template:**
- What changed: hardcoded 64k replaced with configurable variable
- What didn't: other phased planning content unchanged
- Next phase: Phase 5

---

## Phase 5: Add Tool Forecast Realism to Audit Checklist (Finding #5)
**Objective:** Add "Tool forecast realism" row to `shared/implementation-plan-audit.md` checklist.

**Inputs:**
- `shared/implementation-plan-audit.md`

**Actions:**
1. Read `shared/implementation-plan-audit.md` to find checklist table
2. Add new row: `| Tool forecast realism | Each phase specifies exact tools, commands, and expected outputs |`
3. Run `python scripts/validate_skills.py`
4. Commit: `git add -A && git commit -m "fix: add tool forecast realism to implementation plan audit (finding #5)"`

**Outputs:**
- Updated `shared/implementation-plan-audit.md` with new checklist row
- Passing validation
- Per-phase git commit

**Validation:** New row present in checklist, validation passes.

**Context Contract:**
```yaml
context_contract:
  required_files:
    - shared/implementation-plan-audit.md
  required_knowledge:
    - Checklist table format: | criterion | description |
    - Tool forecast realism requires exact tool/command/output specification
  estimated_tokens: 6000
```

**Phase Debrief Template:**
- What changed: new checklist row added
- What didn't: other checklist items unchanged
- Next phase: Phase 6

---

## Phase 6: Update CHANGELOG and Final Validation
**Objective:** Document all changes in CHANGELOG.md and run final validation.

**Inputs:**
- `CHANGELOG.md`
- All previous phase outputs

**Actions:**
1. Read `CHANGELOG.md` to find current version section
2. Add v1.5.2 entry with all 5 fixes:
   ```
   ## v1.5.2 (2026-05-30)
   ### Fixed
   - Extract context budget section from SKILL.md to shared reference (reduces to ~269 lines)
   - Add ml-heavy phase type with 80k token budget to targeted-context-length.md
   - Create minimal behavioral contracts for small model compliance
   - Parameterize hardcoded 64k context budget in phased-planning.md
   - Add tool forecast realism row to implementation plan audit checklist
   ```
3. Run `python scripts/validate_skills.py`
4. Verify all SKILL.md files are under 500 lines
5. Commit: `git add -A && git commit -m "chore: update CHANGELOG for v1.5.2 audit remediation"`

**Outputs:**
- Updated `CHANGELOG.md` with v1.5.2 entry
- Passing validation
- All SKILL.md files under 500 lines
- Final per-phase git commit

**Validation:** CHANGELOG updated, validation passes, all SKILL.md files <= 500 lines.

**Context Contract:**
```yaml
context_contract:
  required_files:
    - CHANGELOG.md
    - scripts/validate_skills.py
  required_knowledge:
    - CHANGELOG format: ## version (date) with ### Fixed/Added/Changed sections
    - v1.5.2 is next patch after v1.5.1
  estimated_tokens: 8000
```

**Phase Debrief Template:**
- What changed: CHANGELOG updated with v1.5.2
- What didn't: previous phases unchanged
- Next phase: complete

---

## Self-Audit (Honest Grading)
| Criterion | Grade | Justification |
|-----------|-------|---------------|
| Task-state integration | B | Phase debriefs are templates, not enforced. Executor must remember to fill them. |
| Handoff quality | B | Context contracts are explicit but executor needs to track which files changed per phase. |
| Tool forecast realism | B | Commands are specified but validation script output format isn't forecasted. |
| Phase atomicity | A | Each phase is a single objective with clear inputs/outputs. |
| Context budget compliance | A | All phases under 60k tokens. Largest is Phase 1 at 12k. |
| Validation completeness | A | Each phase includes validation script run and per-phase commit. |

---

## Fresh Session Guidance
If resuming in a new session:
1. Read this PLAN.md first
2. Read `.agent_work/sprints/contextsmith-1.0/tasks/2026-05-30-audit-remediation/STATUS.md` for current phase
3. Read `.agent_work/sprints/contextsmith-1.0/tasks/2026-05-30-audit-remediation/PHASE_LOG.md` for completed phases
4. Continue from the next incomplete phase
5. Do NOT re-read completed phases unless their outputs are missing

---

## Shared Reference Sync Check
After editing any `shared/` file, check whether per-skill copies in `skills/*/references/` need updating:
- `skills/local-model-prompt-engineer/references/targeted-context-length.md` - update if Phase 2 changes
- `skills/local-model-prompt-engineer/references/behavioral-contracts.md` - update if Phase 3 changes
- `skills/local-model-prompt-engineer/references/phased-planning.md` - update if Phase 4 changes
- `skills/local-model-prompt-engineer/references/implementation-plan-audit.md` - update if Phase 5 changes

If a per-skill copy exists and the shared file changed, update the copy to match.

---

## Task State Updates
After completing each phase, update:
1. `.agent_work/sprints/contextsmith-1.0/tasks/2026-05-30-audit-remediation/STATUS.md` - mark phase complete
2. `.agent_work/sprints/contextsmith-1.0/tasks/2026-05-30-audit-remediation/PHASE_LOG.md` - add phase entry
3. `.agent_work/sprints/contextsmith-1.0/tasks/2026-05-30-audit-remediation/ARTIFACTS.md` - list created/modified files
