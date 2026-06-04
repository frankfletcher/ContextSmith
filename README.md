# ContextSmith

Model-aware agent instruction engineering. Create prompts, skills, and repo instructions that stay reliable under context pressure, tool failures, and long-running tasks.

- [The Problem](#the-problem)
- [What You Get](#what-you-get)
- [Quick Start](#quick-start)
- [Sub-Skills](#sub-skills)
- [Runtime Enforcement](#runtime-enforcement)
- [Documentation](#documentation)
- [Project Status](#project-status)
- [Installation](#installation)

## The Problem

When an agent runs a multi-step task, requirements get lost. Validation steps get skipped. Resuming after an interruption means re-reading everything from the top. ContextSmith addresses this with structured artifacts, explicit phase boundaries, and runtime validation.

## What You Get

- **Prompts** optimized for specific model profiles and context budgets
- **SKILL.md skills** with model-aware instructions and reference packs
- **AGENTS.md files** that keep coding agents on track across long sessions
- **Runtime validators** that check artifacts, domain packs, and workflow closeouts
- **Task-state handoffs** with validation, self-audit, and Ralph improvement loops

## Quick Start

Install the skills, then invoke a sub-skill with the parameters you need:

```bash
# Install all skills
cp -r skills/* ~/.agents/skills/
python scripts/validate_skills.py

# Or build verified packages with checksums
python scripts/build_release.py --package --individual
bash scripts/install_all.sh dist
```

```bash
# Optimize a prompt for a specific model
/contextsmith-prompt-engineer \
  --target-profile qwen36 \
  --context-length 32k \
  --ralph 2

# Audit an existing artifact without modifying it
/contextsmith-agent-evaluator \
  --focus test-quality \
  --target tests/ \
  --domain coding

# Execute a task-state handoff with enforcement
/contextsmith-run \
  --run-mode phase \
  --target .agent_work/sprints/<sprint>/tasks/<task> \
  --validation strict \
  --ralph 2
```

Not sure which sub-skill to use? Try `/contextsmith help`.

## Sub-Skills

| Sub-Skill | Use When |
|-----------|----------|
| `contextsmith-prompt-engineer` | Create or improve a prompt for a specific model |
| `contextsmith-skill-engineer` | Build or adapt a SKILL.md agent skill |
| `contextsmith-skill-migrator` | Migrate skills between profiles or installations |
| `contextsmith-instruction-engineer` | Create or edit AGENTS.md, CLAUDE.md, or repo instructions |
| `contextsmith-agent-evaluator` | Audit or grade an existing artifact |
| `contextsmith-run` | Execute a prompt or task-state handoff with controls |

## Runtime Enforcement

Runtime reinforcement and orchestration is a first-class ContextSmith tool. It is the **default execution path** — users get validation, gate enforcement, and phase progression automatically — but it is **opt-out, not mandatory**. A workflow can skip runtime checks, but the standard path goes through them.

**Enforcement levels** (use these labels everywhere):

| Level | Meaning |
|---|---|
| Deterministic validation | A tool checks artifacts and returns pass/fail evidence. Foundation for all enforcement. |
| Orchestrated workflow enforcement | Default mode. A runner only advances if validators pass. Opt-out available, not the norm. |
| Harness hard blocking | Elevates orchestrated gates to hard blocks where the harness supports it. |
| Human approval | A person must approve an irreversible, costly, private, or high-risk action. |

The validator CLI checks artifact structure, domain-pack compliance, and workflow closeout requirements:

```bash
# Validate a domain pack
python -m runtime.cli domain-pack runtime/domain_packs/software_engineering.json

# Validate a phase closeout
python -m runtime.cli closeout .agent_work/.../closeout.json
```

**Available:** Validator CLI, 6 domain packs (software, writing, research, scheduling, travel/purchase, general fallback), Next Prompt Compiler, Runner skeleton, contextsmith-run pilot integration.

**Active development:** MCP adapter, Harness adapter.

See [Runtime Stability](docs/RUNTIME_STABILITY.md) for details.

## Documentation

| Path | What |
|------|------|
| [Quickstart](docs/QUICKSTART.md) | Fastest path to a useful result |
| [Which Skill](docs/WHICH_SKILL.md) | Choose the right sub-skill for your task |
| [User Guide](docs/USER_GUIDE.md) | General usage and workflow patterns |
| [Examples](docs/EXAMPLES.md) | Example workflows and expected outputs |
| [Workflows](docs/workflows/README.md) | Detailed how-to guides |
| [Concepts](docs/concepts/README.md) | Model profiles, Ralph loop, context budgets |
| [Reference](docs/reference/README.md) | Parameters, versioning, safety rules |
| [FAQ](docs/FAQ.md) | Common questions |

## Project Status

**Production-ready:** prompt engineering, AGENTS.md generation, skill migration, test/plan audits, parameter-enforced handoff execution, runtime validator CLI with 6 domain packs.

**Active development:** MCP adapter, harness adapter, orchestrated runner, cross-harness benchmarks.

## Installation

### Package-based install (recommended)

```bash
python scripts/build_release.py --package --individual
bash scripts/install_all.sh dist
```

Verifies SHA-256 checksums, backs up existing versions, and skips already-installed versions. See [RELEASE_PROCESS.md](docs/RELEASE_PROCESS.md) for the full guide.

### Quick install

```bash
cp -r skills/* ~/.agents/skills/
python scripts/validate_skills.py
```

---

ContextSmith started with small models where instruction quality matters most. The same practices improve agent workflows for larger models too.
