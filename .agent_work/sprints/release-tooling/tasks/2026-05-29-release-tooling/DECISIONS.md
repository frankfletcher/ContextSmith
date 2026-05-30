# DECISIONS.md — Release Tooling Sprint

| # | Decision | Reason | Impact |
|---|----------|--------|--------|
| D1 | build_release.py will be Python, not shell | Cross-platform compatibility, native PyYAML/JSON support, subprocess management for calling existing scripts | Requires Python 3 (already a dependency) |
| D2 | Phase 1 adds --update-manifests flag only; no rewrite of sync_shared_refs.py | Script is production-ready with full CLI surface. Rewriting risks regressions. | Minimal change surface, lower risk |
| D3 | MANIFEST.json uses SHA-256 for file checksums (not SHA-1) | SHA-256 is the standard for package integrity verification. SHA-1 is used internally by sync for git-compatible blob comparison. | Install scripts can verify with sha256sum |
| D4 | Version bump checks git status first | Prevents overwriting uncommitted SKILL.md changes | Requires clean working tree for --version flag |
| D5 | dist/ created at release time, always gitignored | Keeps repo clean, distribution artifacts are reproducible | Users must run build_release.py to get packages |
| D6 | Long-running planning workflows must require concrete task-state files | A single plan file allowed downstream agents to skip `NEXT_PROMPT.md` and other handoff artifacts | Prompt, instruction, skill, migrator, and evaluator workflows now generate or audit the concrete artifact contract |
| D7 | update_manifest_hashes() called before file copying in sync_skill() | Manifest updates operate on source files only; no dependency on staging state | Keeps manifest logic independent of sync destination |
| D8 | total dict includes manifestsUpdated/hashesUpdated keys | Ensures aggregation works across all skills in main() | Summary line prints correct totals |
| D9 | MANIFEST.json excludes itself from file list | Prevents stale hash mismatch on repackage — MANIFEST.json is written after the directory walk | Manifest integrity is verifiable across repackages |
| D10 | SHA-256 checksum file uses relative basename | `sha256sum -c` works from dist/ directory without path issues | User-friendly verification workflow |
| D11 | build_release.py uses subprocess.run() to call existing scripts | Reuses tested sync, validate, and package scripts without duplicating logic | Changes to underlying scripts automatically propagate to the pipeline |
| D12 | Version bump updates both SKILL.md frontmatter and reference_manifest.yml | Keeps package version (from manifest) and skill version (from SKILL.md) in sync | Package filenames reflect the bumped version |
| D13 | Git clean check uses `git diff --name-only` (tracked files only) | Untracked files like the script itself don't block version bump | Still protects against overwriting uncommitted changes to tracked files |
| D14 | RELEASE_SUMMARY.json sha256_path matches package_skill.sh naming (`{skill}-{version}.sha256`) | Summary paths must match actual dist/ filenames for verification | Initial implementation used `{skill}-{version}.zip.sha256` — corrected after T3.4 |
| D15 | install_skill.sh uses Python for MANIFEST.json checksum verification | Python is already a dependency; avoids requiring jq or sha256sum per-file loops in shell | Consistent with package_skill.sh's Python-based MANIFEST.json generation |
| D16 | install_skill.sh extracts to temp dir before installing | Allows full verification before touching target directory. Failed verification leaves target untouched. | Requires sufficient temp disk space (typically negligible for ~60KB packages) |
| D17 | Backup uses timestamped directory rename (`<skill>.backup.<timestamp>`) | Simple, atomic operation. No need for compression or archival. | Accumulates backups over time — user responsibility to clean |
| D18 | install_all.sh delegates to install_skill.sh rather than duplicating logic | Single source of truth for install behavior. Changes to install_skill.sh automatically apply to batch installs. | install_all.sh is a thin orchestrator, not a standalone installer |
| D19 | RELEASE_PROCESS.md is a standalone maintainer guide, not inline README | README is for users; release process is for maintainers. Separating them keeps the landing page concise and the release guide comprehensive. | Users see install commands; maintainers follow RELEASE_PROCESS.md |
| D20 | README shows two install tiers: quick copy and package-based | Existing users expect `cp -r`; new users should use verified packages. Both paths are valid but package-based is recommended. | README installation section has a "recommended" label on the package path |
| D21 | CHANGELOG entries for sprint scripts go under "Unreleased" | The sprint hasn't been tagged as a release yet. Entries will be moved to a versioned section when the release is cut. | Consistent with prior CHANGELOG convention |
| D22 | test_release.sh captures `unzip -l` output to variable before grep | `set -euo pipefail` causes `unzip -l | grep -q` to fail intermittently due to pipe exit code handling — capturing to variable avoids the pipe entirely | More reliable zip content verification under strict shell settings |
| D23 | test_release.sh validates negative case (broken skill) | Integration tests should verify that failures are caught with clear errors, not just that the happy path works | Confirms the pipeline's validation gates actually work |
