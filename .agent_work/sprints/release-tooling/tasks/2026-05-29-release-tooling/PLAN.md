# PLAN.md — Release Tooling Sprint

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
---
```

## Phase Checklist

### Phase 1: Harden sync_shared_refs.py — manifest update mode [x] (1-2h)

**Objective:** Add `--update-manifests` flag so the script can recompute and write back stale hashes in `reference_manifest.yml`.

**Inputs:** `scripts/sync_shared_refs.py`, `skills/*/reference_manifest.yml`
**Files/Directories:** `scripts/`, `skills/*/reference_manifest.yml`

- [x] 1.1 Add `--update-manifests` flag to argparse
- [x] 1.2 When flag is set, recompute SHA-1 blob hash for each synced source file
- [x] 1.3 Write updated hashes back into `skills/<name>/reference_manifest.yml`
- [x] 1.4 Write manifests only when at least one hash changed
- [x] 1.5 Add summary line: "Updated N hashes in M manifests"

**Tests:**
- [x] T1.1: `python scripts/sync_shared_refs.py --skill local-model-prompt-engineer --verbose` works unchanged
- [x] T1.2: Edit a shared ref, run with `--update-manifests`, verify hash updates in all affected manifests
- [x] T1.3: Run without flag — no manifest files modified
- [x] T1.4: `python scripts/validate_skills.py` passes

**Stop Condition:** All tests pass, `validate_skills.py` clean.

---

### Phase 2: Harden package_skill.sh — validation gate + MANIFEST.json + SHA-256 [x] (2-3h)

**Objective:** Make the packaging script produce verifiable, self-describing packages with a pre-flight validation gate.

**Inputs:** `scripts/package_skill.sh`, `scripts/validate_skills.py`
**Files/Directories:** `scripts/`, `.agent_work/staged_skills/`, `dist/`

- [x] 2.1 Add pre-package validation: run `python scripts/validate_skills.py`, abort on failure
- [x] 2.2 Generate MANIFEST.json in staging dir before zipping (skill_name, version, package_date, files array with path/sha256/size)
- [x] 2.3 After zip, generate `<skill>-<version>.sha256` checksum file
- [x] 2.4 Replace fragile `unzip -l | tail -1` with reliable Python one-liner or `zipinfo`

**Tests:**
- [x] T2.1: Package each of 5 skills — zip, MANIFEST.json inside zip, .sha256 file created
- [x] T2.2: Extract zip, verify MANIFEST.json checksums match actual files
- [x] T2.3: `sha256sum -c dist/<skill>.sha256` validates
- [x] T2.4: Break a skill (remove SKILL.md) — packaging aborts with clear error

**Stop Condition:** All 5 skills package successfully with manifest and checksum. Broken skill aborts cleanly.

---

### Phase 3: Create build_release.py — the main missing piece [ ] (3-4h)

**Objective:** A single Python script that orchestrates the full release pipeline: sync → validate → package → summary.

**Inputs:** `scripts/sync_shared_refs.py`, `scripts/package_skill.sh`, `scripts/validate_skills.py`
**Files/Directories:** `scripts/build_release.py` (new), `dist/` (new)

- [x] 3.1 Create `scripts/build_release.py` with argparse: `--version`, `--package`, `--dry-run`, `--dist-dir`
- [x] 3.2 Pipeline step a: sync phase — call `sync_shared_refs.py --all --in-place`
- [x] 3.3 Pipeline step b: manifest update — call `sync_shared_refs.py --all --update-manifests`
- [x] 3.4 Pipeline step c: validation — run `validate_skills.py`, abort on failure
- [x] 3.5 Pipeline step d: version bump (if --version) — update SKILL.md frontmatter and manifests, git status check first
- [x] 3.6 Pipeline step e: package phase — call `package_skill.sh` for each skill, output to dist/
- [x] 3.7 Generate `dist/RELEASE_SUMMARY.json` (skill entries with name/version/zip_path/sha256_path/file_count/total_size_bytes)
- [x] 3.8 Print formatted summary table to stdout

**Tests:**
- [ ] T3.1: `--dry-run --package` prints plan without creating files
- [ ] T3.2: `--package` creates all 5 zips, SHA-256 files, RELEASE_SUMMARY.json in dist/
- [ ] T3.3: `--version X.Y.Z --package` bumps versions (test on branch or revert after)
- [ ] T3.4: RELEASE_SUMMARY.json matches actual files

**Stop Condition:** Full pipeline runs end-to-end, produces valid dist/ with summary.

---

### Phase 4: Installation scripts [x] (1-2h)

**Objective:** Make it trivial for end users to install a ContextSmith skill from a package.

**Inputs:** Packages from dist/, MANIFEST.json inside packages
**Files/Directories:** `scripts/install_skill.sh` (new), `scripts/install_all.sh` (new)

- [x] 4.1 Create `install_skill.sh <zip-file> [target-dir]` — extract, verify MANIFEST.json checksums, version comparison, backup old version, copy to target
- [x] 4.2 Create `install_all.sh <dist-dir> [target-dir]` — find all zips in dist/, call install_skill.sh for each, report status

**Tests:**
- [x] T4.1: Install one skill to temp dir — files extracted correctly
- [x] T4.2: Install same skill again — skips (same version)
- [x] T4.3: Bump installed version down, reinstall — backup created, new version installed
- [x] T4.4: `install_all.sh` with all 5 skills to temp dir

**Stop Condition:** All install tests pass.

---

### Phase 5: Documentation [x] (1-2h)

**Objective:** Document the release process for maintainers and installation for users.

**Inputs:** Completed scripts from Phases 1-4
**Files/Directories:** `docs/RELEASE_PROCESS.md` (new), `README.md`, `CHANGELOG.md`

- [x] 5.1 Create `docs/RELEASE_PROCESS.md` — prerequisites, step-by-step checklist, troubleshooting
- [x] 5.2 Update `README.md` — add installation section with copy-paste commands
- [x] 5.3 Update `CHANGELOG.md` — add entries for new scripts and improvements

**Tests:**
- [x] T5.1: Follow RELEASE_PROCESS.md from scratch on clean checkout — all commands reference existing scripts, pipeline dry-run verified
- [x] T5.2: README installation commands are copy-paste executable — scripts exist, are executable, and dry-run passes

**Stop Condition:** Documentation is complete and actionable.

---

### Phase 5.5: All-skills bundle [x] (30m)

**Objective:** Create a single zip containing all 5 skills for distribution as one download.

**Inputs:** Individual skill packages from Phase 3 pipeline
**Files/Directories:** `scripts/build_release.py` (modify), `dist/` (new bundle artifact)

- [x] 5.5.1 Add `--bundle` flag to `build_release.py` — after packaging all individual skills, create combined zip
- [x] 5.5.2 Bundle naming: `contextsmith-all-bundle.zip` containing all skill directories at top level
- [x] 5.5.3 Generate `contextsmith-all-bundle.zip.sha256` for the bundle
- [x] 5.5.4 Include bundle entry in `RELEASE_SUMMARY.json`
- [x] 5.5.5 Update `docs/RELEASE_PROCESS.md` with bundle section
- [x] 5.5.6 Update `README.md` installation section with bundle install command

**Tests:**
- [x] T5.5.1: `--package --bundle` creates bundle zip with all 5 skill directories
- [x] T5.5.2: `sha256sum -c dist/contextsmith-all-bundle.zip.sha256` validates
- [x] T5.5.3: Extract bundle — all 5 skills present with correct structure

**Stop Condition:** Bundle creates, validates, and extracts correctly.

---

### Phase 6: Integration test script [x] (1h)

**Objective:** A single command that validates the entire release pipeline from clean state.

**Inputs:** All scripts from Phases 1-4
**Files/Directories:** `scripts/test_release.sh` (new)

- [x] 6.1 Create `test_release.sh` — temp dir setup, clean, full pipeline run, verify zips/SHA-256/summary, test install to temp dir, cleanup, pass/fail summary
- [x] 6.2 Make script idempotent and safe to run multiple times

**Tests:**
- [x] T6.1: `bash scripts/test_release.sh` passes with exit code 0 (74/74, stable across 3 runs)
- [x] T6.2: Break a skill — test fails with clear error
- [x] T6.3: Fix skill — test passes again

**Stop Condition:** Integration test passes cleanly.

**Bug learned:** `set -euo pipefail` causes `unzip -l | grep -q` to fail intermittently due to pipe exit code handling. Fix: capture `unzip -l` output to variable, then grep from variable.

---

## Phase Dependencies

```
Phase 1 (harden sync_shared_refs.py)
    ├── Phase 2 (harden package_skill.sh)
    │       └── Phase 3 (build_release.py) ← main missing piece
    │               ├── Phase 4 (install scripts)
    │               └── Phase 5 (documentation)
    │                       ├── Phase 5.5 (all-skills bundle)
    │                       └── Phase 6 (integration test)
```

Phase 1 can run in parallel with Phase 2. Phases 3-6 are sequential.

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| build_release.py subprocess calls fail on macOS | Low | Medium | Use Python zipfile module as fallback |
| Version bump overwrites uncommitted SKILL.md changes | Low | High | Git status check before modifying; abort if dirty |
| MANIFEST.json generation adds dependency | N/A | Low | Python already required (PyYAML) |
| Install scripts conflict with existing skill versions | Medium | Low | Backup before overwrite; version comparison skip logic |
