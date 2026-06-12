# Deep Determinism

Detailed specifications for the ContextSmith deterministic execution system. These files are enriched for planner-to-executor translation — they contain exact data formats, interface contracts, state machine definitions, and error-handling procedures needed to build the orchestrator, harness adapters, and artifact system.

## Architecture

Two execution paths share the same contracts:

```
Path 1: Skill-only (universal, zero infrastructure)
  User → Orchestrator skill → Agent follows instructions → loops itself
  Requirements: an agent that can read files and follow instructions

Path 2: Harness-aware (deterministic, optimized)
  User → Router skill → Orchestrator (Python, built-in loop)
    → Harness adapter → Agent subprocess → RESULT.json
  Requirements: Python, a harness with bash access
```

Both paths use identical workflow configs, artifact contracts, checkpoint formats, and validation rules. The difference is who runs the loop: the agent (skill-only) or Python code (harness-aware).

Key design decisions:
- **Orchestrator skill** is the universal base — works in any harness, ~200 lines
- **Harness companions** are thin reference files (~40 lines each) that add harness-specific optimizations — they enhance but never gate
- **Orchestrator-as-code** adds determinism, crash recovery, external validation, and timeout enforcement
- **RESULT.json** on disk is the structured result channel (NOT stdout)
- **Schemas** are JSON Schema files that validate configs and artifacts

## Start Here

**New to this system?** Read in this order:
1. This file (index)
2. `orchestrator_as_skill.md` (two execution paths — start here to understand the design)
3. `implementation_guide.md` (linear implementation path)
4. `orchestrator_idea.md` (core state machine and architecture)
5. `orchestrator_and_harness.md` (interface contracts — canonical type definitions)
6. Then reference other files as needed per the implementation guide

## Blocking Prerequisites

The following must be created before any implementation code:

| Prerequisite | Status | Notes |
|-------------|--------|-------|
| `schemas/workflow_config.schema.json` | **Done** | Validates both example configs, 10/10 negative tests pass |
| `schemas/agent_config.schema.json` | **Done** | Validates both example agent configs |
| OpenCode CLI flag verification | **Verified** | `--agent`, `--model`, `--prompt`, `--file`, `--format json` confirmed. `--max-steps` does not exist — use agent config `steps` field instead. See `orchestrator_and_harness.md` adapter section. |
| Plan generation pipeline | **Designed** | `workflow_developer_skill.md` spec complete, domain templates created |

See `implementation_prerequisites.md` for the full gap analysis.

## File Role Map

