# TASK.md — Release Tooling Sprint

## Objective

Complete Idea #1 from `.agent_work/top5_ideas_to_implement.md`: automate the syncing of 42 shared references across 5 skills and build a release builder (`scripts/build_release.py`) for packaging and distribution.

## Scope

- Harden `scripts/sync_shared_refs.py` with manifest update mode
- Harden `scripts/package_skill.sh` with validation gate, MANIFEST.json, SHA-256 checksums
- Create `scripts/build_release.py` (main missing backlog item) — full release orchestrator
- Create installation scripts (`install_skill.sh`, `install_all.sh`)
- Document the release process and update README with installation instructions
- Build an end-to-end integration test script

## Constraints

- Python 3 + PyYAML are the only runtime dependencies (already in use)
- Shell scripts must use bash with `set -euo pipefail`
- `dist/` is gitignored; create at release time only
- `.agent_work/staged_skills/` is gitignored; used as staging area by sync script
- No destructive Git operations without explicit user approval (see behavioral contracts)
- Each phase must be completable in a single agent session (1-4 hours)

## Success Criteria

- `python scripts/build_release.py --package` produces valid packages for all 5 skills in `dist/`
- Each zip contains SKILL.md, references/, and MANIFEST.json with correct checksums
- Each zip has a corresponding `.sha256` file that validates
- `scripts/install_skill.sh` correctly installs to target directory with backup
- `scripts/install_all.sh` installs all 5 skills from dist/ without errors
- `dist/RELEASE_SUMMARY.json` contains accurate metadata for all packages
- `docs/RELEASE_PROCESS.md` exists and is actionable (can be followed step-by-step)
- `README.md` has an installation section with working commands
- `bash scripts/test_release.sh` passes end-to-end from clean state
- `python scripts/validate_skills.py` passes after all changes
