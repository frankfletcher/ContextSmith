# Universal Runtime Enforcement Implementation Plan

## Artifact Manifest
- artifact_type: implementation-plan
- parent_task: TASK.md
- target_profile: qwen36 (inherited; executor profile for atomic phases)
- planner_profile: stronger model or human review required for architecture gates
- harness: opencode (inherited)
- context_length: 64k (inherited)
- mode: guided (inherited)
- validation_level: strict for planning and final closeout; available checks for implementation phases
- pytest: pre-approved by current user for runtime validator tests
- references: phased-planning, persistent-task-state, implementation-plan-audit, test-quality-audit, phase-code-review, git-safety, side-effect-matrix
- behavioral_contract: Each phase must be small enough for a local model, must preserve universal skill/agent/prompt applicability, and must end with evidence, task-state updates, and a next action.

## Engineering Metadata
- planner: contextsmith-prompt-engineer
- revised: 2026-06-01
- domain: universal agent tooling, runtime validation, skill packaging, domain packs
- side_effect_tier: planning-only for this task; implementation phases may create source, tests, and task artifacts after approval boundaries are checked

## Purpose
Create an implementation path for runtime enforcement that works for many skill, agent, and prompt use cases, not only coding.

The system should let a user create a plan, run one bounded phase at a time, validate that the requirements chain is preserved, and stop or repair when evidence is missing.

## Core Principle
Do not trust a small model to carry a sweeping architecture in memory.

Instead:
- a stronger planner or human review defines the universal protocol and domain-pack rules;
- a small executor model performs one tiny implementation phase at a time;
- validators check artifacts outside the model;
- an orchestrator or harness controls phase progression when available;
- human approval gates remain explicit for irreversible or external actions.

## Architecture Direction
Build a small `contextsmith-runtime` layer with one validator core and optional adapters:

- **Universal protocol:** machine-readable requirements, phase contracts, evidence, approval, and closeout artifacts.
- **Domain packs:** small validation profiles for software, writing, research, scheduling, travel, business, education, and general fallback.
- **CLI adapter:** portable validator and runner commands.
- **MCP adapter:** structured tool calls around the same validator core.
- **Orchestrated runner:** sequential gate loop that controls prompt flow for workflows that opt into it.
- **Harness adapter:** optional hard-blocking integration when a harness can actually enforce gates.

## Enforcement Levels
Use these labels everywhere. Do not blur them.

| Level | Meaning | Example |
|---|---|---|
| Deterministic validation | A tool checks artifacts and returns pass/fail evidence. | CLI validates an evidence ledger. |
| Orchestrated workflow enforcement | A runner only advances if validators pass. Bypass is possible outside the runner. | Plan runner sends correction prompts until closeout passes. |
| Harness hard blocking | The harness prevents finalization, tool use, or side effects until gates pass. | opencode permission hook blocks an external action. |
| Human approval | A person must approve an irreversible, costly, private, or high-risk action. | Booking airfare or sending calendar invites. |

## Universal Use Cases
The protocol must support more than coding:

| Domain | Example | Required gates |
|---|---|---|
| Software engineering | Implement a validator | tests, lint/validation, changed files, closeout |
| Writing/editing | Rewrite an email | source preservation, tone check, final draft evidence |
| Research | Summarize papers | source citations, uncertainty, unsupported-claim check |
| Scheduling | Find meeting time | participants, time zones, availability, user approval before sending |
| Travel/procurement | Find cheap airline tickets | constraints, price timestamp, fee/refund evidence, explicit purchase approval |
| Education | Create lesson plan | audience level, learning objective, assessment check |
| General fallback | Any prompt/agent task | requirements trace, evidence, validation or blocker |

## Small-Model Execution Rules
- Every implementation phase is one bounded unit with one primary objective.
- Tool-heavy phases run in a fresh session. Never chain multiple implementation or test phases in one session.
- Fresh-session read order: `STATUS.md`, current phase in `PLAN.md`, `CONTEXT.md`, `CHECKLIST.md`, then exact files named by the phase.
- Do not carry raw search output, raw pytest output, or prior chat into later phases.
- If a phase discovers architecture uncertainty, stop and ask for human/frontier review instead of improvising.
- If validation fails twice or needs broad redesign, stop and record a blocker.
- If a phase reads more than 3 source files AND produces more than 2 output artifacts, consider splitting it.
- Pytest is pre-approved; other new dependencies still require approval.
- Track actual token usage per phase. Record in `PHASE_LOG.md`. Use as data for future budgeting.

## Phase Contract Template
Each phase must include this compact contract:

```yaml
context_contract:
  executor: small-model|human-or-frontier-review
  phase_type: discovery|design|implementation|test|integration|rollout|validation
  usable_phase_budget: estimated token range (e.g., 40k-60k). Baseline: Phase 0 discovery actual = 78k.
  expected_tool_calls: read/edit/bash/validation counts or ranges
  validation_output_budget: brief|moderate
  validation_output_reserve: required for all implementation and test phases; reserve at least 25 percent for validation output and one targeted correction
  compaction_trigger: what to summarize before continuing
  stop_rule: when to stop instead of widening scope
```

**Budgeting notes:**
- Phase 0 actual: 78k tokens for a discovery phase (4-8 reads, 1 dry-run, 0 edits). Use as baseline for discovery phases that read multiple files and produce task-state artifacts.
- `usable_phase_budget` should be a numeric estimate, not just `small` or `moderate`.
- For a 64k executor context, small-model phases should normally target 20k-45k usable tokens. Anything estimated above 45k must either be split or explicitly marked for a larger-context/frontier executor.
- Actual token usage may be unavailable in some harnesses. If unavailable, record `actual_token_usage: unavailable` plus proxy metrics: files read, tool calls, commands run, artifacts edited, and validation-output size.
- Any phase that reads more than 3 source files AND produces more than 2 output artifacts is a candidate for splitting.
- Implementation and test phases always include `validation_output_reserve` — no exceptions.
- Tool-heavy phases must run in a fresh session. Never chain multiple implementation phases in one session.

