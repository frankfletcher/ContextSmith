# Artifact Manifest Specification

## Purpose

Track active parameters, applied references, and behavioral contracts for generated artifacts (prompts, implementation plans, next-prompts, skills, instruction files). Enables parameter-aware propagation through generation chains so downstream agents know exactly what constraints apply.

Works for both standalone agents and ContextSmith-equipped agents.

## Placement Rules

- Insert as an ATX heading section (`## Artifact Manifest`) immediately after the artifact title
- Do NOT use YAML frontmatter — ATX headings are universally supported by small models
- Place BEFORE any other content or instructions in the generated artifact
- Every generated artifact MUST include this section

## Format

```markdown
# <Artifact Title>

## Artifact Manifest

**type:** prompt | implementation-plan | next-prompt | skill | instruction-file
**version:** 1.0
**chain-of:** root | <parent artifact id or file path>

### Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| `target_model_family` | qwen3 | user-set |
| `context_window_optimized` | true | default |

### References Applied

| Reference | Version | Contract Summary |
|-----------|---------|-----------------|
| `loop-safety` | 1.0 | No identical consecutive tool calls; retry budget of 3 total attempts per action before escalation |

### Behavioral Contracts (Standalone)

> Condensed requirements from above references. For agents without ContextSmith installed.

**Contract name:** One or two sentences of actionable requirements extracted from the reference.

### Custom Contracts (Artifact-Specific)

> Additional requirements specific to this artifact's domain and purpose.
```

## Parameters Table

Track each active parameter with its source value:

| Column | Description |
|--------|-------------|
| Parameter | Name from `shared/control-parameters.md` or custom (prefixed with `custom:`) |
| Value | Active value for this artifact |
| Source | How the value was determined (see Source Values table below) |

### Source Values

| Source | Meaning |
|--------|---------|
| `user-set` | Explicitly provided by the user in this session |
| `inherited` | Copied from parent artifact's manifest without modification |
| `default` | Set to the system default (from SKILL.md default table or control-parameters.md) |
| `narrowed` | Derived from a parent value but constrained for this artifact's scope — must include reason in parentheses, e.g. `narrowed from 64k (per-phase tight context)` |

## References Applied Table

List each reference whose behavioral contracts are embedded in this artifact:

| Column | Description |
|--------|-------------|
| Reference | Short name matching the shared/ filename stem (e.g., `loop-safety`, `phased-planning`) |
| Version | Semantic version of the reference file |
| Contract Summary | One-line summary of what contracts are embedded from this reference |

## Behavioral Contracts Section

Condensed, actionable requirements extracted from each listed reference. Each contract entry is self-contained: 3-7 lines maximum. For agents without ContextSmith installed, these contracts serve as the behavioral specification.

Format: `**Contract Name:** One or two sentences of actionable requirements.`

## Custom Contracts Section

Skills may append domain-specific contracts here based on the artifact's purpose and user requirements. These supplement the canonical contracts from shared references.

---

## Chain Propagation Rules

1. **Inherit all:** Child artifact starts with all parent parameters and references
2. **Narrow with justification:** Child may narrow a parameter (e.g., `context-length 64k -> 32k` for tight-context phases) — must include reason in `source` column
3. **Add relevant refs:** Child may add references relevant to its specific scope
4. **Never widen without justification:** Child cannot increase context-length, relax safety, or remove references from parent unless explicitly justified with a documented reason
5. **Chain tracking:** Every artifact records its `chain-of` parent for provenance

### Inheritance Model

```
Root Prompt (params: mode=guided, context-length=64k, ralph=2)
  |
  +- Implementation Plan
  |   params: inherits all from root
  |   narrowed: context-length -> 32k (per-phase budget)
  |   chain-of: "Root Prompt"
  |   references: adds implementation-plan-audit, test-quality-audit
  |   |
  |   +- Phase 1 NEXT_PROMPT.md
  |   |   params: inherits from plan
  |   |   added: --focus phase-1-specific
  |   |   chain-of: "Implementation Plan"
  |   |
  |   +- Phase 2 NEXT_PROMPT.md
  |       params: inherits from plan
  |       carry-forward: facts from Phase 1 debrief
  |       chain-of: "Implementation Plan"
  |
  +- Generated Skill (SKILL.md)
      params: inherits target-profile, harness from root
      added: skill-specific params (--reference-policy, --metadata)
      chain-of: "Root Prompt"
```

## Artifact Type -> Default References Matrix

| Artifact Type | Always Includes | Conditionally Adds |
|---------------|-----------------|-------------------|
| Prompt (general) | control-parameters, loop-safety | domain-profile (if domain known), targeted-context-length (if context length provided) |
| Implementation Plan | phased-planning, implementation-plan-audit, persistent-task-state, phase-compression | test-quality-audit (if coding work), phase-code-review (if --phase-review enabled) |
| NEXT_PROMPT.md | persistent-task-state, loop-safety, phase-compression | All parent plan references (inherited) |
| Generated Skill | control-parameters, loop-safety, skill-interoperability | upstream-artifact-audit (if migrating), reference-optimization |
| Instruction File (AGENTS.md) | instruction-deduplication, instruction-precedence, loop-safety, git-safety | domain-profiles (per domain), coding-standards (if coding domain) |

---

## Validation Checklist

Verify a manifest is correct by checking:

1. `## Artifact Manifest` section exists with ATX heading
2. `type`, `version`, and `chain-of` metadata are present
3. Parameters table has at least the default parameters for the artifact type
4. All parameter source values are one of: `user-set | inherited | default | narrowed`
5. Narrowed parameters include a justification in parentheses
6. References applied match entries in Behavioral Contracts section
7. Behavioral contracts are 3-7 lines each, actionable (not background)
8. Artifact type matches the default references matrix for its type
9. `chain-of` correctly identifies parent artifact or is `root`
