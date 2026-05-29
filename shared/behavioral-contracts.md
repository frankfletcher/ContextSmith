# Behavioral Contracts Reference

Pre-extracted, self-contained contract summaries from canonical shared references. Each entry is 3-7 lines of actionable requirements. Embed these in generated artifacts' "Behavioral Contracts" section for standalone operation without ContextSmith installed.

---

## Phase Planning & Execution

**Phased Planning - Phase Structure:** Each phase MUST include: goal, inputs, likely files/directories, explicit tasks, testing/validation steps, unit and integration tests where relevant, outputs/artifacts, validation checks, stop condition, handoff notes.

**Phased Planning - Phase Granularity:** Phase count must scale with complexity. Prefer 6-20 phases for large tasks. For `targeted_context_length <= 32k`, prefer more smaller phases. Each phase must fit within the context window.

**Phased Planning - 12-Step Closeout:** (1) Update STATUS.md, (2) Check off PLAN.md items, (3) Record durable decisions in DECISIONS.md, (4) Record changed files/commands in ARTIFACTS.md, (5) Add compact notes to PHASE_LOG.md, (6) Write carry-forward and do-not-carry-forward notes, (7) Update NEXT_PROMPT.md, (8) Run phase compression and update CONTEXT.md for next phase, (9) Run validation checks — if any fail, set STATUS to "Blocked" and exit, (10) Run implementation plan audit for next phase — if fails, set STATUS to "Blocked" and exit, (11) Include test quality audit for coding work — if fails, set STATUS to "Blocked" and exit, (12) If stop condition met, set STATUS to "Completed" and exit.

**Implementation Plan Audit - Gates:** Before executing each phase, grade the next-phase plan on: phase granularity, atomicity, dependency ordering, context fit, validation strength, task-state integration, handoff quality, rollback/recovery, test strategy, small-model readiness. Block on failure (grade below C). Output: recommendation + must-fix items.

**Test Quality Audit - Requirements:** Tests must cover baseline use cases, realistic edge cases, failure modes (invalid input, missing data, bad state), and changed behavior. Assertions must be specific enough to catch wrong behavior. Avoid: tests that only check imports, tests that only check "no throw", mocking the method being tested, asserting on implementation details instead of user-visible behavior.

**Test Quality Audit - Weak Smells:** Tests pass regardless of actual output; no real assertions; over-mocking (mocking the system under test); tests duplicate production logic; brittle selectors or string matching that breaks on formatting changes.

**Phase Code Review - Standard:** Post-phase code review gate. Focused review of changed code only. 1 iteration maximum. Check: correctness, edge cases, error handling, performance implications, adherence to coding standards.

**Phase Code Review - Deep:** 2 iterations with test quality audit. First iteration: structural and correctness review. Second iteration: test coverage and quality verification against test-quality-audit rubric.

---

## Loop Safety & Stability

**Loop Safety - Prevention Rules:** Do not execute identical consecutive tool calls. If the same command, patch, or edit fails twice, stop and change strategy. Recovery menu: correct (fix input), narrow (reduce scope), inspect (gather evidence), substitute (try alternative tool/approach), escalate (request human input).

**Loop Safety - Retry Budget:** Maximum 1 retry per exact failing action. Maximum 2 related attempts per strategy. Maximum 3 total recovery attempts before requesting human input. After an edit, verify the file changed. Do not repeat no-op edits.

**Runtime Stability - Local Models:** Local model runtime issues include: infinite loops despite loop-safety rules, KV cache precision degradation affecting long contexts, speculative decoding causing output artifacts. Treat as experimental guidance unless the harness can directly control these parameters.

---

## Task State & Context Management

**Persistent Task State - 9-File Layout:**
```
.agent_work/sprints/<sprint>/tasks/<YYYY-MM-DD-slug>/
  TASK.md (objective, scope, constraints, success criteria)
  PLAN.md (phase checklist)
  STATUS.md (current phase, completed work, in-progress, next action)
  DECISIONS.md (durable decisions with reason and impact)
  CONTEXT.md (file map, constraints, evidence notes, skip rules)
  CHECKLIST.md (testable validation items)
  ARTIFACTS.md (changed/generated files and commands run)
  PHASE_LOG.md (one compact entry per phase)
  NEXT_PROMPT.md (short resume prompt for session handoff)
```

**Persistent Task State - Hygiene:** Do not paste full files, logs, transcripts, or model reasoning into state files. Store summaries, paths, commands, evidence anchors, decisions, and validation results only.

**Phase Compression - Debrief Format:** Each phase debrief MUST include: Completed (what was done), Evidence (proof of completion), Blockers (unresolved issues), Decisions (durable choices made), Carry Forward (facts for next session), Do Not Carry Forward (explicitly discard to prevent loops), Next Phase (what comes next).

