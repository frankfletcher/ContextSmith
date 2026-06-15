# Ruff Integration Complete

## Summary

Added ruff linting, formatting, and import sorting to the entire project pipeline. All Python code now passes ruff checks.

## Changes Made

### 1. AGENTS.md Updated

**Setup and Validation Commands:**

```bash
python scripts/validate_skills.py
ruff check orchestrator/ --select E,F,W,I
ruff format orchestrator/ --check
pytest tests/ -v
```

**Coding Standards:**

- All Python code must pass `ruff check --select E,F,W,I` and `ruff format --check`
- Run `ruff check --fix` and `ruff format` before committing
- Follow PEP 8 (enforced by ruff)

**Repository Map:**

- Added orchestrator/ package structure
- Added tests/ directory

### 2. PLAN.md Updated

**Validation Commands:**

```bash

# Validate skills
python scripts/validate_skills.py

# Lint and format Python code
ruff check orchestrator/ --select E,F,W,I
ruff format orchestrator/ --check

# Run tests
pytest tests/ -v
```

**Self-Audit Checklist:**

- Added: "Ruff passes — `ruff check orchestrator/ --select E,F,W,I` and `ruff format --check` succeed (for Python phases)"

### 3. Python Code Fixed

**Files Modified:**

- orchestrator/adapters/**init**.py — import sorting, line length
- orchestrator/adapters/base.py — import sorting, line length, docstrings
- orchestrator/adapters/generic.py — import sorting, formatting
- orchestrator/adapters/opencode.py — import sorting, line length, formatting
- orchestrator/orchestrator.py — import sorting, line length, formatting
- orchestrator/step_compiler.py — import sorting, line length, docstrings
- orchestrator/cli.py — formatting
- orchestrator/checkpoint.py — formatting
- orchestrator/state_reader.py — formatting
- orchestrator/constants.py — formatting
- orchestrator/exceptions.py — formatting
- orchestrator/**init**.py — formatting
- orchestrator/**main**.py — formatting

**Issues Fixed:**

- 4 unsorted imports (I001)
- 36 line-too-long errors (E501)
- All formatting issues

**Result:** All ruff checks pass (E, F, W, I)

### 4. Sprint Artifacts Updated

**STATUS.md:**

- Added "phase_3.5_ruff: PASS" to completed list
- Added item 11 to Phase 3.5 Fixes Applied

**CHECKLIST.md:**

- Added "Code Quality" section with 7 ruff-related items

## Verification

```bash
$ ruff check orchestrator/ --select E,F,W,I
All checks passed!

$ ruff format orchestrator/ --check
13 files already formatted

$ pytest tests/test_adapters.py -v
============================== 28 passed in 0.03s ==============================
```

## Impact

All future Python development in this project must:

1. Pass ruff linting (E, F, W, I rules)
2. Pass ruff formatting
3. Have sorted imports
4. Follow PEP 8

This ensures code quality and consistency across the entire codebase.

## Next Steps

Phase 4 (Validators) will also follow these standards:

- Write tests first
- Implement validators
- Run ruff checks before committing
- All code must pass ruff linting and formatting
