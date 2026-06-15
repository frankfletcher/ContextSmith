# Task-State Execution

Use this reference when running a `.agent_work/.../tasks/<task>/` folder or a `NEXT_PROMPT.md` handoff.

## Read Order

1. `STATUS.md` for current phase and blocker state.
2. `NEXT_PROMPT.md` for fresh-session handoff.
3. `PLAN.md` for the current phase only.
4. `CONTEXT.md` for file map, skip rules, validation commands, and constraints.
5. `DECISIONS.md`, `CHECKLIST.md`, `ARTIFACTS.md`, and `PHASE_LOG.md` only as needed.

Do not load every task-state file in full if the context budget is tight. Read targeted sections first.

## Phase Modes

| Mode | Behavior |
| ------ | ---------- |
| `phase` | Execute only the current phase, then stop after state update. |
| `phased-run` | Execute phases sequentially until complete, blocked, validation fails, context risk appears, or approval is needed. |
| `dry-run` | Validate readiness and report the next action. |
| `audit-only` | Audit phase executability without making changes. |

## Pre-Phase Checks

- Current phase is named in `STATUS.md`.
- Current phase exists in `PLAN.md`.
- Skip rules and validation commands are known.
- Git/file safety constraints from repo instructions are compatible with the phase.
- User approval exists for commits, external actions, destructive changes, or other approval-gated steps.

## Phase Closeout

Update state with compact facts:

- phase completed or blocked
- files changed or artifacts produced
- commands run and result summary
- validation result
- self-audit and Ralph summary when required
- decisions made
- residual risks
- next phase and next action

Refresh `NEXT_PROMPT.md` so a new session can continue without chat history.

## State Hygiene

Do not store:

- raw transcripts
- hidden reasoning
- full command logs
- full source files
- large pasted tool outputs

Store paths, summaries, commands, validation results, durable decisions, blockers, and next actions.

## Blockers

Stop and report a blocker when:

- current phase cannot be determined
- plan and status disagree materially
- validation fails and the next fix is outside the current phase
- required approval is absent
- skip rules conflict with phase actions
- context budget is too tight to continue safely
