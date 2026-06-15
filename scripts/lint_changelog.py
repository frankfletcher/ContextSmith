#!/usr/bin/env python3
"""lint_changelog.py — Validate CHANGELOG.md follows keepachangelog format.

Checks:
- Top-level sections present (Added, Changed, Removed, Deprecated, Fixed, Security, Notes)
- Version headers match semver (vMAJOR.MINOR.PATCH)
- No empty unreleased section
- No duplicate version headers

Usage:
    python scripts/lint_changelog.py
    python scripts/lint_changelog.py --path CHANGELOG.md

Exit codes:
    0 — all checks pass
    1 — violations found
"""

import argparse
import re
import sys
from pathlib import Path


VALID_SECTIONS = {
    "Added", "Changed", "Deprecated", "Removed", "Fixed", "Security", "Notes",
    "Breaking",
}


def lint_changelog(filepath: str) -> int:
    """Validate CHANGELOG.md format. Returns 0 on pass, 1 on violations."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: {filepath} not found")
        return 1

    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    errors = []

    # Check first line is # Changelog
    if not lines or not lines[0].strip().startswith("# Changelog"):
        errors.append("File must start with '# Changelog'")

    version_headers = []
    section_stack = []
    current_version = None
    version_line_numbers = {}

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Match version headers: ## vMAJOR.MINOR.PATCH
        if stripped.startswith("## ") and not stripped.startswith("### "):
            version_match = re.match(r"^## v(\d+\.\d+\.\d+)", stripped)
            if version_match:
                ver = version_match.group(1)
                version_headers.append(ver)
                current_version = ver
                section_stack = []

                if ver in version_line_numbers:
                    errors.append(f"Duplicate version header 'v{ver}' at line {i} (first at line {version_line_numbers[ver]})")
                version_line_numbers[ver] = i
            else:
                errors.append(f"Line {i}: version header does not match semver: '{stripped}'")

        # Match section headers: ### SectionName
        elif stripped.startswith("### "):
            section_name = stripped[4:].strip()
            if section_name in VALID_SECTIONS:
                section_stack.append(section_name)
            elif section_name:
                errors.append(f"Line {i}: unknown section '{section_name}' (valid: {', '.join(sorted(VALID_SECTIONS))})")

    # Check for empty unreleased section
    if "Unreleased" in str(lines):
        unreleased_idx = None
        unreleased_end = None
        for i, line in enumerate(lines):
            if "Unreleased" in line and line.strip().startswith("## "):
                unreleased_idx = i
            if unreleased_idx is not None and i > unreleased_idx and line.strip().startswith("## "):
                unreleased_end = i
                break
        if unreleased_idx is not None and unreleased_end is not None:
            body_lines = lines[unreleased_idx + 1:unreleased_end]
            body_text = "".join(body_lines).strip()
            if not body_text:
                errors.append("Unreleased section is empty")

    if errors:
        print(f"CHANGELOG lint: {len(errors)} violation(s)")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("CHANGELOG lint: OK")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Validate CHANGELOG.md follows keepachangelog format"
    )
    parser.add_argument(
        "--path",
        default="CHANGELOG.md",
        help="Path to CHANGELOG.md (default: CHANGELOG.md)",
    )
    args = parser.parse_args()
    sys.exit(lint_changelog(args.path))


if __name__ == "__main__":
    main()
