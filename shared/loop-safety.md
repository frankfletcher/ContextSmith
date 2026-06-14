# Agentic Loop Safety

Use this reference when a prompt, skill, or repo instruction file will guide a tool-using agent, especially a smaller/local model.

## Core Loop Rules

- Do not execute identical consecutive tool calls.
- If the same command, patch, file write, or edit fails twice, stop repeating it.
- Before retrying, change at least one of: command, arguments, target file, working directory, input data, validation method, or strategy.
- Do not brainstorm repeatedly. After at most three viable options, choose one and act.
- Do not rewrite the plan more than once per phase unless new evidence changes the task.
- After an edit, verify that the file actually changed. Do not repeat no-op edits.
- Keep working notes phase-local and brief.

## Recent Action Check

Before running a tool, compare the action to the last three tool calls. If the same or equivalent action already failed, change strategy before trying again.

For persistent task state, record recent failures in `STATUS.md` or `PHASE_LOG.md`:

```markdown
## Recent Failed Actions
- `npm test`: failed because dependency install is incomplete.
- `npm install`: failed because network access is unavailable.
Next strategy: inspect package scripts and run static validation.
```

## Retry Budget

Default retry budget:

- Maximum retries per exact failing action: 1.
- Maximum related attempts per strategy: 2.
- Maximum total recovery attempts before asking for help: 3.

After the retry budget is exhausted, stop and request human input.

## Recovery Menu

After a failure, choose one recovery type:

- **Correct**: fix an obvious typo, path, flag, missing directory, malformed JSON, or malformed input.
- **Narrow**: reduce scope to isolate the failing part.
- **Inspect**: gather more evidence before acting.
- **Substitute**: use a different tool, command, or method.
- **Escalate**: ask for human input.

Do not choose `Correct` twice in a row for the same error.

## Escalation Strings

Use explicit stop strings when needed:

- `BREAK_LOOP_AWAITING_HUMAN_INPUT`
- `BLOCKED_MISSING_CONTEXT`
- `BLOCKED_TOOL_UNAVAILABLE`
- `BLOCKED_PERMISSION_REQUIRED`
- `BLOCKED_VALIDATION_UNAVAILABLE`
- `BLOCKED_GIT_STATE_REQUIRES_HUMAN_INPUT`

## Compact AGENTS.md Block

```markdown
## Agentic Loop Safety

For tool-using local/smaller models:

1. Do not execute identical consecutive tool calls.
2. If the same command, patch, or edit fails twice, stop repeating it.
3. Before retrying, change the command, arguments, target, working directory, input, or strategy.
4. After a tool failure, inspect the error and make at most one targeted correction.
5. If no safe alternative exists, stop with `BREAK_LOOP_AWAITING_HUMAN_INPUT`.
6. Do not brainstorm repeatedly. After at most 3 options, choose one and act.
7. Do not rewrite the plan more than once per phase unless new evidence changes the task.
8. After an edit, verify that the file changed. Do not repeat no-op edits.
9. Keep working notes phase-local and brief.
10. Focus on the next atomic action: inspect, edit, validate, report, or ask.
```
