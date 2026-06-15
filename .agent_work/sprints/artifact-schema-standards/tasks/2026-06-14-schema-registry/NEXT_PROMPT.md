# NEXT_PROMPT.md

You are continuing work on the ContextSmith artifact schema standards task.

## Current Status

- Phase: 12 of 12 — Packaging and Distribution
- Sub-phase: 12.1 — Orchestrator packaging
- State: execute

## Sub-phase Tasks

- [ ] Add pyproject.toml `[project.scripts]` entry point: `contextsmith-orchestrator = "orchestrator.cli:main"`
- [ ] Ensure `pip install -e .` makes `python -m orchestrator` and `contextsmith-orchestrator` available
- [ ] Verify CLI help output and subcommands work

## Your Task

The orchestrator is now the production runtime (D15 commitment). `.new` file auto-merging is active — agents must NOT merge manually. This sub-phase makes the orchestrator CLI installable:

1. **Update pyproject.toml**: Add `[project.scripts]` with `contextsmith-orchestrator = "orchestrator.cli:main"`. Ensure the build backend supports CLI entry points (hatchling/flit_core already configured).
2. **Test installation**: Run `pip install -e .` (or `uv pip install -e .`) and verify `python -m orchestrator.cli --help` and `contextsmith-orchestrator --help` (or equivalent) work.
3. **Verify no regressions**: Run `uv run pytest tests/ -v` to confirm all tests pass after the change.

## Input Files

- `pyproject.toml`: Build configuration (add entry point)
- `orchestrator/cli.py`: CLI entry point (already exists, verify arg parsing works)
- `orchestrator/__main__.py`: Module entry point (already exists for `python -m orchestrator`)
- `STATUS.md`: Current workflow state
- `PLAN.md`: Phase plan
- `CONTEXT.md`: Project context and constraints
- `DECISIONS.md`: D15 orchestrator commitment

## Output Requirements

- Updated `pyproject.toml` with `[project.scripts]` entry point
- Working CLI: `python -m orchestrator.cli --help` produces expected output
- All 423+ tests pass

## Constraints

- Context Budget: 16k
- Do not modify orchestrator behavior, only packaging
- Do not change existing tests
- Follow pep621 conventions for pyproject.toml

## Ralph Loop Enforcement

3 iterations required. Each is critique+fix. Do not skip or collapse.

## Self-Audit

Before closeout, verify:
- `contextsmith-orchestrator` CLI command is available after pip install
- `python -m orchestrator.cli --help` shows subcommands
- No test regressions
- Side-effect boundaries respected

## Hard Stop

Current phase is Phase 12: Packaging and Distribution. Do not proceed beyond sub-phase 12.1. Do not implement Phase 12.2-12.6 tasks.

## Expected Output Format

```
## Result
## Evidence
## Self-Audit
## Ralph Summary
## Validation
## Declared vs Enforced
## Risks / Next Action
```
