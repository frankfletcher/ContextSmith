# Instruction Propagation System — Design & Implementation Brief

> **Purpose:** This document captures the full design, decisions, and implementation plan for making ContextSmith-generated artifacts (prompts, skills, instructions) parameter-aware and reference-propagating. It is intended as input to `local-model-prompt-engineer` to generate an atomic, small-model-friendly implementation plan with phased execution.

---

## Problem Statement

ContextSmith skills (prompt-engineer, skill-engineer, instruction-engineer) have deep knowledge of:
- A 37-parameter control system (`shared/control-parameters.md`)
- 49 canonical behavioral references (`shared/`) covering phased planning, self-audit, test quality, loop safety, etc.

When these skills generate artifacts (prompts, implementation plans, next prompts), that knowledge does NOT propagate to the generated output. The generated prompt is unaware of:
1. Which parameters were active during its creation
2. Which behavioral references apply to its execution
3. How to chain those parameters/references to downstream artifacts it generates (e.g., a prompt generating an implementation plan, which generates phase prompts)

**Current inheritance rule (one sentence in SKILL.md):** "All generated artifacts MUST preserve this parameter system." — no mechanism, no format, no enforcement.

---

## Design Decisions

### D1: Manifest-Based Inheritance (Chosen Over Alternatives)

| Approach | Description | Why Rejected/Chosen |
|----------|-------------|---------------------|
| A: Parameter Block Injection | Embed only active params as parseable blocks | Too light — doesn't propagate behavioral knowledge |
| B: Embedded Behavioral Contracts | Condense reference requirements into generated prompts | Good, but standalone-only; no upgrade path when ContextSmith is installed downstream |
| C: Parameterized Templates | Make references themselves parameterized templates | Overly heavy; requires template engine, breaks existing refs |
| **D: Manifest-Based Inheritance** | Artifacts carry a manifest of applied references + params + condensed contracts. Downstream agents with ContextSmith resolve to full refs; standalone agents use embedded contracts. | **Chosen.** Best of both worlds: portable AND upgradable. |

### D2: ATX Heading Section Placement (Not YAML Frontmatter)

The artifact manifest lives as an ATX heading section (`## Artifact Manifest`) at the top of generated artifacts, not as YAML frontmatter. Reasons:
- Works in all markdown renderers and agent parsers
- Easy for small models to read and generate
- No delimiter ambiguity with SKILL.md-style `---` fences

### D3: Pre-Extracted Behavioral Contracts + Skill Can Append

Behavioral contracts (condensed requirements from each reference) are pre-extracted into a canonical file. Skills copy the relevant contracts rather than generating them on-the-fly. Reasons:
- Consistent across runs and artifacts
- Auditable — can diff contract changes
- No generation variance in critical instructions
- Skills MAY append artifact-specific custom contracts

### D4: Full Chain Propagation with Param Provenance

Every downstream artifact inherits from its parent. Children can inherit, narrow, or add — but NOT widen without justification. Each parameter tracks its source: `user-set | inherited | default | narrowed`.

---

## Current System State (Research Findings)

### Parameter System

**Definition:** `shared/control-parameters.md` (156 lines)

**Parsing rules:** Parse CLI flags first, user prose overrides flags on conflict, normalize aliases, record parsed controls in output.

**Common flags (37 total):**
```bash
--mode fast|deep|guided|yolo|review-gate|audit-only
--target-profile qwen36|gemma4|llama3|generic-local
--context-length 32k|64k|100k|128k|256k
--domain coding,data-science-ml,frontend,research,email,document-processing
--harness opencode,codex,cursor,aider,openclaw,hermes,generic-agent
--ralph 0|1|2|3  --no-ralph
--output chat|project-local|staging
--education-level none|brief|guided|deep|teaching
--artifact-verbosity compact|normal|detailed
--phase-review off|brief|standard|deep
--code-review-iterations 0|1|2
--target-capability small-local|mid-local|large-local|frontier-cloud|reasoning-specialized|coding-specialized|multimodal
--planner-profile <model/profile name>
--executor-profile <model/profile name>
--focus implementation-plan|test-quality|runtime-stability|agents-md|prompt|skill
```

