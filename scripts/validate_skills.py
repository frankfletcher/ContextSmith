#!/usr/bin/env python3
from pathlib import Path
import yaml, sys, re
root = Path(__file__).resolve().parents[1]
skills = root / 'skills'
errors = 0
warnings = 0

def validate_manifest(skill_dir, skill_name):
    """Validate reference_manifest.yml. Returns (warnings, errors)."""
    manifest_path = skill_dir / 'reference_manifest.yml'
    if not manifest_path.exists():
        print(f"WARN {skill_name}: no reference_manifest.yml")
        return 1, 0

    try:
        manifest = yaml.safe_load(manifest_path.read_text())
    except yaml.YAMLError as e:
        print(f"ERROR {skill_name}: manifest YAML error: {e}")
        return 0, 1

    if not isinstance(manifest, dict):
        print(f"ERROR {skill_name}: manifest is not a dict")
        return 0, 1

    # Check skill field
    if manifest.get('skill') != skill_name:
        print(f"ERROR {skill_name}: manifest skill field '{manifest.get('skill')}' != dir name '{skill_name}'")
        return 0, 1

    # Check version field
    if not manifest.get('version'):
        print(f"WARN {skill_name}: manifest version missing")

    # Check references list
    refs = manifest.get('references', [])
    if not isinstance(refs, list):
        print(f"ERROR {skill_name}: manifest references is not a list")
        return 0, 1

    warn = 0
    err = 0
    sources_seen = set()

    for i, ref in enumerate(refs):
        if not isinstance(ref, dict):
            print(f"ERROR {skill_name}: reference entry {i} is not a dict")
            err += 1
            continue

        source = ref.get('source', '')
        if not source:
            print(f"ERROR {skill_name}: reference entry {i} missing source")
            err += 1
            continue

        # Check duplicate sources
        if source in sources_seen:
            print(f"ERROR {skill_name}: duplicate source '{source}'")
            err += 1
        sources_seen.add(source)

        # Check shared/ prefix for non-local entries
        is_local = ref.get('local', False)
        if not is_local and not source.startswith('shared/'):
            print(f"ERROR {skill_name}: source '{source}' not in shared/ and not local")
            err += 1

        # Check source file exists
        src_path = root / source
        if not src_path.exists():
            if ref.get('required', True):
                print(f"ERROR {skill_name}: required source not found: {source}")
                err += 1
            else:
                print(f"WARN {skill_name}: optional source not found: {source}")
                warn += 1

        # Check version field present
        if not ref.get('version'):
            print(f"WARN {skill_name}: reference '{source}' missing version")

    return warn, err

for skill in sorted(skills.iterdir()):
    if not skill.is_dir():
        continue
    path = skill / 'SKILL.md'
    if not path.exists():
        print(f'ERROR {skill.name}: missing SKILL.md')
        errors += 1
        continue
    text = path.read_text()
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        print(f'ERROR {skill.name}: missing frontmatter')
        errors += 1
        continue
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except Exception as e:
        print(f'ERROR {skill.name}: bad yaml: {e}')
        errors += 1
        continue
    for key in ['name','description']:
        if key not in fm:
            print(f'ERROR {skill.name}: missing {key}')
            errors += 1
    unknown = set(fm) - {'name','description','metadata'}
    if unknown:
        print(f'WARN {skill.name}: unknown frontmatter keys {sorted(unknown)}')
    meta = fm.get('metadata') or {}
    if 'version' not in meta:
        print(f'WARN {skill.name}: metadata.version missing')
    lines = len(text.splitlines())
    status = 'OK' if lines <= 500 else 'WARN'
    print(f'{status} {skill.name}: {lines} lines, version={meta.get("version")}, refs={(skill/"references").exists()}')

    # New manifest validation
    manifest_warns, manifest_errors = validate_manifest(skill, skill.name)
    warnings += manifest_warns
    errors += manifest_errors

print('Validation complete')
sys.exit(1 if errors else 0)
