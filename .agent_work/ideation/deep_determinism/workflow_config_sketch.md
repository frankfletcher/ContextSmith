# Workflow Config Sketch

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
    - CHECKLIST.md
    - ARTIFACTS.md
    - NEXT_PROMPT.md

overlay:
  add_steps:

    - human_approval_gate

  remove_steps:

    - ralph_review

  notes: "Overlay may add optional steps or remove optional steps. Removing required steps requires allow_remove_required=true AND the --force flag at runtime."

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
      - CHECKLIST.md
      - EVIDENCE.md
      - AUDIT_REPORT.md
      - EDUCATIONAL_REPORT.md

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
- Phase configs should include a checklist artifact for each bounded task.
- Closeout phases may emit `AUDIT_REPORT.md`, `EDUCATIONAL_REPORT.md`, and `SUMMARY.md` as user-facing artifacts.

---

## Complete Schema Specification

Every workflow config must conform to this structure. Fields marked **REQUIRED** must be present. Fields marked **DEFAULT** have a default value if omitted.

### Top Level

```yaml

# REQUIRED. Unique identifier for this workflow. Used in checkpoints and logs.
workflow_id: string

# REQUIRED. Schema version. Must match the orchestrator's expected version.
# Increment when breaking changes are made to the config structure.
version: integer (>= 1)

# REQUIRED. Domain category that determines which validators and references apply.
# One of: coding, documentation, migration, audit, planning, general
domain: string

# REQUIRED. Execution mode. Currently only "phased-run" is supported.
mode: "phased-run"

# DEFAULT: "auto". Which harness adapter to use.
# "auto" = detect from environment, "opencode" = force OpenCode adapter.
harness: "auto" | string

# REQUIRED. Baseline blocks define the required workflow shape.
# The orchestrator refuses to run if baseline requirements are not met.
baseline: BaselineBlock

# DEFAULT: {}. Optional overlay that modifies the baseline.
# Overlays can add optional steps or remove baseline steps marked optional.
overlay: OverlayBlock

# DEFAULT: {}. State machine definitions for each phase step.
# Each key is a phase step name; value is a StateDefinition.
states: dict[string, StateDefinition]

# DEFAULT: []. Ordered list of phase step names that form the workflow.
# The orchestrator executes these in order unless the state machine intervenes.
phase_order: [string]

# DEFAULT: {}. Validation rules applied globally (not per-state).
validation: ValidationBlock

# DEFAULT: {}. Metadata for documentation and display.
metadata: MetadataBlock
```

### BaselineBlock

```yaml

# DEFAULT: []. Steps that must be present in phase_order.
# The orchestrator rejects any workflow that omits these.
required_steps:

  - load_task_state
  - compile_contract
  - validate_artifacts
  - close_phase
  - write_next_prompt

# DEFAULT: []. Gates that must pass before the workflow can complete.
# Each gate corresponds to a state machine state that must reach a terminal condition.
required_gates:

  - audit
  - validate

# DEFAULT: []. Files that must exist in the task-state directory
# before the orchestrator considers the workflow consistent.
required_files:

  - STATUS.md
  - PLAN.md
  - CONTEXT.md
  - CHECKLIST.md
  - ARTIFACTS.md
  - NEXT_PROMPT.md
```

### OverlayBlock

```yaml

# DEFAULT: []. Steps to insert into the phase order after specified anchor points.
# Each entry: {step: string, after: string | null}
# If after is null, the step is inserted at the beginning.
add_steps:

  - step: human_approval_gate

    after: validate_artifacts

# DEFAULT: []. Steps to remove from the phase order.
# The orchestrator refuses to remove any step listed in baseline.required_steps
# unless the step is marked optional: true in its state definition.
remove_steps:

  - ralph_review

# DEFAULT: false. If true, the overlay can remove required steps.
# Requires explicit user approval (--force flag).
allow_remove_required: false

# Optional human-readable notes about the overlay's purpose.
notes: "Overlay adds a human approval gate after validation for compliance workflows."
```

### StateDefinition

```yaml

# REQUIRED. The state machine state this phase corresponds to.
# Must be one of the canonical states: init, plan, execute, audit, fix,
# validate, ralph_critique, ralph_revise, closeout, done, blocked.
state: string

# DEFAULT: "contextsmith-builder". Agent profile to use.
agent: string

# REQUIRED. Permission level for this phase.
# read-only: cannot modify files
# edit: can modify project files
# external-action: can run commands and modify files
permissions: "read-only" | "edit" | "external-action"

# DEFAULT: 3. Maximum retries before transitioning to blocked.
max_retries: integer

# DEFAULT: 300. Wall-clock timeout in seconds.
timeout_s: integer

# DEFAULT: false. If true, this step can be removed by overlay.
optional: boolean

# REQUIRED. Valid exit transitions from this state.
# The orchestrator uses result conditions to pick which transition to follow.
transitions:

  - condition: string    # e.g., "pass", "fail", "output_valid", "output_invalid"

    target: string       # target state name or special: "retry-same-state", "blocked"

# DEFAULT: []. Files this phase is expected to produce.
# The orchestrator checks these after execution.
expected_outputs:

  - AUDIT_REPORT.md
  - CHECKLIST.md
  - PHASE_LOG.md
  - NEXT_PROMPT.md

# DEFAULT: []. Files this phase reads as input.
inputs:

  - STATUS.md
  - NEXT_PROMPT.md

# DEFAULT: false. If true, the orchestrator writes a checkpoint
# BEFORE dispatching this step (in addition to after).
checkpoint_before_run: boolean
```

