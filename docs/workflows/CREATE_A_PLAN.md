# Create a Plan: Step-by-Step

Use this workflow when you need a phased implementation plan with validation gates, context contracts, and task-state tracking. ContextSmith helps you create plans that small models can execute safely.

## Table of Contents

- [When to Use This Workflow](#when-to-use-this-workflow)
- [Inputs](#inputs)
- [Step 1: Define Your Task](#step-1-define-your-task)
- [Step 2: Invoke the Skill](#step-2-invoke-the-skill)
- [Step 3: Review the Plan](#step-3-review-the-plan)
- [Step 4: Validate](#step-4-validate)
- [Expected Artifacts](#expected-artifacts)
- [Common Failure Modes](#common-failure-modes)

## When to Use This Workflow

Use this workflow when you have a multi-step task and want a structured plan before execution. It works for coding tasks, documentation work, research, and other structured projects.

If you need to audit an existing plan instead of creating one, see [Implementation Plan Audit](IMPLEMENTATION_PLAN_AUDIT.md).

## Inputs

- A task description (what you want to accomplish)
- Scope boundaries (what is in and out of scope)
- Any constraints (dependencies, tools, approval requirements)

## Step 1: Define Your Task

Write a concise task description. Include the goal, scope, and any known constraints.

**Example:**

```
Migrate our AGENTS.md file to support Qwen3-32B model profiles.
In scope: model profile sections, context budget rules, tool call patterns.
Out of scope: skill migration, prompt rewriting.
```

## Step 2: Invoke the Skill

Use the `contextsmith-instruction-engineer` or `contextsmith-prompt-engineer` skill to generate the plan.

**Example prompt:**

```
Create an implementation plan for migrating our AGENTS.md file
to support Qwen3-32B model profiles. Break it into phases with
validation gates. Store task state under
.agent_work/sprints/my-project/tasks/2026-06-01-agents-md/
```

The agent will create:

- `TASK.md` — objective, scope, constraints
- `PLAN.md` — phased implementation plan with validation gates
- `STATUS.md` — current phase and next action
- `CONTEXT.md` — known facts and file map
- `CHECKLIST.md` — quality and safety checklist
- `ARTIFACTS.md` — artifact tracking
- `PHASE_LOG.md` — phase history
- `NEXT_PROMPT.md` — handoff prompt for the first phase

## Step 3: Review the Plan

Before execution, check:

1. **Phase boundaries** — each phase has bounded scope and clear stop conditions
2. **Validation gates** — each phase specifies how to verify completion
3. **Context contracts** — tool-heavy phases include budget and compaction rules
4. **Recovery procedure** — blocked phases have a documented recovery path
5. **Approval boundaries** — external actions require explicit human approval

If the plan needs adjustment, ask the agent to refine specific phases before proceeding.

## Step 4: Validate

If the plan includes runtime enforcement artifacts, validate them:

```bash
python scripts/validate_skills.py
python scripts/token_budget.py --strict
```

For runtime enforcement plans, you can also validate individual artifacts:

```bash
python -m runtime.cli phase-contract path/to/phase_contract.json
python -m runtime.cli requirements path/to/requirements_chain.json
```

To generate a handoff prompt for the first phase, use the Next Prompt Compiler:

```bash
python -m runtime.cli next-prompt .agent_work/sprints/my-project/tasks/2026-06-01-my-task/
```

Use `--dry-run` to preview, or `--compact` for smaller output.

## Expected Artifacts

| Artifact | Purpose |
| --- | --- |
| `TASK.md` | Objective, scope, constraints |
| `PLAN.md` | Phases, validation gates, context contracts |
| `STATUS.md` | Current phase, next action, blockers |
| `CONTEXT.md` | File map, known facts, constraints |
| `CHECKLIST.md` | Quality and safety checklist |
| `ARTIFACTS.md` | Produced artifact tracking |
| `PHASE_LOG.md` | Compact phase history |
| `NEXT_PROMPT.md` | Handoff prompt for next phase |

## Common Failure Modes

| Problem | Fix |
| --- | --- |
| Plan phases are too broad | Ask the agent to split into smaller phases with explicit stop conditions |
| Missing validation commands | Add concrete validation commands to each phase definition |
| No context contracts for tool-heavy phases | Add `context_contract` YAML blocks with budget and compaction rules |
| Plan exceeds model context | Use the Next Prompt Compiler with `--compact` to generate smaller handoffs |
| Task state files missing | Re-run the planning step and verify all 8 state files are created |
