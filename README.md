# Local Model Agent Engineering Skills

A practical toolkit for making prompts, skills, repo instructions, and agent workflows work better with local/open-weight models such as Qwen, Gemma, Llama, Mistral, Phi, DeepSeek, and similar smaller models.

Most agent instructions are written for frontier cloud models. Local models can be excellent, but they usually need more explicit instructions, tighter context control, safer tool use, and better recovery from loops or crashes. This package gives you reusable skills for that job.

## Why This Exists

Local/smaller models often struggle with:

- vague instructions that require too much inference
- overloaded context windows
- repeated failed tool calls
- malformed tool output
- generic plans that are too coarse
- lost progress after a crash or context reset
- accidental overwrite of user work
- bloated `AGENTS.md` files full of repetitive rules

These skills help by adding:

- atomic instructions
- model profiles
- domain-aware guardrails
- phased execution and memory files
- loop prevention
- Git safety
- context strategy
- validation and A-F grading
- educational change reports

## Included Skills

- `local-model-prompt-engineer` — create, optimize, audit, and test prompt packages.
- `local-model-skill-engineer` — create, convert, audit, and package `SKILL.md`-based skills.
- `local-model-skill-migrator` — safely migrate directories of skills with backup, staging, manifest, and reports.
- `local-model-instruction-engineer` — create and improve `AGENTS.md`, `CLAUDE.md`, copilot instructions, `.cursorrules`, and related agent instruction files.
- `local-model-agent-evaluator` — audit artifacts without modifying them.

## Install

Copy all skills into your agent skills directory:

```bash
cp -r skills/* ~/.agents/skills/
```

Install one skill:

```bash
cp -r skills/local-model-prompt-engineer ~/.agents/skills/
```

Recommended after cloning:

```bash
python scripts/validate_skills.py
```

## Core Concepts

### Interaction Modes

- `yolo`: proceed with safe assumptions; ask only if blocked.
- `guided`: ask 1–3 high-impact questions before major changes.
- `review-gate`: produce plan/staged output first; wait for approval before applying.
- `audit-only`: analyze and report; do not modify.
- `stage`: write outputs to staging; do not apply.
- `apply`: apply staged changes after explicit approval.

### Canonical Work Output

For project work, durable reports and iterations should go under:

```text
<project>/.agent-work/sprints/<sprint-or-subproject>/tasks/<YYYY-MM-DD-short-slug>/
```

Treat `.agent-work/` as local operational state. The skills suggest adding it to `.gitignore` rather than polluting public repos with transient agent artifacts.

### Ralph Loop

The Ralph loop is an optional bounded improvement loop. It saves each iteration, grades A-F, and asks whether the result is merely valid or actually good for smaller models.

Use it for reusable, high-risk, long-running, or important artifacts. Do not use it for every tiny prompt.

## Quick Start Examples

### 1. Optimize a seed prompt for Qwen3.6-27B

```text
/local-model-prompt-engineer
Guided mode. Optimize this seed prompt for Qwen3.6-27B. Make it literal and atomic, avoid exposed chain-of-thought, include a context strategy, and include 5 prompt test cases.

Seed prompt:
"Explain the Gini coefficient and Gini impurity to a high school data science student. Include math and a worked decision-tree example."
```

Why this is useful: the skill will turn a loose request into a structured prompt package with target model profile, assumptions, output format, examples if needed, and test cases.

### 2. Build a long-running coding-agent prompt

```text
/local-model-prompt-engineer
Deep path. Create a prompt for a local Qwen coding agent to port a large Windows/macOS desktop app to Linux. The prompt should create an 8-12 phase plan, use persistent task state, include phase closeouts, include do-not-carry-forward notes, and prevent loop/retry failures.
```

Why this is useful: large tasks need more than a three-phase plan. The skill will require phase memory files so the work can resume after context loss or harness crashes.

### 3. Convert an existing skill for local models

```text
/local-model-skill-engineer
Guided mode. Convert ./skills/find-skills/SKILL.md for generic local models and Qwen3.6. Preserve behavior, optimize references if needed, add loop/context safeguards only if relevant, and write an educational report explaining what changed.
```

