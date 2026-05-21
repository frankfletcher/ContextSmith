# Llama 3.x Profile

Use for Llama 3.x and compatible instruct-tuned local models.

- Follow the runtime's chat template exactly.
- Prefer concise system instructions plus concrete user instructions.
- Use examples for unusual output formats.
- Use explicit schemas and “return only” constraints for structured output.
- Do not request exposed chain-of-thought by default.
- Use concise rationale, tests, or verification summaries instead.
- Validate structured output externally when possible.
