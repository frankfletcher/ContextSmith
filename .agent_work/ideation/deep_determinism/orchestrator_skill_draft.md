---
name: contextsmith-orchestrator
description: Execute workflow configs through a deterministic state machine loop. Use when running a workflow config YAML, resuming a task-state handoff, or executing phased work with validation gates and checkpoint recovery.
metadata:
  version: "1.0.0"
  package: ContextSmith
  target: local-open-weight-models
---

# ContextSmith Orchestrator

Execute a workflow config through a state machine loop. You are the executor — you do the work, validate artifacts, update state, and loop until done or blocked.

## Quick Use

```
/contextsmith-orchestrator
```

The skill reads a workflow config and executes it phase by phase.

## Confirmation Before Execution

Before starting, summarize parameters and plan, then ask the user to confirm. Use `references/run-configuration-preview.md` for the format. Only proceed on positive indication (yes, ok, go, execute, proceed).

Skip confirmation only with `--mode yolo` or explicit "just do it".

## The Loop

You execute this loop. Each iteration is one phase.

```
1. Read workflow_config.yaml (or .json)
2. Read STATUS.md → current_phase field
3. If current_phase is "done" or "blocked" → stop
4. Look up current_phase in workflow config → get state definition
5. Read NEXT_PROMPT.md → your bounded task
6. Read CONTEXT.md → constraints and file map
7. Execute the phase:

   a. Do the work described in NEXT_PROMPT.md
   b. Write expected_outputs per the state definition

8. Validate your artifacts:

   a. Check every expected_output file exists and is non-empty
   b. Check required sections present (see Artifact Templates below)
   c. If validation fails and retries < max_retries → retry
   d. If validation fails and retries >= max_retries → set status to "blocked"

9. Write RESULT.json to the task-state directory
10. Update state files:

    a. Write checkpoint.json (phase, status, counters)
    b. Update STATUS.md (current_phase, next_action)
    c. Append to PHASE_LOG.md
    d. Update CHECKLIST.md (mark completed items)

11. Determine next phase:

    a. Read transitions from the state definition
    b. Match your result status to a transition condition
    c. The target is your next current_phase

12. Write NEXT_PROMPT.md for the next phase
13. Update STATUS.md with the new current_phase
14. Re-read STATUS.md → go to step 2
```

## State Determination

On each loop iteration, read STATUS.md to determine where you are:

```markdown

# Status

## Current Phase
implement_change

## Current State
execute

## Progress

- Phase: 2 of 5
- Checklist: 1/4 complete
- Retries remaining: 3

## Next Action
Implement the error recovery model per NEXT_PROMPT.md

## Blocked By
none
```

The `Current Phase` field maps to a key in the workflow config's `states` section. Look up the state definition to get permissions, transitions, expected outputs, and retry limits.

## Artifact Validation

After writing artifacts, validate them:

```python

# For each expected_output in the state definition:
for artifact_name in state_definition["expected_outputs"]:
    path = task_state_dir / artifact_name
    if not path.exists():
        status = "fail"
        reason = f"Missing artifact: {artifact_name}"
    elif path.stat().st_size == 0:
        status = "fail"
        reason = f"Empty artifact: {artifact_name}"
    else:

        # Check required sections (see Artifact Templates)
        missing = check_required_sections(path, artifact_name)
        if missing:
            status = "fail"
            reason = f"Missing sections in {artifact_name}: {missing}"
```

If all artifacts pass → status = "pass".
If any artifact fails → status = "fail", retry up to max_retries.

## RESULT.json

After validating artifacts, write RESULT.json to the task-state directory:

```json
{
  "status": "pass",
  "reason": "All artifacts produced and validated",
  "artifacts": ["ARTIFACTS.md", "PHASE_LOG.md", "CHECKLIST.md"],
  "issues": [],
  "next_action": "done"
}
```

Status values: `pass`, `fail`, `blocked`.
Next action values: `done`, `retry`, `fix`, `stop`.

## Checkpoint.json