Why this is useful: it avoids a naive rewrite. The skill extracts the source contract, preserves behavior, and reports what was strong, weak, changed, and risky.

### 4. Create a new skill from scratch

```text
/local-model-skill-engineer
Create a new skill named repo-port-planner. It should help local coding agents plan large cross-platform ports. Target generic local models with a Qwen3.6 profile. Include phase memory, Git safety, loop prevention, and Ralph-loop review.
```

Why this is useful: the skill generates a full `SKILL.md` structure with progressive disclosure and local-model reliability patterns.

### 5. Safely migrate all installed skills

```text
/local-model-skill-migrator
Audit and stage a migration for ~/.agents/skills. Target generic-local and qwen36 profiles. Back everything up. Do not apply changes. Produce a manifest, per-skill reports, and mark high-risk skills for manual review.
```

Why this is useful: this performs a safe batch pass without overwriting your installed skills. It stages changes, validates them, and makes restore possible.

### 6. Apply a staged migration after review

```text
/local-model-skill-migrator
Apply the staged migration at ~/.agents/skill-migrations/2026-05-local-model-migration only if validation passed. Show me the files that will be overwritten first and ask for final approval.
```

Why this is useful: batch editing should never be fire-and-forget. This forces an approval gate before real changes.

### 7. Create AGENTS.md for a coding repo

```text
/local-model-instruction-engineer
Guided mode. Create an AGENTS.md for this repo targeting OpenCode and Qwen3.6. Scan the repo first. Include setup/build/test commands, coding standards, Git safety, loop prevention, context strategy, and .agent-work gitignore suggestions. Do not use emojis.
```

Why this is useful: it produces repo-aware instructions instead of generic boilerplate. It scans the project before deciding which standards apply.

### 8. Improve an existing AGENTS.md without duplicating rules

```text
/local-model-instruction-engineer
Improve the existing AGENTS.md for smaller local coding models. First scan AGENTS.md, CLAUDE.md, and .github/copilot-instructions.md. Reuse or strengthen existing safeguards instead of duplicating them. Add missing Git safety, loop prevention, and validation rules only where needed.
```

Why this is useful: it avoids token bloat from repeated guardrails. The skill follows detect → reuse → strengthen → consolidate → add only what is missing.

### 9. Add data science / ML standards to a repo

```text
/local-model-instruction-engineer
Create or update AGENTS.md for this data science repo. Detect the stack first. Add Python, PEP 8, notebook, data handling, leakage prevention, evaluation, reproducibility, and artifact-handling instructions only if relevant.
```

Why this is useful: ML agents need more than normal coding rules. This adds safeguards for leakage, evaluation, random seeds, model artifacts, and raw data handling.

### 10. Evaluate an artifact before changing it

```text
/local-model-agent-evaluator
Audit this AGENTS.md for local-model reliability. Do not edit it. Grade A-F for atomicity, loop safety, Git safety, context strategy, domain fit, validation strength, and bloat. Recommend whether to ship, iterate, or use the instruction engineer.
```

Why this is useful: sometimes you want diagnosis before mutation. The evaluator gives a clear quality report without touching files.

### 11. Evaluate a phase plan

```text
/local-model-agent-evaluator
Audit this implementation plan for a small local model. Check whether the phases are too coarse, whether durable memory files are included, whether stop conditions are clear, and whether phase debrief / do-not-carry-forward notes are required.
```

Why this is useful: it catches the common failure where a big project gets compressed into a vague three-phase plan.

## Recommended Defaults

- Use `guided` mode for reusable artifacts.
- Use `review-gate` for migrations, Git changes, external side effects, or high-risk domains.
- Use Ralph loop only for important artifacts.
- Keep `.agent-work/` local and gitignored by default.
- Prefer one crisp safeguard over five similar reminders.

## What This Will Not Do

This package will not:

- guarantee a small model can do any task
- bypass harness limitations
- make runtime settings controllable if the harness does not expose them
- safely automate destructive Git operations without approval
- replace tests, source verification, or human review
- prevent all loops if the harness ignores instructions

## Package Layout

This repo uses Option C: canonical shared references plus per-skill copied references. Each skill can be installed standalone, while `shared/` remains the canonical source for future syncing.
