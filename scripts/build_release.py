#!/usr/bin/env python3
"""build_release.py — Orchestrate the full release pipeline.

Pipeline: sync → manifest update → validate → (version bump) → package → summary

Usage:
    python scripts/build_release.py --package
    python scripts/build_release.py --package --dry-run
    python scripts/build_release.py --package --version 1.1.0
    python scripts/build_release.py --package --dist-dir /tmp/release
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"
DEFAULT_DIST = REPO_ROOT / "dist"


def discover_skills():
    """Return sorted list of skill directory names."""
    return sorted(
        d.name for d in SKILLS_DIR.iterdir() if d.is_dir() and (d / "SKILL.md").exists()
    )


def run_cmd(cmd, dry_run=False, label=""):
    """Run a subprocess command. Returns (success: bool, stdout: str)."""
    if dry_run:
        print(f"  [DRY-RUN] {label}: {' '.join(str(c) for c in cmd)}")
        return True, ""

    print(f"  {label}: {' '.join(str(c) for c in cmd)}")
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=REPO_ROOT
    )
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, end="" if result.stderr.endswith("\n") else "\n", file=sys.stderr)
    return result.returncode == 0, result.stdout


def step_sync(dry_run=False):
    """Sync shared references in-place."""
    print("\n=== Step A: Sync references ===")
    ok, _ = run_cmd(
        [sys.executable, str(REPO_ROOT / "scripts" / "sync_shared_refs.py"),
         "--all", "--in-place", "--verbose"],
        dry_run=dry_run,
        label="Sync",
    )
    if not ok:
        print("ERROR: sync failed, aborting")
        return False
    return True


def step_manifest_update(dry_run=False):
    """Update manifest hashes."""
    print("\n=== Step B: Update manifests ===")
    ok, _ = run_cmd(
        [sys.executable, str(REPO_ROOT / "scripts" / "sync_shared_refs.py"),
         "--all", "--update-manifests", "--verbose"],
        dry_run=dry_run,
        label="Manifest update",
    )
    if not ok:
        print("ERROR: manifest update failed, aborting")
        return False
    return True


def step_validate(dry_run=False):
    """Run validation, abort on failure."""
    print("\n=== Step C: Validate ===")
    ok, _ = run_cmd(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_skills.py")],
        dry_run=dry_run,
        label="Validate",
    )
    if not ok:
        print("ERROR: validation failed, aborting")
        return False
    print("  Validation passed.")
    return True


def check_git_clean():
    """Check that tracked files have no uncommitted changes. Returns True if clean."""
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    return result.stdout.strip() == ""


def bump_version(skill_name, new_version):
    """Bump version in SKILL.md frontmatter and reference_manifest.yml."""
    skill_dir = SKILLS_DIR / skill_name

    # Update SKILL.md frontmatter metadata.version
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text()

    def replace_version(match):
        fm_block = match.group(1)
        # Try to replace metadata.version
        fm_block = re.sub(
            r"(^|\n)\s*(metadata:\s*\n\s*version:\s*)\S+",
            rf"\g<0>",
            fm_block,
        )
        # More precise: find metadata.version line
        lines = fm_block.split("\n")
        new_lines = []
        in_metadata = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("metadata:"):
                in_metadata = True
                new_lines.append(line)
            elif in_metadata and re.match(r"version:\s*\S+", stripped):
                indent = len(line) - len(line.lstrip())
                new_lines.append(" " * indent + f"version: {new_version}")
                in_metadata = False
            else:
                if not stripped.startswith("metadata.") and not stripped.startswith(" ") and not stripped.startswith("#") and ":" in stripped and not in_metadata:
                    in_metadata = False
                new_lines.append(line)

        # Simpler approach: just do a regex replacement on the whole text
        return "\n".join(new_lines)

    # Simpler and more reliable: regex replace on the full text
    pattern = r"(^---\n.*?^---\n)(?=\n)"
    m = re.match(r"(^---\n)(.*?)(\n---\n)", text, re.S | re.M)
    if m:
        frontmatter_yaml = m.group(2)
        new_fm = re.sub(
            r"(^|\n)(\s*)version:\s*\S+",
            rf"\1\2version: {new_version}",
            frontmatter_yaml,
        )
        text = m.group(1) + new_fm + m.group(3) + text[m.end():]
        skill_md.write_text(text)
        print(f"    Updated SKILL.md metadata.version -> {new_version}")

    # Update reference_manifest.yml version
    manifest_path = skill_dir / "reference_manifest.yml"
    if manifest_path.exists():
        manifest = yaml.safe_load(manifest_path.read_text())
        manifest["version"] = new_version
        manifest_path.write_text(
            yaml.dump(manifest, default_flow_style=False, sort_keys=False)
        )
        print(f"    Updated reference_manifest.yml version -> {new_version}")

    return True


def step_version_bump(new_version, dry_run=False):
    """Bump version across all skills."""
    print(f"\n=== Step D: Version bump to {new_version} ===")

    if not dry_run:
        if not check_git_clean():
            print(
                "ERROR: Working tree is dirty. Commit or stash changes before "
                "bumping versions."
            )
            return False

    skills = discover_skills()
    for skill_name in skills:
        if dry_run:
            print(f"  [DRY-RUN] Would bump {skill_name} to {new_version}")
        else:
            print(f"  Bumping {skill_name}...")
            bump_version(skill_name, new_version)

    return True


def step_package(dist_dir, dry_run=False):
    """Package all skills using package_skill.sh."""
    print("\n=== Step E: Package ===")

    if not dry_run:
        dist_dir.mkdir(parents=True, exist_ok=True)

    skills = discover_skills()
    for skill_name in skills:
        if dry_run:
            print(
                f"  [DRY-RUN] Would package {skill_name} -> {dist_dir}/"
            )
            continue

        # Read version from manifest
        manifest_path = SKILLS_DIR / skill_name / "reference_manifest.yml"
        version = "0.0.0"
        if manifest_path.exists():
            manifest = yaml.safe_load(manifest_path.read_text())
            version = manifest.get("version", "0.0.0")

        ok, _ = run_cmd(
            ["bash", str(REPO_ROOT / "scripts" / "package_skill.sh"),
             skill_name, str(dist_dir)],
            dry_run=False,
            label=f"Package {skill_name}",
        )
        if not ok:
            print(f"ERROR: packaging {skill_name} failed")
            return False

    return True


def generate_summary(dist_dir, dry_run=False):
    """Generate RELEASE_SUMMARY.json and print formatted table."""
    print("\n=== Release Summary ===")

    if dry_run:
        print("  [DRY-RUN] Would generate RELEASE_SUMMARY.json")
        return True

    skills = discover_skills()
    entries = []

    for skill_name in skills:
        manifest_path = SKILLS_DIR / skill_name / "reference_manifest.yml"
        version = "0.0.0"
        if manifest_path.exists():
            manifest = yaml.safe_load(manifest_path.read_text())
            version = manifest.get("version", "0.0.0")

        zip_name = f"{skill_name}-{version}.zip"
        sha_name = f"{skill_name}-{version}.sha256"
        zip_path = dist_dir / zip_name
        sha_path = dist_dir / sha_name

        if not zip_path.exists():
            print(f"  WARN: {zip_name} not found in {dist_dir}")
            continue

        # Count files and total size via zipfile
        file_count = 0
        total_size = 0
        try:
            with zipfile.ZipFile(zip_path) as z:
                file_count = len(z.namelist())
                total_size = sum(info.file_size for info in z.infolist())
        except zipfile.BadZipFile:
            print(f"  WARN: {zip_name} is not a valid zip")
            continue

        entries.append({
            "name": skill_name,
            "version": version,
            "zip_path": zip_name,
            "sha256_path": sha_name,
            "file_count": file_count,
            "total_size_bytes": total_size,
        })

    summary = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "skills": entries,
    }

    summary_path = dist_dir / "RELEASE_SUMMARY.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"  Written: {summary_path}")

    # Print formatted table
    print()
    header = f"  {'Skill':<40} {'Version':<10} {'Files':<8} {'Size':<12}"
    sep = "  " + "-" * 74
    print(header)
    print(sep)
    for entry in entries:
        size_str = (
            f"{entry['total_size_bytes'] / 1024:.1f} KB"
            if entry["total_size_bytes"] < 1024 * 1024
            else f"{entry['total_size_bytes'] / (1024 * 1024):.1f} MB"
        )
        print(
            f"  {entry['name']:<40} {entry['version']:<10} "
            f"{entry['file_count']:<8} {size_str:<12}"
        )
    print(sep)
    print(f"  Total: {len(entries)} skills packaged")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Build release packages for ContextSmith skills.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python scripts/build_release.py --package\n"
            "  python scripts/build_release.py --package --dry-run\n"
            "  python scripts/build_release.py --package --version 1.1.0\n"
            "  python scripts/build_release.py --package --dist-dir /tmp/release\n"
        ),
    )
    parser.add_argument(
        "--version",
        help="Bump all skill versions to this version before packaging",
    )
    parser.add_argument(
        "--package",
        action="store_true",
        help="Run the full release pipeline and create packages",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done without executing",
    )
    parser.add_argument(
        "--dist-dir",
        type=Path,
        default=None,
        help=f"Output directory for packages (default: {DEFAULT_DIST})",
    )

    args = parser.parse_args()
    dist_dir = args.dist_dir or DEFAULT_DIST

    if not args.package:
        parser.print_help()
        sys.exit(0)

    print(f"ContextSmith Release Builder")
    print(f"Repo: {REPO_ROOT}")
    print(f"Dist: {dist_dir}")
    if args.version:
        print(f"Version bump: {args.version}")
    if args.dry_run:
        print("Mode: DRY RUN")
    print()

    # Pipeline execution
    steps = [
        ("Sync", lambda: step_sync(args.dry_run)),
        ("Manifest update", lambda: step_manifest_update(args.dry_run)),
        ("Validate", lambda: step_validate(args.dry_run)),
    ]

    if args.version:
        steps.append(
            ("Version bump", lambda: step_version_bump(args.version, args.dry_run))
        )

    steps.append(("Package", lambda: step_package(dist_dir, args.dry_run)))
    steps.append(("Summary", lambda: generate_summary(dist_dir, args.dry_run)))

    for name, fn in steps:
        try:
            if not fn():
                print(f"\nPipeline aborted at step: {name}")
                sys.exit(1)
        except Exception as e:
            print(f"\nERROR in step {name}: {e}")
            sys.exit(1)

    print("\nRelease pipeline complete.")


if __name__ == "__main__":
    main()