**Phase Compression - Rules:** Summarize, do not paste raw logs or tool output. Do-Not-Carry-Forward entries prevent the same failed approach from repeating in the next phase.

**Small Context Workflows - Fresh Session:** When resuming work, load only 6 files: TASK.md, STATUS.md, CHECKLIST.md, DECISIONS.md, CONTEXT.md, NEXT_PROMPT.md. Do not load full chat history or all state files. Use more phases for tighter context budgets.

**Context Management - Budget Allocation:** Reserve context space for tool results and output generation. Reading order matters: load task definition before evidence, load constraints before exploration. Use evidence anchors (file:line references) for re-anchoring in long sessions.

**Targeted Context Length - Optimization:** Optimize for the stated context budget, not the model's advertised maximum. Affects: verbosity level, phase count (more phases = tighter per-phase budget), example count, report size, and number of files loaded simultaneously.

---

## Instruction Engineering

**Instruction Precedence - 9-Level Hierarchy:** (1) User's current explicit request, (2) Safety boundaries (Git safety, file safety), (3) Project/repo evidence (existing code patterns, package.json, README), (4) Existing repo instructions (AGENTS.md, CLAUDE.md), (5) Target model constraints, (6) Domain-specific requirements, (7) External skill artifacts, (8) Optional style preferences, (9) Generic best practices. Never average conflicts — higher level always wins.

**Instruction Deduplication - Merge Policy:** Scan existing instructions before adding new ones. Preserve clear/specific/correct content. Strengthen vague or incomplete instructions. Consolidate duplicates into single authoritative entries. Add only what is missing. Guard against token bloat: if total instruction length exceeds context budget, trim lowest-priority entries first.

**Git Safety - Approval Gates:** Destructive git commands require explicit user approval: `reset --hard`, `clean -fd`/`clean -fdx`, `rebase` (all variants), `push --force`/`--force-with-lease`, branch deletion, amending/squashing/rewriting commits, discarding uncommitted changes. Safe inspection commands: `status`, `diff`, `log --oneline`.

---

## Skill Engineering

**Skill Interoperability - Verification:** Treat upstream skill outputs as inputs to verify, not authoritative truth. 6-tier classification: confirmed (verified against source), likely (high confidence inference), useful suggestion (worth considering but unverified), unsupported (no evidence), conflicting (contradicts verified source), rejected (actively harmful). Always check for workflow collisions: compatible, overlapping, conflicting, unknown.

**Upstream Artifact Audit - 8-Step Process:** (1) Identify artifacts from upstream skill run, (2) Extract claims and instructions, (3) Verify against current codebase state, (4) Classify each using 6-tier system, (5) Preserve confirmed content unchanged, (6) Downgrade unsupported content to suggestions with "unverified" label, (7) Reject conflicting or hallucinated content, (8) Write required report block: Preserved / Modified / Rejected sections with counts and rationale.

**Engineering Metadata - Schema:** YAML metadata with 8 recommended fields for skills: name, description, version, author, target_model_family, context_length_budget, dependencies (other skills), last_updated. Record targeted context length when provided by user.

---

## Model & Output Constraints

**Small Model Atomicity - Requirements:** Instructions must be atomic for smaller models. Single objective per instruction line. No hidden inference leaps — every step is explicit. Inputs and outputs are stated explicitly. Do not chain multiple operations in a single instruction without intermediate verification steps.

**Ralph Loop - Bounded Improvement:** Maximum 2 improvement iterations (hard maximum 3). A-F evaluation across 10 categories before each iteration: structure, completeness, specificity, small-model readiness, loop safety, context fit, test coverage, edge case handling, error recovery, documentation quality. Store iterations under `.agent_work/.../iterations/`. Stop on bloat or semantic drift (output diverges from original objective).

**Planner-Executor Workflows - Model Selection:** Use stronger model for planning, audits, and design phases. Use smaller model for atomic phase execution when the plan and task state are explicit. Run one phase per session when context is tight (< 32k budget).

**Side Effect Matrix - Risk Tiers:** Tier 1 (read-only): file reads, git inspection commands — no approval needed. Tier 2 (write own files): creating/editing files in `.agent_work/` or new files — proceed without approval. Tier 3 (modify user files): editing existing user code or configuration — require user confirmation for significant changes. Tier 4 (system/network): package installs, network requests, destructive operations — always require explicit approval.

**Output Location - Canonical Paths:** Generated artifacts go under `.agent_work/`. Iterations from Ralph loop go under `.agent_work/sprints/<sprint>/tasks/<YYYY-MM-DD-slug>/iterations/`. Do not scatter outputs across arbitrary directories.
