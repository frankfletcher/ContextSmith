# Context: Runtime Framing Backfill

## Artifact Manifest

- artifact_type: context
- parent_task: TASK.md
- context_scope: files, constraints, known facts, and skip rules for backfill work

## Known Facts

- /home/frank/00-Code/ContextSmith/.agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/PLAN.md (2026-06-01-runtime-enforcement) has been updated to frame runtime reinforcement/orchestration as "first-class, optional but default."
- Key framing changes in /home/frank/00-Code/ContextSmith/.agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/PLAN.md: Architecture Direction, Enforcement Levels, Phase 4B, 5D, 6A, 6B, 8A, 8B, 8B1-8B4, Phase 9, Plan Completion Criteria.
- Codebase artifacts (README, docs, shared refs, SKILL.md files) may still have old framing language.
- Backfill task is to align codebase artifacts with /home/frank/00-Code/ContextSmith/.agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/PLAN.md framing.

## Files to Inspect
| Path | Purpose |
| --- | --- |
| PLAN.md (2026-06-01-runtime-enforcement) | Canonical framing reference |
| README.md | Top-level runtime framing |
| docs/workflows/RUNTIME_ENFORCEMENT.md | Runtime user guide |
| docs/QUICKSTART.md | Quickstart runtime mentions |
| docs/examples/EXAMPLES_LIBRARY.md | Examples runtime framing |
| docs/workflows/CREATE_A_PLAN.md | Workflow runtime mentions |
| docs/workflows/BUILD_OR_IMPROVE_A_SKILL.md | Workflow runtime mentions |
| shared/ | Agent-facing runtime references |
| skills/*/SKILL.md | Skill-level runtime framing |

## Constraints

- Small-model executable phases
- Each sub-phase bounded to one artifact area
- Audit first, fix only if deviation found
- Ralph loop: 2 iterations per phase
- Self-audit: required before phase completion
- Validation: `python scripts/validate_skills.py` and `python scripts/token_budget.py --strict` after each phase
- Stop rule: stop if an artifact requires more than 3 edits or becomes broader than its scope

## Validation Commands

- `python scripts/validate_skills.py` after skill or shared-reference changes.
- `python scripts/token_budget.py --strict` after skill or shared-reference changes.
