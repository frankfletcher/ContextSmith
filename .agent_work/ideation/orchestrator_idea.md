# Orchestrator Idea

> **Superseded.** This is an early draft. The authoritative version is at `deep_determinism/orchestrator_idea.md` — it has the same content enriched with complete state transition tables, function signatures, checkpoint schemas, CLI interface, and error handling matrix.

## Problem Statement

Agent-driven workflows are non-deterministic. The model forgets steps, gets cut off, and spends tokens re-deriving its own control flow. That control flow should live in code. OpenCode should be the execution substrate, not the workflow brain.

## Goal

- Deterministic execution: every action item completes or produces a clear error
- Token reduction: remove orchestration from prompts and reference material
- Resilience: retry and resume after interruptions without losing state
- Simplicity: give the agent one bounded task at a time

## System Model

Three layers:

1. **Orchestrator** - Python state machine that owns workflow state, transitions, retries, and checkpoints.
2. **Harness** - OpenCode runtime that executes one bounded step with permissions, tools, and validation hooks.
3. **Artifacts** - task-state files, validation outputs, and phase closeouts that make the run resumable.

OpenCode is a leaf executor. The orchestrator decides what comes next.

Baseline workflow shape should live in YAML or JSON config, with agent-generated plans acting as overlays that can add or remove optional steps but cannot redefine the required workflow on their own.

## Execution Flow

1. User starts from `NEXT_PROMPT.md` or an implementation plan.
2. Orchestrator loads `STATUS.md`, `PLAN.md`, and `CONTEXT.md`.
3. Orchestrator compiles the current step contract.
4. Orchestrator picks the next state and the matching OpenCode agent profile.
5. Harness executes the step under permission limits and step caps.
6. Validators check outputs on disk.
7. Orchestrator records checkpoint, phase log, and next prompt.
8. Orchestrator retries, advances, or stops.

## Responsibilities

### Orchestrator

- owns workflow graph
- owns retry policy
- owns checkpoint timing
- owns loop detection
- owns resume semantics

### Harness

- enforces permissions
- limits step count
- invokes agents and tools
- runs validation hooks
- blocks bad operations before execution

### Agent

- completes one bounded task
- writes artifacts to known files
- does not decide the workflow shape

## OpenCode Role

OpenCode fits as the runtime layer for `AgentInvoker`:

- **Agent profiles** map to states like audit, fix, review, migrate
- **Permissions** define what the model can touch
- **Step caps** keep one invocation from looping forever
- **Custom tools** can enforce gates, but do not replace the orchestrator
- **Plugins** can validate edits and preserve state across compaction
- **Commands** are launchers, not control flow

## Failure Model

- Agent invocation failure -> retry with backoff
- Structural validation failure -> retry the same state
- Review failure -> transition to a fix/retry state
- Loop detection failure -> abort with a clear error
- Missing checkpoint or task-state file -> stop and request recovery

## Design Rule

If a behavior can be enforced in code, put it in the orchestrator.
If a behavior is about model permissions, put it in the harness agent profile.
If a behavior is about blocking tool misuse, put it in a plugin or custom tool.

## Next Implementation Slice

- define baseline workflow config schema (YAML/JSON)
- define workflow DSL
- define task-state contract
- define OpenCode agent profiles
- define validator registry
- define checkpoint format
- define resume semantics from `NEXT_PROMPT.md`
- define audit and Ralph loop state machine ([audit_and_ralph_state_machine.md](audit_and_ralph_state_machine.md))
- define communications protocol between orchestrator, harness, and agent ([communications_protocol_sketch.md](communications_protocol_sketch.md))
