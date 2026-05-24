# local-model-skill-migrator Help

Safely audit, stage, migrate, validate, apply, or restore whole directories of skills.

## Quickstart

```text
/local-model-skill-migrator --skills-dir ~/.agents/skills --mode review-gate --target-profiles generic-local,qwen36 --context-length 32k --backup --stage --no-apply

Audit and stage a migration. Do not overwrite originals.
```

## Common Uses

- Inventory installed skills.
- Stage local-model migrations with backups.
- Produce migration manifests and per-skill reports.
- Risk-classify skills before conversion.
- Apply staged changes only after approval.
- Restore from backup.

## Common Parameters

```bash
--skills-dir ~/.agents/skills
--mode audit-only|plan-only|review-gate
--target-profiles generic-local,qwen36
--context-length 32k|64k|128k
--backup
--stage
--apply
--no-apply
--restore <migration-id>
--batch-size 3
```

## Output

Creates or reports migration workspace, backup, staging directory, `MANIFEST.json`, per-skill reports, validation results, and restore instructions.

## New v1.4.0 Controls

- `--education-level none|brief|guided|deep|teaching`
- `--artifact-verbosity compact|normal|detailed`
- `--phase-review off|brief|standard|deep`
- `--code-review-iterations 0|1|2`
- `--target-capability small-local|mid-local|large-local|frontier-cloud|reasoning-specialized|coding-specialized|multimodal`
- `--planner-profile <profile>`
- `--executor-profile <profile>`
- `--focus implementation-plan|test-quality|runtime-stability|agents-md|prompt|skill`