## Required Phase Closeout
Every phase, including read-only design phases, must close with a compact debrief. Update all files that changed in relevance; do not paste raw logs.

Required closeout fields:
- `STATUS.md`: current state, validation state, blocker if any, next required action.
- `PHASE_LOG.md`: one compact entry with completed work, evidence, validation, blockers, and next action.
- `ARTIFACTS.md`: created or changed artifacts, source files, fixtures, commands, and validation evidence.
- `DECISIONS.md`: durable decisions or unresolved decision requests.
- `CONTEXT.md`: new facts, constraints, skip rules, or packaging/domain findings.
- `CHECKLIST.md`: checked items only when evidence exists.
- `NEXT_PROMPT.md`: exact resume prompt for the next phase.

Required debrief content:
- carry forward: facts, files, decisions, and commands needed next.
- do not carry forward: raw command output, broad search results, stale assumptions, and resolved dead ends.
- validation evidence: commands/checks run, status, and short result.
- residual risk: what remains uncertain and who must decide.

## Recovery Procedure
Use this when a phase fails validation, exceeds scope, or cannot self-correct safely.

1. Stop phase execution. Do not widen scope or start the next phase.
2. Set `STATUS.md` to `Blocked` with the failed gate, exact reason, and impact.
3. Add a `PHASE_LOG.md` entry with attempted action, validation result, and why one targeted correction was insufficient or unsafe.
4. Update `ARTIFACTS.md` with partial artifacts and mark them `partial` or `invalid`.
5. Add or update `DECISIONS.md` only for durable decisions or explicit approval requests.
6. Write `NEXT_PROMPT.md` for human/frontier review with three options at most: fix, narrow scope, or abandon/replace the approach.
7. Do not mark completion until the blocker is resolved by evidence or explicitly waived by the user.

## Documentation Requirements
Runtime enforcement changes the project architecture, source code, skill operation model, and user workflows. Documentation is part of the implementation, not an afterthought.

User-facing documentation must:
- explain the pain point and benefits clearly;
- minimize time to first value with quick paths and copy-paste examples;
- provide lookup material for detailed use cases;
- include examples for coding and non-coding workflows;
- include a table of contents in every substantial Markdown file;
- remain website-ready, because Markdown is the future website source of truth;
- keep the README catchy, practical, and free of generic AI marketing patterns;
- avoid repeated contrastive phrasing such as frequent `not just X, but Y` constructions;
- follow `docs/contributing/documentation-style.md`, `docs/contributing/documentation-review-checklist.md`, and `shared/documentation-quality.md`.

Documentation should make ContextSmith feel useful, approachable, and enjoyable without overstating implemented features.

Documentation should focus on how to use ContextSmith. Mention architecture only when it helps a user choose the right workflow, understand an output, or avoid a mistake.

## Phase 0: Packaging Discovery
**Goal:** Verify how installed skills and release bundles can carry runtime code, metadata, and references.

```yaml
context_contract:
  executor: small-model
  phase_type: discovery
  usable_phase_budget: 40k-45k estimated; ACTUAL 78k (exceeded budget; use as warning baseline for discovery phases)
  expected_tool_calls: 4-8 reads, optional 1 dry-run command, 0 source edits
  validation_output_budget: brief
  compaction_trigger: summarize include/exclude behavior for each packaging path
  stop_rule: stop if packaging behavior conflicts across scripts
```

**Inputs:**
- `scripts/build_release.py`
- `scripts/package_skill.sh`
- `scripts/sync_shared_refs.py`
- `scripts/token_budget.py`
- `skills/*/reference_manifest.yml`
- `PACKAGE_SPEC.md` read-only unless approval is given

**Actions:**
1. Inspect package and release scripts.
2. Record what individual skill zips include.
3. Record what release bundles include.
4. Record whether executable runtime files, YAML schemas, and fixtures can ship.
5. Record any approval needed before changing package design.

**Outputs:**
- Packaging facts in `CONTEXT.md`.
- Open packaging decisions in `DECISIONS.md`.

**Validation:**
- Every claim cites exact file paths or commands inspected.
- No source behavior is changed.

## Phase 0.5: Runtime Distribution, Dependency, and Surface Decision
**Goal:** Decide the runtime distribution model, dependency policy, and first implementation slice before any validator implementation begins.

```yaml
context_contract:
  executor: human-or-frontier-review
  phase_type: design
  usable_phase_budget: 20k-40k
  expected_tool_calls: 0-2 reads, 0 source edits
  validation_output_budget: brief decision matrix with explicit authorization result
  compaction_trigger: summarize selected distribution model, dependency policy, selected surfaces, rejected surfaces, and Phase 1A authorization
  stop_rule: stop if the distribution model requires package design changes, a dependency not already approved, user-level config edits, or an unresolved runtime install assumption
```

**Required decisions:**
1. Distribution model:
   - per-skill manifest entries for runtime files;
   - separate `contextsmith-runtime` package;
   - hybrid: separate runtime package plus small per-skill references or generated artifacts.
2. Runtime parsing/dependency policy:
   - stdlib-only JSON first;
   - PyYAML-backed YAML with explicit approval/install path;
   - dual JSON/YAML support where YAML is optional and failure messages name the missing dependency.
