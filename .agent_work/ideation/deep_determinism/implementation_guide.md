# Implementation Guide

This document provides a linear implementation path through the deep determinism specs. Read this first, then reference the linked spec files for details on each component.

## Architecture Overview

Two execution paths share the same contracts:

**Path 1: Skill-only (universal, zero infrastructure)**
```
User → Orchestrator skill → Agent follows instructions → loops itself
```
Requirements: an agent that can read files and follow instructions. The agent IS the executor. Less deterministic, but works in any harness.

**Path 2: Harness-aware (deterministic, optimized)**
```
User → Router skill → Orchestrator (Python, built-in loop)
  → Harness adapter → Agent subprocess → RESULT.json
```
Requirements: Python, a harness with bash access. Code drives the loop. More deterministic, with crash recovery and external validation.

Both paths use identical workflow configs, artifact contracts, checkpoint formats, and validation rules. See `orchestrator_as_skill.md` for the full design.

## Build Order

Follow this sequence. Each phase has a gate — do not proceed until the gate passes.

### Phase 1: Schemas (days 1-3)

**Why first:** Every other component validates against these schemas.

**Files to read:**
- `workflow_config_sketch.md` — complete schema specification (lines 83-268)
- `implementation_prerequisites.md` — section 2 (validation schemas)

**Deliverables:**
1. `schemas/workflow_config.schema.json` — validates workflow config YAML/JSON **(done)**
2. `schemas/phase_contract.schema.json` — validates step inputs/outputs
3. `schemas/agent_config.schema.json` — validates OpenCode agent frontmatter **(done)**
4. `scripts/validate_workflow.py` — reads a config, validates against schema

**Gate:** Validation script passes against the two complete examples in `workflow_config_sketch.md` (simple audit at line 272, engineering workflow at line 383). **Gate passed — both examples validate.**

### Phase 2: Core Orchestrator (days 4-10)

**Why second:** The orchestrator is the control plane. Nothing runs without it.

**Files to read:**
- `orchestrator_idea.md` — state machine (lines 100-224), main loop (lines 227-278), CLI (lines 294-333), checkpoint format (lines 337-401), startup/resume (lines 404-469), error matrix (lines 484-503)
- `orchestrator_and_harness.md` — `StepContract` dataclass (line 133), `HarnessResult` dataclass (line 153)
- `audit_and_ralph_state_machine.md` — transition table (lines 119-156), counter management (lines 219-300), validation integration (lines 304-350)

**Deliverables:**
1. `orchestrator/orchestrator.py` — state machine, step selection, checkpoint read/write, outer loop runner
2. `orchestrator/state_reader.py` — parse STATUS.md, PLAN.md, CONTEXT.md
3. `orchestrator/step_compiler.py` — compile StepContract from config + state
4. `orchestrator/checkpoint.py` — checkpoint read/write with atomic writes

**Gate:** Orchestrator can load a workflow config and task-state directory, print the next valid step (via `--dry-run`), and exit 0.

**Key design rule:** The outer loop (`run_workflow`) is a pure Python `while` loop on exit code. No LLM, no agent, no judgment. The orchestrator's `run()` function handles one step; `run_workflow()` calls it until done.

### Phase 3: Harness Adapters (days 11-15)

**Files to read:**
- `orchestrator_and_harness.md` — `HarnessAdapter` ABC (line 165), `HarnessRegistry` (line 253), OpenCode adapter (lines 339-413), error propagation (lines 417-459)
- `agent_start_and_communication.md` — `LaunchPacket` (lines 260-296), artifact collection (lines 400-436), step cap enforcement (lines 503-558)

**Deliverables:**
1. `orchestrator/adapters/base.py` — `HarnessAdapter` ABC, `HarnessResult`, `StepContract`, error types
2. `orchestrator/adapters/opencode.py` — OpenCode adapter (streaming subprocess, RESULT.json reading)
3. `orchestrator/adapters/generic.py` — generic fallback adapter (RESULT.json + artifact checking)

**Gate:** OpenCode adapter can run an audit step end-to-end and return a valid `HarnessResult`.

### Phase 4: Validation (days 16-18)

**Files to read:**
- `state_artifact_strategy.md` — required sections per artifact (lines 221-445), field-level requirements (lines 449-508)
- `audit_and_ralph_state_machine.md` — validation integration (lines 304-350)

**Deliverables:**
1. `orchestrator/validators.py` — file existence, section presence, schema validation
2. `scripts/validate_artifacts.py` — standalone artifact validation

**Gate:** Validators pass against a known-good task-state directory and fail against a known-bad one.

### Phase 5: Integration (days 19-25)

**Files to read:**
- `communications_protocol_sketch.md` — protocol flow (lines 373-407), message schemas (lines 200-369)
- `harness_agnostic_distribution.md` — adapter lifecycle (lines 400-427), reference loading (lines 430-480)

