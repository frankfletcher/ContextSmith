# Audit and Ralph State Machine Sketch

This note sketches how the orchestrator should enforce audit loops and Ralph loops without trusting the agent to remember them.

Related notes:

- [Orchestrator Idea](orchestrator_idea.md)
- [Orchestrator and Harness](orchestrator_and_harness.md)
- [Workflow Config Sketch](workflow_config_sketch.md)

## Core Rule

The orchestrator owns the required loop shape. The agent may produce the audit or critique content, but the orchestrator decides whether another loop is required and whether the workflow may advance.

## Loop Types

### Audit loop

Purpose: verify that the produced artifact is structurally and semantically acceptable.

Typical cycle:

1. generate or edit artifact
2. run validator or reviewer
3. if failed, route to fix
4. if passed, close the phase or continue

### Ralph loop

Purpose: run bounded critique/revision iterations before finalizing a result.

Typical cycle:

1. draft
2. critique
3. revise
4. critique again
5. stop after the required iteration count or max cycle limit

## Suggested State Machine

```yaml
workflow_id: audit-ralph
version: 1

states:
  draft:
    agent: contextsmith-builder
    on_exit: audit

  audit:
    agent: contextsmith-auditor
    validator: audit_schema
    on_pass: ralph_critique
    on_fail: fix

  fix:
    agent: contextsmith-builder
    on_exit: audit

  ralph_critique:
    agent: contextsmith-auditor
    validator: critique_schema
    max_cycles: 2
    on_pass: ralph_revise
    on_fail: ralph_revise

  ralph_revise:
    agent: contextsmith-builder
    on_exit: ralph_critique

  done:
    terminal: true

  blocked:
    terminal: true
```

## Enforcement Rules

- The orchestrator tracks the current state and refuses to advance if the required pass condition is missing.
- The orchestrator counts loop iterations and stops at `max_cycles`.
- The agent's output is only evidence; it does not define the state machine.
- A reviewer result should be structured, ideally JSON, so the orchestrator can decide pass/fail without guessing.

## Recommended Config Fields

From the baseline workflow config, the orchestrator should read:

- required states
- required gates
- required loop counts
- max retries
- terminal states
- review schema names

## Failure Cases

| Problem | Orchestrator response |
|---|---|
| Audit says pass but required fields are missing | Reject and send back to fix |
| Ralph loop exceeds max cycles | Stop and mark blocked |
| Review output is unstructured | Treat as failure |
| Agent tries to skip critique | Keep the workflow in the current loop |

## Related Docs

- `workflow_config_sketch.md` for the baseline config shape
- `orchestrator_idea.md` for the overall system model
- `orchestrator_and_harness.md` for the runtime split
- `RUNTIME_ENFORCEMENT.md` for the user-facing workflow model

---

## State Transition Table

The state machine is defined in the workflow config's `states` section. Each state declares its valid transitions. The orchestrator resolves transitions based on the result from the harness.

### Complete Transition Matrix

| Current State | Condition | Next State | Notes |
|---|---|---|---|
| init | config valid | plan | Config must pass schema validation |
| init | config invalid | blocked | Print validation errors |
| init | state dir missing | plan | Create default state files first |
| plan | plan valid | execute | Plan passes checklist schema |
| plan | plan invalid | plan (retry) | Max retries from config |
| plan | max retries | blocked | |
| execute | output valid | audit | If audit gate required |
| execute | output valid | validate | If no audit gate |
| execute | output valid | ralph_critique | If ralph_review gate but no audit |
| execute | output valid | closeout | If no gates remain |
| execute | output invalid | execute (retry) | Artifacts missing or schema-invalid |
| execute | max retries | blocked | |
| audit | pass | validate | If validate gate required |
| audit | pass | ralph_critique | If ralph_review gate required |
| audit | pass | closeout | If no remaining gates |
| audit | fail | fix | Issues found |
| audit | unstructured output | audit (retry) | No structured result |
| audit | max retries | blocked | |
| fix | always | audit | Fix routes back to audit to verify the fix. Some workflows may skip fix and route audit fail → execute (retry phase) directly; that is valid when the workflow config defines it. |
| fix | max retries | blocked | Count toward the audit-fix loop budget |
| validate | all checks pass | ralph_critique | If ralph_review gate required |
| validate | all checks pass | closeout | If no remaining gates |
| validate | any check fails | execute (retry) | Go back to fix the implementation |
| validate | any check fails | fix | If the phase allows fixing without full retry |
| validate | max retries | blocked | |
| ralph_critique | critique valid + cycles < max | ralph_revise | Normal cycle |
| ralph_critique | critique valid + cycles >= max | closeout | Max cycles reached, move on |
| ralph_critique | critique invalid | ralph_revise | Even invalid critique triggers revise |
| ralph_critique | max cycles exceeded | blocked | Safety catch |
| ralph_revise | always | ralph_critique | Loop counter increments after revise |
| ralph_revise | max retries | blocked | |
| closeout | closeout valid | done | All required outputs exist |
| closeout | closeout invalid | closeout (retry) | Missing SUMMARY.md or NEXT_PROMPT.md |
| closeout | max retries | blocked | |