3. First-slice runtime surfaces:
- CLI validator only.
- CLI validator plus domain packs.
- CLI validator plus orchestrated runner.
- CLI plus MCP adapter.
- CLI plus harness adapter.

**Default recommendation:** Start with CLI validator plus universal protocol plus one or two domain packs. Add runner, MCP, and harness adapters only after the core checks are proven.

**Education:** This prevents a small model from trying to implement every runtime surface at once. The core must be stable before adapters multiply behavior.

**Outputs:**
- Decision entry in `DECISIONS.md`.
- Distribution model, runtime dependency policy, and narrowed first-slice scope in `STATUS.md` and `NEXT_PROMPT.md`.
- Explicit `Phase 1A authorized: yes|no` statement with reason.

**Validation:**
- Decision matrix compares at least the three distribution options above.
- Dependency policy states whether PyYAML is required, optional, or avoided for the first slice.
- No implementation phase starts until Phase 0.5 records the chosen distribution model and authorization result.

## Phase 1A: Universal Artifact Vocabulary
**Goal:** Define the small set of artifact names used across all domains.

```yaml
context_contract:
  executor: small-model
  phase_type: design
  usable_phase_budget: 20k-30k
  expected_tool_calls: 2-4 reads, 1 task artifact edit
  validation_output_budget: brief
  compaction_trigger: summarize artifact names and fields
  stop_rule: stop if more than six artifact types are needed
```

**Artifacts to define:**
- `requirements_chain`
- `phase_contract`
- `domain_pack`
- `evidence_ledger`
- `approval_record`
- `phase_closeout`

**Actions:**
1. Create a compact schema note under this task directory.
2. For each artifact, define purpose, required fields, and one tiny example.
3. Keep examples domain-neutral.

**Validation:**
- No artifact requires hidden reasoning.
- Each artifact can be represented as YAML or JSON.
- Each artifact is reusable for coding, scheduling, travel, writing, and research.

## Phase 1B: Requirements Chain Schema
**Goal:** Define how original requirements trace through phases and evidence.

```yaml
context_contract:
  executor: small-model
  phase_type: design
  usable_phase_budget: 20k-40k
  expected_tool_calls: 1-3 reads, 1 task artifact edit
  validation_output_budget: brief
  compaction_trigger: summarize required fields and one trace example
  stop_rule: stop if trace model needs complex graph logic
```

**Required fields:**
- requirement id
- source text or source path
- domain
- side-effect tier
- validation method
- phase ids that satisfy it
- evidence ids that prove it
- status: pending, passed, blocked, waived_by_user

**Education:** This is what prevents the model from satisfying only the current prompt while forgetting earlier requirements.

**Validation:**
- Example traces one requirement from task request to phase output to validation evidence.

## Phase 1B.5: Approval Record Schema
**Goal:** Define explicit approval records for irreversible, external, private, costly, or high-risk actions.

```yaml
context_contract:
  executor: small-model
  phase_type: design
  usable_phase_budget: 20k-30k
  expected_tool_calls: 1-3 reads, 1 task artifact edit
  validation_output_budget: brief
  compaction_trigger: summarize approval fields and one external-action example
  stop_rule: stop if approval records try to automate external actions instead of documenting authorization
```

**Required fields:**
- approval id
- linked requirement ids
- action requiring approval
- side-effect tier
- requester
- approver or `not_yet_approved`
- approval status: not_required, requested, approved, denied, waived_by_user
- approval timestamp or `pending`
- evidence id or source note
- residual risk disclosure for high-risk actions

**Validation:**
- Example shows travel purchase approval remains `requested` or `denied` unless explicit user approval exists.
- No approval record implies permission for external action without evidence.

## Phase 1C: Domain Pack Schema
**Goal:** Define small domain-specific rule packs without making the core domain-specific.

```yaml
context_contract:
  executor: small-model
  phase_type: design
  usable_phase_budget: 20k-40k
  expected_tool_calls: 1-3 reads, 1 task artifact edit
  validation_output_budget: brief
  compaction_trigger: summarize domain pack fields
  stop_rule: stop if a domain pack needs custom code before the generic fields are defined
```

**Required fields:**
- domain name
- triggers
- required artifacts
- validation gates
- approval gates
- external action boundaries
- residual risk disclosures
- example good closeout
- example blocked closeout

**Starter domain packs:**
- `software_engineering`
- `writing_editing`
- `research_summary`
- `scheduling`
- `travel_purchase`
- `general_fallback`

**Validation:**
- Each starter domain pack fits on one screen.
- No domain pack requires new dependencies.

## Phase 1D: Architecture Review Gate
**Goal:** Review Phases 1A-1C before implementation begins.

```yaml
context_contract:
  executor: human-or-frontier-review
  phase_type: validation
  usable_phase_budget: 20k-40k
  expected_tool_calls: 2-4 reads, 0-1 task artifact edits
  validation_output_budget: brief review findings
  compaction_trigger: summarize approved schema and required corrections
  stop_rule: stop if universal protocol does not support non-coding domains
```

**Review questions:**
1. Can the schema support coding, scheduling, travel, writing, research, and fallback tasks?
2. Are approval boundaries explicit for external actions?
3. Can a small model emit the artifacts without carrying long instructions?
4. Are validators deterministic enough to implement simply?

**Validation:**
- Approved, or corrections are recorded before implementation.

## Phase 2A: Minimal Validator Core
**Goal:** Implement the smallest validator core that checks structure, required fields, and status values.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 35k-45k
  expected_tool_calls: 3-5 reads, 2-4 edits, 1-2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize function names and result schema
  stop_rule: stop if implementation conflicts with the Phase 0.5 distribution or dependency policy, or if it needs an unapproved dependency