**Skill-specific flags:** Each of the 5 skills has additional flags (e.g., `--prompt-file` for prompt-engineer, `--skills-dir` for migrator).

**Current defaults in generated artifacts (6 params only):**
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--mode` | `guided` | Interaction mode |
| `--target-profile` | `qwen36` | Target model profile |
| `--context-length` | `64k` | Targeted context window |
| `--education_level` | `deep` | Explanation depth |
| `--ralph` | `2` | Ralph loop iterations |
| `--harness` | `opencode` | Execution environment |

**Gap:** Only 6 of 37 params are in defaults. No provenance tracking. No format for generated artifacts to carry params forward.

### Reference System

**Canonical source:** `shared/` (49 files total: 37 top-level + 8 domain profiles + 4 model profiles)

**Key references by category:**

| Category | Files | Purpose |
|----------|-------|---------|
| Planning | `phased-planning.md`, `implementation-plan-audit.md` | Phase structure, granularity rules, A-F audit rubric |
| Execution | `persistent-task-state.md`, `phase-compression.md` | Task state files, debrief format, carry-forward/do-not-carry-forward |
| Verification | `test-quality-audit.md`, `phase-code-review.md` | Test quality rubric, post-phase code review gates |
| Safety | `loop-safety.md`, `git-safety.md`, `side-effect-matrix.md` | Loop prevention, git boundaries, risk classification |
| Context | `context-management.md`, `targeted-context-length.md`, `small-context-workflows.md` | Context budget strategies, tight context patterns |
| Model | `model-capability-tiers.md`, `planner-executor-workflows.md` | Capability tiers, planner vs executor model selection |
| Quality | `evaluation-rubrics.md`, `ralph-loop.md`, `small-model-atomicity.md` | A-F grading, bounded improvement loops, atomic instructions |
| Metadata | `engineering-metadata.md`, `output-location.md` | Artifact metadata schema, output file locations |
| Inheritance | `instruction-precedence.md`, `instruction-deduplication.md`, `reference-optimization.md` | Priority hierarchy (9 levels), dedup scan, reference classification |
| Interoperability | `skill-interoperability.md`, `upstream-artifact-audit.md` | Upstream artifact verification, workflow collision detection |

**Per-skill curated copies:** Each skill has a `references/` directory with independent copies of relevant shared refs. Prompt-engineer has ~57 files (largest), agent-evaluator has 70+ (superset).

### Current Artifact Generation

**Prompt Engineer outputs:**
- Prompt package (14-section template): Engineering Metadata, Assumptions, Target Model/Harness, Domain/Intent, Prompt-Control Feasibility, Context Strategy, Interaction Mode, System Prompt, User Prompt Template, Examples, Validation/Test Plan, Loop/Git/File Safety, Persistent Task State, Subagent Delegation, Runtime Recommendations, Educational Change Report
- Required report: Original Strengths/Weaknesses, Changes Made, Why Improved, A-F Grades, Remaining Risks, Files Written, Non-Execution Check

**Implementation plan phases (from `phased-planning.md`):** Each phase MUST include goal, inputs, likely files/directories, explicit tasks, testing/validation steps, unit/integration tests, outputs/artifacts, validation checks, stop condition, handoff notes.

**Phase closeout (12-step procedure):** Update STATUS.md, PLAN.md, DECISIONS.md, ARTIFACTS.md, PHASE_LOG.md; write carry-forward/do-not-carry-forward; update NEXT_PROMPT.md; run phase compression and update CONTEXT.md; run validation checks (block on failure); run implementation plan audit for next phase (block on failure); include test quality audit for coding work (block on failure); check stop condition.

**Persistent task state files (9 total):**
```
.agent_work/sprints/<sprint>/tasks/<YYYY-MM-DD-slug>/
├── TASK.md          # objective, scope, constraints, success criteria
├── PLAN.md           # phase checklist
├── STATUS.md         # current phase, completed work, in-progress, next action
├── DECISIONS.md      # durable decisions with reason and impact
├── CONTEXT.md        # file map, constraints, evidence notes, skip rules
├── CHECKLIST.md      # testable validation items
├── ARTIFACTS.md      # changed/generated files and commands run
├── PHASE_LOG.md      # one compact entry per phase
└── NEXT_PROMPT.md   # short resume prompt for session handoff
```

---

## Proposed Artifact Manifest Format

### Structure

Every generated artifact includes this block after the title, before any other content:

```markdown
# <Artifact Title>

