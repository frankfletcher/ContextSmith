# Reference Optimization

References are part of a skill contract when linked by SKILL.md or used by the workflow.

## Inventory

Classify each reference:

- behavioral: required instructions
- template: reusable output pattern
- model profile: model-specific guidance
- example: behavior demonstration
- background/archive: not needed at runtime

## Edit Rules

- Optimize behavioral references when they contain agent-followed instructions.
- Preserve exact commands, schemas, APIs, paths, examples, and policies.
- Move bulky templates/examples/failure tables out of SKILL.md when helpful.
- Remove duplication between SKILL.md and references.
- Do not rewrite archived/background references unless requested.
- Report every modified reference.

## Validation

- Every linked reference exists.
- SKILL.md says when to read each reference.
- No reference contains exposed chain-of-thought instructions.
- No reference contradicts selected model profiles.
- Modified references are listed in the audit.
