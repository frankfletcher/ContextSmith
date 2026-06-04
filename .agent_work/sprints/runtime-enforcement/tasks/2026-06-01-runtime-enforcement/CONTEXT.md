# Context: Runtime Enforcement for ContextSmith Skills

## Artifact Manifest
- artifact_type: context
- parent_task: TASK.md
- context_scope: files, constraints, known facts, and skip rules for future sessions
- behavioral_contract: Keep this file compact and factual; do not paste transcripts or full command output.

## Known Facts
- ContextSmith skills currently appear to ship as markdown and YAML assets inside `skills/<skill>/`.
- Existing repo validation is build-time and package-structure oriented.
- Runtime behavior is mostly governed by skill instructions, evidence ledgers, self-audit, and declared-vs-enforced checks.
- Deterministic runtime validation requires executable checks or harness-enforced gates.
- Preliminary script inspection found individual skill packaging and release bundle packaging may include different file sets; Phase 0 must verify both paths before implementation.
- The revised plan treats the runtime as universal infrastructure for skills, agents, and prompts, not only coding skills.
- Pytest is pre-approved by the current user. YAML/PyYAML is not needed for the first runtime slice.

## Files to Inspect in Phase 0
| Path | Purpose |
|---|---|
| `scripts/build_release.py` | Determine release packaging flow |
| `scripts/package_skill.sh` | Determine individual skill zip behavior |
| `scripts/sync_shared_refs.py` | Determine what files enter staged skill packages |
| `scripts/token_budget.py` | Required release validation after skill/reference edits |
| `scripts/` | Find packaging, manifest, sync, and release helpers |
| `skills/contextsmith-run/` | Pilot skill for runtime enforcement |
| `skills/*/reference_manifest.yml` | Understand shipped reference declarations |
| `PACKAGE_SPEC.md` | Read-only design context unless approval is granted |
| `CHANGELOG.md` | User-facing changes if implementation modifies behavior |

## Candidate Runtime Concepts
| Concept | Runtime Role |
|---|---|
| Universal protocol | Shared requirements, phase, evidence, approval, and closeout artifacts |
| Domain pack | Domain-specific validation gates and approval boundaries as compact data |
| Artifact manifest validator | Checks generated artifacts expose required metadata |
| Parameter contract validator | Detects missing values and forbidden widenings |
| Evidence ledger validator | Checks declared obligations have evidence |
| Phase closeout validator | Checks validation status before completion |
| Orchestrated runner | Workflow-level gate loop that advances only after validation passes |
| Next prompt compiler | Generates detailed small-model phase prompts from task state without running the model |
| MCP wrapper | Lets agents call validators as tools |
| Harness gate | Optional hard-blocking integration where supported |

## Constraints
- Do not edit files outside the workspace without explicit approval.
- Do not add dependencies without approval.
- Do not edit `PACKAGE_SPEC.md` design decisions without approval.
- Do not modify user-level opencode configuration without approval.
- Do not claim hard enforcement unless the harness actually blocks bypass.
- Do not start validator implementation until Phase 0.5 records the provisional distribution model.
- Do not start validator implementation until Phase 0.5 records the runtime dependency policy and whether YAML/PyYAML is required, optional, or avoided.
- Do not roll out across more than two skills in one phase without explicit approval.
- Do not carry raw search, validation, or fixture output across phases; compact to facts and commands.
- Small models are enabled for all decisions including broad architecture; human/frontier review is optional for universal protocol, domain-pack strategy, runner design, MCP design, and harness claims.
- Do not describe orchestrated runner behavior as hard enforcement; it only enforces workflows that opt into the runner.
- Do not continue after a blocked phase until the recovery procedure updates STATUS.md, PHASE_LOG.md, ARTIFACTS.md, and NEXT_PROMPT.md.
- Do not execute Phase 8B unless Phase 8A names an exact target count and exact skill or skills.
- Do not execute Phase 8B until ISSUE-1 is resolved: packaging flattening breaks runtime module paths. `sync_shared_refs.py` flattens `local: true` files into `references/`, stripping directory structure. Phase 4A manifest declares `runtime/validator.py`, `runtime/cli.py`, `runtime/__init__.py`, and `runtime/domain_packs/*.json` as local entries. After sync, these become `references/validator.py`, `references/cli.py`, etc., breaking `python -m runtime.cli`. Four resolution options documented in DECISIONS.md.
- Do not let the Next Prompt Compiler execute phases or invoke models; it only generates safe handoff prompts.
- Phase 5B risk (from Phase 5A): the 12-section output template may produce prompts exceeding small-model context for complex phases. Phase 5B must test compiler output against actual task-state fixtures and verify generated prompt size fits within the target profile's usable context budget. If oversized, the compiler should support an `--compact` flag that omits education notes and collapses the phase contract to stop_rule + validation commands only.

