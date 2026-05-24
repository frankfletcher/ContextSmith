# Skill Migration

Use `local-model-skill-migrator` for recursive skill directory work.

Default safe workflow:

1. Inventory
2. Plan
3. Backup
4. Stage conversion
5. Validate
6. Report
7. Apply only after approval

Use `~/.agents/skill-migrations/<migration-id>/` for installed user skills and `<project>/.agent-work/skill-migrations/<migration-id>/` for repo-local packages.
