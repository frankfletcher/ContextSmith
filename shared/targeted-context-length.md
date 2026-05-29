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
- references instead of inline long templates

Avoid:

- broad three-phase plans for large projects
- long examples unless absolutely necessary

### Large / Very Large Context

Allow richer templates and examples when useful, but still reserve context for tool output, validation, and recovery. Prefer index/query/verify workflows for large repos.

## Budget Rule

Reserve 25-35% of the stated context length for:

- tool results
- validation output
- final answer
- error recovery
- active task state

If the planned artifact would exceed the usable budget, split into more phases, externalize state, compress references, or stage the work.

## Phase Granularity Rule

Increase phase granularity when context length is tiny/tight or moderate, the project is large, the task spans multiple subsystems, validation is complex, or interruption is likely.

For a large Windows/macOS-to-Linux port under a 32k target, prefer 10-30 smaller phases with durable handoff notes over a 3-phase plan.
