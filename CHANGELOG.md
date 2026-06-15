# Changelog

## v2.2.0

**Released:** 2026-06-15

### Added

- Added `.contextsmith/audit-with-extra.json` workflow config chaining `audit_current_phase` → `extra_audit` with read-only permissions. Provides the deployment vehicle for strategic-lens review per `shared/extra-audit.md`.
- Added `scripts/lint_error_counter.py` to AGENTS.md Repository Map; added reset command and purpose description.
- Added AGENTS.md validation commands pipe through lint error counter for both `ruff check` and `markdownlint`.

### Changed

- Phase 11 (Tooling and Audit Infrastructure) completed: extra-audit workflow config validated, lint counter documented and integrated, decision records verified, full validation suite passes.

### Notes

- All 423 tests pass. Ruff lint and format clean. Markdownlint pre-existing only (`.agent_work/release_bundle/`, `.agent_work/staged_skills/`). Validate_skills.py passes all 8 skills.
- The project is complete: all 11 phases of the artifact schema standards project are delivered.

## v2.1.0

**Released:** 2026-06-14

### Added

- Added artifact schema standards: `schemas/artifact_schemas.yaml` defines required and optional sections, content rules, and validation metadata for all 11 markdown artifact types (STATUS.md, PLAN.md, CONTEXT.md, PHASE_LOG.md, EDUCATIONAL_REPORT.md, AUDIT_REPORT.md, EXTRA_AUDIT.md, DECISIONS.md, ARTIFACTS.md, CHECKLIST.md, TASK.md, NEXT_PROMPT.md).
- Added `state_reader._parse_phase_tree()` — three-level hierarchical parser for PLAN.md (### Phase, #### Sub-phase, - [x] Task) with flat-format backward compatibility and `current_subphase` in `read_status()`.
- Added `validators.validate_phase_tree_structure()` — structural validation of PLAN.md hierarchy with status checking and task well-formedness.
- Added `validators.validate_plan_phase_order()` — cross-reference PLAN.md phases against workflow config `phase_order`.
- Added `_extract_subphase_budget()` to step compiler — extracts Context Budget metadata from sub-phase definitions for phase-level context allocation.
- Added `_try_advance_subphase()` to orchestrator — auto-advances through pending sub-phases with dependency checking and STATUS.md updates.
- Added `artifact_schemas` extension to `workflow_config.schema.json` — `ArtifactSchemaOverride` with `extend_base`, `required_sections`, `optional_sections`, and `additional_sections` for workflow-specific overrides.
- Added `_build_artifact_overrides()` to validators — merges config-level schema overrides with base artifact schemas.
- Added `docs/reference/ARTIFACT_SCHEMAS.md` — user-facing documentation for the schema registry, PLAN.md hierarchical format, STATUS.md sub-phase tracking, and the validation pipeline.
- Added `tests/test_subphase_advancement.py` — 6 integration tests for sub-phase dispatch, completion detection, flat-plan compatibility, and dependency skipping.
- Added 22 new tests across validators, state reader, and step compiler for phase tree parsing, structural validation, budget extraction, and plan–config cross-referencing (403 → 425 total).

### Changed

- **Phase plans now use hierarchical format** — `PLAN.md` defines phases with `###`, sub-phases with `####`, and tasks with `- [ ]` / `- [x]` checkboxes. Sub-phases carry Context Budget, Dependency, and Validation metadata.
- `read_plan()` detects `###` headings and dispatches to `_parse_phase_tree()` automatically; flat checkbox format still supported.
- `compile_step_contract()` accepts `current_subphase` and propagates it to `StepContract.subphase_name` and `subphase_context_budget`.
- `_rewrite_status_content()` and `_update_status()` support `Current Sub-phase` field for tracking active sub-phase.
- `_generate_next_prompt()` includes sub-phase name and task list from PLAN.md.
- `validate_artifacts_with_schemas()` now reads both `section_requirements` and `artifact_schemas` config keys, merging overrides via `_build_artifact_overrides()`.
- `schemas/workflow_config.schema.json` upgraded with `ArtifactSchemaOverride` `$def` and `artifact_schemas` property.
- 9 orchestrator functions refactored from cyclomatic complexity C to ≤ B using radon-guided extraction.
- All markdown tables in `docs/` standardized to spaced pipe separators (MD060 fix).

### Notes

- The project now has 425 passing tests, ruff lint and format clean, and all markdown files pass markdownlint.
- Phase plans migrated from flat checkbox lists to hierarchical format with context budgets and validation metadata per sub-phase.
- The `.new` file auto-merge mechanism is implemented in the orchestrator but not yet deployed as the production runtime; agents currently merge `.new` segments manually (see DECISIONS.md D12).

## v2.0.0

**Released:** 2026-06-13

### Added

- Added `contextsmith-orchestrator` skill — a deterministic state-machine executor that runs workflow configs, raw prompts, and task-state handoffs through a 14-step execution loop with validation gates, self-audit, Ralph loops, and evidence-ledger tracking.
- Added `contextsmith-workflow-developer` skill — generates `workflow_config.yaml` from requirements and domain templates, routing through the orchestrator for execution.
- Added `orchestrator/` Python package (state reader, checkpoint manager, step compiler, harness adapters, validators, CLI) enabling `python -m orchestrator` as a code-level entry point alongside the skill.
- Added deterministic exit codes: `EXIT_DONE=0`, `EXIT_BLOCKED=1`, `EXIT_CONTINUE=2`, `EXIT_CONFIG_ERROR=3`, `EXIT_STATE_INCONSISTENCY=4`, `EXIT_INTERNAL_ERROR=5`.
- Added `validation_mode` field to workflow config state definitions (`strict`/`relaxed`/`none`) with per-state validation strictness enforcement.
- Added `checkpoint_before_run` with pre-dispatch checkpoint markers, stale-marker detection, and crash-recovery warnings on startup.
- Added pre-dispatch retry counter check — phases at `max_retries` block immediately without dispatching the agent.
- Added `model_pin`, `timeout_s`, and `ralph_max_cycles` as per-state configurable parameters, wired from schema through step compiler to harness adapter.
- Added RESULT.json fallback protocol — when RESULT.json is absent (backward compatibility), orchestrator infers status from artifact presence.
- Added append-only file protection — orchestrator snapshots report files before dispatch and auto-repairs on overwrite by prepending original content.
- Added `validate_append_only()` to `orchestrator/validators.py` — validates file content starts with original prefix.
- Added `shared/file-safety.md` — extracted file operation safety rules (read-before-write, append for records, verify after write) into a dedicated reference.
- Added `shared/harness-generic.md` — companion reference for the generic (fallback) harness adapter.
- Added `shared/complexity-gate.md` — reference for enforcing cyclomatic complexity (radon cc) and maintainability index (radon mi) gates in the validation pipeline.
- Added `references/artifact-templates.md` to orchestrator skill — extracted artifact templates for STATUS.md, PHASE_LOG.md, CHECKLIST.md, NEXT_PROMPT.md, RESULT.json, and checkpoint.json.
- Added 90 new tests (374 total): `test_orchestrator_state.py`, `test_checkpoint.py`, `test_step_compiler.py`, `test_orchestrator_determinism.py`, plus test extensions for append validation, exit-code propagation, dry-run, end-to-end workflow, and pre-dispatch marker detection.
- Added `orchestrator/__main__.py` — makes the orchestrator runnable as `python -m orchestrator`.
- Added `.phase_gate` flag file convention for human-review gates between phase handoffs.
- Added `.agent_work/ideation/deep_determinism/schemas/` with workflow config and agent config JSON schemas.
- Added domain-templates to `contextsmith-workflow-developer/references/domain-templates/` (6 templates).
- Added project-level versioning policy: all skills share a single version from `PACKAGE_SPEC.md`; per-skill `metadata.version` mirrors it.

### Changed

- **Removed `contextsmith-run` skill.** All execution — single prompts, task-state handoffs, phased plans — now routes through `contextsmith-orchestrator`. The orchestrator absorbs the run skill's contract, validation, evidence, Ralph, and domain-routing patterns.
- **Version bump 1.7.1 → 2.0.0** across all surviving skills.
- Upgraded `schemas/workflow_config.schema.json` and `schemas/agent_config.schema.json` from JSON Schema draft-07 to 2020-12 (`definitions` → `$defs`, updated `$schema` URI).
- Reduced `skills/contextsmith-orchestrator/SKILL.md` from 572 to 468 lines by extracting artifact templates to `references/artifact-templates.md`.
- Documented "agent output is evidence, not authority" rule in orchestrator SKILL.md and `resolve_next_state()` docstring — the orchestrator owns state transitions, not the agent.
- Updated router skill (`contextsmith/SKILL.md`) — removed `contextsmith-run` from routing table, merged wizard execute options into one "Execute a task" → orchestrator entry.
- Converted `contextsmith-workflow-developer` from a standalone config generator to a thin delegator that invokes the orchestrator with its own `workflow_config.yaml` meta-config.
- Refactored 9 C-ranked orchestrator functions to ≤ B complexity using radon-driven extraction (complexity cleanup pass 6.75).
- Updated all 6 skill `reference_manifest.yml` files to include `shared/file-safety.md` as a conditional-load reference.
- Updated `shared/loop-safety.md` — extracted duplicate file operation safety content into `shared/file-safety.md`.
- Updated `AGENTS.md` — shared reference count 42 → 52, added complexity/maintainability section, replaced `contextsmith-run/` with `contextsmith-orchestrator/` in repository map.
- Updated `PACKAGE_SPEC.md` with project-level versioning decision.
- Upgraded `orchestrator/__init__.py` to export all exit codes, `run()`, and `run_workflow()`.
- Fixed all MD060 table-style issues in `docs/` (15 files) — table header separators now use spaced pipes.

### Fixed

- Fixed `validate_append_only()` byte comparison (`==` → `startswith`) — the original prefix could exceed the check window, causing false positives.
- Fixed harness-generic.md not being included in orchestrator `reference_manifest.yml` (completed in 5.5d, missing entry resolved in 6c).
- Fixed cross-references from 5 existing `reference_manifest.yml` files to correctly point to `shared/file-safety.md`.

### Notes

- This release marks the Deep Determinism project completion (Phases 1-8). The orchestrator is now a deterministic Python state machine with harness-agnostic adapters, production validation, and append-only file safety. Phase 9 (Final Validation and Lock) remains to run full validation and tag the release.

## v1.7.1

**Released:** 2026-06-01

### Added

- Added `scripts/token_budget.py` to estimate always-loaded SKILL.md token footprints, common runtime load sets, and largest shared references, with `--strict` regression checks for release builds.
- Added compact core references for artifact manifests, control parameter parsing, execution contracts, and evidence ledgers so routine skill runs can avoid loading full catalogs while preserving mandatory validation/audit/Ralph enforcement and full-reference fallback.

### Changed

- Added a token-budget gate to `scripts/build_release.py` after skill validation.
- Tightened prompt, instruction, skill, and run skills so declared Ralph loops, audit gates, validation, phase review, plan-completion audit, and evidence checks are mandatory unless explicitly disabled.
- Bumped all skill versions and reference manifests to 1.7.1.

### Fixed

- Corrected `contextsmith-skill-engineer` wording so it describes SKILL.md packages rather than generic instruction files.
- Strengthened artifact-manifest propagation so widening context use, side effects, target model assumptions, validation strictness, or external actions requires explicit current-user approval.

## v1.7.0

**Released:** 2026-06-01

### Changed

- Renamed public skill entry points from `local-model-*` to `contextsmith-*`:
  `contextsmith-prompt-engineer`, `contextsmith-skill-engineer`, `contextsmith-skill-migrator`, `contextsmith-instruction-engineer`, `contextsmith-agent-evaluator`, and `contextsmith-run`.
- Added `contextsmith` as a top-level router skill for package discovery and intent-based dispatch.
- Updated README, Quick Start, Which Skill guidance, package spec, release docs, scripts, manifests, and live design notes for the new naming convention.
- Bumped all skill versions and reference manifests to 1.7.0.
- Clarified that ContextSmith remains local/open-weight first while the methodology also applies to frontier-model agent workflows.

### Breaking

- Existing `/local-model-*` invocations are replaced by `/contextsmith-*` invocations. Installations should use the renamed skill packages.

## v1.6.1

**Released:** 2026-06-01

### Fixed

- Reverted prose threshold in `shared/phased-planning.md` from `{{CONTEXT_BUDGET}}` back to `64k` — the YAML template variable at line 27 is the configurable parameter; the prose at line 105 is a meaningful boundary value, not a budget setting.
- Moved "Downstream Prompt Requirements" section from `shared/targeted-context-length.md` to `shared/persistent-task-state.md` where it belongs semantically. Updated `skills/contextsmith-prompt-engineer/SKILL.md` reference anchor accordingly.

### Changed

- Bumped all skill versions to 1.6.1.

### Notes

- This patch resolves two post-release audit findings: a circular comparison in phased-planning.md and misplaced task-state requirements in targeted-context-length.md.

## v1.6.0

**Released:** 2026-06-01

### Added

- Added `contextsmith-run`, a parameter-enforced run executor for prompts, prompt files, `NEXT_PROMPT.md` handoffs, and `.agent_work/.../tasks/<task>/` folders.
- Added run modes for `single`, `single-with-state`, `phase`, `phased-run`, `dry-run`, and `audit-only`, allowing the same skill to handle lightweight one-shot prompts and durable phased implementation plans.
- Added `--interaction refine` support with bounded multiple-choice questions, recommended defaults, question budgets, and concrete answer-to-parameter mapping so users can guide execution before the model assumes architecture, stack, source quality, tone, output format, or validation strategy.
- Added domain-specific refinement, validation, self-audit, and Ralph critique guidance for software engineering, frontend UX, data analytics, data science/ML, AI/ML engineering, research, writing/editing, business strategy, education/tutoring, ops/DevOps, legal/policy/compliance, and general tasks.
- Added execution-contract and evidence-ledger references so declared controls such as `--target-profile`, `--context-length`, `--validation`, `--ralph`, `--self-audit`, and `--interaction` become runtime obligations with auditable evidence.
- Added task-state execution guidance for reading `STATUS.md`, `NEXT_PROMPT.md`, current `PLAN.md` phase, and `CONTEXT.md`, then closing phases with compact state updates and refreshed handoffs.

### Changed

- Bumped all skill versions and reference manifests to 1.6.0.
- Updated README, Quick Start, Which Skill guidance, repo map, and living notes to include `contextsmith-run` as the sixth ContextSmith skill.
- Strengthened local-model execution guidance with one-screen contracts, one bounded unit at a time, selective reference loading, explicit stop conditions, validation-level semantics, and declared-vs-enforced completion checks.

## v1.5.1

**Released:** 2026-05-30

### Added

- Added `scripts/publish_release.sh` — create and publish GitHub releases with `gh` CLI. Uploads all dist/ artifacts (individual zips, bundle, SHA-256 checksums, RELEASE_SUMMARY.json), creates annotated git tag, and pushes to remote. Supports dry-run, custom release notes, and prerelease/draft flags.

### Changed

- Bumped all skill versions to 1.5.1.
- Strengthened phased planning and implementation-plan audit guidance with forecast-then-compact context contracts, tool-use forecasts, larger tool-heavy context reserves, fresh-session phase execution, and compaction triggers when tool output exceeds the phase forecast.
- Broadened context-budget executable phase budgets to cover all target ranges: 32k, 64k, 128k, and 256k.
- Added `.agent_work/` override in `AGENTS.md`: agent workflow artifacts (Superpowers specs, plans, etc.) belong under `.agent_work/`, not `docs/`.

## v1.5.0

**Released:** 2026-05-29

### Added

- Added `scripts/build_release.py` — release orchestrator that runs the full pipeline: sync references, update manifests, validate, optional version bump, package all skills, and generate `dist/RELEASE_SUMMARY.json`. CLI flags: `--package`, `--version`, `--dry-run`, `--dist-dir`, `--bundle`.
- Added `scripts/install_skill.sh` — install a single skill package from a zip file. Extracts to temp directory, verifies MANIFEST.json SHA-256 checksums, compares versions, backs up existing installation with timestamped rename, and copies to target. Default target: `~/.agents/skills/`.
- Added `scripts/install_all.sh` — batch install all skill packages from a dist directory. Delegates to `install_skill.sh` for each zip and prints a summary table.
- Added `scripts/test_release.sh` — end-to-end integration test with 74 assertions covering full pipeline, zip contents, SHA-256 checksums, bundle, installation, and idempotent re-install.
- Added `docs/RELEASE_PROCESS.md` — maintainer guide with prerequisites, step-by-step release checklist, verification commands, and troubleshooting.
- Added `--bundle` flag to `scripts/build_release.py` — creates `dist/contextsmith-all-bundle.zip` containing all 5 skills as a single download, with `.sha256` checksum.

### Changed

- Updated `scripts/sync_shared_refs.py` with `--update-manifests` flag to recompute and write back stale SHA-1 blob hashes in `reference_manifest.yml`.
- Updated `scripts/package_skill.sh` with pre-package validation gate, MANIFEST.json generation (SHA-256 per-file checksums), and `.sha256` zip-level checksum files.
- Updated `README.md` with a package-based installation section and copy-paste commands.
- Strengthened `contextsmith-prompt-engineer`, `contextsmith-instruction-engineer`, `contextsmith-skill-engineer`, `contextsmith-skill-migrator`, and `contextsmith-agent-evaluator` so long-running planning workflows require or audit a concrete task-state directory with `TASK.md`, `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `CONTEXT.md`, `CHECKLIST.md`, `ARTIFACTS.md`, `PHASE_LOG.md`, and `NEXT_PROMPT.md`, instead of allowing a single narrative plan file to stand in for persistent state. The guidance now distinguishes allowed planning artifacts from source-code edits, requires resumable `NEXT_PROMPT.md` handoffs, and reinforces compact state hygiene for paths, commands, validation results, decisions, constraints, and next actions.

### Notes

- This release completes the release tooling pipeline: sync, validate, package, bundle, install, test, and publish. The package can now be distributed as individual skill zips or a single all-skills bundle, with SHA-256 checksum verification at every step.

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

- Strengthened `contextsmith-prompt-engineer` with a prompt compiler boundary, non-execution self-check, and output contract reminder to reduce accidental execution of seed prompts.
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
  - `contextsmith-prompt-engineer`
  - `contextsmith-skill-engineer`
  - `contextsmith-skill-migrator`
  - `contextsmith-instruction-engineer`
  - `contextsmith-agent-evaluator`

- Introduced model-profile architecture.
  - Added profiles for `generic-local`, `qwen36`, `gemma4`, and `llama3`.
  - Moved model-specific reasoning/runtime guidance out of the central skill logic.
  - Kept the central rules model-agnostic: literal instructions, strict output contracts, progressive disclosure, no exposed CoT by default, context-risk management, validation, and atomicity for smaller models.
  - Preserved Qwen3.6 as an available/default profile when appropriate, while avoiding Qwen-only assumptions for Gemma, Llama, or unknown local models.

### contextsmith-prompt-engineer v1.3

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

### contextsmith-skill-engineer v1.3

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

### contextsmith-skill-migrator v1.1 baseline

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

### contextsmith-instruction-engineer v1.0

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

### contextsmith-agent-evaluator v1.0

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