```

**Actions:**
1. Create the runtime validator module in the location approved by Phase 0.5.
2. Implement parsing according to the Phase 0.5 dependency policy; do not assume YAML support unless that decision explicitly approved it.
3. Implement `validate_requirements_chain(path)`.
4. Implement `validate_phase_contract(path)`.
5. Implement `validate_evidence_ledger(path)`.
6. Implement `validate_approval_record(path)`.
7. Implement `validate_phase_closeout(path)`.
8. Return `{"passed": bool, "violations": list, "warnings": list}` from every public validator.

**Validation:**
- Module imports successfully.
- Each public validator returns the expected result shape for a tiny valid fixture.
- Approval records reject missing approval status for external or high-risk actions.
- Parser behavior matches the Phase 0.5 dependency policy, including clear errors for unsupported file formats or missing optional dependencies.

## Phase 2B: Domain Pack Validator
**Goal:** Add generic validation for domain pack files.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 30k-45k
  expected_tool_calls: 2-3 reads, 1-2 edits, 1-2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize domain pack required fields
  stop_rule: stop if implementation tries to encode domain-specific business logic in the core
```

**Actions:**
1. Implement `validate_domain_pack(path)`.
2. Check required fields and allowed side-effect tiers.
3. Do not implement custom scheduling/travel/business logic yet.

**Validation:**
- Good starter domain pack passes.
- Missing approval gates fail for high-risk domains such as travel purchase.

## Phase 2C: CLI Adapter
**Goal:** Add a small CLI around the validator core.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 30k-45k
  expected_tool_calls: 2-3 reads, 1-2 edits, 2-3 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize subcommands and exit codes
  stop_rule: stop if CLI grows beyond validator dispatch and output formatting
```

**Subcommands:**
- `requirements`
- `phase-contract`
- `evidence`
- `approval`
- `closeout`
- `domain-pack`

**Exit codes:**
- `0`: passed
- `1`: validation failed
- `2`: usage or file-read error

**Validation:**
- `--help` works.
- A passing fixture exits `0`.
- A failing fixture exits `1` and lists exact violations.

## Phase 2D: Pytest Fixture Tests
**Goal:** Test validator behavior with small positive and negative fixtures.

```yaml
context_contract:
  executor: small-model
  phase_type: test
  usable_phase_budget: 35k-45k
  expected_tool_calls: 2-3 reads, 4-8 edits, 2-4 validation commands
  validation_output_budget: compact pytest summary
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize fixture matrix before writing tests
  stop_rule: stop if tests become broad integration tests or require dependencies beyond pytest
```

**Pytest status:** pre-approved by current user.

**Fixtures:**
- good and bad `requirements_chain`
- good and bad `phase_contract`
- good and bad `evidence_ledger`
- good and bad `approval_record`
- good and bad `phase_closeout`
- good and bad `domain_pack`

**Validation:**
- `python -m pytest tests/ -v` passes.
- Negative tests assert specific violation text.
- `python scripts/validate_skills.py` passes if skill files changed.
- `python scripts/token_budget.py --strict` passes if skill or reference files changed.

## Phase 2E: Installed-Workflow Smoke Test
**Goal:** Prove the validator can be called from an installed or staged workflow, not only repo-local assumptions.

```yaml
context_contract:
  executor: small-model
  phase_type: test
  usable_phase_budget: 30k-45k
  expected_tool_calls: 2-4 reads, 0-2 edits, 1-3 commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for staging command result and fallback/blocker summary
  compaction_trigger: summarize staged path and command used
  stop_rule: stop if packaging must change before the smoke test is meaningful; record fallback path instead of redesigning packaging
```

**Actions:**
1. Use the packaging facts from Phase 0.
2. Stage or package the minimal runtime artifacts if safe.
3. Invoke the validator from the staged path or record why unavailable.
4. If packaging cannot carry runtime files, document one fallback path: separate runtime package, repo-level CLI install, or generated artifact-only validation.

**Validation:**
- Evidence shows the command works outside normal source-file assumptions, or a blocker is recorded.
- If blocked, `STATUS.md`, `PHASE_LOG.md`, `ARTIFACTS.md`, and `NEXT_PROMPT.md` name the fallback path and required decision.

## Phase 3A: General Fallback Domain Pack
**Goal:** Create the smallest domain pack that works for any prompt, skill, or agent task.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 25k-40k
  expected_tool_calls: 1-3 reads, 1-2 edits, 1-2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize fields and gates
  stop_rule: stop if domain pack becomes a long instruction file
```

**Required gates:**
- requirement trace exists
- phase contract exists
- evidence ledger exists
- validation result or blocker exists
- approval record exists for external actions
- final claims do not exceed evidence

**Education:** This is the universal safety net for unknown domains.

## Phase 3B: Software Engineering Domain Pack
**Goal:** Create a compact software domain pack.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 25k-40k
  expected_tool_calls: 1-3 reads, 1-2 edits, 1-2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize gates
  stop_rule: stop if this duplicates full coding standards
```

**Required gates:**
- changed files listed
- project validation command run or blocker recorded
- tests added or test gap explained
- code review gate completed
- destructive git operations forbidden without approval

## Phase 3C: Scheduling Domain Pack
**Goal:** Create a compact scheduling domain pack.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 25k-40k
  expected_tool_calls: 1-3 reads, 1-2 edits, 1-2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize gates
  stop_rule: stop if calendar APIs or external sending are implemented here
```

**Required gates:**
- participants known
- time zones resolved or blocker recorded
- duration known
- candidate slots listed
- approval before sending invite or message
- final invite/message evidence if sent

