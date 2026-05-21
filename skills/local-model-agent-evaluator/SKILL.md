---
name: local-model-agent-evaluator
description: Audit prompts, skills, AGENTS.md files, repo instructions, agent workflows, model profiles, and migration outputs for local/open-weight model reliability without modifying them by default. Use when the user wants grades, strengths, weaknesses, A-F rubric scoring, context-risk review, small-model atomicity review, no-chain-of-thought validation, or recommendations before using an engineer or migrator skill.
metadata:
  version: "1.0"
  package: local-model-agent-engineering
  target: local-open-weight-models
---

# Local Model Agent Evaluator

Audit prompts, skills, AGENTS.md files, agent workflows, and instruction packages for local/open-weight model reliability without modifying them by default.

## Default Mode

Audit-only. Do not edit files unless the user explicitly asks.

## Workflow

1. Identify artifact type: prompt, skill, instruction file, workflow, model profile, migration output.
2. Select target model profile or use `generic-local`.
3. Detect domain intent and side-effect risk.
4. Evaluate using `references/evaluation-rubrics.md`.
5. Check context strategy, persistent task state, subagent use, assumptions, and no exposed chain-of-thought.
6. Grade each dimension A-F.
7. Recommend improvements in priority order.
8. State whether a Ralph loop, skill engineer, prompt engineer, instruction engineer, or migrator should be used next.

## Required Output

```markdown
## Summary Grade

## Strengths

## Weaknesses

## A-F Rubric
| Dimension | Grade | Reason | Recommended Fix |

## High-Risk Issues

## Suggested Next Action
```

Use constructive critique. Do not rewrite the artifact unless requested.
