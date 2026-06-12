# Workflow Config Sketch

> **Superseded.** This is an early draft. The authoritative version is at `deep_determinism/workflow_config_sketch.md` — it has the same content enriched with complete schema specification, 2 full example configs, overlay resolution algorithm, and 13 field validation rules.

This is the draft shape for baseline workflow configs owned by the orchestrator.

## Core Idea

- The orchestrator owns the required baseline workflow.
- The agent may add steps or explicitly remove optional steps.
- The orchestrator validates that the resulting workflow still satisfies required gates.
- Plan artifacts are overlays, not the source of truth.

## Suggested Structure

```yaml
workflow_id: runtime-enforcement
version: 1
domain: coding
mode: phased-run

baseline:
  required_steps:
    - load_task_state
    - compile_contract
    - execute_current_phase
    - validate_artifacts
    - close_phase
    - write_next_prompt
  required_gates:
    - validate_artifacts
    - self_audit
    - ralph_review
  required_files:
    - STATUS.md
    - PLAN.md
    - CONTEXT.md
    - NEXT_PROMPT.md

overlay:
  add_steps:
    - human_approval_gate
  remove_steps:
    - ralph_review
  notes: "Overlay may narrow or extend behavior, but cannot remove required baseline gates without explicit approval."

step_contracts:
  execute_current_phase:
    agent: contextsmith-run
    permissions: read-only|edit|external-action
    inputs:
      - NEXT_PROMPT.md
      - STATUS.md
      - PLAN.md
    outputs:
      - phase artifacts
      - ARTIFACTS.md
      - PHASE_LOG.md

validation:
  schema: runtime/phase_contract.schema.json
  required_checks:
    - file_exists
    - command
    - json_schema
    - regex_match
```

## Notes

- YAML is easier for humans to edit; JSON is easier for strict validation.
- The orchestrator should reject configs that omit required baseline steps or gates.
- A skill for creating these configs should generate schema-valid YAML/JSON, not freeform prose.
