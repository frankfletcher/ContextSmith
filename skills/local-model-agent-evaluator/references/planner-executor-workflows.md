# Planner / Executor Workflows

Use this reference when a user can use stronger models for planning and smaller/local models for implementation.

## Core Principle

Strong models can write the plan. Smaller models can execute it — if the plan is atomic enough.

## Recommended Workflow

1. Use a stronger model or ContextSmith deep path to create the implementation plan.
2. Audit the plan for small-model executability.
3. Split the plan into atomic phases sized for `targeted_context_length`.
4. Save durable task state under `.agent-work/`.
5. Execute one phase per local-model session when context is tight.
6. End each phase with a debrief and `NEXT_PROMPT.md`.
7. Run post-phase code review and test-quality audit when relevant.
8. Use a stronger model again for high-risk reviews if desired.

## Planner Profile

Use stronger/planner-capable models for:

- requirements clarification
- architecture planning
- implementation plan audit
- risk analysis
- test strategy
- final review

## Executor Profile

Use smaller/local models for:

- phase execution
- local edits
- targeted refactors
- running validation
- updating docs
- carrying out narrowly specified checklists

## Control Parameters

Supported patterns:

```bash
--planner-profile frontier-cloud
--executor-profile qwen36
--target-capability small-local
--context-length 32k
```

Do not assume the executor can reconstruct the whole plan. Put the carryout instructions in task state and phase prompts.
