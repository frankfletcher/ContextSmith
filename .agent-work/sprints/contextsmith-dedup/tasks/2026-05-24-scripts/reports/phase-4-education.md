## Phase 4 — What You Need to Know

### What Changed
Created `scripts/sync_shared_refs.py` to populate `references/` directories from `shared/` via manifests.

### Design Decisions
- **Git-compatible hashing**: Uses `blob <size>\0` prefix for SHA-1 hashing, matching Git's internal object format.
- **Content-based skipping**: Compares source and destination file hashes before copying; only copies if content differs.
- **Manifest-driven filtering**: Skips files marked `required: false` in the manifest, reducing unnecessary copies.
- **Local file handling**: Copies `help.md` from the skill root (not `shared/`) to `references/`.

### Trade-Offs
- **Optional files excluded**: Files marked `required: false` are not copied to `references/`. This saves disk space but requires the manifest to be accurate.
- **No cleanup**: The script does not delete existing files in `references/`; cleanup is deferred to Phase 5.

### Key Lessons
**Manifest-driven synchronization** is a powerful pattern for managing derived artifacts. By declaring dependencies explicitly in YAML, you enable automated, reproducible population of generated directories without manual intervention.

### Edge Cases Not Handled
- **Stale manifest detection**: The script warns if a manifest's stored version hash differs from the current file hash, but does not fail. This allows gradual updates.
- **Empty directory creation**: The script creates `references/` subdirectories as needed, but does not remove obsolete directories (future work).

### Next Phase Preview
Phase 5 will verify that the sync script reproduces existing copies byte-for-byte, then safely delete the 265 committed copies from `skills/*/references/` and add `.gitignore` rules to prevent accidental commits.
