# Qwen3.6 Profile

Use for Qwen3.6 27B and nearby Qwen3.6 local models.

- Prefer literal, non-conversational instructions with clear task boundaries.
- Use Markdown or XML-style labeled sections.
- Do not request exposed chain-of-thought in any runtime mode.
- Treat thinking/no-thinking as runtime guidance, not guaranteed skill behavior.
- Do not rely on Qwen3 `/think` or `/no_think` text switches unless the runtime explicitly supports them.
- For structured output, prefer schema, examples, validation checks, and direct final outputs.
- For long-context work, use staged inspection, persistent state, and compact evidence notes.
