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
- DRY - do not repeat logic in multiple places.
- YAGNI - do not add features or abstractions until they are needed.
- KISS - prefer simple solutions over complex ones.
- Prefer readability and maintainability over cleverness or terseness.
- Test Driven Development when feasible, especially for new code or behavior changes.

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
## Write Simple Code First

Avoid ever writing a function that will fail a complexity gate. These patterns keep cyclomatic complexity ≤ B and maintainability ≥ A on the first pass.

### One Job Per Function

If a function name contains "and", split it. A function should do one thing, do it well, and return.

```python
# Bad — two jobs
def load_and_validate(path):
    data = json.loads(path.read_text())
    errors = validate_schema(data)
    return data, errors

# Good — extracted
def load_data(path):
    return json.loads(path.read_text())

def validate_data(data):
    return validate_schema(data)
```

### Extract Conditionals

Any if/elif chain with 3+ branches should have each branch extracted into a named function or a dispatch dict.

```python
# Bad — C complexity from branching
def handle_status(status):
    if status == "pass":
        # 8 lines
    elif status == "fail":
        # 8 lines
    elif status == "blocked":
        # 8 lines

# Good — dispatch table
_HANDLERS = {"pass": _handle_pass, "fail": _handle_fail, "blocked": _handle_blocked}

def handle_status(status):
    handler = _HANDLERS.get(status)
    return handler() if handler else _handle_unknown(status)
```

### Guard Clauses Over Nesting

Return early. Never nest deeper than 3 levels. Each `if` without an `else` that returns early is one less path through the function.

```python
# Bad — nested
def process(x):
    if x is not None:
        if x.valid:
            result = x.compute()
            if result:
                return result
    return None

# Good — guard clauses
def process(x):
    if x is None:
        return None
    if not x.valid:
        return None
    result = x.compute()
    if not result:
        return None
    return result
```

### Extract Inner Loops

If a loop body has its own conditionals or nested loops, extract the body.

```python
# Bad — loop + conditional = complexity
for item in items:
    if item.active:
        value = item.compute()
        if value > threshold:
            results.append(transform(value))

# Good — extracted body
def _process_item(item, threshold):
    if not item.active:
        return None
    value = item.compute()
    return transform(value) if value > threshold else None

results = [r for r in (_process_item(i, threshold) for i in items) if r is not None]
```

### Boolean Parameters Are a Smell

A boolean parameter means the function has two behaviors. Extract two functions instead.

```python
# Bad
def render(widget, show_details=False):
    if show_details:
        # detailed path
    else:
        # summary path

# Good
def render_summary(widget): ...
def render_details(widget): ...
```

### 3-Parameter Limit

More than 3 parameters increases coupling and testing complexity. Use a dataclass, config object, or builder pattern.

```python
# Bad — 5 positional params
def train(model, data, epochs, lr, batch_size): ...

# Good — config object
@dataclass
class TrainingConfig:
    model: str
    data: str
    epochs: int = 10
    lr: float = 0.001
    batch_size: int = 32

def train(config: TrainingConfig): ...
```

### Prefer `match` Over Long if/elif Chains

Python 3.10+ `match` statements have clearer branching structure for pattern-based dispatch.

### Cyclomatic Complexity Floor

These heuristics keep complexity ≤ B (≤ 10 independent paths through a function):

- Max 3 if/elif branches (extract each branch if more)
- Max 2 levels of loop nesting
- Max 1 level of conditional nesting inside a loop
- No boolean parameters
- All guard clauses return early (don't count toward path explosion)
- Extract file I/O, validation, and formatting into dedicated helpers

- TDD when feasible.
- Baseline tests for normal use cases.
- Meaningful edge/failure tests.
- Code review after each phase.
- Narrow validation before broad validation.
- Documentation updates when behavior changes.
- Coverage awareness when the project tracks coverage.

Do not add performative tests that only import code, assert no exception, or mock away the behavior under test.
