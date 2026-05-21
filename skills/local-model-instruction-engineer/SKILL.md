---
name: local-model-instruction-engineer
description: Create, improve, audit, and maintain AGENTS.md, CLAUDE.md, copilot-instructions, .cursorrules, and other repo or agent instruction files for local/open-weight models and agent harnesses. Use when creating or optimizing project instructions, coding-agent guidance, setup/test/lint commands, domain guardrails, context management, persistent task state, subagent delegation, human approval boundaries, or phased execution plans.
metadata:
  version: "1.0"
  package: local-model-agent-engineering
  target: local-open-weight-models
---

# Local Model Instruction Engineer

Create, optimize, audit, and maintain repository or agent instruction files such as `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursorrules`, OpenCode/Hermes/OpenClaw instructions, and project-specific agent guidance.

## Priority Order

1. Discern the user's operational intent and domain.
2. Inspect the repository selectively.
3. Produce atomic instructions suitable for local/smaller models.
4. Define commands, boundaries, validation, and approval requirements.
5. Avoid exposed chain-of-thought.
6. Keep instruction files concise and maintainable.
7. Teach the user what changed.

## Workflow

### 1. Classify the Instruction Target

Identify the file type, agent harness, target model profile, repo/domain, side effects, and whether instructions are root-level or subproject-specific.

### 2. Inspect Selectively

Do not read the whole repo. Inspect:

- existing instruction files
- README / CONTRIBUTING / docs
- package/build config files
- test/lint/format config
- scripts/Makefile/task runner
- relevant subproject structure

Use Graphify/index if available, then verify against source files.

### 3. Determine Interaction Mode

Use `references/interaction-modes.md`. For repo-wide instruction files, default to guided mode unless the user requests YOLO. Use review-gate for high side-effect domains.

### 4. Build the Instruction File

For `AGENTS.md`, prefer sections like:

```markdown
# AGENTS.md

## Project Overview
## Repository Map
## Setup Commands
## Build, Test, and Lint Commands
## Development Workflow
## Code Style
## Testing Expectations
## Security and Secrets
## File and Directory Boundaries
## Context Management
## Persistent Task State
## Subagent Delegation
## Validation Before Completion
## Human Approval Required
```

Use nested instruction files only when subprojects have materially different commands, constraints, or ownership.

### 5. Add Phase and Memory Support for Long Work

For complex ports, migrations, refactors, or multi-phase work, add phased planning and persistent task state using `references/phased-planning.md` and `references/persistent-task-state.md`.

### 6. Validate

Check:

- commands exist or are clearly marked assumed
- paths are correct
- setup/build/test/lint instructions are actionable
- generated/vendor/build directories are excluded where appropriate
- security/secrets instructions are present
- validation steps are explicit
- instructions are atomic enough for smaller models
- no exposed chain-of-thought
- domain guardrails are appropriate
- human approval boundaries are clear

### 7. Optional Ralph Loop

Use bounded iteration from `references/ralph-loop.md` when creating reusable or high-value instruction files. Save each iteration.

## Required Output

Return changed files plus educational report: original strengths, original weaknesses, changes made, why this improves local-model reliability, and remaining risks.