## Phase 3D: Travel/Purchase Domain Pack
**Goal:** Create a compact high-risk external-action domain pack.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 25k-40k
  expected_tool_calls: 1-3 reads, 1-2 edits, 1-2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize gates
  stop_rule: stop if purchase automation is implied without explicit approval controls
```

**Required gates:**
- dates, airports, passenger count, and constraints recorded
- price source and timestamp recorded
- fees, baggage, refund/cancellation terms recorded or unavailable noted
- no purchase, payment, or irreversible action without explicit user approval
- residual risk disclosure required because fares and policies may change

## Phase 3E: Writing/Editing Domain Pack
**Goal:** Create a compact writing and editing domain pack.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 25k-40k
  expected_tool_calls: 1-3 reads, 1-2 edits, 1-2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize gates
  stop_rule: stop if writing guidance becomes a style manual instead of validation gates
```

**Required gates:**
- source material or user intent preserved
- audience, tone, and format recorded or blocker noted
- final draft claims do not add unsupported facts
- requested constraints are traced to output evidence
- user approval required before sending, publishing, or representing text as final externally

## Phase 3F: Research Summary Domain Pack
**Goal:** Create a compact research and source-summary domain pack.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 25k-40k
  expected_tool_calls: 1-3 reads, 1-2 edits, 1-2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize gates
  stop_rule: stop if research validation requires live browsing, citation scraping, or complex evidence scoring
```

**Required gates:**
- sources listed with paths or URLs
- unsupported claims flagged or removed
- uncertainty and limitations recorded
- quotes, statistics, and factual claims trace to evidence
- external publication or submission requires approval

## Phase 3G: Domain Pack Review Gate
**Goal:** Review starter domain packs before adding more domains.

```yaml
context_contract:
  executor: human-or-frontier-review
  phase_type: validation
  usable_phase_budget: 20k-40k
  expected_tool_calls: 2-4 reads, 0-1 edits
  validation_output_budget: brief findings
  compaction_trigger: summarize accepted and rejected patterns
  stop_rule: stop if domain packs are too verbose for small models
```

**Validation:**
- Each domain pack is compact.
- Each separates deterministic validation from approval and external action boundaries.
- General fallback can handle unknown domains.

## Phase 4A: ContextSmith-Run Pilot Integration
**Goal:** Update only `contextsmith-run` to emit or request runtime-checkable artifacts.

```yaml
context_contract:
  executor: small-model
  phase_type: integration
  usable_phase_budget: 35k-45k
  expected_tool_calls: 3-5 reads, 1-2 edits, 2-4 validation commands
  validation_output_budget: brief summaries only; reserve space for validate_skills, token_budget, and pytest summaries
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize current SKILL.md line count, changed paths, and intended validator references before validation
  stop_rule: stop if SKILL.md approaches 450 lines, integration needs more than 2 edits, validation output is verbose, or integration duplicates validator logic
```

**Actions:**
1. Keep SKILL.md thin.
2. Point to runtime artifacts and validator gates.
3. Do not paste full schemas into SKILL.md if references or generated artifacts can hold them.
4. If context rises above budget, stop after drafting the integration note and move validation to a fresh session.

**Validation:**
- `python scripts/validate_skills.py` passes.
- `python scripts/token_budget.py --strict` passes.
- Runtime validator tests pass.

## Phase 4B: Thin-Skill Writing Guide
**Goal:** Write a short guide explaining how external validators change skill authoring.

```yaml
context_contract:
  executor: small-model
  phase_type: design
  usable_phase_budget: 20k-40k
  expected_tool_calls: 1-3 reads, 1 edit
  validation_output_budget: brief
  compaction_trigger: summarize old-vs-new skill style
  stop_rule: stop if guide becomes broader than one page
```

**Key message:** Skills should become thin runtime contracts plus routing instructions. Validators own pass/fail rules. Runners own sequencing. Harnesses own hard blocking where possible.

## Phase 5A: Next Prompt Compiler Specification
**Goal:** Specify a small tool that compiles the current phase into a detailed small-model execution prompt.

```yaml
context_contract:
  executor: human-or-frontier-review
  phase_type: design
  usable_phase_budget: 20k-40k
  expected_tool_calls: 2-4 reads, 1 task artifact edit
  validation_output_budget: brief compiler spec
  validation_output_reserve: include generated-prompt quality checklist
  compaction_trigger: summarize input files, output sections, and hard-stop rules
  stop_rule: stop if compiler design tries to run the model or execute the phase
```

**Purpose:** The compiler turns task state into `NEXT_PROMPT.md` and optional `PHASE_<N>_SMALL_MODEL_PROMPT.md` files. It does not run the model. It prepares safe handoffs.

**Inputs:**
- `STATUS.md`
- current phase block in `PLAN.md`
- `CONTEXT.md`
- `CHECKLIST.md`
- `DECISIONS.md`
- optional phase-specific artifacts

**Required generated prompt sections:**
- artifact manifest
- mission and hard phase boundary
- read order
- phase contract
- allowed and disallowed actions
- exact files or commands to inspect
- validation commands
- task-state closeout requirements
- recovery procedure
- self-audit requirements
- expected final output format
- hard stop before the next phase
- deep education notes for the human operator

**Validation:**
- Compiler spec proves it can generate the Phase 0 prompt shape without nested Markdown fence issues.
- Generated prompt includes validation, audit, closeout, recovery, and hard-stop sections.
- Generated prompt does not ask the small model to make broad architecture decisions.

## Phase 5B: Next Prompt Compiler Implementation
**Goal:** Implement the smallest read-only compiler command that generates detailed phase prompts from task state.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 35k-45k
  expected_tool_calls: 3-5 reads, 2-4 edits, 2-4 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for sample generated prompt and validation summary
  compaction_trigger: summarize compiler inputs, output path, and template sections before implementation
  stop_rule: stop if implementation tries to invoke a model, mutate source code, or advance phases
```

