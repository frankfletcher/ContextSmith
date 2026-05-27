## Phase 3 — What You Need to Know

### What Changed
- Created 4 new `reference_manifest.yml` files for remaining skills: `local-model-skill-engineer`, `local-model-skill-migrator`, `local-model-instruction-engineer`, `local-model-agent-evaluator`
- Relocated all 5 `help.md` files from `skills/*/references/help.md` to `skills/*/help.md`
- Updated manifest entries to point to new skill-root location for local files

### Design Decisions
1. **Manifest copying strategy**: Used `local-model-prompt-engineer/reference_manifest.yml` as a template for the remaining 4 skills. This ensures consistency across all manifests while only changing the `skill`, `description`, and `local` file paths.
2. **Blob hash reuse**: All 52 shared files have identical hashes across all manifests. This is correct because shared files are canonical and never change.
3. **Local file handling**: Each skill's `help.md` has a unique blob hash (confirmed by hash verification), and the manifest's `local: true` field marks it as skill-specific.
4. **Required field preservation**: Per Phase 2c decision, all 52 shared entries are marked `required: true` because SKILL.md files use catch-all instructions like "use references/" without naming individual files.

### Trade-Offs
- **Dual location for help.md**: During Phase 3, `help.md` exists in both `skills/*/references/` (old location) and `skills/*/` (new location). This is intentional and will be resolved in Phase 5 when the old copies are deleted.
- **Content verification**: We verified that help.md content matches between old and new locations (byte-for-byte) but did not delete the old copies yet (per phase plan).

### Key Lessons
**Manifest-driven dependency management** is a powerful pattern for eliminating duplication. Instead of copying 52 files × 5 skills = 260 files, we maintain:
- 1 canonical source (`shared/` directory)
- 5 manifest files declaring dependencies
- A sync script that populates `references/` on demand

This reduces storage, simplifies updates (change once in `shared/`), and enables precise version control via blob hashes.

### Edge Cases Not Handled
1. **Corrupted help.md**: If a skill's help.md becomes corrupted, the manifest's version check will catch it when the sync script runs in Phase 4.
2. **Help.md content differences**: We verified all 5 help.md files have different content (different hashes), but we did not audit their actual content differences. This is acceptable because they are skill-specific by design.
3. **References/ directory state**: After relocation, `references/` still contains the old help.md copies. Phase 5 will clean this up.

### Next Phase Preview
Phase 4 creates `scripts/sync_shared_refs.py` — a Python script that reads manifests and copies shared files into `skills/*/references/`. This depends on Phase 3 completing all manifests, ensuring the sync script has complete dependency information for all 5 skills.
