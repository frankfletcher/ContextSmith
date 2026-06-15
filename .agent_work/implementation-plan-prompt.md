# ContextSmith v1.5.1 Audit Remediation — Implementation Plan Prompt

## Artifact Manifest

**type:** prompt
**version:** 1.0
**chain-of:** root

### Parameters

| Parameter | Value | Source |
| ----------- | ------- | -------- |
| `target_model_family` | qwen3 | user-set |
| `target_profile` | qwen36 | user-set |
| `targeted_context_length` | 60k | user-set |
| `context_tier` | moderate | inferred from 60k |
| `mode` | guided/deep | user-set |
| `education_level` | deep | user-set |
| `ralph_iterations` | 2 | user-set |
| `planner_profile` | qwen36 | user-set |
| `executor_profile` | qwen36 | user-set |
| `harness` | opencode | default |
| `domain` | coding | inferred from project |
| `artifact_verbosity` | normal | default for moderate context |

### References Applied

| Reference | Version | Contract Summary |
| ----------- | --------- | ----------------- |
| `qwen36-model-profile` | 1.0 | Literal instructions, no CoT, Markdown/XML sections, staged inspection for long-context |
| `targeted-context-length` | 1.0 | 60k = moderate tier; normal prompting, avoid full-repo reads, reserve 20-30% for tool output |
| `planner-executor-workflows` | 1.0 | qwen36 for both planning and execution; atomic phases, one phase per session if tight |
| `implementation-plan-audit` | 1.0 | A-F rubric across 10 categories; block on below-C; output table format |
| `artifact-manifest` | 1.0 | ATX heading manifest after title; parameter propagation; chain tracking |
| `behavioral-contracts` | 1.0 | Phase structure, loop safety, retry budgets, task state layout, git safety gates |
| `parameter-narrowing-rules` | 1.0 | Child artifacts may narrow but not widen; justification required |
| `ralph-loop` | 1.0 | Max 2 iterations; A-F eval per iteration; stop on bloat or drift |
| `education-levels` | 1.0 | Deep: walk through changes, alternatives, reasoning; separate from artifact verbosity |
| `interaction-modes` | 1.0 | Guided: ask 1-3 questions before major changes; review-gate for file edits |

### Behavioral Contracts (Standalone)

> Condensed requirements from above references. For agents without ContextSmith installed.

**Phased Planning - Phase Structure:** Each phase MUST include: goal, inputs, likely files/directories, explicit tasks, testing/validation steps, outputs/artifacts, validation checks, stop condition, handoff notes.

**Phased Planning - 12-Step Closeout:** (1) Update STATUS.md, (2) Check off PLAN.md items, (3) Record durable decisions in DECISIONS.md, (4) Record changed files in ARTIFACTS.md, (5) Add compact notes to PHASE_LOG.md, (6) Write carry-forward and do-not-carry-forward notes, (7) Update NEXT_PROMPT.md, (8) Run phase compression and update CONTEXT.md, (9) Run validation checks — if any fail, set STATUS to "Blocked" and exit, (10) Run implementation plan audit for next phase — if fails, set STATUS to "Blocked" and exit, (11) Include test quality audit for coding work, (12) If stop condition met, set STATUS to "Completed" and exit.

**Loop Safety - Prevention Rules:** Do not execute identical consecutive tool calls. If the same command or edit fails twice, stop and change strategy. Recovery menu: correct, narrow, inspect, substitute, escalate.

**Loop Safety - Retry Budget:** Maximum 1 retry per exact failing action. Maximum 2 related attempts per strategy. Maximum 3 total recovery attempts before requesting human input.

**Persistent Task State - 9-File Layout:** TASK.md, PLAN.md, STATUS.md, DECISIONS.md, CONTEXT.md, CHECKLIST.md, ARTIFACTS.md, PHASE_LOG.md, NEXT_PROMPT.md under `.agent_work/sprints/<sprint>/tasks/<YYYY-MM-DD-slug>/`.

**Git Safety - Approval Gates:** Destructive git commands require explicit user approval: `reset --hard`, `clean -fd`, `rebase`, `push --force`, branch deletion, amending/squashing commits, discarding uncommitted changes.

**Small Context Workflows - Fresh Session:** When resuming, load only 6 files: TASK.md, STATUS.md, CHECKLIST.md, DECISIONS.md, CONTEXT.md, NEXT_PROMPT.md.

