#!/usr/bin/env python3
from pathlib import Path
import sys, yaml
root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('skills')
failed = False
for skill in sorted(root.iterdir()):
    if not skill.is_dir():
        continue
    p = skill / 'SKILL.md'
    if not p.exists():
        continue
    text = p.read_text(encoding='utf-8')
    if not text.startswith('---'):
        print(f'FAIL {skill.name}: missing YAML frontmatter')
        failed = True
        continue
    parts = text.split('---', 2)
    data = yaml.safe_load(parts[1])
    for key in ['name', 'description']:
        if key not in data:
            print(f'FAIL {skill.name}: missing {key}')
            failed = True
    lines = len(text.splitlines())
    print(f'OK {skill.name}: {lines} lines, version={data.get("metadata",{}).get("version") if isinstance(data.get("metadata"), dict) else "none"}')
sys.exit(1 if failed else 0)
