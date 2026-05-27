# TASK.md — ContextSmith Reference Deduplication Artifacts

## Objective
Eliminate 260+ duplicated reference file copies across 5 skills by replacing them with a manifest-driven sync system that:
1. Defines dependencies explicitly (`reference_manifest.yml` per skill)
2. Populates gitignored `references/` directories from `shared/` via a sync script
3. Provides a packaging script for standalone skill distribution
4. Adds CI validation to prevent drift

## Scope
- 5 skill directories, each with a `reference_manifest.yml`
- 1 sync script (`scripts/sync_shared_refs.py`)
- 1 package script (`scripts/package_skill.sh`)
- Enhanced `scripts/validate_skills.py`
- `.github/workflows/validate.yml`
- Updated `.gitignore`
- New `CONTRIBUTING.md`
- 52 shared source files (unchanged)
- Skill-local `help.md` files (moved to skill roots)

## Constraints
- Python 3.9+ stdlib + PyYAML only
- No new dependencies
- Shared files are NOT modified (they are the canonical source)
- SKILL.md files are NOT modified
- `skills/*/references/` becomes gitignored (generated)
- Must preserve subdirectory structure (`model-profiles/`, `domain-profiles/`)
- All 5 skills must produce byte-identical references after sync
