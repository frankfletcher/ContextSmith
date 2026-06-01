---
name: contextsmith
description: Meta-skill for ContextSmith — precision instruction engineering for local/open-weight and frontier model agents. Routes to sub-skills for prompt engineering, skill creation, skill migration, repo instruction engineering, agent evaluation, and prompt execution. Use when the user needs to create, improve, audit, migrate, or execute model-aware agent artifacts.
metadata:
  version: "1.0.0"
  package: ContextSmith
  target: all-models
  type: meta-skill
---

# ContextSmith

Model-aware agent instruction engineering. This meta-skill routes to the appropriate ContextSmith sub-skill based on user intent.

## When to Load

Load this skill when the user's request involves any of:

- Creating or improving prompts for local/open-weight models
- Building or adapting SKILL.md-based agent skills
- Migrating skills between model profiles or installations
- Engineering AGENTS.md, CLAUDE.md, or other repo instruction files
- Auditing prompts, skills, or agent workflows for model reliability
- Executing prompts or task-state handoffs with declared controls
- Improving agent behavior for specific model profiles or context budgets

## Skill Routing

Dispatch to exactly one sub-skill based on the user's primary intent:

| User Intent | Sub-Skill |
|---|---|
| Create, improve, or audit a prompt or seed prompt | `local-model-prompt-engineer` |
| Build, convert, or improve a SKILL.md skill | `local-model-skill-engineer` |
| Migrate a directory of skills to a new profile or location | `local-model-skill-migrator` |
| Create or edit AGENTS.md, CLAUDE.md, copilot-instructions, or repo-level agent files | `local-model-instruction-engineer` |
| Audit, grade, or evaluate an existing artifact without modifying it | `local-model-agent-evaluator` |
| Execute a prompt, prompt file, or NEXT_PROMPT.md handoff with controls | `local-model-run` |

If the request spans multiple areas, pick the sub-skill that matches the user's *first* or *primary* action, then mention the follow-up skill.

## Shared Defaults

When passing parameters to a sub-skill, forward user-provided values as-is. For unspecified parameters, use these defaults unless the sub-skill documents different ones:

| Parameter | Default |
|---|---|
| `--target-profile` | `generic-local` |
| `--context-length` | `64k` |
| `--mode` | `guided` |
| `--education-level` | `guided` |
| `--harness` | inferred from project files |

## Cross-Skill Coordination

Some workflows chain skills:

1. **Build then audit**: `skill-engineer` -> `agent-evaluator`
2. **Migrate then validate**: `skill-migrator` -> `agent-evaluator`
3. **Engineer then execute**: `prompt-engineer` -> `local-model-run`
4. **Audit then fix**: `agent-evaluator` -> appropriate engineer skill

When the user's request implies a chain, complete the first step, then offer the next with a concise summary of what to carry forward.

## Parameter Forwarding

Accept both natural-language controls and CLI-style flags at the meta-skill level. Strip the `contextsmith` routing layer and forward the remaining parameters to the sub-skill. If a parameter is specific to one sub-skill and not recognized at the meta level, pass it through anyway.

## Help Mode

If the user invokes this skill with `help`, `describe`, `examples`, `modes`, `parameters`, `quickstart`, or CLI-style equivalents such as `--help`, do not route to a sub-skill. Return a concise overview of the ContextSmith package and list the available sub-skills with one-line descriptions.