### ValidationBlock

```yaml

# DEFAULT: "runtime/phase_contract.schema.json". Schema file path (relative to project root).
schema: string

# DEFAULT: []. Checks to run after phase execution.
# Each check is a string identifier mapped to a validator function in scripts/validators/.
required_checks:

  - file_exists
  - json_schema
  - regex_match
  - command_exit_zero

# DEFAULT: false. If true, validation failures are reported but do not block advancement.
relaxed: boolean
```

### MetadataBlock

```yaml

# DEFAULT: "". Human-readable name.
name: string

# DEFAULT: "". Description of what this workflow does.
description: string

# DEFAULT: "". Author or owning team.
author: string

# DEFAULT: {}. Arbitrary key-value pairs for display.
tags:
  domain: coding
  complexity: medium
```

---

## Complete Example: Simple Audit Workflow

```yaml
workflow_id: simple-audit
version: 1
domain: audit
mode: phased-run
harness: auto

baseline:
  required_steps:

    - load_task_state
    - audit_current_phase
    - write_report
    - close_phase
    - write_next_prompt

  required_gates:

    - audit

  required_files:

    - STATUS.md
    - PLAN.md
    - CONTEXT.md

states:
  load_task_state:
    state: plan
    agent: contextsmith-planner
    permissions: read-only
    max_retries: 2
    timeout_s: 60
    transitions:

      - condition: pass

        target: audit_current_phase

      - condition: fail

        target: blocked
    expected_outputs: []
    inputs:

      - STATUS.md
      - PLAN.md

  audit_current_phase:
    state: audit
    agent: contextsmith-auditor
    permissions: read-only
    max_retries: 3
    timeout_s: 300
    transitions:

      - condition: pass

        target: write_report

      - condition: fail

        target: audit_current_phase

      - condition: max_retries

        target: blocked
    expected_outputs:

      - AUDIT_REPORT.md
      - EVIDENCE.md

    inputs:

      - PLAN.md
      - CONTEXT.md

  write_report:
    state: closeout
    agent: contextsmith-closer
    permissions: edit
    max_retries: 2
    timeout_s: 120
    transitions:

      - condition: pass

        target: write_next_prompt

      - condition: fail

        target: write_report
    expected_outputs:

      - AUDIT_REPORT.md
      - SUMMARY.md

    inputs:

      - AUDIT_REPORT.md

  write_next_prompt:
    state: closeout
    agent: contextsmith-closer
    permissions: edit
    max_retries: 2
    timeout_s: 60
    transitions:

      - condition: pass

        target: done

      - condition: fail

        target: write_next_prompt
    expected_outputs:

      - NEXT_PROMPT.md

    inputs:

      - STATUS.md
      - AUDIT_REPORT.md

phase_order:

  - load_task_state
  - audit_current_phase
  - write_report
  - write_next_prompt

validation:
  schema: schemas/phase_contract.schema.json
  required_checks:

    - file_exists
    - json_schema
```

---

## Complete Example: Engineering Workflow With Audit and Ralph Loops

Note: In this example, `audit_output` fail routes to `implement_change` (re-execute) rather than a separate `fix` state. This is a valid design choice — the `fix` canonical state is optional. Workflows that need a distinct fix phase (e.g., to apply targeted patches rather than re-executing) should add a `fix` state between `audit` and `execute`.

