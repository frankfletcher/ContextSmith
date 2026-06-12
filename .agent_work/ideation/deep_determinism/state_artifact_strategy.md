# State Artifacts and Agent Handoffs

This note defines the artifact set that lets one agent hand work to another with no hidden conversational context.

The principle is simple: if a future agent needs the information, it should be in a file.

## Why This Matters

Agents working different phases should not depend on memory, chat history, or unstated assumptions.
The next agent should be able to open a small, predictable set of markdown files and continue safely.

## Artifact Groups

### 1. Control artifacts

These tell the system what to do next.

- `TASK.md` - objective, scope, constraints
- `PLAN.md` - phase plan and task checklist
- `STATUS.md` - current phase and current blocker
- `NEXT_PROMPT.md` - the next bounded prompt for the next run

These are the minimum navigation files.

### 2. Context artifacts

These explain the work already known.

- `CONTEXT.md` - facts, file map, assumptions, constraints
- `DECISIONS.md` - durable decisions and why they were made
- `REFERENCE_MAP.md` - optional map of source docs and key links

These should be short and factual.

### 3. Execution artifacts

These capture what the current phase produced.

- `PHASE_LOG.md` - compact timeline of what happened in the phase
- `ARTIFACTS.md` - files changed and commands run
- `EVIDENCE.md` - outputs, excerpts, or proof used to validate work
- `CHECKLIST.md` - per-task or per-phase checklist items with status

These help the next agent understand what is done and what remains.

### 4. Review artifacts

These communicate outcomes to the user and to later review agents.

- `AUDIT_REPORT.md` - findings, severity, evidence, and fixes
- `EDUCATIONAL_REPORT.md` - what changed, why it matters, how to use it
- `SUMMARY.md` - short plain-language summary of the completed work
- `REVIEW_NOTES.md` - optional notes for follow-up review

These should be readable without the rest of the session.

## Recommended Minimal Set Per Phase

For most phases, the minimum useful set is:

1. `STATUS.md`
2. `PLAN.md`
3. `NEXT_PROMPT.md`
4. `CHECKLIST.md`
5. `PHASE_LOG.md`
6. `CONTEXT.md`
7. `ARTIFACTS.md`

When the phase includes review or assessment, add:

- `AUDIT_REPORT.md`
- `EVIDENCE.md`

When the phase is meant to teach or summarize for the user, add:

- `EDUCATIONAL_REPORT.md`
- `SUMMARY.md`

Other artifacts (`DECISIONS.md`, `TASK.md`, `REVIEW_NOTES.md`) are optional and added only when the workflow requires them.

## Per-Phase Checklists

Each phase should have its own checklist so the next agent can see exactly what is complete.

Preferred shape:

```md
# Checklist

- [x] Load task state
- [x] Review current phase contract
- [ ] Validate outputs
- [ ] Write next prompt
```

Checklist rules:

- one item per concrete action
- no vague items like "finish work"
- checkboxes should reflect reality, not intent
- completed items stay visible for later phases

## User-Facing Reports

The system should produce markdown files that communicate value to the user without marketing language.

### Audit report

Use this when the work is a review or evaluation.

Example:

```md
# Audit Report

## Findings
- High: validation step missing in phase 3
- Medium: checklist does not mention user-facing summary

## Evidence
- `PLAN.md` line 14
- validation log output

## Recommended Fixes
- add explicit schema validation step
- write `SUMMARY.md` after closeout
```

### Educational report

Use this when the user should understand what was changed and how it works.

Example:

```md
# Educational Report

## What Was Done
- added a harness adapter layer
- added conditional OpenCode references

## Why It Matters
- keeps the core portable
- lets OpenCode runs use native agent definitions

## How To Use It
- set the harness flag when running on OpenCode
- keep harness-specific files out of universal skills unless needed
```

### Summary file

Use this for concise closeout communication.

Example:

```md
# Summary

Completed the workflow-state and artifact model updates.
Validated the new docs and linked them into the deep-determinism index.
Next step: define the schema for `CHECKLIST.md` and `AUDIT_REPORT.md`.
```

## How Agents Should Use Artifacts

### First agent

The first agent should write the starting state and planned checklist.

### Middle agent

The middle agent should read the checklist, context, and decisions before touching files.

### Review agent

The review agent should rely on the audit report, evidence, and phase log.

### Final agent

The final agent should write the summary and next prompt for the next session.

## Communication Contract Between Agents

The handoff contract should answer these questions:

- What was the objective?
- What has already been completed?
- What remains open?
- What files changed?
- What evidence supports the result?
- What should the next agent do first?

If the answer is not in the files, the next agent should treat it as unknown.

## Suggested File Order

When resuming work, read files in this order:

