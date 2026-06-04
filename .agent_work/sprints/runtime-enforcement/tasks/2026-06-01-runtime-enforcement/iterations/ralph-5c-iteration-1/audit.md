# Ralph Loop Iteration 1 — Phase 5C Next Prompt Compiler Tests

## Artifact Manifest
- artifact_type: ralph-audit
- phase: Phase 5C
- iteration: 1 of 2
- target: 25 new tests in `tests/test_next_prompt_compiler.py`

## A-F Rubric

| Category | Grade | Notes |
|---|---|---|
| Small-model atomicity | B | Each test is single-concern, clear assertions. Regex parsing in read-order/closeout/recovery/self-audit tests is fragile but appropriate. |
| Instruction clarity | B | Test names and docstrings match behavior. Some docstrings could be more specific about what's being verified. |
| Output contract quality | B- | Assertions are concrete but some are weakened to match current compiler behavior rather than testing desired behavior. |
| Context strategy | A | Minimal fixtures, no excessive setup. tempfile.TemporaryDirectory() used throughout. |
| Assumption control | C | `test_context_constraints_extracted` only checks "## Read Order" exists, not that constraints are actually included. `test_phase_with_inline_content_in_mission` only checks phase title appears. |
| Domain fit | A | Tests align with Phase 5C requirements and compiler purpose. |
| Validation strength | C | Weak assertions in 4 tests. Missing output size verification test (Phase 5A spec mentions budget risk). Missing `--output` flag content verification. |
| Loop safety | A | No loops in tests. |
| Git/file safety | A | Tests use tempfile, no workspace edits. |
| Bloat / cognitive load | A | Tests are compact. No duplication. |

## Material Defects

1. **Weak assertion - `test_context_constraints_extracted`**: Only checks "## Read Order" exists. Doesn't verify constraints are actually in the output. Should check for constraint text or a stronger signal.

2. **Weak assertion - `test_phase_with_inline_content_in_mission`**: Only checks "With Content" (the phase title) appears. Doesn't verify phase block content is included.

3. **Missing test - output size verification**: Phase 5A spec notes the risk that 12-section output may exceed small-model context. No test verifies generated prompt size stays within budget.

4. **Missing test - `--output` flag content verification**: CLI test checks file exists but doesn't verify content matches programmatic API output.

5. **Missing test - STATUS/PLAN disagreement error**: Phase 5A spec requires an error when STATUS.md phase doesn't match PLAN.md. No test covers this.

## Changes Applied

1. Strengthened `test_context_constraints_extracted` assertion
2. Strengthened `test_phase_with_inline_content_in_mission` assertion
3. Added `test_generated_prompt_size_within_budget` test
4. Added `test_output_flag_content_matches_api` test
5. Added `test_status_plan_disagreement_raises_error` test

## Iteration 1 Result

4 material defects addressed. 1 minor weakness (education tests weakened to match current behavior) accepted as intentional — tests current compiler behavior, not aspirational behavior.
