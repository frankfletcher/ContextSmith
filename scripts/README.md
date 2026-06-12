# ContextSmith Scripts

Quick-reference for all build, sync, validation, and release scripts.

## Quick Reference

| Script | Purpose |
|---|---|
| [`validate_skills.py`](#validate_skillspy) | Validates SKILL.md frontmatter, line counts, reference manifests, and shared reference formatting |
| [`token_budget.py`](#token_budgetpy) | Reports approximate token budgets for skills and common load sets |
| [`sync_shared_refs.py`](#sync_shared_refspy) | Populates skill `references/` from `shared/` via `reference_manifest.yml` |
| [`build_release.py`](#build_releasepy) | Orchestrates the full release pipeline: sync → manifest update → validate → token budget → (version bump) → bundle |
| [`package_skill.sh`](#package_skillsh) | Packages a single skill into a zip with checksums |
| [`install_skill.sh`](#install_skillsh) | Installs a skill zip to a target directory with checksum verification |
| [`install_all.sh`](#install_allsh) | Installs all skill zips from a dist directory |
| [`publish_release.sh`](#publish_releasesh) | Builds and publishes a release to GitHub (tags + `gh release`) |
| [`test_release.sh`](#test_releasesh) | End-to-end integration test for the release pipeline |

---

## validate_skills.py {#validate_skillspy}

Validates SKILL.md frontmatter, line counts, reference manifests, and shared reference formatting.

```bash
python scripts/validate_skills.py
```

**Options:** None.

**Exit codes:**
- `0` — all checks passed
- `1` — one or more errors found

**Output example:**
```
OK contextsmith: 120 lines, version=1.7.0, refs=True
WARN contextsmith-run: metadata.version missing
ERROR contextsmith-prompt-engineer: missing reference_manifest.yml
Validation complete
```

---

## token_budget.py {#token_budgetpy}

Reports approximate token budgets for skills and common load sets.

```bash
python scripts/token_budget.py
```

**Options:**

| Flag | Description |
|---|---|
| `--strict` | Exit non-zero when a SKILL.md exceeds its budget |

**Exit codes:**
- `0` — all budgets within limits (or `--strict` not set)
- `1` — one or more skills exceed budget (only with `--strict`)

**Output:** Three tables — skill budgets, common load-set estimates, and largest shared references.

---

## sync_shared_refs.py {#sync_shared_refspy}

Populates skill `references/` directories from `shared/` using each skill's `reference_manifest.yml`.

By default writes to a staging directory (`.agent_work/staged_skills/`) so the repo working tree stays clean.

```bash
# Staging (default) — writes to .agent_work/staged_skills/
python scripts/sync_shared_refs.py

# Staging for a single skill
python scripts/sync_shared_refs.py --skill contextsmith-prompt-engineer

# Write directly into skills/*/references/ (for CI validation)
python scripts/sync_shared_refs.py --in-place

# Dry run — print what would be copied
python scripts/sync_shared_refs.py --dry-run

# Update manifest hashes (recompute SHA-1 blob hashes)
python scripts/sync_shared_refs.py --update-manifests

# Custom staging location
python scripts/sync_shared_refs.py --staging-dir /tmp/my_staging
```

**Options:**

| Flag | Description |
|---|---|
| `--all` | Sync all skills (default) |
| `--skill <name>` | Sync only the named skill directory |
| `--dry-run` | Print what would be copied without copying |
| `--verbose` | Print each file operation |
| `--force` | Overwrite even if content hashes match |
| `--staging-dir <dir>` | Output staging directory (default: `.agent_work/staged_skills/`) |
| `--in-place` | Write directly into `skills/*/references/` instead of staging |
| `--update-manifests` | Recompute SHA-1 blob hashes and write back to `reference_manifest.yml` |
| `--repo-root <dir>` | Override repo root directory (for testing) |

**Exit codes:**
- `0` — synced successfully
- `1` — one or more errors (e.g., missing required source files)

**Fixing stale manifest warnings:**
If you see `WARN ...: manifest version stale for ...`, run:
```bash
python scripts/sync_shared_refs.py --update-manifests
```

---

## build_release.py {#build_releasepy}

Orchestrates the full release pipeline: sync → manifest update → validate → token budget → (version bump) → package/bundle.

```bash
# Full pipeline with bundle
python scripts/build_release.py --package

# Full pipeline with individual per-skill zips and bundle
python scripts/build_release.py --package --individual

# With version bump
python scripts/build_release.py --package --individual --version 1.7.0

# Dry run
python scripts/build_release.py --package --dry-run

# Custom output directory
python scripts/build_release.py --package --dist-dir /tmp/release
```

**Options:**

| Flag | Description |
|---|---|
| `--package` | Run the full release pipeline and create packages (required) |
| `--version <ver>` | Bump all skill versions before packaging |
| `--dry-run` | Print what would be done without executing |
| `--bundle` | Create release bundle (default) |
| `--individual` | Also create individual per-skill zip packages |
| `--dist-dir <dir>` | Output directory for packages (default: `dist/`) |

**Pipeline steps:**
1. **Sync** — runs `sync_shared_refs.py --in-place`
2. **Manifest update** — runs `sync_shared_refs.py --update-manifests`
3. **Validate** — runs `validate_skills.py`
4. **Token budget** — runs `token_budget.py --strict`
5. **Version bump** (optional) — updates versions in SKILL.md and manifests
6. **Package** (with `--individual`) — runs `package_skill.sh` per skill
7. **Bundle** (with `--bundle`) — stages files and creates `contextsmith-release.zip`
8. **Summary** — generates `RELEASE_SUMMARY.json`

---

## package_skill.sh {#package_skillsh}

Packages a single skill into a zip with a SHA-256 checksum file.

```bash
bash scripts/package_skill.sh <skill-name> [output-dir]
```

**Arguments:**

| Position | Description |
|---|---|
| `<skill-name>` | Skill directory name (e.g., `contextsmith-prompt-engineer`) |
| `[output-dir]` | Output directory (default: `dist/`) |

**Example:**
```bash
bash scripts/package_skill.sh contextsmith-prompt-engineer
bash scripts/package_skill.sh contextsmith-prompt-engineer /tmp/release
```

**What it does:**
1. Syncs references to staging (`.agent_work/staged_skills/`)
2. Runs validation
3. Generates `MANIFEST.json` with file checksums
4. Creates `<skill>-<version>.zip` and `<skill>-<version>.sha256`

---

## install_skill.sh {#install_skillsh}

Installs a skill zip package to a target directory with checksum verification.

```bash
bash scripts/install_skill.sh <zip-file> [target-dir]
```

**Arguments:**

| Position | Description |
|---|---|
| `<zip-file>` | Path to the skill zip file |
| `[target-dir]` | Target directory (default: `~/.agents/skills`) |

**Example:**
```bash
bash scripts/install_skill.sh dist/contextsmith-prompt-engineer-1.7.0.zip
bash scripts/install_skill.sh dist/contextsmith-prompt-engineer-1.7.0.zip /custom/skills
```

**What it does:**
1. Extracts zip to a temp directory
2. Verifies all file checksums against `MANIFEST.json`
3. Backs up existing installation (if any)
4. Copies to target directory

---

## install_all.sh {#install_allsh}

Installs all skill zip packages from a dist directory.

```bash
bash scripts/install_all.sh <dist-dir> [target-dir]
```

**Arguments:**

| Position | Description |
|---|---|
| `<dist-dir>` | Directory containing skill zip files |
| `[target-dir]` | Target directory (default: `~/.agents/skills`) |

**Example:**
```bash
bash scripts/install_all.sh dist
bash scripts/install_all.sh dist /custom/skills
```

**What it does:**
1. Finds all skill zips in the dist directory (excludes `contextsmith-release.zip`)
2. Calls `install_skill.sh` for each
3. Prints a summary report

---

## publish_release.sh {#publish_releasesh}

Builds and publishes a release to GitHub with tags and `gh release`.

```bash
bash scripts/publish_release.sh <version> [options]
```

**Arguments:**

| Position | Description |
|---|---|
| `<version>` | Release version (e.g., `1.7.0`) |

**Options:**

| Flag | Description |
|---|---|
| `--dry-run` | Print what would be done without executing |
| `--skip-build` | Skip `build_release.py` (use existing `dist/`) |
| `--skip-push` | Skip git push and `gh release create` |
| `--prerelease` | Mark as a prerelease on GitHub |
| `--draft` | Create as a draft release on GitHub |
| `--notes <file>` | Use file as release notes (default: auto-generate from `CHANGELOG.md`) |
| `--dist-dir <dir>` | Override dist directory (default: `dist/`) |

**Example:**
```bash
bash scripts/publish_release.sh 1.7.0
bash scripts/publish_release.sh 1.7.0 --dry-run
bash scripts/publish_release.sh 1.7.0 --skip-push
```

**Prerequisites:** python3, gh CLI (authenticated), git, zip, sha256sum, PyYAML, clean working tree.

---

## test_release.sh {#test_releasesh}

End-to-end integration test for the release pipeline.

```bash
bash scripts/test_release.sh
```

**Options:** None.

**What it does:**
1. Creates a clean temp directory
2. Runs the full build pipeline
3. Verifies all zip artifacts and checksums
4. Verifies zip contents (SKILL.md, references/, MANIFEST.json)
5. Verifies bundle contents
6. Verifies `RELEASE_SUMMARY.json`
7. Tests installation via `install_all.sh`
8. Tests idempotent re-install (same version should skip)
9. Verifies installed file checksums
10. Cleans up temp directory on exit
