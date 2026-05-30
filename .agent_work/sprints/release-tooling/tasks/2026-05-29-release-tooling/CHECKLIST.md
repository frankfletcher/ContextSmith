# CHECKLIST.md — Release Tooling Sprint

## Phase 1: Harden sync_shared_refs.py
- [x] T1.1: `python scripts/sync_shared_refs.py --skill local-model-prompt-engineer --verbose` works unchanged
- [x] T1.2: Edit a shared ref, run with `--update-manifests`, verify hash updates in all affected manifests
- [x] T1.3: Run without flag — no manifest files modified
- [x] T1.4: `python scripts/validate_skills.py` passes

## Phase 2: Harden package_skill.sh
- [x] T2.1: Package each of 5 skills — zip, MANIFEST.json inside zip, .sha256 file created
- [x] T2.2: Extract zip, verify MANIFEST.json checksums match actual files
- [x] T2.3: `sha256sum -c dist/<skill>.sha256` validates
- [x] T2.4: Break a skill (remove SKILL.md) — packaging aborts with clear error

## Phase 3: Create build_release.py
- [x] T3.1: `--dry-run --package` prints plan without creating files
- [x] T3.2: `--package` creates all 5 zips, SHA-256 files, RELEASE_SUMMARY.json in dist/
- [x] T3.3: `--version X.Y.Z --package` bumps versions (test on branch or revert after)
- [x] T3.4: RELEASE_SUMMARY.json matches actual files

## Phase 4: Installation scripts
- [x] T4.1: Install one skill to temp dir — files extracted correctly
- [x] T4.2: Install same skill again — skips (same version)
- [x] T4.3: Bump installed version down, reinstall — backup created, new version installed
- [x] T4.4: `install_all.sh` with all 5 skills to temp dir

## Phase 5: Documentation
- [ ] T5.1: Follow RELEASE_PROCESS.md from scratch on clean checkout
- [ ] T5.2: README installation commands are copy-paste executable

## Phase 6: Integration test script
- [ ] T6.1: `bash scripts/test_release.sh` passes with exit code 0
- [ ] T6.2: Break a skill — test fails with clear error
- [ ] T6.3: Fix skill — test passes again

## Post-Sprint Validation
- [ ] `python scripts/validate_skills.py` passes after all changes
- [ ] All success criteria from TASK.md met
