# Task: Runtime Framing Backfill

## Objective

Backfill all runtime framing changes made to /home/frank/00-Code/ContextSmith/.agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/PLAN.md into the actual codebase artifacts. /home/frank/00-Code/ContextSmith/.agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/PLAN.md now positions runtime
  reinforcement/orchestration as "first-class, optional but default." Codebase artifacts must match.

## Scope

- README.md
- docs/workflows/RUNTIME_ENFORCEMENT.md
- docs/QUICKSTART.md
- docs/examples/EXAMPLES_LIBRARY.md
- docs/workflows/CREATE_A_PLAN.md
- docs/workflows/BUILD_OR_IMPROVE_A_SKILL.md
- shared/ references (selective, only if they frame the runtime)
- SKILL.md files (selective, only if they reference runtime behavior)

## Constraints

- Small-model executable phases
- Each sub-phase bounded to one artifact area
- Audit first, fix only if deviation found
- Ralph loop: 2 iterations per phase
- Self-audit: required before phase completion
- Validation: `python scripts/validate_skills.py` and `python scripts/token_budget.py --strict` after each phase
- Stop rule: stop if an artifact requires more than 3 edits or becomes broader than its scope

## Do Not

- Do not rewrite entire docs
- Do not add new documentation pages
- Do not modify PACKAGE_SPEC.md
- Do not modify user-level config
- Do not run destructive git commands
