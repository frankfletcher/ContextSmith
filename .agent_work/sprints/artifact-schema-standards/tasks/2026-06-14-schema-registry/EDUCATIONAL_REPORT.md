# EDUCATIONAL_REPORT.md

## Sub-phase 7.1: artifact_schemas extension

### Original Strengths

- The existing `workflow_config.schema.json` was already well-structured with `$defs` for reusable blocks and `additionalProperties: false` for strict validation.
- The codebase already had a `section_requirements` mechanism in `validators.py` that allowed config-driven overrides of required sections, which provided a foundation to formalize into a schema property.

### Original Weaknesses

- The `section_requirements` mechanism was an informal `config.get()` pattern — typed only at runtime, not in the JSON schema. Workflow authors had no schema-level documentation or type-checking for artifact section overrides.
- There was no way to specify optional section overrides, additive-only sections, or control merge-vs-replace behavior from the config.
- The `artifact_schemas.yaml` registry was the single source of truth for section requirements, with no workflow-level customization path documented in the schema.

### Changes Made

1. Added `artifact_schemas` property to `workflow_config.schema.json` at the top-level `properties` section, before `metadata`.
2. Added `ArtifactSchemaOverride` `$def` with fields: `extends`, `required_sections`, `optional_sections`, `additional_sections`, `extend_base`.
3. Used `additionalProperties: false` on the override block to prevent typos.
4. Made `extend_base` default to `true` so that overrides merge by default (least-surprise behavior).
5. Validated schema syntax with Draft202012Validator and backward compatibility with existing workflow configs.

### Why This Improves

- **Schema-level documentation**: Workflow authors can now discover artifact overrides from the JSON schema itself, not just from reading validators.py.
- **Type safety**: Override fields are typed and validated at schema-validation time, not just at runtime.
- **Flexible extension modes**: The `extend_base` + `additional_sections` combination lets workflows add sections without knowing the base schema, or fully replace sections when needed.
- **Backward compatible**: Existing configs without `artifact_schemas` pass validation unchanged.

### Remaining Risks or Assumptions

- The existing `section_requirements` config key in `validators.py` is not yet wired to `artifact_schemas` — validators still use the old key. A migration phase (or follow-up sub-phase) should update `validate_artifacts_with_schemas()` to read from `artifact_schemas` instead or in addition.
- The `extends` field documents a runtime defaulting behavior that the schema itself cannot enforce — validation code must implement the fallback to the artifact filename key.
- No integration tests yet verify that `artifact_schemas` overrides actually propagate to validation. This should be covered in Phase 8 (Integration Tests).

## Sub-phase 8.1: Sub-phase advancement test

### What was done
Added 5 tests in `tests/test_subphase_advancement.py` covering `_try_advance_subphase`:
- **test_advance_to_next_pending_subphase**: Verifies function returns `EXIT_CONTINUE` and sets `step_contract.subphase_name` when a pending sub-phase follows a completed one.
- **test_all_subphases_done_returns_none**: Verifies function returns `None` when all sub-phases in the current phase are completed.
- **test_flat_plan_no_subphases_returns_none**: Verifies backward compatibility — flat plan format (no sub-phases) returns `None`.
- **test_advance_verifies_status_file_updated**: Integration check that STATUS.md content is rewritten with the new sub-phase name.
- **test_no_current_subphase_starts_from_first_pending**: Edge case where `current_subphase` is empty — function correctly skips completed sub-phases and picks the first pending one.

### Key decisions
- Wrote a new test file (`test_subphase_advancement.py`) instead of adding to `test_orchestrator_determinism.py` to keep the sub-phase advancement tests self-contained and organized.
- Tests use `tempfile.TemporaryDirectory` for `state_dir` to provide a real STATUS.md for `_update_status` to read/write, matching the existing test pattern.
- Plan and status dicts are constructed in-memory rather than parsed from files, keeping tests fast and focused on the function under test.
- Added 2 bonus tests beyond the 3 required scenarios for robustness.
