# Local Model Agent Engineering — Living Design Notes

Status: living backlog / implementation tracker  
Purpose: capture implemented features and future improvements so the package evolves intentionally.

## Package Thesis

Local and smaller open-weight models perform best when agent instructions are explicit, staged, validated, context-aware, loop-safe, and durable across interruptions. The package helps users engineer prompts, skills, repo instruction files, and skill migrations that work reliably under limited context, imperfect reasoning, and varied agent harnesses.

## Current Core Skills

- [x] `local-model-prompt-engineer`
- [x] `local-model-skill-engineer`
- [x] `local-model-skill-migrator`
- [x] `local-model-instruction-engineer`
- [x] `local-model-agent-evaluator`

Package structure:

- [x] Option C: canonical shared references under `shared/` plus copied references inside each skill for standalone installation.
- [x] README with install instructions.
- [x] Validation script.
- [ ] Sync script for shared references.
- [ ] Release builder script.
- [ ] Webpage / landing page.

## Implemented Foundation

- [x] Model profiles: `generic-local`, `qwen36`, `gemma4`, `llama3`.
- [x] Domain intent detection.
- [x] Interaction modes: YOLO, guided, review-gate, audit-only, stage, apply, restore.
- [x] Prompt-control feasibility checks.
- [x] No exposed chain-of-thought rule.
- [x] Context engineering / context-risk detection.
- [x] Persistent task state.
- [x] Subagent delegation.
- [x] Engineering metadata.
- [x] Educational change reports.
- [x] Reference optimization and validation.
- [x] Ralph loop with A-F grading.
- [x] Phased planning with durable memory.
- [x] Phase compression and debrief.
- [x] Do-not-carry-forward notes.

## Top Reliability Improvements

- [x] `shared/loop-safety.md`
- [x] Git safety rules.
- [x] Existing instruction scan / duplicate safeguard detection.
- [x] Canonical output location policy.
- [x] `.gitignore` suggestion policy for `.agent-work/` and related artifacts.
- [x] Ralph A-F scoring with bounded iteration rules.
- [x] Domain profiles and side-effect matrix.
- [x] Interaction modes across the package.
- [x] Instruction conflict detector.
- [x] Package validation script.

## Recent Implemented Ideas

### Loop and Tool Safety

- [x] Tool-call format discipline is harness-aware rather than hardcoded to markdown JSON.
- [x] No identical consecutive tool calls.
- [x] Retry budgets.
- [x] Recent action checks.
- [x] No-op edit detection.
- [x] Same-output detection.
- [x] Anti-brainstorming rules.
- [x] Planning-loop guard.
- [x] Execution-loop guard.
- [x] Escalation strings.

### Existing Instruction Scan

- [x] Scan `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursorrules`, `.windsurfrules`, `.cursor/rules/*`, `.continue/config.*`, `.aider.conf.yml`, and harness-specific files.
- [x] Detect equivalent safeguards by concept, not only exact wording.
- [x] Reuse, strengthen, consolidate, then add only missing safeguards.
- [x] Token-bloat guard.

### Output Location and Git Hygiene

- [x] Canonical project output under `<project>/.agent-work/`.
- [x] Canonical Ralph iteration folders.
- [x] Migration workspace policy.
- [x] `/tmp` limited to disposable scratch.
- [x] `.gitignore` suggestions.
- [x] Commit-worthiness check for agent artifacts.

### Git Safety

- [x] Destructive Git commands require explicit approval.
- [x] Rebase policy.
- [x] Working tree protection.
- [x] Git loop prevention.
- [x] Branching and commit guidance.
- [x] Do not run `git add`, `git commit`, or `git push` unless explicitly asked.

### Coding Standards

- [x] Repo-aware coding standards.
- [x] Practical SOLID guidance without over-engineering.
- [x] Python / PEP 8 guidance.
- [x] JavaScript/TypeScript baseline guidance.
- [x] Validation evidence rules.
- [x] UI standards.
- [x] No emojis by default unless project/user asks.

### Data Science / ML / AI

- [x] Data handling standards.
- [x] Leakage prevention.
- [x] Evaluation discipline.
- [x] Reproducibility rules.
- [x] LLM/RAG standards.
- [x] AI modality profiles: tabular, time series, vision, NLP, speech/audio, multimodal/agentic AI.

## Future Ideas Backlog

### Additional Skills

