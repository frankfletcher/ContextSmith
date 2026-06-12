# Token Optimization: Skill Startup & Invocation Load

Date: 2026-06-05

## Problem

Two separate concerns:
1. **Startup cost** — when the user first asks a question, opencode loads system prompt, tool schemas, AGENTS.md, custom rules, and skill descriptions. For small models, this leaves little context buffer.
2. **Invocation cost** — when a ContextSmith skill is invoked, the full SKILL.md loads. For small models, `contextsmith-run` alone is ~4,000 tokens.

## What We Can't Control

Opencode's system prompt and tool schemas are the dominant cost (~15-16k tokens). We can't reduce this.

## What We Can Control

### Startup Cost (configurable files)

| Component | Bytes | Est. Tokens |
|-----------|------:|------------:|
| AGENTS.md | 7,063 | ~690 |
| Skill descriptions (7 skills) | ~ | ~380 |
| CLAUDE.md | 226 | ~20 |
| custom_rules.md | 258 | ~20 |
| **Total** | **~7.5 KB** | **~1,110** |

### Invocation Cost (installed SKILL.md files)

| Skill | Bytes | Est. Tokens |
|-------|------:|------------:|
| contextsmith-run | 15,238 | ~4,000 |
| contextsmith-prompt-engineer | 14,313 | ~3,800 |
| contextsmith-instruction-engineer | 13,315 | ~3,500 |
| contextsmith-skill-engineer | 12,453 | ~3,300 |
| contextsmith-skill-migrator | 8,040 | ~2,100 |
| contextsmith-agent-evaluator | 7,489 | ~2,000 |
| contextsmith | 3,711 | ~1,000 |
| **Total** | **74,559** | **~19,700** |

## Issue 1: Cross-Skill Duplication (biggest invocation win)

These sections are copy-pasted nearly verbatim across multiple skills. When any skill is invoked, the agent pays for all the inline boilerplate:

| Section | Skills | Approx. lines |
|---------|--------:|------:|
| `## Help Mode` | 7 | ~21 |
| `## Control Parameter Parsing` | 5 | ~20 |
| `## Model Capability and Planner/Executor Profiles` | 5 | ~25 |
| `## Education Level and Artifact Verbosity` | 5 | ~20 |
| `## Run Configuration Preview` | 5 | ~20 |
| `## Documentation Quality` | 6 | ~18 |
| `## Implementation Plan, Test, and Phase Review Audits` | 3 | ~45 |
| `## Quick Use` | 6 | ~36 |
| `## Priority Order` | 3 | ~21 |
| `## Artifact Manifest Propagation` | 3 | ~30 |
| Default parameter tables | 5 | ~40 |
| **Total** | | **~296** |

### Mechanism: Defer from SKILL.md to references

**Before**: Boilerplate content lives inline in each SKILL.md → when the skill is invoked, the agent pays for all the inline content immediately.

**After**: Boilerplate content moves to `references/shared-boilerplate.md` → the agent only loads the reference if it needs those details. SKILL.md stays lean.

The savings come from moving content from "always loaded on invocation" to "loaded on demand", not from eliminating duplicate copies across skills. Each skill still has its own `references/shared-boilerplate.md` on disk.

### Recommendation

Create a `references/shared-boilerplate.md` in each skill's `references/` directory containing these sections. Each SKILL.md replaces the inline copies with a single line:

```
For help mode, control parameters, model capability profiles, education level, run configuration preview, and documentation quality, load `references/shared-boilerplate.md`.
```

This moves ~300 lines from invocation cost to on-demand loading.

## Issue 2: Execution-Only Content Inline

Content that is only needed for specific workflow steps, but is loaded on every invocation because it's inline in SKILL.md. The same pattern will apply to baseline workflow configs: keep the authoritative YAML/JSON separate so the agent only loads it when a workflow actually needs to execute or validate it.

### contextsmith (meta-skill) — ~85 lines

The entire Wizard Mode section (Q1/Q2/Q3 tables, confirmation template, defaults table) only fires when the wizard is triggered. Move to `references/wizard-mode.md`.

### contextsmith-run (340 lines) — ~150 lines

The largest skill. Much of the detail already exists in its own references:

- Execution Contract YAML example (lines 131-146) → `references/execution-contract.md` already exists
- Validation Gate levels table (lines 225-233) → move to reference
- Evidence Ledger details (lines 271-285) → `references/evidence-ledger.md` already exists
- Task-State Execution file list + details (lines 197-215) → `references/task-state-execution.md` already exists
- Interaction Modes table (lines 117-124) → `references/interaction-modes.md` already exists
- Failure Handling (lines 299-309) → move to reference
- Local-Model Execution Rules (lines 93-105) → `references/small-model-atomicity.md` already exists

### contextsmith-prompt-engineer — ~80 lines

