# Phase 3.5: Integration and Bug Fixes

## Issues Identified

After Phase 3 completion, a thorough review identified 11 critical issues:

### Critical Integration Gaps

1. **Adapters not wired into orchestrator** — orchestrator.py has simulated execution, doesn't call HarnessRegistry.get() or adapter.execute()
2. **No tests anywhere** — building complex system with zero test coverage

### Adapter Bugs

3. **OpenCodeAdapter.cancel() broken** — uses subprocess.run() which is synchronous, doesn't populate self._processes dict
2. **GenericAdapter test_mode doesn't write artifacts** — claims files exist but doesn't write them to disk
3. **GenericAdapter await_human doesn't wait** — polls once and returns immediately, misleading name
4. **OpenCodeAdapter exit code handling** — doesn't properly prioritize RESULT.json over exit code

### Architectural Problems

7. **No logging** — uses print() statements everywhere instead of logging module
2. **Checkpoint/STATUS.md race condition** — writes checkpoint then STATUS.md, can diverge on crash
3. **No config validation** — loads workflow config without validating against schema
4. **Unused imports in step_compiler.py** — Path and Optional imported but not used
5. **HarnessRegistry._detect_auto() error handling** — uses step_id="auto" which is a hack

## Fixes Applied

### 1. Wire adapters into orchestrator.py

- Replace simulated execution with actual adapter calls
- Import HarnessRegistry, call discover_adapters()
- Get adapter by name, call validate_environment(), execute()
- Use HarnessResult to determine next state

### 2. Fix OpenCodeAdapter to use Popen

- Change subprocess.run() to subprocess.Popen()
- Store process in self._processes dict
- Implement proper wait with timeout
- Fix cancel() to actually terminate the process

### 3. Fix GenericAdapter test_mode

- Actually write fixture artifacts to disk
- Update artifacts_written to reflect what was written
- Validate artifacts exist after writing

### 4. Rename GenericAdapter await_human

- Rename to poll_human() to clarify it's polling, not blocking
- Add documentation explaining the polling behavior
- Consider adding timeout parameter in future

### 5. Add logging module

- Replace print() statements with logging.info(), logging.warning(), logging.error()
- Use module-level logger: logger = logging.getLogger(**name**)
- Configure logging in orchestrator.py main()

### 6. Add config validation

- Validate workflow config against schema before running
- Check required fields exist
- Return clear error messages for invalid configs

### 7. Fix unused imports

- Remove unused Path and Optional imports from step_compiler.py

### 8. Fix HarnessRegistry error handling

- Create specific exception type for auto-detection failure
- Don't use step_id="auto" hack

### 9. Fix OpenCodeAdapter exit code handling

- Prioritize RESULT.json status over exit code
- Only use exit code as fallback when RESULT.json missing

### 10. Add tests for adapters

- Test GenericAdapter execute with mock artifacts
- Test OpenCodeAdapter command building
- Test adapter registration and discovery
- Test timeout and cancellation

### 11. Document race condition

- Add comment explaining checkpoint/STATUS.md ordering
- Consider atomic write for both files in future

## Sprint Artifacts Updated

- PLAN.md — updated to reflect test-first approach for Phase 4
- CHECKLIST.md — added Phase 3.5 items
- STATUS.md — updated to reflect integration phase
- NEXT_PROMPT.md — updated for Phase 4a with test-first approach

## Files Modified

1. orchestrator/orchestrator.py — wire in adapters, add logging, add config validation
2. orchestrator/adapters/opencode.py — fix cancel(), fix exit code handling
3. orchestrator/adapters/generic.py — fix test_mode, rename await_human
4. orchestrator/adapters/base.py — fix error handling
5. orchestrator/step_compiler.py — remove unused imports
6. tests/test_adapters.py — new file, adapter tests
7. tests/test_orchestrator_integration.py — new file, integration tests

## Next Steps

After these fixes:

- Phase 4 (Validators) should be done test-first
- Phase 5 (Skills) can proceed
- Phase 6 (Integration) will be simpler since tests already exist
