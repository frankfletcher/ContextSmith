#!/usr/bin/env bash
set -euo pipefail

# test_release.sh — End-to-end integration test for the release pipeline.
#
# Creates a clean temp directory, runs the full pipeline, verifies all artifacts,
# tests installation, and cleans up. Safe to run multiple times.
#
# Usage: bash scripts/test_release.sh

SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
REPO_ROOT=$(dirname "$SCRIPT_DIR")

PASS=0
FAIL=0
TOTAL=0

pass() {
    PASS=$((PASS + 1))
    TOTAL=$((TOTAL + 1))
    echo "  PASS: $1"
}

fail() {
    FAIL=$((FAIL + 1))
    TOTAL=$((TOTAL + 1))
    echo "  FAIL: $1"
}

# Create temp directory for all test artifacts
TEST_ROOT=$(mktemp -d)
trap 'rm -rf "$TEST_ROOT"' EXIT

DIST_DIR="$TEST_ROOT/dist"
INSTALL_DIR="$TEST_ROOT/install"
BUNDLE_EXTRACT="$TEST_ROOT/bundle-extract"

echo "============================================="
echo "ContextSmith Release Integration Test"
echo "============================================="
echo "Test root: $TEST_ROOT"
echo "Dist dir:  $DIST_DIR"
echo "Install:   $INSTALL_DIR"
echo ""

# Check prerequisites
echo "--- Prerequisites ---"
for cmd in python zip unzip sha256sum; do
    if command -v "$cmd" &> /dev/null; then
        pass "$cmd available"
    else
        fail "$cmd not found on PATH"
    fi
done

# Check PyYAML
if python -c "import yaml" 2>/dev/null; then
    pass "PyYAML available"
else
    fail "PyYAML not installed (pip install pyyaml)"
fi
echo ""

# Step 1: Full pipeline run
echo "=== Step 1: Full Pipeline Run ==="
if python "$REPO_ROOT/scripts/build_release.py" --package --bundle --dist-dir "$DIST_DIR" > "$TEST_ROOT/pipeline.log" 2>&1; then
    pass "Pipeline completed successfully"
else
    fail "Pipeline failed (see $TEST_ROOT/pipeline.log)"
    echo ""
    echo "Pipeline log:"
    cat "$TEST_ROOT/pipeline.log"
    echo ""
    echo "============================================="
    echo "INTEGRATION TEST FAILED"
    echo "============================================="
    exit 1
fi
echo ""

# Step 2: Verify zip artifacts
echo "=== Step 2: Verify Zip Artifacts ==="
EXPECTED_SKILLS=(
    "local-model-prompt-engineer"
    "local-model-skill-engineer"
    "local-model-instruction-engineer"
    "local-model-agent-evaluator"
    "local-model-skill-migrator"
)

for skill in "${EXPECTED_SKILLS[@]}"; do
    # Find the zip for this skill
    ZIP_FILE=$(find "$DIST_DIR" -maxdepth 1 -name "${skill}-*.zip" 2>/dev/null | head -1)
    if [ -n "$ZIP_FILE" ] && [ -f "$ZIP_FILE" ]; then
        pass "Zip exists: $(basename "$ZIP_FILE")"
    else
        fail "Zip missing for $skill"
    fi

    # Find the corresponding .sha256 file
    SHA_FILE=$(find "$DIST_DIR" -maxdepth 1 -name "${skill}-*.sha256" 2>/dev/null | head -1)
    if [ -n "$SHA_FILE" ] && [ -f "$SHA_FILE" ]; then
        pass "SHA256 exists: $(basename "$SHA_FILE")"
    else
        fail "SHA256 missing for $skill"
    fi
done

# Check bundle
if [ -f "$DIST_DIR/contextsmith-all-bundle.zip" ]; then
    pass "Bundle zip exists"
else
    fail "Bundle zip missing"
fi

if [ -f "$DIST_DIR/contextsmith-all-bundle.zip.sha256" ]; then
    pass "Bundle SHA256 exists"
else
    fail "Bundle SHA256 missing"
fi

# Check RELEASE_SUMMARY.json
if [ -f "$DIST_DIR/RELEASE_SUMMARY.json" ]; then
    pass "RELEASE_SUMMARY.json exists"
else
    fail "RELEASE_SUMMARY.json missing"
fi
echo ""

# Step 3: Verify SHA256 checksums
echo "=== Step 3: Verify SHA256 Checksums ==="
cd "$DIST_DIR"
for sha_file in *.sha256; do
    if [ -f "$sha_file" ]; then
        if sha256sum -c "$sha_file" &> /dev/null; then
            pass "Checksum valid: $sha_file"
        else
            fail "Checksum invalid: $sha_file"
        fi
    fi
done
cd "$REPO_ROOT"
echo ""

# Step 4: Verify zip contents
echo "=== Step 4: Verify Zip Contents ==="
for skill in "${EXPECTED_SKILLS[@]}"; do
    ZIP_FILE=$(find "$DIST_DIR" -maxdepth 1 -name "${skill}-*.zip" 2>/dev/null | head -1)
    if [ -z "$ZIP_FILE" ]; then
        fail "Cannot verify contents: $skill zip not found"
        continue
    fi

    # List zip contents once, reuse for all checks
    ZIP_LIST=$(unzip -l "$ZIP_FILE" 2>/dev/null) || true

    # Check SKILL.md is in the zip
    if echo "$ZIP_LIST" | grep -q "SKILL.md"; then
        pass "$skill: SKILL.md in zip"
    else
        fail "$skill: SKILL.md missing from zip"
    fi

    # Check references/ directory exists in zip
    if echo "$ZIP_LIST" | grep -q "references/"; then
        pass "$skill: references/ in zip"
    else
        fail "$skill: references/ missing from zip"
    fi

    # Check MANIFEST.json is in the zip
    if echo "$ZIP_LIST" | grep -q "MANIFEST.json"; then
        pass "$skill: MANIFEST.json in zip"
    else
        fail "$skill: MANIFEST.json missing from zip"
    fi

    # Check reference_manifest.yml is NOT in the zip
    if echo "$ZIP_LIST" | grep -q "reference_manifest.yml"; then
        fail "$skill: reference_manifest.yml should not be in zip"
    else
        pass "$skill: reference_manifest.yml correctly excluded"
    fi
