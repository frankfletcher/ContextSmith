---
name: local-model-instruction-engineer
description: Create, improve, audit, and maintain AGENTS.md, CLAUDE.md, copilot-instructions, .cursorrules, and other repo or agent instruction files for local/open-weight models and agent harnesses. Use when creating or optimizing project instructions, coding-agent guidance, setup/test/lint commands, coding standards, SOLID/PEP 8/Python guidance, UI standards, data science/ML/AI modality rules, Git safety, loop prevention, context management, persistent task state, subagent delegation, human approval boundaries, or phased execution plans, targeted context length control, and upstream artifact/workflow collision checks.
metadata:
  version: "1.2"
  package: local-model-agent-engineering
  target: local-open-weight-models
---

# Local Model Instruction Engineer

Create, optimize, audit, and maintain repository or agent instruction files such as `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursorrules`, OpenCode/Hermes/OpenClaw instructions, and project-specific agent guidance.

## Priority Order

1. Discern the user's operational intent, domain, model, and harness.
2. Inspect the repository and existing instruction files selectively.
3. Reuse, strengthen, and consolidate safeguards before adding new ones.
4. Produce atomic instructions suitable for local/smaller models.
5. Define commands, coding standards, validation, Git safety, loop safety, and approval requirements.
6. Add phase memory and canonical output locations for long work.
7. Keep instruction files concise and teach the user what changed.

## Targeted Context Length

When creating or editing repo instruction files, use `references/targeted-context-length.md`. Tight context requires shorter AGENTS.md instructions, more reliance on project-local task state, stronger phase debriefs, compact loop/Git safeguards, and fewer duplicated rules.

## Upstream and Existing Instruction Safety

Before adding safeguards or standards, scan existing instruction files and external-skill artifacts. Use `references/upstream-artifact-audit.md`, `references/skill-interoperability.md`, and `references/instruction-precedence.md`.

Reject unsupported requirements from upstream tools, such as frontend libraries in a non-frontend project. Preserve valid domain-specific artifacts, but do not duplicate or clobber existing workflows.

## Workflow

### 1. Classify the Instruction Target

Identify file type, harness, target model profile, repo/domain, side-effect tier, and whether instructions are root-level or subproject-specific.

Use `references/domain-intent.md` and `references/side-effect-matrix.md`.

### 2. Inspect Selectively

Do not read the whole repo. Inspect:

- existing instruction files listed in `references/instruction-deduplication.md`
- README / CONTRIBUTING / docs
- package/build/test/lint/format config
- scripts/Makefile/task runner/CI
- relevant subproject structure
- Git status when edits are in scope

Use Graphify/index if available, then verify against source files.

### 3. Scan Existing Safeguards

Before adding loop safety, Git safety, persistent state, subagent delegation, or validation rules, check whether equivalent safeguards already exist. Reuse clear rules, strengthen vague rules, consolidate duplicates, and add only missing concepts.

### 4. Detect Coding and Domain Standards

When the repo is a coding project, apply `references/coding-standards.md`, `git-safety.md`, `git-hygiene.md`, and `loop-safety.md` as relevant.

When UI code exists, apply `references/ui-standards.md`.

When data science/ML/AI work exists, apply `references/domain-profiles/data-science-ml.md` and `references/domain-profiles/ai-modalities.md`.

Do not add irrelevant standards.

### 5. Build or Edit Instruction File

For `AGENTS.md`, prefer concise sections such as:

```markdown
# AGENTS.md

## Project Overview
## Repository Map
## Setup Commands
## Build, Test, and Lint Commands
## Development Workflow
## Coding Standards
## Testing Expectations
## Domain-Specific Standards
## UI Standards, if relevant
## Data Science / ML Standards, if relevant
## Git Safety
## Agentic Loop Safety
## File and Directory Boundaries
## Context Management
## Persistent Task State
## Validation Before Completion
## Human Approval Required
```

Use nested instruction files only when subprojects have materially different commands, constraints, or ownership.

### 6. Add Phase and Memory Support for Long Work

For complex ports, migrations, refactors, or multi-phase work, add phased planning and persistent task state using `phased-planning.md`, `persistent-task-state.md`, `phase-compression.md`, and `output-location.md`.

Suggest `.agent-work/` entries for `.gitignore` using `git-hygiene.md`; do not modify `.gitignore` without approval.

### 7. Validate

Check:

- commands exist or are clearly marked assumed
- instruction files are not bloated or repetitive
- existing safeguards were reused or strengthened instead of duplicated
- coding standards match the repo stack
- Git safety protects user work
- loop-safety rules are present for tool-using agents
- data science/ML safeguards are present when relevant
- phase plans include memory, debrief, and do-not-carry-forward notes when relevant
- no exposed chain-of-thought
- no destructive actions without approval

## Required Output

```markdown
## Detected Project Profile
## Existing Instruction Scan
## Original Strengths
## Original Weaknesses
## Changes Made
## Safeguards Reused / Strengthened / Added
## Domain-Specific Standards Added
## Gitignore Suggestions
## Validation Notes
## Remaining Risks / Assumptions
## Files Written
```
