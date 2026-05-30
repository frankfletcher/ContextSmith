#!/usr/bin/env bash
set -euo pipefail

# install_all.sh — Install all ContextSmith skill packages from a dist directory.
#
# Usage: install_all.sh <dist-dir> [target-dir]
# Example: install_all.sh dist
#
# Finds all .zip files in dist-dir, calls install_skill.sh for each,
# and prints a summary report.

DIST_DIR="${1:-}"
TARGET_DIR="${2:-$HOME/.agents/skills}"

if [ -z "$DIST_DIR" ]; then
    echo "Usage: $0 <dist-dir> [target-dir]"
    echo "Example: $0 dist"
    exit 1
fi

if [ ! -d "$DIST_DIR" ]; then
    echo "ERROR: dist directory not found: $DIST_DIR"
    exit 1
fi

# Resolve paths
DIST_DIR=$(realpath "$DIST_DIR")
SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
INSTALL_SCRIPT="$SCRIPT_DIR/install_skill.sh"

if [ ! -f "$INSTALL_SCRIPT" ]; then
    echo "ERROR: install_skill.sh not found at $INSTALL_SCRIPT"
    exit 1
fi

# Find all zip files (excluding .sha256 files)
ZIPS=()
while IFS= read -r -d '' zip; do
    ZIPS+=("$zip")
done < <(find "$DIST_DIR" -maxdepth 1 -name '*.zip' -print0 | sort -z)

if [ ${#ZIPS[@]} -eq 0 ]; then
    echo "ERROR: no .zip files found in $DIST_DIR"
    exit 1
fi

echo "Found ${#ZIPS[@]} package(s) in $DIST_DIR"
echo "Target: $TARGET_DIR"
echo "---"

TOTAL=${#ZIPS[@]}
SUCCESS=0
SKIPPED=0
FAILED=0

for zip in "${ZIPS[@]}"; do
    echo ""
    echo "==> Installing $(basename "$zip")..."
    if bash "$INSTALL_SCRIPT" "$zip" "$TARGET_DIR"; then
        # Check if it was skipped (exit 0 with SKIP message)
        SUCCESS=$((SUCCESS + 1))
    else
        FAILED=$((FAILED + 1))
        echo "FAILED: $(basename "$zip")"
    fi
done

echo ""
echo "==============================="
echo "Installation Summary"
echo "==============================="
echo "Total:   $TOTAL"
echo "Success: $SUCCESS"
echo "Failed:  $FAILED"
echo "==============================="

if [ "$FAILED" -gt 0 ]; then
    exit 1
fi
