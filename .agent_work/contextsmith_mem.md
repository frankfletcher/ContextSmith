# ContextSmith Conversation Memory

_Last updated: 2026-05-23_

This file captures the current saved/compacted ContextSmith memory from this conversation so it can be reused outside ChatGPT.

---

## User / Project Context

- User: Frank Fletcher / @cogsci2.
- User is a data scientist and coding-agent power user.
- User is developing an open-source GitHub repo named **ContextSmith**.
- ContextSmith is a local/open-weight model agent engineering toolkit.
- The package emphasizes practical reliability for small/local models, especially Qwen3.6-27B, while remaining useful for broader model-aware agent workflows.
- User prefers constructive critique and wants ideas challenged kindly.
- User prefers practical, low-friction tools with high benefit.
- User prefers durable project-local output under `.agent-work/`.
- User wants to avoid “vibecoding artifacts” in public repos.
- User wants docs to be catchy, informative, honest, warm, and practical without sounding like generic AI marketing copy.

---

## Critical Naming / Editorial Rule

Do **not** use the term `ProWritingAid` anywhere in the ContextSmith package.

This applies to:

- README
- package docs
- skills
- shared references
- per-skill references
- changelog
- generated artifacts
- examples
- documentation-quality guidance

The project may borrow general writing-review ideas such as readability, repeated phrasing, tone, style, sentence variety, and documentation review, but must describe them generically.

Use terms such as:

- documentation-quality audit
- writing-quality audit
- readability and style review
- editorial review checklist
- technical documentation review

---

## Core ContextSmith Positioning

ContextSmith is **model-aware agent instruction engineering**.

It started with small local models, where instruction quality matters most, but the same discipline improves larger-model agent workflows too.

Preferred positioning:

- ContextSmith helps create agent instructions that remain usable under context pressure, tool failures, long coding runs, and real project constraints.
- ContextSmith turns messy agent instructions into model-aware operating plans that local and smaller models can actually follow.
- A bigger context window is not a strategy.
- ContextSmith optimizes for the context you actually have, not the context the model card promised.
- Strong models can write the plan. Smaller models can execute it — if the plan is atomic enough.
- Passing validation is not the same as being good.
- ContextSmith can run bounded improvement loops and grade what still needs work.
- The best AGENTS.md files are concise operating instructions for this repo, this harness, this model, and this risk profile.
- Speed optimizations are optional. Stability is the baseline.
- The package is small-model-first, but the operational discipline applies across the model spectrum.
- Local agents fail in boring ways: they loop, forget context, write weak tests, overwrite files, and follow hallucinated requirements from upstream tools. ContextSmith is built to prevent those boring failures.
- ContextSmith scans, infers, explains, and asks for correction before doing important work.

Avoid implying that the user lacks capability. Prefer language about speed, ease, clarity, and getting real work started.

Avoid phrases like:

- lowers cognitive load
- reduces user confusion
- helps users who cannot remember flags
- prevents overwhelm

Prefer:

- makes the next step obvious
- keeps the workflow easy to follow
- lets you use the tool without memorizing every option
- keeps setup focused
- gives you a clean path into real work
- lets you start with a clear configuration and adjust only the parts that matter

---

## README / Documentation Voice

The docs should feel like:

> a practical open-source maintainer explaining lessons learned

They should not feel like:

- a marketing bot
- a strict agent instruction file
- a generated brochure
- an LLM-only artifact with no human editorial judgment

README direction:

- README = landing page / front door.
- `docs/` = project documentation.
- `shared/` = agent/skill references.
- `skills/*/references/` = standalone skill references.

Use:

- `Quick Start`

Avoid:

- `first success`
- `Start Small`

Reasoning:

- “First success” is useful internally but feels growth-hacky as a heading.
- “Start Small” sounds too diminutive for ambitious users with serious projects.
- Users may want to make real changes or tackle big projects; they still want a fast entry point.

Preferred README section sequence:

```markdown
## Why ContextSmith Exists
## What It Helps You Build
## Quick Start
## Common Workflows
## Control Phrases and Flags
## Documentation
## Project Status
```

Possible Quick Start intro:

