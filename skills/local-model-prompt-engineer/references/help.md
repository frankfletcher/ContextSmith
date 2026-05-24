# local-model-prompt-engineer Help

Create, improve, audit, test, and package prompts for local/open-weight models.

## Quickstart

```text
/local-model-prompt-engineer --mode deep --target-profile qwen36 --context-length 32k --ralph 2 --output project-local

Optimize this prompt for a local coding agent. Include context strategy, test cases, loop safety, and a validation checklist.
```

## Common Uses

- Optimize a seed prompt for Qwen, Gemma, Llama, or generic local models.
- Build system/user prompt packages.
- Add context strategy for long files, repos, RAG, logs, or tool output.
- Add test cases, validation criteria, and output contracts.
- Run upstream artifact audits when another optimizer modified the prompt first.

## Common Parameters

```bash
--mode fast|deep|guided|yolo|review-gate|audit-only
--target-profile qwen36|gemma4|llama3|generic-local
--context-length 32k|64k|100k|128k
--domain coding,data-science-ml,research,email
--harness opencode,codex,cursor,aider,generic-agent
--ralph 0|1|2|3
--output chat|project-local|staging
```

## Output

Normally returns an optimized prompt package, assumptions, model/context strategy, validation checklist, test cases when useful, and an educational change report.

## New v1.4.0 Controls

- `--education-level none|brief|guided|deep|teaching`
- `--artifact-verbosity compact|normal|detailed`
- `--phase-review off|brief|standard|deep`
- `--code-review-iterations 0|1|2`
- `--target-capability small-local|mid-local|large-local|frontier-cloud|reasoning-specialized|coding-specialized|multimodal`
- `--planner-profile <profile>`
- `--executor-profile <profile>`
- `--focus implementation-plan|test-quality|runtime-stability|agents-md|prompt|skill`
