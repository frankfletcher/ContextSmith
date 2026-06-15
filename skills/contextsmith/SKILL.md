---
name: contextsmith
description: Meta-skill for ContextSmith, an instruction-engineering toolkit for local/open-weight models that is also useful for frontier-model agent workflows. Routes to sub-skills for prompt engineering, skill creation, skill migration, repo instruction engineering, agent evaluation, and prompt execution. Use when the user needs to create, improve, audit, migrate, or execute model-aware agent artifacts.
metadata:
  version: "2.2.0"
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
| --- | --- |
| Create or improve a prompt or seed prompt | `contextsmith-prompt-engineer` |
| Build, convert, or improve a SKILL.md skill | `contextsmith-skill-engineer` |
| Migrate a directory of skills to a new profile or location | `contextsmith-skill-migrator` |
| Create or edit AGENTS.md, CLAUDE.md, copilot-instructions, or repo-level agent files | `contextsmith-instruction-engineer` |
| Audit, grade, or evaluate an existing artifact without modifying it | `contextsmith-agent-evaluator` |
| Execute a prompt, prompt file, NEXT_PROMPT.md handoff, or workflow config | `contextsmith-orchestrator` |
| Generate a workflow config from natural language intent | `contextsmith-workflow-developer` |

Use `contextsmith-agent-evaluator` for audit-only requests, even when the artifact is a prompt. Use `contextsmith-prompt-engineer` when the user wants the prompt improved or packaged.

If the request spans multiple areas, pick the sub-skill that matches the user's *first* or *primary* action, then mention the follow-up skill.

## Parameter Defaults

Forward user-provided parameters as-is. Do not supply routing-layer defaults for omitted parameters; let the selected sub-skill apply its own documented defaults.

## Cross-Skill Coordination

Some workflows chain skills:

1. **Build then audit**: `contextsmith-skill-engineer` -> `contextsmith-agent-evaluator`
2. **Migrate then validate**: `contextsmith-skill-migrator` -> `contextsmith-agent-evaluator`
3. **Engineer then execute**: `contextsmith-prompt-engineer` -> `contextsmith-orchestrator`
4. **Audit then fix**: `contextsmith-agent-evaluator` -> appropriate engineer skill
5. **Generate then run**: `contextsmith-workflow-developer` -> `contextsmith-orchestrator`

When the user's request implies a chain, complete the first step, then offer the next with a concise summary of what to carry forward.

## Parameter Forwarding

Accept both natural-language controls and CLI-style flags at the meta-skill level. Strip the `contextsmith` routing layer and forward the remaining parameters to the sub-skill. If a parameter is specific to one sub-skill and not recognized at the meta level, pass it through anyway.

## Help Mode

If the user invokes this skill with `help`, `describe`, `examples`, `modes`, `parameters`, `quickstart`, or CLI-style equivalents such as `--help`, do not route to a sub-skill. Return a concise overview from `references/help.md` and list the available sub-skills with one-line descriptions.

## Wizard Mode

When this skill is invoked with no clear intent, no flags, and no specific sub-skill name, enter wizard mode. Wizard mode asks one question at a time using the harness's structured question tool (e.g., `AskUserQuestion` in OpenCode) to determine intent, model profile, and context budget, then dispatches to the appropriate sub-skill.

Skip the wizard when the user provides any of: a sub-skill name, CLI flags, or natural-language intent that maps clearly to a sub-skill.

For questioning format and page-flow patterns, see `references/structured-questioning.md`.

### Wizard Questions

Ask exactly these three questions in order. Use the structured question tool for each. After Q3, present a confirmation table and ask for approval.

**Q1: "What are you working on?"**

| Option | Maps to |
| -------- | --------- |
| A prompt | `contextsmith-prompt-engineer` |
| A skill (SKILL.md) | `contextsmith-skill-engineer` |
| Repo instructions (AGENTS.md, etc.) | `contextsmith-instruction-engineer` |
| Something to review or audit | `contextsmith-agent-evaluator` |
| A prompt, handoff, or workflow config to execute | `contextsmith-orchestrator` |
| A workflow plan to generate from intent | `contextsmith-workflow-developer` |
| A directory of skills to migrate | `contextsmith-skill-migrator` |
| Not sure yet | Ask Q2 with a freeform description |

If the user cannot describe their task after Q2, dispatch to `contextsmith-agent-evaluator` with `--mode audit-only --target .` to review the current project.

**Q2: "Which model will use the result?"**

| Option | Maps to |
| -------- | --------- |
| Qwen 3 (6B) | `--target-profile qwen36` |
| Qwen 3 (14B) | `--target-profile qwen3-14b` |
| Qwen 3 (32B) | `--target-profile qwen3-32b` |
| Gemma 4 | `--target-profile gemma4` |
| Llama 3.x | `--target-profile llama3` |
| Generic local model | `--target-profile generic-local` |
| Not sure (use generic-local) | `--target-profile generic-local` |

If the agent harness identifies its model (e.g., the user is running in opencode, cursor, or another harness that exposes model info), use that information to pre-select the profile and note the inference in the confirmation table.

**Q3: "How much context can it work with?"**

| Option | Maps to |
| -------- | --------- |
| 8K — very small | `--context-length 8k` |
| 64K — common modern | `--context-length 64k` |
| 128K — larger local or frontier | `--context-length 128k` |
| Not sure (use 64k) | `--context-length 64k` |

### Confirmation

After Q3, display the full command and parameter table:

```
→ ContextSmith will run:

  /contextsmith-<sub-skill> \
    --target-profile <profile> \
    --context-length <length> \
    --mode guided \
    --ralph 1

  Parameters:
  ┌──────────────────┬────────────────────────────────────────┐
  │ Target profile   │ <profile> (inferred from harness/info) │
  │ Context length   │ <length>                                │
  │ Mode             │ guided                                  │
  │ Ralph iterations │ 1                                       │
  │ Output           │ chat (no files written)                  │
  └──────────────────┴────────────────────────────────────────┘

  [Yes, run it] [No, let me modify → restart at Q2]
```

- **Yes**: dispatch to the sub-skill with the inferred parameters.
- **No**: re-enter the wizard at Q2 (not Q1 — the user already chose their task type).

### Defaults When Skipping Wizard

When the user provides flags or intent but omits some parameters, apply these defaults:

| Parameter | Default | Logic |
| ----------- | --------- | ------- |
| `--target-profile` | Harness-derived if available, else `generic-local` | Infer from the agent environment when possible |
| `--context-length` | `64k` | Safer modern default for most local models |
| `--mode` | `guided` | Best for interactive work |
| `--ralph` | `1` | One improvement pass is usually enough |
| `--output` | `chat` for zero-flag invocations | Do not write files without explicit direction |
