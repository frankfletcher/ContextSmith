# OpenCode Feature Analysis for ContextSmith

**Date:** 2026-06-09
**Purpose:** Assess which OpenCode features matter for ContextSmith, and how they fit with the orchestrator idea.

## Executive Summary

The highest-value pieces are **Custom Tools**, **Plugins**, and the **orchestrator** itself. OpenCode should be the runtime layer that executes one bounded step at a time. The orchestrator should own state, retries, transitions, and checkpoints. Commands are just launchers, agents are just role-specific executors, and MCP/ACP are lower-priority integration surfaces.

## How the Pieces Fit

- **Orchestrator**: deterministic state machine, checkpoint/resume, retries, loop detection.
- **OpenCode agents**: bounded execution profiles for audit, fix, migrate, and review.
- **Custom tools**: optional gates for phase completion and validation.
- **Plugins**: harness-level enforcement for validation on edit and compaction state.
- **Commands**: user-facing shortcuts that start the right workflow.

The main rule is simple: if something can be enforced in code, it belongs in the orchestrator; if it is about what the model may do, it belongs in the agent profile.

## 1. Custom Tools

Custom tools are useful for workflow gates like `phase_complete`, `artifact_check`, and `validation_run`. They can make transitions explicit, but they should not replace the orchestrator's checkpointed state machine. Their job is to reduce manual friction, not to become the source of truth.

## 2. Agents

Agent profiles are useful because they let us define:

- read-only audit roles
- edit-capable build roles
- limited-bash migration roles
- review-only subagents
- step caps for loop control

For this project, temperature is not the important lever. Permissions, step limits, and model pinning matter more. A default agentic temperature around 0.6 is fine; determinism should come from the workflow controller and validation gates.

## 3. Commands

Commands are useful as launch points:

- `/contextsmith-audit`
- `/contextsmith-build`
- `/contextsmith-migrate`
- `/contextsmith-validate`

They improve workflow entry correctness, but they do not prevent drift mid-run. That is the orchestrator's job.

## 4. Plugins

Plugins are the strongest harness-level enforcement mechanism. They can:

- run validation when SKILL.md changes
- inject workflow state during compaction
- block disallowed operations before execution

That makes them a good companion to the orchestrator, especially when a step boundary needs to be enforced even if the model wanders.

## 5. ACP and MCP

ACP is just transport. MCP can expose validation services, but it adds more overhead than we need right now. Both are lower priority than custom tools and plugins.

## Recommended Architecture

1. Python orchestrator owns the workflow graph.
2. OpenCode agents execute one step at a time.
3. Validators check file existence, line counts, command exit codes, and schemas.
4. Checkpoints live in `.agent_work/`.
5. Commands launch the right workflow.
6. Tools/plugins add optional harness enforcement.

## Bottom Line

The orchestrator makes the workflow deterministic. OpenCode makes the agent execution bounded and reproducible. Together, they solve different parts of the same problem.
