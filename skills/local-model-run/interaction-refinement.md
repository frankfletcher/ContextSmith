# Interaction Refinement

Refinement mode lets the user guide execution without turning the run into an open-ended interview.

## Modes

| Mode | Question behavior |
|------|-------------------|
| `silent` | Ask only when blocked or unsafe. |
| `confirm` | Ask one approval question before side effects. |
| `refine` | Ask up to the question budget before execution. |
| `collaborative` | Ask during setup and at major tradeoff boundaries. |
| `review-gate` | Prepare a proposed action and require approval before applying side effects. |

## Question Rules

- Ask only questions whose answers change execution behavior, validation, safety, artifact format, or user-facing output.
- Prefer multiple choice with one recommended default.
- Use multi-select only when choices can coexist.
- Include a short freeform option only when the predefined choices may not cover the user's intent.
- Do not ask cosmetic questions unless the task is explicitly design, style, or voice work.
- Do not ask for information already fixed by user instructions or reliable project evidence.

## Question Budget

Defaults:

| Interaction | Default budget |
|-------------|----------------|
| `silent` | 0 |
| `confirm` | 1 |
| `refine` | 3 |
| `collaborative` | 3 upfront, then phase boundaries |
| `review-gate` | 1 approval per risky step |

Use fewer questions when the prompt is simple. Use all budget only when each question removes a material assumption.

## Generic Refinement Questions

Use these when no stronger domain-specific question applies.

```markdown
1. How should I handle side effects?
- Preview only
- Ask before edits
- Apply safe edits automatically (Recommended when repo validation exists)
- Full execution with validation

2. How strict should validation be?
- Basic sanity check
- Run available validation (Recommended)
- Strict validation plus self-audit
- Strict validation plus Ralph loop

3. What should I optimize for?
- Small-model reliability (Recommended)
- Concise output
- Deep explanation
- Fast completion
```

## Mapping Answers To Parameters

Convert answers into explicit contract fields.

| User choice | Contract effect |
|-------------|-----------------|
| Preview only | `run_mode: dry-run`, `side_effects: none` |
| Ask before edits | `interaction: review-gate` |
| Apply safe edits | `side_effects: file-editing`, `validation: available` |
| Strict validation plus Ralph loop | `validation: strict`, `ralph_iterations_required: max(1, current)` |
| Small-model reliability | compact contract, literal steps, target-profile constraints enforced |
| Deep explanation | report detail increases; model-facing execution context stays compact |

## Anti-Assumption Rule

In refinement mode, do not assume choices that materially affect architecture, dependencies, public APIs, UI framework, storage, deployment, model family, data source, source quality, tone, audience, legal posture, or output format. Infer from evidence when reliable; otherwise ask.
