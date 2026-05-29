# Parameter Narrowing Rules

Specifies when and how child artifacts may narrow inherited parameters from their parent artifact's manifest.

## Core Principle

Child artifacts may narrow (constrain) inherited parameters but MUST NOT widen (relax) them without explicit justification documented in the `source` column.

---

## Allowed Narrowings

A narrowing is permitted when the child artifact operates under a more constrained scope than its parent. The following are common, acceptable narrowings:

| Parameter | Parent Value | Child Value | Justification Pattern |
|-----------|-------------|-------------|----------------------|
| `targeted_context_length` | 64k | 32k | Per-phase tight context budget; each phase must fit in window |
| `targeted_context_length` | 128k | 48k | Sub-artifact has narrower scope than parent plan |
| `ralph_iterations` | 3 | 2 | Child artifact is intermediate; reserve iterations for final output |
| `education_level` | deep | standard | Child artifact is a reference summary, not the primary deliverable |
| `verbosity` | detailed | concise | Child artifact is a status update or debrief, not full report |
| `example_count` | 5 | 2 | Child artifact targets smaller context budget |
| `phase_count` | 20 | 8 | Child plan covers a subset of parent scope (single module vs full project) |

### Narrowing Format in Manifest

```markdown
| Parameter | Value | Source |
|-----------|-------|--------|
| `targeted_context_length` | 32k | narrowed from 64k (per-phase tight context budget) |
| `ralph_iterations` | 2 | narrowed from 3 (intermediate artifact; reserve for final output) |
```

The justification in parentheses MUST state WHY the narrowing is necessary, not just that it occurred.

---

## Forbidden Widenings

The following widenings are NOT permitted without explicit user request or documented exception:

| Parameter | Parent Value | Forbidden Child Value | Reason |
|-----------|-------------|----------------------|--------|
| `targeted_context_length` | 32k | 64k | Would exceed parent's context budget allocation |
| `loop_safety_enabled` | true | false | Cannot relax safety constraints without user approval |
| `phase_review` | deep | standard | Cannot reduce review rigor without documented reason |
| `test_coverage_required` | comprehensive | basic | Weakening test requirements risks undetected regressions |

### Exception Format

If a widening is absolutely necessary, document it with this format:

```markdown
| Parameter | Value | Source |
|-----------|-------|--------|
| `targeted_context_length` | 64k | widened from 32k (EXCEPTION: phase requires loading full file tree; user approved at <timestamp>) |
```

Required elements for exceptions:
1. Label as `EXCEPTION:` in the justification
2. State the specific reason widening is required
3. Reference user approval or documented decision (with timestamp or DECISIONS.md anchor)

---

## Narrowing vs. Chain-of Tracking

Every narrowing creates a provenance trail through the chain:

```
Root Prompt: context-length=128k (user-set)
  -> Implementation Plan: context-length=64k (narrowed from 128k, per-plan budget split)
    -> Phase 1 NEXT_PROMPT.md: context-length=32k (narrowed from 64k, single-phase execution)
```

Each artifact's `chain-of` field points to its parent. Tracing the chain reveals the full narrowing history. If a downstream artifact's behavior is unexpected, follow the chain upward to find where parameters were narrowed.

### Verification Rule

When generating a child artifact:
1. Read the parent's manifest parameters
2. Copy all parameters as `inherited` by default
3. For each parameter you narrow, change source to `narrowed from <old> (<reason>)`
4. For each parameter the user explicitly sets on this child, mark as `user-set`
5. Never remove a parameter from the parent's list without documenting why

---

## Interaction with Artifact Types

Different artifact types have different default narrowing behaviors:

| Artifact Type | Typical Narrowing | Typical Inheritance |
|---------------|-------------------|---------------------|
| Implementation Plan from Prompt | context-length (split across phases), ralph-iterations | mode, target-profile, harness, education-level |
| NEXT_PROMPT.md from Plan | context-length (single-phase budget) | All plan parameters; adds phase-specific focus params |
| Generated Skill from Prompt | ralph-iterations (skills are structural, not iterative) | target-profile, harness, reference-policy |
| Instruction File from Prompt | verbosity (instructions are imperative, concise) | target-profile, loop-safety rules, git-safety rules |

---

## Validation Checklist

When reviewing a child artifact's manifest:

1. All parent parameters appear in the child (inherited, narrowed, or user-set)
2. Narrowed parameters include a justification in parentheses
3. No widenings exist without `EXCEPTION:` label and approval reference
4. `chain-of` correctly identifies the parent artifact
5. Narrowing direction is valid (value moved toward more constrained, not less)