### Transition Resolution Pseudocode

```python
def resolve_transition(
    current_state: str,
    result: HarnessResult,
    validation: ValidationResult,
    config: dict,
    counters: Counters,
) -> str:
    """
    Given the current state and execution result, determine the next state.
    Raises NoValidTransition if no transition condition matches.
    """
    state_def = config["states"].get(current_state)
    if not state_def:
        raise NoValidTransition(f"State {current_state} not found in config")

    for transition in state_def["transitions"]:
        condition = transition["condition"]
        target = transition["target"]

        if _matches_condition(condition, result, validation):
            # Handle retry limit
            if target == current_state or target == "retry-same-state":
                retries = counters.get(current_state, {}).get("retries", 0)
                max_r = state_def.get("max_retries", 3)
                if retries >= max_r:
                    return "blocked"
                return current_state

            # Handle Ralph cycle limit
            if current_state == "ralph_critique" and target == "ralph_revise":
                cycles = counters.get("ralph_critique", {}).get("cycles", 0)
                max_c = state_def.get("ralph_max_cycles", 2)
                if cycles >= max_c:
                    return config.get("ralph_complete_target", "closeout")
                return target

            return target

    return "blocked"  # no transition matched


def _matches_condition(condition: str, result: HarnessResult, validation: ValidationResult) -> bool:
    """Check if an execution result matches a transition condition."""
    conditions = {
        "pass": result.status == "pass" and validation.get("passed", True),
        "fail": result.status == "fail",
        "output_valid": len(result.artifacts_written) > 0,
        "output_invalid": len(result.artifacts_written) == 0,
        "max_retries": False,  # handled by resolve_transition
        "max_cycles_reached": False,  # handled by resolve_transition
        "unstructured": result.status == "fail" and not result.reason,
        "always": True,
    }
    return conditions.get(condition, False)
```

---

## Iteration Counter Management

Counters are stored in `checkpoint.json` under the `counters` key. They persist across orchestrator restarts for crash recovery.

### Counter Structure

```json
{
  "counters": {
    "load_context": {"retries": 0, "ralph_cycles": 0},
    "implement_change": {"retries": 2, "ralph_cycles": 0},
    "audit_output": {"retries": 1, "ralph_cycles": 0},
    "review_via_ralph": {"retries": 1, "ralph_cycles": 1},
    "ralph_revise": {"retries": 0, "ralph_cycles": 1},
    "validate": {"retries": 0, "ralph_cycles": 0},
    "close": {"retries": 0, "ralph_cycles": 0}
  }
}
```

### Counter Rules

1. **Retries increment** when a phase produces `status: "fail"` and the orchestrator transitions to the same state.
2. **Ralph cycles increment** when the orchestrator transitions from `ralph_revise` back to `ralph_critique`.
3. **Counters reset** when a phase completes successfully (moves to a different state).
4. **Counters do NOT reset** across orchestrator restarts (crash recovery).
5. **Max retries** is read from the state definition in the workflow config (`max_retries` field).
6. **Max Ralph cycles** is read from the `ralph_critique` state definition (`ralph_max_cycles` field).

### Counter Update Logic

```python
def update_counters(
    counters: dict,
    current_state: str,
    next_state: str,
    config: dict,
) -> dict:
    """Update retry and cycle counters based on state transition."""
    counters = deepcopy(counters)

    # Initialize if missing
    if current_state not in counters:
        counters[current_state] = {"retries": 0, "ralph_cycles": 0}

    if current_state == next_state:
        # Retry: increment retry counter
        counters[current_state]["retries"] += 1
    elif current_state == "ralph_revise" and next_state == "ralph_critique":
        # Ralph cycle complete: increment cycle counter
        counters["ralph_critique"]["ralph_cycles"] += 1
    elif current_state == "ralph_critique" and next_state != "ralph_revise":
        # Ralph cycle exited: mark done
        pass
    else:
        # Phase completed successfully: reset counters for this state
        counters[current_state] = {"retries": 0, "ralph_cycles": 0}

    return counters
```

