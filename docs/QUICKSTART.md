# Quick Start

Get your first useful ContextSmith result in under two minutes — or dive into the full five-minute paths below.

## Zero to Output (30 seconds)

New to ContextSmith? Type the skill name with no flags and answer a few questions:

```
/contextsmith
```

The wizard asks what you're working on, which model to target, and how much context it has. Then it shows you the command it will run and asks for confirmation. Three clicks, zero flag memorization.

Each sub-skill also works with zero flags, using safe defaults (generic-local model, 64k context, guided mode):

```
/contextsmith-prompt-engineer        # paste a prompt, get an optimized version
/contextsmith-instruction-engineer  # scan your project, get an AGENTS.md
/contextsmith-agent-evaluator       # audit any artifact
/contextsmith-skill-engineer        # optimize a SKILL.md
/contextsmith-skill-migrator        # migrate a directory of skills
/contextsmith-run                   # execute with enforcement
```

**Prerequisites:** ContextSmith skills installed in `~/.agents/skills/`. If you haven't installed yet, copy the `skills/` directory from the ContextSmith repo into `~/.agents/skills/`.

Pick a path below, run the command, and check the expected output.

- [5-Minute Path: Improve a Prompt](#5-minute-path-improve-a-prompt)
- [Next 30 Minutes: Plan, Audit, and Execute](#next-30-minutes-plan-audit-and-execute)
- [All Paths](#all-paths)
  - [Path 1: Improve a Prompt](#path-1-improve-a-prompt)
  - [Path 2: Create or Improve AGENTS.md](#path-2-create-or-improve-agentsmd)
  - [Path 3: Audit a Plan](#path-3-audit-a-plan)
  - [Path 4: Execute a Task-State Handoff](#path-4-execute-a-task-state-handoff)
  - [Path 5: Audit Tests](#path-5-audit-tests)
  - [Path 6: Convert a Skill](#path-6-convert-a-skill)
  - [Path 7: Migrate Many Skills](#path-7-migrate-many-skills)
- [Good Default Controls](#good-default-controls)
- [What to Read Next](#what-to-read-next)

## 5-Minute Path: Improve a Prompt

The fastest way to see ContextSmith work is to improve an existing prompt for a local model.

Run the prompt-engineering skill:

```
/contextsmith-prompt-engineer \
  --mode deep \
  --target-profile qwen36 \
  --context-length 32k \
  --ralph 2 \
  --artifact-verbosity compact
```

Paste your prompt when asked.

**Expected output:**
- An optimized prompt tailored for the target model profile
- A list of assumptions and what changed
- A validation checklist you can use to test the result

If the output includes a clearer prompt with fewer instructions and better structure for your target model, it worked.

## Next 30 Minutes: Plan, Audit, and Execute

For multi-step projects, the standard execution path goes through runtime enforcement — validation gates, phase progression, and evidence collection happen automatically. This example creates repo instructions, audits them, and runs a phase with enforcement.

**Step 1 — Create the plan.** Use the instruction engineer to generate repo instructions:

```
/contextsmith-instruction-engineer \
  --project . \
  --mode guided \
  --target-profile qwen36 \
  --harness opencode
```

**Step 2 — Audit before using.** Check the instructions are reliable for your target model:

```
/contextsmith-agent-evaluator \
  --mode audit-only \
  --target AGENTS.md \
  --executor-profile qwen36
```

**Step 3 — Execute a task with enforcement.** Run a phase with validation gates:

```
/contextsmith-run \
  --run-mode phase \
  --target .agent_work/sprints/<sprint>/tasks/<task> \
  --validation strict \
  --ralph 2
```

**Expected output after all three steps:**
- A compact `AGENTS.md` with Git safety, loop safety, and project-specific standards
- An audit report with strengths, weaknesses, and specific improvement recommendations
- Execution results with validation evidence, self-audit, and Ralph summaries

## All Paths

### Path 1: Improve a Prompt

Use this when a prompt is vague, bloated, or written for a frontier model but needs to run on a smaller/local model.

```
/contextsmith-prompt-engineer \
  --mode deep \
  --target-profile qwen36 \
  --context-length 32k \
  --domain coding \
  --ralph 2 \
  --artifact-verbosity compact \
  --education-level guided
```

**Expected output:**
- Optimized prompt or prompt package
- Assumptions and model/context strategy
- Validation checklist
- Ralph iteration report showing what improved and why

### Path 2: Create or Improve AGENTS.md

Use this when you want better repo instructions for a coding agent.

```
/contextsmith-instruction-engineer \
  --project . \
  --mode guided \
  --target-profile qwen36 \
  --context-length 32k \
  --domain coding,data-science-ml \
  --harness opencode
```

**Expected output:**
- Repo scan summary
- Recommended instruction blocks
- Concise `AGENTS.md` with Git safety, loop safety, and coding standards

### Path 3: Audit a Plan

Use this when a plan was created by a strong model and you want to verify a smaller model can execute it.

```
/contextsmith-agent-evaluator \
  --mode audit-only \
  --focus implementation-plan \
  --target IMPLEMENTATION_PLAN.md \
  --executor-profile qwen36 \
  --context-length 32k
```

**Expected output:**
- Phase granularity grade
- Atomicity grade
- Context-fit grade
- Missing task-memory notes and validation gaps
- Recommendations for splitting or rewriting phases

### Path 4: Execute a Task-State Handoff

Use this when you want ContextSmith controls enforced during execution, not only included in the prompt.

```
/contextsmith-run \
  --run-mode phase \
  --target .agent_work/sprints/<sprint>/tasks/<task> \
  --target-profile qwen36 \
  --context-length 32k \
  --interaction refine \
  --validation strict \
  --ralph 2
```

**Expected output:**
- Compact execution contract
- Domain-specific refinement questions when choices matter
- Validation evidence or a recorded blocker
- Self-audit and Ralph summary
- Declared-vs-enforced status
- Updated task state files

### Path 5: Audit Tests

Use this when tests exist but you suspect they are shallow or agent-generated fluff.

```
/contextsmith-agent-evaluator \
  --mode audit-only \
  --focus test-quality \
  --target tests/ \
  --domain coding
```

**Expected output:**
- Baseline behavior coverage review
- Edge-case realism assessment
- Assertion-strength review
- Regression-catching assessment
- Over-mocking risks and recommended additions

### Path 6: Convert a Skill

Use this when you have a `SKILL.md` and want it optimized for local/open-weight models without changing its behavior.

```
/contextsmith-skill-engineer \
  --source ./my-skill/SKILL.md \
  --mode guided \
  --target-profiles generic-local,qwen36 \
  --context-length 32k \
  --output staging
```

**Expected output:**
- Source-contract extraction
- Converted skill optimized for target profiles
- Semantic diff showing what changed
- Reference audit and target-profile metadata

### Path 7: Migrate Many Skills

Use this when you want to stage changes across a whole skills directory without clobbering originals.

```
/contextsmith-skill-migrator \
  --skills-dir ~/.agents/skills \
  --mode review-gate \
  --target-profiles generic-local,qwen36 \
  --context-length 32k \
  --backup \
  --stage \
  --no-apply
```

**Expected output:**
- Inventory and risk classification
- Backup of originals
- Staging directory with manifest
- Per-skill reports and restore instructions

## Good Default Controls

Not sure which skill to use? Start with the router:

```
/contextsmith help
```

The router selects a sub-skill based on intent and applies its own defaults for any parameters you omit.

Common control combinations:

| Use case | Controls |
|----------|----------|
| Local Qwen coding work | `--mode guided --target-profile qwen36 --context-length 32k --domain coding` |
| Quick cleanup | `--mode fast --target-profile generic-local --no-ralph` |
| Important reusable artifacts | `--mode deep --ralph 2 --output project-local` |
| Execute with enforcement | `--run-mode phase --interaction refine --validation strict --ralph 2` |
| Anything that may overwrite files | `--mode review-gate --backup --stage --no-apply` |

## What to Read Next

- Not sure which skill to use? Read [`WHICH_SKILL.md`](WHICH_SKILL.md).
- Want the full flag and mode reference? Read [`CONTROL_PARAMETERS.md`](reference/CONTROL_PARAMETERS.md).
- Working with a small context window? Read [`SMALL_CONTEXT_WORKFLOWS.md`](workflows/SMALL_CONTEXT_WORKFLOWS.md).
- Creating repo instructions? Read [`AGENTS_MD_GUIDE.md`](workflows/AGENTS_MD_GUIDE.md).