done
echo ""

# Step 5: Verify bundle contents
echo "=== Step 5: Verify Bundle Contents ==="
if [ -f "$DIST_DIR/contextsmith-all-bundle.zip" ]; then
    BUNDLE_LIST=$(unzip -l "$DIST_DIR/contextsmith-all-bundle.zip" 2>/dev/null) || true
    for skill in "${EXPECTED_SKILLS[@]}"; do
        if echo "$BUNDLE_LIST" | grep -q "$skill/"; then
            pass "Bundle contains $skill/"
        else
            fail "Bundle missing $skill/"
        fi
    done
else
    fail "Cannot verify bundle: bundle zip not found"
fi
echo ""

# Step 6: Verify RELEASE_SUMMARY.json
echo "=== Step 6: Verify RELEASE_SUMMARY.json ==="
if [ -f "$DIST_DIR/RELEASE_SUMMARY.json" ]; then
    # Check it has the expected number of entries (5 skills + 1 bundle = 6)
    ENTRY_COUNT=$(python -c "
import json
with open('$DIST_DIR/RELEASE_SUMMARY.json') as f:
    data = json.load(f)
print(len(data.get('skills', [])))
")
    if [ "$ENTRY_COUNT" -ge 6 ]; then
        pass "RELEASE_SUMMARY.json has $ENTRY_COUNT entries (expected >= 6)"
    else
        fail "RELEASE_SUMMARY.json has $ENTRY_COUNT entries (expected >= 6)"
    fi

    # Check all entries have required fields
    python -c "
import json, sys
with open('$DIST_DIR/RELEASE_SUMMARY.json') as f:
    data = json.load(f)
errors = 0
for entry in data.get('skills', []):
    for field in ('name', 'version', 'zip_path', 'sha256_path', 'file_count', 'total_size_bytes'):
        if field not in entry:
            print(f'Missing field {field} in entry {entry.get(\"name\", \"unknown\")}')
            errors += 1
if errors > 0:
    sys.exit(1)
" 2>/dev/null && pass "All summary entries have required fields" || fail "Summary entries missing required fields"
else
    fail "Cannot verify summary: file not found"
fi
echo ""

# Step 7: Test installation
echo "=== Step 7: Test Installation ==="
if bash "$REPO_ROOT/scripts/install_all.sh" "$DIST_DIR" "$INSTALL_DIR" > "$TEST_ROOT/install.log" 2>&1; then
    pass "install_all.sh completed successfully"
else
    fail "install_all.sh failed (see $TEST_ROOT/install.log)"
fi

# Verify all skills are installed
for skill in "${EXPECTED_SKILLS[@]}"; do
    if [ -d "$INSTALL_DIR/$skill" ]; then
        pass "Installed: $skill"
    else
        fail "Not installed: $skill"
    fi

    # Check SKILL.md exists in installed directory
    if [ -f "$INSTALL_DIR/$skill/SKILL.md" ]; then
        pass "$skill: SKILL.md present"
    else
        fail "$skill: SKILL.md missing after install"
    fi

    # Check MANIFEST.json exists in installed directory
    if [ -f "$INSTALL_DIR/$skill/MANIFEST.json" ]; then
        pass "$skill: MANIFEST.json present"
    else
        fail "$skill: MANIFEST.json missing after install"
    fi
done
echo ""

# Step 8: Test idempotent re-install (same version should skip)
echo "=== Step 8: Test Idempotent Re-Install ==="
if bash "$REPO_ROOT/scripts/install_all.sh" "$DIST_DIR" "$INSTALL_DIR" > "$TEST_ROOT/reinstall.log" 2>&1; then
    pass "Re-install completed (same version, should skip)"
else
    fail "Re-install failed"
fi
echo ""

# Step 9: Verify MANIFEST.json checksums in installed skills
echo "=== Step 9: Verify Installed Checksums ==="
for skill in "${EXPECTED_SKILLS[@]}"; do
    MANIFEST="$INSTALL_DIR/$skill/MANIFEST.json"
    if [ -f "$MANIFEST" ]; then
        if python -c "
import json, hashlib, os, sys
with open('$MANIFEST') as f:
    manifest = json.load(f)
errors = 0
for entry in manifest.get('files', []):
    filepath = os.path.join('$INSTALL_DIR/$skill', entry['path'])
    if not os.path.isfile(filepath):
        errors += 1
        continue
    with open(filepath, 'rb') as f:
        actual = hashlib.sha256(f.read()).hexdigest()
    if actual != entry['sha256']:
        errors += 1
if errors > 0:
    sys.exit(1)
" 2>/dev/null; then
            pass "$skill: all installed file checksums valid"
        else
            fail "$skill: installed file checksum mismatch"
        fi
    else
        fail "$skill: MANIFEST.json not found for checksum verification"
    fi
done
echo ""

# Final summary
echo "============================================="
echo "Integration Test Results"
echo "============================================="
echo "Total:  $TOTAL"
echo "Passed: $PASS"
echo "Failed: $FAIL"
echo "============================================="

if [ "$FAIL" -gt 0 ]; then
    echo "RESULT: FAILED"
    exit 1
else
    echo "RESULT: ALL TESTS PASSED"
    exit 0
fi
