# Implementation Plan: Repo & Release Tooling

## Artifact Manifest
```yaml
---
artifact_type: implementation_plan
idea: "scripts/sync_shared_refs.py + scripts/build_release.py (Repo & Release Tooling)"
source: ".agent_work/top5_ideas_to_implement.md (Idea #1)"
date: "2026-05-29"
parameters:
  --mode: guided,deep
  --target-profile: qwen36
  --context-length: 60k
  --education_level: deep
  --ralph: 2
  --planner-profile: qwen36
  --executor-profile: qwen36
references:
  - shared/phased-planning.md
  - shared/implementation-plan-audit.md
  - shared/git-safety.md
behavioral_contracts:
  - Plan must be executable by qwen36 in guided mode
  - Each phase must be atomic and testable
  - No code changes — plan file output only
---
```

## Context Summary

**The idea (from `top5_ideas_to_implement.md`, Idea #1):**
There are 42 files in `shared/` that get copied into each skill's `references/` for standalone installation. Keeping them in sync is manual — every edit to a shared reference requires deciding whether each of 5 skills needs an updated copy (42 × 5 = 210 potential operations). The sync script automates propagation; the release builder packages everything for distribution. These are force multipliers that make every future edit safer and faster.

**Backlog items from the idea:**
- [x] `scripts/sync_shared_refs.py` — **COMPLETE** (see audit below)
- [ ] `scripts/build_release.py` — **NOT STARTED** (does not exist)

## Existing Code Audit

### `scripts/sync_shared_refs.py` — COMPLETE (160 lines)
A production-ready sync tool with full CLI surface:
- `--skill <name>` / `--all` for targeted or bulk sync
- `--dry-run` previews without writing
- `--force` overwrites even if content matches
- `--verbose` logs each file operation
- `--in-place` writes directly to `skills/*/references/` (for CI)
- Default mode writes to `.agent_work/staged_skills/` (keeps working tree clean)
- Git-compatible SHA-1 blob hash comparison for change detection
- Manifest version staleness warnings when source content drifts from stored hash
- YAML error handling, missing file detection, required/optional reference support

**Remaining gaps (minor):**
- No "update manifests" mode — when content changes, the stored hash in `reference_manifest.yml` stays stale. A `--update-manifests` flag would recompute hashes and write them back.
- No summary report (e.g., JSON output of what changed for CI integration).

### `scripts/package_skill.sh` — PARTIALLY COMPLETE (75 lines)
A functional packaging script with these capabilities:
- Validates skill directory and SKILL.md existence
- Directory traversal protection on skill name input
- Extracts version from `reference_manifest.yml` via PyYAML
- Calls `sync_shared_refs.py --skill <name> --verbose` internally
- Creates a zip from the staging directory (excludes manifest and .gitkeep)
- Reports file count in output

**Gaps to address:**
- No pre-package validation gate (should run `validate_skills.py` before packaging)
- No `MANIFEST.json` inside the package (file list + checksums for install verification)
- Zip-only format (no tar.gz for Unix-friendly distribution)
- File count uses fragile `unzip -l | tail -1` parsing
- No SHA-256 checksum file alongside the zip

### `scripts/validate_skills.py` — FUNCTIONAL (200 lines)
Covers:
- SKILL.md frontmatter validation (name, description, metadata.version)
- Line count warning at 500 lines
- Reference manifest validation (skill name match, source existence, duplicate detection, shared/ prefix check)
- Artifact manifest reference check for engineer skills
- Shared reference format validation (ATX headings, no YAML frontmatter) — only checks 3 specific files

**Gaps:**
- Shared reference format check only runs on 3 hardcoded files, not all 42 in `shared/`
- No SKILL.md internal cross-reference validation (does SKILL.md mention files that don't exist in references/)

### What does NOT exist yet
- `scripts/build_release.py` — the main missing piece from the backlog
- Installation scripts (`install_skill.sh`, `install_all.sh`)
- Release documentation (`docs/RELEASE_PROCESS.md`)
- End-to-end integration test workflow
- `dist/` directory (gitignored, created at release time)

## Implementation Plan

### Phase 1: Harden sync_shared_refs.py — manifest update mode (Estimated: 1-2 hours)

**Objective:** Add a `--update-manifests` flag so the script can recompute and write back stale hashes in `reference_manifest.yml`.

**Context:** The sync script already detects stale hashes and warns about them, but doesn't fix them. After syncing references, the manifests still contain old hashes. This means the next sync run will warn again even though content is correct.

**Tasks:**
1. Add `--update-manifests` flag to argparse in `scripts/sync_shared_refs.py`.
2. When this flag is set, after copying files, recompute SHA-1 blob hash for each source file and write the updated hash back into the corresponding `reference_manifest.yml` (in `skills/<name>/reference_manifest.yml`).
3. Write manifests only when at least one hash changed (avoid unnecessary file writes).
4. Add a summary line: "Updated N hashes in M manifests."

**Deliverables:**
- Updated `scripts/sync_shared_refs.py` with `--update-manifests` flag

**Tests:**
1. Run `python scripts/sync_shared_refs.py --skill local-model-prompt-engineer --verbose` — verify it still works unchanged.
2. Deliberately edit one shared reference (e.g., add a blank line to `shared/git-safety.md`), then run with `--update-manifests` — verify the hash updates in all manifests that reference that file.
3. Run without `--update-manifests` — verify no manifest files are modified.
4. Run `python scripts/validate_skills.py` — verify no new errors introduced.

**Estimated effort:** 1-2 hours

---

### Phase 2: Harden package_skill.sh — validation gate + MANIFEST.json + SHA-256 (Estimated: 2-3 hours)

**Objective:** Make the packaging script produce verifiable, self-describing packages with a pre-flight validation gate.

**Context:** The current script packages without validating the skill first, produces no manifest inside the zip, and has no checksum file. This means broken skills can be packaged silently, and there's no way to verify package integrity after download.

**Tasks:**
1. Add a pre-package validation step: run `python scripts/validate_skills.py` and abort with exit code 1 if it fails. (The validator checks all skills; add a `--skill <name>` filter to validate_skills.py if needed, or accept that it validates all.)
2. Generate `MANIFEST.json` inside the staging directory before zipping:
   - Fields: `skill_name`, `version`, `package_date`, `files` (array of `{path, sha256, size}` for each file in the skill).
3. After creating the zip, generate a `<skill>-<version>.sha256` checksum file alongside it.
4. Replace the fragile `unzip -l | tail -1` file count with a reliable Python one-liner or `zipinfo` command.

**Deliverables:**
- Updated `scripts/package_skill.sh` with validation gate, MANIFEST.json generation, SHA-256 checksum
- Optionally: `--skill <name>` filter added to `scripts/validate_skills.py` (only if needed for single-skill packaging)

**Tests:**
1. Package each of the 5 skills individually — verify zip, MANIFEST.json inside zip, and .sha256 file are created.
2. Extract a zip and verify MANIFEST.json checksums match actual files: `python3 -c "import json,hashlib; ..."` for each entry.
3. Verify SHA-256 file validates the zip: `sha256sum -c dist/<skill>.sha256`.
4. Deliberately break a skill (remove SKILL.md) — verify packaging aborts with clear error.

**Estimated effort:** 2-3 hours

---

### Phase 3: Create build_release.py — the main missing piece (Estimated: 3-4 hours)

**Objective:** A single Python script that orchestrates the full release pipeline: sync → validate → package → summary.

**Context:** This is the backlog item explicitly called out in the ideas document. It does not exist yet. The script should be Python (not shell) for cross-platform compatibility and to leverage PyYAML/JSON natively.

**Tasks:**
1. Create `scripts/build_release.py` with argparse CLI:
   - `--version <semver>` — set version for all skills (optional, defaults to current versions)
   - `--package` — run full pipeline: sync → validate → package all skills
   - `--dry-run` — preview without writing packages or modifying manifests
   - `--dist-dir <path>` — output directory (default: `dist/`)
2. Pipeline implementation (run in order):
   a. **Sync phase:** Call `sync_shared_refs.py --all --in-place` to update `skills/*/references/`.
   b. **Manifest update phase:** Call `sync_shared_refs.py --all --update-manifests` to refresh hashes.
   c. **Validation phase:** Run `validate_skills.py`, abort on failure with clear message.
   d. **Version bump (if --version specified):** Update `metadata.version` in each SKILL.md frontmatter and `version` in each `reference_manifest.yml`. Check git status first — abort if SKILL.md files have uncommitted changes.
   e. **Package phase:** Call `package_skill.sh` for each of the 5 skills, collecting output to `dist/`.
3. Generate `dist/RELEASE_SUMMARY.json`:
   - Array of skill entries: `{name, version, zip_path, sha256_path, file_count, total_size_bytes}`
   - Top-level: `{release_date, total_skills, total_size_bytes}`
4. Print a formatted summary table to stdout after completion.

**Deliverables:**
- `scripts/build_release.py` (new file)

**Tests:**
1. `python scripts/build_release.py --dry-run --package` — verify it prints the plan without creating files in dist/.
2. `python scripts/build_release.py --package` — verify all 5 zips, SHA-256 files, and RELEASE_SUMMARY.json are created in dist/.
3. `python scripts/build_release.py --version 1.1.0 --package` — verify version bumps in SKILL.md and manifests (run on a branch or revert after test).
4. Verify RELEASE_SUMMARY.json matches actual files: file counts, sizes, SHA-256 values.

**Estimated effort:** 3-4 hours

---

### Phase 4: Installation scripts (Estimated: 1-2 hours)

**Objective:** Make it trivial for end users to install a ContextSmith skill from a package.

**Context:** Users need a simple way to install skills from the zip packages. The target is `~/.claude/skills/` (or equivalent for other agents). Scripts should handle backup, version comparison, and verification.

**Tasks:**
1. Create `scripts/install_skill.sh`:
   - Usage: `install_skill.sh <zip-file> [target-dir]`
   - Default target: `~/.claude/skills/`
   - Extract zip to a temp directory first
   - Verify MANIFEST.json checksums before installing (fail fast if corrupted)
   - If skill already exists at target, compare versions — skip if installed version >= package version, otherwise back up old version to `<name>.backup.<timestamp>/`
   - Copy staged files to target directory
   - Print installation summary: skill name, version, target path, backup path (if applicable)
2. Create `scripts/install_all.sh`:
   - Usage: `install_all.sh <dist-dir> [target-dir]`
   - Default dist-dir: `./dist`
   - Find all `<skill>-<version>.zip` files in dist/
   - Call `install_skill.sh` for each, report per-skill status (installed/skipped/failed)
   - Exit code 1 if any installation failed

**Deliverables:**
- `scripts/install_skill.sh` (new file)
- `scripts/install_all.sh` (new file)

**Tests:**
1. Create a temp directory, install one skill from dist/ — verify files extracted correctly.
2. Install the same skill again — verify it skips (same version).
3. Manually bump installed version down, reinstall — verify backup created and new version installed.
4. Run `install_all.sh` with all 5 skills — verify all install to temp directory.

**Estimated effort:** 1-2 hours

---

### Phase 5: Documentation (Estimated: 1-2 hours)

**Objective:** Document the release process for maintainers and installation for users.

**Context:** Without documentation, the scripts are unusable by anyone other than their author. The README needs an installation section so visitors can get started immediately.

**Tasks:**
1. Create `docs/RELEASE_PROCESS.md`:
   - Prerequisites (Python 3, PyYAML, zip)
   - Step-by-step release checklist:
     1. Ensure working tree is clean: `git status`
     2. Run validation: `python scripts/validate_skills.py`
     3. Preview release: `python scripts/build_release.py --dry-run --package`
     4. Execute release: `python scripts/build_release.py --version X.Y.Z --package`
     5. Verify output: check dist/ contents and RELEASE_SUMMARY.json
   - Troubleshooting section (common errors and fixes)
2. Update `README.md`:
   - Add an "Installation" section with commands for installing from packages
   - Reference `docs/RELEASE_PROCESS.md` for maintainers
3. Update `CHANGELOG.md`:
   - Add entries for new scripts and improvements

**Deliverables:**
- `docs/RELEASE_PROCESS.md` (new file)
- Updated `README.md` with installation section
- Updated `CHANGELOG.md` with release tooling entries

**Tests:**
1. Follow the RELEASE_PROCESS.md steps from scratch on a clean checkout — verify they work without modification.
2. Verify README installation commands are copy-paste executable.

**Estimated effort:** 1-2 hours

---

### Phase 6: Integration test script (Estimated: 1 hour)

**Objective:** A single command that validates the entire release pipeline from clean state.

**Context:** This is the quality gate that ensures future changes don't break the release workflow. It should be fast enough to run before committing.

**Tasks:**
1. Create `scripts/test_release.sh`:
   - Set up a temp directory (e.g., `/tmp/contextsmith-release-test-$$`)
   - Clean: remove temp dist/ and staging directories
   - Run full pipeline: `python scripts/build_release.py --package` (without version bump)
   - Verify: all 5 zips exist in dist/, all SHA-256 files validate, RELEASE_SUMMARY.json is valid JSON with 5 entries
   - Test install: create temp target dir, run `install_all.sh`, verify all skills extracted
   - Cleanup: remove temp directories
   - Print pass/fail summary
2. Make the script idempotent and safe to run multiple times.

**Deliverables:**
- `scripts/test_release.sh` (new file)

**Tests:**
1. Run `bash scripts/test_release.sh` — verify it passes with exit code 0.
2. Deliberately break a skill, run again — verify it fails with clear error message.
3. Fix the skill, run again — verify it passes.

**Estimated effort:** 1 hour

---

## Phase Dependencies

```
Phase 1 (harden sync_shared_refs.py)
    ├── Phase 2 (harden package_skill.sh)
    │       └── Phase 3 (build_release.py) ← main missing piece
    │               ├── Phase 4 (install scripts)
    │               └── Phase 5 (documentation)
    │                       └── Phase 6 (integration test)
```

Phase 1 can run in parallel with Phase 2. Phases 3-6 are sequential.

## Persistent Task State

Track progress in `.agent_work/sprints/release-tooling/tasks/`:

```
.agent_work/sprints/release-tooling/tasks/
├── TASK.md          # objective: complete Idea #1 from top5_ideas
├── PLAN.md          # phase checklist (mirror of this plan)
├── STATUS.md        # current phase, last updated date
├── DECISIONS.md     # durable decisions with reasons
└── PHASE_LOG.md     # one entry per completed phase
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| `build_release.py` subprocess calls fail on macOS (different zip path) | Low | Medium | Use Python zipfile module as fallback; test on macOS if available |
| Version bump overwrites uncommitted SKILL.md changes | Low | High | Git status check before modifying; abort with clear error if dirty |
| MANIFEST.json generation adds dependency (jq or Python) | N/A | Low | Python already required (sync_shared_refs.py uses PyYAML) |
| Install scripts conflict with existing skill versions | Medium | Low | Backup before overwrite; version comparison skip logic |

## Success Criteria

- [ ] `python scripts/build_release.py --package` produces valid packages for all 5 skills in `dist/`
- [ ] Each zip contains SKILL.md, references/, and MANIFEST.json with correct checksums
- [ ] Each zip has a corresponding `.sha256` file that validates
- [ ] `scripts/install_skill.sh` correctly installs to target directory with backup
- [ ] `scripts/install_all.sh` installs all 5 skills from dist/ without errors
- [ ] `dist/RELEASE_SUMMARY.json` contains accurate metadata for all packages
- [ ] `docs/RELEASE_PROCESS.md` exists and is actionable (can be followed step-by-step)
- [ ] `README.md` has an installation section with working commands
- [ ] `bash scripts/test_release.sh` passes end-to-end from clean state
- [ ] `python scripts/validate_skills.py` passes after all changes