```markdown
## Quick Start

The fastest way to understand ContextSmith is to run it on one real artifact.

Choose the path closest to what you are doing:

- Improve a prompt for a local/open-weight model.
- Create or refine an `AGENTS.md` file for a repo.
- Audit an implementation plan before handing it to a coding agent.
- Convert a `SKILL.md` for smaller/local models.
- Evaluate tests, prompts, skills, or repo instructions without changing files.

You can start with just three controls:

```bash
--mode guided --target-profile qwen36 --context-length 32k
```

Add more controls only when they matter.

```
For larger projects:

```markdown
## For Larger Projects

For large coding tasks, migrations, ports, or multi-file refactors, ContextSmith helps turn a broad objective into executable phases with durable task memory.

A strong model can create or audit the plan. A smaller local model can execute the phases — if each phase is atomic enough, context-aware enough, and validated before the next one begins.
```

---

## Avoid Overused GPT-Style Contrast

Avoid overusing contrast as a literary device. It can make the docs sound AI-generated.

Common patterns to watch:

- not just X, but Y
- not merely
- not only
- not about
- the goal is not
- the result is not
- X is not Y. It is Z.
- rather than
- instead

Do not ban contrast entirely. Use it when it clarifies a real misconception. Do not use it as the default way to create emphasis.

Example to rewrite:

```markdown
The goal is not just better prompts.
The goal is agent instructions that remain usable under context pressure, tool failures, long coding runs, and real project constraints.
```

Preferred:

```markdown
ContextSmith helps create agent instructions that remain usable under context pressure, tool failures, long coding runs, and real project constraints.
```

Borderline acceptable if used sparingly:

```markdown
The result is not just a prettier prompt. It is a more reliable agent workflow.
```

---

## Imperative vs Suggestive Language

Use different tone by artifact type.

User docs:

- warmer
- explanatory
- practical
- suggestive when appropriate

Agent references:

- imperative
- precise
- operational
- constraint-driven

Example runtime stability rewrite:

Avoid:

```markdown
Do not change every knob at once.
```

Prefer:

```markdown
When adjusting parameters for stability, treat it like an experiment. We suggest changing one knob at a time so you can tell what helped.
```

For AGENTS.md / agent references, imperative rules are still appropriate:

```markdown
Do not run destructive Git commands without explicit user approval.
```

---

## Documentation Structure Preference

Current preferred docs architecture:

```text
docs/
├── QUICKSTART.md
├── WHICH_SKILL.md
├── USER_GUIDE.md
├── CONTROL_PARAMETERS.md
├── FAQ.md
├── EXAMPLES.md
├── workflows/
│   ├── prompt-engineering.md
│   ├── agents-md.md
│   ├── skill-engineering.md
│   ├── skill-migration.md
│   ├── implementation-plan-audit.md
│   ├── test-quality-audit.md
│   ├── small-context-coding.md
│   ├── planner-executor.md
│   └── runtime-stability.md
├── concepts/
│   ├── targeted-context-length.md
│   ├── model-profiles.md
│   ├── ralph-loop.md
│   ├── persistent-task-state.md
│   ├── phase-compression.md
│   └── skill-interoperability.md
├── reference/
│   ├── flags.md
│   ├── skill-list.md
│   ├── metadata.md
│   └── versioning.md
└── contributing/
    ├── documentation-style.md
    └── documentation-review-checklist.md
```

Use docs categories:

- project documentation
- user guides
- workflow guides
- concepts
- reference
- contributing

Avoid:

- human-facing docs

---

## Documentation Quality Audit

ContextSmith should include generic documentation-quality review ideas for both:

1. Generated artifacts.
2. ContextSmith’s own README/docs.

Checks:

- readability
- clarity
- sentence variety
- repeated sentence openings
- overused phrases
- overused contrast constructions
- jargon density
- tone
- specificity
- actionability
- example quality
- truthfulness / factual claims
- user empathy
- time-to-usefulness / clear next step
- whether examples help the reader choose, run, review, or troubleshoot

Artifact-specific style:

| Artifact                | Style                               |
| ----------------------- | ----------------------------------- |
| README / user docs      | warm, practical, explanatory        |
| AGENTS.md               | concise, operational, repo-specific |
| SKILL.md                | imperative, precise, low ambiguity  |
| shared agent references | compact, checklist-driven           |
| educational reports     | explanatory and user-teaching       |
| changelog               | factual, scannable, restrained      |

