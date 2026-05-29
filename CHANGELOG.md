# Changelog

## Unreleased

### Changed

- Strengthened `local-model-prompt-engineer`, `local-model-instruction-engineer`, `local-model-skill-engineer`, `local-model-skill-migrator`, and `local-model-agent-evaluator` so long-running planning workflows require or audit a concrete task-state directory with `TASK.md`, `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `CONTEXT.md`, `CHECKLIST.md`, `ARTIFACTS.md`, `PHASE_LOG.md`, and `NEXT_PROMPT.md`, instead of allowing a single narrative plan file to stand in for persistent state. The guidance now distinguishes allowed planning artifacts from source-code edits, requires resumable `NEXT_PROMPT.md` handoffs, and reinforces compact state hygiene for paths, commands, validation results, decisions, constraints, and next actions.

## v1.4.2

**Released:** 2026-05-22

### Added

- Added `shared/source-artifact-boundary.md` and wired it into prompt, skill, instruction, and migration workflows so source artifacts with executable-looking instructions are treated as data unless explicitly activated.
- Added `shared/documentation-quality.md` for readability, style, factuality, repeated-phrasing, example usefulness, and generated-writing-pattern checks.
- Added `shared/run-configuration-preview.md` so skills can show inferred parameters, assumptions, and planned approach before important guided/review-gate work.
- Added `--review-config` / `--preview-config` and `--no-review-config` control guidance.
- Added `--focus documentation-quality` guidance for the evaluator.
- Added `docs/contributing/documentation-style.md` and `docs/contributing/documentation-review-checklist.md`.
- Added `docs/workflows/`, `docs/concepts/`, and `docs/reference/` organization with index files.
- Added explicit default-parameter tables to the prompt, instruction, and skill engineering workflows.

### Changed

- Strengthened `local-model-prompt-engineer` with a prompt compiler boundary, non-execution self-check, and output contract reminder to reduce accidental execution of seed prompts.
- Rewrote `README.md` to reduce generated-sounding contrast patterns, remove “project documentation” wording, and keep the tone practical, factual, and reader-centered.
- Reorganized detailed docs into workflow, concept, reference, and contributing sections.
- Updated user documentation to prefer advisory wording where appropriate, while keeping safety-critical agent references direct.
- Updated all skills to reference run configuration previews and documentation-quality checks when relevant.
- Updated package spec terminology from “project documentation docs” to “project documentation.”
- Expanded coding standards with DRY, YAGNI, KISS, readability, and TDD guidance.
- Tightened phased-planning guidance with narrower phase sizing, validation/test expectations, phase compression, implementation-plan audit, and test-quality audit closeout checks.
- Updated targeted-context guidance to reserve more context for tool output and favor more granular phases for moderate and tight context budgets.
- Added `tmp` to `.gitignore`.

### Notes

- This release keeps the product name restriction: no references to third-party writing-assistant product names are included in package docs, skills, references, README, changelog, or generated artifacts.


## v1.4.1

**Released:** 2026-05-22

### Changed

- Reworked the documentation as a project documentation onboarding release rather than only agent-facing reference material.
- Rewrote `README.md` to be a clearer project front door with stronger positioning, a lower-friction Quick Start, fewer dense manual sections, and factual project status language.
- Added `docs/QUICKSTART.md` with practical paths for prompt engineering, AGENTS.md generation, implementation-plan audit, test-quality audit, single-skill conversion, and safe skill migration.
- Added `docs/WHICH_SKILL.md` so users can quickly choose the right ContextSmith skill.
- Expanded `docs/USER_GUIDE.md` with the core mental model, mode guidance, targeted-context explanation, project-local output guidance, and strong-planner/local-executor workflow.
- Expanded `docs/CONTROL_PARAMETERS.md` with human explanations, recommended starting controls, and conflict-handling behavior.
- Expanded `docs/EXAMPLES.md` with copy-paste workflows and benefits for each major tool.
- Expanded `docs/AGENTS_MD_GUIDE.md` into a human-readable guide explaining why AGENTS.md matters, what to include, what to avoid, and how to keep it concise.
- Expanded `docs/SMALL_CONTEXT_WORKFLOWS.md` with context tiers, phase sizing, one-phase-per-session guidance, compaction, persistent task state, and Graphify/index-first workflows.
- Expanded `docs/IMPLEMENTATION_PLAN_AUDIT.md`, `docs/TEST_QUALITY_AUDIT.md`, `docs/PHASE_CODE_REVIEW.md`, `docs/RUNTIME_STABILITY.md`, `docs/MODEL_PROFILES.md`, and `docs/SKILL_MIGRATION.md` with fuller educational explanations and examples.
- Added `docs/FAQ.md`.

### Notes

- No skill behavior changes were required for this patch. This release focuses on reducing cognitive load, improving time-to-use, and separating human documentation from terse agent-facing references.


## v1.4.0

**Released:** 2026-05-22

### Added

- Added `docs/` manual split: user manual, control parameters, examples, small-context workflows, AGENTS.md guide, runtime stability, model profiles, implementation-plan audit, test-quality audit, phase code review, Ralph loop, skill migration, and versioning policy.
- Added `shared/implementation-plan-audit.md` with A-F grading for phase granularity, atomicity, context fit, validation strength, task-state integration, handoff quality, test strategy, and small-model executability.
- Added `shared/small-context-workflows.md` for fresh-session-per-phase workflows, compaction triggers, tight-context phase sizing, and phase handoff.
- Added `shared/test-quality-audit.md` to evaluate baseline coverage, edge-case realism, assertion strength, regression-catching power, fixture realism, over-mocking, DS/ML tests, and LLM/RAG tests.
- Added `shared/phase-code-review.md` for post-phase coding review, focused improvement passes, and phase-local review reports.
- Added `shared/model-capability-tiers.md` for small-local, mid-local, large-local, frontier-cloud, reasoning-specialized, coding-specialized, and multimodal capabilities.
- Added `shared/planner-executor-workflows.md` for strong-planner/local-executor workflows.
- Added `shared/runtime-stability.md` for local agentic coding runtime diagnostics, including context, reasoning, speculative decoding, KV cache, sampling, and harness loop controls.
- Added `shared/education-levels.md` separating human educational verbosity from model-facing artifact verbosity.
- Added new control parameters: `--education-level`, `--artifact-verbosity`, `--phase-review`, `--code-review-iterations`, `--target-capability`, `--planner-profile`, `--executor-profile`, and `--focus`.

### Changed

- Rewrote `README.md` as a clearer landing page with stronger positioning, short quick-start examples, factual project status, and links to deeper docs.
- Updated prompt, skill, instruction, migrator, and evaluator workflows to reference implementation-plan audit, test-quality audit, phase code review, education-level controls, model capability tiers, and planner/executor workflows when relevant.
- Updated package philosophy from small-model-only to small-model-first, capability-aware agent instruction engineering.
- Added SemVer-style versioning guidance going forward without renumbering historical releases.

### Notes

- Versioning is now `MAJOR.MINOR.PATCH` for package releases. Patch releases should be used for documentation, typo fixes, and small refinements; minor releases for backward-compatible capabilities; major releases for breaking changes.

## v1.3

**Released:** 2026-05-20

### Added

- Added CLI-style control parameters across all ContextSmith skills.
- Added `shared/control-parameters.md` with flag parsing, aliases, normalization, conflict handling, and skill-specific flags.
- Added `shared/help-mode.md` and `shared/usage-patterns.md`.
- Added per-skill `references/help.md` files for `help`, `describe`, `examples`, `modes`, `parameters`, and `quickstart` invocations.
- Added README sections for two control styles: natural language and CLI-style flags.
- Added a CLI-style flag cheat sheet and additional detailed invocation examples.
- Added package-spec guidance that CLI-style flags are an instruction convention and future-compatible path toward a real `contextsmith` CLI/UI.

### Changed

- Bumped skill versions: prompt engineer v1.6, skill engineer v1.6, skill migrator v1.4, instruction engineer v1.3, and agent evaluator v1.3.
- Updated every `SKILL.md` to short-circuit normal workflow when help/describe/example/parameter modes are requested.
- Updated every `SKILL.md` to parse CLI-style flags alongside natural-language control phrases.
- Copied new shared references into each skill for standalone installation.

### Notes

- No UI behavior was added. UI handoff remains a future idea.
- Natural-language controls remain supported. CLI-style flags are optional but recommended for repeatable workflows.

## v1.2

**Released:** 2026-05-20

### Added

- Added `targeted_context_length` as a first-class package control and metadata field.
- Added context tiers: tiny, tight, moderate, large, and very-large.
- Added context-length-dependent behavior for prompt verbosity, phase granularity, examples, output budgets, migration batch sizes, persistent task state, subagent use, and report size.
- Added `shared/targeted-context-length.md` and copied it into standalone skill references.
- Added upstream artifact audit for prompts, skills, specs, plans, and instruction files influenced by other optimizers or skills.
- Added unsupported requirement detection to reject hallucinated libraries, frameworks, dependencies, tools, workflows, or domain requirements not supported by user request or project evidence.
- Added skill interoperability guidance for multi-skill workflows and workflow collisions.
- Added instruction precedence hierarchy for resolving conflicts between user requests, safety, project evidence, repo instructions, model profiles, domain requirements, external skill artifacts, preferences, and generic best practices.
- Added bridge-artifact guidance for `WORKFLOW_ADAPTER.md`, `PROMPT_BRIDGE.md`, and `SKILL_BRIDGE.md` when multiple skill workflows must coexist.
- Added README control phrase table and expanded invocation examples showing targeted context length, upstream audits, review-gate mode, deep path, guided mode, and project-local output.
- Added targeted-context-fit and skill-interoperability grading to evaluation rubrics.

### Changed

- Reworked validation gates across all five skills to check targeted context fit and upstream artifact safety.
- Strengthened phase compression/debrief guidance and made it part of long-running task validation.
- Updated engineering metadata guidance to use `targeted_context_length` rather than `usable_context_length`.
- Updated package spec to reflect targeted-context and chained-skill workflows.
- Updated living notes with checkbox tracking for all recently discussed ideas.
- Repeated shared references into each skill for standalone installation.
- Reformatted the changelog so each version uses `**Released:** YYYY-MM-DD` metadata.

### Fixed

- Reduced the risk that another prompt optimizer or frontend skill can silently introduce unsupported project requirements.
- Reduced the risk that nominal model-card context length is mistaken for the actual local runtime target.
- Reduced the risk that large projects receive overly broad three-phase plans under tight context.

## v1.1

**Released:** 2026-05-20

### Added

- Added loop-safety reference and injection guidance.
- Added Git safety, rebase policy, working-tree protection, and Git loop prevention.
- Added canonical output-location policy for Ralph iterations, reports, migrations, and task state.
- Added `.gitignore` suggestion and commit-worthiness guidance for `.agent_work/` artifacts.
- Added instruction-scan/de-duplication rules to avoid duplicate safeguards.
- Added coding standards, practical SOLID guidance, Python/PEP 8 guidance, UI standards, and no-emoji default.
- Added data science / ML / AI modality domain guidance.
- Added side-effect matrix, instruction-conflict detector, and phase compression/debrief reference.
- Expanded README with detailed invocation examples and benefits.
- Converted living notes into a checkbox-based implementation tracker.
- Bumped skill versions: prompt/skill engineer v1.4, migrator v1.2, instruction/evaluator v1.1.

## v1.0

**Released:** 2026-05-19

Initial GitHub-ready consolidation of the local-model agent engineering toolkit. This release bundled the prior standalone Qwen-focused prompt and skill work into a broader, model-profile-driven package for local/open-weight models.

### Pre-consolidation lineage included in v1.0

- Created the original `qwen36-prompt-engineer` skill for Qwen3.6-27B prompt design.
  - Added strict, literal, smaller-model-oriented prompt structure.
  - Added no-exposed-chain-of-thought guidance.
  - Added deterministic output-contract patterns.
  - Added Qwen-specific runtime guidance as optional model-profile material rather than assuming the skill could control runtime variables.
  - Added prompt package sections for assumptions, target model/profile, system prompt, user prompt, examples, validation, and runtime recommendations when relevant.

- Iterated the Qwen prompt engineer after skill-review feedback.
  - Reduced the main `SKILL.md` from a large monolithic file into a smaller progressively disclosed skill.
  - Moved detailed templates, runtime settings, failure modes, prompt audit checks, and Refract/diversity guidance into references.
  - Removed unsupported/unknown top-level frontmatter keys.
  - Added prompt-quality checks inspired by skill-auditor behavior: specificity, trigger/intent quality, completeness, distinctiveness, conciseness, actionability, workflow clarity, progressive disclosure, model compatibility, and no exposed CoT.

- Created the original `qwen36-skill-optimizer` skill to convert existing skills for Qwen3.6-27B.
  - Added source-contract extraction before rewriting.
  - Added semantic-preservation rules to prevent the optimizer from merely making skills “Qwen-shaped” while changing behavior.
  - Added semantic diff validation covering preserved, changed, removed, and added behaviors.
  - Added no-invented-precision rules to prevent fabricated thresholds, policies, or confirmation gates.
  - Added permission-boundary preservation.
  - Added command, flag, reference, script, and resource preservation.
  - Added default-output-contract guidance without making flexible source behavior brittle.

- Iterated the skill optimizer after audit/review feedback.
  - Collapsed overly long phase structures into fewer clearer phases.
  - Added skill-auditor-style checks: mechanical validity, description quality, conciseness, actionability, workflow clarity, progressive disclosure, and local-model compatibility.
  - Added reference files for conversion patterns, semantic diff, examples, context management, and model profiles.
  - Added a required conversion audit so users can see what changed and why.

### Generalization from Qwen-specific skills to local-model skills

- Renamed and generalized the core skills into local/open-weight model tools:
  - `local-model-prompt-engineer`
  - `local-model-skill-engineer`
  - `local-model-skill-migrator`
  - `local-model-instruction-engineer`
  - `local-model-agent-evaluator`

- Introduced model-profile architecture.
  - Added profiles for `generic-local`, `qwen36`, `gemma4`, and `llama3`.
  - Moved model-specific reasoning/runtime guidance out of the central skill logic.
  - Kept the central rules model-agnostic: literal instructions, strict output contracts, progressive disclosure, no exposed CoT by default, context-risk management, validation, and atomicity for smaller models.
  - Preserved Qwen3.6 as an available/default profile when appropriate, while avoiding Qwen-only assumptions for Gemma, Llama, or unknown local models.

### local-model-prompt-engineer v1.3

- Added support for creating, improving, auditing, and packaging prompts for local/open-weight models.
- Added model-profile selection and fallback to `generic-local` when the target model is unknown.
- Added prompt-control feasibility checks to distinguish prompt-fixable issues from missing data, weak tools, retrieval problems, runtime limits, or model capability limits.
- Added context-engineering guidance for short input, pasted long input, file paths, repos/folders, retrieved context, tool output, and multi-turn agent state.
- Added generated-prompt support for:
  - context strategy
  - persistent task state
  - subagent delegation
  - Graphify/index-aware context lookup when available
  - prompt test plans
  - output contracts
  - validation gates
- Added test-driven prompt engineering guidance inspired by prompt evaluation practices.
- Added prompt package metadata: engineer name, version, target model, profile used, optimization scope, assumptions, and runtime recommendation boundaries.
- Added educational reporting: original strengths, weaknesses, changes made, why changes improve local-model reliability, and remaining risks.
- Added optional Ralph loop support with bounded iteration and A–F grading concept in shared references.

### local-model-skill-engineer v1.3

- Added creation, conversion, improvement, audit, and packaging of `SKILL.md`-based agent skills.
- Added skill contract extraction for purpose, triggers, inputs, outputs, tools, files/resources, side effects, permission boundaries, failure handling, and validation.
- Added semantic-preserving conversion rules for existing skills.
- Added target-profile engineering metadata for generated/converted skills.
- Added conservative reference optimization.
  - References are treated as part of the skill contract when linked or behaviorally relevant.
  - The engineer inventories `references/`, `scripts/`, `assets/`, and `agents/`.
  - It modifies behavioral references only when needed and reports every modified reference.
  - It avoids rewriting scripts/assets unless explicitly required or behaviorally necessary.
- Added reference validation: linked references exist, instructions say when to read them, no contradictory model-profile guidance, no duplicate large blocks, and no exposed CoT patterns.
- Added local-model compatibility gate, context-risk audit, persistent-state audit, subagent delegation audit, Graphify/index support audit, and skill-auditor-style validation.
- Added educational change report to show original strengths, original weaknesses, changes made, improvement rationale, and remaining risks.

### local-model-skill-migrator v1.1 baseline

- Added a conservative recursive migration skill for directories such as `~/.agents/skills`.
- Defaulted to staged migration rather than in-place rewrites.
- Added safe workflow:
  - inventory
  - plan
  - backup
  - stage conversion
  - validate
  - report
  - apply only with explicit approval
- Added modes: audit-only, plan-only, stage, apply, and restore.
- Added timestamped migration workspaces with backup, staging, reports, manifest, and restore instructions.
- Added per-skill risk classification: low, medium, high.
- Added target-profile metadata marking for migrated skills.
- Added conservative reference optimization during migration.
- Added batch-level manifest and reports so migrated output can be reviewed before applying.

### local-model-instruction-engineer v1.0

- Added a new skill for creating, optimizing, and auditing agent-facing instruction files that are not prompts or skills.
- Supported instruction artifacts such as:
  - `AGENTS.md`
  - `CLAUDE.md`
  - `GEMINI.md`
  - `.github/copilot-instructions.md`
  - `.cursorrules`
  - `.windsurfrules`
  - harness-specific instruction files
- Added repo-aware scanning before generating or editing instruction files.
- Added detection of project structure, languages, frameworks, package/build files, test/lint commands, existing instruction files, and relevant domain signals.
- Added support for layered instruction files, with root-level general rules and nested subproject-specific rules only when justified.
- Added local-model-oriented instruction guidance: atomic steps, clear validation, loop-safety hooks, context economy, and small-model-friendly operating rules.

### local-model-agent-evaluator v1.0

- Added a non-mutating evaluator skill for prompts, skills, AGENTS.md files, and other agent-facing instructions.
- Separated “passes validation” from “is actually good.”
- Added A–F style grading hooks for small-model fit, clarity, actionability, context strategy, validation strength, assumption control, and bloat/cognitive load.
- Added recommendations such as ship, iterate, ask user, reject, or stage for review.
- Added regression-risk and token-impact concepts for edited artifacts.

### Shared references and package architecture

- Adopted Option C packaging:
  - canonical shared references under `shared/`
  - copied per-skill references inside each skill for standalone installation
- Added shared model profiles.
- Added shared domain profiles for coding, documents, email, purchasing/tickets, research, scheduling, data science/ML, and AI modalities.
- Added shared references for:
  - context management
  - persistent task state
  - subagent delegation
  - Ralph loop
  - interaction modes
  - small-model atomicity
  - domain intent detection
  - engineering metadata
  - educational reports
  - phased planning
  - reference optimization
  - evaluation rubrics
- Added persistent task-state conventions for long-running work:
  - `TASK.md`
  - `PLAN.md`
  - `STATUS.md`
  - `DECISIONS.md`
  - `CONTEXT.md`
  - `CHECKLIST.md`
  - `ARTIFACTS.md`
  - `PHASE_LOG.md`
  - `NEXT_PROMPT.md`
- Added support for sprint/subproject/task hierarchy under `.agent_work/`.
- Added guidance for avoiding task-state junk drawers: narrow file responsibilities, summaries instead of raw dumps, state hygiene, cleanup, and resume prompts.
- Added subagent delegation rules: bounded scopes, exact files/directories, compact report schemas, no full-context dumping, main-agent synthesis, and conflict resolution by evidence.
- Added Graphify/index-aware guidance as an optional context provider for large repos/document sets.
- Added a validation script for package-level skill checks.

### README and repository packaging

- Added initial README, package specification, changelog, living notes, scripts directory, shared references, and individual skill folders.
- Added installation guidance for copying all skills or installing individual skills.
- Added basic invocation examples for the five skills.
- Added version metadata to skills.
- Added package-level living notes so future ideas can be tracked without immediately expanding the core skills.
