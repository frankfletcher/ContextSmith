# Local Model Agent Engineering Skills

A practical toolkit for making prompts, skills, repo instructions, and agent workflows work better with local/open-weight models such as Qwen, Gemma, Llama, Mistral, Phi, DeepSeek, and similar smaller models.

Most agent instructions are written for frontier cloud models. Local models can be excellent, but they usually need more explicit instructions, tighter context control, safer tool use, and better recovery from loops or crashes. This package gives you reusable skills for that job.

## Why This Exists

Local/smaller models often struggle with:

- vague instructions that require too much inference
- overloaded or locally capped context windows
- repeated failed tool calls
- malformed tool output
- generic plans that are too coarse
- lost progress after a crash or context reset
- accidental overwrite of user work
- hallucinated requirements from chained prompt optimizers or other skills
- bloated `AGENTS.md` files full of repetitive rules

These skills help by adding:

- atomic instructions
- model profiles
- targeted context-length adaptation
- domain-aware guardrails
- phased execution and memory files
- loop prevention
- Git safety
- context strategy
- validation and A-F grading
- upstream artifact audits
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

## How To Drive These Skills

Use these control phrases naturally. They are the steering wheel for the package.

| Control phrase | Meaning |
|---|---|
| `fast path` | Concise one-pass improvement with minimal questions and minimal reports. |
| `deep path` | Stronger analysis, richer audit, optional Ralph loop, saved iterations when useful. |
| `guided mode` | Ask 1-3 high-impact questions before major choices. |
| `yolo mode` | Proceed with reasonable assumptions unless blocked. |
| `review-gate mode` | Plan or stage first; ask before applying changes. |
| `audit only` | Analyze and report; do not modify files. |
| `stage only` | Write output to staging; do not overwrite originals. |
| `apply` | Apply already-staged changes after validation and approval. |
| `no ralph loop` | Disable iterative refinement. |
| `ralph loop: 2` | Run up to two improvement iterations, saving each one. |
| `target profile: qwen36` | Use a model-specific profile. |
| `target profiles: generic-local, qwen36` | Optimize for a group of model profiles. |
| `harness: opencode` | Adapt instructions to a known agent harness when supported. |
| `domain: data-science-ml` | Apply domain-specific standards and safeguards. |
| `targeted context length: 32k` | Optimize artifacts for the stated usable context budget. |
| `project-local output` | Save durable reports and iterations under `<project>/.agent-work/`. |
| `chat-only output` | Return the result in chat; avoid writing files unless required. |
| `backup first` | Create backups before edits or migrations. |
| `do not apply` | Do not overwrite originals or perform in-place changes. |

### Why `targeted context length` matters

A model may advertise 128k or 256k context, but your local runtime may be capped at 32k, 64k, or 100k. The skills optimize for the targeted context length you provide, not the model card.

Example:

```text
target profile: qwen36
targeted context length: 32k
```

This should produce shorter prompts, more granular phases, fewer examples, more persistent state, stricter output budgets, and more selective reading than the same task at 128k.

## Best Practices

1. Use `guided mode` for important reusable artifacts.
2. Use `fast path` for small one-off improvements.
3. Use `deep path` when the output will be reused, shared, or used by a coding agent.
4. Use `review-gate mode` for batch migrations, Git-sensitive work, external side effects, or high-risk domains.
5. Specify the target profile when you know it: `qwen36`, `gemma4`, `llama3`, or `generic-local`.
6. Specify `targeted context length` when your local runtime context is capped.
7. Specify the harness when relevant: `opencode`, `codex`, `cursor`, `aider`, `generic-agent`.
8. Specify the domain when relevant: `coding`, `data-science-ml`, `email`, `research`, `document-processing`, etc.
9. For project work, prefer project-local output under `.agent-work/`.
10. Use `audit only` when you want diagnosis before modification.
11. Use `stage only` when you want generated changes without overwriting originals.
12. When chaining this package with other skills, ask for an upstream artifact audit to catch hallucinated requirements.

## Quick Start Examples

### 1. Optimize a seed prompt for Qwen3.6-27B

```text
/local-model-prompt-engineer
Guided mode. Target profile: qwen36. Targeted context length: 64k.
Optimize this seed prompt. Make it literal and atomic, avoid exposed chain-of-thought, include a context strategy, and include 5 prompt test cases.

Seed prompt:
"Explain the Gini coefficient and Gini impurity to a high school data science student. Include math and a worked decision-tree example."
```

Benefit: turns a loose request into a structured prompt package with model profile, assumptions, output format, examples if needed, and test cases.

### 2. Build a long-running coding-agent prompt under tight context

```text
/local-model-prompt-engineer
Deep path. Target profile: qwen36. Targeted context length: 32k.
Create a prompt for a local coding agent to port a large Windows/macOS desktop app to Linux.
Use 8-12 small phases, persistent task state, phase debriefs, do-not-carry-forward notes, loop safety, and Git safety.
Project-local output. Ralph loop: 2.
```

Benefit: avoids the common failure where a huge port is compressed into a vague three-phase plan that causes context churn.

