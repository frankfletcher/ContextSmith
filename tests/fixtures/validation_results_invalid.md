# Validation Results: Invalid Test Fixtures

## Purpose

These fixtures are negative test cases — they should FAIL validation against the schemas.

## Results

### invalid_workflow_missing_field

- Fixture: `tests/fixtures/invalid_workflow_missing_field.yaml`
- Expected failure: Missing required field `version`
- Result: **EXPECTED FAIL**
- Error message: `'version' is a required property`
- Matches expected rule: Yes

### invalid_workflow_bad_state

- Fixture: `tests/fixtures/invalid_workflow_bad_state.yaml`
- Expected failure: Invalid state enum value
- Result: **EXPECTED FAIL**
- Error message: `'invalid_state' is not one of ['init', 'plan', 'execute', 'audit', 'fix', 'validate', 'ralph_critique', 'ralph_revise', 'closeout', 'done', 'blocked']`
- Matches expected rule: Yes

### invalid_workflow_bad_transition

- Fixture: `tests/fixtures/invalid_workflow_bad_transition.yaml`
- Expected failure: Transition missing required field `target`
- Result: **EXPECTED FAIL**
- Error message: `'target' is a required property`
- Matches expected rule: Yes

### invalid_agent_missing_permission

- Fixture: `tests/fixtures/invalid_agent_missing_permission.yaml`
- Expected failure: Missing required field `permission`
- Result: **EXPECTED FAIL**
- Error message: `'permission' is a required property`
- Matches expected rule: Yes

### invalid_agent_bad_mode

- Fixture: `tests/fixtures/invalid_agent_bad_mode.yaml`
- Expected failure: Invalid mode enum value
- Result: **EXPECTED FAIL**
- Error message: `'invalid_mode' is not one of ['primary', 'subagent']`
- Matches expected rule: Yes

## Summary

All 5 invalid fixtures failed validation as expected. Each error message matches the expected validation rule indicated in the fixture filename.
