#!/usr/bin/env python3
from pathlib import Path
import yaml, sys, re
root = Path(__file__).resolve().parents[1]
skills = root / 'skills'
errors = 0
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
print('Validation complete')
sys.exit(1 if errors else 0)