| File | What It Specifies | Key Detail Added |
|------|-------------------|-------------------|
| [Implementation Guide](implementation_guide.md) | Linear implementation path, canonical type locations, build order | Phase-by-phase deliverables, gates, spec file map, minimal artifact set |
| [Orchestrator Idea](orchestrator_idea.md) | State machine spec, CLI, checkpoint format, startup/resume, error matrix, function reference | Complete state transition table, orchestrator.py function signatures, checkpoint JSON schema, CLI interface, error handling matrix |
| [Orchestrator and Harness](orchestrator_and_harness.md) | Harness adapter interface, subprocess model, error propagation | HarnessAdapter ABC, StepContract/HarnessResult dataclasses, HarnessRegistry, OpenCode adapter specifics, subprocess timeout enforcement |
| [System Components](system_components.md) | Component map | No changes (conceptual map, not implementation spec) |
| [Workflow Config Sketch](workflow_config_sketch.md) | Workflow config YAML/JSON schema, field reference, examples, overlay mechanics | Complete schema with types and validation rules, 2 full examples, overlay resolution algorithm, 13 field validation rules |
| [Agent Startup and Communication](agent_start_and_communication.md) | Launch packet format, artifact collection, step cap enforcement | LaunchPacket dataclass, artifact collection procedure with validation, step cap detection, agent instruction file format |
| [Harness Agnostic Distribution](harness_agnostic_distribution.md) | Adapter lifecycle, reference loading, new harness guide | Adapter lifecycle states, reference loading protocol with ordered steps, step-by-step new harness guide, generic adapter spec |
| [Orchestrator as Skill](orchestrator_as_skill.md) | Skill-only execution path, harness companion model, installation methods | Orchestrator-as-skill loop spec, companion template, 3 installation methods, contextsmith-run relationship |
| [Workflow Developer Skill](workflow_developer_skill.md) | Plan generation from natural language, domain templates | Workflow config generation process, domain templates, Ralph integration, overlay support |
| [Migration: run to orchestrator](migration_run_to_orchestrator.md) | Backward compatibility, migration paths, coexistence model | Task-state compatibility, config generation from existing workflows, timeline |
| [State Artifacts and Agent Handoffs](state_artifact_strategy.md) | Required sections per artifact, field-level validation | Exact markdown templates for all 13 artifact files, field-level requirements table, validation pseudocode, write atomicity protocol |
| [Implementation Prerequisites](implementation_prerequisites.md) | Gaps to resolve before coding | Sections 9-15 added: plan generation, deviation protocol, human escalation, idempotency, dependencies, run comparison, skill-orchestrator contract |
| [Audit and Ralph State Machine Sketch](audit_and_ralph_state_machine.md) | Loop enforcement, transition table, iteration counters | Complete state transition matrix (24 rows), iteration counter management, validation integration, 4 execution examples |
| [Communications Protocol Sketch](communications_protocol_sketch.md) | Message schemas, transport decisions, protocol sequences | 3 open choices resolved, JSON schemas for StepRequest/StepResult/ErrorEnvelope, normal/timeout/crash sequences, 7 message validation rules |
| [OpenCode Feature Analysis](opencode-analysis-report.md) | OpenCode feature assessment | No changes (analysis doc, not implementation spec) |
| [Token Optimization Ideas](token_optimization_ideas.md) | Token cost reduction | No changes (skills-focused, not orchestrator) |
| [Orchestrator Skill Draft](orchestrator_skill_draft.md) | Concrete SKILL.md for skill-only path | Agent-facing instructions, loop logic, artifact validation, RESULT.json, checkpoint format |
| [Harness: OpenCode](harness-opencode.md) | OpenCode harness companion | Verified CLI flags, agent config format, permission model, step limiting, result protocol |
| [End-to-End Example](end_to_end_example.md) | Full workflow walkthrough | User sees: confirmations, progress, validation, summary. Covers all phases from start to done. |
| [Domain Templates](domain-templates/) | Default workflow shapes per domain | coding, writing, research, migration, audit, general — each with phases, gates, states, transitions |

## Usage

These files are authored for the **planner agent** — a model that converts these specifications into atomic instructions for a **small model executor**. The planner should not need to infer or guess any interface contract, data format, or error path. Every interface, every file format, every state transition, and every error response is specified explicitly.

## Content Counts

| File | Lines | Detail Type |
|------|-------|-------------|
| implementation_guide.md | ~150 | Implementation path |
| orchestrator_idea.md | ~330 | Implementation specification |
| orchestrator_and_harness.md | ~280 | Interface contract |
| workflow_config_sketch.md | ~320 | Data schema |
| agent_start_and_communication.md | ~420 | Launch procedure |
| communications_protocol_sketch.md | ~350 | Message protocol |
| audit_and_ralph_state_machine.md | ~280 | State transitions |
| harness_agnostic_distribution.md | ~370 | Adapter interface |
| orchestrator_as_skill.md | ~200 | Skill-only path, companion model |
| workflow_developer_skill.md | ~150 | Plan generation, domain templates |
| migration_run_to_orchestrator.md | ~150 | Backward compatibility, migration paths |
| state_artifact_strategy.md | ~370 | File formats |
| orchestrator_skill_draft.md | ~250 | Concrete SKILL.md for skill-only path |
| harness-opencode.md | ~100 | OpenCode harness companion |
| end_to_end_example.md | ~200 | Full workflow walkthrough |
| domain-templates/ (6 files) | ~500 | Default workflow shapes per domain |
| implementation_prerequisites.md | ~830 | Gap analysis |
