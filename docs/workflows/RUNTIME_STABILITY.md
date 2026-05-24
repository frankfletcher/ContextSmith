# Runtime Stability

ContextSmith improves prompts, skills, plans, and instruction files. It cannot fix every runtime problem.

Long agentic coding runs can fail because of the model prompt, but they can also fail because of the runtime stack: context length, KV cache precision, speculative decoding, reasoning settings, sampling, harness behavior, or tool-call parsing.

## Principle

> Speed optimizations are optional. Stability is the baseline.

If a setup is stable without an optimization and unstable with it, treat the optimization as experimental until proven otherwise.

## Diagnose one layer at a time

When adjusting parameters for stability, treat the process like an experiment. We suggest changing one setting at a time when possible, recording the result, and keeping a known-stable baseline.

Useful layers to test:

1. targeted context length
2. actual server context size
3. reasoning or thinking budget
4. thinking preservation across turns
5. speculative decoding or draft model
6. KV cache precision/compression
7. sampling parameters
8. harness loop controls

## Example experiment log

```markdown
| Run | Ctx | Reasoning | Preserve thinking | Spec decoding | KV K/V | Sampling | Loop? | Notes |
|---|---:|---|---|---|---|---|---|---|
| baseline | 64k | off | false | off | q4/q4 | baseline | no | known stable |
| A | 128k | on 2048 | true | dflash | turbo/tcq | baseline | yes | loop after long tool run |
| B | 64k | on 2048 | true | dflash | q4/q4 | baseline | ? | tests DFlash with conservative KV |
| C | 64k | off | false | off | q4/q4 | repeat 1.05 | ? | tests sampling tweak only |
```

## Context length

A 128k or 256k model may be more reliable when the agent targets 32k or 64k.

Use `--context-length` to tell ContextSmith what to optimize for:

```bash
--context-length 32k
```

This should change the generated plan: smaller phases, stricter output budgets, and stronger task state.

## Reasoning and thinking preservation

Runtime reasoning controls are deployment guidance, not guaranteed skill behavior.

For tool-heavy coding runs, strict structured output, or final artifact generation, test lower reasoning budgets or non-reasoning modes if loops occur.

Do not store or replay reasoning/thinking content in task state, subagent reports, or resume prompts unless the runtime explicitly requires it and it is safe.

## Speculative decoding

Speculative decoding can speed up generation, but it adds another moving part.

If the model is stable without speculative decoding and loops with it, treat speculation as a suspect. Test with speculation disabled, or with a less aggressive speculative configuration, before changing every other setting.

## KV cache precision

Aggressive KV cache compression can trade precision for context and VRAM. If long-context loops appear, test whether a more conservative KV cache improves stability, even if it requires lowering context size.

On constrained GPUs, you often choose between:

- larger context + aggressive cache compression
- smaller context + more conservative cache precision

For long autonomous coding, stable effective context is usually more valuable than maximum theoretical context.

## Harness loop controls

Even a stable model can loop if the harness repeats failed commands or keeps feeding back bad state.

Use AGENTS.md or harness instructions for:

- no identical consecutive tool calls
- retry budget
- no-op edit detection
- same-output detection
- strategy change after repeated failure
- escalation strings such as `BREAK_LOOP_AWAITING_HUMAN_INPUT`

## What to add to ContextSmith outputs

For runtime-sensitive work, include a short note:

```markdown
## Runtime Assumptions

- Targeted context length: 32k
- Runtime settings are recommendations only unless the harness can set them.
- Prefer stability over speed for long autonomous coding runs.
- If loops occur, record a one-variable-at-a-time experiment log before changing many settings.
```
