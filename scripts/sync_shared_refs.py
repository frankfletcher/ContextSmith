#!/usr/bin/env python3
"""sync_shared_refs.py — Populate skill references/ from shared/ via manifests."""

import argparse
import os
import shutil
import sys
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]

def compute_blob_hash(filepath):
    """Compute git-compatible blob hash."""
    import hashlib
    content = filepath.read_bytes()
    header = f'blob {len(content)}\0'.encode()
    return hashlib.sha1(header + content).hexdigest()

def sync_skill(skill_dir, args):
    manifest_path = skill_dir / 'reference_manifest.yml'
    if not manifest_path.exists():
        if args.verbose:
            print(f"SKIP {skill_dir.name}: no reference_manifest.yml")
        return {'copied': 0, 'skipped': 0, 'warnings': 1, 'errors': 0}

    try:
        manifest = yaml.safe_load(manifest_path.read_text())
    except yaml.YAMLError as e:
        print(f"ERROR {skill_dir.name}: invalid YAML in manifest: {e}")
        return {'copied': 0, 'skipped': 0, 'warnings': 0, 'errors': 1}

    stats = {'copied': 0, 'skipped': 0, 'warnings': 0, 'errors': 0}
    refs_dir = skill_dir / 'references'

    for entry in manifest.get('references', []):
        source = entry.get('source', '')
        required = entry.get('required', True)
        is_local = entry.get('local', False)

        if not required:
            continue

        src_path = REPO_ROOT / source
        if not is_local and not source.startswith('shared/'):
            print(f"ERROR {skill_dir.name}: source '{source}' not in shared/")
            stats['errors'] += 1
            continue

        if not src_path.exists():
            if required:
                print(f"ERROR {skill_dir.name}: required source not found: {source}")
                stats['errors'] += 1
            else:
                print(f"WARN {skill_dir.name}: optional source not found: {source}")
                stats['warnings'] += 1
            continue

        # Compute source hash and check manifest version freshness
        src_hash = compute_blob_hash(src_path)
        manifest_version = entry.get('version', '')
        if manifest_version and manifest_version != src_hash:
            print(f"WARN {skill_dir.name}: manifest version stale for {source} "
                  f"(stored={manifest_version[:8]}..., current={src_hash[:8]}...)")

        # Determine relative path under references/
        if is_local:
            dest_rel = src_path.name
        else:
            dest_rel = Path(source).relative_to('shared')
        dest_path = refs_dir / dest_rel

        if args.dry_run:
            print(f"WOULD COPY: {source} -> {dest_path}")
            stats['copied'] += 1
            continue

        # Check if destination exists and content matches source
        if not args.force and dest_path.exists():
            dest_hash = compute_blob_hash(dest_path)
            if dest_hash == src_hash:
                if args.verbose:
                    print(f"SKIP {source} -> {dest_path} (unchanged)")
                stats['skipped'] += 1
                continue

        # Create parent directories and copy
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dest_path)
        if args.verbose:
            print(f"COPY {source} -> {dest_path}")
        stats['copied'] += 1

    return stats

def main():
    parser = argparse.ArgumentParser(description="Sync shared references to skill directories")
    parser.add_argument("--skill", help="Sync only one skill (directory name)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be copied")
    parser.add_argument("--verbose", action="store_true", help="Print each file operation")
    parser.add_argument("--force", action="store_true", help="Overwrite even if versions match")
    args = parser.parse_args()

    skills_dir = REPO_ROOT / 'skills'
    total = {'copied': 0, 'skipped': 0, 'warnings': 0, 'errors': 0}

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        if args.skill and skill_dir.name != args.skill:
            continue

        stats = sync_skill(skill_dir, args)
        for k in total:
            total[k] += stats[k]

    print(f"Synced: {total['copied']} copied, {total['skipped']} skipped, "
          f"{total['warnings']} warnings, {total['errors']} errors")
    if total['errors'] > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