After each phase, write checkpoint.json:

```json
{
  "workflow_id": "my-workflow",
  "version": 1,
  "current_phase": "implement_change",
  "current_state": "execute",
  "last_updated": "2026-06-12T10:30:00Z",
  "completed_phases": ["load_context"],
  "counters": {
    "implement_change": {"retries": 0, "ralph_cycles": 0}
  },
  "last_result": {
    "state": "execute",
    "status": "pass",
    "artifacts_written": ["ARTIFACTS.md", "PHASE_LOG.md"]
  }
}
```

## Transition Resolution

After validation, determine the next phase:

1. Read the `transitions` list from the current state definition
2. Match your result to a condition:
   - `pass` → result.status == "pass"
   - `fail` → result.status == "fail"
   - `output_valid` → all expected artifacts exist
   - `output_invalid` → some artifacts missing
   - `always` → always matches
   - `max_retries` → retries >= max_retries
3. The matching transition's `target` is the next phase
4. If no transition matches → next phase is "blocked"

## Retry Logic

When validation fails:

1. Increment the retry counter in checkpoint.json
2. If retries < max_retries → stay in current phase, retry
3. If retries >= max_retries → follow the `max_retries` transition (usually "blocked")

When retrying, re-read NEXT_PROMPT.md and try again. Don't repeat the same approach — change something.

## Ralph Loop

If the state has `ralph_max_cycles` > 0:

1. Execute the phase normally
2. After execution, critique your own output (what could be better?)
3. Revise based on the critique
4. Increment ralph_cycles in checkpoint.json
5. If ralph_cycles < ralph_max_cycles → critique again
6. If ralph_cycles >= ralph_max_cycles → move to next phase

Ralph is self-improvement, not blind iteration. Each cycle should address a concrete defect.

## Artifact Templates

### STATUS.md

```markdown

# Status

## Current Phase
<phase-name>

## Current State
<state-name>

## Progress

- Phase: <N> of <M>
- Checklist: <X>/<Y> complete
- Retries remaining: <N>

## Next Action
<what should happen next>

## Blocked By
<none or description>
```

### PHASE_LOG.md

```markdown

# Phase Log

## Phase <name>
Date: <ISO 8601>
State: <state-name>
Action: <what was done>
Result: <pass/fail/blocked>
Artifacts: <list>
```

### CHECKLIST.md

```markdown

# Checklist

- [x] <completed item>
- [ ] <pending item>
```

### NEXT_PROMPT.md

```markdown

# Next Prompt

## Current Status

- Phase: <phase-name>
- State: <state-name>
- Completed: <list>

## Your Task
<specific bounded instruction>

## Input Files

- <file>: <what to read>

## Output Requirements

- <file>: <what to write>

## Constraints

- <limits>
```

## Termination

The loop ends when:

- STATUS.md `Current Phase` is "done" → workflow complete
- STATUS.md `Current Phase` is "blocked" → human intervention needed
- You've been in the same phase for max_retries → set to "blocked"
- The user interrupts (Ctrl-C, or says "stop")

## Harness-Specific Behavior

When running in a harness with a structured question tool (e.g., `AskUserQuestion` in OpenCode), use it for confirmations. When running in a harness without one, ask in natural language and wait for a response.

When running with RESULT.json support (harness-aware path), write RESULT.json after each phase. The harness reads it for structured status.

When running without RESULT.json support (skill-only path), your status is determined by artifact presence and validation results.

## Reference Loading

| Need | Read |
| ------ | ------ |
| Every run | `references/run-configuration-preview.md` |
| Workflow config format | `workflow_config_sketch.md` (in deep_determinism) |
| Artifact templates | `state_artifact_strategy.md` (in deep_determinism) |
| Transition rules | `audit_and_ralph_state_machine.md` (in deep_determinism) |
| Checkpoint format | `orchestrator_idea.md` (in deep_determinism) |

## Token Budget

Target: under 300 lines. This skill is the executor — keep it lean.