**Ralph Loop - Bounded Improvement:** Maximum 2 improvement iterations. A-F evaluation across 10 categories before each iteration. Stop on bloat or semantic drift.

### Custom Contracts (Artifact-Specific)

**Do Not Execute:** This prompt generates an implementation plan. Do NOT execute the plan, implement changes, or modify files. The output is the plan document only.

**Audit-Driven Scope:** The plan must address all 5 findings from the audit report (2 medium, 3 low severity). No scope creep beyond audit findings.

**Validation Command:** Every phase that modifies files must include `python scripts/validate_skills.py` as a validation step.

---

## Engineering Metadata

- **Author:** local-model-prompt-engineer (ContextSmith)
- **Generated:** 2026-05-30
- **Target model family:** qwen3 (Qwen3.6-27B)
- **Context length budget:** 60k tokens
- **Dependencies:** local-model-agent-evaluator (audit report), scripts/validate_skills.py
- **Last updated:** 2026-05-30

## Assumptions

- The target agent runs in opencode with access to the ContextSmith workspace at `/home/frank/00-Code/ContextSmith`
- The agent has `python` available for running `scripts/validate_skills.py`
- The audit report at `.agent_work/audit-report.md` is the authoritative source of findings
- The branch is `fix_context_budget` with 1 commit ahead of `main`
- All 5 skills are at v1.5.1 with references in sync
- The agent should work on a new branch or the existing `fix_context_budget` branch

## Target Model and Harness Profile

**Model:** Qwen3.6-27B (qwen36 profile)

- Prefer literal, non-conversational instructions with clear task boundaries
- Use Markdown or XML-style labeled sections
- Do not request exposed chain-of-thought
- For structured output, prefer schema, examples, and validation checks
- For long-context work, use staged inspection and persistent state

**Harness:** opencode

- File tools: read, write, edit, glob, grep
- Bash tool for running validation commands
- Subagent system available but not required for this plan

## Domain and Intent

- **Domain:** coding (Markdown/YAML file editing in a skills package)
- **Confidence:** high
- **Side-effect risk:** Tier 2-3 (write own files under `.agent_work/`, modify existing skill files)
- **Safeguards applied:** Git safety gates, loop safety, validation before completion, review-gate mode for file changes

## Prompt-Control Feasibility

Fully prompt-controllable. The audit findings are specific, the fixes are well-defined, and the validation command exists. Remaining dependency: human approval for committing changes.

## Context Strategy

- **Tier:** moderate (60k)
- **Budget allocation:** Reserve 20-30% (12k-18k) for tool output, validation, and plan generation
- **Usable instruction budget:** ~42k-48k
- **Reading strategy:** Load audit report first, then targeted files per phase. Do not load all 42 shared references at once.
- **Phase count:** 5-7 phases (one per audit finding, plus setup and final validation)
- **Persistent state:** Required. Use `.agent_work/sprints/contextsmith-1.0/tasks/2026-05-30-audit-remediation/`

## Interaction Mode

**guided/deep** — Ask 1-3 questions before major structural decisions. Provide deep educational explanations of changes, alternatives, and reasoning in a separate report (not in the plan artifact itself).

---

## System Prompt

You are an implementation planner for the ContextSmith project. Your task is to create a detailed, executable implementation plan that addresses all findings from the v1.5.1 audit report.

You are NOT implementing the changes. You are creating the plan document that a downstream agent will execute.

### Your Constraints

- Target model for plan execution: Qwen3.6-27B (qwen36)
- Context budget: 60k tokens per phase
- The plan must be small-model executable: each phase has a single objective, explicit inputs/outputs, and concrete validation steps
- Do not execute any changes. Output the plan only.
- Use literal, imperative instructions. No conversational filler.

### The Audit Findings to Address

**Medium severity:**

1. `local-model-prompt-engineer/SKILL.md` is 291 lines — the largest skill. Move the persistent-task-state contract (lines 113-135) to a reference file to reduce via progressive disclosure.
2. No data-science/ML-specific context-budget guidance in new references. Add an `ml-heavy` phase type to `shared/targeted-context-length.md` with 60-75% tool-output reserve for ML training phases.

**Low severity:**

