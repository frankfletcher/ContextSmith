# Artifacts: Runtime Enforcement for ContextSmith Skills

## Artifact Manifest
- artifact_type: artifact-index
- parent_task: TASK.md
- status: Phase 3 audit complete
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
| `contextsmith-run` pilot integration | 4A | Pending |
| Thin-skill writing guide | 4B | Pending |
| Next Prompt Compiler specification | 5A | Pending |
| Next Prompt Compiler implementation | 5B | Pending |
| Next Prompt Compiler tests | 5C | Pending |
| Orchestrated runner specification | 5D | Pending |
| Runner skeleton | 5E | Pending |
| MCP adapter design | 6A | Pending |
| Harness adapter design | 6B | Pending |
| User documentation map | 7A | Pending |
| README refresh | 7B | Pending |
| Quickstart and time-to-first-value docs | 7C | Pending |
| Runtime workflow usage docs | 7D | Pending |
| Use-case workflow docs | 7E | Pending |
| Examples library | 7F | Pending |
| Documentation quality audit | 7G | Pending |

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

## Phase 3G Changed Artifacts
| File | Change |
|---|---|
| `runtime/domain_packs/general_fallback.json` | Corrected fallback trigger to wildcard `*` |
| `tests/fixtures/domain_pack_general_fallback.json` | Matched fixture to runtime pack wildcard trigger |
| `runtime/validator.py` | Added schema rule 10 enforcement for `general_fallback` |
| `tests/test_validator.py` | Added regression test for non-wildcard fallback trigger rejection |

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
