---
name: local-model-skill-migrator
description: Safely audit, stage, migrate, validate, apply, or restore whole directories of SKILL.md-based skills for local/open-weight model compatibility. Use for recursive skill migrations such as ~/.agents/skills, with backup, manifest, staging, per-skill reports, target-profile metadata, reference optimization, loop/Git/context safeguards, semantic-diff validation, Ralph-loop quality review, and explicit approval before applying changes.
metadata:
  version: "1.2"
  package: local-model-agent-engineering
  target: local-open-weight-models
---

# Local Model Skill Migrator

Safely migrate directories of skills to local/open-weight model engineering standards.

## Default Safety Posture

Default to **stage, do not apply**. Never rewrite source skills in place before backup and manifest creation.

## Modes

- `audit-only`: inspect and report
- `plan-only`: produce migration plan
- `stage`: backup and write converted skills to staging
- `apply`: apply staged changes only with explicit approval
- `restore`: restore from backup

Use `references/interaction-modes.md`.

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