## Artifact Manifest

**type:** prompt | implementation-plan | next-prompt | skill | instruction-file
**version:** 1.0
**chain-of:** root | <parent artifact id or file path>

### Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| `--mode` | guided | default |
| `--target-profile` | qwen36 | user-set |
| `--context-length` | 32k | narrowed from 64k (per-phase tight context) |
| `--ralph` | 2 | inherited |
| `--phase-review` | standard | inherited |
| `--education-level` | deep | default |
| `--harness` | opencode | default |

### References Applied

| Reference | Version | Contract Summary |
|-----------|---------|-----------------|
| `phased-planning` | 1.0 | Phase structure, granularity rules, 12-step closeout procedure |
| `implementation-plan-audit` | 1.0 | A-F pre-execution grading rubric, 10 audit questions |
| `test-quality-audit` | 1.0 | Test quality rubric, weak test smells, ML/LLM-specific checks |
| `loop-safety` | 1.0 | Agentic loop prevention: no repeated identical tool calls, retry budget of 3 |
| `persistent-task-state` | 1.0 | 9-file task state layout under `.agent_work/sprints/` |

### Behavioral Contracts (Standalone)

> Condensed requirements from above references. For agents without ContextSmith installed.

**Phase Structure:** Each phase MUST include: goal, inputs, likely files/directories, explicit tasks, testing/validation steps, unit and integration tests where relevant, outputs/artifacts, validation checks, stop condition, handoff notes.

**Phase Granularity:** Phase count must scale with complexity. Prefer 6-20 phases for large tasks. For `targeted_context_length <= 32k`, prefer more smaller phases. Each phase must fit within the context window.

**12-Step Phase Closeout:** (1) Update STATUS.md, (2) Check off PLAN.md items, (3) Record durable decisions in DECISIONS.md, (4) Record changed files/commands in ARTIFACTS.md, (5) Add compact notes to PHASE_LOG.md, (6) Write carry-forward and do-not-carry-forward notes, (7) Update NEXT_PROMPT.md, (8) Run phase compression and update CONTEXT.md for next phase, (9) Run validation checks — if any fail, set STATUS to "Blocked" and exit, (10) Run implementation plan audit for next phase — if fails, set STATUS to "Blocked" and exit, (11) Include test quality audit for coding work — if fails, set STATUS to "Blocked" and exit, (12) If stop condition met, set STATUS to "Completed" and exit.

**Implementation Plan Audit Gates:** Before executing each phase, grade the next-phase plan on: phase granularity, atomicity, context fit, validation strength, task-state integration, handoff quality, test strategy. Block on failure.

**Test Quality Requirements:** Tests must cover baseline use cases, realistic edge cases, failure modes (invalid input, missing data, bad state), and changed behavior. Assertions must be specific enough to catch wrong behavior. Avoid: tests that only check imports, tests that only check "no throw", mocking the method being tested, asserting on implementation details instead of user-visible behavior.

