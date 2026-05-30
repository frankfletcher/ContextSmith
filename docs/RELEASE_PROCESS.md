# Release Process

This guide walks maintainers through building, verifying, and distributing ContextSmith skill packages.

## Prerequisites

- Python 3 with PyYAML (`pip install pyyaml`)
- `zip` and `unzip` commands
- `sha256sum` (coreutils on Linux, `brew install coreutils` on macOS)
- `git` (for clean-tree checks during version bumps)
- A clean working tree (no uncommitted changes to tracked files)

## Quick Release

Build all 5 skill packages into `dist/`:

```bash
python scripts/build_release.py --package
```

This runs the full pipeline: sync references, update manifests, validate, package, and generate summary.

## Step-by-Step Checklist

### 1. Verify the working tree is clean

```bash
git status --short
```

If there are uncommitted changes to tracked files, commit or stash them before proceeding. The version bump step will abort if the tree is dirty.

### 2. Preview the release (dry run)

```bash
python scripts/build_release.py --package --dry-run
```

This prints every step the pipeline will execute without modifying any files.

### 3. Run the release pipeline

```bash
# Without version bump (uses current versions from manifests)
python scripts/build_release.py --package

# With version bump
python scripts/build_release.py --package --version 1.5.0

# With all-skills bundle
python scripts/build_release.py --package --bundle
```

The pipeline executes in this order:

| Step | Script | Purpose |
|------|--------|---------|
| A | `sync_shared_refs.py --all --in-place` | Copy shared references to staging |
| B | `sync_shared_refs.py --all --update-manifests` | Recompute stale SHA-1 hashes |
| C | `validate_skills.py` | Abort if any skill fails validation |
| D | *(optional)* Version bump | Update SKILL.md and manifest versions |
| E | `package_skill.sh` (per skill) | Create zip, MANIFEST.json, .sha256 |
| F | *(optional)* Bundle | Create combined all-skills zip |
| G | Summary | Generate `RELEASE_SUMMARY.json` and print table |

### 4. Verify the output

```bash
# Check all zip checksums
sha256sum -c dist/*.sha256

# Inspect summary
cat dist/RELEASE_SUMMARY.json
```

Each `dist/` entry:
- `{skill}-{version}.zip` — the skill package
- `{skill}-{version}.sha256` — zip-level checksum for `sha256sum -c`
- `contextsmith-all-bundle.zip` — combined all-skills package (when `--bundle` is used)
- `contextsmith-all-bundle.zip.sha256` — bundle checksum
- `RELEASE_SUMMARY.json` — per-skill metadata (name, version, file count, size)

### 5. Test installation (optional but recommended)

```bash
# Install a single skill to a temp directory
bash scripts/install_skill.sh dist/local-model-prompt-engineer-1.0.0.zip /tmp/test-install

# Install all skills
bash scripts/install_all.sh dist /tmp/test-install-all
```

## Packaging a Single Skill

If you only need to package one skill (e.g., after editing a single skill):

```bash
bash scripts/package_skill.sh local-model-prompt-engineer [output-dir]
```

This syncs references, validates, generates MANIFEST.json, creates the zip, and produces the `.sha256` file. Output defaults to `dist/`.

## Installation Scripts

### Install a single skill

```bash
bash scripts/install_skill.sh <zip-file> [target-dir]
```

- Extracts to a temp directory
- Verifies all file SHA-256 checksums against MANIFEST.json
- Compares installed version vs package version
- Skips if same version is already installed
- Backs up existing installation with timestamped rename before upgrading
- Default target: `~/.agents/skills/`

### Install all skills from dist/

```bash
bash scripts/install_all.sh <dist-dir> [target-dir]
```

Finds all `.zip` files, delegates to `install_skill.sh`, and prints a summary table.

### Install from the all-skills bundle

```bash
# Extract bundle, then install each skill
unzip contextsmith-all-bundle.zip -d /tmp/bundle-extract
for skill_dir in /tmp/bundle-extract/*/; do
  bash scripts/install_skill.sh "$skill_dir" [target-dir]
done
```