## Phase 7A Documentation Map Facts (2026-06-03)
- `USER_DOCS_MAP.md` created with 8 sections: inventory, reader journey, user jobs, user-facing vs agent-facing classification, TOC requirements, website-readiness constraints, phase assignments, and runtime feature labeling.
- Documentation inventory: 14 root-level docs, 8 workflow docs, 3 concept docs, 4 reference docs, 2 contributing docs.
- Identified 8 documentation gaps: runtime enforcement user guide, domain packs guide, Next Prompt Compiler guide, recovery/troubleshooting guide, "create a plan" walkthrough, "run with enforcement" walkthrough, non-coding examples, runner guide.
- Identified duplication issue: several files exist at both `docs/` root and in subdirectories (e.g., `docs/AGENTS_MD_GUIDE.md` and `docs/workflows/AGENTS_MD_GUIDE.md`).
- Reader journey: README -> QUICKSTART -> WHICH_SKILL -> workflows/<specific> -> reference/ -> concepts/.
- Runtime enforcement labeling: implemented (validator CLI, 6 domain packs, Next Prompt Compiler, Runner skeleton, contextsmith-run pilot), active development (MCP adapter design, Harness adapter design), design only (orchestrated runner full implementation, cross-harness benchmarks, automated behavioral tests).

## Phase 7B README Refresh Facts (2026-06-03)
- `README.md` rewritten to follow reader journey from Phase 7A documentation map.
- Added: pain point section, benefit bullets, sub-skills routing table, runtime enforcement section with honest labeling, documentation routing table, table of contents.
- Removed: generic AI marketing language, repeated contrastive constructions, overly detailed parameter reference.
- Runtime enforcement section labels features honestly: Available (validator CLI, 6 domain packs, Next Prompt Compiler, Runner skeleton, contextsmith-run pilot) vs Active development (MCP adapter, harness adapter, orchestrated runner, cross-harness benchmarks).
- Ralph loop: 2 iterations. Iteration 1 added missing TOC. Iteration 2 no-op by evidence.
- Validation: `python scripts/validate_skills.py` passed. Documentation style checklist passes.

## Phase 7C Quickstart Polish Facts (2026-06-03)
- `docs/QUICKSTART.md` rewritten with TOC, 5-minute path, 30-minute path, and polished all 7 paths.
- 5-minute path: install, scan a domain pack, validate an artifact — concrete commands with expected output.
- 30-minute path: "Plan, Audit, Execute" workflow — create AGENTS.md, audit with evaluator, execute with contextsmith-run.
- All paths include expected outputs, concrete examples, and clear next steps.
- Installation prerequisites moved to document header for visibility.
- Links to WHICH_SKILL.md, CONTROL_PARAMETERS.md, and relevant workflow docs verified.
- Ralph loop: 2 iterations. Iteration 1 fixed 30-min path coherence and moved prerequisites upfront. Iteration 2 no-op by evidence.
- Validation: `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.

## Phase 7D Runtime Workflow Docs Facts (2026-06-03)
- `docs/workflows/RUNTIME_ENFORCEMENT.md` created — runtime-workflow user guide covering all 8 required user tasks: create implementation plan, choose domain, run phases, validate, read evidence, fix failed gates, resume from NEXT_PROMPT.md, know when approval required.
- Includes TOC, enforcement levels table (Advisory/Deterministic/Orchestrated/Hard-blocked), quickstart reference, feature labeling (implemented/active development), and non-coding examples with expected outputs.
- Non-coding examples: scheduling a meeting, comparing travel options, editing a document.
- Ralph loop: 2 iterations. Iteration 1 added quickstart reference to intro and expected output to all 3 non-coding examples. Iteration 2 no-op by evidence.
- Validation: `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.

