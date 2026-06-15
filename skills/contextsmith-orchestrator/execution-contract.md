# Execution Contract

The execution contract turns user instructions and ContextSmith parameters into runtime obligations.

## Build Order

1. Start with skill defaults.
2. Apply inherited artifact manifest values.
3. Apply explicit CLI-style flags.
4. Apply current user prose when it clearly overrides earlier values.
5. Narrow scope when the input is smaller than the parent artifact.
6. Ask one question only when conflicting values change side effects, domain, validation, target model, or output location.

## Minimal Contract

```yaml
execution_contract:
  input_type: raw_prompt
  run_mode: single
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
    - declared_vs_enforced
```

## Parameter Obligations

| Parameter | Runtime obligation |
| ----------- | -------------------- |
| `--target-profile` | Shape instruction length, literalness, ambiguity tolerance, and output compactness for the selected model. |
| `--context-length` | Load selectively; summarize state before broad reads; avoid bulk reference loading. |
| `--mode guided` | Proceed with safe assumptions; ask only blocking or material questions. |
| `--mode deep` | Add stronger validation, self-audit, and explanation, not bloated model-facing context. |
| `--mode fast` | Reduce reporting; keep safety and declared gates. |
| `--mode yolo` | Minimize questions but do not bypass safety, validation, or user permission boundaries. |
| `--interaction refine` | Ask bounded multiple-choice questions before execution when choices matter. |
| `--validation strict` | Do not mark complete without validation evidence or an explicit blocker. |
| `--ralph N` | Run bounded critique/revision checks and record evidence. |
| `--self-audit false` | Skip self-audit only for explicit low-risk, nonpersistent work. |
| `--education-level deep` | Explain decisions in the report; keep execution artifacts compact. |
| `--side-effects external-action` | Require approval before irreversible or external effects. |

## Declared-Vs-Enforced Check

Before final output, compare declared obligations against evidence.

Example:

```yaml
declared_vs_enforced:
  ralph_2: evidence_present
  validation_strict: blocked_validation_command_missing
  target_profile_qwen36: evidence_present
  interaction_refine: evidence_present
```

If a required obligation lacks evidence, either perform the missing step or report the run as blocked/partial.

## Small-Model Guidance

Keep contracts short. Use concrete nouns and paths. Avoid abstract reminders. For small models, contract entries should be observable: a command, file path, output section, question, or validation result.

Treat `silent-unless-blocked` as an alias for `silent` when inherited from older artifacts.