**Loop Safety Rules:** Do not execute identical consecutive tool calls. If same command/edit fails twice, stop and change strategy (correct/narrow/inspect/substitute/escalate). Maximum 1 retry per exact failing action, 2 related attempts per strategy, 3 total recovery attempts before requesting human input. After an edit, verify the file changed. Do not repeat no-op edits.

**Task State Hygiene:** Do not paste full files, logs, transcripts, or model reasoning into state files. Store summaries, paths, commands, evidence anchors, decisions, and validation results.

### Custom Contracts (Artifact-Specific)

> Additional requirements specific to this artifact's domain and purpose.

- <Skill may append custom contracts here based on domain, task type, user requirements>
```

### Source Values for Parameters

| Source | Meaning |
|--------|---------|
| `user-set` | Explicitly provided by the user in this session |
| `inherited` | Copied from parent artifact's manifest without modification |
| `default` | Set to the system default (from SKILL.md default table) |
| `narrowed` | Derived from a parent value but constrained for this artifact's scope (e.g., 64k → 32k per phase) |

---

## Chain Propagation Rules

### Inheritance Model

```
Root Prompt (params: mode=guided, context-length=64k, ralph=2)
  │
  ├─ Implementation Plan
  │   params: inherits all from root
  │   narrowed: context-length → 32k (per-phase budget)
  │   chain-of: "Root Prompt"
  │   references: adds implementation-plan-audit, test-quality-audit
  │   │
  │   ├─ Phase 1 NEXT_PROMPT.md
  │   │   params: inherits from plan
  │   │   added: --focus phase-1-specific
  │   │   chain-of: "Implementation Plan"
  │   │   references: inherits plan refs, adds loop-safety (if tool-using)
  │   │
  │   ├─ Phase 2 NEXT_PROMPT.md
  │   │   params: inherits from plan
  │   │   carry-forward: facts from Phase 1 debrief
  │   │   chain-of: "Implementation Plan"
  │   │
  │   └─ ... (each phase inherits from plan, carries forward from prior phase)
  │
  └─ Generated Skill (SKILL.md)
      params: inherits target-profile, harness from root
      added: skill-specific params (--reference-policy, --metadata)
      chain-of: "Root Prompt"
      references: adds skill-interoperability, upstream-artifact-audit
