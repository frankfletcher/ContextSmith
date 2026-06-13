# Which ContextSmith Skill Should I Use?

ContextSmith is a toolkit, not one giant skill. Each skill has a narrow job so the agent loads less context and mixes fewer workflows.

If you are unsure, start with the router:

```bash
/contextsmith help
```

The router dispatches to one sub-skill and leaves omitted parameters for that sub-skill's own defaults.

## I have a prompt

Use:

```text
contextsmith-prompt-engineer
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
/contextsmith-prompt-engineer --mode deep --target-profile qwen36 --context-length 32k --ralph 2
```

## I want to run a prompt or handoff

Use:

```text
contextsmith-orchestrator
```

Good for:

- executing a prompt while enforcing target model, context budget, validation, self-audit, and Ralph controls
- running `NEXT_PROMPT.md` or a `.agent_work/.../tasks/<task>/` phase handoff
- asking refinement questions before execution so domain choices are not silently assumed
- handling code and non-code runs such as research, email rewriting, data analysis, ML work, and business memos

Example:

```bash
/contextsmith-orchestrator --run-mode phase --target .agent_work/sprints/<sprint>/tasks/<task> --interaction refine --validation strict --ralph 2
```

## I have a SKILL.md

Use:

```text
contextsmith-skill-engineer
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
/contextsmith-skill-engineer --source ./my-skill/SKILL.md --target-profiles generic-local,qwen36 --output staging
```

## I have a directory full of skills

Use:

```text
contextsmith-skill-migrator
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
/contextsmith-skill-migrator --skills-dir ~/.agents/skills --backup --stage --no-apply
```

## I have a repo and want better agent instructions

Use:

```text
contextsmith-instruction-engineer
```

Good for:

- creating or improving `AGENTS.md`
- scanning existing instruction files
- adding Git safety and loop safety without duplication
- adding coding, UI, data-science, or ML guidance when relevant
- building repo-specific instructions instead of generic boilerplate

Example:

```bash
/contextsmith-instruction-engineer --project . --mode guided --domain coding,data-science-ml --context-length 32k
```

## I want to audit without changing files

Use:

```text
contextsmith-agent-evaluator
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
/contextsmith-agent-evaluator --mode audit-only --focus implementation-plan --target IMPLEMENTATION_PLAN.md
```

## If you are still unsure

Start with the router for discovery or the evaluator for audit-only work:

```bash
/contextsmith help
```

For an existing artifact you want reviewed without edits:

```bash
/contextsmith-agent-evaluator --mode audit-only --target <file-or-folder>
```

It will tell you what is weak and which ContextSmith skill is likely to help.