## Phase 7E Use-Case Workflow Docs Facts (2026-06-03)
- `docs/workflows/CREATE_A_PLAN.md` created — step-by-step workflow for creating implementation plans with validation gates, context contracts, and task-state tracking.
- `docs/workflows/BUILD_OR_IMPROVE_A_SKILL.md` created — workflow for creating new skills, adapting for different model profiles, and improving existing skills.
- `docs/workflows/README.md` updated with new entries.
- 3 remaining starter workflows (run task-state handoff, schedule with approval gates, compare travel options) deferred.
- Ralph loop: 2 iterations. Iteration 1 added Next Prompt Compiler reference and budget fix guidance. Iteration 2 no-op by evidence.
- Validation: `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.

## Phase 7F Examples Library Facts (2026-06-03)
- `docs/examples/EXAMPLES_LIBRARY.md` created — 3 examples: (1) Task-State Run (contextsmith-run with NEXT_PROMPT.md), (2) Domain Pack Validation (validator CLI with domain packs), (3) Failure and Recovery (recovery procedure when a phase fails). 5 additional example types deferred.
- All examples labeled as implemented, show expected outputs, and avoid synthetic claims about unimplemented tooling.
- Ralph loop: 2 iterations. Iteration 1: no material defects found. Iteration 2: no-op by evidence.
- Validation: `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.

