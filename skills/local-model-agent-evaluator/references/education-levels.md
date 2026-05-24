# Education Level and Artifact Verbosity

Use this reference when the user wants to learn from the agent's work, not just receive the final artifact.

## Core Distinction

Artifact verbosity and educational verbosity are different.

- `artifact-verbosity`: how verbose the generated prompt, skill, AGENTS.md, plan, or instruction artifact should be.
- `education-level`: how much the agent explains changes to the user.

When `targeted_context_length` is tight, keep model-facing artifacts compact even if education level is high. Put teaching detail in separate reports.

## Education Levels

- `none`: minimal explanation; changes, validation, risks.
- `brief`: short rationale for important changes.
- `guided`: explain key decisions and tradeoffs.
- `deep`: walk through major changes, alternatives, and reasoning.
- `teaching`: teach concepts, mistakes to avoid, examples, and practice questions.

## Artifact Verbosity

- `compact`: short, atomic, reference-driven.
- `normal`: balanced detail.
- `detailed`: richer inline guidance when context budget permits.

## Example

```bash
--context-length 32k --artifact-verbosity compact --education-level deep
```

Meaning: generate a compact artifact for the small model, but provide a separate deep explanation for the user.
