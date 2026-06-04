# Run a Task-State Handoff: Step-by-Step

Use this workflow when you want to resume a multi-phase ContextSmith task from a `NEXT_PROMPT.md` handoff file. The `contextsmith-run` skill reads the handoff, executes the next phase, and updates task state.

## Table of Contents

- [When to Use This Workflow](#when-to-use-this-workflow)
- [Inputs](#inputs)
- [Step 1: Locate Your Task State](#step-1-locate-your-task-state)
- [Step 2: Read NEXT_PROMPT.md](#step-2-read-next_promptmd)
- [Step 3: Invoke contextsmith-run](#step-3-invoke-contextsmith-run)
- [Step 4: Validate the Phase Output](#step-4-validate-the-phase-output)
- [Step 5: Review Updated Task State](#step-5-review-updated-task-state)
- [Expected Artifacts](#expected-artifacts)
- [Common Failure Modes](#common-failure-modes)

## When to Use This Workflow

Use this workflow when:
- Resuming a multi-phase task after an agent session ends
- Handing off work to another agent or session
- Continuing after an interruption or context limit

If you need to create the initial plan instead of resuming one, see [Create a Plan](CREATE_A_PLAN.md). For a copy-paste example with expected output, see [Example 1: Run a Task-State Phase](../examples/EXAMPLES_LIBRARY.md).

## Inputs

- Task-state directory path (e.g., `.agent_work/sprints/my-project/tasks/2026-06-01-my-task/`)
- `NEXT_PROMPT.md` file inside the task directory
- Optional controls: `--ralph N`, `--validation level`, `--domain name`

## Step 1: Locate Your Task State

Task state lives under `.agent_work/sprints/<sprint>/tasks/<date-slug>/`. Find the most recent task directory:

```bash
ls .agent_work/sprints/<sprint>/tasks/
```

## Step 2: Read NEXT_PROMPT.md

The handoff file contains the next phase's objective, steps, constraints, and validation commands. Read it to understand what the agent should do next.

## Step 3: Invoke contextsmith-run

Point the `contextsmith-run` skill at the handoff file with any controls:

```
Run the prompt in this file:
.agent_work/sprints/my-project/tasks/2026-06-01-my-task/NEXT_PROMPT.md
--ralph 2 --validation available
```

The agent will:
1. Read `STATUS.md` for the current phase
2. Read `PLAN.md` for phase requirements
3. Read `CONTEXT.md` for constraints and known facts
4. Execute the phase per `NEXT_PROMPT.md` instructions
5. Run validation commands
6. Run self-audit and Ralph loop iterations
7. Update task-state files

## Step 4: Validate the Phase Output

Check the reported validation results. For project-level checks:

```bash
python scripts/validate_skills.py
python scripts/token_budget.py --strict
```

## Step 5: Review Updated Task State

After the phase completes, verify the updated state files:

- `STATUS.md` — reflects completed phase and next action
- `PHASE_LOG.md` — compact entry for the completed phase
- `ARTIFACTS.md` — new artifacts tracked
- `NEXT_PROMPT.md` — handoff for the following phase

If everything looks correct, you can resume with the next `NEXT_PROMPT.md`.

## Expected Artifacts

| Artifact | Purpose |
|----------|---------|
| `STATUS.md` | Current phase, next action, blockers |
| `PHASE_LOG.md` | Compact phase history |
| `ARTIFACTS.md` | Produced artifact tracking |
| `NEXT_PROMPT.md` | Handoff prompt for next phase |

## Common Failure Modes

| Problem | Fix |
|---------|-----|
| Stale task state | Re-read `STATUS.md` and `CONTEXT.md` to confirm the current phase |
| Missing `NEXT_PROMPT.md` | The previous phase may not have completed closeout. Check `PHASE_LOG.md` for the blocker |
| Context overflow during long runs | Use `--compact` flag with the Next Prompt Compiler to generate smaller handoffs |
| Phase mismatch — wrong phase executed | Verify `STATUS.md` current phase matches `NEXT_PROMPT.md` objective |