Add / maintain:

```text
shared/documentation-quality.md
docs/contributing/documentation-style.md
docs/contributing/documentation-review-checklist.md
```

Evaluator should support:

```bash
--focus documentation-quality
```

---

## Run Configuration Preview / Parameter Review Gate

ContextSmith should support a **Run Configuration Preview** / **Parameter Review Gate**.

Purpose:

- Keep the parameter system rich without making users memorize every flag.
- Let skills infer a configuration, explain why, and let the user correct it before important work.
- Make ContextSmith feel transparent and professional.

Use for:

- guided mode
- review-gate mode
- deep mode when important parameters were inferred
- high-impact tasks
- AGENTS.md generation/refinement
- batch migration
- long-running or side-effectful work

Skip or keep brief for:

- fast mode
- yolo mode
- trivial audit-only runs

Supported flags / natural language:

```bash
--review-config
--preview-config
--no-review-config
```

Natural language equivalents:

- show me the run configuration before proceeding
- skip the parameter preview

Preview should include:

- inferred project context
- likely user intent
- target artifact
- risk level
- existing instruction files found
- parameters with brief explanations
- planned approach
- low-confidence assumptions
- proceed/change prompt

For metadata/internal language:

- User-facing flag can be `--context-length 32k`.
- Internal/generated metadata should use `targeted_context_length: "32k"` and `context_tier: tight`.

---

## Core Skills

Keep separate descriptive skill names; ContextSmith is the package/repo brand.

Current core skills:

1. `local-model-prompt-engineer`
   
   - Creates, improves, audits, and packages prompts for local/open-weight models and broader model capability tiers.

2. `local-model-skill-engineer`
   
   - Creates, converts, improves, audits, and packages `SKILL.md`-based skills while preserving source behavior and adapting for local/smaller models or selected profiles.

3. `local-model-skill-migrator`
   
   - Recursively audits, stages, and migrates skill directories safely with backups, staging, manifests, reports, and apply-after-approval.

4. `local-model-instruction-engineer`
   
   - Creates, optimizes, and audits AGENTS.md and equivalent repo/agent instruction files.
   - Should default to guided/human-in-loop for AGENTS.md because it is high-impact.

5. `local-model-agent-evaluator`
   
   - Audit-only diagnosis for prompts, skills, AGENTS.md, implementation plans, tests, runtime setups, and documentation quality.

Possible future skills:

- `local-model-agent-profile-builder`
- `agent-task-state-manager`
- `local-model-agent-harness-adapter`
- package validator / sync script / release builder
- optional tiny router skill if users struggle to choose

Do not collapse all skills into one mega-skill unless a harness supports true subskill lazy-loading.

---

## Package Layout

Preferred Option:

- Canonical shared references in `shared/`.
- Copied per-skill references in each `skills/<skill>/references/` for standalone installation.

Potential repo layout:

```text
ContextSmith/
├── README.md
├── PACKAGE_SPEC.md
├── CHANGELOG.md
├── LOCAL_MODEL_AGENT_ENGINEERING_LIVING_NOTES.md
├── docs/
├── scripts/
├── shared/
└── skills/
    ├── local-model-prompt-engineer/
    ├── local-model-skill-engineer/
    ├── local-model-skill-migrator/
    ├── local-model-instruction-engineer/
    └── local-model-agent-evaluator/
```

Need maintainability helpers:

- `scripts/sync_shared_refs.py`
- `scripts/validate_skills.py`
- release builder
- package validator
- changelog discipline

---

## Versioning and Changelog

Use SemVer going forward:

- `MAJOR.MINOR.PATCH`
- Patch = docs/refinements/non-breaking fixes.
- Minor = backward-compatible capabilities.
- Major = breaking changes.

Changelog style:

```markdown
## vX.Y.Z

**Released:** YYYY-MM-DD

### Added
- ...

### Changed
- ...

### Fixed
- ...

### Notes
- ...
```

Backfill dates for older versions when editing changelog.

---

## Recent Package Evolution

### v1.4.0

Added advanced workflow guidance:

