#!/usr/bin/env bash
set -euo pipefail

# install_skill.sh — Install a ContextSmith skill package to a target directory.
#
# Usage: install_skill.sh <zip-file> [target-dir]
# Example: install_skill.sh dist/local-model-prompt-engineer-1.0.0.zip
#
# The script extracts the zip, verifies MANIFEST.json checksums, compares
# versions, backs up any existing installation, and copies to target.

ZIP_FILE="${1:-}"
TARGET_DIR="${2:-$HOME/.agents/skills}"

if [ -z "$ZIP_FILE" ]; then
    echo "Usage: $0 <zip-file> [target-dir]"
    echo "Example: $0 dist/local-model-prompt-engineer-1.0.0.zip"
    exit 1
fi

if [ ! -f "$ZIP_FILE" ]; then
    echo "ERROR: zip file not found: $ZIP_FILE"
    exit 1
fi

# Resolve to absolute path
ZIP_FILE=$(realpath "$ZIP_FILE")

# Check for required commands
for cmd in unzip python sha256sum; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "ERROR: '$cmd' is required but not found on PATH"
        exit 1
    fi
done

# Create a temp directory for extraction
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "Extracting $ZIP_FILE..."
unzip -q "$ZIP_FILE" -d "$TEMP_DIR"

# Find the skill directory (top-level directory in the zip)
SKILL_DIR=$(python -c "
import os
entries = os.listdir('$TEMP_DIR')
dirs = [e for e in entries if os.path.isdir(os.path.join('$TEMP_DIR', e))]
print(dirs[0] if dirs else '')
")

if [ -z "$SKILL_DIR" ]; then
    echo "ERROR: could not determine skill directory from zip"
    exit 1
fi

EXTRACTED_SKILL="$TEMP_DIR/$SKILL_DIR"

# Read MANIFEST.json
if [ ! -f "$EXTRACTED_SKILL/MANIFEST.json" ]; then
    echo "ERROR: MANIFEST.json not found in package"
    exit 1
fi

SKILL_NAME=$(python -c "import json; print(json.load(open('$EXTRACTED_SKILL/MANIFEST.json'))['skill_name'])")
PACKAGE_VERSION=$(python -c "import json; print(json.load(open('$EXTRACTED_SKILL/MANIFEST.json'))['version'])")

echo "Skill: $SKILL_NAME (v$PACKAGE_VERSION)"

# Verify MANIFEST.json checksums
echo "Verifying file checksums..."
python -c "
import json, hashlib, os, sys

manifest_path = '$EXTRACTED_SKILL/MANIFEST.json'
with open(manifest_path) as f:
    manifest = json.load(f)

errors = 0
verified = 0
for entry in manifest.get('files', []):
    filepath = os.path.join('$EXTRACTED_SKILL', entry['path'])
    if not os.path.isfile(filepath):
        print(f'  MISSING: {entry[\"path\"]}')
        errors += 1
        continue
    with open(filepath, 'rb') as f:
        actual = hashlib.sha256(f.read()).hexdigest()
    expected = entry['sha256']
    if actual != expected:
        print(f'  MISMATCH: {entry[\"path\"]} (expected {expected[:12]}..., got {actual[:12]}...)')
        errors += 1
    else:
        verified += 1

print(f'Verified {verified} files')
if errors > 0:
    print(f'ERRORS: {errors} file(s) failed verification')
    sys.exit(1)
" || { echo "ERROR: checksum verification failed"; exit 1; }

# Determine target skill directory
INSTALL_DIR="$TARGET_DIR/$SKILL_NAME"

# Check if skill is already installed
if [ -d "$INSTALL_DIR" ]; then
    # Read installed version from MANIFEST.json if present
    INSTALLED_VERSION=""
    if [ -f "$INSTALL_DIR/MANIFEST.json" ]; then
        INSTALLED_VERSION=$(python -c "import json; print(json.load(open('$INSTALL_DIR/MANIFEST.json')).get('version', ''))")
    fi

    if [ "$INSTALLED_VERSION" = "$PACKAGE_VERSION" ]; then
        echo "SKIP: $SKILL_NAME v$PACKAGE_VERSION is already installed at $INSTALL_DIR"
        exit 0
    fi

    echo "Existing version: v${INSTALLED_VERSION:-unknown}, new version: v$PACKAGE_VERSION"

    # Backup existing installation
    BACKUP_DIR="${INSTALL_DIR}.backup.$(date +%Y%m%d%H%M%S)"
    echo "Backing up existing installation to $BACKUP_DIR..."
    mv "$INSTALL_DIR" "$BACKUP_DIR"
fi

# Install
mkdir -p "$TARGET_DIR"
cp -r "$EXTRACTED_SKILL" "$INSTALL_DIR"

echo "Installed $SKILL_NAME v$PACKAGE_VERSION to $INSTALL_DIR"
if [ -n "${BACKUP_DIR:-}" ]; then
    echo "Backup: $BACKUP_DIR"
fi
