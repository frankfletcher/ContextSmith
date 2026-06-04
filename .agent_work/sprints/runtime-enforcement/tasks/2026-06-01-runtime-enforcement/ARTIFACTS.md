# Artifacts: Runtime Enforcement for ContextSmith Skills

## Artifact Manifest
- artifact_type: artifact-index
- parent_task: TASK.md
- status: Phase 8C.5 complete (Implementation Plan Creation Example)
- behavioral_contract: Track generated files, future source changes, and validation evidence.

## Task-State Files
| File | Purpose | Status |
|---|---|---|
| `TASK.md` | Objective, scope, constraints | Created |
| `PLAN.md` | Phased implementation plan | Created |
| `STATUS.md` | Current phase and next action | Created |
| `DECISIONS.md` | Durable decisions and pending decisions | Created |
| `CONTEXT.md` | File map, constraints, open questions | Created |
| `CHECKLIST.md` | Planning and implementation audit checklist | Created |
| `ARTIFACTS.md` | Artifact index | Created |
| `PHASE_LOG.md` | Compact phase history | Created |
| `NEXT_PROMPT.md` | Resume prompt | Created |

## Future Implementation Artifacts
| Artifact | Expected Phase | Status |
|---|---:|---|
| Packaging discovery notes | 0 | Complete — recorded in CONTEXT.md and DECISIONS.md |
| Runtime surface decision matrix | 0.5 | Complete — recorded in DECISIONS.md |
| Runtime dependency policy | 0.5 | Complete — stdlib-only JSON for the first slice; YAML deferred, recorded in DECISIONS.md |
| Universal artifact vocabulary | 1A | Complete — `ARTIFACT_VOCABULARY.md` |
| Requirements chain schema | 1B | Complete — `REQUIREMENTS_CHAIN_SCHEMA.md` |
| Approval record schema | 1B.5 | Complete — `APPROVAL_RECORD_SCHEMA.md` |
| Domain pack schema | 1C | Complete — `DOMAIN_PACK_SCHEMA.md` |
| Architecture review notes | 1D | Complete — recorded in DECISIONS.md (Decision 18) |
| Minimal validator core | 2A | Complete — `runtime/validator.py`, `runtime/__init__.py`, `tests/test_validator.py`, `tests/fixtures/` |
| Domain pack validator | 2B | Complete — enhanced `runtime/validator.py` with Rule 3 and Rule 8; 6 new fixtures, 7 new tests |
| CLI adapter | 2C | Complete — `runtime/cli.py`, `tests/test_cli.py` |
| Pytest fixture tests | 2D | Complete — 17 new fixtures, 24 new tests, 1 validator bug fix |
| Installed-workflow smoke test | 2E | Complete — smoke test evidence below |
| Starter domain packs | 3A-3F | Complete — `runtime/domain_packs/general_fallback.json`, `runtime/domain_packs/software_engineering.json`, `runtime/domain_packs/scheduling.json`, `runtime/domain_packs/travel_purchase.json`, `runtime/domain_packs/writing_editing.json`, `runtime/domain_packs/research_summary.json` |
| Domain pack review notes | 3G | Complete — recorded in STATUS.md, CONTEXT.md, CHECKLIST.md, and PHASE_LOG.md |
| Phase 3 audit report | 3A-3G | Complete — `PHASE_3_AUDIT.md` |
| `contextsmith-run` pilot integration | 4A | Complete — `skills/contextsmith-run/SKILL.md`, `skills/contextsmith-run/reference_manifest.yml` |
| Thin-skill writing guide | 4B | Complete — `THIN_SKILL_WRITING_GUIDE.md` |
| Next Prompt Compiler specification | 5A | Complete — `NEXT_PROMPT_COMPILER_SPEC.md` |
| Next Prompt Compiler implementation | 5B | Complete — `runtime/next_prompt_compiler.py`, `runtime/cli.py` (updated), `tests/test_next_prompt_compiler.py` |
| Next Prompt Compiler tests | 5C | Complete — 28 new tests in `tests/test_next_prompt_compiler.py` (55 total) |
| CLI integration tests | 5D | Complete — `tests/test_cli_integration.py` with 45 tests covering all 6 domain packs, exit codes, output format, cross-validator workflows, edge cases, multiple artifacts, and programmatic API
| Runner skeleton | 5E | Complete — `runtime/runner.py` with `plan_status()` and `next_gate()` commands, updated `runtime/cli.py`, `tests/test_runner.py` with 8 tests, `RUNNER_SPECIFICATION.md`
| MCP adapter design | 6A | Complete — `MCP_ADAPTER_DESIGN.md` |
| Harness adapter design | 6B | Complete — `HARNESS_ADAPTER_DESIGN.md` |
| Phase 6 audit report | 6A-6B | Complete — `PHASE_6_AUDIT.md` |
| User documentation map | 7A | Complete — `USER_DOCS_MAP.md` |
| README refresh | 7B | Complete — `README.md` rewritten with reader journey, pain point, benefits, sub-skills table, runtime enforcement section, documentation routing, and TOC |
| Quickstart and time-to-first-value docs | 7C | Complete — `docs/QUICKSTART.md` rewritten with TOC, 5-min path, 30-min path, polished paths with expected outputs |
| Runtime workflow usage docs | 7D | Complete — `docs/workflows/RUNTIME_ENFORCEMENT.md` |
| Use-case workflow docs | 7E | Complete — `docs/workflows/CREATE_A_PLAN.md`, `docs/workflows/BUILD_OR_IMPROVE_A_SKILL.md` |
| Examples library | 7F | Complete — `docs/examples/EXAMPLES_LIBRARY.md` |
| Documentation quality audit | 7G | Complete — 6 docs audited, 3 targeted fixes applied |
| ISSUE-1 fix: sync_shared_refs.py | 8B | Complete — preserves directory structure for `local: true` entries |
| Sync shared refs regression tests | 8B | Complete — `tests/test_sync_shared_refs.py` with 3 tests |
| `contextsmith-prompt-engineer` runtime manifest | 8B | Complete — 10 runtime file entries added |
| `contextsmith-prompt-engineer` runtime SKILL.md | 8B | Complete — runtime validation section (step 8) added |
| `contextsmith-agent-evaluator` runtime manifest | 8B4 | Complete — 10 runtime file entries added |
| `contextsmith-agent-evaluator` runtime SKILL.md | 8B4 | Complete — runtime validation section (step 8) added |
| Prompt engineering example | 8C.4 | Complete — Example 4 added to `docs/examples/EXAMPLES_LIBRARY.md` |
| Implementation plan creation example | 8C.5 | Complete — Example 5 in `docs/examples/EXAMPLES_LIBRARY.md` |

