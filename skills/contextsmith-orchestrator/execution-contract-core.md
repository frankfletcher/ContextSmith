# Execution Contract Core

Use this core reference for every ContextSmith run. Use `execution-contract.md` only when the full schema or examples are needed.

## Build Order

1. Start with skill defaults.
2. Apply inherited artifact manifest values.
3. Apply explicit CLI-style flags.
4. Apply current user prose when it clearly overrides earlier values.
5. Narrow scope when child input is smaller than the parent artifact.
6. Ask one concise question only when conflicts change side effects, domain, validation, target model/profile, permission boundaries, or output location.

## Required Contract Fields

```yaml
execution_contract:
  input_type: raw_prompt|prompt_file|next_prompt|task_state|plan|checklist
  run_mode: single|single-with-state|phase|phased-run|dry-run|audit-only
  target_profile: qwen36
  context_length: 64k
  domain: general-task
  interaction: silent
  side_effects: read-only
  validation: available
  ralph_iterations_required: 1
  self_audit_required: true
  evidence_required:
    - parameters_applied
    - validation_result
    - self_audit_result
    - ralph_result
    - declared_vs_enforced
```

## Enforcement Rules

- `--validation strict`: do not mark complete without validation evidence or explicit blocker.
- `--ralph N`: run N bounded critique/revision checks or record why later iterations were no-op/bloat.
- `--self-audit true`: run self-audit before completion.
- `--interaction refine`: ask bounded, material questions before execution unless the prompt already fixes every material choice.
- `--target-profile qwen36`: keep execution literal, atomic, and compact.
- `--mode yolo`: reduce questions, not safety, validation, audit, Ralph, or permission boundaries.

## Declared-Vs-Enforced Rule

Before final output, compare each declared obligation against evidence. If required evidence is missing, perform the gate or report blocked/partial. Do not mark complete with `missing_evidence`.
