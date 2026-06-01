# Artifacts: ContextSmith v1.5.1 Audit Remediation

## Created Files
- `shared/minimal-behavioral-contracts.md` - model-specific behavioral contracts for 6 model families

## Modified Files
- `skills/local-model-prompt-engineer/SKILL.md` - extracted lines 113-135 to shared reference (291 -> 269 lines)
- `shared/targeted-context-length.md` - added Phase-Specific Budgets section and Phase Types table
- `shared/behavioral-contracts.md` - added cross-reference to minimal-behavioral-contracts.md
- `shared/phased-planning.md` - replaced hardcoded 64k with {{CONTEXT_BUDGET}} variable
- `CHANGELOG.md` - added v1.5.2 entry

## Commits
- 17ae7b2 - fix: extract context budget section to shared reference (finding #1)
- 4bdf198 - fix: add ml-heavy phase type with 80k budget (finding #2)
- 6770a92 - fix: create minimal behavioral contracts for small models (finding #3)
- 690d811 - fix: parameterize hardcoded context budget in phased planning (finding #4)
- 494e472 - chore: update CHANGELOG for v1.5.2 audit remediation

## Phase 5 Note
Finding #5 (Tool forecast realism) was already addressed in implementation-plan-audit.md - criterion exists in rubric (line 17) and output format table (line 69). No change needed.
