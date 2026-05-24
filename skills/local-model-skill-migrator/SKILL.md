---
name: local-model-skill-migrator
description: Safely audit, stage, migrate, validate, apply, or restore whole directories of SKILL.md-based skills for local/open-weight model compatibility. Use for recursive skill migrations such as ~/.agents/skills, with backup, manifest, staging, per-skill reports, target-profile metadata, reference optimization, loop/Git/context safeguards, semantic-diff validation, Ralph-loop quality review, and explicit approval before applying changes, targeted context length control, and upstream workflow collision checks.
metadata:
  version: "1.5.1"
  package: ContextSmith
  target: local-open-weight-models
---

# Local Model Skill Migrator

Safely migrate directories of skills to local/open-weight model engineering standards.


## Help Mode

If the user invokes this skill with `help`, `describe`, `examples`, `modes`, `parameters`, `quickstart`, or CLI-style equivalents such as `--help`, do not run the normal workflow.

Return the requested usage guidance from `references/help.md` and `references/help-mode.md`.

## Control Parameter Parsing

Accept both natural-language controls and CLI-style flags. Use `references/control-parameters.md` for parsing rules.

Examples:

```bash
--mode deep --target-profile qwen36 --context-length 32k --domain coding --harness opencode --ralph 2 --output project-local --no-apply
```

When CLI flags and prose conflict, prefer explicit current-user prose or ask one concise clarification question if the intended priority is unclear.

## Default Safety Posture

Default to **stage, do not apply**. Never rewrite source skills in place before backup and manifest creation.

## Modes

- `audit-only`: inspect and report
- `plan-only`: produce migration plan
- `stage`: backup and write converted skills to staging
- `apply`: apply staged changes only with explicit approval
- `restore`: restore from backup

Use `references/interaction-modes.md`.

## Targeted Context Length

When the user provides a targeted context length, use it to set migration batch size, report size, Ralph-loop detail, subagent use, and phase granularity. For tiny/tight context, migrate in smaller batches and rely on compact per-skill reports plus manifests instead of loading many skills at once.

## Upstream and Workflow Collision Handling

During migration, detect skills or instruction files that already encode another tool's workflow, prompt optimizer output, frontend specs, or implementation plans. Use `references/skill-interoperability.md` and `references/instruction-precedence.md` to avoid clobbering valid workflows or preserving hallucinated requirements.



## Model Capability and Planner/Executor Profiles

When the user provides `--target-capability`, `--planner-profile`, or `--executor-profile`, load `references/model-capability-tiers.md` and `references/planner-executor-workflows.md`.

Use stronger/planner profiles for planning, audits, architecture, test strategy, and final review. Use smaller/executor profiles for atomic phase execution when the plan and task state are explicit.



## Education Level and Artifact Verbosity

If the user provides `--education-level` or `--artifact-verbosity`, load `references/education-levels.md`.

Keep model-facing artifacts compact when `targeted_context_length` is tight. Put teaching detail in separate reports instead of bloating prompts, skills, AGENTS.md files, or phase instructions.


## Run Configuration Preview

For guided, deep, review-gate, AGENTS.md, migration, or file-changing work, show a compact run configuration preview when important parameters were inferred. Use `references/run-configuration-preview.md`.

The preview should state the inferred context, chosen parameters, low-confidence assumptions, and planned approach. Ask the user whether to proceed or change a parameter unless the user explicitly selected yolo/fast behavior.

## Workflow

### 1. Inventory

Find valid skill folders with `SKILL.md`. Record line count, frontmatter, references, scripts, assets, agents metadata, existing safeguards, and risk level.

Risk:

- low: simple SKILL.md, no scripts/assets, no side effects
- medium: references, commands, generated artifacts, moderate workflows
- high: scripts, destructive actions, deployment, external services, credentials, production systems, purchasing, messaging, or complex side effects

### 2. Plan Workspace

Use canonical output rules from `references/output-location.md`.

Installed user skills:

```text
~/.agents/skill-migrations/<YYYY-MM-DD-short-slug>/
├── BACKUP/
├── STAGING/
├── REPORTS/
├── MANIFEST.json
├── MIGRATION_PLAN.md
├── MIGRATION_REPORT.md
└── RESTORE.md
```

Repo-local skill packages use `<project>/.agent-work/skill-migrations/<migration-id>/`.

### 3. Backup

Copy every touched skill before conversion. Write checksums to `MANIFEST.json`.

### 4. Stage Conversion

Use local-model-skill-engineer principles per skill:

- preserve behavior
- apply target profiles
- add engineering metadata
- optimize references conservatively
- scan existing safeguards and avoid duplication
- add loop/Git/context/persistence/subagent support only when warranted
- avoid exposed chain-of-thought
- classify domain and side-effect risks

### 5. Validate

For each staged skill, validate:

- frontmatter and metadata
- source contract and semantic diff
- references and linked files
- no exposed CoT
- safeguards reused/added/skipped
- context-risk handling
- Git/file safety for repo/coding skills
- duplicate-rule and token-bloat guard
- A-F quality grades

High-risk skills require manual review before apply.

### 6. Report

Write per-skill and batch reports:

- original strengths/weaknesses
- changes made
- references modified
- safeguards added/reused/skipped
- token impact
- A-F grades
- manual review items
- restore instructions

### 7. Apply or Restore

Apply only after explicit approval. Restore only from recorded backup manifest.

## Never

- edit source in place before backup
- silently delete files
- modify scripts/assets without reason and report
- apply staged changes with failed validation
- run destructive Git operations without approval
- duplicate existing safeguards instead of consolidating them


## Documentation Quality

When generating or editing README material, user guides, educational reports, AGENTS.md explanations, or other reader-facing documentation, use `references/documentation-quality.md`. Keep generated artifacts factual, practical, and easy to act on. Avoid overused generated-writing patterns, unsupported claims, and unnecessary imperatives in user documentation.
