## Phase 2 — What You Need to Know

### What Changed
- Created `skills/local-model-prompt-engineer/reference_manifest.yml` with 53 reference entries (52 shared files + 1 local help.md).

### Design Decisions
- Used git-compatible blob hash algorithm (`blob <size>\0` prefix) for versioning.
- Marked all 52 shared files as `required: true` per Phase 2c concrete answer.
- Used skill root path for local help.md even though file not yet relocated (hash computed from current location).

### Trade-Offs
- Manifest references help.md at skill root location before Phase 3 relocation; content is identical so hash is valid.
- No error handling for missing files in manifest validation (deferred to Phase 7).

### Key Lessons
- Manifest-driven dependency management enables precise version control and eliminates duplication across multiple skills.

### Edge Cases Not Handled
- None for this phase; relocation handled in Phase 3.

### Next Phase Preview
Phase 3 will create manifests for remaining 4 skills and relocate help.md files to skill roots.
