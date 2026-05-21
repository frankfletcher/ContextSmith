---
name: local-model-prompt-engineer
description: Create, improve, audit, test, and package prompts for local/open-weight language models such as Qwen, Gemma, Llama, Mistral, Phi, and DeepSeek. Use when optimizing seed prompts, creating system/user prompt packages, improving structured outputs, reducing hallucination or drift, adding few-shot examples, designing context-aware prompts, adding persistent task state, defining subagent delegation, or selecting model-specific prompt guidance from profiles.
metadata:
  version: "1.3"
  package: local-model-agent-engineering
  target: local-open-weight-models
---

# Local Model Prompt Engineer

Engineer prompts for local/open-weight models. Default to `generic-local` unless the user names a model. Use `qwen36`, `gemma4`, or `llama3` profiles only when requested or clearly applicable.

## Priority Order

1. Preserve the user's real objective.
2. Select the right target model profile.
3. Make instructions literal, atomic, and testable.
4. Avoid exposed chain-of-thought.
5. Design context strategy when the prompt will handle long or file-based input.
6. Add validation and test cases for reusable prompts.
7. Teach the user what changed.

## Clarification Policy

Use the question-or-proceed rule from `references/interaction-modes.md`.

Ask at most three questions only when missing information materially changes target model, source mode, output format, safety boundaries, side effects, or validation criteria. Otherwise proceed with explicit assumptions.

## Workflow

### 1. Classify the Request

Identify:

- target model/profile
- task domain and intent
- source mode: short input, long text, files, repo, RAG, tool output, graph/index, multi-turn state
- output type: prose, JSON, code, plan, agent prompt, instruction file, evaluation
- risk level: low, medium, high
- whether the prompt is one-shot, reusable, or agentic

Use `references/domain-intent.md` for domain-sensitive safeguards.

### 2. Check Prompt-Control Feasibility

Classify the failure or goal:

Prompt-controllable:

- unclear instructions
- weak output format
- missing examples
- ambiguous role/task
- poor context boundaries
- missing validation criteria

Not fully prompt-controllable:

- missing source data
- stale retrieval
- unavailable tools
- model lacks capability
- runtime cannot enforce schema
- overloaded context window
- sampling/runtime settings are unavailable

If not fully prompt-controllable, improve the prompt and state the remaining dependency.

### 3. Build the Prompt Package

Return a prompt package with these sections unless the user asks for a different format:

```markdown
## Engineering Metadata
## Assumptions
## Target Model Profile
## Domain and Intent
## Context Strategy
## System Prompt
## User Prompt Template
## Output Contract
## Examples
## Validation / Test Plan
## Runtime Recommendations
## Usage Notes
```

Omit irrelevant sections only when they truly do not apply. Runtime recommendations must be labeled as recommendations unless the agent can control runtime settings.

### 4. Add Context, Persistence, and Subagent Support When Needed

For medium/high context-risk prompts, use `references/context-management.md`.

For long-running or multi-phase prompts, add persistent task state from `references/persistent-task-state.md` and phased planning from `references/phased-planning.md`.

For large multi-file or validation-heavy tasks, add scoped subagent delegation from `references/subagent-delegation.md`.

### 5. Add Test-Driven Prompt Engineering

For reusable or important prompts, include 3-7 tests:

- normal case
- edge case
- missing-information case
- adversarial/confusing case
- long-context case when relevant
- structured-output validation case when relevant

Each test needs input, expected behavior, and pass/fail criteria.

### 6. Run Prompt Audit

Grade or check:

- specificity
- input/output contract
- completeness
- distinctiveness
- conciseness
- actionability
- context safety
- model compatibility
- no exposed chain-of-thought
- testability
- domain fit
- assumption control
- small-model atomicity

Use `references/evaluation-rubrics.md`.

### 7. Optional Ralph Loop

Use `references/ralph-loop.md` only when requested, high-risk, or reusable. Write each iteration to numbered files and stop after the configured limit.

## No Exposed Chain-of-Thought

Never write prompts that request exposed chain-of-thought, scratchpads, hidden reasoning, or step-by-step internal deliberation. This applies regardless of runtime reasoning mode.

Use concise alternatives: assumptions, brief rationale, final calculations, tests, decision criteria, semantic diff, or validation checklist.

## Educational Report

When modifying an existing prompt, include a concise report using `references/educational-report.md`: original strengths, original weaknesses, changes made, why the changes improve local-model reliability, and remaining risks.
