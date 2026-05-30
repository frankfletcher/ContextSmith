# ContextSmith v1.5.1 Audit Report — `fix_context_budget` branch

**Date:** 2026-05-30
**Auditor:** local-model-agent-evaluator skill
**Target profile:** generic-local (Qwen3.6-27B, Llama, Mistral class)
**Scope:** 5 SKILL.md files, 7 changed shared references, AGENTS.md

---

## Summary Grade: B+

The v1.5.1 context-budget changes are a strong, coherent addition that meaningfully improves context-risk management across the package. The forecast-then-compact pattern is well-designed and consistently propagated. Primary remaining risks are instruction bloat in the prompt-engineer SKILL.md and the absence of explicit data-science/ML safeguard content in the new context-budget references.

---

## Strengths

- **Forecast-then-compact is concrete and testable**: `context_contract` YAML blocks in `phased-planning.md` give models explicit budgets (usable_phase_budget, tool_output_reserve, expected_tool_calls) rather than vague guidance. Small models can follow these mechanically.
- **Consistent propagation**: The same compaction triggers appear across `phased-planning.md`, `phase-compression.md`, `small-context-workflows.md`, and `behavioral-contracts.md`. No contradictions detected.
- **Parameter narrowing rules are production-ready**: `parameter-narrowing-rules.md` now covers all 5 context tiers with executable-phase-budget narrowings. The chain-of-tracking provenance trail is a strong anti-hallucination measure.
- **Behavioral contracts are self-contained**: `behavioral-contracts.md` summaries are 3-7 lines each, embeddable in generated artifacts without requiring ContextSmith installed. Good for standalone skill operation.
- **Blocking conditions are explicit**: `implementation-plan-audit.md` Blocking Conditions section gives clear "refine before execution" triggers. Models won't silently proceed past context overflow.
- **AGENTS.md `.agent_work/` override is correct**: Prevents external skills from scattering artifacts into `docs/`. Good file-safety boundary.
- **Loop safety is comprehensive**: AGENTS.md 10-rule loop-safety section + behavioral-contracts retry budget (max 1 retry per action, max 3 total) + BREAK_LOOP sentinel. No-chain-of-thought is enforced across all 5 skills.
- **Fresh-session pattern is well-specified**: `small-context-workflows.md` lists exactly which 6-7 files to load on resume. Prevents context bloat from full-history reloads.

---

## Weaknesses / Risks

| Severity | Issue |
|----------|-------|
| **Medium** | `local-model-prompt-engineer/SKILL.md` is 291 lines — the largest skill. For a 32k target with system prompt overhead, this consumes ~3-4% of usable context. Consider progressive disclosure: move the persistent-task-state contract (lines 113-135) to a reference file. |
| **Medium** | No data-science/ML-specific context-budget guidance in new references. `targeted-context-length.md` and `phase-compression.md` are coding-centric. ML phases (training runs, eval sweeps, artifact uploads) have different tool-output profiles that aren't addressed. |
| **Low** | `behavioral-contracts.md` is 105 lines. When embedded in a generated artifact alongside other contracts, it adds meaningful token cost. Consider a "minimal contracts" subset for tight-context artifacts. |
| **Low** | The `context_contract` YAML example in `phased-planning.md` hardcodes `targeted_context_length: 64k`. A model might copy this verbatim for a 32k-target phase. Should be parameterized or include a comment to adjust. |
| **Low** | `implementation-plan-audit.md` output format table doesn't include the new "Tool forecast realism" row in the template, though it's in the rubric. Minor inconsistency. |

---

## A-F Rubric

