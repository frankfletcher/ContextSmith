#!/usr/bin/env bash
set -euo pipefail

# Compute repo root (location-independent)
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || dirname "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)")

SKILL_NAME="${1:-}"
OUTPUT_DIR="${2:-$REPO_ROOT/dist}"

if [ -z "$SKILL_NAME" ]; then
    echo "Usage: $0 <skill-name> [output-dir]"
    echo "Example: $0 local-model-prompt-engineer"
    exit 1
fi

# Security: Validate SKILL_NAME to prevent directory traversal
if [[ "$SKILL_NAME" == *".."* ]] || [[ "$SKILL_NAME" == /* ]]; then
    echo "ERROR: Invalid skill name (directory traversal detected)"
    exit 1
fi

SKILL_DIR="$REPO_ROOT/skills/$SKILL_NAME"
STAGING_DIR="$REPO_ROOT/.agent_work/staged_skills/$SKILL_NAME"

if [ ! -d "$SKILL_DIR" ]; then
    echo "ERROR: skill directory not found: $SKILL_DIR"
    exit 1
fi

if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "ERROR: SKILL.md not found in $SKILL_DIR"
    exit 1
fi

# Extract Version from Manifest
MANIFEST="$SKILL_DIR/reference_manifest.yml"
if [ -f "$MANIFEST" ]; then
    VERSION=$(python -c "
import yaml
with open(\"$MANIFEST\") as f:
    print(yaml.safe_load(f).get('version', '0.0.0'))
")
else
    VERSION="0.0.0"
fi

# Sync references to staging directory (does not touch repo working tree)
echo "Syncing references for $SKILL_NAME..."
python "$REPO_ROOT/scripts/sync_shared_refs.py" --skill "$SKILL_NAME" --verbose
if [ $? -ne 0 ]; then
    echo "ERROR: sync failed, aborting package"
    exit 1
fi

# Verify staging directory has the expected files
if [ ! -f "$STAGING_DIR/SKILL.md" ]; then
    echo "ERROR: staging missing SKILL.md at $STAGING_DIR"
    exit 1
fi

# Create Output Directory and Zip
mkdir -p "$OUTPUT_DIR"
ZIP_NAME="$OUTPUT_DIR/${SKILL_NAME}-${VERSION}.zip"

if [ -f "$ZIP_NAME" ]; then
    echo "WARN: overwriting existing $ZIP_NAME"
fi

# Check for zip command
if ! command -v zip &> /dev/null; then
    echo "ERROR: zip command not found. Install zip to use this script."
    exit 1
fi

# Zip from staging directory, excluding manifest and .gitkeep
cd "$REPO_ROOT/.agent_work/staged_skills"
zip -r "$ZIP_NAME" "$SKILL_NAME/" \
    -x "$SKILL_NAME/reference_manifest.yml" \
    -x "$SKILL_NAME/references/.gitkeep"

FILE_COUNT=$(unzip -l "$ZIP_NAME" | tail -1 | awk '{print $2}')
echo "Packaged $ZIP_NAME ($FILE_COUNT files)"
