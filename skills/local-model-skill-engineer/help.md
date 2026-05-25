# local-model-skill-engineer Help

Create, convert, improve, audit, and package `SKILL.md`-based skills for local/open-weight models.

## Quickstart

```text
/local-model-skill-engineer --source ./my-skill/SKILL.md --mode guided --target-profiles generic-local,qwen36 --context-length 64k --reference-policy optimize --output staging

Convert this skill for local models. Preserve behavior and report all changes.
```

## Common Uses

- Create a new skill from requirements.
- Convert a Claude/GPT/Codex-oriented skill for local models.
- Optimize references and progressive disclosure.
- Add target-profile metadata.
- Run semantic diff and upstream artifact audits.
- Add loop/context/Git/task-state safeguards only when relevant.

## Common Parameters

```bash
--source ./path/to/SKILL.md
--mode fast|deep|guided|review-gate|audit-only
--target-profile qwen36|gemma4|llama3|generic-local
--target-profiles generic-local,qwen36
--context-length 32k|64k|128k
--reference-policy inspect|optimize|preserve
--ralph 0|1|2|3
--output chat|project-local|staging
--no-apply
```

## Output

Usually returns a revised skill or staged skill package, semantic diff, reference audit, metadata summary, validation checklist, and educational change report.

## New v1.4.0 Controls

- `--education-level none|brief|guided|deep|teaching`
- `--artifact-verbosity compact|normal|detailed`
- `--phase-review off|brief|standard|deep`
- `--code-review-iterations 0|1|2`
- `--target-capability small-local|mid-local|large-local|frontier-cloud|reasoning-specialized|coding-specialized|multimodal`
- `--planner-profile <profile>`
- `--executor-profile <profile>`
- `--focus implementation-plan|test-quality|runtime-stability|agents-md|prompt|skill`


## Additional Controls

- `--review-config` / `--preview-config`: show inferred parameters before important work.
- `--no-review-config`: skip the preview for low-risk work.
- `--focus documentation-quality`: audit reader-facing documentation for clarity, tone, examples, factuality, and style.
