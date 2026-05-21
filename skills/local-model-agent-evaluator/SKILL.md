---
name: local-model-agent-evaluator
description: Audit prompts, skills, AGENTS.md files, repo instructions, agent workflows, model profiles, migration outputs, and long-running plans for local/open-weight model reliability without modifying them by default. Use when the user wants grades, strengths, weaknesses, A-F rubric scoring, context-risk review, loop-safety review, Git/file safety review, data science/ML safeguard review, small-model atomicity review, no-chain-of-thought validation, or targeted context fit review, upstream artifact audits, skill interoperability grading, or recommendations before using an engineer or migrator skill.
metadata:
  version: "1.2"
  package: local-model-agent-engineering
  target: local-open-weight-models
---

# Local Model Agent Evaluator

Audit prompts, skills, AGENTS.md files, agent workflows, migration outputs, and instruction packages for local/open-weight model reliability without modifying them by default.

## Default Mode

Audit-only. Do not edit files unless the user explicitly asks.

## Targeted Context and Interoperability Checks

When evaluating an artifact, grade targeted context fit using `references/targeted-context-length.md` and skill interoperability using `references/skill-interoperability.md`.

Check whether upstream tools or skills introduced unsupported requirements, duplicate workflows, conflicting instructions, or hallucinated dependencies. Recommend rejection or downgrade of unsupported additions.

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