**Actions:**
1. Implement a CLI command such as `next-prompt` or equivalent per Phase 0.5 distribution decision.
2. Read the current phase from `STATUS.md` and `PLAN.md`.
3. Generate `NEXT_PROMPT.md` with detailed small-model execution instructions.
4. Optionally generate `PHASE_<phase>_SMALL_MODEL_PROMPT.md` for archival clarity.
5. Use safe Markdown fences: prefer `~~~` for inner code blocks and four-backtick fences for Markdown templates.
6. Do not run the phase and do not call any model.

**Validation:**
- Generated Phase 0 prompt includes all required sections.
- Generated prompt renders cleanly as Markdown.
- Prompt hard-stops before Phase 0.5.
- Pytest covers at least one good task-state fixture and one missing-phase fixture.

## Phase 5C: Next Prompt Compiler Tests
**Goal:** Test prompt generation, phase boundaries, and Markdown formatting.

```yaml
context_contract:
  executor: small-model
  phase_type: test
  usable_phase_budget: 30k-45k
  expected_tool_calls: 2-4 reads, 2-5 edits, 2-3 validation commands
  validation_output_budget: compact pytest summary
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize fixture cases before writing tests
  stop_rule: stop if tests require dependencies beyond pytest
```

**Required tests:**
- Good Phase 0 fixture generates a prompt with mission, read order, validation, audit, closeout, recovery, and hard stop.
- Missing current phase fails with a clear violation.
- Generated prompt does not include instructions to execute the next phase.
- Generated prompt has balanced Markdown fences.
- Generated prompt includes deep education notes when requested.

**Validation:**
- `python -m pytest tests/ -v` passes.
- `python scripts/validate_skills.py` passes if skill files changed.
- `python scripts/token_budget.py --strict` passes if skill or reference files changed.

## Phase 5D: Orchestrated Runner Specification
**Goal:** Specify a harness-independent runner without implementing it yet.

```yaml
context_contract:
  executor: human-or-frontier-review
  phase_type: design
  usable_phase_budget: 20k-40k
  expected_tool_calls: 1-3 reads, 1 task artifact edit
  validation_output_budget: brief
  compaction_trigger: summarize gate loop and bypass limits
  stop_rule: stop if runner is described as hard enforcement without harness support
```

**Runner loop:**
1. Read task state.
2. Select current phase and domain pack.
3. Build a compact model prompt.
4. Run or hand off to model.
5. Validate artifacts.
6. If failed, issue one correction prompt with exact violations.
7. Retry up to configured limit.
8. Advance only on evidence or record blocker.

**Education:** The runner is useful because it controls workflow order. It is not hard enforcement if users bypass it.

## Phase 5E: Runner Skeleton
**Goal:** Implement the smallest CLI runner skeleton if Phase 5D is approved.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 35k-45k
  expected_tool_calls: 2-4 reads, 2-4 edits, 2-4 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize supported runner commands
  stop_rule: stop if runner needs live model API, MCP, or harness integration
```

**Actions:**
1. Implement read-only commands first, such as `plan-status` and `next-gate`.
2. Implement validation dispatch to the existing CLI validator.
3. Reuse the Next Prompt Compiler when producing phase handoffs.
4. Do not automate model invocation yet.

**Validation:**
- Good task-state fixture reports next gate.
- Bad fixture reports exact missing artifacts.
- Pytest covers pass/fail runner behavior.

## Phase 6A: MCP Adapter Design
**Goal:** Design MCP tools around the same validator core.

```yaml
context_contract:
  executor: human-or-frontier-review
  phase_type: design
  usable_phase_budget: 20k-40k
  expected_tool_calls: 1-3 reads, 1 task artifact edit
  validation_output_budget: brief
  compaction_trigger: summarize tool names and JSON shapes
  stop_rule: stop if MCP design duplicates validation logic
```

**Tools:**
- `validate_requirements`
- `validate_phase_contract`
- `validate_evidence`
- `validate_closeout`
- `validate_domain_pack`
- `compile_next_prompt`
- `next_gate`

## Phase 6B: Harness Adapter Design
**Goal:** Identify hard-blocking opportunities without modifying user-level config.

```yaml
context_contract:
  executor: human-or-frontier-review
  phase_type: design
  usable_phase_budget: 20k-40k
  expected_tool_calls: 1-4 reads, 0-1 task artifact edits
  validation_output_budget: brief capability matrix
  validation_output_reserve: include positive completion evidence for each reviewed harness capability
  compaction_trigger: summarize hard-block vs advisory boundaries
  stop_rule: stop before modifying opencode config or claiming unsupported hard blocking
```

**Validation:**
- Capability matrix labels every gate as hard-blocked, orchestrated, deterministic-only, or human approval.
- Positive completion criterion: every proposed harness gate includes trigger point, enforcement mechanism, validator input, pass behavior, fail behavior, and bypass limitation.
- If no hard-blocking path exists, phase completes with an advisory-only matrix and no config changes.

## Phase 7A: User Documentation Map
**Goal:** Design the user-facing documentation path before writing pages.

```yaml
context_contract:
  executor: human-or-frontier-review
  phase_type: design
  usable_phase_budget: 20k-40k
  expected_tool_calls: 3-6 reads, 1 task artifact edit
  validation_output_budget: brief user journey map
  validation_output_reserve: include docs inventory and gaps summary
  compaction_trigger: summarize target docs, user tasks, and reader path
  stop_rule: stop if docs scope becomes a website implementation project
