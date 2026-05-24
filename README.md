# ContextSmith

**Prompt, skill, and AGENTS.md engineering for model-aware AI agents.**

> ContextSmith turns messy agent instructions into operating plans that models can actually follow.

Local and smaller models can do serious work, but they are unforgiving. They loop. They lose the thread. They write tests that pass but do not protect anything. They follow hallucinated requirements from upstream tools. They overwrite files when the repo state is unclear. They burn context on long explanations when what they need is the next atomic step.

ContextSmith is built for that reality.

It helps you engineer the artifacts that shape agent behavior:

- prompts
- `SKILL.md` files
- `AGENTS.md` and repo instruction files
- implementation plans
- test-quality reviews
- migration reports
- long-running task state

> The goal is not just better prompts.  
> The goal is agent instructions that remain usable under context pressure, tool failures, long coding runs, and real project constraints.

## Why ContextSmith exists

Most prompt tools optimize the text of a prompt.

ContextSmith optimizes the operating environment around the prompt:

- the model profile or capability tier
- the context length you are actually targeting
- how large each phase should be
- what the agent should read first
- when to ask the user for input
- how to avoid loops and unsafe Git operations
- how to preserve task memory across sessions
- how to review implementation plans and tests
- how to reject unsupported requirements from upstream tools
- how to make `AGENTS.md` useful instead of generic

The result is not just a prettier prompt. It is a more reliable agent workflow.

> A bigger context window is not a strategy.  
> ContextSmith optimizes for the context you actually have, not the context the model card promised.

## Quick Start

The fastest way to understand ContextSmith is to run it on one real artifact.

Choose the path closest to what you are doing:

- improve a prompt for a local/open-weight model
- create or refine an `AGENTS.md` file for a repo
- audit an implementation plan before handing it to a coding agent
- convert a `SKILL.md` for smaller/local models
- evaluate tests, prompts, skills, or repo instructions without changing files

You do not need to learn every control parameter first. Start with a few high-signal controls:

```bash
--mode guided --target-profile qwen36 --context-length 32k
```

Add more controls only when they matter.

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

Use this when a prompt will be reused or will drive a coding agent. ContextSmith will keep the model-facing artifact compact, add a context strategy, include validation checks, and optionally save Ralph iterations and reports.

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

Use this when you want a repo-aware instruction file instead of a generic manifesto. The instruction engineer scans the repo, detects relevant standards, checks existing instruction files, avoids duplicate safeguards, and asks for user input before locking in broad project instructions.

### Audit an implementation plan before giving it to a small model

```bash
/local-model-agent-evaluator \
  --mode audit-only \
  --focus implementation-plan \
  --target IMPLEMENTATION_PLAN.md \
  --executor-profile qwen36 \
  --context-length 32k
```

Use this when a plan looks reasonable but may be too broad for a smaller model. The evaluator checks phase granularity, atomicity, validation, task memory, handoff quality, and whether the plan can be executed under the targeted context length.

### Audit tests for usefulness

```bash
/local-model-agent-evaluator \
  --mode audit-only \
  --focus test-quality \
  --target tests/ \
  --domain coding \
  --education-level guided
```

Use this when tests pass but you are not sure they protect real behavior. ContextSmith looks for weak assertions, fake edge cases, over-mocking, missing baseline tests, and tests that would not fail during realistic regressions.

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

Use this when you want to modernize a directory of skills without overwriting your working setup. The migrator inventories, backs up, stages, validates, reports, and waits for explicit approval before applying changes.

## Included skills

| Skill | Use it for |
|---|---|
| `local-model-prompt-engineer` | Create, optimize, audit, and package prompts. |
| `local-model-skill-engineer` | Create, convert, audit, and package `SKILL.md`-based skills. |
| `local-model-skill-migrator` | Safely migrate skill directories with backup, staging, manifest, and reports. |
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

ContextSmith accepts natural language and CLI-style flags.

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
--output chat|project-local|staging
--backup --stage --no-apply
```

You can also write the same controls naturally:

> Deep path. Target profile: qwen36. Context length: 32k. Domain: coding. Use project-local output. Ralph loop: 2.

See [`docs/CONTROL_PARAMETERS.md`](docs/CONTROL_PARAMETERS.md) for the full parameter guide.

## Core ideas

> Strong models can write the plan. Smaller models can execute it — if the plan is atomic enough.

ContextSmith is small-model-first, but the operational discipline applies across the model spectrum. Use stronger models for planning, auditing, architecture, and test strategy when available. Use smaller/local models for atomic phase execution when the plan is explicit, context-aware, and backed by durable task state.

> Passing validation is not the same as being good.

ContextSmith supports bounded Ralph loops, implementation-plan audits, phase code reviews, and test-quality audits so artifacts can improve beyond bare-minimum validation without turning into endless polish.

> The best `AGENTS.md` files are not generic manifestos.  
> They are concise operating instructions for this repo, this harness, this model, and this risk profile.

## Documentation

Human-facing docs:

- [`docs/QUICKSTART.md`](docs/QUICKSTART.md)
- [`docs/WHICH_SKILL.md`](docs/WHICH_SKILL.md)
- [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md)
- [`docs/CONTROL_PARAMETERS.md`](docs/CONTROL_PARAMETERS.md)
- [`docs/EXAMPLES.md`](docs/EXAMPLES.md)
- [`docs/FAQ.md`](docs/FAQ.md)

Workflow guides:

- [`docs/SMALL_CONTEXT_WORKFLOWS.md`](docs/SMALL_CONTEXT_WORKFLOWS.md)
- [`docs/AGENTS_MD_GUIDE.md`](docs/AGENTS_MD_GUIDE.md)
- [`docs/IMPLEMENTATION_PLAN_AUDIT.md`](docs/IMPLEMENTATION_PLAN_AUDIT.md)
- [`docs/TEST_QUALITY_AUDIT.md`](docs/TEST_QUALITY_AUDIT.md)
- [`docs/PHASE_CODE_REVIEW.md`](docs/PHASE_CODE_REVIEW.md)
- [`docs/RUNTIME_STABILITY.md`](docs/RUNTIME_STABILITY.md)
- [`docs/SKILL_MIGRATION.md`](docs/SKILL_MIGRATION.md)
- [`docs/MODEL_PROFILES.md`](docs/MODEL_PROFILES.md)
- [`docs/VERSIONING.md`](docs/VERSIONING.md)

## Project status

ContextSmith is early-stage and actively evolving.

Currently included:

- installable skill folders
- shared reference docs
- model/domain/control parameter guidance
- copied per-skill references for standalone installs
- lightweight validation script for skill metadata, references, and layout sanity checks

Not yet included:

- full automated behavioral tests
- integration tests across agent harnesses
- benchmark results across models/harnesses
- a ContextSmith CLI
- a UI
- guaranteed support for every skill runner

Use `audit-only`, `stage`, or `review-gate` mode for important changes.

## Versioning

From v1.4.0 onward, ContextSmith follows a SemVer-style `MAJOR.MINOR.PATCH` policy. Patch releases are for docs/refinements, minor releases are for backward-compatible features, and major releases are reserved for breaking changes. Minor versions can grow past 9; `1.10.0` is a normal release, not a sign that v2 is imminent.

## Philosophy

> Speed optimizations are optional. Stability is the baseline.

> ContextSmith is model-aware agent instruction engineering. It started with small local models, where instruction quality matters most, but the same discipline improves larger-model agent workflows too.
