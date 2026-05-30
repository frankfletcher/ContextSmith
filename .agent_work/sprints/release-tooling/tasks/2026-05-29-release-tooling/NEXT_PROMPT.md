# NEXT_PROMPT.md — Release Tooling Sprint (COMPLETE)

## Artifact Manifest

```yaml
---
artifact_type: executor_prompt
sprint: release-tooling
task: "2026-05-29-release-tooling"
phase: complete
date: "2026-05-29"
parameters:
  --mode: guided,deep
  --target-profile: qwen36
  --context-length: 60k
  --education_level: deep
  --ralph: 2
  --planner-profile: qwen36
  --executor-profile: qwen36
references:
  - shared/phased-planning.md
  - shared/implementation-plan-audit.md
  - shared/git-safety.md
  - shared/loop-safety.md
  - shared/persistent-task-state.md
  - shared/phase-compression.md
  - shared/test-quality-audit.md
---
```

## Sprint Status: COMPLETE

All 7 phases (1, 2, 3, 4, 5, 5.5, 6) are complete.

### Summary of Deliverables
- `scripts/sync_shared_refs.py` — added `--update-manifests` flag (Phase 1, persisted in Phase 5.5)
- `scripts/package_skill.sh` — hardened with validation gate, MANIFEST.json, SHA-256 checksums (Phase 2)
- `scripts/build_release.py` — full release orchestrator with sync → validate → version bump → package → bundle → summary pipeline (Phase 3, Phase 5.5)
- `scripts/install_skill.sh` — single skill installer with checksum verification, version comparison, backup (Phase 4)
- `scripts/install_all.sh` — batch installer for all skills from dist/ (Phase 4)
- `scripts/test_release.sh` — 74 integration tests across 9 steps, validates full pipeline end-to-end (Phase 6)
- `docs/RELEASE_PROCESS.md` — release process documentation (Phase 5)
- `README.md` — updated with installation section (Phase 5)
- `CHANGELOG.md` — updated with sprint entries (Phase 5)

### Integration Test Results
- `bash scripts/test_release.sh` — 74/74 passed, stable across 3 consecutive runs
- Negative test: breaking a skill causes pipeline to fail with clear error
- Restore test: fixing the skill restores passing state

### Bugs Learned
1. `[ -n "${VAR:-}" ] && echo` returns exit code 1 under `set -e` when VAR is empty — use if/then/fi
2. `set -euo pipefail` causes `unzip -l | grep -q` to fail intermittently — capture output to variable first

---

## Behavioral Contracts (embedded for standalone execution)

### Phase Planning & Execution
- Each phase MUST include: goal, inputs, likely files/directories, explicit tasks, testing/validation steps, outputs/artifacts, validation checks, stop condition, handoff notes.
- 12-step closeout: (1) Update STATUS.md, (2) Check off PLAN.md items, (3) Record durable decisions in DECISIONS.md, (4) Record changed files/commands in ARTIFACTS.md, (5) Add compact notes to PHASE_LOG.md, (6) Write carry-forward and do-not-carry-forward notes, (7) Update NEXT_PROMPT.md, (8) Run phase compression and update CONTEXT.md for next phase, (9) Run validation checks — if any fail, set STATUS to "Blocked" and exit, (10) Run implementation plan audit for next phase — if fails, set STATUS to "Blocked" and exit, (11) Include test quality audit for coding work — if fails, set STATUS to "Blocked" and exit, (12) If stop condition met, set STATUS to "Completed" and exit.

### Loop Safety
- Do not execute identical consecutive tool calls.
- If the same command, patch, or edit fails twice, stop and change strategy.
- Maximum 1 retry per exact failing action. Maximum 3 total recovery attempts before requesting human input.
- After an edit, verify the file changed. Do not repeat no-op edits.

### Git Safety
- Destructive git commands require explicit user approval: reset --hard, clean -fd, rebase (all variants), push --force/--force-with-lease, branch deletion, amending/squashing/rewriting commits, discarding uncommitted changes.
- Safe inspection: status, diff, log --oneline.

### Task State Hygiene
- Do not paste full files, logs, transcripts, or model reasoning into state files. Store summaries, paths, commands, evidence anchors, decisions, and validation results.
- Record start time in STATUS.md when marking a phase "In Progress". Record elapsed time when marking "Completed".

---

## Sprint Artifacts Location

```
.agent_work/sprints/release-tooling/tasks/2026-05-29-release-tooling/
├── TASK.md                # Sprint objective, scope, constraints, success criteria
├── PLAN.md                # Phase checklist with artifact manifest (THIS FILE'S SOURCE)
├── STATUS.md              # Current phase tracker — UPDATE THIS during execution
├── DECISIONS.md           # Durable decisions with reasons
├── CONTEXT.md             # File map, constraints, skip rules
├── CHECKLIST.md           # Testable validation items — CHECK OFF as tests pass
├── ARTIFACTS.md           # Changed/generated files and commands run — UPDATE during execution
├── PHASE_LOG.md           # One compact entry per completed phase — UPDATE at closeout
├── EDUCATIONAL_REPORT.md  # Per-phase educational reports — APPEND after each phase
└── NEXT_PROMPT.md         # This file — resume prompt for next session
```

## Fresh Session Load Order
When resuming in a new session, load only: TASK.md, STATUS.md, CHECKLIST.md, DECISIONS.md, CONTEXT.md, NEXT_PROMPT.md. Do not load full chat history or all state files.