```

**Inputs:**
- `README.md`
- `docs/`
- `docs/contributing/documentation-style.md`
- `docs/contributing/documentation-review-checklist.md`
- `shared/documentation-quality.md`
- Implemented and planned runtime features from prior phases, labeled by user-visible status.

**Actions:**
1. Inventory existing docs and identify pages to update or create.
2. Define the reader path: README -> quickstart -> choose-a-workflow -> examples -> detailed how-to -> reference.
3. List the primary user jobs: create a plan, run a plan, validate a phase, recover from a blocker, use a domain pack, review examples.
4. Decide which pages are user-facing docs and which remain agent-facing references.
5. Define table-of-contents requirements for every substantial Markdown file.
6. Record website-readiness constraints: stable headings, clear page purpose, examples that can become website sections, and no hidden chat-only context.

**Outputs:**
- User documentation map in `ARTIFACTS.md` or a task artifact referenced from `ARTIFACTS.md`.
- Updated `NEXT_PROMPT.md` naming the first documentation edit phase.

**Validation:**
- Documentation map covers first-value path, use-case lookup, examples, recovery help, and reference details.
- No documentation implementation begins before the map is approved.

## Phase 7B: README Refresh
**Goal:** Update `README.md` so it sells ContextSmith clearly and routes users into the documentation.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 35k-45k
  expected_tool_calls: 3-5 reads, 1 edit, 2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize README narrative, primary calls to action, and changed sections before editing
  stop_rule: stop if README rewrite needs broad product positioning decisions not settled in Phase 7A
```

**Actions:**
1. Keep the README catchy, practical, and concrete.
2. Explain the pain point in user terms: long agent tasks lose requirements, skip validation, or become hard to resume.
3. Explain the benefit in user terms: ContextSmith helps users create clearer plans, run smaller phases, validate evidence, and recover cleanly.
4. Add a short runtime-enforcement section only after features are implemented or clearly label active development.
5. Make README a launchpad to deeper docs.
6. Avoid generic AI copy and repeated contrastive constructions.

**Validation:**
- New users can identify one useful first action in under one minute.
- README links to quickstart, examples, concepts, workflows, and reference docs.
- README does not claim unimplemented runtime adapters as production-ready.
- Documentation style checklist passes.

## Phase 7C: Quickstart And Time-To-First-Value Docs
**Goal:** Create or update quickstart material so users can try ContextSmith quickly.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 35k-45k
  expected_tool_calls: 3-6 reads, 1-3 edits, 2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize the shortest successful user path before editing
  stop_rule: stop if quickstart depends on unimplemented commands or runtime features
```

**Required content:**
- What to install.
- Which skill to use first.
- One prompt-engineering example.
- One implementation-plan example.
- One task-state/run handoff example.
- One audit example.
- Expected outputs and how to judge success.
- A visible `5-minute path` for the quickest useful workflow.
- A visible `next 30 minutes` path for users ready to create a reusable task-state plan.

**Validation:**
- Quickstart has a table of contents.
- Every command or skill invocation is factual for the current repo state.
- The first useful workflow is short and clearly marked.

## Phase 7D: How To Use Runtime Workflows
**Goal:** Create or update one runtime-workflow user guide without widening into the full examples library.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 35k-45k
  expected_tool_calls: 3-5 reads, 1 edit, 2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize user workflow steps before editing
  stop_rule: stop if usage instructions depend on unimplemented commands, unclear feature status, more than one substantial doc edit, or more than five source/doc reads
```

**Required user tasks:**
- Create an implementation plan.
- Choose a domain or fallback workflow.
- Run one phase at a time.
- Validate a phase.
- Read evidence and phase closeout.
- Fix a failed gate.
- Resume from `NEXT_PROMPT.md`.
- Know when human approval is required.

**Concepts to define only as needed:**
- Requirements chain.
- Domain pack.
- Evidence ledger.
- Phase closeout.
- Enforcement levels.

**Validation:**
- File has a table of contents.
- Enforcement levels are accurately labeled.
- Non-coding examples are included.
- Unimplemented adapters are marked as active development or planned work.
- A user can follow the page without understanding the internal architecture.
- If the workflow guide needs multiple pages, record the split in `ARTIFACTS.md` and stop after the first page.

## Phase 7E: Use-Case Workflow Docs
**Goal:** Add a bounded first batch of use-case workflow docs.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 35k-45k
  expected_tool_calls: 3-5 reads, 1-3 edits, 2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize selected workflows before editing
  stop_rule: stop if more than two workflow pages are attempted in one phase, or if any workflow depends on unimplemented tooling without an explicit planned/illustrative label
```

**Starter workflows:**
- Create a small-model implementation plan.
- Run a task-state handoff with validation.
- Build or improve a skill.
- Schedule a meeting with approval gates.
- Compare travel options without purchasing.

**Validation:**
- Each workflow has a table of contents.
- Each workflow includes inputs, commands or prompts, expected artifacts, validation, and common failure modes.
- External actions clearly require human approval.
- Remaining workflow ideas are recorded as deferred, not attempted in the same phase.

## Phase 7F: Examples Library
**Goal:** Add a bounded first batch of examples that users can copy, adapt, and compare.

```yaml
context_contract:
  executor: small-model
  phase_type: implementation
  usable_phase_budget: 35k-45k
  expected_tool_calls: 2-4 reads, 1-2 edits, 2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize example set before editing
  stop_rule: stop if more than three examples are attempted, examples become synthetic claims about unimplemented tooling, or examples need more than two edited files