**Deliverables:**
1. Wire orchestrator into `contextsmith-run` skill
2. `--harness` flag integration
3. Conditional reference loading
4. End-to-end test: user runs `contextsmith run <config>` and the full cycle completes

**Gate:** `contextsmith run <config> --state <dir>` executes the full cycle through orchestrator, adapter, agent, and validation.

## Canonical Data Structure Locations

These types are defined once. Reference them from other files.

| Type | Defined In | Line |
|------|-----------|------|
| `StepContract` | `orchestrator_and_harness.md` | 133 |
| `HarnessResult` | `orchestrator_and_harness.md` | 153 |
| `HarnessAdapter` (ABC) | `orchestrator_and_harness.md` | 165 |
| `HarnessRegistry` | `orchestrator_and_harness.md` | 253 |
| `HarnessTimeoutError` | `orchestrator_and_harness.md` | 231 |
| `HarnessExecutionError` | `orchestrator_and_harness.md` | 238 |
| `LaunchPacket` | `agent_start_and_communication.md` | 263 |
| Checkpoint format | `orchestrator_idea.md` | 341 |
| State machine transitions | `audit_and_ralph_state_machine.md` | 119 |
| Workflow config schema | `workflow_config_sketch.md` | 83 |

## Assumptions That Need Verification

Before implementation, verify these:

1. **OpenCode CLI flags:** `--agent`, `--model`, `--prompt-file`, `--max-steps` — used in `orchestrator_and_harness.md:356-377` and `agent_start_and_communication.md:519-521`. Check against actual OpenCode CLI.
2. **OpenCode agent config format:** YAML frontmatter in `.opencode/agents/*.md` — used in `system_components.md:179-204`. Check against actual OpenCode agent config spec.
3. **OpenCode plugin API:** TypeScript hooks (`file.edited`, `tool.execute.after`, `experimental.session.compacting`) — used in `opencode-analysis-report.md:171-191`. Check against actual OpenCode plugin API.

## Minimal Artifact Set

For MVP, use 7 artifacts per phase (reduced from 13). Add others only when the workflow requires them.

| Artifact | Always Required | Purpose |
|----------|----------------|---------|
| `STATUS.md` | Yes | Current phase and next action |
| `PLAN.md` | Yes | Phase checklist |
| `NEXT_PROMPT.md` | Yes | Handoff to next agent |
| `CHECKLIST.md` | Yes | Per-phase task tracking |
| `PHASE_LOG.md` | Yes | Compact phase history |
| `CONTEXT.md` | Yes | File map and constraints |
| `ARTIFACTS.md` | Yes | Files changed and commands run |

**Optional (add when workflow requires):**
- `AUDIT_REPORT.md` — when audit gate is present
- `EVIDENCE.md` — when validation needs proof
- `SUMMARY.md` — for user-facing closeout
- `EDUCATIONAL_REPORT.md` — when the user needs to learn
- `DECISIONS.md` — when durable decisions need tracking
- `TASK.md` — for initial task definition (may be folded into STATUS.md for simple workflows)
- `REVIEW_NOTES.md` — for follow-up review

## Spec File Map

| File | Role | Key Content |
|------|------|-------------|
| `README.md` | Index | File role map, content counts |
| `orchestrator_idea.md` | Core spec | State machine, CLI, checkpoint, startup/resume, error matrix |
| `orchestrator_and_harness.md` | Interface contract | StepContract, HarnessResult, HarnessAdapter ABC, error types |
| `workflow_config_sketch.md` | Data schema | Complete config schema, examples, overlay mechanics, validation rules |
| `agent_start_and_communication.md` | Launch procedure | LaunchPacket, artifact collection, step cap enforcement |
| `communications_protocol_sketch.md` | Message protocol | JSON schemas, protocol sequences, validation rules |
| `audit_and_ralph_state_machine.md` | Loop enforcement | Transition matrix, counter management, validation integration |
| `harness_agnostic_distribution.md` | Adapter model | Adapter lifecycle, reference loading, new harness guide |
| `orchestrator_as_skill.md` | Skill-only path | Orchestrator-as-skill loop, harness companion model, installation methods |
| `state_artifact_strategy.md` | File formats | Artifact templates, field-level requirements, write atomicity |
| `system_components.md` | Component map | High-level overview of all components |
| `implementation_prerequisites.md` | Gap analysis | 15 open decisions, MVP build order, testing strategy |
| `opencode-analysis-report.md` | Feature assessment | OpenCode feature analysis, implementation priority |
| `token_optimization_ideas.md` | Token reduction | Cross-skill duplication, invocation cost reduction |
| `implementation_guide.md` | This file | Linear implementation path, canonical type locations |
