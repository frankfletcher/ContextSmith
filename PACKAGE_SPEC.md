# Package Spec

## Name

Local Model Agent Engineering Skills

## Version

v1.2

## Thesis

Local and smaller open-weight models do best when instructions are explicit, staged, validated, context-aware, loop-safe, and durable across interruptions. Artifacts must also be sized and structured for the user's targeted context length, not the model card maximum.

## Core Skills

- `local-model-prompt-engineer`
- `local-model-skill-engineer`
- `local-model-skill-migrator`
- `local-model-instruction-engineer`
- `local-model-agent-evaluator`

## Shared Principles

- Preserve the user's real objective.
- Optimize for the selected model profile and targeted context length.
- Ask only when blocked or when the answer materially changes the output.
- Detect upstream skill/tool artifacts and reject unsupported requirements.
- Resolve conflicts using instruction precedence.
- Prefer atomic instructions, checklists, and validation gates.
- Avoid exposed chain-of-thought instructions.
- Use context management, persistent state, subagents, and phase debriefs when complexity warrants them.
- Avoid duplicated safeguards and token bloat.
- Use review-gate mode for destructive, external, or batch actions.

## Packaging

Use Option C: canonical shared references plus copied per-skill references for standalone installation.