## Phase 7G Documentation Quality Audit Facts (2026-06-03)
- 6 docs audited: README.md, QUICKSTART.md, RUNTIME_ENFORCEMENT.md, CREATE_A_PLAN.md, BUILD_OR_IMPROVE_A_SKILL.md, EXAMPLES_LIBRARY.md.
- All 6 docs PASS audit. 3 material defects found and fixed.
- Fix 1: QUICKSTART.md 30-min path coherence — Step 2 now audits AGENTS.md instead of IMPLEMENTATION_PLAN.md to match what Step 1 produces.
- Fix 2: README.md directory links changed to point to README.md files for website readiness.
- Fix 3: RUNTIME_ENFORCEMENT.md "quickstart" changed to link `../QUICKSTART.md`.
- Ralph loop: 2 iterations. Iteration 1: no additional defects found. Iteration 2: no-op by evidence.
- Validation: `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.

## Validation Commands
- `python scripts/validate_skills.py` after skill or shared-reference changes.
- `python scripts/token_budget.py --strict` after skill or shared-reference changes.
- `python -m pytest tests/ -v` after runtime validator, domain-pack, CLI, or runner test changes.
- Future runtime validator commands after the validator exists.

## Risk Mitigations
- Packaging uncertainty: Phase 0 verifies individual packages, release bundle, and staged reference sync separately.
- Context overflow: every tool-heavy phase has a context contract, compaction trigger, and stop rule.
- Distribution rework: Phase 0.5 decides the provisional runtime distribution path before implementation.
- Dependency drift: Phase 0.5 decides runtime parsing/dependency policy before Phase 2A; Phase 2A must stop if parser implementation conflicts with that policy.
- Overstated enforcement: every design must label deterministic validation, advisory model behavior, and harness hard-blocking separately.
- Rollout blast radius: Phase 6 is split into scope selection and per-batch rollout.
- Validation gaps: fixture checks must include passing and failing cases before skill integration.
- Architecture sweep risk: phases are split into small-model implementation slices and optional human/frontier review gates.
- Generality risk: starter domain packs must cover software, writing, research, scheduling, travel/purchase, and general fallback before rollout.
- Rollout scope creep: Phase 8A must name an exact target count, and Phase 8B cannot touch deferred skills.
- Smoke-test fragility: if packaging cannot carry runtime files, Phase 2E records a fallback path instead of redesigning packaging mid-phase.
- Handoff drift: every phase closeout records carry-forward and do-not-carry-forward notes.
- Handoff quality: Next Prompt Compiler creates detailed phase prompts with validation, audit, closeout, recovery, and hard-stop sections.
- Documentation drift: docs phases focus on user tasks, examples, time to first value, and lookup paths; architecture details appear only when they help users operate the system.

## Documentation Direction
- README should be catchy, practical, and clear about the pain point.
- README should act as the front door to quickstart, workflows, examples, and reference docs.
- User docs should teach how to use ContextSmith, not primarily explain internal architecture.
- Substantial Markdown docs should include a table of contents and stable headings for future website generation.
- Examples should show expected outputs and recovery paths, not only commands.

## Phase 0 Packaging Facts (2026-06-02)

### Individual skill zip (`package_skill.sh`)
1. Syncs references via `sync_shared_refs.py --skill <name>` into `.agent_work/staged_skills/<name>/`
2. Generates `MANIFEST.json` (sha256 checksums for every staged file)
3. Zips from staging, excluding `reference_manifest.yml` and `references/.gitkeep`
4. **Zip contents**: `SKILL.md`, `MANIFEST.json`, and all manifest-declared references under `references/`
5. Skill-root local files (e.g., `execution-contract.md`) are NOT included unless declared as `local: true` in the manifest — they end up under `references/`, not at the skill root
6. Evidence: `package_skill.sh:48-121`, `sync_shared_refs.py:43-111`

### Release bundle (`build_release.py step_bundle`)
1. Stages `README.md`, `CHANGELOG.md`, `docs/`, and `skills/<name>/SKILL.md` into `.agent_work/release_bundle/`
2. Runs `sync_shared_refs.py --all --staging-dir <bundle>/skills/` to populate references
3. Walks entire staging tree into `contextsmith-release.zip`
4. **Bundle contents**: top-level files, all docs, SKILL.md + synced references for each skill
5. Evidence: `build_release.py:256-345`

### Staging sync behavior (`sync_shared_refs.py`)
- Copies SKILL.md into staging (line 44-51)
- Iterates `reference_manifest.yml` entries; copies only `required: true` entries (line 60)
- Non-local sources must start with `shared/` (line 66-68)
- Local sources (`local: true`) copy by basename into `references/` (line 86-88)
- Non-local sources preserve subdirectory structure under `references/` (line 90-91)
- **Does NOT copy arbitrary files** — only manifest-declared references
- No file-type filtering: any file declared in the manifest can be copied
- Evidence: `sync_shared_refs.py:28-113`

### Can runtime files ship?
| File type | Can ship? | How |
|---|---|---|
| Executable `.py` / `.sh` | Yes, if added to `reference_manifest.yml` | Declare as `local: true` (skill-root) or `shared/` source |
| YAML schemas (`.yml`) | Yes, if added to manifest | Same mechanism |
| Fixtures (`.yml`, `.json`) | Yes, if added to manifest | Same mechanism |
| Domain packs (`.yml`) | Yes, if added to manifest | Same mechanism |
| `reference_manifest.yml` itself | **Excluded** from zip | `package_skill.sh:119` explicitly excludes it |

### Key constraint
The sync script is manifest-driven, not directory-driven. Any new file type (`.py`, `.yml`, `.json`) must be explicitly declared in each skill's `reference_manifest.yml` to ship. There is no wildcard or directory-sweep behavior.

### Separate runtime package likely needed?
The manifest mechanism can carry runtime files, but adding Python executables and YAML schemas to every skill's manifest would be repetitive. A separate `contextsmith-runtime` package (or a `shared/runtime/` directory with its own manifest) would avoid duplication. This is a Phase 0.5 decision.

### Phase 0.5 Decisions (2026-06-02)
- **Decision 1**: Hybrid enforcement — repo validation AND installed-skill enforcement.
- **Decision 4**: Pilot skills — `contextsmith-run` and `contextsmith-prompt-engineer`.
- **Decision 6**: Small model enabled for everything; frontier model optional.
- **Decision 8**: Per-skill manifest entries — runtime files declared in each skill's `reference_manifest.yml`, same as shared references.
- **Decision 9**: stdlib-only JSON for the first runtime slice; YAML/PyYAML deferred.
- **Decision 10**: Full stack first slice — CLI + MCP + runner + harness + domain packs, incremental testing OK.

## Phase Token Budgets (Actuals)
| Phase | Estimated | Actual | Notes |
|---|---|---|---|
| Phase 0 | 40k-60k | 78k | Discovery: 4-8 reads, 1 dry-run, 0 edits. Exceeded due to accumulated system/AGENTS.md/PLAN.md overhead. Use as baseline for discovery phases. |
| Phase 3C | 25k-40k | unavailable | Proxy: 11 task/source reads, 4 source/test edits, 5 task-state edits, 8 validation commands. Stayed within phase scope; no calendar APIs or external sends. |
| Phase 3D | 25k-40k | unavailable | Proxy: 10 task/source reads, 3 source/test edits, 5 task-state edits, 5 validation commands. Stayed within phase scope; no booking APIs, purchases, payments, or external reservations. |
| Phase 3E | 25k-40k | unavailable | Proxy: 11 task/source reads, 3 source/test edits, 5 task-state edits, 7 validation commands. Stayed within phase scope; no external sending, publishing, submitting, or representing text as final. |
| Phase 3F | 25k-40k | unavailable | Proxy: 10 task/source reads, 3 source/test edits, 5 task-state edits, 5 validation commands. Stayed within phase scope; no live browsing, citation scraping, publication, submission, or external citation workflow. |
| Phase 3G | 20k-40k | unavailable | Proxy: 10 task/source reads, 4 source/test edits, 6 task-state edits, 9 validation commands. Stayed within review scope; no new domains, runner, MCP, harness, or skill integration edits. |

## Phase 3G Domain Pack Review Facts (2026-06-02)
- All six starter domain packs remain compact JSON data artifacts (52-58 lines each).
- All `requires_approval` external action boundaries have matching `approval_gates` entries.
- Deterministic checks and human confirmation checks are separated by explicit `check_type` values; human confirmation gates also have approval/boundary coverage.
- `general_fallback` now uses `triggers: ["*"]` so it can handle unknown domains without domain-specific claims.
- `validate_domain_pack()` now enforces schema rule 10 for the `general_fallback` wildcard trigger.
- No new domain packs were created in Phase 3G.

## Open Questions
- Should runtime files be declared per-skill in each `reference_manifest.yml`, or shipped as a separate package? — Resolved: per-skill manifest entries (Decision 8, 2026-06-02).
- Which runtime surfaces belong in the first implementation slice? — Resolved: full stack (Decision 10, 2026-06-02).
- Can opencode require a successful validator call before finalization or risky actions?

## Phase 6B Harness Adapter Design Facts (2026-06-02)
- HARNESS_ADAPTER_DESIGN.md created with 213 lines.
- 7 gates mapped to opencode capabilities: Phase Boundary, Validator Gate, Context Budget, Side Effect, Rollout Scope, Recovery, Distribution.
- Enforcement classifications: 1 hard-blocked (Gate 4 via tool deny), 4 orchestrated (custom tools), 1 deterministic-only (Gate 7), 1 human approval (Gate 4 ask mode).
- Capability matrix covers: tool allow/ask/deny permissions, experimental policies, custom tool overrides for `edit`/`read`/`write`/`shell`.
- Key finding: opencode can hard-block destructive git operations via tool deny policy. Other gates require orchestrated enforcement or human approval.
- Key finding: advisory-only enforcement is sufficient for most gates; hard blocking only needed for side-effect tier 3+ actions.
- Ralph loop: 2 iterations. Iteration 1 identified 3 design-quality defects for carry-forward: (1) Gate 2 circular validation: wrapping shell could block validation commands, (2) Gate 7 classification mismatch: "Deterministic-only" label conflicts with "Custom tool" mechanism, (3) custom tool bypass gap: missing analysis for alternative tool names and aliases. Iteration 2: no-op by evidence.
- Design does not modify user-level config or claim unsupported hard blocking.
- Packaging notes: `runtime/harness_config.json` would need manifest declaration for distribution.
- ISSUE-1 (packaging flattening) remains unresolved; blocks Phase 8B rollout.

## Phase 8A Rollout Scope Selection Facts (2026-06-03)
- Rollout matrix created for all 7 ContextSmith skills.
- `contextsmith` skipped: meta-skill router, no direct execution.
- `contextsmith-run` selected: already integrated in Phase 4A pilot.
- `contextsmith-prompt-engineer` selected: Decision 4 pilot candidate, Phase 8B target.
- `contextsmith-skill-engineer` deferred: Phase 8C+.
- `contextsmith-skill-migrator` deferred: Phase 8C+.
- `contextsmith-instruction-engineer` deferred: Phase 8C+.
- `contextsmith-agent-evaluator` deferred: Phase 8C+.
- Phase 8B target count: 1 skill (`contextsmith-prompt-engineer`).
- ISSUE-1 resolution path: Option 3 (extend `sync_shared_refs.py` to preserve directory structure for `local: true` entries).
- Validation: `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.
- Ralph loop: 2 iterations (iteration 1: no material defects; iteration 2: no-op by evidence).

