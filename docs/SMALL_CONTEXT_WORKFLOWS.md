# Small-Context Workflows

A model's advertised context window is not the same thing as the context you should design for.

A local model may technically support 128k or 256k tokens, but your actual run may be constrained by VRAM, KV cache precision, context shift, harness overhead, tool output, or stability. ContextSmith uses `targeted_context_length` to design for the context you actually want the model to rely on.

## Why small context needs a different workflow

When context is tight, the agent cannot keep the whole project, full chat history, logs, plans, and tool outputs in working memory. If the plan assumes it can, the model will drift, loop, or repeat work.

The solution is not just a shorter prompt. It is a different workflow:

- smaller phases
- fewer active files per phase
- explicit stop conditions
- project-local task state
- phase debriefs
- do-not-carry-forward notes
- selective file reading
- compact validation reports

## Context tiers

### Tiny: 16k or less

Use micro-phases. Keep prompts short. Avoid examples unless essential. Rely heavily on task-state files and narrow file reads.

### Tight: 32k

Use compact artifacts, more phases, short examples, strict output budgets, and phase-local context. This is a good target for many local coding-agent workflows.

### Moderate: 64k

Use normal local-model prompts, but still avoid dumping entire repos or long histories into context.

### Large: 128k

Allow richer context, but still reserve budget for tool outputs and validation.

### Very large: above 128k

Large context helps, but it is still not a substitute for structure. Use indexes, graph queries, and phase memory when the project is complex.

## Phase sizing rule

For `targeted_context_length <= 32k`, prefer 8-15 small phases for a large project rather than 3 broad phases.

A weak plan:

```text
1. Analyze the app.
2. Port it to Linux.
3. Test and polish.
```

A better tight-context plan:

```text
1. Inventory platform-specific assumptions.
2. Identify build and packaging dependencies.
3. Establish a minimal Linux build path.
4. Fix filesystem/path assumptions.
5. Fix process/shell invocation assumptions.
6. Fix UI/windowing/platform integration.
7. Fix installer/packaging behavior.
8. Add Linux-specific tests.
9. Run narrow validation.
10. Run broader validation.
11. Document remaining platform gaps.
```

Each phase should have:

- goal
- likely files/directories
- tasks
- outputs/artifacts
- validation
- stop condition
- handoff notes

## One phase per session

For tight context and long tasks, consider a fresh session for each phase.

At the start of a phase, load only:

- `TASK.md`
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`
- `CONTEXT.md`
- `CHECKLIST.md`
- current phase files

Do not reload the entire old chat unless required.

## Phase debrief

At the end of each phase, write a compact debrief:

```markdown
## Phase Debrief

- Completed:
- Evidence:
- Blockers:
- Decisions:
- Carry forward:
- Do not carry forward:
- Next phase:
```

The `Do not carry forward` section is important. It prevents the next session from repeating dead ends or obsolete assumptions.

## Persistent task state

For project work, use:

```text
<project>/.agent-work/sprints/<sprint-or-subproject>/tasks/<YYYY-MM-DD-short-slug>/
```

Recommended files:

- `TASK.md`
- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `CONTEXT.md`
- `CHECKLIST.md`
- `ARTIFACTS.md`
- `PHASE_LOG.md`
- `NEXT_PROMPT.md`
- `iterations/`
- `reports/`

Keep these files short. Store summaries, paths, decisions, and validation results. Do not dump raw logs, full files, or long transcripts into task state.

## Compacting

Compact or start a new phase/session when:

- tool output is dominating the chat
- the agent starts repeating prior context
- the plan has changed materially
- a phase is complete
- validation results are stable enough to summarize
- the next step only needs a subset of files

A good compaction includes:

- current objective
- completed work
- files changed
- decisions
- blockers
- validation results
- next atomic action
- do-not-carry-forward notes

## Graph/index support

If Graphify or another index exists, use:

```text
index → query → verify → edit
```

Do not recursively read the whole repo when a graph/search/index can identify relevant files first.