```yaml
workflow_id: skill-engineering
version: 1
domain: coding
mode: phased-run
harness: opencode

baseline:
  required_steps:

    - load_context
    - implement_change
    - audit_output
    - review_via_ralph
    - validate
    - close

  required_gates:

    - audit
    - validate
    - ralph_review

  required_files:

    - STATUS.md
    - PLAN.md
    - CONTEXT.md
    - CHECKLIST.md
    - ARTIFACTS.md
    - NEXT_PROMPT.md

states:
  load_context:
    state: init
    agent: contextsmith-planner
    permissions: read-only
    max_retries: 2
    timeout_s: 30
    transitions:

      - condition: pass

        target: implement_change

      - condition: fail

        target: blocked
    expected_outputs: []
    inputs:

      - STATUS.md
      - PLAN.md

  implement_change:
    state: execute
    agent: contextsmith-builder
    permissions: edit
    max_retries: 3
    timeout_s: 600
    transitions:

      - condition: output_valid

        target: audit_output

      - condition: output_invalid

        target: implement_change

      - condition: max_retries

        target: blocked
    expected_outputs:

      - ARTIFACTS.md
      - PHASE_LOG.md

    inputs:

      - NEXT_PROMPT.md
      - CONTEXT.md

  audit_output:
    state: audit
    agent: contextsmith-auditor
    permissions: read-only
    max_retries: 2
    timeout_s: 300
    transitions:

      - condition: pass

        target: review_via_ralph

      - condition: fail

        target: implement_change

      - condition: max_retries

        target: blocked
    expected_outputs:

      - AUDIT_REPORT.md

    inputs:

      - ARTIFACTS.md
      - PLAN.md

  review_via_ralph:
    state: ralph_critique
    agent: contextsmith-auditor
    permissions: read-only
    max_retries: 2
    timeout_s: 300
    transitions:

      - condition: pass

        target: validate

      - condition: fail

        target: ralph_revise

      - condition: max_cycles_reached

        target: validate
    ralph_max_cycles: 2
    expected_outputs:

      - AUDIT_REPORT.md
      - EVIDENCE.md

    inputs:

      - ARTIFACTS.md
      - AUDIT_REPORT.md

  ralph_revise:
    state: ralph_revise
    agent: contextsmith-builder
    permissions: edit
    max_retries: 2
    timeout_s: 300
    transitions:

      - condition: pass

        target: review_via_ralph

      - condition: fail

        target: review_via_ralph
    expected_outputs:

      - ARTIFACTS.md

    inputs:

      - AUDIT_REPORT.md

  validate:
    state: validate
    agent: contextsmith-validator
    permissions: read-only
    max_retries: 2
    timeout_s: 120
    transitions:

      - condition: pass

        target: close

      - condition: fail

        target: implement_change

      - condition: max_retries

        target: blocked
    expected_outputs: []
    inputs:

      - ARTIFACTS.md
      - CHECKLIST.md

  close:
    state: closeout
    agent: contextsmith-closer
    permissions: edit
    max_retries: 2
    timeout_s: 60
    transitions:

      - condition: pass

        target: done

      - condition: fail

        target: close
    expected_outputs:

      - SUMMARY.md
      - EDUCATIONAL_REPORT.md
      - NEXT_PROMPT.md

    inputs:

      - STATUS.md
      - AUDIT_REPORT.md

phase_order:

  - load_context
  - implement_change
  - audit_output
  - review_via_ralph
  - ralph_revise
  - validate
  - close

validation:
  schema: schemas/workflow_config.schema.json
  required_checks:

    - file_exists
    - json_schema
    - command_exit_zero
```

---

## Overlay Mechanics

Overlays let plans modify a baseline workflow without rewriting it. The orchestrator resolves the overlay before entering the main loop.

### Resolution Steps

```
Step 1: Start with a copy of the baseline phase_order and state definitions.
Step 2: Remove any step listed in overlay.remove_steps.

  - If the step is in baseline.required_steps and not marked optional → BLOCK unless allow_remove_required=true.

Step 3: Add steps from overlay.add_steps.

  - Each entry specifies where to insert: {step: name, after: anchor-step-name}.
  - If anchor step has been removed, insert at the end.
  - If anchor step is null, insert at the beginning.

Step 4: For each added step, check it has a corresponding state definition.

  - If the state definition is missing and the step is in baseline.required_steps → BLOCK.
  - If the state definition is missing and the step is NOT required → warn and skip.

Step 5: The resulting phase_order and states dict are the "resolved workflow."
```

### Example

Baseline phase_order: `[A, B, C, D]`
Overlay:
```yaml
add_steps:

  - step: X

    after: B

  - step: Y

    after: D
remove_steps:

  - C
```

Resolved phase_order: `[A, B, X, D, Y]`

The orchestrator treats the resolved phase_order as authoritative for execution ordering.

---

## Field Validation Rules

The orchestrator validates these rules at startup, before any execution:

1. `workflow_id` must be non-empty and match `^[a-z0-9_-]+$`.
2. `version` must be >= 1 and <= orchestrator.max_supported_version.
3. `domain` must be one of the supported domains.
4. `mode` must be "phased-run" (only mode supported in v1).
5. Every state referenced in `phase_order` must have a definition in `states`.
6. Every state definition's `transitions` must reference valid target states or special targets (`retry-same-state`, `blocked`, `done`).
7. No transition target may reference a state that does not exist.
8. At least one phase must have a transition path to `done` (reachability check).
9. `baseline.required_steps` must be a subset of `phase_order` after overlay resolution.
10. `baseline.required_gates` must have corresponding state definitions that can reach a passing terminal.
11. Every state with `ralph_max_cycles` must have `ralph_critique` or `ralph_revise` as its state.
12. `overlay.allow_remove_required` requires `--force` flag at runtime.
13. `harness` must be `"auto"` or a registered harness adapter name.
