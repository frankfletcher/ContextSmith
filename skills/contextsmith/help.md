# contextsmith Help

`contextsmith` is the ContextSmith router skill. Use it when you are not sure which ContextSmith sub-skill should handle a request.

## Quickstart

```bash
/contextsmith help
```

## Routing Targets

- `contextsmith-prompt-engineer` for creating or improving prompts.
- `contextsmith-skill-engineer` for creating or improving `SKILL.md` skills.
- `contextsmith-skill-migrator` for staged directory-wide skill migrations.
- `contextsmith-instruction-engineer` for repo instruction files such as `AGENTS.md`.
- `contextsmith-agent-evaluator` for audit-only reviews and grading.
- `contextsmith-orchestrator` for executing prompts, task-state handoffs, and workflow configs with contract enforcement.

## Default Behavior

The router forwards user-provided parameters unchanged and does not invent defaults for omitted parameters. The selected sub-skill applies its own defaults.
