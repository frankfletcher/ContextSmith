---
name: local-model-skill-engineer
description: Create, convert, improve, audit, and package SKILL.md-based agent skills for local/open-weight language models. Use when building a new skill, adapting an existing skill for smaller/local models, preserving source skill behavior while rewriting it, adding model profiles, optimizing references, adding loop safety, Git/file safety, context-aware workflows, persistent task state, subagent delegation, Ralph-loop iteration, engineering metadata, semantic diff validation, targeted context length control, upstream artifact audits, skill interoperability handling, or skill-auditor-style quality checks.
metadata:
  version: "1.7.1"
  package: ContextSmith
  target: local-open-weight-models
---

# Local Model Skill Engineer

Create, convert, improve, and audit SKILL.md-based skills for local/open-weight models.


## Help Mode

If the user invokes this skill with `help`, `describe`, `examples`, `modes`, `parameters`, `quickstart`, or CLI-style equivalents such as `--help`, do not run the normal workflow.

Return the requested usage guidance from `references/help.md` and `references/help-mode.md`.

## Control Parameter Parsing

Accept both natural-language controls and CLI-style flags. Use `references/control-parameters.md` for parsing rules.

Examples:

```bash
--mode deep --target-profile qwen36 --context-length 32k --domain coding --harness opencode --ralph 2 --output project-local --no-apply
```

When CLI flags and prose conflict, prefer explicit current-user prose or ask one concise clarification question if the intended priority is unclear.

## Priority Order

1. Preserve the source skill's behavioral contract.
2. Identify target model/profile, harness, domain, context risk, and side-effect risk.
3. Make instructions literal, atomic, testable, and small-model-friendly.
4. Do not add exposed chain-of-thought.
5. Optimize references when they are part of the skill contract.
6. Add loop/Git/file/context/persistence/subagent safeguards only when relevant and not already covered.
7. Validate mechanically and semantically; teach the user what changed.

## Clarification Policy

Use `references/interaction-modes.md`. Ask only when blocked or when the answer materially changes target profile, source path, output format, side effects, permission boundaries, validation, or output location. Otherwise proceed with stated assumptions.

## Targeted Context Length

When the user provides a targeted context length, use `references/targeted-context-length.md`. The context target must affect `SKILL.md` size, reference splitting, instruction atomicity, example count, phase granularity, and report verbosity.

## Skill Interoperability

When another skill, optimizer, scaffold, or planner contributed requirements, specs, plans, or workflow artifacts, load `references/skill-interoperability.md` and `references/upstream-artifact-audit.md`.

Do not preserve unsupported upstream additions. Do not replace valid domain-specific workflows unless they conflict with safety, project evidence, or local-model reliability. If workflows collide, preserve the existing workflow in YOLO mode and add only missing safeguards; in guided/review-gate mode, ask whether to use, merge, replace, or bridge workflows.



## Model Capability and Planner/Executor Profiles

When the user provides `--target-capability`, `--planner-profile`, or `--executor-profile`, load `references/model-capability-tiers.md` and `references/planner-executor-workflows.md`.

Use stronger/planner profiles for planning, audits, architecture, test strategy, and final review. Use smaller/executor profiles for atomic phase execution when the plan and task state are explicit.



## Education Level and Artifact Verbosity

If the user provides `--education-level` or `--artifact-verbosity`, load `references/education-levels.md`.

Keep model-facing artifacts compact when `targeted_context_length` is tight. Put teaching detail in separate reports instead of bloating prompts, skills, AGENTS.md files, or phase instructions.


## Run Configuration Preview

For guided, deep, review-gate, AGENTS.md, migration, or file-changing work, show a compact run configuration preview when important parameters were inferred. Use `references/run-configuration-preview.md`.

The preview should state the inferred context, chosen parameters, low-confidence assumptions, and planned approach. Ask the user whether to proceed or change a parameter unless the user explicitly selected yolo/fast behavior.

## Workflow

### 1. Determine Task Type

Classify as create, convert, optimize, audit, repair, package, or evaluate.

Identify model profile, harness, domain intent, side-effect tier, and whether the skill is coding/repo/tool-oriented.

### 2. Extract or Define the Skill Contract

For existing skills, extract:

- purpose and trigger conditions
- inputs and outputs
- commands/tools/APIs
- files/resources/references
- side effects and permission boundaries
- failure handling and validation
- examples that encode behavior

Preserve these unless a change is required for safety, compatibility, or explicit user instruction.

### 3. Inventory Existing Instructions and Resources

Inspect `SKILL.md`, linked references, and relevant repo instruction files when available.

Use `references/instruction-deduplication.md` to avoid duplicating existing loop, context, Git, task-state, or validation safeguards.

Inventory `references/`, `scripts/`, `assets/`, and `agents/`. Use `references/reference-optimization.md`. Modify references only when they are behavioral, duplicated, stale, model-hostile, or needed for progressive disclosure.

### 4. Rewrite or Create the Skill

Use a concise main `SKILL.md` with progressive disclosure. Keep core workflow, non-negotiable rules, and validation gates inline. Move long templates, examples, model profiles, runtime notes, failure tables, and detailed protocols to references.

Add engineering metadata using `references/engineering-metadata.md`.

### 5. Add Domain and Safeguards When Relevant

Use `references/domain-intent.md`, `side-effect-matrix.md`, and domain profiles.

For tool-using skills, add loop safety from `loop-safety.md` unless equivalent safeguards already exist.

For coding/repo skills, add Git safety and coding standards using `git-safety.md`, `coding-standards.md`, `git-hygiene.md`, and `output-location.md`.

For AGENTS.md/instruction-related skills, add instruction scan/de-duplication.

For data science/ML/AI skills, use `domain-profiles/data-science-ml.md` and `domain-profiles/ai-modalities.md` when relevant.

### 6. Add Context, Phase, and Memory Support

If the skill may handle long docs, repos, files, logs, tool outputs, RAG, graph/index data, or multi-turn state, add context strategy from `context-management.md`.

If the skill supports long-running work, add phased planning, persistent task state, output location, and phase compression/debrief.

If scoped review reduces context pressure or improves validation, add subagent delegation.

### 7. Optional Ralph Loop

For reusable/high-risk skills, or when requested, run the bounded Ralph loop. Save each iteration to the canonical task folder and grade A-F. Do not iterate for cosmetics.

### 8. Validate

Check:

- frontmatter valid; only supported top-level keys
- description specific, complete, and distinctive
- source contract preserved
- references exist and are linked with when-to-read guidance
- no exposed chain-of-thought
- no invented thresholds or permission changes
- loop/Git/context/persistence safeguards added only when warranted
- duplicate/near-duplicate rules removed or consolidated
- instructions atomic enough for smaller models
- semantic diff and educational report included

## Required Output

```markdown
## Original Strengths
## Original Weaknesses
## Changes Made
## Semantic Diff
## Reference Changes
## Safeguards Added / Reused / Skipped
## A-F Quality Grades
## Why This Improves Local-Model Reliability
## Remaining Risks / Assumptions
## Files Written
```


## Documentation Quality

When generating or editing README material, user guides, educational reports, AGENTS.md explanations, or other reader-facing documentation, use `references/documentation-quality.md`. Keep generated artifacts factual, practical, and easy to act on. Avoid overused generated-writing patterns, unsupported claims, and unnecessary imperatives in user documentation.
