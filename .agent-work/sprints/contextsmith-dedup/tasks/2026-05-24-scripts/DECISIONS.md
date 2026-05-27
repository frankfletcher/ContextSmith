# DECISIONS.md

## D-001: Versioning Strategy
**Decision:** Use git-compatible SHA-1 blob hash (`git hash-object` equivalent: `hashlib.sha1(f'blob {len(content)}\0'.encode() + content).hexdigest()`) as the version identifier for each shared file.
**Reason:** No shared files have version metadata (YAML frontmatter, header comments, etc.). Git-compatible blob hashes are content-addressed, deterministic, verifiable with `git hash-object`, and change only when file content changes. This is the most reliable mechanism for detecting drift between manifest versions and actual file content.
**Alternatives considered:** Raw content SHA-1 (not git-verifiable), manual version strings (labor-intensive, error-prone), timestamps (unreliable across clones).

## D-002: help.md Placement
**Decision:** Move each skill's `help.md` from `references/help.md` to `skills/<skill>/help.md` (skill root). List it in the manifest with `source: skills/<skill>/help.md` and `local: true`.
**Reason:** Since `references/` will be gitignored, any skill-local file currently in `references/` must be moved to a non-gitignored location. The skill root is the natural place. The sync script copies it into `references/` for standalone distribution.
**Alternatives considered:** Keep help.md in references/ with a gitignore exception (fragile, adds complexity), move to a `local-refs/` subdirectory (unnecessary indirection).

## D-003: Manifest Schema Extension for Local Files
**Decision:** Add a `local: true` field (default `false`) to distinguish shared dependencies from skill-local files that happen to live in `references/`.
**Reason:** The sync script needs to know whether to copy from `shared/` or from a skill-local path. A boolean field is simpler than path-prefix heuristics.
**Alternatives considered:** Detect by source path prefix (brittle if `shared/` paths change), separate `local_references` section (more complex schema for a single entry).

## D-004: Sync Script — Force Flag Semantics
**Decision:** `--force` re-copies all files regardless of version match. Default behavior skips if destination blob hash matches manifest version.
**Reason:** For normal use (post-manifest-update), the version change triggers re-copy. `--force` is for recovery scenarios (corrupted references, accidental edits to gitignored files).
**Alternatives considered:** Always overwrite (wastes time on no-op copies), compare with `diff` (slower than hash comparison for large files).

## D-005: Dry-Run as Separate Code Path
**Decision:** `--dry-run` does NOT open source files, compute hashes, or check versions. It only resolves paths and prints the copy plan.
**Reason:** Dry-run should be instant. Version validation happens during actual sync.
**Alternatives considered:** Full validation during dry-run (slow, mixes concerns).

## D-006: validate_skills.py Manifest Checks
**Decision:** Manifest validation checks structure (valid YAML, required fields, source existence, no duplicates). Version freshness is checked by `sync_shared_refs.py` at runtime (computes current source hash, warns if manifest version is stale). CI catches staleness because the sync step runs before validation.
**Reason:** Validation script runs independently of heavy I/O (hash computation on 52 files). Keeping it structural makes it fast. Sync already computes hashes for copy decisions, so it naturally checks freshness.
**Alternatives considered:** Compute hashes in validate_skills.py (slow, duplicates sync logic), rely only on content comparison without manifest version checking (no traceability — manifests go stale silently).
