# Control Parameters

ContextSmith accepts both natural language and CLI-style controls.

You can write:

```text
Deep path. Target profile: qwen36. Context length: 32k. Domain: coding. Ralph loop: 2.
```

or:

```bash
--mode deep --target-profile qwen36 --context-length 32k --domain coding --ralph 2
```

Both mean the same thing. CLI-style flags are easier to copy, repeat, and later map to a real CLI. Natural language remains supported.

## Start with these three

Most users only need these at first:

```bash
--mode guided --target-profile qwen36 --context-length 32k
```

Add more controls only when they matter.

## Modes

| Flag | Meaning | Use when |
|---|---|---|
| `--mode fast` | One-pass, concise output | Small, low-risk tasks |
| `--mode deep` | More analysis, stronger validation, optional Ralph loop | Reusable or important artifacts |
| `--mode guided` | Ask 1-3 high-impact questions when needed | Broad instructions, AGENTS.md, ambiguous tasks |
| `--mode yolo` | Proceed with assumptions unless blocked | Low-risk work where speed matters |
| `--mode review-gate` | Plan or stage before applying | File edits, migrations, high-risk changes |
| `--mode audit-only` | Diagnose without changing files | Reviews, safety checks, evaluations |

## Model and capability controls

```bash
--target-profile qwen36
--target-profiles generic-local,qwen36
--target-capability small-local
--planner-profile frontier-cloud
--executor-profile qwen36
```

Use model profiles when you know the target model family. Use capability tiers when you care more about the role than the specific model.

Examples:

```bash
--target-profile qwen36 --context-length 32k
```

Optimizes for Qwen3.6-like local execution under tight context.

```bash
--planner-profile frontier-cloud --executor-profile qwen36
```

Uses the idea that a stronger model may create/audit the plan, while a smaller model executes atomic phases.

## Context length

Accepted forms:

```bash
--context-length 32k
--targeted-context-length 32k
--ctx 32768
```

Generated metadata should use:

```yaml
metadata:
  targeted_context_length: "32k"
```

This is not cosmetic. Tight context should change phase size, artifact verbosity, examples, migration batch size, task-state usage, and output budget.

## Domain and harness

```bash
--domain coding,data-science-ml
--harness opencode
```

Domain affects guardrails and validation. Harness affects assumptions about tools, approval, file edits, and loop safety.

Common domains:

- `coding`
- `data-science-ml`
- `frontend`
- `research`
- `document-processing`
- `email`
- `purchasing-tickets`
- `calendar-scheduling`

## Iteration and review

```bash
--ralph 2
--no-ralph
--phase-review standard
--code-review-iterations 1
```

Use Ralph loops for artifact improvement. Use phase review for code changes after a phase completes.

## Education and verbosity

```bash
--education-level none|brief|guided|deep|teaching
--artifact-verbosity compact|normal|detailed
```

`education-level` controls how much the human report teaches.

`artifact-verbosity` controls how verbose the generated artifact is.

For tight context, prefer:

```bash
--artifact-verbosity compact --education-level guided
```

## Output and safety

```bash
--output chat
--output project-local
--output staging
--backup
--stage
--apply
--no-apply
```

Use `project-local` when you want durable task state and reports under `.agent_work/`.

Use `staging` or `--no-apply` when original files should not be overwritten.

## Conflict handling

If flags conflict with prose, the user's current explicit prose wins unless the intent is ambiguous.

Example:

```text
--mode yolo
Please ask before making changes.
```

The skill should not blindly YOLO. It should ask one concise clarification question or default to the safer review-gate behavior for file changes.


## Run Configuration Preview

Use `--review-config` or `--preview-config` when you want ContextSmith to show inferred parameters before it proceeds. Use `--no-review-config` when you want to skip that preview for low-risk work.

Recommended for:

- AGENTS.md generation;
- skill migration;
- deep/guided runs;
- review-gate workflows;
- file-changing tasks;
- cases where ContextSmith inferred the domain, harness, or context length.
