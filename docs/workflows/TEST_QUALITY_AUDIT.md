# Test Quality Audit

Passing tests are not always useful tests.

Agent-generated tests often look reasonable but fail to protect meaningful behavior. They may only check imports, assert that something “does not throw,” mock away the real behavior, or test edge cases that are not realistic.

A test-quality audit asks:

> Would these tests catch a realistic regression?

## When to use it

Use a test-quality audit when:

- an agent added tests
- a coding phase changed behavior
- tests pass but feel shallow
- a refactor or migration depends on tests for safety
- data-science, ML, or RAG code needs leakage/factuality checks

## What to grade

Grade A-F:

| Dimension | What it checks |
|---|---|
| Baseline behavior | Does the test cover the normal expected use case? |
| Edge-case realism | Are edge cases plausible and meaningful? |
| Failure modes | Are invalid input, missing data, bad state, timeouts, or errors tested when relevant? |
| Regression power | Would the test fail if the changed behavior broke? |
| Assertion strength | Are assertions specific enough? |
| Coverage depth | Are important branches and boundaries covered? |
| Isolation | Does the test avoid fragile global state, timing, network, or order dependence? |
| Fixture realism | Do fixtures resemble real inputs enough to matter? |
| Maintainability | Is the test readable and stable? |
| Over-mocking risk | Did mocks remove the behavior the test claims to verify? |

## Weak test smells

Watch for tests that:

- only check that code imports
- only check that a function does not throw
- assert the result of a mocked method instead of real behavior
- use unrealistic fixtures
- test implementation details instead of public behavior
- do not include a normal happy path
- include edge cases that would never occur
- add snapshots that are too broad to review
- pass even if the core logic is replaced with a stub

## Useful tests

Useful tests usually:

- protect user-visible behavior
- include one normal baseline case
- include meaningful boundaries or failures
- use specific assertions
- would fail if the bug regressed
- use realistic fixtures or representative data
- avoid over-mocking
- are readable enough to maintain

## Data science and ML tests

For DS/ML code, also check:

- schema and column expectations
- missing values
- target definition
- train/validation/test split integrity
- preprocessing fit only on training data
- leakage-prone columns
- deterministic seeds where practical
- metric calculation correctness
- baseline model behavior
- inference pipeline consistency

## LLM/RAG tests

For LLM/RAG code, also check:

- retrieval quality separately from generation
- empty retrieval results
- conflicting retrieved context
- citation/evidence requirements
- prompt injection attempts
- structured-output parsing failures
- model/provider unavailable cases
- golden cases and adversarial cases

## Example output

```markdown
## Test Quality Summary

Overall grade: B-

## Strong Tests
- `tests/test_parser.py::test_valid_multiline_input`
  - Why: covers normal use case and asserts exact parsed structure.

## Weak Tests
- `tests/test_parser.py::test_parser_does_not_crash`
  - Problem: only asserts no exception; would pass with incorrect output.
  - Fix: assert expected parsed fields.

## Missing Tests
- empty input
- malformed multiline input
- Unicode input
- backward compatibility with single-line input

## Recommended Additions
1. Add baseline happy-path test with realistic fixture.
2. Add boundary test for empty input.
3. Add regression test for the bug fixed in this change.
```
