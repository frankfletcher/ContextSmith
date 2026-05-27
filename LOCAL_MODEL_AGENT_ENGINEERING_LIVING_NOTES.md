# Local Model Agent Engineering — Living Design Notes

Status: living backlog / implementation tracker  
Purpose: capture implemented features and future improvements so the package evolves intentionally.

## Package Thesis

Local and smaller open-weight models perform best when agent instructions are explicit, staged, validated, context-aware, loop-safe, and durable across interruptions. The package helps users engineer prompts, skills, repo instruction files, and skill migrations that work reliably under limited context, imperfect reasoning, varied agent harnesses, and chained-skill workflows.

## Current Core Skills

- [x] `local-model-prompt-engineer`
- [x] `local-model-skill-engineer`
- [x] `local-model-skill-migrator`
- [x] `local-model-instruction-engineer`
- [x] `local-model-agent-evaluator`

Package structure:

- [x] Option C: canonical shared references under `shared/` plus copied references inside each skill for standalone installation.
- [x] README with install instructions.
- [x] Detailed invocation examples per tool.
- [x] Control phrases / keyword cheat sheet.
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
- [x] Targeted context length as a first-class control.
- [x] Persistent task state.
- [x] Subagent delegation.
- [x] Engineering metadata.
- [x] Educational change reports.
- [x] Reference optimization and validation.
- [x] Ralph loop with A-F grading.
- [x] Phased planning with durable memory.
- [x] Phase compression and debrief.
- [x] Do-not-carry-forward notes.
- [x] Upstream artifact audit.
- [x] Instruction precedence hierarchy.
- [x] Skill interoperability / workflow collision handling.

## Top Reliability Improvements

- [x] `shared/loop-safety.md`
- [x] Git safety rules.
- [x] Existing instruction scan / duplicate safeguard detection.
- [x] Canonical output location policy.
- [x] `.gitignore` suggestion policy for `.agent_work/` and related artifacts.
- [x] Ralph A-F scoring with bounded iteration rules.
- [x] Domain profiles and side-effect matrix.
- [x] Interaction modes across the package.
- [x] Instruction conflict detector.
- [x] Package validation script.
- [x] Upstream artifact audit for chained optimizers/skills.
- [x] Instruction precedence and conflict resolution.
- [x] `targeted_context_length` metadata and context-tier behavior.
- [x] Phase compression/debrief and do-not-carry-forward guidance.

## Recent Implemented Ideas

### Targeted Context Length

- [x] Recognize `targeted context length: 32k`, `context length: 32k`, `ctx: 32k`, and related phrases.
- [x] Normalize generated metadata to `metadata.targeted_context_length`.
- [x] Derive context tier: tiny, tight, moderate, large, very-large.
- [x] Make context length materially affect phase granularity, verbosity, example count, output budget, batching, persistent state, and subagent use.
- [x] Add targeted context fit to A-F grading.

### Upstream Artifact / Multi-Skill Safety

- [x] Treat upstream skill/optimizer outputs as inputs to verify, not authoritative truth.
- [x] Classify upstream additions as confirmed, likely, useful suggestion, unsupported, conflicting, or rejected.
- [x] Reject hallucinated frameworks/libraries/dependencies when unsupported by user request or project evidence.
- [x] Detect workflow collisions between external skill workflows and local-model workflows.
- [x] Support bridge artifacts such as `WORKFLOW_ADAPTER.md` when workflows must be reconciled.
- [x] Add skill interoperability grading.

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

- [x] Canonical project output under `<project>/.agent_work/`.
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
- [x] Targeted context fit grading.
- [x] Skill interoperability grading.
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
- Three phases were too coarse for a small model and tight context.
- The task caused context churn.
- The plan lacked durable memory/progress documentation.

Implemented response:

- [x] Phase granularity must scale with task complexity and targeted context length.
- [x] Complex tasks should usually use 6-12 phases, and tight context often needs more smaller phases.
- [x] Each phase needs explicit goal, inputs, likely files, tasks, outputs, validation, stop condition, and handoff notes.
- [x] Each phase needs debrief, carry-forward, and do-not-carry-forward notes.
- [x] Durable task-state files should be created for long-running projects.


## v1.3 Implemented