- [x] `local-model-agent-evaluator` — implemented.
- [ ] `local-model-profile-builder` — create/update model profiles based on user tests, model cards, runtime behavior, and known failure modes.
- [ ] `agent-task-state-manager` — initialize, clean, audit, or resume persistent task-state folders.
- [ ] `local-model-agent-harness-adapter` — adapt instructions for OpenCode, Codex, OpenClaw, Hermes, Aider-like tools, Cursor, Continue, etc.

### Harness Profiles

- [ ] Add `references/harness-profiles/`.
- [ ] Add `generic-agent.md`.
- [ ] Add `opencode.md`.
- [ ] Add `codex.md`.
- [ ] Add `aider.md`.
- [ ] Add `openclaw.md`.
- [ ] Add `hermes.md`.
- [ ] Add `cursor.md`.
- [ ] Add `continue.md`.
- [ ] Add `cli-only.md`.

Harness profile fields:

- tool-call format
- file-edit behavior
- approval model
- subagent support
- shell support
- browser/web/search support
- runtime/model parameter control
- known failure modes

### Domain Profiles

- [x] Coding.
- [x] Documents.
- [x] Email.
- [x] Purchasing/tickets.
- [x] Research.
- [x] Scheduling.
- [x] Data science / ML.
- [x] AI modalities.
- [ ] Travel.
- [ ] Finance-sensitive.
- [ ] Legal-sensitive.
- [ ] Medical-sensitive.
- [ ] Personal knowledge management.
- [ ] Workflow automation.

### Prompt and Skill Evaluation

- [x] Separate validation pass/fail from quality grade.
- [x] A-F scoring.
- [x] Ship / iterate / ask-user / reject labels.
- [x] Regression-risk evaluation.
- [ ] Token impact report with approximate word/token counts.
- [ ] Automated duplicate-rule detector script.
- [ ] Automated exposed-CoT phrase scanner.

### Task State and Phase Memory

- [x] Durable task-state folder.
- [x] Phase closeout.
- [x] Do-not-carry-forward notes.
- [x] Active context manifest.
- [ ] Task-state cleanup skill.
- [ ] State file size-limit enforcement.
- [ ] Phase summary compaction command.

### Subagents

- [x] Subagent cost gate.
- [x] Narrow subagent report schemas.
- [x] Main-agent synthesis responsibility.
- [ ] Task-specific subagent report templates.
- [ ] Subagent conflict-resolution protocol.

### Repo and Release Tooling

- [x] README quick start examples.
- [x] Detailed invocation examples per tool.
- [x] Package validation script.
- [ ] `scripts/sync_shared_refs.py`.
- [ ] `scripts/build_release.py`.
- [ ] `scripts/check_no_duplicate_rules.py`.
- [ ] `scripts/check_references.py`.
- [ ] GitHub Actions validation workflow.
- [ ] Example outputs for each skill.

## Phased Execution Plan Lessons

Problem observed:

- A prompt builder generated a nice three-phase plan for porting a large Windows/macOS application to Linux.
- Three phases were too coarse for a small model.
- The task caused context churn.
- The plan lacked durable memory/progress documentation.

Implemented response:

- [x] Phase granularity must scale with task complexity.
- [x] Complex tasks should usually use 6–12 phases.
- [x] Each phase needs explicit goal, inputs, likely files, tasks, outputs, validation, stop condition, and handoff notes.
- [x] Long plans require persistent phase memory.
- [x] End-of-phase debrief and do-not-carry-forward notes are required for long tasks.

Large porting/migration tasks should usually include phases such as:

1. Repository inventory and build-system discovery
2. Platform-dependency inventory
3. Runtime/environment assumptions
4. Build bootstrap on Linux
5. Dependency replacement strategy
6. Filesystem/path/process/shell compatibility
7. UI/windowing/input/audio/network compatibility, if relevant
8. Test harness setup
9. Incremental port of core modules
10. Incremental port of platform-specific modules
11. Packaging/distribution work
12. Validation, regression testing, and cleanup

## Product / README Ideas

- [x] README should explain why the toolkit exists.
- [x] README should provide multiple invocation examples per tool.
- [x] README should explain benefits without pushy sales copy.
- [ ] Add screenshots or example before/after diffs.
- [ ] Add a simple webpage later.
- [ ] Add a “Which skill should I use?” decision tree.

## Open Design Questions

- [ ] Should harness profiles become first-class in v1.2?
- [ ] Should the profile builder be its own skill or part of the skill engineer?
- [ ] Should `.agent-work/` default sprint be `general` or inferred from repo/project name?
- [ ] Should generated AGENTS.md files include a short “Local Model Notes” section or keep all local-model behavior implicit?
- [ ] Should model profiles include user-observed empirical notes separately from public/official guidance?