1. `TASK.md`
2. `STATUS.md`
3. `PLAN.md`
4. `CONTEXT.md`
5. `DECISIONS.md`
6. `CHECKLIST.md`
7. `PHASE_LOG.md`
8. `ARTIFACTS.md`
9. `AUDIT_REPORT.md` or `EDUCATIONAL_REPORT.md`
10. `NEXT_PROMPT.md`

That order gives the agent the shortest path from goal to action.

## Related Notes

- `system_components.md` for the full component map
- `orchestrator_and_harness.md` for state-on-disk behavior
- `agent_start_and_communication.md` for startup and message flow
- `workflow_config_sketch.md` for required workflow fields

---

## Required Sections Per Artifact

Each artifact file must contain specific sections. The orchestrator uses these to parse state. Agents use these to understand context.

### TASK.md

```markdown
# Task: <objective>

## Objective
One-line summary of what this task achieves.

## Scope
- In scope: <list of things this task covers>
- Out of scope: <list of things this task explicitly does NOT cover>

## Constraints
- <list of constraints: time, resources, dependencies>
```

### PLAN.md

```markdown
# Plan

## Phases
List of phases with checkbox status. Each phase item is a link to its state definition.

- [x] Phase 1: Load task state (init)
- [ ] Phase 2: Implement change (execute)
- [ ] Phase 3: Review output (audit)
- [ ] Phase 4: Validate (validate)
- [ ] Phase 5: Close (closeout)

## Dependencies
- <phase name>: <depends on phase or artifact>

## Validation Gates
- <gate name>: <condition that must pass>
```

### STATUS.md

```markdown
# Status

## Current Phase
<phase-identifier>

## Current State
<state-machine-state-name>

## Progress
- Phase: <N> of <M>
- Checklist: <X>/<Y> complete
- Retries remaining: <N>

## Next Action
<what should happen next>

## Blocked By
<none or description of blocking condition>
```

### CONTEXT.md

```markdown
# Context

## File Map
- <path>: <description>

## Assumptions
- <assumption>

## Known Constraints
- <constraint>

## Reference Links
- <link>

## Harness
<harness-name>
```

### DECISIONS.md

```markdown
# Decisions

## <Decision Title>
- Decision: <what was decided>
- Reason: <why>
- Date: <YYYY-MM-DD>
- Alternatives considered: <what was rejected>
```

### CHECKLIST.md

```markdown
# Checklist

- [ ] <concrete action item>
- [x] <completed action item>

Rules:
- Each item must be a single concrete action
- No vague items like "finish work"
- Checkboxes reflect current reality
- Completed items stay visible
```

### ARTIFACTS.md

```markdown
# Artifacts

## Files Changed
- <path>: <description of change>

## Commands Run
- `$ <command>` → <exit code>: <output summary>
```

### PHASE_LOG.md

```markdown
# Phase Log

## Phase <name>
Date: <YYYY-MM-DDTHH:MM:SS>
State: <state-machine-state>
Action: <what was done>
Result: <pass/fail/blocked>
Duration: <seconds>
Artifacts: <list>

## Phase <name>
...
```

### EVIDENCE.md

```markdown
# Evidence

## <Evidence Category>
- Source: <file path or command>
- Excerpt: <relevant content>
- Conclusion: <what this proves>
```

### NEXT_PROMPT.md

```markdown
# Next Prompt

You are continuing a workflow on <project>.

## Current Status
- Phase: <phase-name>
- State: <state-name>
- Completed: <list of completed items>

## Your Task
<specific bounded instruction for the next agent>

## Input Files
- <file path>: <what to read from it>

## Output Requirements
- <file path>: <what to write to it>

## Constraints
- <limit: permissions, step cap, etc.>

## Context (from previous phases)
- <key facts the agent needs>
```

### AUDIT_REPORT.md

```markdown
# Audit Report

## Summary
<one-line conclusion>

## Findings
- <Severity>: <description>
  - Evidence: <where>
  - Fix: <how>

## Overall Verdict
pass / fail / conditional-pass
```

### EDUCATIONAL_REPORT.md

```markdown
# Educational Report

## What Changed
- <change description>

## Why It Matters
- <impact on user or system>

## How to Use
- <instructions>
```

### SUMMARY.md

```markdown
# Summary

Completed <task-name>.

## Key Outcomes
- <outcome>

## Next Steps
- <what comes next>
```

---

## Field-Level Requirements

### Required Fields Per Phase

Every phase must produce these fields in STATUS.md before the orchestrator advances:

