# Small-Context Workflows

Use this reference when `targeted_context_length` is tight or when the user wants small/local models to execute long-running work.

## Core Principle

A bigger context window is not a strategy. Optimize for the context that is reliable in the user's runtime.

## Small-Context Rules

For `targeted_context_length <= 32k`:

- Prefer one phase per session for large tasks.
- Start each phase by reading task-state files, not the full prior chat.
- Load only files needed for the current phase.
- Use Graphify/search/index queries before raw recursive reads when available.
- Keep the active file set small, usually 3-7 files.
- Use short phase prompts with explicit stop conditions.
- Put educational detail in reports, not in the model-facing artifact.
- End every phase with phase compression/debrief.
- Save `NEXT_PROMPT.md` so the next session can resume without the full chat.

For `targeted_context_length <= 16k`:

- Use micro-phases.
- One phase should generally modify one component or one narrow path.
- Avoid multi-objective phases.
- Use compact summaries and external task state aggressively.

## Fresh-Session Pattern

For long work, prefer a new session per phase when context grows noisy.

Start the new session with:

1. `TASK.md`
2. `STATUS.md`
3. `CHECKLIST.md`
4. `DECISIONS.md`
5. `CONTEXT.md`
6. the current phase's `NEXT_PROMPT.md`

Do not reload old iterations, raw logs, or full chat history unless needed.

## Compaction Trigger

Compact or start a new session when:

- tool output dominates the context
- the model repeats old mistakes
- phase goals drift
- more than one failed strategy has accumulated
- the session has crossed the intended phase boundary

## Phase Closeout Requirement

Each phase should end with:

- Completed
- Evidence
- Blockers
- Decisions
- Carry forward
- Do not carry forward
- Next phase
