# ContextSmith

**Model-aware prompt, skill, and AGENTS.md engineering for real agent workflows.**

> ContextSmith turns messy agent instructions into model-aware operating plans that local and smaller models can actually follow.

Local agents fail in boring ways: they loop, forget context, write weak tests, overwrite files, follow hallucinated requirements, and drown in oversized AGENTS.md files.

ContextSmith is built to prevent those boring failures.

It started with small local models, where instruction quality matters most. The same operational discipline now helps across the model spectrum: local/open-weight models, coding-specialized models, reasoning models, and stronger planner models.

> The goal is not just better prompts.  
> The goal is agent instructions that remain usable under context pressure, tool failures, long coding runs, and real project constraints.

## Why ContextSmith exists

Most prompt tools optimize text.

ContextSmith optimizes the operating environment around the prompt:

- model profile and capability tier
- targeted context length
- task phase size
- AGENTS.md and repo instruction quality
- loop and Git safety
- persistent task memory
- post-phase code review
- test quality
- implementation-plan audit
- domain-specific guardrails
- upstream artifact sanity checks

The result is not just a prettier prompt. It is a more reliable agent workflow.

> A bigger context window is not a strategy.
>
> ContextSmith optimizes for the context you actually have, not the context the model card promised.

## Included skills

| Skill | Use it for |
|---|---|
| `local-model-prompt-engineer` | Create, optimize, audit, and package prompts. |
| `local-model-skill-engineer` | Create, convert, audit, and package `SKILL.md`-based skills. |
| `local-model-skill-migrator` | Safely migrate skill directories with backup, staging, manifest, and reports. |
| `local-model-instruction-engineer` | Create and improve `AGENTS.md`, `CLAUDE.md`, copilot instructions, `.cursorrules`, and related agent instruction files. |
| `local-model-agent-evaluator` | Audit prompts, skills, tests, plans, workflows, and instruction files without modifying them. |

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

## Quick start

### Optimize a prompt for a tight local coding model

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

Why it helps: compact model-facing prompt, stronger human-readable report, saved iterations, and explicit context strategy.

### Create or improve AGENTS.md

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

Why it helps: AGENTS.md is the backbone of an agentic coding project. This scans the repo, avoids duplicate safeguards, and asks for user input before locking in broad project instructions.

### Audit an implementation plan before giving it to a small model

```bash
/local-model-agent-evaluator \
  --mode audit-only \
  --focus implementation-plan \
  --target IMPLEMENTATION_PLAN.md \
  --executor-profile qwen36 \
  --context-length 32k
```

Why it helps: catches plans that are too broad, too vague, missing task memory, or not executable by a smaller local model.

### Audit tests for usefulness

```bash
/local-model-agent-evaluator \
  --mode audit-only \
  --focus test-quality \
  --target tests/ \
  --domain coding \
  --education-level guided
```

Why it helps: passing tests can still be useless. This checks baseline coverage, edge-case realism, assertion strength, regression-catching power, and over-mocking.

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

Why it helps: backs up first, stages changes, writes reports, and avoids in-place overwrite.

## Control parameters

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

See [`docs/CONTROL_PARAMETERS.md`](docs/CONTROL_PARAMETERS.md) and [`docs/EXAMPLES.md`](docs/EXAMPLES.md) for the full manual.

## Core ideas

> Strong models can write the plan. Smaller models can execute it — if the plan is atomic enough.

- Use stronger models for planning, auditing, architecture, and test strategy when available.
- Use smaller/local models for atomic phase execution.
- Use `targeted_context_length` to size phases and artifacts for the context that is actually reliable.
- Use project-local task state under `.agent-work/` for durable memory.
- End phases with debriefs, carry-forward notes, and do-not-carry-forward notes.
- Run post-phase code review and test-quality audits for coding work.

> Passing validation is not the same as being good.

ContextSmith supports bounded Ralph loops and A-F rubrics so artifacts can improve beyond bare-minimum validation without turning into endless polish.

## Project status

ContextSmith is early-stage and actively evolving.

Current validation includes:

- `SKILL.md` frontmatter parsing
- metadata/version checks
- approximate line-count checks
- reference-folder presence checks
- packaging/layout sanity checks

Not yet included:

- full automated behavioral tests
- integration tests across agent harnesses
- benchmarked model comparisons
- guaranteed compatibility with every skill runner

Use `audit-only`, `stage`, or `review-gate` mode for important changes.

## Documentation

- [`docs/USER_MANUAL.md`](docs/USER_MANUAL.md)
- [`docs/CONTROL_PARAMETERS.md`](docs/CONTROL_PARAMETERS.md)
- [`docs/EXAMPLES.md`](docs/EXAMPLES.md)
- [`docs/SMALL_CONTEXT_WORKFLOWS.md`](docs/SMALL_CONTEXT_WORKFLOWS.md)
- [`docs/AGENTS_MD_GUIDE.md`](docs/AGENTS_MD_GUIDE.md)
- [`docs/RUNTIME_STABILITY.md`](docs/RUNTIME_STABILITY.md)
- [`docs/MODEL_PROFILES.md`](docs/MODEL_PROFILES.md)
- [`docs/IMPLEMENTATION_PLAN_AUDIT.md`](docs/IMPLEMENTATION_PLAN_AUDIT.md)
- [`docs/TEST_QUALITY_AUDIT.md`](docs/TEST_QUALITY_AUDIT.md)
- [`docs/PHASE_CODE_REVIEW.md`](docs/PHASE_CODE_REVIEW.md)
- [`docs/VERSIONING.md`](docs/VERSIONING.md)

## Versioning

From v1.4.0 onward, ContextSmith follows a SemVer-style `MAJOR.MINOR.PATCH` policy. Patch releases are for docs/refinements, minor releases are for backward-compatible features, and major releases are reserved for breaking changes. Minor versions can grow past 9; `1.10.0` is a normal release, not a sign that v2 is imminent.

## Philosophy

> The best AGENTS.md files are not generic manifestos.  
> They are concise operating instructions for this repo, this harness, this model, and this risk profile.

> Speed optimizations are optional. Stability is the baseline.

> ContextSmith is small-model-first, but the operational discipline applies across the model spectrum.
