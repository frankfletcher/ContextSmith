# Next Prompt: Phase 3A General Fallback Domain Pack

## Artifact Manifest
- artifact_type: next_prompt
- phase: 3A
- target_profile: qwen36
- parent_plan: PLAN.md
- version: 1.0.0

## Mission

Create the smallest domain pack that works for any prompt, skill, or agent task. This is the universal safety net for unknown domains.

## Read Order

1. `STATUS.md` — current phase and next action
2. `PLAN.md` — Phase 3A section (lines 528+)
3. `CONTEXT.md` — Phase 0 packaging facts and constraints
4. `DECISIONS.md` — Phase 0.5 decisions
5. `DOMAIN_PACK_SCHEMA.md` — domain pack schema (Phase 1C artifact)
6. `ARTIFACT_VOCABULARY.md` — universal artifact vocabulary (Phase 1A artifact)
7. `runtime/validator.py` — existing validator core (domain_pack validator)
8. `tests/fixtures/domain_pack_valid.json` — existing valid fixture for reference

## Actions

1. Define the `general_fallback` domain pack following the schema from Phase 1C.
2. The pack should cover any prompt, skill, or agent task where the domain is unknown or unspecified.
3. Include minimal validation gates focused on universal requirements:
   - Requirement trace exists
   - Phase contract exists
   - Evidence ledger exists
   - Validation result or blocker exists
   - Approval record exists for external actions
   - Final claims do not exceed evidence
4. Keep the pack compact — it should fit on one screen.
5. Create a test fixture in `tests/fixtures/` for the general_fallback domain pack.
6. Add pytest tests to validate the fixture passes the domain_pack validator.

## Validation

- `python -m pytest tests/ -v` passes
- `python scripts/validate_skills.py` passes
- `python scripts/token_budget.py --strict` passes
- Domain pack validates against all 10 domain pack validation rules
- Fixture is compact and screen-readable

## Hard Stop

Do not proceed to Phase 3B until the general_fallback domain pack is complete and validated. Do not let the domain pack become a long instruction file — it should be a compact data artifact. If the pack grows beyond one screen, trim non-essential fields.
