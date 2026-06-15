# Runtime Enforcement: How To Use It

Runtime reinforcement and orchestration is a first-class ContextSmith tool. It is the **default execution path** — users get validation, gate enforcement, and phase progression automatically — but it is **opt-out, not mandatory**. A workflow can skip runtime checks, but the standard path goes through them.

This guide walks through the eight main tasks you will encounter when using runtime enforcement.

## Table of Contents

- [What Is Runtime Enforcement?](#what-is-runtime-enforcement)
- [1. Create an Implementation Plan](#1-create-an-implementation-plan)
- [2. Choose a Domain](#2-choose-a-domain)
- [3. Run One Phase at a Time](#3-run-one-phase-at-a-time)
- [4. Validate a Phase](#4-validate-a-phase)
- [5. Read Evidence and Phase Closeout](#5-read-evidence-and-phase-closeout)
- [6. Fix a Failed Gate](#6-fix-a-failed-gate)
- [7. Resume from NEXT_PROMPT.md](#7-resume-from-next_promptmd)
- [8. Know When Human Approval Is Required](#8-know-when-human-approval-is-required)
- [Enforcement Levels](#enforcement-levels)
- [Non-Coding Examples](#non-coding-examples)

## What Is Runtime Enforcement?

Runtime enforcement adds validation gates to agent workflows. Each phase of work produces structured artifacts that can be checked before the workflow advances. This catches problems early instead of discovering them after the entire run completes.

If you have not yet completed the [quickstart](../QUICKSTART.md), do that first. This guide assumes you can install ContextSmith and invoke a skill.

**Available now:**

- Validator CLI for checking artifacts
- 6 domain packs (software engineering, writing, research, scheduling, travel/purchase, general fallback)
- Next Prompt Compiler for generating phase handoff prompts
- Runner skeleton for plan status and gate queries
- Pilot integration in the `contextsmith-orchestrator` skill

**Active development:**

- MCP adapter for tool-based validation from any agent
- Harness adapter for hard-blocking enforcement in supported environments
- Full orchestrated runner with automated gate loops

## 1. Create an Implementation Plan

An implementation plan breaks a task into phases, each with bounded scope and explicit validation criteria. ContextSmith can help you create one using the `contextsmith-instruction-engineer` or `contextsmith-prompt-engineer` skill.

**What you do:**
Provide a task description and ask the agent to create a phased plan. The plan should include:

- Phase name and goal
- Allowed and disallowed actions
- Validation commands
- Expected output

**Example prompt:**

```
Create an implementation plan for migrating our AGENTS.md file
to support Qwen3-32B model profiles. Break it into phases with
validation gates.
```

**Expected output:** A `PLAN.md` file with phase definitions, context contracts, and closeout requirements.

## 2. Choose a Domain

Domain packs define what validation gates apply to your workflow. ContextSmith ships with six domain packs:

| Domain | Use When |
| --- | --- |
| `software_engineering` | Coding, testing, refactoring, dependency management |
| `writing_editing` | Drafting, editing, rewriting, tone adjustment |
| `research_summary` | Literature review, fact-checking, source synthesis |
| `scheduling` | Calendar operations, meeting coordination |
| `travel_purchase` | Flight comparison, hotel search, purchase planning |
| `general_fallback` | Any task not matching a specific domain |

**How to choose:**
Most tasks match a single domain. If your task spans multiple domains, pick the one with the most restrictive approval boundaries. When unsure, `general_fallback` provides safe defaults.

**Example -- scanning a domain pack:**

```bash
python -m runtime.cli domain-pack runtime/domain_packs/software_engineering.json
```

Expected output:

```
PASS  runtime/domain_packs/software_engineering.json
```

## 3. Run One Phase at a Time

Runtime enforcement works best when the agent executes one phase, validates, then moves to the next. Use the `contextsmith-orchestrator` skill with `--mode phase` or `--run-mode single-with-state`.

**What you do:**
Point the agent at your task directory and let it execute the current phase.

**Example prompt:**

```
Run the current phase from .agent_work/sprints/my-task/tasks/2026-06-01-my-task/
Use contextsmith-orchestrator with --ralph 2 and --validation available.
```

**What the agent does:**

1. Reads `STATUS.md` to find the current phase
2. Reads the phase definition from `PLAN.md`
3. Executes the phase within declared boundaries
4. Produces artifacts and evidence
5. Updates task state on completion

**Expected output:** Updated task-state files, including `STATUS.md` with the phase marked complete and `NEXT_PROMPT.md` for the next phase.

## 4. Validate a Phase

After a phase completes, validate its artifacts using the runtime validator CLI.

**Subcommands:**

| Command | Validates |
| --- | --- |
| `requirements` | Requirements chain (task requirements traced to phases) |
| `phase-contract` | Phase contract (bounded scope, allowed actions, validation) |
| `evidence` | Evidence ledger (claims backed by concrete evidence) |
| `approval` | Approval record (external actions have human approval) |
| `closeout` | Phase closeout (validation status, completion criteria) |
| `domain-pack` | Domain pack (schema compliance, approval boundary alignment) |

**Example:**

```bash
python -m runtime.cli closeout .agent_work/sprints/my-task/tasks/2026-06-01-my-task/phase_closeout.json
```

**Exit codes:**

- `0` -- validation passed
- `1` -- validation failed (violations listed in output)
- `2` -- usage error or file-read error

**Runner commands:**

```bash

# Check current plan status
python -m runtime.cli plan-status .agent_work/sprints/my-task/tasks/2026-06-01-my-task/

# Determine the next validation gate
python -m runtime.cli next-gate .agent_work/sprints/my-task/tasks/2026-06-01-my-task/
```

## 5. Read Evidence and Phase Closeout

Each completed phase produces an evidence ledger and a phase closeout record. These are JSON artifacts that summarize what happened.

**Evidence ledger** shows:

- Which parameters were applied
- What validation ran and whether it passed
- Self-audit results
- Ralph loop iterations and findings
- Changed files and produced artifacts

**Phase closeout** shows:

- Whether the phase passed or failed
- Validation results for each gate
- Blockers, if any
- Carry-forward notes for the next phase

**Where to find them:**

- `ARTIFACTS.md` -- lists all produced artifacts with paths
- `PHASE_LOG.md` -- compact entry per phase with results
- `STATUS.md` -- current phase and validation state

## 6. Fix a Failed Gate

When validation fails, the CLI outputs the specific violations. Use these to make targeted corrections.

**Example failure:**

```
FAIL  phase_closeout.json
  violation: Rule 3 - validation_status is missing
  violation: Rule 7 - closeout_notes is empty
```

**What to do:**

1. Open the failing artifact
2. Add the missing field or fix the violation
3. Re-run the validator
4. If the fix requires changing the phase output, re-run the phase with a corrected prompt

**Recovery procedure for blocked phases:**

1. Record the blocker in `STATUS.md`
2. Update `PHASE_LOG.md` with blocker details
3. Update `ARTIFACTS.md` with partial findings
4. Update `NEXT_PROMPT.md` with recovery instructions

## 7. Resume from NEXT_PROMPT.md

When a phase completes, it generates a `NEXT_PROMPT.md` for the next phase. This file contains:

- Mission and phase boundary
- Read order for context files
- Allowed and disallowed actions
- Validation commands
- Task-state closeout requirements
- Recovery procedure

**To resume:**

```
Run the prompt in .agent_work/sprints/my-task/tasks/2026-06-01-my-task/NEXT_PROMPT.md
```

The Next Prompt Compiler can also generate these handoff prompts:

```bash
python -m runtime.cli next-prompt .agent_work/sprints/my-task/tasks/2026-06-01-my-task/
```

Use `--dry-run` to preview without writing, or `--compact` for a smaller output suitable for constrained context windows.

## 8. Know When Human Approval Is Required

Runtime enforcement distinguishes between actions the agent can take autonomously and actions that require human approval.

**Always requires approval:**

- External actions (sending emails, making API calls, posting content)
- Irreversible actions (deleting data, force-pushing to Git, purchasing)
- Actions outside the declared phase scope

**Does not require approval:**

- Reading local files and context
- Writing local artifacts (docs, code, task state)
- Running validation commands
- Generating handoff prompts

**How it works:**
The agent creates an `approval_record` artifact before taking an external action. This record includes the action description, risk level, and a request for approval. The workflow pauses until you respond.

**Example approval record:**

```json
{
  "artifact_type": "approval_record",
  "request_id": "email-send-001",
  "action": "Send project status email to team@company.com",
  "risk_level": "medium",
  "status": "pending",
  "boundary": "external_action"
}
```

## Enforcement Levels

Use these labels everywhere. Do not blur them. Orchestrated workflow enforcement is the default — workflows go through it unless explicitly opted out. Deterministic validation is the foundation. Harness hard blocking elevates gates where the harness supports it. Human approval remains explicit for irreversible actions.

| Level | Meaning | Example |
| --- | --- | --- |
| Deterministic validation | A tool checks artifacts and returns pass/fail evidence. Foundation for all enforcement. | CLI validates an evidence ledger. |
| Orchestrated workflow enforcement | Default mode. A runner only advances if validators pass. Opt-out available, not the norm. | Plan runner sends correction prompts until closeout passes. |
| Harness hard blocking | Elevates orchestrated gates to hard blocks where the harness supports it. | opencode permission hook blocks an external action. |
| Human approval | A person must approve an irreversible, costly, private, or high-risk action. | Booking airfare or sending calendar invites. |

The current CLI provides deterministic validation. Orchestrated and hard-blocked enforcement are under active development via the MCP adapter and harness adapter.

## Non-Coding Examples

### Scheduling a meeting

```
Use contextsmith-orchestrator to schedule a team standup for Monday at 10am.
Domain: scheduling. Require approval before sending calendar invites.
```

The agent will:

1. Create a phase contract for the scheduling task
2. Check the `scheduling` domain pack for validation gates
3. Draft the meeting details
4. Create an approval record before sending invites
5. Wait for your confirmation

**Expected output:** An `approval_record` artifact with `status: pending` and a meeting summary. The agent pauses until you approve.

### Comparing travel options

```
Research flight options from NYC to London for July 15-22.
Domain: travel_purchase. Do not book anything.
```

The agent will:

1. Use the `travel_purchase` domain pack
2. Compare options and record evidence for each
3. Produce a comparison with prices, times, and layovers
4. Stop before any booking action (irreversible actions are blocked)

**Expected output:** A comparison table with flight options, an evidence ledger entry for each option, and no booking actions taken.

### Editing a document

```
Rewrite our onboarding doc to be clearer for new hires.
Domain: writing_editing. Ralph loop: 2 iterations.
```

The agent will:

1. Read the existing document
2. Apply the rewrite with the `writing_editing` domain validation
3. Run 2 Ralph loop iterations to improve quality
4. Produce evidence showing what changed and why

**Expected output:** A rewritten document, an evidence ledger entry for the edit, and a Ralph summary noting any improvements from iterations 1 and 2.
