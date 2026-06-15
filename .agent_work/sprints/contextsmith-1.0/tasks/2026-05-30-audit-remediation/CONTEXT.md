# Context: ContextSmith v1.5.1 Audit Remediation

## File Map
| File | Phase | Action |
| ------ | ------- | -------- |
| `skills/local-model-prompt-engineer/SKILL.md` | 1 | Extract lines 113-135 to shared reference |
| `shared/targeted-context-length.md` | 1, 2 | Add phase-specific budgets, add ml-heavy phase type |
| `shared/minimal-behavioral-contracts.md` | 3 | Create new file |
| `shared/behavioral-contracts.md` | 3 | Add cross-reference only (do not modify content) |
| `shared/phased-planning.md` | 4 | Replace hardcoded 64k with {{CONTEXT_BUDGET}} |
| `shared/implementation-plan-audit.md` | 5 | Add tool forecast realism row |
| `CHANGELOG.md` | 6 | Add v1.5.2 entry |

## Audit Findings Summary

1. **Finding #1 (Medium):** SKILL.md context budget section should be extracted to shared reference
2. **Finding #2 (Medium):** Missing ml-heavy phase type in targeted-context-length.md
3. **Finding #3 (Low):** Need minimal behavioral contracts for small models
4. **Finding #4 (Low):** Hardcoded 64k context budget in phased-planning.md
5. **Finding #5 (Low):** Missing tool forecast realism in implementation plan audit

## Skip Rules

- Do NOT modify `shared/behavioral-contracts.md` content - only add cross-reference
- Do NOT append to existing files where a separate file is called for
- Do NOT skip validation script runs between phases
- Do NOT skip per-phase git commits
- Do NOT skip task state updates after each phase

## Validation Command

```bash
python scripts/validate_skills.py
```

## Branch
`fix_context_budget`
