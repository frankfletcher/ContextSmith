# Skill Migration

Skill migration means applying local-model engineering patterns to a directory of existing skills.

This is powerful, but it is risky if done in place. A bad batch rewrite could subtly damage many skills. ContextSmith therefore treats migration as a staged workflow.

## Safe default

```bash
/local-model-skill-migrator \
  --skills-dir ~/.agents/skills \
  --mode review-gate \
  --target-profiles generic-local,qwen36 \
  --backup \
  --stage \
  --no-apply
```

This should:

1. inventory the skills
2. classify risk
3. back up originals
4. stage converted versions
5. validate staged output
6. produce reports
7. wait for approval before applying

## What migration should preserve

A migrated skill should preserve:

- purpose
- trigger conditions
- inputs and outputs
- commands and flags
- permission boundaries
- failure handling
- examples that encode behavior
- linked references and scripts

It should not invent new requirements, thresholds, frameworks, or workflows unless supported by user request, project evidence, or the selected model/domain profile.

## Migration workspace

For installed user skills, use:

```text
~/.agents/skill-migrations/<migration-id>/
```

For repo-local skills, use:

```text
<project>/.agent-work/skill-migrations/<migration-id>/
```

The workspace should include:

- `BACKUP/`
- `STAGING/`
- `REPORTS/`
- `MANIFEST.json`
- `MIGRATION_PLAN.md`
- `MIGRATION_REPORT.md`
- `RESTORE.md`

## Risk levels

Low risk:

- short `SKILL.md`
- no scripts
- no assets
- no side effects

Medium risk:

- references
- tool commands
- generated outputs
- moderate workflow complexity

High risk:

- scripts
- destructive actions
- external services
- credentials or secrets
- production/deployment behavior
- complex side effects

High-risk skills should be staged and manually reviewed before apply.