```

### Propagation Rules

1. **Inherit all:** Child starts with all parent parameters and references
2. **Narrow with justification:** Child may narrow a parameter (e.g., context-length 64k → 32k for tight-context phases) — must include reason in `source` column
3. **Add relevant refs:** Child may add references relevant to its specific scope
4. **Never widen without justification:** Child cannot increase context-length, relax safety, or remove references from parent unless explicitly justified with a documented reason
5. **Chain tracking:** Every artifact records its `chain-of` parent for provenance

### Artifact Type → Default References Matrix

| Artifact Type | Always Includes | Conditionally Adds |
|---------------|-----------------|-------------------|
| Prompt (general) | control-parameters, loop-safety | domain-profile (if domain known), targeted-context-length (if ctx provided) |
| Implementation Plan | phased-planning, implementation-plan-audit, persistent-task-state, phase-compression | test-quality-audit (if coding), phase-code-review (if --phase-review on) |
| NEXT_PROMPT.md | persistent-task-state, loop-safety, phase-compression | All parent plan refs (inherited) |
| Generated Skill | control-parameters, loop-safety, skill-interoperability | upstream-artifact-audit (if migrating), reference-optimization |
| Instruction File (AGENTS.md) | instruction-deduplication, instruction-precedence, loop-safety, git-safety | domain-profiles (per domain), coding-standards (if coding domain) |

---

## Implementation Plan Overview

### Phase 1: Shared Infrastructure (New Files in `shared/`)

#### 1A: Create `shared/artifact-manifest.md`

Canonical specification for the artifact manifest system. Must include:
- Manifest format specification (as designed above)
- ATX heading placement rules
- Parameter source values table (`user-set | inherited | default | narrowed`)
- Chain propagation rules (inherit, narrow, add, never widen without justification)
- Artifact type → default references matrix
- Example manifests for each artifact type: prompt, implementation plan, next-prompt, skill, instruction file
- Validation checklist: how to verify a manifest is correct

#### 1B: Create `shared/behavioral-contracts.md`

Pre-extracted contract summaries for each of the ~30 most relevant references. Each entry must be self-contained, 3-7 lines max, capturing only actionable requirements (not background or rationale). The contracts are what get embedded in generated artifacts' "Behavioral Contracts" section.

**Contract entries needed (derived from current shared/ refs):**

| Reference | Contract Summary (to pre-extract) |
|-----------|----------------------------------|
| `phased-planning` | Phase structure requirements (10 fields per phase), granularity rule (6-20 phases for large tasks, scale with context budget), 12-step closeout procedure |
| `implementation-plan-audit` | A-F rubric categories (phase granularity, atomicity, dependency ordering, context fit, validation strength, task-state integration, handoff quality, rollback/recovery, test strategy, small-model readiness), 10 audit questions, output format with recommendation + must-fix |
| `test-quality-audit` | A-F rubric (baseline coverage, edge-case realism, failure-mode coverage, assertion strength, regression-catching power, changed-behavior coverage, fixture realism, isolation/determinism, over-mocking risk, maintainability), weak test smells list, ML/LLM-specific checks |
| `loop-safety` | No identical consecutive tool calls. Same action failing twice = stop and change strategy. Retry budget: 1 per exact action, 2 per strategy, 3 total before escalation. Recovery menu: correct/narrow/inspect/substitute/escalate. Escalation strings list |
| `persistent-task-state` | 9-file layout under `.agent_work/sprints/<sprint>/tasks/<YYYY-MM-DD-slug>/`. File responsibilities table. State hygiene: no full file/log dumps |
| `phase-compression` | Required debrief format (Completed, Evidence, Blockers, Decisions, Carry Forward, Do Not Carry Forward, Next Phase). Compression rules: summarize, don't paste raw logs. Do-Not-Carry-Forward prevents loops |
| `small-context-workflows` | Fresh session pattern: load 6 files (TASK, STATUS, CHECKLIST, DECISIONS, CONTEXT, NEXT_PROMPT), not full chat. More phases for tighter context |
| `context-management` | Context budget allocation: reserve space for tool results and output. Reading order matters. Evidence anchors for re-anchoring |
| `targeted-context-length` | Optimize for stated budget, not advertised max. Affects verbosity, phase count, example count, report size |
| `instruction-precedence` | 9-level priority hierarchy: (1) user's current explicit request, (2) safety boundaries, (3) project/repo evidence, (4) existing repo instructions, (5) target model constraints, (6) domain-specific requirements, (7) external skill artifacts, (8) optional style preferences, (9) generic best practices. Never average conflicts |
| `instruction-deduplication` | Scan existing instructions before adding new ones. Merge policy: preserve clear/specific/correct, strengthen vague, consolidate duplicates, add missing. Token-bloat guard |
| `engineering-metadata` | YAML metadata schema with 8 recommended fields. Record targeted context length when provided |
| `output-location` | Canonical output paths under `.agent_work/`. Iterations subdirectory for Ralph loop |
| `git-safety` | Destructive git commands require explicit approval: reset --hard, clean -fd, rebase, push --force, branch deletion, amending/squashing. Safe inspection: status, diff, log |
| `upstream-artifact-audit` | 8-step process: identify, extract, verify, classify, preserve confirmed, downgrade unsupported, reject conflicting/hallucinated, report. Required report block with Preserved/Modified/Rejected sections |
| `skill-interoperability` | Treat upstream skill outputs as inputs to verify, not authoritative truth. 6-tier classification: confirmed, likely, useful suggestion, unsupported, conflicting, rejected. Workflow collision check: compatible, overlapping, conflicting, unknown |
| `small-model-atomicity` | Instructions must be atomic for smaller models. Single objective per instruction. No hidden inference leaps. Explicit inputs and outputs |
| `ralph-loop` | Bounded improvement loop: max 2 iterations (hard max 3). A-F evaluation across 10 categories. Canonical iteration storage under `.agent_work/.../iterations/`. Stop on bloat or semantic drift |
| `planner-executor-workflows` | Stronger model for planning/audits/design. Smaller model for atomic phase execution when plan and task state are explicit. One phase per session when context is tight |
| `phase-code-review` | Post-phase code review gate. Standard: focused review of changed code, 1 iteration max. Deep: 2 iterations with test quality audit |
| `runtime-stability` | Local model runtime issues: loops, KV cache precision, speculative decoding effects. Treat as experimental guidance unless harness can control |
| `side-effect-matrix` | Risk classification for agent actions: tier 1 (read-only), tier 2 (write own files), tier 3 (modify user files), tier 4 (system/network). Approval gates per tier |

#### 1C: Create `shared/parameter-narrowing-rules.md`

Specifies when and how child artifacts may narrow inherited parameters:
- Allowed narrowings with examples (context-length, ralph iterations, education-level)
- Forbidden widenings without justification
- Justification format for exceptions
- Interaction between narrowing and chain-of tracking

### Phase 2: Engineer Skill Updates (Edit Existing SKILL.md Files)

#### 2A: Update `skills/local-model-prompt-engineer/SKILL.md`

**Changes needed:**
1. Replace current "Default Parameters" section (lines ~131-145) with manifest-based approach
2. Add generation rule: "All generated artifacts MUST include an Artifact Manifest section per `references/artifact-manifest.md`"
3. Add parameter tracking instructions: how to determine source value for each param (`user-set | inherited | default | narrowed`)
4. Add reference selection guidance: which references to include based on artifact type (use the matrix from design)
5. Add behavioral contract embedding instructions: copy from `references/behavioral-contracts.md`, append custom contracts for domain-specific requirements
6. Update parameter inheritance section (lines ~246-249) — replace with manifest-based propagation rules
7. Add example of what a complete prompt output looks like with manifest

**Specific edits:**
- Section "0. Apply Default Parameters" → rename to "Apply Parameters and Build Manifest", expand with full procedure
- Section "Ensure all generated artifacts implement the parameter inheritance system" (lines 246-249) → replace with manifest propagation rules
- Add new section after "Required Output": "Artifact Manifest Requirements" with embedding instructions

#### 2B: Update `skills/local-model-skill-engineer/SKILL.md`

Same pattern as 2A, adapted for skill generation:
- Generated SKILL.md files must include artifact manifest
- Skill-specific parameters (`--reference-policy`, `--metadata`, `--in-place`) included in manifest
- References applied must include skill-interoperability, upstream-artifact-audit (if migrating)

#### 2C: Update `skills/local-model-instruction-engineer/SKILL.md`

Same pattern as 2A, adapted for instruction file generation:
- Generated AGENTS.md/CLAUDE.md files must include artifact manifest
- Instruction-specific parameters included in manifest
- References applied must include instruction-deduplication, instruction-precedence, git-safety

#### 2D: Copy New References to Per-Skill `references/` Directories

For each of the three engineer skills, copy:
- `artifact-manifest.md` → each skill's `references/`
- `behavioral-contracts.md` → each skill's `references/`
- `parameter-narrowing-rules.md` → each skill's `references/`

### Phase 3: Validation & Examples

#### 3A: Update `scripts/validate_skills.py`

Add validation checks for:
- SKILL.md files reference `artifact-manifest.md` in their generation instructions
- Generated artifact examples include manifest sections (if examples exist)
- New shared references have correct format (no frontmatter, ATX headings only)

#### 3B: Add Example Manifests to Each Skill

Each engineer skill should have a compact example of what a complete output looks like with the manifest, showing:
- A prompt with manifest (prompt-engineer)
- A generated skill with manifest (skill-engineer)
- An AGENTS.md with manifest (instruction-engineer)
- An implementation plan phase with manifest (prompt-engineer coding path)
- A NEXT_PROMPT.md with inherited manifest (prompt-engineer execution path)

---

## Constraints & Optimization Notes for Small Model Implementation

### Context Budget Considerations

- The behavioral contracts section can be large. For tight context budgets (`--context-length <= 32k`), include only the most critical contracts and rely on the references-applied table as a pointer
- The manifest should be compact enough not to consume excessive context in generated artifacts
- Consider a `--artifact-verbosity compact` mode where the manifest omits the full behavioral contracts section and only includes the references-applied table

### Atomicity Requirements

Each implementation phase must:
- Have a single, clear objective
- Name specific files to create or edit
- Include explicit validation steps (run `python scripts/validate_skills.py`, check file exists, verify format)
- End with a stop condition that is objectively verifiable
- Not depend on vague "make it work" outcomes

### File Boundaries

**New files to create:**
1. `shared/artifact-manifest.md` — manifest spec (~200 lines expected)
2. `shared/behavioral-contracts.md` — pre-extracted contracts (~300 lines expected)
3. `shared/parameter-narrowing-rules.md` — narrowing rules (~80 lines expected)

**Files to edit:**
1. `skills/local-model-prompt-engineer/SKILL.md` — replace default params section, add manifest generation rules
2. `skills/local-model-skill-engineer/SKILL.md` — same pattern
3. `skills/local-model-instruction-engineer/SKILL.md` — same pattern

**Files to copy (new per-skill references):**
- For each of 3 engineer skills: copy the 3 new shared files to `references/`

**Validation:**
- Run `python scripts/validate_skills.py` after all edits
- May need to update `scripts/validate_skills.py` with new checks

### Phase Ordering Dependencies

```
Phase 1A (artifact-manifest.md) — no dependencies
Phase 1B (behavioral-contracts.md) — depends on reading all shared/ refs to extract contracts
Phase 1C (parameter-narrowing-rules.md) — depends on 1A for format consistency

