# Generic Local/Open-Weight Model Profile

Use when the target model is unknown or when the artifact should work across local/open-weight models.

- Use explicit, imperative instructions.
- Use strict output contracts.
- Do not request exposed chain-of-thought.
- Request concise rationale, assumptions, tests, validation, or semantic diff instead.
- Use few-shot examples only when pattern fidelity matters.
- Avoid model-specific runtime claims.
- Treat runtime settings as recommendations unless controllable by the harness.
- Apply context-risk, persistent-state, and subagent protocols when task complexity warrants them.