## Validation Evidence
- 2026-06-01: `python scripts/validate_skills.py` passed. Output reported all 7 skills OK and `Validation complete`.
- 2026-06-01: Implementation plan audit completed; plan refined to add context contracts, split rollout, token-budget validation, recovery rules, and a distribution decision gate.
- 2026-06-01: Post-refinement validation passed: `python scripts/validate_skills.py` and `python scripts/token_budget.py --strict`.
- 2026-06-01: Plan rewritten for universal skill/agent/prompt runtime enforcement, domain packs, pytest-approved tests, small-model implementation phases, and human/frontier review gates.
- 2026-06-01: Post-rewrite validation passed: `python scripts/validate_skills.py` and `python scripts/token_budget.py --strict`.
- 2026-06-01: Plan audit refinements added: recovery procedure, required closeout/debrief, Phase 2E fallback path, Phase 4A validation reserve, Phase 6B completion criteria, and bounded rollout semantics.
- 2026-06-01: Post-audit-refinement validation passed: `python scripts/validate_skills.py` and `python scripts/token_budget.py --strict`.
- 2026-06-01: Documentation workstream added before rollout; clarified docs should focus on how to use ContextSmith rather than explaining architecture internals.
- 2026-06-01: Post-documentation-workstream validation passed: `python scripts/validate_skills.py` and `python scripts/token_budget.py --strict`.
- 2026-06-01: Next Prompt Compiler phases added before orchestrated runner so detailed small-model handoff prompts can be generated automatically.
- 2026-06-01: Post-compiler-plan validation passed: `python scripts/validate_skills.py` and `python scripts/token_budget.py --strict`.
- 2026-06-02: Phase 0 validation: `python scripts/validate_skills.py` passed (7 skills OK). `python scripts/token_budget.py --strict` passed (all 7 skills within budget). `python scripts/build_release.py --package --dry-run` completed successfully.
- 2026-06-02: Granular-plan review fixes applied: small-model budgets capped for 64k context, approval-record validation path added, writing/research domain-pack phases added, and stale rollout references corrected to Phase 8.
- 2026-06-02: Post-granular-plan-fix validation passed: `python scripts/validate_skills.py` and `python scripts/token_budget.py --strict`.
- 2026-06-02: Audit-level plan fixes applied: Phase 0.5 now includes distribution model, dependency policy, first-slice scope, and Phase 1A authorization; Phase 2A obeys dependency policy; documentation and examples phases are bounded to smaller batches.
- 2026-06-02: Post-audit-level-fix validation passed: `python scripts/validate_skills.py` and `python scripts/token_budget.py --strict`.
- 2026-06-02: Phase 1A artifact vocabulary created: `ARTIFACT_VOCABULARY.md` with six artifact types, each with purpose, required fields, and a domain-neutral JSON example. All JSON examples validated.
- 2026-06-02: Phase 1B requirements chain schema created: `REQUIREMENTS_CHAIN_SCHEMA.md` with eight required fields, linear trace model, four-step trace example, validation rules, and deferred YAML documentation. All JSON examples validated.
- 2026-06-02: Phase 1B.5 approval record schema created: `APPROVAL_RECORD_SCHEMA.md` with ten required fields, status semantics table, three-step travel purchase example, 12 validation rules, and deferred YAML documentation. All JSON examples validated.
- 2026-06-02: Phase 1C domain pack schema created: `DOMAIN_PACK_SCHEMA.md` with seven required fields, two optional fields, six starter domain packs, good/blocked closeout examples, 10 validation rules, and deferred YAML documentation. All 10 JSON examples validated.
- 2026-06-02: Phase 1D architecture review completed: four review questions all pass. One correction (software_engineering approval_gates consistency), one documentation gap (phase_contract and evidence_ledger schema files), one design note (deterministic vs content checks). Recorded in `DECISIONS.md`.
- 2026-06-02: Phase 2A minimal validator core created: `runtime/validator.py` with 6 validators and cross-artifact `validate_workflow()`. 13 test fixtures in `tests/fixtures/`. 26 pytest tests in `tests/test_validator.py`. All tests pass. `python scripts/validate_skills.py` passes. `python scripts/token_budget.py --strict` passes.
- 2026-06-02: Phase 2B domain pack validator enhanced: `runtime/validator.py` updated with Rule 3 (required_artifacts vocabulary) and Rule 8 (residual_risk non-empty). 6 new fixtures in `tests/fixtures/`. 7 new tests in `tests/test_validator.py`. All 32 tests pass. `python scripts/validate_skills.py` passes. `python scripts/token_budget.py --strict` passes.
- 2026-06-02: Phase 2C CLI adapter created: `runtime/cli.py` with 6 subcommands, exit codes, compact output, and `--help`. 25 new tests in `tests/test_cli.py`. All 57 tests pass. `python scripts/validate_skills.py` passes. `python scripts/token_budget.py --strict` passes.
- 2026-06-02: Phase 2D pytest fixture tests expanded: 17 new fixtures in `tests/fixtures/`, 24 new tests in `tests/test_validator.py` (+4) and `tests/test_cli.py` (+2). Validator bug fix: `runtime/validator.py:85` empty source detection (`not isinstance` → `isinstance`). All 81 tests pass. `python scripts/validate_skills.py` passes. `python scripts/token_budget.py --strict` passes.
- 2026-06-02: Phase 2E installed-workflow smoke test passed: staged `contextsmith-run` skill, copied runtime files to `.agent_work/staged_skills/contextsmith-run/runtime/`, invoked CLI from staged path. `--help` works, domain_pack PASS (valid fixture) and FAIL (invalid_domain fixture) both succeed from staged directory. No packaging redesign required. All 81 tests pass. `python scripts/validate_skills.py` passes. `python scripts/token_budget.py --strict` passes.
- 2026-06-02: Phase 3A general fallback domain pack complete: created `runtime/domain_packs/general_fallback.json`, `tests/fixtures/domain_pack_general_fallback.json`, and validator tests for both. `python -m runtime.cli domain-pack runtime/domain_packs/general_fallback.json` passed. `python -m runtime.cli domain-pack tests/fixtures/domain_pack_general_fallback.json` passed. All 85 pytest tests pass. `python scripts/validate_skills.py` passes. `python scripts/token_budget.py --strict` passes.
- 2026-06-02: Phase 3B software engineering domain pack complete: created `runtime/domain_packs/software_engineering.json`, `tests/fixtures/domain_pack_software_engineering.json`, and validator tests for both. `python -m runtime.cli domain-pack runtime/domain_packs/software_engineering.json` passed. `python -m runtime.cli domain-pack tests/fixtures/domain_pack_software_engineering.json` passed. All 87 pytest tests pass. `python scripts/validate_skills.py` passes. `python scripts/token_budget.py --strict` passes.
- 2026-06-02: Phase 3C scheduling domain pack complete: created `runtime/domain_packs/scheduling.json`, `tests/fixtures/domain_pack_scheduling.json`, and validator tests for both. `python runtime/cli.py domain-pack runtime/domain_packs/scheduling.json` passed. `python runtime/cli.py domain-pack tests/fixtures/domain_pack_scheduling.json` passed. All 89 pytest tests pass. `python scripts/validate_skills.py` passes. `python scripts/token_budget.py --strict` passes.
- 2026-06-02: Phase 3D travel/purchase domain pack complete: created `runtime/domain_packs/travel_purchase.json`, `tests/fixtures/domain_pack_travel_purchase.json`, and validator tests for both. `python -m runtime.cli domain-pack runtime/domain_packs/travel_purchase.json` passed. `python -m runtime.cli domain-pack tests/fixtures/domain_pack_travel_purchase.json` passed. All 91 pytest tests pass. `python scripts/validate_skills.py` passes. `python scripts/token_budget.py --strict` passes.
- 2026-06-02: Phase 3E writing/editing domain pack complete: created `runtime/domain_packs/writing_editing.json`, `tests/fixtures/domain_pack_writing_editing.json`, and validator tests for both. `python -m runtime.cli domain-pack runtime/domain_packs/writing_editing.json` passed. `python -m runtime.cli domain-pack tests/fixtures/domain_pack_writing_editing.json` passed. All 93 pytest tests pass. `python scripts/validate_skills.py` passes. `python scripts/token_budget.py --strict` passes.
- 2026-06-02: Phase 3F research summary domain pack complete: created `runtime/domain_packs/research_summary.json`, `tests/fixtures/domain_pack_research_summary.json`, and validator tests for both. `python -m runtime.cli domain-pack runtime/domain_packs/research_summary.json` passed. `python -m runtime.cli domain-pack tests/fixtures/domain_pack_research_summary.json` passed. All 95 pytest tests pass. `python scripts/validate_skills.py` passes. `python scripts/token_budget.py --strict` passes.
- 2026-06-02: Phase 3G domain pack review complete: reviewed all six starter packs; corrected `general_fallback` to `triggers: ["*"]`; added `validate_domain_pack()` enforcement and pytest coverage for rule 10. `python -m pytest tests/ -v` passed with 96 tests. `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed. CLI validation passed for all six runtime domain packs.
- 2026-06-02: Phase 3 audit complete: all six starter domain packs pass schema compliance, plan compliance, and Rule 9 approval boundary alignment. Audit verdict: PASS. Created `PHASE_3_AUDIT.md` with detailed findings.
- 2026-06-02: Phase 4A ContextSmith-Run Pilot Integration complete: updated `contextsmith-run` SKILL.md with runtime-checkable artifact integration. Added "Runtime Validators" subsection to Validation Gate section, "Runtime Artifacts" subsection to Evidence Ledger section, and runtime validation step (step 9) to Execution Workflow. Updated `reference_manifest.yml` with 10 local entries for runtime files. SKILL.md at 328 lines, 3979 tokens (within 4000 budget). `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed. `python -m pytest tests/ -v` passed (96 tests). Ralph loop: 2 iterations, both no-op by evidence.
- 2026-06-02: Phase 4B Thin-Skill Writing Guide complete: created `THIN_SKILL_WRITING_GUIDE.md` with five patterns, checklist, Phase 4A example, and escalation path. 113 lines, compact and practical. `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed. `python -m pytest tests/ -v` passed (96 tests). Ralph loop: 2 iterations, iteration 1 added budget target to checklist, iteration 2 no-op by evidence.
- 2026-06-02: Phase 5A Next Prompt Compiler Specification complete: created `NEXT_PROMPT_COMPILER_SPEC.md` with 12-section output template, input specification, CLI interface design, Markdown fence safety rules, 7 hard-stop rules, and verification table. 197 lines, compact and design-focused. `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed. `python -m pytest tests/ -v` passed (96 tests). Ralph loop: 2 iterations, iteration 1 narrowed phase contract to executor-relevant fields and added STATUS/PLAN disagreement error rule, iteration 2 no-op by evidence.
- 2026-06-02: Phase 5B Next Prompt Compiler Implementation complete: created `runtime/next_prompt_compiler.py` with `compile_next_prompt()` and `compile_next_prompt_cli()`. Updated `runtime/cli.py` with `next-prompt` subcommand. Created 27 pytest tests in `tests/test_next_prompt_compiler.py`. Created 3 test fixtures. Compiler generates all 12 required sections from Phase 5A spec. Supports `--dry-run`, `--compact`, `--include-education`, `--phase`, and `--output` flags. `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed. `python -m pytest tests/ -v` passed (123 tests). Ralph loop: 2 iterations, iteration 1 fixed fixture files and test expectations, iteration 2 no-op by evidence.
- 2026-06-02: Phase 5C Next Prompt Compiler Tests complete: expanded test coverage from 27 to 55 tests (+28) with `TestEdgeCases` (24 tests: last phase hard stop, empty phase block, YAML context contract, phase title in mission, context validation/constraints, compact mode, education with/without content, phase override, balanced fences, no execute instructions, stop rule, read order, closeout files, recovery steps, self-audit items, artifact manifest, optional files, hard stop phase, prompt size budget, STATUS/PLAN disagreement, --output flag content match) and `TestIntegrationActualTaskState` (4 tests: all sections, balanced fences, hard stop boundaries, education flag). Ralph loop: 2 iterations, iteration 1 fixed 2 weak assertions and added 3 new tests, iteration 2 no-op by evidence. `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed. `python -m pytest tests/ -v` passed (151 tests).
- 2026-06-02: Phase 6A MCP Adapter Design complete: created `MCP_ADAPTER_DESIGN.md` with tool catalog (7 tools from PLAN.md + `plan_status` bonus), JSON-RPC schemas, dispatch function, wrapper patterns, server integration modes, path resolution, batch validation guidance, error handling, and packaging notes. Design wraps existing runtime functions without duplicating validation logic. Ralph loop: 2 iterations, iteration 1 added path resolution, batch validation, and error handling sections, iteration 2 corrected `compile_next_prompt` wrapper and added `output` parameter. `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed. `python -m pytest tests/ -v` passed (204 tests).
- 2026-06-02: Phase 6B Harness Adapter Design complete: created `HARNESS_ADAPTER_DESIGN.md` with opencode capabilities analysis, harness capability matrix (7 gates), enforcement classification summary, key findings, integration points, and packaging notes. Design identifies hard-blocking opportunities without modifying user-level config. Ralph loop: 2 iterations, iteration 1 identified 3 design-quality defects for Phase 6C carry-forward (Gate 2 circular validation, Gate 7 classification mismatch, custom tool bypass gap), iteration 2 no-op by evidence. `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed. `python -m pytest tests/ -v` passed (204 tests).
- 2026-06-02: Phase 6A/6B A-F rubric audit complete: initial grades 6A=B+, 6B=B. Applied targeted fixes to raise both to A. Phase 6A fixes: dispatch registry mapping, `validate_all` batch tool, path resolution rules, tool versioning, implementation test strategy. Phase 6B fixes: Gate 2 circular validation resolved (whitelist), Gate 7 classification corrected (structural validator), bypass analysis table, Ralph loop history, packaging manifest entries, gate priority ordering, implementation test strategy. Post-audit grades: 6A=A, 6B=A. `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed. `python -m pytest tests/ -v` passed (204 tests).
- 2026-06-03: Phase 7A User Documentation Map complete: created `USER_DOCS_MAP.md` with documentation inventory, reader journey, user jobs, user-facing vs agent-facing classification, TOC requirements, website-readiness constraints, phase assignments, and runtime feature labeling. Identified 8 documentation gaps and duplication issue between root-level and subdirectory docs. `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed. Ralph loop: 2 iterations, both no-op by evidence.
- 2026-06-03: Phase 7B README Refresh complete: rewrote `README.md` with reader journey from Phase 7A documentation map. Added pain point section, benefit bullets, sub-skills table, runtime enforcement section with honest feature labeling, documentation routing table, and TOC. Removed generic AI marketing language and repeated contrastive constructions. `python scripts/validate_skills.py` passed. Ralph loop: 2 iterations (iteration 1 added missing TOC, iteration 2 no-op by evidence).
- 2026-06-03: Phase 7C Quickstart Polish complete: rewrote `docs/QUICKSTART.md` with TOC, 5-minute path, 30-minute path, and polished all 7 paths with expected outputs, concrete examples, and clear next steps. Ralph loop: 2 iterations (iteration 1 fixed 30-min path coherence and moved prerequisites upfront, iteration 2 no-op by evidence). `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.
- 2026-06-03: Phase 7F Examples Library complete: created `docs/examples/EXAMPLES_LIBRARY.md` with 3 examples (task-state run, domain pack validation, failure and recovery) and 5 deferred examples. All examples labeled as implemented, show expected outputs, and avoid synthetic claims. Ralph loop: 2 iterations (iteration 1: no material defects found; iteration 2: no-op by evidence). `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.
- 2026-06-03: Phase 7G Documentation Quality Audit complete: audited 6 docs (README.md, QUICKSTART.md, RUNTIME_ENFORCEMENT.md, CREATE_A_PLAN.md, BUILD_OR_IMPROVE_A_SKILL.md, EXAMPLES_LIBRARY.md). All 6 docs PASS. Applied 3 targeted fixes: (1) QUICKSTART.md Step 2 audit target corrected from IMPLEMENTATION_PLAN.md to AGENTS.md, (2) README.md directory links changed to README.md files, (3) RUNTIME_ENFORCEMENT.md "quickstart" changed to link. Ralph loop: 2 iterations (iteration 1: no additional defects; iteration 2: no-op by evidence). `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.
- 2026-06-03: Phase 8A Rollout Scope Selection complete: created rollout matrix for all 7 skills. Selected `contextsmith-prompt-engineer` for Phase 8B (1 skill). `contextsmith-run` already integrated (Phase 4A). `contextsmith` skipped (meta-skill router). `contextsmith-skill-engineer`, `contextsmith-skill-migrator`, `contextsmith-instruction-engineer`, `contextsmith-agent-evaluator` deferred for Phase 8C+. ISSUE-1 resolution path: Option 3 (extend `sync_shared_refs.py` to preserve directory structure for `local: true` entries). Ralph loop: 2 iterations (iteration 1: no material defects; iteration 2: no-op by evidence). `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.
- 2026-06-03: Phase 8B ISSUE-1 resolved: fixed `sync_shared_refs.py` to preserve directory structure for `local: true` entries (runtime files → `references/runtime/`, skill-local files → `references/` flat). Added `--repo-root` CLI option for test isolation. Created `tests/test_sync_shared_refs.py` with 3 regression tests. Updated `contextsmith-prompt-engineer/reference_manifest.yml` with 10 runtime file entries. Updated `contextsmith-prompt-engineer/SKILL.md` with runtime validation section (step 8). Increased token budget from 3600 to 3800. `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed. `python -m pytest tests/ -v` passed (207 tests). CLI validation 6/6 PASS.
- 2026-06-03: Phase 8B1 Skill-Engineer Runtime Integration complete: updated `contextsmith-skill-engineer/reference_manifest.yml` with 10 runtime file entries. Updated `contextsmith-skill-engineer/SKILL.md` with runtime validation section (step 9). Increased token budget from 3200 to 3400. `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed. `python -m pytest tests/ -v` passed (207 tests). Ralph loop: 2 iterations, both no-op by evidence.
- 2026-06-03: Phase 8B3 Skill-Migrator Runtime Integration complete: updated `contextsmith-skill-migrator/reference_manifest.yml` with 10 runtime file entries. Updated `contextsmith-skill-migrator/SKILL.md` with runtime validation section (step 8). No token budget change needed (2097/2500). `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed. `python -m pytest tests/ -v` passed (207 tests). Ralph loop: 2 iterations, both no-op by evidence.
- 2026-06-03: Phase 8C.1 Run Task-State Handoff Workflow Doc complete: created `docs/workflows/RUN_TASK_STATE_HANDOFF.md` (99 lines) following CREATE_A_PLAN.md / BUILD_OR_IMPROVE_A_SKILL.md pattern. Updated `docs/workflows/README.md`. Ralph loop: 2 iterations (iteration 1 added EXAMPLES_LIBRARY.md cross-reference, iteration 2 no-op by evidence). `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.
- 2026-06-03: Phase 8C.2 Schedule with Approval Gates Workflow Doc complete: created `docs/workflows/SCHEDULE_WITH_APPROVAL_GATES.md` (95 lines) following CREATE_A_PLAN.md / BUILD_OR_IMPROVE_A_SKILL.md pattern with approval gate specifics. Updated `docs/workflows/README.md`. Ralph loop: 2 iterations (iteration 1 refined example prompt and added file paths to expected artifacts, iteration 2 no-op by evidence). `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.
- 2026-06-03: Phase 8C.3 Compare Travel Options Workflow Doc complete: created `docs/workflows/COMPARE_TRAVEL_OPTIONS.md` (106 lines) following CREATE_A_PLAN.md / BUILD_OR_IMPROVE_A_SKILL.md pattern with travel/purchase domain specifics. Updated `docs/workflows/README.md`. Ralph loop: 2 iterations (iteration 1 removed stale EXAMPLES_LIBRARY.md cross-reference, iteration 2 no-op by evidence). `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.
- 2026-06-03: Phase 8C.4 Prompt Engineering Example complete: added Example 4 (Prompt Engineering) to `docs/examples/EXAMPLES_LIBRARY.md`. Follows established example pattern with Status, Scenario, Input, Prompt, What happens (7 steps), Expected output (Engineering Metadata, System Prompt, User Prompt Template, Context Strategy, Validation and Test Plan, Ralph Summary, Risks), and Recovery. Removed prompt engineering from Deferred Examples section. Updated TOC. Ralph loop: 2 iterations (iteration 1: no material defects; iteration 2: no-op by evidence). `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.
- 2026-06-03: Phase 8C.5 Implementation Plan Creation Example complete: verified Example 5 (Implementation Plan Creation) in `docs/examples/EXAMPLES_LIBRARY.md`. Follows established example pattern with Status, Scenario, Input, Prompt, What happens (7 steps), Expected output (Detected Project Profile, Changes Made, Safeguards, Validation Notes, Ralph Summary, Risks, Files Written), and Recovery. Deferred Examples section correctly excludes implementation plan creation (3 remain: plan audit, meeting scheduling, travel comparison). Ralph loop: 2 iterations (iteration 1: no material defects; iteration 2: no-op by evidence). `python scripts/validate_skills.py` passed. `python scripts/token_budget.py --strict` passed.

## Phase 3G Changed Artifacts
| File | Change |
|---|---|
| `runtime/domain_packs/general_fallback.json` | Corrected fallback trigger to wildcard `*` |
| `tests/fixtures/domain_pack_general_fallback.json` | Matched fixture to runtime pack wildcard trigger |
| `runtime/validator.py` | Added schema rule 10 enforcement for `general_fallback` |
| `tests/test_validator.py` | Added regression test for non-wildcard fallback trigger rejection |

## Phase 4A Changed Artifacts
| File | Change |
|---|---|
| `skills/contextsmith-run/SKILL.md` | Added "Runtime Validators" subsection to Validation Gate, "Runtime Artifacts" subsection to Evidence Ledger, runtime validation step 9 to Execution Workflow |
| `skills/contextsmith-run/reference_manifest.yml` | Added 10 local entries for runtime files (validator.py, cli.py, __init__.py, 6 domain pack JSON files) |

## Phase 8B Changed Artifacts
| File | Change |
|---|---|
| `scripts/sync_shared_refs.py` | Fixed ISSUE-1: preserves directory structure for `local: true` entries; added `--repo-root` CLI option |
| `tests/test_sync_shared_refs.py` | NEW — 3 regression tests for directory structure preservation |
| `skills/contextsmith-prompt-engineer/reference_manifest.yml` | Added 10 runtime file entries (validator.py, cli.py, __init__.py, 6 domain packs) |
| `skills/contextsmith-prompt-engineer/SKILL.md` | Added runtime validation section (step 8) with CLI reference table |
| `scripts/token_budget.py` | Increased contextsmith-prompt-engineer budget from 3600 to 3800 |

## Phase 8B1 Changed Artifacts
| File | Change |
|---|---|
| `skills/contextsmith-skill-engineer/reference_manifest.yml` | Added 10 runtime file entries (validator.py, cli.py, __init__.py, 6 domain packs) |
| `skills/contextsmith-skill-engineer/SKILL.md` | Added runtime validation section (step 9) with CLI reference |
| `scripts/token_budget.py` | Increased contextsmith-skill-engineer budget from 3200 to 3400 |

## Phase 8B2 Changed Artifacts
| File | Change |
|---|---|
| `skills/contextsmith-instruction-engineer/reference_manifest.yml` | Added 10 runtime file entries (validator.py, cli.py, __init__.py, 6 domain packs) |
| `skills/contextsmith-instruction-engineer/SKILL.md` | Added runtime validation section (step 8) with CLI reference |
| `scripts/token_budget.py` | Increased contextsmith-instruction-engineer budget from 3400 to 3600 |

## Phase 8B3 Changed Artifacts
| File | Change |
|---|---|
| `skills/contextsmith-skill-migrator/reference_manifest.yml` | Added 10 runtime file entries (validator.py, cli.py, __init__.py, 6 domain packs) |
| `skills/contextsmith-skill-migrator/SKILL.md` | Added runtime validation section (step 8) with CLI reference |

## Phase 8B4 Changed Artifacts
| File | Change |
|---|---|
| `skills/contextsmith-agent-evaluator/reference_manifest.yml` | Added 10 runtime file entries (validator.py, cli.py, __init__.py, 6 domain packs) |
| `skills/contextsmith-agent-evaluator/SKILL.md` | Added runtime validation section (step 8) with CLI reference |
| `scripts/token_budget.py` | Increased contextsmith-agent-evaluator budget from 1900 to 2100 |

## Phase 8C.1 Changed Artifacts
| File | Change |
|---|---|
| `docs/workflows/RUN_TASK_STATE_HANDOFF.md` | NEW — workflow guide for resuming tasks from NEXT_PROMPT.md handoffs (99 lines) |
| `docs/workflows/README.md` | Added Run a Task-State Handoff entry |

## Phase 8C.2 Changed Artifacts
| File | Change |
|---|---|
| `docs/workflows/SCHEDULE_WITH_APPROVAL_GATES.md` | NEW — workflow guide for scheduling with approval gates (95 lines) |
| `docs/workflows/README.md` | Added Schedule with Approval Gates entry |

## Phase 8C.3 Changed Artifacts
| File | Change |
|---|---|
| `docs/workflows/COMPARE_TRAVEL_OPTIONS.md` | NEW — workflow guide for comparing travel options without purchasing (106 lines) |
| `docs/workflows/README.md` | Added Compare Travel Options entry |

## Phase 8C.4 Changed Artifacts
| File | Change |
|---|---|
| `docs/examples/EXAMPLES_LIBRARY.md` | Added Example 4 (Prompt Engineering) with Status, Scenario, Input, Prompt, What happens, Expected output, and Recovery; updated TOC; removed prompt engineering from Deferred Examples |

## Phase 8C.5 Changed Artifacts
| File | Change |
|---|---|
| `docs/examples/EXAMPLES_LIBRARY.md` | Example 5 (Implementation Plan Creation) present with Status, Scenario, Input, Prompt, What happens, Expected output, and Recovery; Deferred Examples correctly excludes implementation plan creation (3 remain) |

## Phase 8B1-8B4 Plan — ALL COMPLETE
Phase 8B1-8B4 each integrated runtime validation into one deferred skill, following the Phase 8B pattern:
- Phase 8B1: `contextsmith-skill-engineer` — COMPLETE
- Phase 8B2: `contextsmith-instruction-engineer` — COMPLETE
- Phase 8B3: `contextsmith-skill-migrator` — COMPLETE
- Phase 8B4: `contextsmith-agent-evaluator` — COMPLETE

Each sub-phase added 10 runtime file entries to `reference_manifest.yml`, added a compact runtime validation section to SKILL.md, and updated token budget if needed. All 4 sub-phases pass `validate_skills.py`, `token_budget.py --strict`, and `pytest`.

## Phase 8C Documentation Workstream

### Phase 8C.1: Run Task-State Handoff Workflow Doc
- **Artifact**: `docs/workflows/RUN_TASK_STATE_HANDOFF.md` (99 lines)
- **Status**: Complete — created workflow doc, updated README, validations pass, Ralph loop 2 iterations
- **Pattern**: Follows CREATE_A_PLAN.md / BUILD_OR_IMPROVE_A_SKILL.md structure
- **Key Content**: 5-step workflow for resuming tasks from NEXT_PROMPT.md handoffs

### Phase 8C.2: Schedule with Approval Gates Workflow Doc
- **Artifact**: `docs/workflows/SCHEDULE_WITH_APPROVAL_GATES.md` (95 lines)
- **Status**: Complete — created workflow doc, updated README, validations pass, Ralph loop 2 iterations
- **Pattern**: Follows CREATE_A_PLAN.md / BUILD_OR_IMPROVE_A_SKILL.md structure with approval gate specifics
- **Key Content**: 5-step workflow for scheduling tasks requiring human approval gates, references `shared/side-effect-matrix.md`

### Phase 8C.3: Compare Travel Options Workflow Doc
- **Artifact**: `docs/workflows/COMPARE_TRAVEL_OPTIONS.md` (106 lines)
- **Status**: Complete — created workflow doc, updated README, validations pass, Ralph loop 2 iterations
- **Pattern**: Follows CREATE_A_PLAN.md / BUILD_OR_IMPROVE_A_SKILL.md structure with travel/purchase domain specifics
- **Key Content**: 5-step workflow for comparing travel options without purchasing, references `shared/side-effect-matrix.md`

### Phase 8C.4: Prompt Engineering Example
- **Artifact**: `docs/examples/EXAMPLES_LIBRARY.md` (Example 4 added)
- **Status**: Complete — added example, updated TOC, removed from Deferred, validations pass, Ralph loop 2 iterations
- **Pattern**: Follows established example pattern with Status, Scenario, Input, Prompt, What happens, Expected output, Recovery
- **Key Content**: contextsmith-prompt-engineer invocation with --target-profile, --domain, --ralph flags; expected output shows Engineering Metadata, System Prompt, User Prompt Template, Context Strategy, Validation and Test Plan, Ralph Summary, Risks

### Phase 8C.5: Implementation Plan Creation Example
- **Artifact**: `docs/examples/EXAMPLES_LIBRARY.md` (Example 5)
- **Status**: Complete — verified example pattern compliance, validations pass, Ralph loop 2 iterations
- **Pattern**: Follows established example pattern with Status, Scenario, Input, Prompt, What happens, Expected output, Recovery
- **Key Content**: contextsmith-instruction-engineer invocation for phased plan creation; expected output shows Detected Project Profile, Changes Made, Safeguards, Validation Notes, Ralph Summary, Risks, Files Written

## Phase 8C Documentation Summary
- Total workflow docs created: 3 (8C.1, 8C.2, 8C.3)
- Total examples created: 2 (8C.4, 8C.5)
- Total lines: 300 (under 130 per doc limit)
- All validations pass: `validate_skills.py`, `token_budget.py --strict`
- Ralph loop: 2 iterations per phase, 1 fix applied in 8C.3 (stale cross-reference removed)
- Deferred examples remaining: 3 (plan audit, meeting scheduling, travel comparison)

## Phase 0 Files Inspected
| File | Purpose |
|---|---|
| `scripts/build_release.py` | Release pipeline: sync, validate, bundle, individual packaging |
| `scripts/package_skill.sh` | Individual skill zip: stage, manifest, checksum, zip |
| `scripts/sync_shared_refs.py` | Reference sync: manifest-driven copy to staging |
| `scripts/token_budget.py` | Token budget validation (not packaging, but required gate) |
| `scripts/install_skill.sh` | Install: extract, verify checksums, backup, copy |
| `skills/contextsmith-run/reference_manifest.yml` | Example manifest with 51 references (shared + local) |
| `skills/contextsmith-prompt-engineer/reference_manifest.yml` | Example manifest with 64 references |
| `skills/contextsmith/` | Skill directory structure: SKILL.md, help.md, reference_manifest.yml, references/ |
| `skills/contextsmith-run/` | Skill directory structure: SKILL.md, local refs, reference_manifest.yml, references/ |
