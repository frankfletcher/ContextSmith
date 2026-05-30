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

For tool-heavy work under tight or moderate targets (`targeted_context_length <= 64k`):

- Forecast expected tool calls before execution.
- Reserve 50-65% of context for tool output, validation, recovery, and closeout.
- Prefer one phase per fresh session.
- Split discovery, editing, and validation into separate phases when tool output would dominate the transcript.
- Stop and compact when actual tool use exceeds the forecast instead of expanding the phase.

For large and very-large targets (`targeted_context_length > 64k`), still forecast tool use and compact raw output. Larger windows permit larger phases, but they do not make raw search results, validation logs, or repeated recovery attempts good long-term memory.

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
3. current `PLAN.md` phase section
4. `CONTEXT.md` carry-forward notes and tool ledger
5. `DECISIONS.md`
6. `CHECKLIST.md`
7. the current phase's `NEXT_PROMPT.md`

Do not reload old iterations, raw logs, full `PHASE_LOG.md`, full `ARTIFACTS.md`, broad search output, or full chat history unless blocked.

## Compaction Trigger

Compact or start a new session when:

- actual tool calls exceed the phase forecast by 50%
- tool output dominates the context
- validation output is large enough that only summarized failures remain useful
- new discovery is required after edits have started
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