## Phase 8C Sub-Phases Plan (2026-06-03)
- Phase 7E deferred 3 workflow docs; Phase 7F deferred 5 examples. Renumbered as Phase 8C.1-8C.11 to execute after skill rollout (Phase 8B), so docs reflect actual rolled-out skill behavior, not projected capabilities.
- Phase 8C.1: Run task-state handoff workflow doc.
- Phase 8C.2: Schedule with approval gates workflow doc.
- Phase 8C.3: Compare travel options workflow doc.
- Phase 8C.4: Prompt engineering example.
- Phase 8C.5: Implementation plan creation example.
- Phase 8C.6: Plan audit example.
- Phase 8C.7: Meeting scheduling example.
- Phase 8C.8: Travel comparison example.
- Phase 8C.9: Skill migration example.
- Phase 8C.10: Custom domain pack example.
- Phase 8C.11: Agent evaluation example.
- Each sub-phase bounded to one doc or one example. Max 35k-45k context budget. Ralph loop: 2 iterations per phase.
- Validation per phase: `python scripts/validate_skills.py`, `python scripts/token_budget.py --strict`.

## Phase 8C.1 Run Task-State Handoff Workflow Doc Facts (2026-06-03)
- `docs/workflows/RUN_TASK_STATE_HANDOFF.md` created — 99 lines, follows CREATE_A_PLAN.md / BUILD_OR_IMPROVE_A_SKILL.md pattern.
- Covers: when to use, inputs, 5 steps (locate task state, read NEXT_PROMPT.md, invoke contextsmith-run, validate, review updated state), expected artifacts table, common failure modes table.
- Cross-references EXAMPLES_LIBRARY.md Example 1 and CREATE_A_PLAN.md.
- `docs/workflows/README.md` updated with new entry.
- Ralph loop: 2 iterations. Iteration 1 added EXAMPLES_LIBRARY.md cross-reference. Iteration 2 no-op by evidence.
- Validation: `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.

## Phase 8C.2 Schedule with Approval Gates Workflow Doc Facts (2026-06-03)
- `docs/workflows/SCHEDULE_WITH_APPROVAL_GATES.md` created — 95 lines, follows CREATE_A_PLAN.md / BUILD_OR_IMPROVE_A_SKILL.md pattern.
- Covers: when to use, inputs, 5 steps (define approval boundaries, invoke with gates, review actions, approve/reject, validate), expected artifacts table, common failure modes table.
- Cross-references RUN_TASK_STATE_HANDOFF.md and shared/side-effect-matrix.md.
- `docs/workflows/README.md` updated with new entry.
- Ralph loop: 2 iterations. Iteration 1 refined example prompt and added file paths to expected artifacts. Iteration 2 no-op by evidence.
- Validation: `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.