### Counter Validation Before Execution

Before dispatching each step, the orchestrator validates the counter state:

```python
def validate_counters(state: str, counters: dict, state_def: dict) -> bool:
    """Return True if the step can proceed. Return False if max limits exceeded."""
    if state not in counters:
        return True  # no prior attempts

    max_retries = state_def.get("max_retries", 3)
    max_cycles = state_def.get("ralph_max_cycles", 2)

    if counters[state]["retries"] >= max_retries:
        return False  # blocked

    if state == "ralph_critique" and counters[state]["ralph_cycles"] >= max_cycles:
        return False  # max cycles reached

    return True
```

---

## Validation Integration

Validation is NOT a separate state in most workflows. It is a GATE that runs after certain states. The orchestrator runs validators and uses the result in transition decisions.

### When Validation Runs

| Trigger | What Gets Validated | Schema |
|---|---|---|
| After `execute` completes | Expected output files exist, are non-empty, match schemas | phase_contract.schema.json |
| After `audit` completes | AUDIT_REPORT.md has required sections | audit_result.schema.json |
| After `fix` completes | Same as `execute` validation | phase_contract.schema.json |
| After `ralph_critique` completes | Critique output has required fields | critique_schema (implied in ralph config) |
| After `closeout` completes | All terminal artifacts exist | closeout schema |
| At startup (always) | Config file, state directory, checkpoint | workflow_config.schema.json |

### Validation Failure → Transition Mapping

| Validation Failure | Current State | Next State |
|---|---|---|
| Config schema invalid | init | blocked |
| Task state missing | init | plan (auto-create) |
| Output artifacts missing | execute | execute (retry) |
| Audit report schema invalid | audit | audit (retry) |
| Critique missing required fields | ralph_critique | ralph_revise (proceed anyway) |
| Closeout incomplete | closeout | closeout (retry) |
| All required files present | any | Continue to next state |

### Validator Function Signature

```python
def validator_fn(
    state_dir: Path,
    expected_outputs: list[str],
    validation_config: dict,
) -> ValidationResult:
    """
    Run all configured validators and return combined result.

    Standard validators (registered in scripts/validators/):
    - file_exists: check every expected_outputs file exists
    - json_schema: validate JSON/YAML files against schema
    - command_exit_zero: run configured commands, check exit code 0
    - regex_match: check file content against regex patterns
    - content_non_empty: check files are not empty
    """
    ...
```

---

## Audit/Ralph Loop Examples

### Example 1: Simple Audit (single pass)

```
execute → audit (pass) → closeout → done
```

No loop needed. One audit pass confirms the output is correct.

### Example 2: Audit with Fix Loop

```
execute → audit (fail: missing evidence) → fix → audit (pass) → closeout → done
```

One fix iteration. The audit identified missing evidence, the fix added it, the second audit passed.

### Example 3: Full Ralph Loop

```
execute → audit (pass) → ralph_critique → ralph_revise → ralph_critique → ralph_revise
  → ralph_critique (max_cycles=2 reached) → closeout → done
```

Two Ralph cycles completed, then the workflow advanced to closeout even if the critique still had findings.

### Example 4: Blocked After Limit

```
execute → audit (fail) → fix → audit (fail) → fix → audit (fail) → fix
  → audit (max retries=3) → blocked
```

Three fix-audit cycles exhausted the retry budget. Human intervention required.

---

## Configuring Ralph in Workflow Config

Ralph behavior is configured in the state definition for `ralph_critique`:

```yaml
states:
  review_via_ralph:
    state: ralph_critique
    agent: contextsmith-auditor
    permissions: read-only
    max_retries: 2
    ralph_max_cycles: 2    # Number of critique-revise cycles before forced advance
    transitions:
      - condition: pass
        target: ralph_revise
      - condition: fail
        target: ralph_revise   # Even on fail, we revise and try again
      - condition: max_cycles_reached
        target: closeout
```

Key rule: `ralph_max_cycles` is checked during transition resolution. When cycles reach the limit, the orchestrator overrides the normal transition target and routes to the configured terminal target (default: `closeout`).
