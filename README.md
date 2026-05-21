# Local Model Agent Engineering Skills

This is a package of skills for engineering prompts, skills, migrations, and agent instruction files for local/open-weight models such as Qwen, Gemma, Llama, Mistral, Phi, and DeepSeek.

## Included Skills

- `local-model-prompt-engineer` — create, optimize, audit, and test prompts.
- `local-model-skill-engineer` — create, convert, audit, and package SKILL.md-based skills.
- `local-model-skill-migrator` — safely migrate directories of skills with backup, staging, manifest, and reports.
- `local-model-instruction-engineer` — create and improve AGENTS.md, CLAUDE.md, copilot instructions, .cursorrules, and related agent instruction files.
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

## Quick Start

Optimize a prompt:

```text
/local-model-prompt-engineer
Optimize this prompt for Qwen3.6-27B. Use guided mode and include test cases.
```

Engineer a skill:

```text
/local-model-skill-engineer
Convert ./my-skill/SKILL.md for generic local models and Qwen3.6. Preserve behavior.
```

Migrate a directory safely:

```text
/local-model-skill-migrator
Audit and stage migration for ~/.agents/skills. Back everything up. Do not apply yet.
```

Create AGENTS.md:

```text
/local-model-instruction-engineer
Create AGENTS.md for this repo targeting local coding agents. Use guided mode.
```

Evaluate without editing:

```text
/local-model-agent-evaluator
Audit this AGENTS.md for local-model reliability and grade it A-F.
```

## Design Principles

- Local/smaller models need literal, atomic, testable instructions.
- Do not request exposed chain-of-thought.
- Runtime settings are guidance unless the harness exposes control.
- Context engineering matters as much as prompt wording.
- Long-running tasks need phased execution and durable task state.
- Subagents help only when scoped narrowly.
- Batch migration stages changes before applying.
- Every change should teach the user what was strong, weak, and improved.

## Package Layout

This repo uses Option C: canonical shared references plus per-skill copied references. Each skill can be installed standalone, while `shared/` remains the canonical source for future syncing.