- implementation-plan audit
- small-context workflows
- test-quality audit
- phase code review
- model capability tiers
- planner/executor workflows
- runtime stability notes
- education levels
- artifact verbosity
- phase review
- code-review iterations
- target capability
- planner/executor profiles
- evaluator focus flags
- VERSIONING.md

Commit message:

Brief:

```text
feat: add advanced ContextSmith workflow guidance
```

Long:

```text
feat: add advanced ContextSmith workflow guidance

Add major workflow and evaluation capabilities across the package:

- Add implementation plan auditing guidance.
- Add small-context workflow documentation.
- Add test-quality audit guidance.
- Add phase code review workflow.
- Add model capability tiers.
- Add planner/executor workflow guidance.
- Add runtime stability guidance for local agent runs.
- Add education-level and artifact-verbosity controls.
- Add SemVer-based versioning policy.
- Expand control parameters for phase review, code review iterations,
  target capabilities, planner/executor profiles, and evaluator focus.
- Update skills to reference the new audit, review, runtime, and
  model-capability guidance.
- Refresh README, changelog, and living notes for the new capabilities.
```

### v1.4.1

Documentation/onboarding focused:

- README rewritten as project front door.
- Deeper docs split into docs such as QUICKSTART, WHICH_SKILL, FAQ, USER_GUIDE, CONTROL_PARAMETERS, EXAMPLES, AGENTS_MD_GUIDE, SMALL_CONTEXT_WORKFLOWS, IMPLEMENTATION_PLAN_AUDIT, TEST_QUALITY_AUDIT, PHASE_CODE_REVIEW, RUNTIME_STABILITY, MODEL_PROFILES, and SKILL_MIGRATION.

Commit message:

Brief:

```text
docs: improve onboarding and split user docs
```

Long:

```text
docs: improve onboarding and split user docs

Rework ContextSmith documentation to make the project easier to understand
and use:

- Rewrite README as a clearer project front door.
- Add a Quick Start path with practical examples.
- Add user-oriented docs for choosing skills, control parameters, examples,
  AGENTS.md guidance, small-context workflows, implementation plan audits,
  test-quality audits, phase code reviews, runtime stability, model profiles,
  and skill migration.
- Split deeper documentation into dedicated docs files instead of overloading
  the README.
- Clarify the difference between project documentation and agent-facing
  shared references.
- Update package spec, changelog, and living notes.
- Preserve existing skill behavior while improving documentation structure.
```

### v1.4.2

Added documentation quality/style system:

- `shared/documentation-quality.md`
- `shared/run-configuration-preview.md`
- `docs/contributing/documentation-style.md`
- `docs/contributing/documentation-review-checklist.md`
- docs organized into `docs/workflows/`, `docs/concepts/`, `docs/reference/`, and `docs/contributing/`
- evaluator support for `--focus documentation-quality`
- config preview/review flags
- stricter language-quality guidance
- README tone updates
- control parameter updates

Commit message:

Brief:

```text
docs: add documentation quality review and config previews
```

Long:

```text
docs: add documentation quality review and config previews

Add a documentation-quality and style-system pass across ContextSmith:

- Add documentation quality guidance for readability, tone, repeated phrasing,
  factuality, examples, and usefulness.
- Add run configuration preview guidance so skills can explain inferred
  parameters before important work.
- Add documentation style and review checklist docs.
- Reorganize docs into workflow, concept, reference, and contributing areas.
- Update README tone and structure to sound more practical and less generic.
- Replace awkward documentation labels with clearer project-documentation
  language.
- Update skills to reference configuration previews and documentation-quality
  checks.
- Add evaluator support for documentation-quality review focus.
- Update control parameters for review/preview configuration behavior.
- Update changelog and living notes.
- Verify the package avoids disallowed writing-assistant product naming.
```

---

## Metadata / Artifact Marking

Use `metadata.version` in `SKILL.md` frontmatter when versioned.

Generated / engineered artifacts should mark:

- `engineered_by`
- `engineered_version`
- `target_model_profiles`
- `target_model_capability`
- `targeted_context_length`
- `context_tier`
- optimization scope
- source skill name/hash when converting, if available

Avoid arbitrary top-level frontmatter keys that trigger unknown-key warnings. Use `metadata` or a compact body section when needed.

Important:

- Use `targeted_context_length`, not `usable_context_length`.
- It should not be nominal; it must materially change outputs.

---

