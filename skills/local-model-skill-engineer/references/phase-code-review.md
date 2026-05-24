# Phase Code Review

Use this reference at the end of coding phases.

## Purpose

At phase completion, review only the changes from the phase, catch missed issues, optionally apply one focused improvement pass, validate again, and record the review.

## Default Behavior

- `phase-review: standard` for coding domains.
- `code-review-iterations: 1` by default.
- Use `education-level` to control how much explanation appears in the user-facing review.
- Keep the review phase-local for tight context budgets.

## Review Steps

1. Inspect the phase diff.
2. Review only files changed in this phase unless broader inspection is required.
3. Check correctness, edge cases, tests, maintainability, style, security/secrets, performance, typing/lint, and project conventions.
4. Classify findings as must fix, should fix, note for later, or acceptable tradeoff.
5. Apply at most one focused improvement pass unless the user requested deeper iteration.
6. Re-run the narrowest relevant validation.
7. Record the review in `PHASE_LOG.md` or `reports/phase-XX-code-review.md`.

## Focused Improvement Pass

Only change code if the improvement:

- fixes correctness
- strengthens a weak test
- removes unnecessary complexity
- aligns with project conventions
- reduces regression risk
- improves maintainability without broad refactor

Do not perform cosmetic refactors or expand scope.

## Report Format

```markdown
# Phase Code Review

## Scope
- Phase:
- Files reviewed:
- Validation run:

## Summary
- Overall assessment:
- Main risk:
- Recommendation: proceed | fix first | needs human review

## Findings

### Must Fix
- ...

### Should Fix
- ...

### Notes for Later
- ...

## Test Quality
- Baseline tests:
- Edge cases:
- Missing tests:
- Weak assertions:

## Improvements Applied
- ...

## Remaining Risks
- ...

## User Learning Notes
- ...
```
