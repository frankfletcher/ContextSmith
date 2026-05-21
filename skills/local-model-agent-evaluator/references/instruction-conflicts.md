# Instruction Conflict Detector

Before finalizing prompts, skills, or instruction files, scan for conflicting or competing instructions.

## Common Conflicts

- “Ask before editing” vs “edit automatically.”
- “Return JSON only” vs “explain your reasoning.”
- “Do not browse” vs “search online.”
- “Do not request chain-of-thought” vs “think step by step.”
- “Do not modify Git” vs “rebase the branch.”
- “Stage only” vs “apply changes immediately.”
- “Use existing style” vs “replace with new framework.”

## Resolution Order

1. Current explicit user request.
2. Safety and permission boundaries.
3. Current phase objective.
4. Repo/skill instructions.
5. General style preferences.
6. Optional improvements.

## Report Format

```markdown
## Instruction Conflicts
- Conflict:
- Location:
- Resolution:
```
