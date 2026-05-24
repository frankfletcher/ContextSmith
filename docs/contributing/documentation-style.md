# Documentation Style

ContextSmith documentation should feel like a practical maintainer explaining what works, what is risky, and how to get useful results quickly.

## Voice

Use a clear, candid, technically credible tone. Favor concrete examples over broad claims. Explain why a workflow matters, then give the command or checklist that helps the reader use it.

## Audience

Project documentation is for people evaluating or using ContextSmith. Agent references are for agents executing ContextSmith workflows. These two audiences need different styles.

- Project documentation: explanatory, warm, practical, factual.
- Agent references: compact, imperative, operational.
- Changelog: factual and restrained.
- Educational reports: explanatory, but separated from model-facing artifacts.

## Style Guidelines

Prefer:

- short paragraphs;
- specific examples;
- copy-paste commands;
- honest project status;
- plain explanations of project terms;
- suggestions in user docs when the action is advisory;
- direct imperatives in agent references when safety or correctness requires them.

Avoid:

- generic AI marketing language;
- repeated “not just X, but Y” contrast constructions;
- language that implies the user needs hand-holding;
- long bullet lists without context;
- claims about tests, integrations, or benchmarks unless they are factual;
- making every document sound like an agent instruction file.

## Contrast Patterns

Contrast can be useful, but repeated contrast is a recognizable generated-writing pattern. Use it sparingly.

Instead of:

> The goal is not just better prompts. The goal is agent instructions that remain usable.

Prefer:

> ContextSmith helps create agent instructions that remain usable under context pressure, tool failures, long coding runs, and real project constraints.

## Imperatives

In user docs, soften advisory rules when possible:

> When adjusting runtime settings, treat the process like an experiment. We suggest changing one setting at a time.

In agent references, keep safety rules direct:

> Do not run destructive Git commands without explicit user approval.