- [x] Added CLI-style parameter support across all skills.
- [x] Added `shared/control-parameters.md` with parsing, normalization, conflict handling, and skill-specific flags.
- [x] Added help/describe/examples/modes/parameters/quickstart support across all skills.
- [x] Added per-skill `references/help.md` pages.
- [x] Updated README with CLI-style examples and a flag cheat sheet.
- [x] Preserved natural-language control phrases while making flags first-class for repeatability.
- [x] Added package spec notes explaining that flags are an instruction convention and future CLI/UI bridge.

## Future Ideas Still Open

- [ ] Build an actual `contextsmith` CLI around the same flags.
- [ ] Build a local-first UI/workbench after CLI semantics stabilize.
- [ ] Add harness profiles for OpenCode, Hermes, OpenClaw, Codex, Cursor, Aider, Continue.
- [ ] Add package sync/release builder scripts for Option C shared-reference copying.
- [ ] Add a tiny router skill only if users struggle to pick the correct specialized skill.

## v1.4.0 Living Notes Update

### Implemented in this pass

- [x] Rewrite README to be more compelling and less AI-generic.
- [x] Split long user-manual content into `docs/`.
- [x] Add factual project status section.
- [x] Add SemVer-style versioning policy going forward without backfilling/renumbering history.
- [x] Add model capability tiers beyond small/local models.
- [x] Add planner/executor workflow guidance.
- [x] Add implementation plan audit rubric.
- [x] Add small-context workflow documentation.
- [x] Add test-quality audit rubric.
- [x] Add phase code review loop.
- [x] Add education-level and artifact-verbosity controls.
- [x] Add runtime-stability diagnostic guidance for local agentic coding.

### Future ideas retained

- [ ] Build a real `contextsmith` CLI.
- [ ] Build a local-first UI after CLI/workflows stabilize.
- [ ] Add harness profiles for OpenCode, Codex, Cursor, Aider, OpenClaw, Hermes, and generic CLI agents.
- [ ] Add optional UI handoff protocol once CLI/UI exists.
- [ ] Add package sync/release scripts for shared reference propagation.
- [ ] Add full behavioral test fixtures for prompts, skills, AGENTS.md files, plans, and test audits.
- [ ] Consider a tiny router/help skill only if users struggle to choose the correct skill.


## Documentation and Onboarding

- [x] Keep README as a project documentation landing page instead of a full manual.
- [x] Use `Quick Start` as the entry section rather than growth-hacky wording like “first success.”
- [x] Add `docs/QUICKSTART.md` for practical first-run workflows.
- [x] Add `docs/WHICH_SKILL.md` to reduce tool-selection cognitive load.
- [x] Split deeper guidance into human docs under `docs/` while keeping `shared/` as agent-facing references.
- [x] Humanize terse docs with explanations, examples, benefits, and common failure modes.
- [x] Keep project status factual: lightweight validation exists; behavioral/integration tests are not yet implemented.
- [x] Preserve strong project soundbites for README and eventual website copy.
- [ ] Add screenshots or terminal-output examples once real usage examples are available.
- [ ] Create a web page later using the README positioning and soundbites.


## Documentation quality and voice

- [x] Separate project documentation from agent references.
- [x] Add documentation-quality audit for README/docs/user-facing explanations and educational reports.
- [x] Add documentation style guide with tone, factuality, examples, and generated-writing-pattern checks.
- [x] Avoid using third-party writing-assistant product names in ContextSmith package docs or generated artifacts.
- [x] Replace “project documentation docs” wording with project documentation/user guides/reader-facing explanations as appropriate.
- [x] Reorganize docs into workflows, concepts, reference, and contributing sections.
- [x] Reduce repeated “not just X, but Y” contrast patterns in README-style copy.
- [x] Use suggestive language in user docs where appropriate; keep agent references direct for safety-critical instructions.

## Run configuration preview

- [x] Add run configuration preview for guided, deep, review-gate, AGENTS.md, migration, and file-changing workflows.
- [x] Show inferred parameters with short reasons.
- [x] Call out low-confidence assumptions.
- [x] Let users change one parameter instead of rewriting the request.
- [x] Keep fast/yolo paths lightweight unless approval is required.
