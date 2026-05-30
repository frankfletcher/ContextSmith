#!/usr/bin/env bash
# publish_release.sh — Build and publish a ContextSmith release to GitHub.
#
# Usage:
#   bash scripts/publish_release.sh <version> [options]
#
# Options:
#   --dry-run          Print what would be done without executing
#   --skip-build       Skip build_release.py (use existing dist/)
#   --skip-push        Skip git push and gh release create
#   --prerelease       Mark as a prerelease on GitHub
#   --draft            Create as a draft release on GitHub
#   --notes FILE       Use FILE as release notes (default: auto-generate from CHANGELOG.md)
#   --dist-dir DIR     Override dist/ directory (default: ./dist)
#
# Prerequisites:
#   - Python 3 with PyYAML
#   - gh CLI authenticated (gh auth login)
#   - git remote origin configured
#   - Clean working tree (no uncommitted changes to tracked files)
#
# Example:
#   bash scripts/publish_release.sh 1.5.0
#   bash scripts/publish_release.sh 1.5.0 --dry-run
#   bash scripts/publish_release.sh 1.5.0 --notes my-notes.md --prerelease

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Parse arguments
VERSION=""
DRY_RUN=false
SKIP_BUILD=false
SKIP_PUSH=false
PRERELEASE=false
DRAFT=false
NOTES_FILE=""
DIST_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --skip-build)
      SKIP_BUILD=true
      shift
      ;;
    --skip-push)
      SKIP_PUSH=true
      shift
      ;;
    --prerelease)
      PRERELEASE=true
      shift
      ;;
    --draft)
      DRAFT=true
      shift
      ;;
    --notes)
      NOTES_FILE="$2"
      shift 2
      ;;
    --dist-dir)
      DIST_DIR="$2"
      shift 2
      ;;
    -*)
      echo "ERROR: Unknown option: $1"
      echo "Usage: bash scripts/publish_release.sh <version> [options]"
      exit 1
      ;;
    *)
      if [[ -z "$VERSION" ]]; then
        VERSION="$1"
      else
        echo "ERROR: Unexpected argument: $1"
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ -z "$VERSION" ]]; then
  echo "ERROR: Version is required."
  echo "Usage: bash scripts/publish_release.sh <version> [options]"
  exit 1
fi

TAG="v${VERSION}"
DEFAULT_DIST="${REPO_ROOT}/dist"
ACTUAL_DIST="${DIST_DIR:-$DEFAULT_DIST}"

echo "ContextSmith Release Publisher"
echo "Version: ${VERSION}"
echo "Tag: ${TAG}"
echo "Dist: ${ACTUAL_DIST}"
echo "Repo: ${REPO_ROOT}"
if $DRY_RUN; then
  echo "Mode: DRY RUN"
fi
echo ""

# Check prerequisites
check_prerequisites() {
  local missing=0

  if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is required but not found on PATH"
    missing=1
  fi

  if ! command -v gh &>/dev/null; then
    echo "ERROR: gh CLI is required but not found on PATH"
    echo "Install: https://cli.github.com/"
    missing=1
  fi

  if ! command -v git &>/dev/null; then
    echo "ERROR: git is required but not found on PATH"
    missing=1
  fi

  if ! command -v zip &>/dev/null; then
    echo "ERROR: zip is required but not found on PATH"
    missing=1
  fi

  if ! command -v sha256sum &>/dev/null; then
    echo "ERROR: sha256sum is required but not found on PATH"
    echo "On macOS: brew install coreutils"
    missing=1
  fi

  if ! $SKIP_PUSH; then
    if ! gh auth status &>/dev/null; then
      echo "ERROR: gh CLI is not authenticated. Run: gh auth login"
      missing=1
    fi
  fi

  if [[ -n "$(git -C "$REPO_ROOT" diff --name-only)" ]]; then
    echo "ERROR: Working tree is dirty. Commit or stash changes before publishing."
    missing=1
  fi

  return $missing
}

