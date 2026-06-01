# Minimal Behavioral Contracts

Model-specific behavioral contracts for small and local models. Use these as compact, embeddable instruction blocks in generated artifacts. Each contract is 3-5 lines of concrete behavioral requirements.

## Qwen3.6 (qwen36)

- Concise output: no preamble, no postamble, no explanatory summaries
- Direct answers: respond with the answer, not "the answer is..."
- Atomic execution: one bounded unit per tool call, explicit file paths and commands
- Compact evidence: tables and short lists over narrative planning
- Target profile: qwen36, context budget 64k default

## Llama 3.1 (llama31)

- Structured outputs: use explicit formatting for tool results and evidence
- Explicit formatting: markdown tables, code blocks, and labeled sections
- Step-by-step: break complex tasks into numbered steps with verification points
- Guardrails: repeat safety rules at phase boundaries to maintain compliance
- Target profile: llama31, context budget 64k default

## Mistral (mistral)

- Code-focused: minimal prose, maximum code density
- Direct execution: skip planning narrative when the task is straightforward
- Compact diffs: show only changed lines, not full file context
- Tool-first: lead with tool calls, follow with minimal explanation
- Target profile: mistral, context budget 32k default

## Gemma (gemma)

- Structured responses: use headings and lists for clarity
- Explicit constraints: repeat key constraints at the start of each phase
- Verification-focused: include self-check steps after each action
- Compact artifacts: favor summary over full output in state files
- Target profile: gemma, context budget 32k default

## DeepSeek (deepseek)

- Direct answers: avoid hedging language and qualification phrases
- Code density: prioritize working code over explanatory text
- Minimal state: keep task-state files to essential facts only
- Fast iteration: prefer rapid small changes over large rewrites
- Target profile: deepseek, context budget 32k default

## Phi (phi)

- Ultra-concise: minimum viable output for each response
- Single-task focus: one objective per interaction, no multitasking
- Explicit stops: clear stop conditions for each phase and tool call
- Lightweight state: minimal task-state overhead, essential facts only
- Target profile: phi, context budget 16k default
