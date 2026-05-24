# Which ContextSmith Skill Should I Use?

ContextSmith is a toolkit, not one giant skill. Each skill has a narrow job so the agent loads less context and mixes fewer workflows.

## I have a prompt

Use:

```text
local-model-prompt-engineer
```

Good for:

- optimizing a seed prompt
- creating system/user prompt packages
- adding context strategy
- adding test cases
- making a prompt usable by Qwen, Gemma, Llama, or a generic local model
- separating model-facing brevity from reader-facing explanation

Example:

```bash
/local-model-prompt-engineer --mode deep --target-profile qwen36 --context-length 32k --ralph 2
```

## I have a SKILL.md

Use:

```text
local-model-skill-engineer
```

Good for:

- creating a new skill
- converting a skill for local/open-weight models
- preserving source behavior while improving structure
- optimizing references
- adding model-profile metadata
- rejecting unsupported requirements from upstream tools

Example:

```bash
/local-model-skill-engineer --source ./my-skill/SKILL.md --target-profiles generic-local,qwen36 --output staging
```

## I have a directory full of skills

Use:

```text
local-model-skill-migrator
```

Good for:

- inventorying many skills
- backing up before changes
- staging conversions
- validating converted skills
- producing a manifest and restore plan
- applying only after review

Example:

```bash
/local-model-skill-migrator --skills-dir ~/.agents/skills --backup --stage --no-apply
```

## I have a repo and want better agent instructions

Use:

```text
local-model-instruction-engineer
```

Good for:

- creating or improving `AGENTS.md`
- scanning existing instruction files
- adding Git safety and loop safety without duplication
- adding coding, UI, data-science, or ML guidance when relevant
- building repo-specific instructions instead of generic boilerplate

Example:

```bash
/local-model-instruction-engineer --project . --mode guided --domain coding,data-science-ml --context-length 32k
```

## I want to audit without changing files

Use:

```text
local-model-agent-evaluator
```

Good for:

- prompt audits
- skill audits
- AGENTS.md audits
- implementation-plan audits
- test-quality audits
- runtime-stability reviews
- small-model-readiness scoring

Example:

```bash
/local-model-agent-evaluator --mode audit-only --focus implementation-plan --target IMPLEMENTATION_PLAN.md
```

## If you are still unsure

Start with the evaluator:

```bash
/local-model-agent-evaluator --mode audit-only --target <file-or-folder>
```

It will tell you what is weak and which ContextSmith skill is likely to help.
