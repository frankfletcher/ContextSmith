# Model Profiles and Capability Tiers

ContextSmith began as a way to make agent instructions work better for local/smaller models. That remains the center of gravity.

But the underlying idea is broader:

> ContextSmith is model-aware agent instruction engineering. It started with small local models, where instruction quality matters most, but the same discipline improves larger-model agent workflows too.

## Profiles vs capability tiers

Use a model profile when you know the target family:

```bash
--target-profile qwen36
--target-profile gemma4
--target-profile llama3
--target-profile generic-local
```

Use a capability tier when you know the role but not the exact model:

```bash
--target-capability small-local
--target-capability frontier-cloud
--target-capability reasoning-specialized
```

## Common profiles

### `qwen36`

Use for Qwen3.6-style local workflows. Emphasize literal instructions, compact artifacts under tight context, no exposed chain-of-thought, context-aware phases, and runtime settings as recommendations unless the harness can control them.

### `gemma4`

Use for Gemma 4-style workflows. Keep instructions explicit, do not request exposed chain-of-thought, avoid replaying thinking content into history/task state, and account for multimodal input ordering when relevant.

### `llama3`

Use for Llama 3.x-style local instruct models. Follow the runtime chat template, use strict output contracts, and validate structured outputs externally when possible.

### `generic-local`

Use when the exact model is unknown. Avoid model-specific runtime claims. Prefer explicit instructions, compact phases, and validation gates.

## Capability tiers

### `small-local`

Use for smaller/local models or tight context. Generate compact artifacts, more phases, fewer examples, stronger task state, and more explicit stop conditions.

### `mid-local`

Use for local models with moderate reliability and context. Keep atomicity and validation, but allow slightly richer examples and explanations.

### `large-local`

Use for larger local/open-weight models. Allow richer analysis, but still manage context and tool loops.

### `frontier-cloud`

Use for stronger cloud models. Good for planning, auditing, architecture, and test strategy. Do not remove safety and validation just because the model is stronger.

### `reasoning-specialized`

Use for hard planning, debugging, architecture tradeoffs, and implementation-plan audits. Still do not ask for exposed chain-of-thought by default; request concise rationale, criteria, tests, and verification.

### `coding-specialized`

Use for code-focused executor or reviewer models. Prefer exact files, narrow tasks, tests, and phase-local review.

### `multimodal`

Use when images, screenshots, PDFs, UI, charts, or audio/video are part of the task. Include modality-specific source handling and evidence anchors.

## Planner/executor split

For large tasks, consider:

```bash
--planner-profile frontier-cloud --executor-profile qwen36
```

The planner creates or audits the plan. The executor carries out one atomic phase at a time.

This works only when the plan is specific enough for the executor to follow without reconstructing the whole project context.
