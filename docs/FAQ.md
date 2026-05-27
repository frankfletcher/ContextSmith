# FAQ

## Is ContextSmith a coding agent?

No. ContextSmith helps create and improve the instructions, prompts, skills, plans, and review artifacts that coding agents use.

## Is ContextSmith only for small models?

No. It is small-model-first, but the same practices help larger models too: clear instructions, context discipline, validation, Git safety, and phase memory.

## Why not just use the biggest context window available?

Because usable context is not the same as advertised context. Local runtimes may degrade before the model-card limit, especially with long tool output, KV cache compression, context shift, speculative decoding, or harness overhead.

## Why does ContextSmith care about AGENTS.md so much?

For coding agents, `AGENTS.md` can shape every run in a repo. If it is vague, bloated, contradictory, or missing safety rules, the agent inherits those problems.

## Should I commit `.agent_work/`?

Usually no. Treat `.agent_work/` as local operational state. Commit curated final documents only when they are intentionally useful to the project.

## Does ContextSmith modify files automatically?

It depends on the mode and harness. Use `audit-only`, `stage`, `review-gate`, `--no-apply`, and `--backup` when you want safe behavior.

## What is a Ralph loop?

A bounded improvement loop. ContextSmith saves each iteration, grades it, improves only material weaknesses, and stops after the configured limit.

## What does `education-level` do?

It controls how much the human report teaches. It should not bloat the model-facing artifact unless you also increase `artifact-verbosity`.

## What if another optimizer already changed my prompt?

ContextSmith should audit upstream additions. Unsupported requirements should be flagged or rejected instead of blindly preserved.

## What if I do not know my model profile?

Use `generic-local` or a capability tier such as `small-local`, `coding-specialized`, or `frontier-cloud`.
