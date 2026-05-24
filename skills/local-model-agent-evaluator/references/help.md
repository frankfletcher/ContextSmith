# local-model-agent-evaluator Help

Audit prompts, skills, AGENTS.md files, repo instructions, agent workflows, model profiles, migration outputs, and long-running plans without modifying them by default.

## Quickstart

```text
/local-model-agent-evaluator --target ./AGENTS.md --mode audit-only --target-profile qwen36 --context-length 32k --domain coding

Grade this file for local-model reliability and recommend fixes. Do not edit files.
```

## Common Uses

- Diagnose before using an engineer skill.
- Grade small-model atomicity, context fit, loop safety, Git safety, domain fit, validation, and bloat.
- Check upstream artifact hallucinations and instruction conflicts.
- Decide whether a Ralph loop or engineering pass is worth running.

## Common Parameters

```bash
--target ./artifact.md
--mode audit-only
--target-profile qwen36|gemma4|llama3|generic-local
--context-length 32k|64k|128k
--domain coding,data-science-ml,research,email
--grade-only
--recommend-fixes
--output chat|project-local
```

## Output

Returns summary grade, strengths, weaknesses, A-F rubric table, high-risk issues, duplicate/conflicting instructions, and suggested next action.

## New v1.4.0 Controls

- `--education-level none|brief|guided|deep|teaching`
- `--artifact-verbosity compact|normal|detailed`
- `--phase-review off|brief|standard|deep`
- `--code-review-iterations 0|1|2`
- `--target-capability small-local|mid-local|large-local|frontier-cloud|reasoning-specialized|coding-specialized|multimodal`
- `--planner-profile <profile>`
- `--executor-profile <profile>`
- `--focus implementation-plan|test-quality|runtime-stability|agents-md|prompt|skill`