- "Build the Prompt Package" template (lines 192-208) → move to reference
- "Implementation Plan, Test, and Phase Review Audits" (lines 99-116) → shared boilerplate
- "Artifact Manifest Propagation" details (lines 280-288) → move to reference

### contextsmith-instruction-engineer — ~80 lines

- AGENTS.md template (lines 155-175) → move to reference
- Task-state file descriptions (lines 183-193) → consolidate with shared task-state reference
- "Implementation Plan, Test, and Phase Review Audits" (lines 93-106) → shared boilerplate

### contextsmith-skill-engineer — ~50 lines

- "Add Context, Phase, and Memory Support" detail (lines 153-168) → move to reference
- "Artifact Manifest Propagation" (lines 211-219) → move to reference

### contextsmith-skill-migrator — ~40 lines

- Shared boilerplate sections (help, control params, model capability, education level, run config preview, documentation quality)

### contextsmith-agent-evaluator — ~30 lines

- Shared boilerplate sections

## Issue 3: Frontmatter Descriptions Oversized

Descriptions are loaded on startup for every skill. They currently try to enumerate every possible trigger phrase.

| Skill | Words |
|-------|------:|
| contextsmith-prompt-engineer | 71 |
| contextsmith-skill-engineer | 71 |
| contextsmith-agent-evaluator | 72 |
| contextsmith-instruction-engineer | 71 |
| contextsmith-skill-migrator | 57 |
| contextsmith-run | 54 |
| contextsmith | 50 |

Trim to ~25-30 words each. Focus on core purpose and 2-3 key triggers. The full trigger list lives in the SKILL.md body, which only loads when the skill is selected.

## Issue 4: Structural Problems

1. **Section ordering**: `contextsmith-skill-engineer` and `contextsmith-instruction-engineer` both have `## Parameters and Artifact Manifest` before the `# Title` H1. The H1 should come first.

2. **Step numbering**: `contextsmith-prompt-engineer` workflow goes 1, 0, 2, 3, 4, 5, 6, 7, 8 (step 0 after step 1).

3. **Ralph default inconsistency**: Parameter tables say `--ralph 1` but workflow sections in several skills say `default 2`.

4. **Education-level default inconsistency**: `contextsmith-run` uses `guided` as default; other skills use `deep`.

## Issue 5: Reference Directory Bloat (secondary)

Each skill carries ~40 reference files totaling ~2,500 lines. Many references are identical copies across skills (`documentation-quality.md`, `control-parameters-core.md`, `loop-safety.md`, etc.). This doesn't affect startup cost but increases disk usage and maintenance burden.

**Not a priority** — only relevant if we want to reduce the installed package size. The `shared/` directory already serves as the canonical source; per-skill copies exist for standalone installation.

## User Documentation Strategy

SKILL.md serves two audiences: the agent (needs lean instructions) and the human user (needs education). Moving everything to references hurts user readability.

**Option: README.md per skill** — opencode only loads `SKILL.md`, not `README.md`. A `README.md` in each skill directory would be invisible to the agent (zero token cost) but available for humans to read. SKILL.md can link to it: "For detailed usage examples, see `README.md`."

Risk: the agent might follow the link and load README.md, adding tokens. Mitigation: use language like "For human readers, see `README.md`" to discourage the agent from loading it.

## Estimated Impact

### Invocation Cost Reduction

| Change | Lines saved per invocation |
|--------|------------------------:|
| Extract boilerplate to references | ~296 |
| Move wizard mode to reference | ~85 |
| Slim contextsmith-run | ~150 |
| Slim prompt-engineer | ~80 |
| Slim instruction-engineer | ~80 |
| Slim skill-engineer | ~50 |
| Slim skill-migrator | ~40 |
| Slim agent-evaluator | ~30 |
| **Total** | **~811 lines** |

**Target: ~785 lines / ~42 KB** instead of 1,596 lines / 86 KB. Approximately 51% reduction in invocation token load.

### Startup Cost Reduction

| Change | Tokens saved |
|--------|------------:|
| Trim frontmatter descriptions | ~180 |
| Slim AGENTS.md | ~200 |
| **Total** | **~380** |

**Target: ~730 tokens** instead of ~1,110. Approximately 34% reduction in startup token load.

## Priority Order

1. **Extract shared boilerplate to references** — highest ROI, defers ~300 lines from invocation to on-demand
2. **Move wizard mode to reference** — 85 lines, zero behavioral change
3. **Slim contextsmith-run** — biggest single skill, detail already in own references
4. **Fix structural issues** — section ordering, step numbering, Ralph default inconsistency
5. **Trim frontmatter descriptions** — ~180 token startup savings, cleaner trigger matching
6. **Slim remaining skills** — prompt-engineer, instruction-engineer, skill-engineer
7. **Slim AGENTS.md** — ~200 token startup savings