| Field | Source | Required By | Validation |
|-------|--------|-------------|------------|
| Current Phase | STATUS.md | Every phase | Must match workflow config phase_order entry |
| Current State | STATUS.md | Every phase | Must be a valid canonical state |
| Next Action | STATUS.md | Every phase | Must be non-empty |
| Checklist | CHECKLIST.md | execute, fix, audit, ralph_revise | At least 1 item |
| Phase Log Entry | PHASE_LOG.md | Every phase | Must exist |
| Artifacts List | ARTIFACTS.md | execute, fix, ralph_revise | At least 1 entry |

### File-Level Validation Rules

Each artifact has a minimum content requirement. **Required** artifacts must exist for the orchestrator to advance. **Optional** artifacts are validated only if they exist.

| File | Required | Must Have Content | Must Have Required Sections |
|------|----------|-------------------|---------------------------|
| STATUS.md | **Yes (always)** | Yes | `## Current Phase`, `## Current State`, `## Next Action` |
| PLAN.md | **Yes (after plan)** | Yes | `## Phases`, `## Validation Gates` |
| NEXT_PROMPT.md | **Yes (except terminal)** | Yes | `## Your Task`, `## Output Requirements`, `## Constraints` |
| CHECKLIST.md | **Yes (after plan)** | Yes | `## Checklist` with `- [ ]` or `- [x]` items |
| PHASE_LOG.md | **Yes (always)** | At least 1 entry | `## Phase <name>` with Date, Action, Result |
| CONTEXT.md | **Yes (after init)** | Yes | `## File Map`, `## Assumptions`, `## Constraints` |
| ARTIFACTS.md | **Yes (after execute/fix)** | If content | `## Files Changed` or `## Commands Run` |
| AUDIT_REPORT.md | After audit gate | Yes | `## Summary`, `## Findings`, `## Overall Verdict` |
| EVIDENCE.md | Optional | If exists | `## <category>` with Source, Excerpt, Conclusion |
| SUMMARY.md | After closeout | Yes | `## Key Outcomes`, `## Next Steps` |
| EDUCATIONAL_REPORT.md | Optional | If exists | `## What Changed`, `## Why It Matters`, `## How to Use` |
| DECISIONS.md | Optional | If exists | `## <title>` with Decision, Reason, Date |
| TASK.md | Optional | If exists | `## Objective`, `## Scope`, `## Constraints` |

### Validation Pseudocode

```python
def validate_artifact(file_path: Path, required_sections: list[str]) -> list[str]:
    """
    Check that an artifact file exists and contains all required sections.
    Returns list of validation error messages (empty = valid).
    """
    errors = []

    if not file_path.exists():
        errors.append(f"Missing required file: {file_path.name}")
        return errors

    if file_path.stat().st_size == 0:
        errors.append(f"File is empty: {file_path.name}")
        return errors

    content = file_path.read_text(encoding="utf-8")
    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section '{section}' in {file_path.name}")

    return errors
```

---

## Agent Reading Order

When an agent resumes work or starts a new phase, it should read files in this exact order to minimize context usage while gaining maximum understanding:

```
1. STATUS.md          → What phase am I in? What state? Am I blocked?
2. NEXT_PROMPT.md     → What exactly should I do right now?
3. CONTEXT.md         → What project is this? What are the constraints?
4. PLAN.md            → What is the overall plan? What phase comes after mine?
5. CHECKLIST.md       → What items are done? What still needs doing?
6. PHASE_LOG.md       → What happened in previous phases? What was tried?
7. DECISIONS.md       → What decisions were made? What was rejected?
8. ARTIFACTS.md       → What files have been changed? What commands were run?
9. EVIDENCE.md        → What proof supports the current state? (if exists)
10. AUDIT_REPORT.md   → What did the last audit find? (if exists)
```

The first 5 files give the agent enough context to act. Files 6-10 are needed only when the agent must understand history or validate prior work.

---

## File Change Protocol

When the orchestrator updates artifacts, it follows these rules:

1. **STATUS.md** is rewritten entirely (not appended) on each phase transition.
2. **PHASE_LOG.md** is appended to (new section added at end).
3. **CHECKLIST.md** is rewritten entirely (items may be marked complete).
4. **NEXT_PROMPT.md** is rewritten entirely (new prompt for next phase).
5. **ARTIFACTS.md** is rewritten entirely (cumulative or phase-specific - configurable).
6. **All other files** are written once (at creation) and not modified by the orchestrator.
7. Agents may modify any file as part of their task, but the orchestrator re-validates after.

### Write Atomicity

To prevent partial writes during crashes:

```python
def atomic_write(file_path: Path, content: str) -> None:
    """Write content to file atomically using write-to-temp-then-rename."""
    temp_path = file_path.with_suffix(file_path.suffix + ".tmp")
    temp_path.write_text(content, encoding="utf-8")
    temp_path.rename(file_path)  # atomic on POSIX; close enough on Windows
```

The orchestrator uses this for all artifact writes. On recovery, it ignores `.tmp` files.
