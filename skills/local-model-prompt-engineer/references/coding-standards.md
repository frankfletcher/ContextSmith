# Coding Standards for Agent Instructions

Use this reference when generating `AGENTS.md` or coding-agent prompts for software projects.

## Repo-Aware First Rule

Follow existing project conventions first. Scan the repo before injecting standards.

Relevant files to inspect:

- `README.md`, `CONTRIBUTING.md`, docs
- `package.json`, `pyproject.toml`, `setup.cfg`, `ruff.toml`, `tox.ini`, `pytest.ini`
- `Makefile`, task runners, CI configs
- `src/`, `tests/`, `notebooks/`, `scripts/`
- existing agent instruction files

## General Coding Standards

- Prefer small, focused changes.
- Keep functions/classes/modules cohesive.
- Use clear names.
- Avoid speculative abstractions.
- Avoid unrelated refactors.
- Preserve public APIs unless the task requires changing them.
- Do not introduce new dependencies without approval.
- Add or update tests for behavior changes.
- Run the narrowest relevant validation first.

## SOLID, Without Ceremony

Use SOLID principles as practical heuristics, not as a reason to over-engineer.

- Single Responsibility: keep each unit focused on one reason to change.
- Open/Closed: extend behavior without modifying stable interfaces when practical.
- Liskov: do not weaken expected behavior of implementations/subclasses.
- Interface Segregation: avoid forcing callers to depend on unused methods.
- Dependency Inversion: depend on abstractions when it reduces coupling, not as ceremony.

Do not add abstractions unless they simplify the current task or protect an existing boundary.

## Python Standards

- Follow PEP 8 unless the repository has a stronger local convention.
- Use the project’s configured formatter/linter when present.
- Prefer type hints for public functions and complex data structures when consistent with the repo.
- Use `uv` when the project already uses it or the user prefers it.
- Do not commit notebooks, data, or model artifacts unless the repo intentionally tracks them.

## JavaScript/TypeScript Standards

- Follow existing formatter/linter settings.
- Prefer TypeScript types that clarify boundaries.
- Avoid broad dependency additions.
- Preserve public component/API behavior unless requested.

## Validation Evidence

Do not claim tests pass unless a test command was run and observed. If validation was not run, state the command and reason.
## Phase Code Review and Test Quality

For coding domains, implementation plans should include:

- TDD when feasible.
- Baseline tests for normal use cases.
- Meaningful edge/failure tests.
- Code review after each phase.
- Narrow validation before broad validation.
- Documentation updates when behavior changes.
- Coverage awareness when the project tracks coverage.

Do not add performative tests that only import code, assert no exception, or mock away the behavior under test.