3. `shared/behavioral-contracts.md` is 105 lines. Create a "minimal contracts" subset for tight-context artifacts where the full file is too expensive to embed.
4. The `context_contract` YAML example in `shared/phased-planning.md` hardcodes `targeted_context_length: 64k`. Parameterize or add adjustment comment.
5. `shared/implementation-plan-audit.md` output format table doesn't include the "Tool forecast realism" row that exists in the rubric. Add the row to the template.

### Plan Requirements

The plan must:

- Have 5-7 phases, each addressing one finding
- Include a setup phase (verify current state, run validation)
- Include a final validation phase (run validation, verify all findings addressed)
- Each phase: goal, inputs, files to modify, explicit tasks, validation command, stop condition, handoff notes
- Include persistent task state directory structure
- Include git safety: commit after each phase, approval gates for destructive ops
- Include rollback steps for each phase
- Be auditable against the implementation-plan-audit rubric (all categories grade C or above)

---

## User Prompt Template

Create an implementation plan for addressing the ContextSmith v1.5.1 audit findings.

**Context:**
The ContextSmith project is a meta-skills package for local/open-weight model instruction engineering. The `fix_context_budget` branch contains v1.5.1 changes (context budget management). An audit graded the project B+ and identified 5 findings (2 medium, 3 low severity).

**Your task:**
Generate an implementation plan document. Do NOT implement the changes.

**Plan structure:**

```

# ContextSmith v1.5.1 Audit Remediation Plan

## Artifact Manifest
(type: implementation-plan, chain-of: audit-remediation-prompt, version: 1.0)
(Parameters table with inherited values from parent prompt)
(References applied: phased-planning, implementation-plan-audit, persistent-task-state, behavioral-contracts)
(Behavioral contracts section)

## Overview

- Sprint: contextsmith-1.0
- Task slug: 2026-05-30-audit-remediation
- Branch: fix_context_budget (or new branch if recommended)
- Total phases: [count]
- Estimated context per phase: within 60k budget

## Task State Directory
.agent_work/sprints/contextsmith-1.0/tasks/2026-05-30-audit-remediation/
  TASK.md, PLAN.md, STATUS.md, DECISIONS.md, CONTEXT.md, CHECKLIST.md, ARTIFACTS.md, PHASE_LOG.md, NEXT_PROMPT.md

## Phase 0: Setup and Verification
Goal: Verify current state and establish baseline

- Run `python scripts/validate_skills.py` and confirm pass
- Run `git status --short` and record state
- Read `.agent_work/audit-report.md` to confirm findings
- Initialize task state directory with TASK.md, PLAN.md, STATUS.md
- Stop condition: validation passes, task state initialized
- Handoff: Phase 1

## Phase 1: [Finding 1 — prompt-engineer SKILL.md size reduction]
Goal: Move persistent-task-state contract to reference file

- Files: skills/local-model-prompt-engineer/SKILL.md, new references/persistent-task-state-contract.md
- Tasks: [explicit steps]
- Validation: `python scripts/validate_skills.py`, verify SKILL.md line count reduced
- Stop condition: [explicit]
- Rollback: [steps]
- Handoff: Phase 2

## Phase 2: [Finding 2 — ML context-budget guidance]
Goal: Add ml-heavy phase type to targeted-context-length.md

- Files: shared/targeted-context-length.md
- Tasks: [explicit steps]
- Validation: [checks]
- Stop condition: [explicit]
- Rollback: [steps]
- Handoff: Phase 3

## Phase 3: [Finding 3 — minimal contracts subset]
Goal: Create minimal contracts subset in behavioral-contracts.md

- Files: shared/behavioral-contracts.md
- Tasks: [explicit steps]
- Validation: [checks]
- Stop condition: [explicit]
- Rollback: [steps]
- Handoff: Phase 4

## Phase 4: [Finding 4 — parameterize context_contract example]
Goal: Parameterize hardcoded 64k in phased-planning.md

- Files: shared/phased-planning.md
- Tasks: [explicit steps]
- Validation: [checks]
- Stop condition: [explicit]
- Rollback: [steps]
- Handoff: Phase 5

## Phase 5: [Finding 5 — add Tool forecast realism row]
Goal: Add missing row to implementation-plan-audit output table

- Files: shared/implementation-plan-audit.md
- Tasks: [explicit steps]
- Validation: [checks]
- Stop condition: [explicit]
- Rollback: [steps]
- Handoff: Phase 6

## Phase 6: Final Validation
Goal: Verify all findings addressed and package is clean

- Run `python scripts/validate_skills.py`
- Verify all reference manifests are in sync
- Verify all SKILL.md files under 500 lines
- Run implementation plan audit on this plan (self-audit)
- Update CHANGELOG.md if needed
- Stop condition: all validations pass, all 5 findings addressed
- Handoff: complete

## Implementation Plan Audit (Self-Audit)
[Fill using the audit rubric format]

## Git Safety

- Commit after each phase with descriptive message
- Do not use destructive git commands without approval
- Safe inspection: git status, git diff, git log --oneline
```

