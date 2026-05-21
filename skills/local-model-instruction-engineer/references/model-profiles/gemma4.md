# Gemma 4 Profile

Use for Gemma 4 variants such as 31B, 26B A4B, E4B, and E2B.

- Use explicit instructions and strict output contracts.
- Do not request exposed chain-of-thought.
- Treat thinking controls as runtime/chat-template guidance, not guaranteed skill behavior.
- Do not store or replay thinking-channel content in task state, conversation history, subagent reports, or resume prompts.
- Store only final answers, decisions, evidence, and validation results.
- For multimodal tasks, follow the runtime's expected media/text ordering.
- Keep context-risk controls active even with large nominal context windows.
