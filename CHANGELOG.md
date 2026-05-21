# Changelog



## v1.0 

### 2026-05-19

- Added Ralph loop with A-F grading and numbered iterations.
- Added educational change reports.
- Added domain intent detection and guardrails.
- Added interaction modes: YOLO, guided, review-gate, audit-only, stage/apply.
- Strengthened assumption control.
- Added phased planning and persistent task memory requirements.
- Added `local-model-instruction-engineer`.
- Added `local-model-agent-evaluator`.
- Packaged all skills into a GitHub-ready repo layout.



## Consolidation of individual scripts pre-v1.0

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
- Added support for sprint/subproject/task hierarchy under `.agent-work/`.
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