## Core Controls / Parameters

Support both natural language controls and CLI-style flags.

Key natural-language controls:

- fast path
- deep path
- guided mode
- yolo mode
- review-gate mode
- audit only
- stage only
- apply
- no ralph loop
- ralph loop: N
- target profile: qwen36/gemma4/llama3/generic-local
- target capability: small-local/mid-local/large-local/frontier-cloud/reasoning-specialized/coding-specialized/multimodal/generic-agent
- planner profile: frontier-cloud
- executor profile: qwen36
- context length: 32k
- targeted context length: 32k
- ctx: 32k
- runtime context: 32k
- domain: coding,data-science-ml,frontend,research,email,document-processing,...
- harness: opencode,codex,cursor,aider,generic-agent,...
- project-local output
- chat-only output
- backup first
- do not apply

Key flags:

```bash
--mode fast|deep|guided|yolo|review-gate|audit-only
--target-profile qwen36|gemma4|llama3|generic-local
--context-length 32k|64k|100k|128k
--domain ...
--harness ...
--ralph 0|1|2|3
--output chat|project-local|staging
--stage
--apply
--backup
--no-apply
--no-ralph
--help
--examples
--modes
--parameters
--quickstart
--education-level none|brief|guided|deep|teaching
--artifact-verbosity compact|normal|detailed
--phase-review off|brief|standard|deep
--code-review-iterations 0|1|2
--target-capability small-local|mid-local|large-local|frontier-cloud|reasoning-specialized|coding-specialized|multimodal
--planner-profile ...
--executor-profile ...
--focus implementation-plan|test-quality|runtime-stability|agents-md|prompt|skill|documentation-quality
--review-config
--preview-config
--no-review-config
```

Help mode:

Every skill should support help, describe, examples, modes, parameters, quickstart, and flag equivalents. Help mode should return usage guidance only and not start normal workflow.

---

## Interaction Modes

Human-in-loop modes:

- `yolo`: proceed with assumptions unless blocked.
- `guided`: ask 1–3 high-impact questions before major changes.
- `review-gate`: stage/plan first, require approval before applying.
- `audit-only`: analyze and report only.
- `stage` / `apply`: staging/apply workflow.

Defaults:

- Prompt improvement: yolo/fast or guided depending importance.
- Reusable prompts/skills: guided.
- AGENTS.md / instruction engineer: guided by default.
- Batch migration: review-gate/stage only by default.
- High-side-effect domains: review-gate.

Clarification / assumption policy:

- Ask only when missing info materially changes target model/profile, source files/paths, output format, permission boundaries, side effects, safety/privacy, validation criteria, or context strategy.
- Otherwise proceed with explicit assumptions.
- Cap questions at 1–3 concise questions in one message.
- Categorize assumptions by severity when useful: safe/material/risky/blocked.

---

## Education Level and Artifact Verbosity

Add controls:

```bash
--education-level none|brief|guided|deep|teaching
--artifact-verbosity compact|normal|detailed
```

Separate:

- `education-level` = how much to teach the user in reports.
- `artifact-verbosity` = how verbose the generated model-facing artifact should be.

Tight context should keep artifacts compact even when education-level is deep/teaching. Put educational detail in separate reports.

Default:

- `education-level: brief`
- `artifact-verbosity` determined by `targeted_context_length`.

---

## Model Profiles and Capability Tiers

Original small-model focus:

- Qwen3.6-27B as primary target.
- Generalize to local/open-weight models.

Profiles:

- `qwen36`
- `gemma4`
- `llama3`
- `generic-local`

Model capability tiers:

- `small-local`
- `mid-local`
- `large-local`
- `frontier-cloud`
- `reasoning-specialized`
- `coding-specialized`
- `multimodal`
- `generic-agent`

Planner/executor workflow:

- Stronger models can create plans, audit plans, clarify requirements, design architecture, define test strategy, and do final review.
- Smaller/local models can execute atomic phases, make targeted edits, run validation, and update docs.

Specific notes:

### Qwen3.6

- No exposed chain-of-thought in prompt text.
- Avoid `/think` and `/no_think` assumptions unless runtime supports them.
- Thinking/non-thinking controls belong in runtime/deployment guidance, not core skill behavior unless output is a runtime config.

