# Checklist: ContextSmith v1.5.1 Audit Remediation

## Phase 0: Baseline Validation

- [ ] Validation script passes
- [ ] SKILL.md line count is 291
- [ ] Git status is clean

## Phase 1: Extract Context Budget Section

- [ ] Lines 113-135 extracted from SKILL.md
- [ ] Content appended to `shared/targeted-context-length.md`
- [ ] SKILL.md has reference link to shared file
- [ ] SKILL.md line count is ~269
- [ ] Validation script passes
- [ ] Per-phase commit created

## Phase 2: Add ML-Heavy Phase Type

- [ ] ml-heavy row added to phase types table
- [ ] Budget is 80k tokens
- [ ] Validation script passes
- [ ] Per-phase commit created

## Phase 3: Create Minimal Behavioral Contracts

- [ ] `shared/minimal-behavioral-contracts.md` created
- [ ] Qwen3.6, Llama 3.1, Mistral guidance included
- [ ] Cross-reference added to `shared/behavioral-contracts.md`
- [ ] Validation script passes
- [ ] Per-phase commit created

## Phase 4: Parameterize Context Budget

- [ ] All hardcoded "64k" replaced with `{{CONTEXT_BUDGET}}`
- [ ] Comments added before each replacement
- [ ] No hardcoded "64k" remains
- [ ] Validation script passes
- [ ] Per-phase commit created

## Phase 5: Add Tool Forecast Realism

- [ ] New row added to checklist table
- [ ] Row specifies exact tools, commands, outputs
- [ ] Validation script passes
- [ ] Per-phase commit created

## Phase 6: CHANGELOG and Final Validation

- [ ] v1.5.2 entry added to CHANGELOG.md
- [ ] All 5 fixes documented
- [ ] Validation script passes
- [ ] All SKILL.md files under 500 lines
- [ ] Per-phase commit created

## Shared Reference Sync

- [ ] Per-skill copies in `skills/*/references/` checked and updated if needed
