## Phase 6 — What You Need to Know

### What Changed
- Created `scripts/package_skill.sh` to produce self-contained zip of a skill.
- Modified `scripts/package_skill.sh` to fix directory traversal and CWD dependency (3 MUST FIX issues).
- Modified `scripts/package_skill.sh` to fix Python quoting bug (1 additional MUST FIX).

### Design Decisions
- Used `git rev-parse --show-toplevel` to compute repo root for location independence.
- Used `set -euo pipefail` for strict error handling.
- Excluded `reference_manifest.yml` and `references/.gitkeep` from zip (development artifacts).
- Used absolute paths for output directory to avoid CWD dependency.

### Trade-Offs
- Script requires `zip` command to be installed (external dependency).
- Script assumes `reference_manifest.yml` exists to extract version; defaults to 0.0.0 if missing.

### Key Lessons
- Bash variable expansion inside Python one-liners requires careful quoting: use `\"$VAR\"` inside double-quoted strings passed to `python -c`.
- Location independence can be achieved by computing the repo root once and using absolute paths.

### Edge Cases Not Handled
- `zip` command not installed (handled with error message).
- Invalid `SKILL_NAME` (handled with validation).
- Missing `reference_manifest.yml` (handled with default version).

### Next Phase Preview
Phase 7 will enhance `scripts/validate_skills.py` and create a GitHub Actions CI workflow to run validation on every push/PR.