| Dimension | Grade | Reason | Recommended Fix |
|-----------|-------|--------|-----------------|
| Small-model atomicity | A | Instructions are literal, single-objective, with explicit stop conditions. context_contract is mechanical. | None. |
| Instruction clarity | A | No ambiguous language. Imperative, testable, with concrete thresholds (50%, 3-7 files, 12k-16k budgets). | None. |
| Output contract quality | A | Required output sections are explicit per skill. Artifact manifest propagation is well-defined. | None. |
| Context strategy | A | Forecast-then-compact, tier-based budgets, fresh-session pattern, tool-output reserves. Comprehensive. | None. |
| Targeted context fit | A- | All 5 tiers covered with specific guidance. Minor: context_contract example hardcodes 64k. | Parameterize the example or add adjustment note. |
| Assumption control | A | Parameter defaults are explicit. Narrowing requires justification. Widening requires EXCEPTION label + approval. | None. |
| Domain fit | B+ | Coding domain is well-covered. ML/data-science context-budget patterns are missing. | Add ML-specific tool-output reserve guidance to targeted-context-length.md. |
| Loop safety | A | 10-rule AGENTS.md section, retry budgets, BREAK_LOOP sentinel, no-identical-calls rule. | None. |
| Git/file safety | A | Approval gates for destructive ops, .agent_work/ boundaries, .gitignore hygiene, no-edit-outside-workspace. | None. |
| Validation strength | A | implementation-plan-audit rubric, blocking conditions, test-quality-audit integration, 12-step closeout. | None. |
| Skill interoperability | A | upstream-artifact-audit, 6-tier classification, workflow collision detection, bridge artifacts. | None. |
| Bloat / cognitive load | B- | prompt-engineer SKILL.md at 291 lines is the heaviest. behavioral-contracts.md at 105 lines adds cost when embedded. | Move prompt-engineer task-state contract to reference. Add minimal-contracts subset. |

---

## Loop / Git / Context Safety

- **Loop safety**: Excellent. AGENTS.md 10 rules + behavioral-contracts retry budget + no-identical-consecutive-calls. Covers the failure modes that cause local model instability.
- **Git safety**: Complete. Destructive operation approval gates, safe inspection whitelist, pre-edit status check, no-overwrite-user-changes rule.
- **Context safety**: The new v1.5.1 changes directly address this. Forecast-then-compact with 50% exceedance trigger, tier-based executable budgets, fresh-session preference for tool-heavy work, and do-not-carry-forward notes. This is the strongest dimension of the package.

---

## Domain-Specific Risks

- **Data science/ML**: The new context-budget references are coding-centric. ML training phases produce different tool-output profiles (long stdout, large artifact files, batch eval logs) that don't fit the current reserve percentages. Recommend adding an `ml-heavy` phase type to `phased-planning.md` context_contract with adjusted reserves (e.g., 60-75% for training output).
- **No other domain-specific gaps detected** for the scope of this change.

---

## Duplicate or Conflicting Instructions

No conflicts detected. The same compaction triggers appear in 4 files but they're consistent, not contradictory. This is intentional redundancy for standalone skill operation (each shared reference must work independently when copied to per-skill `references/`).

---

## High-Risk Issues

None. The changes are additive, backward-compatible, and well-integrated.

---

## Suggested Next Action

1. **Prompt engineering pass** on `local-model-prompt-engineer/SKILL.md` to reduce from 291 lines via progressive disclosure (move persistent-task-state contract to `references/persistent-task-state-contract.md`).
2. **Add ML-specific context-budget guidance** to `shared/targeted-context-length.md` — an `ml-heavy` phase type with 60-75% tool-output reserve.
3. **Parameterize the context_contract example** in `shared/phased-planning.md` to use the user's targeted_context_length rather than hardcoding 64k.
4. **Add "Tool forecast realism" row** to the implementation-plan-audit output format table for consistency.
5. **Consider a minimal-contracts subset** in `behavioral-contracts.md` for tight-context artifacts where the full 105-line file is too expensive to embed.

Downstream skill: `local-model-prompt-engineer` for the SKILL.md size reduction, then `local-model-agent-evaluator` for a follow-up verification audit.
