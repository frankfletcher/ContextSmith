# Usage Patterns

Use this reference when writing README sections, help pages, or examples.

## Common Pattern

```text
/<skill-name> --mode <mode> --target-profile <profile> --context-length <N> --domain <domain> --harness <harness>

Natural language task goes here.
```

## Recommended Defaults

- Low-risk one-off improvement: `--mode fast --no-ralph --output chat`
- Important reusable prompt/skill: `--mode deep --ralph 2 --output project-local`
- File-changing repo work: `--mode guided --output project-local`
- Batch migration: `--mode review-gate --backup --stage --no-apply`
- Diagnosis only: `--mode audit-only --output chat`

## Benefits to Explain

- `targeted_context_length` makes artifacts actually fit the user's local runtime.
- `guided mode` reduces bad assumptions without forcing a long interview.
- `review-gate mode` prevents destructive or wide changes without approval.
- `Ralph loop` improves quality after baseline validation, but only when materially useful.
- `project-local output` preserves reports and iterations under `.agent_work/` instead of `/tmp`.
## Strong Planner, Local Executor Pattern

For large coding tasks, use a stronger model or deep-path ContextSmith run to create and audit the plan, then use a smaller/local model to execute atomic phases.

Example:

```bash
/local-model-prompt-engineer   --mode deep   --planner-profile frontier-cloud   --executor-profile qwen36   --target-capability small-local   --context-length 32k
```

This pattern works because the executor model does not need to rediscover the architecture. It carries out well-scoped instructions with durable task state.
