# ContextSmith

**Prompt, skill, and AGENTS.md engineering for model-aware AI agents.**

> ContextSmith can infer a run configuration, explain the choices, and ask for correction before important work.

Local agents can do serious work when their instructions match the project, the harness, the model, and the context budget. ContextSmith helps shape those instructions: prompts, `SKILL.md` files, `AGENTS.md` files, implementation plans, reviews, and migration reports.

It is small-model-first because that is where instruction quality matters most. The same operating discipline also helps larger models: clearer plans, safer Git behavior, better tests, cleaner task state, and fewer workflow collisions.

## Why ContextSmith exists

Agent runs often fail for ordinary reasons: vague repo instructions, repeated failed tool calls, weak tests, unsafe Git operations, oversized context, or unsupported requirements inherited from another tool. ContextSmith helps you build the artifacts that prevent those failures before the run begins.

It can help you:

- turn a rough prompt into a reusable prompt package;
- create repo-aware `AGENTS.md` instructions;
- audit implementation plans before handing them to a coding agent;
- review tests for usefulness rather than pass/fail status alone;
- migrate skill directories with backup and staging;
- tune artifacts for the context length you are actually targeting.

> A bigger context window is not a strategy. ContextSmith optimizes for the context you actually plan to use.

## Quick Start

The fastest way to understand ContextSmith is to run it on one real artifact. Choose the path closest to your task.

### Improve a prompt for a tight local coding model

```bash
/local-model-prompt-engineer \
  --mode deep \
  --target-profile qwen36 \
  --context-length 32k \
  --domain coding \
  --harness opencode \
  --ralph 2 \
  --education-level guided \
  --artifact-verbosity compact \
  --output project-local
```

Use this when a prompt will be reused or will drive a coding agent. ContextSmith keeps the model-facing artifact compact, adds a context strategy, includes validation checks, and can save Ralph iterations and reports.

### Create or improve `AGENTS.md`

```bash
/local-model-instruction-engineer \
  --project . \
  --mode guided \
  --target-profile qwen36 \
  --context-length 32k \
  --domain coding,data-science-ml \
  --harness opencode \
  --phase-review standard
```

Use this when you want repo-aware operating instructions instead of generic advice. The instruction engineer scans the repo, detects relevant standards, checks existing instruction files, avoids duplicate safeguards, and asks for user input before changing broad project guidance.

### Audit an implementation plan

```bash
/local-model-agent-evaluator \
  --mode audit-only \
  --focus implementation-plan \
  --target IMPLEMENTATION_PLAN.md \
  --executor-profile qwen36 \
  --context-length 32k
```

Use this when a plan looks reasonable but may be too broad for a smaller model. The evaluator checks phase granularity, atomicity, validation, task memory, handoff quality, and targeted-context fit.

### Audit tests for usefulness

```bash
/local-model-agent-evaluator \
  --mode audit-only \
  --focus test-quality \
  --target tests/ \
  --domain coding \
  --education-level guided
```

Use this when tests pass but you are not sure they protect real behavior. ContextSmith looks for weak assertions, artificial edge cases, over-mocking, missing baseline tests, and tests that would not fail during realistic regressions.

### Migrate installed skills safely

```bash
/local-model-skill-migrator \
  --skills-dir ~/.agents/skills \
  --mode review-gate \
  --target-profiles generic-local,qwen36 \
  --context-length 32k \
  --backup \
  --stage \
  --no-apply
```

Use this when you want to modernize a directory of skills without overwriting your working setup. The migrator inventories, backs up, stages, validates, reports, and waits for approval before applying changes.

## Included skills

| Skill | Use it for |
|---|---|
| `local-model-prompt-engineer` | Create, optimize, audit, and package prompts. |
| `local-model-skill-engineer` | Create, convert, audit, and package `SKILL.md`-based skills. |
| `local-model-skill-migrator` | Migrate skill directories with backup, staging, manifests, and reports. |
| `local-model-instruction-engineer` | Create and improve `AGENTS.md`, `CLAUDE.md`, copilot instructions, `.cursorrules`, and related agent instruction files. |
| `local-model-agent-evaluator` | Audit prompts, skills, tests, plans, workflows, and instruction files without modifying them. |

Not sure which one to use? Start with [`docs/WHICH_SKILL.md`](docs/WHICH_SKILL.md).

## Install

Copy all skills into your agent skills directory:

```bash
cp -r skills/* ~/.agents/skills/
```

Install one skill:

```bash
cp -r skills/local-model-prompt-engineer ~/.agents/skills/
```

Optional validation:

```bash
python scripts/validate_skills.py
```

## Common controls

ContextSmith accepts natural language and CLI-style flags. Start with a few high-signal controls, then add more only when they matter.

```bash
--mode fast|deep|guided|yolo|review-gate|audit-only
--target-profile qwen36|gemma4|llama3|generic-local
--target-capability small-local|mid-local|large-local|frontier-cloud|reasoning-specialized|coding-specialized|multimodal
--planner-profile frontier-cloud
--executor-profile qwen36
--context-length 32k
--domain coding,data-science-ml
--harness opencode
--ralph 2
--education-level none|brief|guided|deep|teaching
--artifact-verbosity compact|normal|detailed
--phase-review off|brief|standard|deep
--code-review-iterations 0|1|2
--review-config
--output chat|project-local|staging
--backup --stage --no-apply
```

Natural language works too:

> Deep path. Target profile: qwen36. Context length: 32k. Domain: coding. Use project-local output. Ralph loop: 2.

See [`docs/reference/CONTROL_PARAMETERS.md`](docs/reference/CONTROL_PARAMETERS.md) for the full parameter guide.

## Core ideas

> Strong models can write the plan. Smaller models can execute it — if the plan is atomic enough.

Use stronger models for planning, auditing, architecture, and test strategy when available. Use smaller/local models for atomic phase execution when the plan is explicit, context-aware, and backed by durable task state.

> Passing validation is not the same as being good.

ContextSmith supports bounded Ralph loops, implementation-plan audits, phase code reviews, and test-quality audits so artifacts can improve beyond bare-minimum validation without turning into endless polish.

> The best `AGENTS.md` files are concise operating instructions for this repo, this harness, this model, and this risk profile.

## Documentation

Project documentation:

- [`docs/QUICKSTART.md`](docs/QUICKSTART.md)
- [`docs/WHICH_SKILL.md`](docs/WHICH_SKILL.md)
- [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md)
- [`docs/workflows/`](docs/workflows/)
- [`docs/concepts/`](docs/concepts/)
- [`docs/reference/`](docs/reference/)
- [`docs/contributing/documentation-style.md`](docs/contributing/documentation-style.md)

Agent references live in `shared/` and in each skill's `references/` directory. They are intentionally more compact and operational than the project documentation.

## Project Status

ContextSmith is early-stage and evolving quickly.

Currently included:

- installable skill folders;
- shared agent references;
- project documentation;
- model, domain, capability, and control-parameter guidance;
- a lightweight validation script for skill metadata, line counts, and reference presence.

Not yet included:

- full integration tests across agent harnesses;
- benchmarked model comparisons;
- a ContextSmith CLI;
- a UI;
- guaranteed support for every skill runner.

Use staged or review-gate mode for important file-changing work.

## License and Contributing

Choose the license you want for the repository before publishing. Contributions should preserve the core design goal: practical, model-aware agent instruction engineering with clear docs and low-friction workflows.
