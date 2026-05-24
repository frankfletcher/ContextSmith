# ContextSmith User Guide

ContextSmith helps you build agent-facing artifacts that are easier for models to follow under real conditions: limited context, imperfect tools, repo complexity, long-running tasks, and human safety boundaries.

It is small-model-first, but not small-model-only. The same patterns that help Qwen, Gemma, Llama, and other local models also improve workflows with stronger models: clearer instructions, smaller phases, better validation, safer Git behavior, and less instruction clutter.

## The mental model

```text
User goal
  ↓
ContextSmith skill
  ↓
model profile + context budget + domain profile + harness assumptions
  ↓
prompt / skill / AGENTS.md / implementation plan / audit report
  ↓
agent executes with less drift, fewer loops, and better review points
```

ContextSmith does not replace your coding agent. It shapes the instructions, plans, and guardrails your coding agent will use.

## The core workflow

Most ContextSmith runs follow this pattern:

1. Choose the right skill.
2. Identify the target model profile or model capability tier.
3. Set the targeted context length.
4. Select the domain and harness when relevant.
5. Choose an interaction mode: fast, guided, deep, review-gate, or audit-only.
6. Generate or audit the artifact.
7. Review the educational report: what was strong, what was weak, what changed, and what risk remains.

## The most important control: targeted context length

Do not treat the model card's maximum context as the plan. Your runtime may fit less context. Your model may become unreliable before the theoretical maximum. Your agent harness may add tool output, logs, and hidden state.

When you say:

```bash
--context-length 32k
```

ContextSmith should materially change the output:

- shorter model-facing artifacts
- more phases
- fewer examples
- smaller migration batches
- stricter output budgets
- stronger task-state usage
- more selective reading
- more phase compression

This is one of the main reasons ContextSmith exists.

## Model-facing artifact vs reader-facing explanation

A common mistake is making the prompt or `AGENTS.md` verbose because the user wants to learn.

ContextSmith separates those concerns:

```bash
--artifact-verbosity compact --education-level deep
```

That means:

- keep the artifact compact enough for the model
- give the human a deeper explanation in a separate report

This is especially useful for students, junior engineers, data scientists, and people learning agentic coding workflows.

## Modes

Use `fast` when the task is small and low risk.

Use `guided` when choices matter but you do not want a long process.

Use `deep` when the artifact will be reused, shared, or used by an agent in a serious workflow.

Use `review-gate` when changes could overwrite files, migrate many skills, or affect future agent behavior.

Use `audit-only` when you want diagnosis before modification.

## Project-local outputs

For project work, ContextSmith should prefer:

```text
<project>/.agent-work/
```

This keeps task memory, phase reports, Ralph iterations, validation reports, and resume prompts near the project, without relying on `/tmp`.

By default, `.agent-work/` should usually be gitignored. ContextSmith should suggest `.gitignore` entries, but it should not modify `.gitignore` without approval.

## Strong planner, local executor

For large coding work, a practical workflow is:

1. Use a stronger model or ContextSmith deep path to create/audit the plan.
2. Split the plan into atomic phases.
3. Save task state under `.agent-work/`.
4. Execute one phase at a time with the local model.
5. End each phase with a debrief.
6. Start the next phase from task state, not the full previous chat.

> Strong models can write the plan. Smaller models can execute it — if the plan is atomic enough.

## What ContextSmith is not

ContextSmith is not:

- a model runtime
- a replacement for tests
- a replacement for source verification
- a guarantee that a small model can do every task
- a UI or CLI yet
- a promise that every harness supports every behavior

It is a toolkit for producing better agent instructions, plans, and audits.


## Run Configuration Preview

For guided, deep, review-gate, AGENTS.md, and migration workflows, ContextSmith can show the inferred run configuration before doing important work. The preview uses familiar flags, explains the choices briefly, and lets you change one line instead of rewriting the whole request.

Example:

```bash
--mode guided
--target-profile qwen36
--context-length 32k
--domain coding,data-science-ml
--harness generic-agent
--output project-local
```

If it looks right, say `proceed`. If one value is wrong, change that value.

## Documentation Quality

ContextSmith separates project documentation from agent references. Project documentation should explain the idea, show useful commands, and stay factual. Agent references should stay compact and operational.
