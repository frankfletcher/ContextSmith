# Evaluation Rubrics

Use A-F grades to separate bare validation from practical quality.

## Core Dimensions

- Small-model atomicity
- Instruction clarity
- Output contract quality
- Context strategy
- Targeted context fit
- Assumption control
- Domain fit
- Loop safety
- Git/file safety, when relevant
- Validation strength
- Skill interoperability
- Bloat / cognitive load

## Grade Meanings

- **A**: strong, concrete, low-risk, ready to use
- **B**: good, minor weaknesses remain
- **C**: usable but materially weak; iterate if important
- **D**: risky or vague; do not ship without revision
- **F**: fails the requirement or creates unacceptable risk

## Ralph Iteration Rule

Create another iteration only if it materially improves a graded weakness, reduces risk, improves targeted context fit, improves small-model atomicity, fixes validation, or resolves interoperability conflict. Do not iterate for cosmetic polish.

Run another iteration when any critical dimension is C or worse, or when a B-grade issue is high-risk. Stop when all critical dimensions are B or better and no high-risk issue remains.

## Targeted Context Fit

Grade whether the artifact is appropriate for the user's `targeted_context_length`:

- phase granularity fits context budget
- examples/templates are not too long
- reports are compact enough
- context strategy reserves enough room for tools/output
- persistent task state and phase compression are used when context is tight

## Skill Interoperability

Grade whether the artifact handles upstream tool/skill contributions correctly:

- distinguishes confirmed requirements from unsupported additions
- rejects hallucinated libraries/frameworks/workflows
- resolves workflow collisions
- avoids duplicate safeguards
- respects valid domain-specific artifacts