## Phase 8C.3 Compare Travel Options Workflow Doc Facts (2026-06-03)
- `docs/workflows/COMPARE_TRAVEL_OPTIONS.md` created — 106 lines, follows CREATE_A_PLAN.md / BUILD_OR_IMPROVE_A_SKILL.md pattern.
- Covers: when to use, inputs, 5 steps (define constraints, invoke with travel domain, review options, validate no external actions, finalize with evidence), expected artifacts table, common failure modes table.
- Cross-references SCHEDULE_WITH_APPROVAL_GATES.md and shared/side-effect-matrix.md.
- `docs/workflows/README.md` updated with new entry.
- Ralph loop: 2 iterations. Iteration 1 removed stale EXAMPLES_LIBRARY.md cross-reference to deferred example. Iteration 2 no-op by evidence.
- Validation: `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.

## Phase 8C.4 Prompt Engineering Example Facts (2026-06-03)
- `docs/examples/EXAMPLES_LIBRARY.md` updated with Example 4 (Prompt Engineering). Follows established example pattern with Status, Scenario, Input, Prompt, What happens (7 steps), Expected output, and Recovery.
- Example shows contextsmith-prompt-engineer invocation with --target-profile, --domain, and --ralph flags.
- Expected output includes Engineering Metadata, System Prompt, User Prompt Template, Context Strategy, Validation and Test Plan, Ralph Summary, and Risks sections.
- Prompt engineering removed from Deferred Examples section (3 remaining: plan audit, meeting scheduling, travel comparison).
- Ralph loop: 2 iterations. Iteration 1: no material defects. Iteration 2: no-op by evidence.
- Validation: `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.

## Phase 8C.5 Implementation Plan Creation Example Facts (2026-06-03)
- `docs/examples/EXAMPLES_LIBRARY.md` contains Example 5 (Implementation Plan Creation). Follows established example pattern with Status, Scenario, Input, Prompt, What happens (7 steps), Expected output, and Recovery.
- Example shows contextsmith-instruction-engineer invocation for creating a phased implementation plan with validation gates for a unittest-to-pytest migration.
- Expected output includes Detected Project Profile, Changes Made, Safeguards Reused/Strengthened/Added, Validation Notes, Ralph Summary, Remaining Risks, and Files Written sections.
- Implementation plan creation removed from Deferred Examples section (3 remain: plan audit, meeting scheduling, travel comparison).
- Ralph loop: 2 iterations. Iteration 1: no material defects. Iteration 2: no-op by evidence.
- Validation: `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.
