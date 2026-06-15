#!/usr/bin/env python3
"""Validate version consistency across all version sources.

Reads canonical version from pyproject.toml, then checks:
- PACKAGE_SPEC.md header matches
- All skill SKILL.md metadata.version matches

Usage:
    python scripts/validate_version_consistency.py

Exit codes:
    0 — all versions match
    1 — violations found
"""

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read_pyproject_version() -> str:
    """Extract version from pyproject.toml."""
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r'^version\s*=\s*"([^"]+)"', text, re.M)
    if not m:
        print("Error: version not found in pyproject.toml")
        sys.exit(1)
    return m.group(1)


def _read_package_spec_version() -> str | None:
    """Extract version from PACKAGE_SPEC.md."""
    path = REPO_ROOT / "PACKAGE_SPEC.md"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    m = re.search(r'v?(\d+\.\d+\.\d+)', text)
    return m.group(1) if m else None


def _read_skill_version(skill_dir: Path) -> str | None:
    """Extract metadata.version from skill SKILL.md."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return None
    text = skill_md.read_text(encoding="utf-8")
    m = re.search(r'version:\s*"(\d+\.\d+\.\d+)"', text)
    return m.group(1) if m else None


def main() -> int:
    canonical = _read_pyproject_version()
    errors = []

    # Check PACKAGE_SPEC.md
    pkg_version = _read_package_spec_version()
    if pkg_version is not None and pkg_version != canonical:
        errors.append(f"PACKAGE_SPEC.md: v{pkg_version} != pyproject.toml v{canonical}")

    # Check all skills
    skills_dir = REPO_ROOT / "skills"
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_ver = _read_skill_version(skill_dir)
        if skill_ver is None:
            continue
        if skill_ver != canonical:
            errors.append(f"skills/{skill_dir.name}/SKILL.md: v{skill_ver} != pyproject.toml v{canonical}")

    if errors:
        print(f"Version consistency: {len(errors)} violation(s)")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"Version consistency: OK (all match v{canonical})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