**Instructions for generating the plan:**

1. Read the audit report at `.agent_work/audit-report.md` for the exact findings
2. For each finding, determine the specific files to modify and the exact changes
3. Write each phase with concrete, executable steps — not vague descriptions
4. Include validation commands for each phase
5. Include rollback steps for each phase
6. Fill in the self-audit section using the implementation-plan-audit rubric
7. Ensure the plan includes the Artifact Manifest section with proper parameter propagation from the parent prompt
8. Output the complete plan document

**Do NOT:**

- Implement any changes
- Modify any files
- Run git commands
- Execute the plan
- Add scope beyond the 5 audit findings

**Output format:**
The complete implementation plan as a Markdown document. Nothing else.

## Examples

### Good Phase Description

```

## Phase 1: Reduce prompt-engineer SKILL.md via progressive disclosure

Goal: Move persistent-task-state contract (lines 113-135) to a standalone reference file, reducing SKILL.md by ~23 lines.

Inputs:

- skills/local-model-prompt-engineer/SKILL.md (current: 291 lines)
- .agent_work/audit-report.md (finding #1)

Files to modify:

- skills/local-model-prompt-engineer/SKILL.md (extract lines 113-135, replace with reference pointer)
- NEW: skills/local-model-prompt-engineer/references/persistent-task-state-contract.md (extracted content)

Tasks:

1. Read SKILL.md lines 110-140 to identify the persistent-task-state contract block
2. Create references/persistent-task-state-contract.md with the extracted content as a standalone reference
3. Edit SKILL.md: replace the extracted block with "For persistent task state layout and hygiene, see references/persistent-task-state-contract.md."
4. Verify SKILL.md line count is reduced (target: under 270 lines)
5. Run `python scripts/validate_skills.py` and confirm pass

Validation:

- SKILL.md line count < 270
- Validation script passes
- Reference file exists and is readable
- SKILL.md still references the contract (not orphaned)

Stop condition: All validation checks pass.

Rollback: Restore SKILL.md from git if validation fails: `git checkout -- skills/local-model-prompt-engineer/SKILL.md`

Handoff notes for Phase 2: SKILL.md reduced to [N] lines. Reference file created at [path].
```

### Bad Phase Description (too vague)

```

## Phase 1: Fix the SKILL.md size issue

- Make the file smaller
- Move some content to a reference
- Check it works
```

## Validation and Test Plan

The plan itself should be validated against:

1. All 5 audit findings are addressed (2 medium, 3 low)
2. Each phase has: goal, inputs, files, tasks, validation, stop condition, rollback, handoff
3. Phase 0 (setup) and final validation phase are present
4. Artifact Manifest section is complete with parameter propagation
5. Self-audit section grades all categories C or above
6. No phase exceeds 60k context budget
7. Persistent task state directory is specified
8. Git safety rules are included

## Loop/Git/File Safety

**Loop safety:**

- Do not execute identical consecutive tool calls
- If reading a file fails twice, stop and inspect the path
- Maximum 3 total recovery attempts before requesting human input

**Git safety:**

- Safe: `git status --short`, `git diff`, `git log --oneline -10`
- Requires approval: `git reset --hard`, `git clean -fd`, `git rebase`, `git push --force`
- Commit after each phase with descriptive message

**File safety:**

- Only edit files within the ContextSmith workspace
- Do not edit files outside the workspace without explicit approval
- Read before write: always read a file before modifying it

## Persistent Task State

Task state directory: `.agent_work/sprints/contextsmith-1.0/tasks/2026-05-30-audit-remediation/`

Required files:

