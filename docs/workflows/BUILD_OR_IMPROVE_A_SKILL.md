# Build or Improve a Skill: Step-by-Step

Use this workflow when you need to create a new SKILL.md-based agent skill, adapt an existing skill for a different model profile, or improve a skill's instructions and references.

## Table of Contents

- [When to Use This Workflow](#when-to-use-this-workflow)
- [Inputs](#inputs)
- [Step 1: Define the Skill Scope](#step-1-define-the-skill-scope)
- [Step 2: Invoke the Skill Engineer](#step-2-invoke-the-skill-engineer)
- [Step 3: Review the Skill](#step-3-review-the-skill)
- [Step 4: Validate](#step-4-validate)
- [Step 5: Audit (Optional)](#step-5-audit-optional)
- [Expected Artifacts](#expected-artifacts)
- [Common Failure Modes](#common-failure-modes)

## When to Use This Workflow

Use this workflow for:
- Creating a new skill from scratch
- Adapting an existing skill for smaller or local models
- Improving skill instructions, references, or model profiles
- Adding loop safety, Git safety, or context management to a skill

If you need to migrate a directory of skills to a new location or profile, see [Skill Migration](SKILL_MIGRATION.md) instead.

## Inputs

- Skill name and purpose
- Target model profile (e.g., `qwen36`, `gemma-27b`, `llama-8b`)
- Existing skill to adapt (if improving an existing one)
- Domain and side-effect tier

## Step 1: Define the Skill Scope

Decide what the skill does, what it does not do, and which model profiles it targets.

**Example scope:**
```
Skill: code-review-assistant
Purpose: Review pull requests for security issues and style violations
Target: qwen36 and larger models
Domain: software engineering
Side effects: read-only (reviews code, does not edit)
```

## Step 2: Invoke the Skill Engineer

Use the `contextsmith-skill-engineer` skill to build or improve the skill.

**Example prompt for new skill:**
```
Create a new skill called code-review-assistant.
Target profile: qwen36.
Domain: software engineering.
The skill should review PRs for security issues and style violations.
Include loop safety rules and a compact reference set.
```

**Example prompt for improving an existing skill:**
```
Improve the code-review-assistant skill for smaller models.
Target profile: llama-8b.
Reduce context usage, add explicit stop conditions,
and optimize the reference set for 32k context windows.
```

The agent will create or update:
- `SKILL.md` — skill instructions with frontmatter
- `references/` — skill-specific reference files
- `reference_manifest.yml` — shipped reference declarations

## Step 3: Review the Skill

Before using the skill, check:

1. **Line count** — SKILL.md should be under 500 lines
2. **Frontmatter** — YAML block with `name`, `description`, and `metadata.version`
3. **Model profiles** — instructions match the target model's capabilities
4. **Loop safety** — rules to prevent repeated tool calls and infinite loops
5. **Reference set** — only necessary references, not bulk-loaded
6. **Side-effect boundaries** — clear approval requirements for external actions

## Step 4: Validate

Run the project validation commands:

```bash
python scripts/validate_skills.py
python scripts/token_budget.py --strict
```

`validate_skills.py` checks SKILL.md frontmatter, line counts, and reference directory presence.

`token_budget.py --strict` verifies the skill is within its declared token budget. If the budget is exceeded, reduce instruction verbosity or move detailed content to `references/` files.

## Step 5: Audit (Optional)

For a quality check without modifying the skill, use the `contextsmith-agent-evaluator` skill:

```
Audit the code-review-assistant skill.
Give me an A-F grade with strengths, weaknesses, and specific fixes.
```

The evaluator will check for context risk, loop safety, Git/file safety, model-profile alignment, and instruction clarity.

## Expected Artifacts

| Artifact | Purpose |
|----------|---------|
| `SKILL.md` | Skill instructions and frontmatter |
| `references/` | Skill-specific reference files |
| `reference_manifest.yml` | Declarations for shipped references |

## Common Failure Modes

| Problem | Fix |
|---------|-----|
| SKILL.md exceeds 500 lines | Move detailed content to `references/` files |
| Token budget exceeded | Reduce instruction verbosity; use compact tables instead of prose |
| Missing frontmatter | Add YAML frontmatter with `name`, `description`, and `metadata.version` |
| Skill too generic for small models | Add explicit stop conditions, bounded loops, and concrete file paths |
| Reference set too large | Keep only references the skill actually loads; use manifest for the rest |
| Frontmatter validation fails | Run `python scripts/validate_skills.py` and fix reported issues |
