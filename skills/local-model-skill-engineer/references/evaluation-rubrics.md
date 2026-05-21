# Evaluation Rubrics

Use these rubrics when auditing prompts, skills, AGENTS.md files, or generated instruction artifacts for local/open-weight models.

## A-F Scale

- **A**: Excellent. Clear, atomic, testable, model-appropriate, low drift risk.
- **B**: Good. Minor gaps remain, but safe and usable.
- **C**: Adequate. Works, but important weaknesses remain; improve when artifact will be reused.
- **D**: Risky. Likely to fail under small-model, long-context, or tool-use conditions.
- **F**: Broken. Missing core behavior, unsafe, contradictory, or not executable.

## Core Dimensions

Grade each relevant dimension:

1. **Small-model atomicity** — Are instructions broken into explicit executable steps?
2. **Instruction clarity** — Are task, scope, constraints, and first action clear?
3. **Output contract** — Is the required output precise and parsable?
4. **Context strategy** — Does it avoid unnecessary large context and define read order?
5. **Assumption control** — Are assumptions stated and high-risk unknowns escalated?
6. **Domain fit** — Does it reflect the real domain intent and risk profile?
7. **Validation strength** — Are checks, tests, semantic diffs, or pass/fail criteria present?
8. **Bloat control** — Is the artifact detailed enough without becoming a junk drawer?
9. **Model profile fit** — Are model-specific claims isolated in a selected profile?
10. **No exposed CoT** — Does it avoid requesting chain-of-thought or scratchpads?

## Iteration Threshold

Run another improvement iteration only when:

- any high-impact dimension is **C** or worse, or
- a **B** issue is likely to cause semantic drift, unsafe side effects, context failure, or poor small-model execution.

Do not iterate for cosmetic changes alone.
