---
name: contextsmith
description: Meta-skill for ContextSmith, an instruction-engineering toolkit for local/open-weight models that is also useful for frontier-model agent workflows. Routes to sub-skills for prompt engineering, skill creation, skill migration, repo instruction engineering, agent evaluation, and prompt execution. Use when the user needs to create, improve, audit, migrate, or execute model-aware agent artifacts.
metadata:
  version: "1.7.1"
  package: ContextSmith
  target: local-open-weight-first
  type: meta-skill
---

# ContextSmith

Model-aware agent instruction engineering. This meta-skill routes to the appropriate ContextSmith sub-skill based on user intent. ContextSmith is local/open-weight first, with practices that also transfer to frontier-model agent workflows.

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
| Create or improve a prompt or seed prompt | `contextsmith-prompt-engineer` |
| Build, convert, or improve a SKILL.md skill | `contextsmith-skill-engineer` |
| Migrate a directory of skills to a new profile or location | `contextsmith-skill-migrator` |
| Create or edit AGENTS.md, CLAUDE.md, copilot-instructions, or repo-level agent files | `contextsmith-instruction-engineer` |
| Audit, grade, or evaluate an existing artifact without modifying it | `contextsmith-agent-evaluator` |
| Execute a prompt, prompt file, or NEXT_PROMPT.md handoff with controls | `contextsmith-run` |

Use `contextsmith-agent-evaluator` for audit-only requests, even when the artifact is a prompt. Use `contextsmith-prompt-engineer` when the user wants the prompt improved or packaged.

If the request spans multiple areas, pick the sub-skill that matches the user's *first* or *primary* action, then mention the follow-up skill.

## Parameter Defaults

Forward user-provided parameters as-is. Do not supply routing-layer defaults for omitted parameters; let the selected sub-skill apply its own documented defaults.

## Cross-Skill Coordination

Some workflows chain skills:

1. **Build then audit**: `contextsmith-skill-engineer` -> `contextsmith-agent-evaluator`
2. **Migrate then validate**: `contextsmith-skill-migrator` -> `contextsmith-agent-evaluator`
3. **Engineer then execute**: `contextsmith-prompt-engineer` -> `contextsmith-run`
4. **Audit then fix**: `contextsmith-agent-evaluator` -> appropriate engineer skill

When the user's request implies a chain, complete the first step, then offer the next with a concise summary of what to carry forward.

## Parameter Forwarding

Accept both natural-language controls and CLI-style flags at the meta-skill level. Strip the `contextsmith` routing layer and forward the remaining parameters to the sub-skill. If a parameter is specific to one sub-skill and not recognized at the meta level, pass it through anyway.

## Help Mode

If the user invokes this skill with `help`, `describe`, `examples`, `modes`, `parameters`, `quickstart`, or CLI-style equivalents such as `--help`, do not route to a sub-skill. Return a concise overview from `references/help.md` and list the available sub-skills with one-line descriptions.
