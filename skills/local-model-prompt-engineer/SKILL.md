---
name: local-model-prompt-engineer
description: Create, improve, audit, test, and package prompts for local/open-weight language models such as Qwen, Gemma, Llama, Mistral, Phi, and DeepSeek. Use when optimizing seed prompts, creating system/user prompt packages, improving structured outputs, reducing hallucination or drift, adding few-shot examples, designing context-aware prompts, adding persistent task state, defining subagent delegation, loop-safety rules, Git/file safety, phased execution, Ralph-loop iteration, targeted context length control, upstream artifact audits, or selecting model-specific prompt guidance from profiles.
metadata:
  version: "1.6"
  package: local-model-agent-engineering
  target: local-open-weight-models
---

# Local Model Prompt Engineer

Engineer prompt packages for local/open-weight models. Default to `generic-local` unless the user names a model. Use model profiles only when requested or clearly applicable.


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

1. Preserve the user's real objective.
2. Identify model, harness, domain, context risk, and side-effect risk.
3. Make instructions literal, atomic, and testable.
4. Avoid exposed chain-of-thought; request assumptions, rationale, tests, diffs, or verification instead.
5. Add context strategy, loop safety, Git/file safety, persistent state, or subagent delegation only when relevant.
6. Validate with A-F rubrics; optionally run a bounded Ralph loop.
7. Teach the user what was strong, weak, and improved.

## Clarification Policy

Use `references/interaction-modes.md`.

Ask at most three questions only when missing information materially changes target model/profile, source mode, output format, side effects, safety boundaries, validation, or artifact location. Otherwise proceed with explicit assumptions.

## Targeted Context Length

When the user provides `targeted context length`, `context length`, `ctx`, or equivalent, optimize for that budget instead of the model's advertised maximum. Load `references/targeted-context-length.md`.

The targeted context length must materially affect the output: verbosity, phase count, example count, context strategy, persistent state, subagent use, and validation/report size.

## Upstream Artifact Audit

If the prompt was previously modified by another optimizer, skill, or generator, run `references/upstream-artifact-audit.md` before preserving upstream additions. Reject unsupported frameworks, libraries, workflows, dependencies, or requirements not supported by user request or project evidence.

Use `references/instruction-precedence.md` when upstream artifacts conflict with user/project/model/domain requirements.

## Workflow

### 1. Classify the Request

Identify:

- target model/profile and harness, if known
- domain and operational intent using `references/domain-intent.md`
- source mode: short input, long text, files, repo, RAG, tool output, graph/index, multi-turn state
- side-effect tier using `references/side-effect-matrix.md`
- output type: prompt, prompt package, plan, agent prompt, evaluator, JSON/schema, instruction file
- whether this is one-shot, reusable, long-running, or agentic

### 2. Check Prompt-Control Feasibility

Classify whether the requested improvement is prompt-controllable.

Prompt-controllable: unclear instructions, weak output format, missing examples, ambiguous task, poor context boundaries, missing validation criteria.

Not fully prompt-controllable: missing data, stale retrieval, unavailable tools, model capability limits, runtime settings unavailable, overloaded context, weak harness support.

If not fully prompt-controllable, improve the prompt and state the remaining dependency.

### 3. Select References

Load only relevant references:

- model profiles: `references/model-profiles/`
- context and output location: `context-management.md`, `output-location.md`
- long-running work: `phased-planning.md`, `persistent-task-state.md`, `phase-compression.md`
- loop/tool safety: `loop-safety.md`, `git-safety.md`
- domains: `domain-profiles/`
- quality: `evaluation-rubrics.md`, `ralph-loop.md`, `small-model-atomicity.md`
- existing instruction scan: `instruction-deduplication.md`

### 4. Build the Prompt Package

Return these sections unless the user requests otherwise:

```markdown
## Engineering Metadata
## Assumptions
## Target Model and Harness Profile
## Domain and Intent
## Prompt-Control Feasibility
## Context Strategy
## Interaction Mode
## System Prompt
## User Prompt Template
## Examples, if needed
## Validation and Test Plan
## Loop/Git/File Safety, if relevant
## Persistent Task State, if relevant
## Subagent Delegation, if relevant
## Runtime Recommendations, if requested or useful
## Educational Change Report
```

Runtime settings are recommendations unless the harness exposes control.

### 5. Add Context, Phase, and Loop Controls When Needed

For medium/high context tasks, specify source mode, reading order, chunking/summarization, evidence anchors, and final re-anchor.

For long-running work, require phase plans with durable memory and phase closeout/debrief using `references/phased-planning.md`, `persistent-task-state.md`, and `phase-compression.md`.

For tool-using prompts, add loop-safety rules. For coding/repo prompts, add Git/file safety and gitignore suggestions.

### 6. Optional Ralph Loop

Use `references/ralph-loop.md` only when requested, reusable, high-risk, or likely to benefit. Save each iteration in the canonical location from `references/output-location.md`. Grade each iteration A-F using `references/evaluation-rubrics.md`.

### 7. Audit Before Delivery

Check:

- no exposed chain-of-thought
- model-specific assumptions are profile-bound
- prompt is atomic enough for smaller models
- output contract is testable
- context strategy is sufficient
- assumptions and side effects are explicit
- loop/Git/file safeguards are present when relevant
- instructions are de-duplicated and non-contradictory
- validation/test plan exists for reusable prompts
- educational report explains strengths, weaknesses, changes, and remaining risks

## Required Output

Deliver the optimized prompt package plus a concise report:

```markdown
## Original Strengths
## Original Weaknesses
## Changes Made
## Why This Improves Local-Model Reliability
## A-F Quality Grades
## Remaining Risks / Assumptions
## Files Written, if any
```
