---
name: local-model-skill-migrator
description: Safely audit, stage, migrate, validate, apply, or restore whole directories of SKILL.md-based skills for local/open-weight model compatibility. Use for recursive skill migrations such as ~/.agents/skills, with backup, manifest, staging, per-skill reports, target-profile metadata, reference optimization, semantic-diff validation, and explicit approval before applying changes.
metadata:
  version: "1.1"
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

Find valid skill folders with `SKILL.md`. Record line count, frontmatter, references, scripts, assets, agents metadata, and risk level.

Risk:

- low: simple SKILL.md, no scripts/assets, no side effects
- medium: references, commands, generated artifacts, moderate workflows
- high: scripts, destructive actions, deployment, external services, credentials, production systems, purchasing, messaging, or complex side effects

### 2. Plan

Create migration workspace:

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

### 3. Backup

Copy every touched skill before conversion. Write checksums to `MANIFEST.json`.

### 4. Stage Conversion

Use local-model-skill-engineer principles per skill:

- preserve behavior
- apply target profiles
- add engineering metadata
- optimize references conservatively
- add context/persistence/subagent support only when warranted
- avoid exposed chain-of-thought

### 5. Validate

For each staged skill, validate frontmatter, body, references, source contract, metadata, no exposed CoT, context-risk handling, and semantic diff.

High-risk skills require manual review before apply.

### 6. Report

Write per-skill report and batch report with:

- original strengths
- original weaknesses
- changes made
- validation grades
- target profiles
- modified files
- manual review required
- remaining risks

### 7. Apply or Restore

Apply only after explicit approval. Restore only from a recorded backup and manifest.

## Optional Ralph Loop

Use `references/ralph-loop.md` for high-value batch migrations. Save each skill iteration under the migration workspace.
