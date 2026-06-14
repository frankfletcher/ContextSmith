# Artifact Templates

Reference for the standard task-state artifact templates used by the orchestrator skill. These files are written and updated throughout a workflow execution.

## STATUS.md

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

## PHASE_LOG.md

```markdown
# Phase Log

## Phase <name>
Date: <ISO 8601>
State: <state-name>
Action: <what was done>
Result: <pass/fail/blocked>
Artifacts: <list>
```

## CHECKLIST.md

```markdown
# Checklist

- [x] <completed item>
- [ ] <pending item>
```

## NEXT_PROMPT.md

When generating NEXT_PROMPT.md for handoff, include a `.phase_gate` guard at the top:

```
## Gate: .phase_gate

This prompt is queued for the next run. Do NOT execute until
`<task-dir>/.phase_gate` exists. If the file is missing, stop and
report "Phase gate not set. Awaiting human instruction to proceed."
```

The downstream agent creates `<task-dir>/.phase_gate` when ready to proceed. This gives the human operator a chance to review before side effects occur.

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

## RESULT.json

```json
{
  "status": "pass",
  "reason": "All artifacts produced and validated",
  "artifacts": ["ARTIFACTS.md", "PHASE_LOG.md", "CHECKLIST.md"],
  "issues": [],
  "next_action": "done"
}
```

Status values: `pass`, `fail`, `blocked`. Next action: `done`, `retry`, `fix`, `stop`.

## Checkpoint.json

```json
{
  "workflow_id": "my-workflow",
  "version": 1,
  "current_phase": "implement_change",
  "current_state": "execute",
  "last_updated": "2026-06-13T00:00:00Z",
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

If `checkpoint_before_run` is true for the state, the orchestrator also writes a pre-dispatch checkpoint marker before agent execution. On startup, it warns about stale pre-dispatch markers (possible crash evidence).
