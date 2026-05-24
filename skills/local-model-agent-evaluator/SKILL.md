---
name: local-model-agent-evaluator
description: Audit prompts, skills, AGENTS.md files, repo instructions, agent workflows, model profiles, migration outputs, and long-running plans for local/open-weight model reliability without modifying them by default. Use when the user wants grades, strengths, weaknesses, A-F rubric scoring, context-risk review, loop-safety review, Git/file safety review, data science/ML safeguard review, small-model atomicity review, no-chain-of-thought validation, or targeted context fit review, upstream artifact audits, skill interoperability grading, or recommendations before using an engineer or migrator skill.
metadata:
  version: "1.4.0"
  package: ContextSmith
  target: local-open-weight-models
---

# Local Model Agent Evaluator

Audit prompts, skills, AGENTS.md files, agent workflows, migration outputs, and instruction packages for local/open-weight model reliability without modifying them by default.


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

## Default Mode

Audit-only. Do not edit files unless the user explicitly asks.

## Targeted Context and Interoperability Checks

When evaluating an artifact, grade targeted context fit using `references/targeted-context-length.md` and skill interoperability using `references/skill-interoperability.md`.

Check whether upstream tools or skills introduced unsupported requirements, duplicate workflows, conflicting instructions, or hallucinated dependencies. Recommend rejection or downgrade of unsupported additions.



## Model Capability and Planner/Executor Profiles

When the user provides `--target-capability`, `--planner-profile`, or `--executor-profile`, load `references/model-capability-tiers.md` and `references/planner-executor-workflows.md`.

Use stronger/planner profiles for planning, audits, architecture, test strategy, and final review. Use smaller/executor profiles for atomic phase execution when the plan and task state are explicit.



## Education Level and Artifact Verbosity

If the user provides `--education-level` or `--artifact-verbosity`, load `references/education-levels.md`.

Keep model-facing artifacts compact when `targeted_context_length` is tight. Put teaching detail in separate reports instead of bloating prompts, skills, AGENTS.md files, or phase instructions.



## Implementation Plan, Test, and Phase Review Audits

When generating or auditing coding plans, tests, or phase workflows, use:

- `references/implementation-plan-audit.md`
- `references/test-quality-audit.md`
- `references/phase-code-review.md`
- `references/small-context-workflows.md`

For coding domains, implementation plans should include test strategy, code review gates, and phase debriefs. Tests should be audited for usefulness, not just pass/fail status.

## Workflow

1. Identify artifact type: prompt, skill, instruction file, workflow, model profile, migration output, phase plan.
2. Select target model profile or use `generic-local`.
3. Detect domain intent and side-effect risk using `domain-intent.md` and `side-effect-matrix.md`.
4. Inspect existing safeguards and duplicate rules using `instruction-deduplication.md`.
5. Evaluate context strategy, persistent task state, subagent use, assumptions, loop safety, Git/file safety, and no exposed chain-of-thought.
6. For coding or repo artifacts, check coding standards, validation evidence, Git safety, and gitignore hygiene.
7. For data science/ML/AI artifacts, check leakage prevention, evaluation, reproducibility, artifact handling, and modality-specific rules.
8. Grade each dimension A-F using `evaluation-rubrics.md`.
9. Recommend improvements in priority order.
10. State whether a Ralph loop, prompt engineer, skill engineer, instruction engineer, or migrator should be used next.



## Runtime Stability Notes

If the user asks about local model loops, server settings, speculative decoding, KV cache precision, or long agentic coding instability, use `references/runtime-stability.md`. Treat runtime settings as experimental deployment guidance unless the harness can control them.

## Required Output

```markdown
## Summary Grade
## Strengths
## Weaknesses
## A-F Rubric
| Dimension | Grade | Reason | Recommended Fix |
## Loop / Git / Context Safety
## Domain-Specific Risks
## Duplicate or Conflicting Instructions
## High-Risk Issues
## Suggested Next Action
```

Use constructive critique. Do not rewrite the artifact unless requested.
