# Task: ContextSmith v1.5.1 Audit Remediation

## Objective
Address 5 audit findings from v1.5.1 audit report by modifying shared references and SKILL.md files.

## Scope

- Finding #1: Extract context budget section from SKILL.md to shared reference
- Finding #2: Add ml-heavy phase type to targeted-context-length.md
- Finding #3: Create minimal behavioral contracts for small models
- Finding #4: Parameterize hardcoded 64k context budget in phased-planning.md
- Finding #5: Add tool forecast realism to implementation plan audit checklist

## Constraints

- Target model: Qwen3.6-27B (qwen36)
- Context budget: 60k tokens per phase
- Do NOT modify `shared/behavioral-contracts.md` content - create separate file
- Do NOT append to existing files where a separate file is called for
- Each phase must run validation script and create per-phase commit
- After editing shared/ files, check per-skill copies in skills/*/references/

## Success Criteria

- All 5 audit findings addressed
- `python scripts/validate_skills.py` passes after every phase
- SKILL.md reduced to ~269 lines (from 291)
- All SKILL.md files under 500 lines
- CHANGELOG.md updated with v1.5.2 entry
- Per-phase git commits created
- Task state artifacts updated after each phase