### Gemma4

- Supports thinking mode, but Gemma-specific controls differ.
- Do not store/replay thinking content in conversation history, task state, subagent reports, or resume prompts.
- Multimodal ordering may matter in some runtimes.

### Unknown model

- Use `generic-local`.
- Avoid model-specific runtime claims.

---

## targeted_context_length and Context Tiers

`targeted_context_length` must materially affect outputs.

Context tiers:

- Tiny ≤16k
- Tight >16k and ≤32k
- Moderate >32k and ≤64k
- Large >64k and ≤128k
- Very large >128k

For `targeted_context_length <= 32k`:

- Prefer many small phases.
- One subsystem/behavior per phase.
- 3–7 active files max.
- Explicit stop conditions.
- Narrow validation.
- Phase debrief.
- Do-not-carry-forward notes.
- One phase per session or compaction between phases.
- Shorter prompts.
- Fewer examples.
- Stronger task state.
- Smaller migration batches.
- More selective reading.

---

## Persistent Task State

For long-running/multi-file/crash-sensitive tasks, use durable state under project-local `.agent-work/`, not `/tmp`.

Canonical output priority:

1. User-specified output dir wins.
2. Project/repo task → `<project>/.agent-work/sprints/<sprint-or-subproject>/tasks/<YYYY-MM-DD-short-slug>/`
3. Installed skill migration → `~/.agents/skill-migrations/<migration-id>/`
4. Non-project → `~/.agent-work/tasks/<YYYY-MM-DD-short-slug>/`
5. `/tmp` only for disposable scratch.

Suggested task state:

```text
.agent-work/
└── sprints/<sprint-or-subproject>/tasks/<YYYY-MM-DD-short-slug>/
    ├── TASK.md
    ├── PLAN.md
    ├── STATUS.md
    ├── DECISIONS.md
    ├── CONTEXT.md
    ├── CHECKLIST.md
    ├── ARTIFACTS.md
    ├── PHASE_LOG.md
    ├── NEXT_PROMPT.md
    ├── iterations/
    └── reports/
```

Keep state files short and current.

---

## Implementation Plan Audit

Implementation plan auditor should grade A–F for:

- phase granularity
- atomicity
- dependency ordering
- context fit
- testability
- task-state integration
- rollback/recovery
- validation strength
- small-model executability
- handoff quality

Strong planner/local executor workflow:

1. Use stronger model/ContextSmith deep path to create plan.
2. Audit plan for small-model executability.
3. Split into atomic phases.
4. Save state under `.agent-work`.
5. Execute one phase per local-model session if context is tight.
6. End each phase with debrief and `NEXT_PROMPT.md`.
7. Start next session from state, not full original chat.

---

## Phase Code Review

At the end of each coding phase:

- Inspect phase diff.
- Review only files changed this phase unless broader inspection is required.
- Check correctness, edge cases, tests, regressions, simplicity, maintainability, security/secrets, performance, typing/lint/style, and project conventions.
- Classify issues as must fix, should fix, note for later, or acceptable tradeoff.
- Apply at most one focused improvement pass unless user requests deeper.
- Re-run narrowest validation.
- Record review in `PHASE_LOG.md` or `reports/phase-XX-code-review.md`.

Parameters:

```bash
--phase-review off|brief|standard|deep
--code-review-iterations 0|1|2
```

---

## Test Quality Audit

Key principle:

> Tests are not useful because they pass. Tests are useful because they would fail when important behavior breaks.

Audit dimensions:

- baseline use-case coverage
- edge-case realism
- failure modes
- regression relevance
- assertion strength
- coverage of changed behavior/branches
- fixture/data realism
- isolation/flakiness
- maintainability
- over-mocking risk

Evaluator should support:

```bash
--focus test-quality
```

---

## Runtime Stability for Local Agentic Coding

Runtime stability guidance should be diagnostic/user guidance, not core skill behavior.

For Qwen3.6 + llama.cpp/BeeLlama/OpenCoder:

- Treat speed optimizations like DFlash/speculative decoding, aggressive KV compression, large context, preserved thinking, and reasoning budget as variables to A/B test.
- Keep a known-stable baseline.
- Change one knob at a time when possible.
- Speed optimizations are optional; stability is baseline.
- For user’s RTX 3090, stable no-spec q4_0/q4_0 baseline is valuable.
- DFlash + turbo cache + 128k + preserve thinking may cause loops.
- Prefer stable moderate context with task state for serious long runs.