# Build the release
do_build() {
  echo "=== Step 1: Build release ==="

  local build_cmd=(
    python3 "${REPO_ROOT}/scripts/build_release.py"
    --package
    --dist-dir "$ACTUAL_DIST"
  )

  if $DRY_RUN; then
    echo "  [DRY-RUN] Would run: ${build_cmd[*]}"
    return 0
  fi

  echo "  Running: ${build_cmd[*]}"
  "${build_cmd[@]}"
  echo ""
}

# Verify dist/ artifacts
verify_artifacts() {
  echo "=== Step 2: Verify artifacts ==="

  if [[ ! -d "$ACTUAL_DIST" ]]; then
    echo "ERROR: dist/ directory not found at ${ACTUAL_DIST}"
    return 1
  fi

  local zip_count
  zip_count=$(find "$ACTUAL_DIST" -maxdepth 1 -name "*.zip" ! -name "*.sha256" | wc -l)
  if [[ "$zip_count" -eq 0 ]]; then
    echo "ERROR: No zip files found in ${ACTUAL_DIST}"
    return 1
  fi

  echo "  Found ${zip_count} zip file(s)"

  # Verify SHA-256 checksums
  local sha_files
  sha_files=$(find "$ACTUAL_DIST" -maxdepth 1 -name "*.sha256" | wc -l)
  if [[ "$sha_files" -gt 0 ]]; then
    echo "  Verifying ${sha_files} SHA-256 checksum(s)..."
    if $DRY_RUN; then
      echo "  [DRY-RUN] Would run: sha256sum -c for each .sha256 in ${ACTUAL_DIST}"
    else
      local failed=0
      for sha_file in "$ACTUAL_DIST"/*.sha256; do
        local basename
        basename=$(basename "$sha_file")
        if (cd "$ACTUAL_DIST" && sha256sum -c "$basename") &>/dev/null; then
          echo "    OK: ${basename}"
        else
          echo "    FAIL: ${basename}"
          failed=1
        fi
      done
      if [[ "$failed" -ne 0 ]]; then
        echo "ERROR: SHA-256 verification failed"
        return 1
      fi
    fi
  fi

  # Check for RELEASE_SUMMARY.json
  if [[ -f "${ACTUAL_DIST}/RELEASE_SUMMARY.json" ]]; then
    echo "  OK: RELEASE_SUMMARY.json present"
  else
    echo "  WARN: RELEASE_SUMMARY.json not found"
  fi

  echo ""
}

# Generate release notes
generate_notes() {
  local notes_content=""

  if [[ -n "$NOTES_FILE" ]]; then
    if [[ ! -f "$NOTES_FILE" ]]; then
      echo "ERROR: Notes file not found: ${NOTES_FILE}"
      return 1
    fi
    notes_content=$(cat "$NOTES_FILE")
  else
    # Auto-generate from CHANGELOG.md
    local changelog="${REPO_ROOT}/CHANGELOG.md"
    if [[ ! -f "$changelog" ]]; then
      echo "ERROR: CHANGELOG.md not found at ${changelog}"
      return 1
    fi

    # Extract the section for this version
    notes_content=$(python3 -c "
import re, sys

with open('${changelog}', 'r') as f:
    content = f.read()

# Find the section for this version
version = '${VERSION}'
pattern = rf'## v?{re.escape(version)}\s*\n(?:\*\*Released:\*\*.*?\n)?\s*\n(.*?)(?=^## [^#]|\Z)'
match = re.search(pattern, content, re.DOTALL | re.MULTILINE)

if match:
    section = match.group(1).strip()
    if section:
        print(section)
    else:
        print(f'## ContextSmith v{version}')
        print()
        print('Release notes not found in CHANGELOG.md for v{version}.')
        print('Please add release notes to CHANGELOG.md and retry.')
        sys.exit(1)
else:
    print(f'## ContextSmith v{version}')
    print()
    print('Release notes not found in CHANGELOG.md for v{version}.')
    print('Please add release notes to CHANGELOG.md and retry.')
    sys.exit(1)
")
  fi

  echo "$notes_content"
}

# Create git tag and push
do_git_tag() {
  echo "=== Step 3: Git tag ==="

  if $DRY_RUN; then
    echo "  [DRY-RUN] Would create tag: ${TAG}"
    echo "  [DRY-RUN] Would push tag to origin"
    return 0
  fi

  # Check if tag already exists
  if git -C "$REPO_ROOT" rev-parse "$TAG" &>/dev/null; then
    echo "  WARN: Tag ${TAG} already exists locally"
    if git -C "$REPO_ROOT" ls-remote origin "refs/tags/${TAG}" &>/dev/null; then
      echo "  WARN: Tag ${TAG} already exists on remote"
    fi
  else
    local tag_message="ContextSmith v${VERSION}"
    echo "  Creating annotated tag: ${TAG}"
    git -C "$REPO_ROOT" tag -a "$TAG" -m "$tag_message"
  fi

  if ! $SKIP_PUSH; then
    echo "  Pushing tag to origin..."
    git -C "$REPO_ROOT" push origin "$TAG"
  fi

  echo ""
}

# Create GitHub release
do_github_release() {
  echo "=== Step 4: GitHub release ==="

  if $DRY_RUN; then
    echo "  [DRY-RUN] Would create GitHub release: ${TAG}"
    echo "  [DRY-RUN] Would upload artifacts from ${ACTUAL_DIST}"
    return 0
  fi

  # Generate release notes
  local notes_content
  notes_content=$(generate_notes)

  # Write notes to a temp file for gh CLI
  local tmp_notes
  tmp_notes=$(mktemp)
  echo "$notes_content" > "$tmp_notes"

  # Build gh release create command
  local gh_cmd=(
    gh release create
    "$TAG"
    --repo "$(git -C "$REPO_ROOT" remote get-url origin)"
    --title "ContextSmith v${VERSION}"
    --notes-file "$tmp_notes"
  )

  if $PRERELEASE; then
    gh_cmd+=(--prerelease)
  fi

  if $DRAFT; then
    gh_cmd+=(--draft)
  fi

  # Add artifacts
  local artifacts=()
  for artifact in "$ACTUAL_DIST"/*.zip "$ACTUAL_DIST"/*.sha256 "$ACTUAL_DIST"/RELEASE_SUMMARY.json; do
    if [[ -f "$artifact" ]]; then
      artifacts+=("$artifact")
    fi
  done

  if [[ ${#artifacts[@]} -eq 0 ]]; then
    echo "ERROR: No artifacts to upload"
    rm -f "$tmp_notes"
    return 1
  fi

  gh_cmd+=("${artifacts[@]}")

  echo "  Creating release with ${#artifacts[@]} artifact(s)..."
  "${gh_cmd[@]}"

  rm -f "$tmp_notes"
  echo ""
}

# Main execution
if ! check_prerequisites; then
  echo ""
  echo "Prerequisites check failed. Fix the above errors and retry."
  exit 1
fi

if ! $SKIP_BUILD; then
  do_build
fi

if ! verify_artifacts; then
  echo "Artifact verification failed. Fix the above errors and retry."
  exit 1
fi

if ! $SKIP_PUSH; then
  do_git_tag
  do_github_release
else
  echo "=== Skipping git push and GitHub release (--skip-push) ==="
  echo ""
  echo "To publish manually:"
  echo "  git tag -a ${TAG} -m 'ContextSmith v${VERSION}'"
  echo "  git push origin ${TAG}"
  echo "  gh release create ${TAG} --repo \$(git remote get-url origin) \\"
  echo "    --title 'ContextSmith v${VERSION}' \\"
  echo "    --notes-file <notes.md> \\"
  echo "    ${ACTUAL_DIST}/*.zip ${ACTUAL_DIST}/*.sha256 ${ACTUAL_DIST}/RELEASE_SUMMARY.json"
fi

echo "Release pipeline complete."
if $DRY_RUN; then
  echo "Mode: DRY RUN — no changes were made."
fi
