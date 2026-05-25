# local-model-instruction-engineer Help

Create, improve, audit, and maintain `AGENTS.md`, `CLAUDE.md`, copilot instructions, `.cursorrules`, and similar repo/agent instruction files.

## Quickstart

```text
/local-model-instruction-engineer --project . --mode guided --target-profile qwen36 --context-length 32k --harness opencode --domain coding,data-science-ml --output project-local

Create or improve AGENTS.md. Scan existing instructions first. Add only relevant safeguards.
```

## Common Uses

- Create AGENTS.md for a repo.
- Improve existing repo instructions without duplicating rules.
- Add loop safety, Git safety, coding standards, PEP 8, UI standards, and DS/ML rules when relevant.
- Add phase memory and canonical `.agent-work/` policies.
- Suggest `.gitignore` entries without editing `.gitignore` unless approved.

## Common Parameters

```bash
--project .
--instruction-file AGENTS.md
--mode fast|deep|guided|review-gate|audit-only
--target-profile qwen36|gemma4|llama3|generic-local
--context-length 32k|64k|128k
--domain coding,data-science-ml,frontend,research
--harness opencode,codex,cursor,aider,generic-agent
--scan-existing
--suggest-gitignore
--output project-local|chat|staging
```

## Output

Returns or stages instruction files plus repo profile, detected domains, reused/strengthened safeguards, conflicts, validation steps, and educational change report.

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