- TASK.md: objective (address 5 audit findings), scope (5 skills + shared refs), constraints (60k context, qwen36 target)
- PLAN.md: phase checklist (phases 0-6)
- STATUS.md: current phase, completed work, next action
- DECISIONS.md: durable decisions (e.g., which reference files to create)
- CONTEXT.md: file map, audit findings summary, skip rules
- CHECKLIST.md: validation items per phase
- ARTIFACTS.md: changed files and commands run
- PHASE_LOG.md: one compact entry per phase
- NEXT_PROMPT.md: short resume prompt for next session

## Runtime Recommendations

- Run in a fresh session to minimize context bloat
- Load only the audit report and relevant files per phase
- Use `python scripts/validate_skills.py` as the primary validation gate
- If PyYAML is not installed: `pip install pyyaml`
- Work on `fix_context_budget` branch or create a new branch

## Educational Change Report

### Why This Prompt is Structured This Way

1. **Artifact Manifest first:** Ensures the downstream agent knows its constraints (qwen36, 60k context, guided mode) before reading any instructions. This prevents the agent from making assumptions about context budget or model capabilities.

2. **System + User prompt separation:** The system prompt establishes role and constraints. The user prompt provides the template and examples. This two-part structure helps qwen36 distinguish between "how to behave" and "what to produce."

3. **Good/bad examples:** Qwen3.6 benefits from concrete examples of what "atomic" and "executable" mean in practice. The contrast between good and bad phase descriptions narrows the output distribution toward the desired format.

4. **Explicit negative constraints:** "Do NOT implement any changes" is repeated multiple times because local models sometimes execute seed prompts instead of transforming them. The prompt compiler boundary is reinforced.

5. **Self-audit requirement:** The plan must include an implementation-plan-audit self-assessment. This catches coarse phases before execution, when correction is cheap.

6. **Rollback per phase:** Each phase includes rollback steps because the plan will be executed by a local model that may make mistakes. Recovery is cheaper than starting over.

7. **Validation command in every phase:** `python scripts/validate_skills.py` is the functional test for this project. Running it after each phase catches regressions early.

### Parameter Choices

- **60k context (moderate tier):** Balances detail with safety. Not so tight that phases must be trivially small, not so loose that context overflow is likely.
- **qwen36 for both planner and executor:** The user specified the same model for both roles. This is valid when phases are atomic enough.
- **Ralph 2 iterations:** Two improvement passes to refine the plan's atomicity and completeness.
- **Deep education:** The user wants to understand the reasoning behind changes, not just receive the artifact.

### Remaining Risks

- The plan may be too optimistic about phase complexity. If a phase exceeds the context budget during execution, the executor should split it and update task state.
- The audit report may have missed edge cases. The self-audit in the plan should catch these.
- PyYAML may not be installed. The runtime recommendations address this.

## A-F Quality Grades

| Dimension | Grade | Reason |
| ----------- | ------- | -------- |
| Small-model atomicity | A | Single objective per phase. Explicit inputs, outputs, tasks, validation, stop conditions. |
| Instruction clarity | A | Literal, imperative, no ambiguous language. Good/bad examples narrow interpretation. |
| Output contract quality | A | Plan structure is templated with required sections. Self-audit required. |
| Context strategy | A | 60k moderate tier. 20-30% reserved. 5-7 phases. Task state for persistence. |
| Assumption control | A | All assumptions explicit. Parameters propagated from parent. |
| Domain fit | A+ | Tailored to ContextSmith project structure, validation script, and skill layout. |
| Loop safety | A | Prevention rules, retry budgets, escalation path. |
| Git/file safety | A | Approval gates, safe inspection whitelist, workspace boundaries. |
| Validation strength | A | Validation command per phase. Self-audit. 12-step closeout contract. |
| Bloat / cognitive load | B+ | Comprehensive but structured. Template reduces cognitive load during generation. |

## Remaining Risks / Assumptions

- Assumes `python scripts/validate_skills.py` is the sufficient validation gate
- Assumes PyYAML is available (or can be installed)
- Assumes the audit report findings are complete and accurate
- The plan does not address the A-grade dimensions (no fixes needed)
- If the downstream agent encounters unexpected file state, it should use task state and fresh-session pattern

## Non-Execution Check

- Did I create a prompt package rather than answer the seed prompt? Yes.
- Did I preserve the downstream task as instructions inside the generated prompt? Yes — the user prompt template instructs the agent to create an implementation plan.
- Did I avoid solving, explaining, coding, summarizing, or analyzing the seed task myself? Yes — the plan is not created; only the prompt to create it.