---

## Loop Safety

Agentic loop safety for small/local tool-using agents:

- Harness-aware tool-call discipline.
- No identical consecutive tool calls.
- If command/patch/edit has same error/same output/no progress twice, stop repeating.
- Retry budget: max 1 retry per failing action, 2 related attempts per strategy, 3 recovery attempts before asking.
- Next action must change target, command, args, working dir, input, strategy, or validation.
- No-op edit detection.
- Same-output detection.
- Anti-brainstorming: max 3 options, then choose and act.
- Planning-loop guard: don’t rewrite plan repeatedly unless new evidence.

Escalation strings:

- `BREAK_LOOP_AWAITING_HUMAN_INPUT`
- `BLOCKED_GIT_STATE_REQUIRES_HUMAN_INPUT`
- `BLOCKED_MISSING_CONTEXT`
- `BLOCKED_TOOL_UNAVAILABLE`
- `BLOCKED_PERMISSION_REQUIRED`
- `BLOCKED_VALIDATION_UNAVAILABLE`

---

## Git Safety

Before editing in coding harnesses:

```bash
git status --short
```

Do not overwrite user changes.

Do not run unless user asks:

- `git add`
- `git commit`
- `git push`

Forbidden without explicit approval:

- `git reset --hard`
- `git clean -fd`
- `git clean -fdx`
- `git checkout -- .`
- `git restore .`
- `git restore --staged .`
- `git rebase`
- `git rebase --continue`
- `git rebase --abort`
- `git merge --abort`
- `git push --force`
- `git push --force-with-lease`
- deleting branches
- amending/squashing/rewriting commits
- discarding uncommitted changes
- removing files outside scope

---

## AGENTS.md / Instruction Engineer

AGENTS.md is a high-impact backbone for coding-agent projects.

`local-model-instruction-engineer` should default to guided/human-in-loop for AGENTS.md creation/refinement.

It should:

- scan repo first
- detect language/framework/domain/harness
- scan existing instruction files
- detect → reuse → strengthen → consolidate → add only missing safeguards
- avoid duplicate/token-bloating rules
- present menu of recommended instruction blocks
- add nested AGENTS.md only when subprojects differ materially
- avoid generic manifestos

Recommended blocks:

- core workflow
- loop safety
- Git safety
- coding standards
- Python PEP 8
- DS/ML leakage prevention
- testing
- docs
- `.agent-work`

---

## Upstream Artifact / Skill Interoperability

When other skills/optimizers generated prompts/specs/plans:

- Treat external skill contributions as inputs to verify, not authoritative truth.
- Run upstream artifact audit.
- Unsupported requirements should be rejected/called out.
- Preserve valid domain-specific artifacts if supported.

Classify additions:

- confirmed requirement
- likely requirement
- useful suggestion
- unsupported addition
- conflicting requirement
- rejected requirement

Instruction precedence:

1. User’s current explicit request
2. Safety/privacy/permission/destructive boundaries
3. Actual project/repo/source evidence
4. Existing repo instructions
5. Target model/profile constraints
6. Domain-specific requirements
7. External skill artifacts/specs
8. Optional style preferences
9. Generic best practices

---

## Recent Generated Artifacts

Recent artifacts generated in the conversation included:

- `ContextSmith-package-v1.4.0.zip`
- `ContextSmith-package-v1.4.1.zip`
- `ContextSmith-package-v1.4.2.zip`
- docs-only zips for v1.4.1 and v1.4.2
- individual skill packages for v1.4.2
- README / CHANGELOG / living notes files for v1.4.0, v1.4.1, v1.4.2

Latest package state: **ContextSmith v1.4.2**.

Latest known skill versions in v1.4.2 validation output:

```text
OK local-model-prompt-engineer: 207 lines, version=1.7.1
OK local-model-skill-engineer: 173 lines, version=1.7.1
OK local-model-skill-migrator: 171 lines, version=1.5.1
OK local-model-instruction-engineer: 198 lines, version=1.4.1
OK local-model-agent-evaluator: 120 lines, version=1.4.1
```
