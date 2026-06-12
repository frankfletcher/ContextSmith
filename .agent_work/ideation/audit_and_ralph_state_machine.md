# Audit and Ralph State Machine Sketch

> **Superseded.** This is an early draft. The authoritative version is at `deep_determinism/audit_and_ralph_state_machine.md` — it has the same content enriched with a complete 24-row state transition matrix, iteration counter management, validation integration, and 4 execution examples.

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
