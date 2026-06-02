# ContextSmith

**Precision instruction engineering for reliable AI agents**

> ContextSmith transforms agent workflows by optimizing prompts, skills, and repo instructions for your specific models and context constraints.

## Why ContextSmith?

Smaller/local models (Qwen, Gemma, Llama) require surgical precision in instructions. ContextSmith provides:

- **Model-aware optimizations** - Tailor artifacts for specific model capabilities
- **Context-length discipline** - Design for your actual capacity (16k-128k+)
- **Atomic execution plans** - Break work into phases smaller models can execute
- **Enforced run contracts** - Execute prompts and handoffs with validation, self-audit, and Ralph evidence
- **Safety-first workflows** - Helps prevent loops, unsafe Git ops, and context bloat
- **Rich parameter system** - Control every aspect of artifact engineering

```bash
# Unsure which sub-skill to use? Start with the router.
/contextsmith help

# Sample advanced workflow
/contextsmith-prompt-engineer \
  --target-profile qwen36 \
  --context-length 32k \
  --ralph 2 \
  --education-level deep \
  --artifact-verbosity compact
```

## Core Capabilities

### Precision Engineering
- Optimize prompts for specific model profiles (Qwen, Gemma, Llama)
- Create context-aware SKILL.md files
- Generate repo-specific AGENTS.md instructions
- Migrate skills with version control

### Validation & Improvement
- Audit tests for real-world protection
- Grade implementation plans (A-F scale)
- Run bounded improvement loops (Ralph iterations)
- Conduct phase code reviews
- Execute prompts and `NEXT_PROMPT.md` handoffs with declared-vs-enforced evidence

### Advanced Controls
```bash
--target-profile qwen36|gemma4|llama3  # Model-specific optimizations
--context-length 16k|32k|64k|128k      # Design for actual capacity
--ralph 0|1|2|3                        # Improvement iterations
--phase-review brief|standard|deep      # Validation depth
--education-level guided|deep|teaching  # Explanation depth
--artifact-verbosity compact|detailed    # Output control
```

## Quick Start

**Create atomic implementation plan**
```bash
/contextsmith-instruction-engineer \
  --project . \
  --target-profile qwen36 \
  --context-length 32k
```

**Audit test quality**
```bash
/contextsmith-agent-evaluator \
  --focus test-quality \
  --target tests/ \
  --domain coding
```

**Execute a prompt or task-state handoff**
```bash
/contextsmith-run \
  --run-mode phase \
  --target .agent_work/sprints/<sprint>/tasks/<task> \
  --target-profile qwen36 \
  --interaction refine \
  --validation strict \
  --ralph 2
```

**Migrate skills safely**
```bash
/contextsmith-skill-migrator \
  --skills-dir ~/.agents/skills \
  --mode review-gate \
  --backup --stage
```

## Full Documentation

| Category | Documents |
|----------|-----------|
| **Getting Started** | [Quickstart](docs/QUICKSTART.md) • [Skill Guide](docs/WHICH_SKILL.md) • [User Guide](docs/USER_GUIDE.md) |
| **Workflows** | [Small Context Coding](docs/workflows/small-context-coding.md) • [AGENTS.md Guide](docs/workflows/agents-md-guide.md) • [Test Audits](docs/workflows/test-quality-audit.md) |
| **Concepts** | [Targeted Context](docs/concepts/targeted-context.md) • [Model Profiles](docs/concepts/model-profiles.md) • [Persistent State](docs/concepts/persistent-task-state.md) |
| **Reference** | [Parameters](docs/reference/CONTROL_PARAMETERS.md) • [Versioning](docs/reference/VERSIONING.md) • [Safety Rules](docs/reference/SAFETY_RULES.md) |

## Project Status

**Production-ready**
- Prompt engineering
- AGENTS.md generation
- Skill migration
- Test/plan audits
- Parameter-enforced prompt and handoff execution

**Active Development**
- Harness adapters (Opencode, Cursor)
- Cross-harness benchmarks
- Automated behavioral tests

## Installation

### Quick install (all skills)

```bash
cp -r skills/* ~/.agents/skills/
python scripts/validate_skills.py
```

### Package-based install (recommended)

Build verified packages with checksums, then install:

```bash
# Build all installable skill packages and the release bundle
python scripts/build_release.py --package --individual

# Install all skills
bash scripts/install_all.sh dist

# Or install a single skill
bash scripts/install_skill.sh dist/contextsmith-prompt-engineer-1.7.1.zip
```

Package-based install verifies SHA-256 checksums, backs up existing versions, and skips already-installed versions. See [RELEASE_PROCESS.md](docs/RELEASE_PROCESS.md) for the full release and installation guide.

> ContextSmith started with small models where instruction quality matters most, but its discipline improves all agent workflows. Developed by engineers for engineers.