Or install all individual zips from `dist/` (recommended — checksums are verified):

```bash
bash scripts/install_all.sh dist ~/.agents/skills
```

## All-Skills Bundle

Add `--bundle` to create a single zip containing all 5 skills:

```bash
python scripts/build_release.py --package --bundle
```

Produces `dist/contextsmith-all-bundle.zip` (all skill directories at top level) and its `.sha256` file. Useful for distribution as a single download.

## Custom Output Directory

```bash
python scripts/build_release.py --package --dist-dir /tmp/my-release
```

## Troubleshooting

### "ERROR: Working tree is dirty"

The version bump step checks `git diff --name-only` and aborts if tracked files have uncommitted changes. Commit or stash your changes, then retry.

### "ERROR: validation failed, aborting"

`validate_skills.py` found an issue (missing SKILL.md, bad frontmatter YAML, line count exceeded, etc.). Run it standalone to see details:

```bash
python scripts/validate_skills.py
```

### "ERROR: zip command not found"

Install the `zip` package:
- Ubuntu/Debian: `sudo apt install zip unzip`
- macOS: `brew install zip`
- Fedora: `sudo dnf install zip unzip`

### "ERROR: sha256sum is required but not found on PATH"

On macOS, install coreutils: `brew install coreutils`. On Linux, it's part of coreutils and should be available by default.

### MANIFEST.json checksum mismatch during install

The package zip was corrupted or modified after packaging. Re-run the release pipeline to regenerate packages.

### "WARN: overwriting existing zip"

A zip with the same name already exists in `dist/`. This is normal when re-packaging the same version. The old zip is replaced.

### Backup directories accumulating

`install_skill.sh` creates timestamped backups (`<skill>.backup.<YYYYMMDDHHmmss>`) when upgrading. Clean old backups manually:

```bash
ls -t ~/.agents/skills/ | grep backup | tail -n +3 | xargs rm -rf
```

This keeps the two most recent backups.

## Publishing to GitHub

### Automated publish

```bash
# Build and publish in one command
bash scripts/publish_release.sh 1.5.0

# Dry-run (no changes)
bash scripts/publish_release.sh 1.5.0 --dry-run

# Build only, skip GitHub push (for manual review)
bash scripts/publish_release.sh 1.5.0 --skip-push

# Prerelease
bash scripts/publish_release.sh 1.5.0-rc.1 --prerelease

# Draft release
bash scripts/publish_release.sh 1.5.0 --draft

# Custom release notes
bash scripts/publish_release.sh 1.5.0 --notes my-notes.md
```

The publish script:
1. Builds the release (calls `build_release.py --package --bundle`)
2. Verifies all SHA-256 checksums
3. Creates an annotated git tag
4. Pushes the tag to origin
5. Creates the GitHub release via `gh` CLI
6. Uploads all dist/ artifacts (zips, checksums, RELEASE_SUMMARY.json)

### Manual publish

If you prefer to publish manually:

```bash
# Build
python scripts/build_release.py --package --bundle

# Verify
sha256sum -c dist/*.sha256

# Tag and push
git tag -a v1.5.0 -m "ContextSmith v1.5.0"
git push origin v1.5.0

# Create release
gh release create v1.5.0 \
  --title "ContextSmith v1.5.0" \
  --notes-file <notes.md> \
  dist/*.zip dist/*.sha256 dist/RELEASE_SUMMARY.json
```

## Pipeline Architecture

```
publish_release.sh
└── build_release.py
    ├── sync_shared_refs.py   (steps A, B)
    ├── validate_skills.py    (step C)
    ├── package_skill.sh      (step E, per skill)
    └── generates RELEASE_SUMMARY.json (step F)

install_skill.sh          (standalone, consumes dist/ packages)
install_all.sh            (standalone, delegates to install_skill.sh)
test_release.sh           (integration test, 74 assertions)
```

Scripts delegate via `subprocess.run()` or direct bash invocation — no logic duplication. Changes to an underlying script automatically propagate to the pipeline.
