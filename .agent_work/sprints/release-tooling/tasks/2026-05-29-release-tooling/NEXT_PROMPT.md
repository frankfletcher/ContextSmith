# NEXT_PROMPT.md — Resume Release Tooling Sprint at Phase 5

## Artifact Manifest

```yaml
---
artifact_type: executor_prompt
sprint: release-tooling
task: "2026-05-29-release-tooling"
phase: 5
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

## Instructions for Executor

You are resuming the **Release Tooling Sprint** at **Phase 5**.

### Current State
- Phase 1 completed: `--update-manifests` flag added to `scripts/sync_shared_refs.py`.
- Phase 2 completed: `scripts/package_skill.sh` hardened with validation gate, MANIFEST.json, SHA-256 checksums.
- Phase 3 completed: `scripts/build_release.py` created — full release orchestrator. All 4 tests pass.
- Phase 4 completed: `scripts/install_skill.sh` and `scripts/install_all.sh` created. All 4 tests pass.
- STATUS.md says: "Phase 4 completed."
- All sprint artifacts exist under `.agent_work/sprints/release-tooling/tasks/2026-05-29-release-tooling/`.

### Phase 5 Objective
Document the release process for maintainers and installation for users.

### Context (load before starting)
1. Read `TASK.md` for full sprint objective and success criteria.
2. Read `PLAN.md` for the complete phase checklist (Phase 5 details).
3. Read `CONTEXT.md` for file map, constraints, and skip rules.
4. Read existing `README.md` and `CHANGELOG.md` to understand current content.

### Phase 5 Tasks (from PLAN.md)
1. Create `docs/RELEASE_PROCESS.md` — prerequisites, step-by-step checklist, troubleshooting
2. Update `README.md` — add installation section with copy-paste commands
3. Update `CHANGELOG.md` — add entries for new scripts and improvements

### Phase 5 Tests
- T5.1: Follow RELEASE_PROCESS.md from scratch on clean checkout
- T5.2: README installation commands are copy-paste executable

### Stop Condition
Documentation is complete and actionable.

### After Phase 5 Completes
Run the 12-step phase closeout from behavioral contracts above, then update this file with Phase 6 instructions.

**Educational report:** Append the Phase 5 educational report to `EDUCATIONAL_REPORT.md` using the 5-section template from `shared/educational-report.md`. Do not overwrite existing phase reports.

### Phase 6 Preview (for planning only — do not execute yet)
Phase 6: Integration test script. See PLAN.md for full details.

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
