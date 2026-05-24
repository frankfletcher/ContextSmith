# Test Quality Audit

Use this reference when auditing generated or modified tests. Passing tests are not necessarily useful tests.

## Core Principle

Tests are useful when they would fail if important behavior breaks.

## A-F Rubric

Grade each category A-F.

- **Baseline use-case coverage**: Does the test cover normal expected behavior?
- **Edge-case realism**: Are edge cases plausible and meaningful?
- **Failure-mode coverage**: Are invalid input, missing data, bad state, permissions, timeouts, and other negative paths tested when relevant?
- **Assertion strength**: Are assertions specific enough to catch wrong behavior?
- **Regression-catching power**: Would the test fail if the changed behavior regressed?
- **Changed-behavior coverage**: Do tests exercise the code actually changed?
- **Fixture/data realism**: Do fixtures resemble real inputs enough to matter?
- **Isolation and determinism**: Are tests stable, deterministic, and not dependent on fragile order/timing/network state?
- **Over-mocking risk**: Do mocks remove the behavior the test claims to verify?
- **Maintainability**: Are tests readable and easy to update?

## Weak Test Smells

- Only checks that code imports.
- Only checks that a function does not throw.
- Mocks the method being tested.
- Asserts on implementation details instead of user-visible behavior.
- Uses unrealistic fixtures that miss real boundaries.
- Adds snapshot tests with huge unreviewed outputs.
- Does not include the bug/regression scenario that motivated the change.

## Data Science / ML Test Checks

When relevant, check:

- schema/column expectations
- missing values
- target definition
- train/validation/test split integrity
- preprocessing fit only on training data
- leakage-prone columns
- deterministic seeds
- metric calculation correctness
- inference pipeline consistency
- representative small fixtures

## LLM / RAG Test Checks

When relevant, check:

- retrieval quality separately from generation
- empty retrieval results
- conflicting retrieved context
- citation/evidence requirements
- prompt injection attempts
- structured-output parsing failures
- model/provider unavailable behavior
- golden cases and adversarial cases

## Output Format

```markdown
## Test Quality Summary

Overall grade:
Recommendation: ship | improve tests first | add edge cases | rewrite weak tests | needs human review

## Strong Tests
- ...

## Weak Tests
- test/path::name
  - Problem:
  - Why it matters:
  - Fix:

## Missing Tests
- ...

## Over-Mocking Risks
- ...

## Recommended Additions
1. ...
```