```

**Example types:**
- Prompt engineering.
- Implementation plan creation.
- Plan audit.
- Task-state run.
- Domain pack use.
- Meeting scheduling.
- Travel comparison.
- Failure and recovery.

**Validation:**
- Examples are labeled as implemented, planned, or illustrative.
- Examples reduce cognitive load by showing expected outputs, not only inputs.
- No example performs an irreversible external action.
- Deferred examples are listed for a later batch instead of expanding this phase.

## Phase 7G: Documentation Quality Audit
**Goal:** Review README and documentation before rollout.

```yaml
context_contract:
  executor: human-or-frontier-review
  phase_type: validation
  usable_phase_budget: 20k-40k
  expected_tool_calls: 4-8 reads, 0-2 edits, 2 validation commands
  validation_output_budget: compact audit findings
  validation_output_reserve: include link/path issues and factuality findings
  compaction_trigger: summarize must-fix docs issues before editing
  stop_rule: stop if docs imply runtime features are complete when they are planned only
```

**Audit checks:**
- README still sells ContextSmith and explains the pain point clearly.
- README routes users into further docs.
- Docs prioritize how to use the system over how the architecture is built.
- Docs include one fastest useful path and several use-case paths.
- Every substantial Markdown doc has a table of contents.
- Docs avoid generic AI marketing and overused contrast patterns.
- Docs are website-ready Markdown with stable headings.
- Docs include enough examples for users to find their use case.
- Active-development features are labeled honestly.
- Documentation reduces cognitive load and time to first value.

## Phase 8A: Rollout Scope Selection
**Goal:** Decide which skills should use the runtime protocol first.

```yaml
context_contract:
  executor: small-model
  phase_type: rollout
  usable_phase_budget: 20k-40k
  expected_tool_calls: 2-5 reads, 1 task-state edit
  validation_output_budget: brief
  validation_output_reserve: include rollout matrix and exact target count
  compaction_trigger: summarize selected skills
  stop_rule: stop if rollout exceeds two skills
```

**Actions:**
1. List every skill as `selected`, `deferred`, or `skipped` with one-line reason.
2. Select an exact rollout target count: `0`, `1`, or `2` skills.
3. Name the exact skill or skills for Phase 8B.
4. If more skills seem eligible, record them as deferred; do not expand Phase 8B.

**Outputs:**
- Rollout matrix in `ARTIFACTS.md` or a task artifact referenced from `ARTIFACTS.md`.
- `STATUS.md` and `NEXT_PROMPT.md` naming the exact Phase 8B target skill or stating no rollout is approved.

**Validation:**
- Matrix explains selected, deferred, and skipped skills.
- No skill files edited in this phase.
- Phase 8B target count is explicit and is not greater than two.

## Phase 8B: Bounded Per-Skill Rollout
**Goal:** Apply the pattern only to the exact skill or skills selected in Phase 8A.

```yaml
context_contract:
  executor: small-model
  phase_type: rollout
  usable_phase_budget: 35k-45k
  expected_tool_calls: 4-8 reads, 1-3 edits, 3-5 validation commands for the selected batch only
  validation_output_budget: brief summaries with reserve for validate_skills, token_budget, pytest, and smoke-test status
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize changed paths and validation
  stop_rule: stop after the Phase 8A target batch; do not start additional skills without a new Phase 8A selection
```

**Inputs:**
- Exact target skill or skills from Phase 8A.
- Pilot integration evidence from Phase 4A.
- Thin-skill writing guide from Phase 4B.
- Documentation quality audit from Phase 7G.

**Actions:**
1. Edit only the Phase 8A target skill or skills.
2. If two skills were selected and the first skill raises context or validation risk, stop after the first and update Phase 8A/`NEXT_PROMPT.md`.
3. Do not start any deferred skill in this phase.

**Validation:**
- `python scripts/validate_skills.py` passes.
- `python scripts/token_budget.py --strict` passes.
- `python -m pytest tests/ -v` passes.
- Installed-workflow smoke test still passes or blocker recorded.
- `ARTIFACTS.md` and `PHASE_LOG.md` list exact changed files and validation evidence.

## Phase 9: Final Closeout Audit
**Goal:** Verify the implementation remains universal, small-model executable, and honest about enforcement limits.

```yaml
context_contract:
  executor: human-or-frontier-review
  phase_type: validation
  usable_phase_budget: 20k-40k
  expected_tool_calls: 2-4 reads, 2-4 validation commands
  validation_output_budget: compact final evidence
  compaction_trigger: summarize evidence before final report
  stop_rule: stop if validation evidence is incomplete or hard enforcement claims exceed evidence
```

**Audit checks:**
- Universal protocol supports coding, writing, research, scheduling, travel/purchase, and fallback.
- Small-model phases stayed atomic.
- Domain packs are compact.
- Pytest validation passes.
- Skills are thinner, not longer.
- CLI/MCP/runner/harness claims are correctly labeled by enforcement level.
- Approval boundaries remain explicit.

## Plan Completion Criteria
- Packaging facts are known before implementation.
- Runtime surface scope is narrowed before coding.
- Universal artifacts are defined before validators.
- Domain packs are data, not hard-coded validator logic.
- Small-model phases never require broad architecture decisions.
- Human/frontier review gates protect architecture choices.
- Pytest tests cover positive and negative cases.
- Installed-workflow smoke test proves runtime checks are usable outside planning context.
- No dependency beyond pytest is added without approval.
- No `PACKAGE_SPEC.md`, user-level opencode config, destructive git operation, or mass migration occurs without approval.
