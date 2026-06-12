# Validation Results: Agent Config Schema

## Schema

- File: `schemas/agent_config.schema.json`
- Draft: JSON Schema Draft 7
- Required top-level fields: `description`, `mode`, `permission`

## Results

### auditor

- Fixture: `tests/fixtures/valid_agent_auditor.yaml`
- Result: **PASS**
- Errors: none
- Notes: Uses pattern-based bash permissions (object form with `*` default and specific overrides)

### builder

- Fixture: `tests/fixtures/valid_agent_builder.yaml`
- Result: **PASS**
- Errors: none
- Notes: Uses simple string form for bash permission; no `steps` field (optional, omitted)

## Schema Issues Discovered

None. Both examples from `system_components.md` validate without modification.

## Notes

- The `bash` field accepts both a simple string (`allow`/`deny`) and an object with pattern-based rules via `oneOf`
- The `steps` field is optional — the builder example omits it, the auditor example sets it to 10
- The `permission` block requires only `edit`; `bash`, `webfetch`, and `external_directory` are optional
- `additionalProperties: false` is enforced on both root and `PermissionBlock`