Phase 2A (prompt-engineer SKILL.md) — depends on 1A, 1B, 1C existing
Phase 2B (skill-engineer SKILL.md) — depends on 1A, 1B, 1C; parallel with 2A
Phase 2C (instruction-engineer SKILL.md) — depends on 1A, 1B, 1C; parallel with 2A
Phase 2D (copy refs to per-skill dirs) — depends on 1A, 1B, 1C; can parallel with 2A-2C

Phase 3A (validate_skills.py) — depends on all above
Phase 3B (example manifests) — depends on all above
```

### Risk Areas

1. **Behavioral contracts length:** If too verbose, they'll bloat every generated artifact. Must be aggressively condensed — 3-7 lines per contract, actionable requirements only.
2. **SKILL.md line count:** Adding manifest sections may push SKILL.md files over the 500-line limit. Need to be concise in new sections, possibly removing redundant content from existing sections (e.g., the current default params table can be replaced by a reference to `artifact-manifest.md`).
3. **Per-skill copy sync:** After creating the 3 new shared files, they must be copied to all per-skill `references/` directories. This is mechanical but error-prone — validate after copying.

---

## Success Criteria

After implementation:
1. Generated prompts include an Artifact Manifest with parameters (with provenance), references applied, and behavioral contracts
2. Generated implementation plans inherit params from parent prompt, narrow context-length per phase, add planning-specific references
3. Generated NEXT_PROMPT.md files inherit from their plan, carry forward phase debrief facts, track chain-of provenance
4. The validation script passes after all changes
5. All three engineer skills produce consistent manifest format in their outputs
6. Artifacts work standalone (behavioral contracts embedded) AND with ContextSmith installed downstream (references-applied table resolves to full refs)