### 3. Optimize a prompt that another optimizer already changed

```text
/local-model-prompt-engineer
Audit and improve this prompt for generic local models.
Another optimizer modified it first. Run an upstream artifact audit and reject unsupported requirements.
The target project is an MCP server, not a frontend app.
Targeted context length: 32k.
```

Benefit: catches hallucinated dependencies such as React/Vite/Tailwind when they were never part of the project.

### 4. Convert an existing skill for local models

```text
/local-model-skill-engineer
Guided mode. Convert ./skills/find-skills/SKILL.md for generic local models and Qwen3.6.
Targeted context length: 64k.
Preserve behavior, optimize references if needed, add safeguards only if relevant, and write an educational report explaining what changed.
```

Benefit: extracts and preserves the source contract instead of performing a generic rewrite.

### 5. Create a new skill from scratch

```text
/local-model-skill-engineer
Create a new skill named repo-port-planner.
Target profiles: generic-local, qwen36. Targeted context length: 32k.
It should help local coding agents plan large cross-platform ports.
Include phase memory, Git safety, loop prevention, upstream artifact audit, and Ralph-loop review.
```

Benefit: generates a full `SKILL.md` structure with progressive disclosure and local-model reliability patterns.

### 6. Safely migrate all installed skills

```text
/local-model-skill-migrator
Review-gate mode. Audit and stage a migration for ~/.agents/skills.
Target profiles: generic-local, qwen36. Targeted context length: 32k.
Back everything up. Do not apply changes.
Process in small batches if needed. Produce a manifest, per-skill reports, and mark high-risk skills for manual review.
```

Benefit: performs a safe batch pass without overwriting installed skills. Tight context changes batch sizing and report verbosity.

### 7. Apply a staged migration after review

```text
/local-model-skill-migrator
Apply the staged migration at ~/.agents/skill-migrations/2026-05-local-model-migration only if validation passed.
Show me the files that will be overwritten first and ask for final approval.
```

Benefit: batch editing should never be fire-and-forget. This forces an approval gate before real changes.

### 8. Create AGENTS.md for a coding repo

```text
/local-model-instruction-engineer
Guided mode. Create an AGENTS.md for this repo targeting OpenCode and Qwen3.6.
Targeted context length: 32k. Domain: coding, data-science-ml.
Scan the repo first. Include setup/build/test commands, coding standards, Git safety, loop prevention, context strategy, phase debriefs, and .agent-work gitignore suggestions.
Do not use emojis.
```

Benefit: creates repo-aware instructions, not boilerplate. It adds only standards supported by the repo scan.

### 9. Improve existing AGENTS.md without duplicating rules

```text
/local-model-instruction-engineer
Improve the existing AGENTS.md for smaller local coding models.
First scan AGENTS.md, CLAUDE.md, and .github/copilot-instructions.md.
Reuse or strengthen existing safeguards instead of duplicating them.
Add missing Git safety, loop prevention, targeted context-length handling, and validation rules only where needed.
```

Benefit: avoids token bloat from repeated guardrails.

### 10. Add data science / ML standards to a repo

```text
/local-model-instruction-engineer
Create or update AGENTS.md for this data science repo.
Detect the stack first. Domain: data-science-ml, ai-modalities.
Add Python, PEP 8, notebook, data handling, leakage prevention, evaluation, reproducibility, and artifact-handling instructions only if relevant.
```

Benefit: ML agents need domain safeguards for leakage, evaluation, seeds, model artifacts, and raw data handling.

### 11. Evaluate an artifact before changing it

```text
/local-model-agent-evaluator
Audit this AGENTS.md for local-model reliability. Do not edit it.
Grade A-F for atomicity, targeted context fit, loop safety, Git safety, skill interoperability, context strategy, domain fit, validation strength, and bloat.
Recommend whether to ship, iterate, ask the user, reject, or use the instruction engineer.
```

Benefit: gives diagnosis before mutation.

### 12. Evaluate a phase plan

```text
/local-model-agent-evaluator
Audit this implementation plan for a small local model.
Targeted context length: 32k.
Check whether phases are too coarse, durable memory files are included, stop conditions are clear, and phase debrief / do-not-carry-forward notes are required.
```

Benefit: catches big-project plans that are too broad for limited-context local models.

## Recommended Defaults

- Use `guided mode` for reusable artifacts.
- Use `review-gate` for migrations, Git changes, external side effects, or high-risk domains.
- Use Ralph loop only for important artifacts.
- Keep `.agent-work/` local and gitignored by default.
- Prefer one crisp safeguard over five similar reminders.
- Provide `targeted context length` whenever local runtime context differs from the model card.

## What This Will Not Do

This package will not:

- guarantee a small model can do any task
- bypass harness limitations
- make runtime settings controllable if the harness does not expose them
- safely automate destructive Git operations without approval
- replace tests, source verification, or human review
- prevent all loops if the harness ignores instructions
- make unsupported upstream skill requirements true

## Package Layout

This repo uses Option C: canonical shared references plus per-skill copied references. Each skill can be installed standalone, while `shared/` remains the canonical source for future syncing.
