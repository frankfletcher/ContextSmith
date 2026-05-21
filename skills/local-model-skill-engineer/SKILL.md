---
name: local-model-skill-engineer
description: Create, convert, improve, audit, and package SKILL.md-based agent skills for local/open-weight language models. Use when building a new skill, adapting an existing skill for smaller/local models, preserving a source skill behavior while rewriting it, adding model profiles, optimizing references, adding context-aware workflows, persistent task state, subagent delegation, Ralph-loop iteration, semantic diff validation, or skill-auditor-style quality checks.
metadata:
  version: "1.3"
  package: local-model-agent-engineering
  target: local-open-weight-models
---

# Local Model Skill Engineer

Create, convert, improve, and audit SKILL.md-based skills for local/open-weight models.

## Priority Order

1. Preserve the source skill's behavioral contract.
2. Identify domain intent and target model profile.
3. Make instructions literal, atomic, testable, and context-aware.
4. Do not add exposed chain-of-thought.
5. Optimize references when they are part of the skill contract.
6. Validate mechanically and semantically.
7. Teach the user what changed.

## Clarification Policy

Use `references/interaction-modes.md`. Ask only when blocked or when the answer materially changes target profile, source path, output format, side effects, permission boundaries, or validation. Otherwise proceed with stated assumptions.

## Workflow

### 1. Determine Task Type

Classify as create, convert, optimize, audit, repair, or package.

Identify target profiles. Default to `generic-local` unless the user specifies Qwen, Gemma, Llama, or another model.

### 2. Extract or Define the Skill Contract

For existing skills, extract:

- purpose
- trigger conditions
- inputs
- outputs
- commands/tools/APIs
- files/resources/references
- permission boundaries
- failure handling
- examples that encode behavior
- validation requirements

Preserve these unless a change is required for safety, compatibility, or explicit user instruction.

### 3. Inventory Resources

Inspect `SKILL.md`, then referenced files. Inventory `references/`, `scripts/`, `assets/`, and `agents/`.

Use `references/reference-optimization.md` if present. If not, apply this policy:

- optimize behavioral references when they contain instructions the agent follows
- preserve exact commands, schemas, APIs, paths, and examples
- move bulky templates/failure tables into references when helpful
- do not edit scripts/assets unless required or requested
- list every modified reference in the audit

### 4. Rewrite or Create the Skill

Use a concise main `SKILL.md` with progressive disclosure. Keep core workflow, non-negotiable rules, and validation gates inline. Move long templates, examples, model profiles, runtime notes, and failure tables to references.

Add engineering metadata using `references/engineering-metadata.md` when supported.

### 5. Add Context-Aware Behavior When Relevant

If the target skill may handle long docs, repos, files, logs, tool outputs, RAG, graph/index data, or multi-turn agent state, add context strategy from `references/context-management.md`.

If the target skill supports long-running work, add persistent task state and phased planning from `references/persistent-task-state.md` and `references/phased-planning.md`.

If scoped review will reduce context pressure or improve validation, add subagent delegation from `references/subagent-delegation.md`.

### 6. Domain Intent Adaptation

Use `references/domain-intent.md` to infer the domain and add domain-specific safeguards only when relevant. Do not overfit weak evidence.

### 7. Validate

Run these gates:

- YAML/frontmatter validity
- description specificity and trigger quality
- body present
- references linked and existent
- source contract preserved
- no exposed chain-of-thought
- commands/resources preserved or justified
- permission boundaries preserved or justified
- no invented thresholds/policies
- context/persistence/subagent support included only when warranted
- small-model atomicity sufficient
- progressive disclosure appropriate
- domain guardrails appropriate

### 8. Optional Ralph Loop

Use `references/ralph-loop.md` when requested or high-risk. Save numbered iterations and grade each iteration using `references/evaluation-rubrics.md`.

## Required Output

When changing a skill, return:

1. changed files or download link
2. original strengths
3. original weaknesses
4. changes made
5. semantic diff summary
6. target model/profile metadata
7. validation result
8. remaining risks/assumptions
