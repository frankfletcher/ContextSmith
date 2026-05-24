# Runtime Stability for Local Agentic Coding

Prompt and instruction engineering cannot fix every loop. Long-running local agent workflows also depend on runtime settings, context policy, speculative decoding, KV cache precision, sampling, and harness behavior.

## Core Principle

Speed optimizations are optional. Stability is the baseline.

## Diagnostic Ladder

Change one layer at a time and record results.

1. **Harness loop controls**
   - Add loop safety, retry budgets, no-op detection, and escalation strings.
2. **Targeted context length**
   - Operate at 32k/64k even if the server allows 128k/256k.
3. **Reasoning/thinking preservation**
   - For tool-heavy loops, test lower reasoning budget or reasoning off when runtime supports it.
4. **Speculative decoding**
   - If stable without speculation but looping with speculation, treat speculation as suspect.
   - Test lower speculation/cross-context settings or disable speculation for long autonomous runs.
5. **KV cache precision**
   - Aggressive KV compression trades precision for VRAM/context.
   - If loops occur in long context, A/B test more conservative KV when hardware allows.
6. **Sampling**
   - Change sampling conservatively. Do not change many knobs at once.

## Experiment Log Template

```markdown
| Run | Context | Targeted ctx | Reasoning | Preserve thinking | KV cache | Spec decoding | Sampling | Loop? | Notes |
|---|---:|---:|---|---|---|---|---|---|---|
| baseline | 128k | 64k | on 4096 | true | turbo/turbo | dflash | current | yes | |
| A | 128k | 64k | on 2048 | true | turbo/turbo | dflash reduced | same | ? | |
| B | 64k | 32k | off | false | q4/q4 | off | same | ? | |
```

## ContextSmith Guidance

- Keep a known-stable baseline profile.
- Use speed profiles only after A/B testing.
- Prefer stable moderate context plus task-state over unstable maximum context.
- Record runtime assumptions in reports, not in model-facing AGENTS.md unless relevant.
