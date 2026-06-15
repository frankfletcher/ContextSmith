# Targeted Context Length

Use the user's stated context budget as a first-class design input. The targeted context length is the context length the artifact is deliberately optimized for. It may be smaller than the model's advertised maximum or even smaller than the runtime cap.

## Control Phrases

Recognize natural phrases such as:

- `targeted context length: 32k`
- `context length: 32k`
- `context window: 32k`
- `usable context: 32k`
- `runtime context: 32k`
- `ctx: 32k`
- `max context: 32768`

Normalize to:

```yaml
metadata:
  targeted_context_length: "32k"
  context_tier: "tight"
```

## Context Tiers

- **tiny**: <=16k
- **tight**: >16k and <=32k
- **moderate**: >32k and <=64k
- **large**: >64k and <=128k
- **very-large**: >128k

If no context length is provided, infer from the selected model profile only as an assumption.

## Design Effects

The targeted context length must materially change the artifact.

### Tiny / Tight Context

Use:

- shorter main instructions
- more but smaller phases
- minimal examples
- stricter output budgets
- aggressive selective reading
- persistent task state by default for complex work
- phase compression and debrief
- tool-use forecasts before phase execution
- subagents only for tightly scoped summarization/validation
- graph/index/search before raw context loading
- references instead of inline long templates
- compact reports unless the user requests detail

Avoid:

- broad three-phase plans for large projects
- full repo or document dumps
- repeated safeguards in multiple sections
- long examples unless absolutely necessary
- verbose educational reports by default

### Moderate Context

Use normal local-model prompting but still avoid full-repo reads. Include examples when they materially improve pattern fidelity. Use staged inspection for multi-file work.

Use:

- shorter main instructions
- more but smaller phases
- persistent task state by default for complex work
- phase compression and debrief
- tool-use forecasts for implementation phases
- references instead of inline long templates

Avoid:

- broad three-phase plans for large projects
- long examples unless absolutely necessary

### Large / Very Large Context

Allow richer templates and examples when useful, but still reserve context for tool output, validation, and recovery. Prefer index/query/verify workflows for large repos.

## Budget Rule

Reserve context before planning phase scope:

- read-only or analysis-heavy phases: reserve 25-35% for tool results, validation output, final answer, error recovery, and active task state
- tool-heavy phases such as coding, editing, migration, validation, or broad discovery: reserve 50-65% for tool output, validation output, failed attempts, recovery, and closeout state

If tool calls are expected to dominate the transcript, size the phase against the remaining usable phase budget, not the headline context target. Typical tool-heavy executable phase budgets are:

| Target | Typical Executable Phase Budget | Planning Consequence |
| ---: | ---: | --- |
| 32k | 12k-16k | Use micro-phases and fresh sessions. |
| 64k | 24k-32k | Split discovery, editing, and validation. |
| 128k | 48k-64k | Larger phases are possible, but tool forecasts still gate execution. |
| 256k | 96k-128k | Broad context is available, but raw tool transcripts still need compaction. |

If the harness injects large system prompts, skill content, or repo instructions, narrow the executable budget further.

If the planned artifact would exceed the usable budget, split into more phases, externalize state, compress references, forecast tool use more narrowly, or stage the work.

## Phase Types

Use phase types to select appropriate context budgets for different work categories:

| Phase Type | Budget | Description |
| --- | --- | --- |
| analysis | 32k | Reading, searching, understanding code or documents. |
| editing | 48k | Targeted file edits, refactoring, test writing. |
| migration | 64k | Cross-file migrations, framework upgrades, bulk changes. |
| ml-heavy | 80k | Data loading, model training, evaluation, experiment tracking. |
| validation | 32k | Running tests, linting, typechecking, reviewing results. |
| planning | 24k | Design, architecture decisions, task breakdown. |

## Phase Granularity Rule

Increase phase granularity when context length is tiny/tight or moderate, the project is large, the task spans multiple subsystems, validation is complex, or interruption is likely.

For a large Windows/macOS-to-Linux port under a 32k target, prefer 10-30 smaller phases with durable handoff notes over a 3-phase plan.

For tool-heavy work under tight or moderate targets, prefer discovery/edit/validation separation and fresh-session phase execution when expected tool output would consume the reserve. For large and very-large targets, keep tool forecasts and compaction triggers because raw tool transcripts can still dominate long sessions.
