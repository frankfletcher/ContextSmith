# Quick Start

The easiest way to understand ContextSmith is to use it on one real artifact: a prompt, an `AGENTS.md` file, an implementation plan, a test suite, or a `SKILL.md`.

You do not need to learn the whole package first. Pick the closest workflow and run it with a few high-signal controls.

## Good default controls

For local Qwen coding work:

```bash
--mode guided --target-profile qwen36 --context-length 32k --domain coding
```

For quick cleanup:

```bash
--mode fast --target-profile generic-local --no-ralph
```

For important reusable artifacts:

```bash
--mode deep --ralph 2 --output project-local
```

For anything that may overwrite files:

```bash
--mode review-gate --backup --stage --no-apply
```

## Path 1: Improve a prompt

Use this when a prompt is vague, bloated, too frontier-model-oriented, or likely to be run by a smaller/local model.

```bash
/local-model-prompt-engineer \
  --mode deep \
  --target-profile qwen36 \
  --context-length 32k \
  --domain coding \
  --ralph 2 \
  --artifact-verbosity compact \
  --education-level guided
```

What you should get:

- an optimized prompt or prompt package
- assumptions and model/context strategy
- validation checklist
- optional test cases
- optional Ralph iteration report
- explanation of what improved and why

## Path 2: Create or improve AGENTS.md

Use this when you want better repo instructions for a coding agent.

```bash
/local-model-instruction-engineer \
  --project . \
  --mode guided \
  --target-profile qwen36 \
  --context-length 32k \
  --domain coding,data-science-ml \
  --harness opencode
```

What you should get:

- repo scan summary
- recommended instruction blocks
- choices before broad instructions are added
- Git safety and loop safety when relevant
- coding/data-science standards when detected
- concise `AGENTS.md` content, not a generic manifesto

## Path 3: Audit a plan before giving it to a small model

Use this when a strong model or another tool created an implementation plan and you want to know if a smaller model can execute it.

```bash
/local-model-agent-evaluator \
  --mode audit-only \
  --focus implementation-plan \
  --target IMPLEMENTATION_PLAN.md \
  --executor-profile qwen36 \
  --context-length 32k
```

What you should get:

- phase granularity grade
- atomicity grade
- context-fit grade
- missing task-memory notes
- validation gaps
- recommendations for splitting or rewriting phases

## Path 4: Audit tests for usefulness

Use this when tests exist but you suspect they are shallow or agent-generated fluff.

```bash
/local-model-agent-evaluator \
  --mode audit-only \
  --focus test-quality \
  --target tests/ \
  --domain coding
```

What you should get:

- baseline behavior coverage review
- edge-case realism review
- assertion-strength review
- regression-catching assessment
- over-mocking risks
- recommended test additions

## Path 5: Convert a skill safely

Use this when you have a `SKILL.md` and want it optimized for local/open-weight models without changing its behavior.

```bash
/local-model-skill-engineer \
  --source ./my-skill/SKILL.md \
  --mode guided \
  --target-profiles generic-local,qwen36 \
  --context-length 32k \
  --output staging
```

What you should get:

- source-contract extraction
- converted skill
- semantic diff
- reference audit
- target-profile metadata
- rejected unsupported additions, if any

## Path 6: Migrate many skills without clobbering originals

Use this when you want to stage changes across a whole skills directory.

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

What you should get:

- inventory
- risk classification
- backup
- staging directory
- manifest
- per-skill reports
- restore instructions

## What to read next

- Not sure which skill to use? Read `WHICH_SKILL.md`.
- Want flags and modes? Read `CONTROL_PARAMETERS.md`.
- Working with a small context window? Read `SMALL_CONTEXT_WORKFLOWS.md`.
- Creating repo instructions? Read `AGENTS_MD_GUIDE.md`.
