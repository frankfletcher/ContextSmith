# Phased Planning for Limited Context

Large tasks need more than a short plan. The plan must support context churn, crashes, and resumption.

## Phase Count Heuristic

- 1-3 phases: short, one-artifact, low-risk tasks.
- 4-7 phases: moderate multi-file tasks.
- 8-12 phases: large ports, migrations, refactors, batch conversions, repo-level work.
- 12+ phases: split into milestones/sprints.

## Required Phase Fields

Each phase should include:

```markdown
## Phase N — Name
Goal:
Inputs:
Files/directories likely involved:
Tasks:
Outputs/artifacts:
Validation checks:
Stop condition:
Handoff notes:
```

## Memory Integration

For long plans, create task-state files from `persistent-task-state.md`. Update `STATUS.md`, `PHASE_LOG.md`, `ARTIFACTS.md`, and `NEXT_PROMPT.md` after each phase.

## Anti-Pattern

Do not compress a large complex project into three vague phases such as “analyze, implement, test.” That creates context churn and weak handoffs.
