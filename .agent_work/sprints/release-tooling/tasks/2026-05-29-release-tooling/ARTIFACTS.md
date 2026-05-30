# ARTIFACTS.md — Release Tooling Sprint

## Changed Files

### Planning follow-up
- `skills/local-model-prompt-engineer/SKILL.md` — implementation-plan prompts now require concrete task-state artifacts for long-running planning work.
- `skills/local-model-instruction-engineer/SKILL.md` — generated repo instructions must require concrete task-state artifacts for downstream planning.
- `skills/local-model-skill-engineer/SKILL.md` — generated skills that direct long-running work must embed the concrete task-state contract.
- `skills/local-model-skill-migrator/SKILL.md` — multi-phase migrations must maintain task-state files in addition to migration plans.
- `skills/local-model-agent-evaluator/SKILL.md` — audits now flag narrative-only persistent state as high-risk.
- `CHANGELOG.md` — Unreleased note added for task-state contract hardening.

### Phase 1
- `scripts/sync_shared_refs.py` — added `--update-manifests` flag with `update_manifest_hashes()` function; recomputes SHA-1 blob hashes for synced source files and writes back to `reference_manifest.yml` only when at least one hash changed.
- `skills/*/reference_manifest.yml` (all 5) — hashes updated by `--update-manifests` during Phase 1 testing.

### Phase 2
- `scripts/package_skill.sh` — added pre-package validation gate (validate_skills.py), MANIFEST.json generation (SHA-256 per-file checksums), `.sha256` checksum file generation, and reliable file count via Python zipfile module. Grew from 82 to 135 lines.

### Phase 3
- `scripts/build_release.py` — new release orchestrator (~260 lines). Pipeline: sync → manifest update → validate → version bump (optional) → package → summary. CLI: `--version`, `--package`, `--dry-run`, `--dist-dir`. Generates `dist/RELEASE_SUMMARY.json` with per-skill metadata and formatted stdout table.

### Phase 4
- `scripts/install_skill.sh` — new installation script (~100 lines). Extracts zip to temp dir, verifies MANIFEST.json SHA-256 checksums via Python, compares installed vs package version, backs up existing installation with timestamped rename, copies to target. Default target: `~/.agents/skills/`.
- `scripts/install_all.sh` — new batch installation script (~70 lines). Finds all .zip files in dist directory, delegates to install_skill.sh for each, prints summary table with success/fail counts.

## Generated Files

### Planning follow-up
- `.agent_work/sprints/release-tooling/tasks/2026-05-29-release-tooling/NEXT_PROMPT.md`

### Phase 2 (dist/ artifacts)
- `dist/local-model-prompt-engineer-1.0.0.zip` (66602 bytes, 60 files)
- `dist/local-model-prompt-engineer-1.0.0.sha256`
- `dist/local-model-skill-engineer-1.0.0.zip` (65504 bytes, 60 files)
- `dist/local-model-skill-engineer-1.0.0.sha256`
- `dist/local-model-instruction-engineer-1.0.0.zip` (66207 bytes, 60 files)
- `dist/local-model-instruction-engineer-1.0.0.sha256`
- `dist/local-model-agent-evaluator-1.0.0.zip` (62255 bytes, 59 files)
- `dist/local-model-agent-evaluator-1.0.0.sha256`
- `dist/local-model-skill-migrator-1.0.0.zip` (63695 bytes, 60 files)
- `dist/local-model-skill-migrator-1.0.0.sha256`

## Commands Run

### Phase 1
- `python scripts/sync_shared_refs.py --skill local-model-prompt-engineer --verbose` — existing behavior unchanged
- `python scripts/sync_shared_refs.py --all --update-manifests` — hash recomputation and manifest write-back
- `python scripts/validate_skills.py` — passed

### Phase 2
- `bash scripts/package_skill.sh <each-of-5-skills>` — all 5 packaged successfully with MANIFEST.json and .sha256
- `sha256sum -c dist/*.sha256` — all 5 checksums verified OK
- Python zipfile MANIFEST.json checksum verification — all 5 skills pass (54-55 files each)
- SKILL.md removal test on local-model-agent-evaluator — packaging aborted with `ERROR: SKILL.md not found` and exit code 1
- `python scripts/validate_skills.py` — passed after all changes

### Phase 3
- `python scripts/build_release.py --package --dry-run` — printed plan without creating files (T3.1)
- `python scripts/build_release.py --package` — full pipeline: sync, validate, package all 5 skills, summary (T3.2)
- `python scripts/build_release.py --package --version 1.1.0` — bumped all versions, packaged with new version (T3.3, on test branch, reverted)
- RELEASE_SUMMARY.json verification — all zip and sha256 paths match actual dist/ files (T3.4)
- `python scripts/validate_skills.py` — passed after all changes

### Phase 4
- `bash scripts/install_skill.sh dist/local-model-prompt-engineer-1.0.0.zip <temp-dir>` — installed with checksum verification (T4.1)
- `bash scripts/install_skill.sh dist/local-model-prompt-engineer-1.0.0.zip <temp-dir>` (repeat) — skipped same version (T4.2)
- Downgraded installed MANIFEST.json to v0.9.0, reinstalled v1.0.0 — backup created, new version installed (T4.3)
- `bash scripts/install_all.sh dist <temp-dir>` — all 10 packages (5 skills x 2 versions) installed, 0 failures (T4.4)
- `python scripts/validate_skills.py` — passed after all changes
