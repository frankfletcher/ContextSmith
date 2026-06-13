# Educational Report: Phase 3 — Harness Adapters

## What Was Done

Phase 3 implemented the harness adapter layer, which bridges the orchestrator and the agent execution runtime. Four files were created:

### 1. `orchestrator/adapters/base.py` (144 lines)

- **StepContract** dataclass: bounded step definition with step_id, state, agent_profile, permissions, inputs, expected_outputs, timeout_s, max_retries, and optional fields
- **HarnessResult** dataclass: structured result with status, reason, artifacts, validation, issues, next_action
- **HarnessAdapter** ABC: abstract base class with name, validate_environment(), execute(), cancel(), get_capabilities()
- **HarnessRegistry** class: adapter discovery and registration with register(), get(), list_available(),_detect_auto()
- **HarnessTimeoutError** and **HarnessExecutionError**: exception types for harness-level failures

### 2. `orchestrator/adapters/__init__.py` (39 lines)

- ADAPTER_REGISTRY list: ["opencode", "generic"]
- discover_adapters() function: imports all registered adapters to trigger registration
- Re-exports all base types for convenience

### 3. `orchestrator/adapters/generic.py` (174 lines)

- **GenericAdapter** class: file-based fallback with no external agent runtime
- Writes .pending_prompt.md to disk for human or test execution
- Supports test_mode (fixture injection) and await_human mode
- Reads RESULT.json if present, otherwise checks artifact presence
- Registers with HarnessRegistry at module import time

### 4. `orchestrator/adapters/opencode.py` (177 lines)

- **OpenCodeAdapter** class: subprocess-based agent execution via OpenCode CLI
- Builds command: `opencode run --agent <profile> --model <model> --file NEXT_PROMPT.md --format json`
- Maps permissions to agent profiles (read-only → contextsmith-auditor, edit → contextsmith-builder, external-action → contextsmith-migrator)
- Launches subprocess with timeout enforcement
- Reads RESULT.json and collects artifacts from disk
- Supports cancellation via process termination
- Registers with HarnessRegistry at module import time

### Integration Changes

- Updated `orchestrator/step_compiler.py` to import StepContract from adapters/base.py instead of defining it locally
- Updated `orchestrator/exceptions.py` to re-export HarnessTimeoutError and HarnessExecutionError from adapters/base.py
- Updated `orchestrator/__init__.py` to export the new exception types

## Why It Matters

The harness adapter layer is the bridge between the orchestrator's workflow logic and the agent execution runtime. Without it:

- The orchestrator cannot launch agents or collect their outputs
- There is no way to enforce timeouts, permissions, or step limits
- The system cannot work with different agent runtimes (OpenCode, generic, future harnesses)
- Test mode and human-in-the-loop workflows would not be possible

The adapter pattern allows the orchestrator to remain harness-agnostic while still providing best-in-class support for specific runtimes like OpenCode. The generic adapter ensures the system works even without an external agent runtime, enabling testing, debugging, and manual execution.

## How It Works

### Adapter Registration

1. Each adapter module (generic.py, opencode.py) defines a class that inherits from HarnessAdapter
2. At module import time, the adapter calls `HarnessRegistry.register(AdapterClass)`
3. The registry instantiates the adapter and stores it by name
4. The orchestrator calls `HarnessRegistry.get(name)` to retrieve an adapter instance

### Adapter Lifecycle

1. **Discovery**: orchestrator calls `discover_adapters()` to import all registered adapter modules
2. **Selection**: orchestrator calls `HarnessRegistry.get(harness_name)` or `_detect_auto()`
3. **Validation**: orchestrator calls `adapter.validate_environment()` to check runtime availability
4. **Execution**: orchestrator calls `adapter.execute(contract, state_dir)` for each step
5. **Result**: adapter returns HarnessResult with status, artifacts, validation
6. **Cancellation**: orchestrator may call `adapter.cancel(step_id)` from another thread

### Step Execution Flow

1. Orchestrator compiles StepContract from config + state + plan
2. Orchestrator calls `adapter.execute(contract, state_dir)`
3. Adapter translates contract into harness-native commands
4. Adapter launches agent (subprocess for OpenCode, file-based for generic)
5. Adapter waits for completion or timeout
6. Adapter reads RESULT.json from state_dir
7. Adapter collects artifacts from disk
8. Adapter returns HarnessResult to orchestrator
9. Orchestrator validates artifacts and transitions to next state

### Key Design Decisions

**StepContract defined in adapters/base.py, not step_compiler.py**: This avoids circular imports and makes the contract available to both the orchestrator and the adapters. The step_compiler imports it from base.py.

**HarnessTimeoutError and HarnessExecutionError in adapters/base.py**: These are harness-level exceptions, not orchestrator-level. The exceptions.py module re-exports them for convenience, but the canonical definition is in adapters/base.py.

**GenericAdapter writes .pending_prompt.md**: This allows human operators to execute steps manually by reading the prompt file and writing RESULT.json. It also enables test mode by injecting fixture responses.

**OpenCodeAdapter maps permissions to agent profiles**: The adapter translates generic permission levels (read-only, edit, external-action) into OpenCode-specific agent profiles (contextsmith-auditor, contextsmith-builder, contextsmith-migrator). This keeps the orchestrator harness-agnostic.

**Adapters register at import time**: This allows the registry to discover adapters without explicit registration calls. The **init**.py maintains a manifest (ADAPTER_REGISTRY) and imports all listed modules.

## Data Flow

```
Orchestrator
  ↓
compile_step_contract(state, config, plan, context)
  ↓
StepContract
  ↓
HarnessRegistry.get(harness_name)
  ↓
HarnessAdapter instance
  ↓
adapter.validate_environment() → []
  ↓
adapter.execute(contract, state_dir)
  ↓
[OpenCode: subprocess.run()] or [Generic: write .pending_prompt.md]
  ↓
[Read RESULT.json] or [Check artifacts]
  ↓
HarnessResult
  ↓
Orchestrator validates and transitions
```

## For Small Models

- **StepContract**: A dataclass with all the information needed to execute one bounded step. The adapter uses this to build the agent invocation.
- **HarnessResult**: A dataclass with the execution outcome. The orchestrator uses this to decide the next state.
- **HarnessAdapter**: An abstract base class. Every adapter must implement name, validate_environment, execute, cancel, and get_capabilities.
- **HarnessRegistry**: A class that stores adapter instances by name. Call register() to add an adapter, get() to retrieve it.
- **GenericAdapter**: Always available, no external runtime. Writes .pending_prompt.md, checks for RESULT.json.
- **OpenCodeAdapter**: Launches OpenCode subprocess. Maps permissions to agent profiles. Reads RESULT.json.

**Common mistakes to avoid:**

- Do not define StepContract in step_compiler.py (it's in adapters/base.py)
- Do not forget to call HarnessRegistry.register() at module import time
- Do not raise exceptions for agent-level failures (use HarnessResult.status instead)
- Do not capture agent stdout (let it stream to user for real-time visibility)

**What to check if something goes wrong:**

- `python3 -c "from orchestrator.adapters.base import HarnessAdapter"` should succeed
- `python3 -c "from orchestrator.adapters import discover_adapters"` should succeed
- `HarnessRegistry.list_available()` should return ['generic', 'opencode']
- `adapter.validate_environment()` should return [] if the runtime is available

---

# Educational Report: Phase 3 — Harness Adapters (Reconstructed Version)

## What Was Done

### Files Created

- `orchestrator/adapters/__init__.py` (39 lines) — adapter discovery and registry exports
- `orchestrator/adapters/base.py` (144 lines) — StepContract, HarnessResult, HarnessAdapter ABC, HarnessRegistry, HarnessTimeoutError, HarnessExecutionError
- `orchestrator/adapters/generic.py` (174 lines) — GenericAdapter for file-based fallback execution
- `orchestrator/adapters/opencode.py` (177 lines) — OpenCodeAdapter for subprocess-based agent execution

### Files Modified

- `orchestrator/step_compiler.py` — removed local StepContract definition, now imports from adapters.base
- `orchestrator/exceptions.py` — re-exports HarnessTimeoutError and HarnessExecutionError from adapters.base
- `orchestrator/__init__.py` — exports HarnessTimeoutError and HarnessExecutionError

### Key Classes and Functions

- `StepContract` dataclass — bounded step definition with step_id, state, agent_profile, permissions, inputs, expected_outputs, timeout_s, max_retries, validation_mode, model_pin, task_state_dir, extra
- `HarnessResult` dataclass — structured result with status, step_id, reason, artifacts, artifacts_written, validation, issues, next_action
- `HarnessAdapter` ABC — abstract base with name, validate_environment(), execute(), cancel(), get_capabilities()
- `HarnessRegistry` — class-level registry with register(), get(), list_available(),_detect_auto()
- `GenericAdapter` — file-based adapter with test_mode and await_human support
- `OpenCodeAdapter` — subprocess-based adapter with _build_command() and _read_result()

## Why It Matters

Phase 3 implements the harness adapter layer, which is the bridge between the orchestrator (workflow control) and the agent runtime (execution). This separation allows:

1. **Harness agnosticism** — the orchestrator doesn't care if the agent is OpenCode, a human, or a mock
2. **Testability** — GenericAdapter supports test_mode with fixture injection
3. **Flexibility** — new adapters can be added without modifying the orchestrator
4. **Fallback** — GenericAdapter works without any external agent runtime

Without this layer, the orchestrator would be tightly coupled to OpenCode, making it impossible to test, debug, or use in environments without OpenCode installed.

## How It Works

### Adapter Discovery and Registration

1. Each adapter module (generic.py, opencode.py) calls `HarnessRegistry.register(AdapterClass)` at import time
2. The registry instantiates the adapter and stores it by name
3. `orchestrator/adapters/__init__.py` maintains `ADAPTER_REGISTRY` list and provides `discover_adapters()` to import all adapters
4. The orchestrator calls `HarnessRegistry.get(name)` to retrieve an adapter by name, or `"auto"` to auto-detect

### Execution Flow

1. Orchestrator loads workflow config and reads state
2. Orchestrator compiles StepContract from config + state + plan
3. Orchestrator retrieves adapter via `HarnessRegistry.get(harness_name)`
4. Adapter.validate_environment() checks if runtime is available
5. Adapter.execute(contract, state_dir) launches agent subprocess
6. Adapter reads RESULT.json from state_dir
7. Adapter collects artifacts from expected_outputs
8. Adapter returns HarnessResult to orchestrator
9. Orchestrator validates result, resolves next state, updates checkpoint

### Generic Adapter Protocol

1. Writes `.pending_prompt.md` to state_dir (the prompt for the agent)
2. If test_mode: loads fixture from contract.extra["fixture"], returns mock result
3. If await_human: waits for `.human_response.md`, returns human response
4. Otherwise: reads RESULT.json if present, collects existing artifacts
5. Returns HarnessResult with status from RESULT.json or inferred from artifact presence

### OpenCode Adapter Protocol

1. Builds command: `opencode run --agent <profile> --model <model> --file NEXT_PROMPT.md --format json`
2. Launches subprocess with timeout enforcement
3. Reads RESULT.json from state_dir
4. Collects artifacts from expected_outputs
5. Returns HarnessResult with status from RESULT.json or inferred from exit code + artifacts

## Key Function Signatures

```python
# base.py
@dataclass
class StepContract:
    step_id: str
    state: str
    agent_profile: str
    permissions: str
    inputs: list[str]
    expected_outputs: list[str]
    timeout_s: int
    max_retries: int
    ralph_max_cycles: int = 0
    validation_mode: str = "strict"
    model_pin: Optional[str] = None
    checkpoint_before_run: bool = False
    prompt_template: Optional[str] = None
    workflow_id: str = ""
    task_state_dir: str = ""
    extra: dict = field(default_factory=dict)

@dataclass
class HarnessResult:
    status: str
    step_id: str
    reason: str
    artifacts: dict[str, str]
    artifacts_written: list[str]
    validation: dict
    issues: list[str]
    next_action: str
    extra: dict = field(default_factory=dict)

class HarnessAdapter(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...
    
    @abstractmethod
    def validate_environment(self) -> list[str]: ...
    
    @abstractmethod
    def execute(self, contract: StepContract, state_dir: Path) -> HarnessResult: ...
    
    @abstractmethod
    def cancel(self, step_id: str) -> bool: ...
    
    def get_capabilities(self) -> dict: ...

class HarnessRegistry:
    @classmethod
    def register(cls, adapter_class: type[HarnessAdapter]) -> None: ...
    
    @classmethod
    def get(cls, name: str) -> HarnessAdapter: ...
    
    @classmethod
    def list_available(cls) -> list[str]: ...
```

## Data Flow

```
orchestrator.py
  ↓ compile_step_contract()
StepContract
  ↓ HarnessRegistry.get(name)
HarnessAdapter
  ↓ adapter.execute(contract, state_dir)
  ↓ launches subprocess / writes .pending_prompt.md
  ↓ reads RESULT.json
  ↓ collects artifacts
HarnessResult
  ↓ orchestrator.py
  ↓ resolve_next_state()
  ↓ update_checkpoint()
  ↓ _update_status()
  ↓ _write_phase_log()
```

## For Small Models

**How to use the adapters:**

```python
from orchestrator.adapters import discover_adapters
from orchestrator.adapters.base import HarnessRegistry

# Discover all adapters
discover_adapters()

# Get adapter by name
adapter = HarnessRegistry.get("generic")  # or "opencode"

# Check environment
errors = adapter.validate_environment()
if errors:
    print(f"Adapter not ready: {errors}")
else:
    # Execute a step
    result = adapter.execute(contract, state_dir)
    print(f"Status: {result.status}")
```

**Common mistakes to avoid:**

- Don't import StepContract from step_compiler.py anymore — it's now in adapters.base
- Don't forget to call discover_adapters() before using HarnessRegistry.get()
- Don't modify checkpoint.json in the adapter — the orchestrator owns that
- Don't capture agent stdout — let it stream to the user

**What to check if something goes wrong:**

- ImportError: make sure you're importing from orchestrator.adapters.base, not orchestrator.step_compiler
- KeyError: adapter not registered — call discover_adapters() first
- HarnessTimeoutError: agent took too long — increase timeout_s in workflow config
- HarnessExecutionError: harness itself failed — check opencode is installed, check subprocess errors

---

# Educational Report: Phase 4a — File Validators

## What Was Done

### Files Created

- `tests/test_validators.py` (188 lines) — comprehensive test suite with 29 tests for all validator functions
- `orchestrator/validators.py` (107 lines) — file existence, non-empty, section presence, and batch artifact validators

### Key Functions

```python
def _extract_sections(content: str) -> list[str]:
    """Extract ATX-style section names from Markdown content.
    Returns section names without the '## ' prefix.
    """

def validate_file_exists(path: Path) -> list[str]:
    """Check if file exists. Returns [] if exists, [error] if not."""

def validate_file_nonempty(path: Path) -> list[str]:
    """Check if file is non-empty. Returns [] if non-empty, [error] otherwise."""

def validate_required_sections(path: Path, sections: list[str]) -> list[str]:
    """Check file has required sections. Returns [] if all present, [errors] if missing."""

def validate_artifact(file_path: Path, required_sections=None) -> list[str]:
    """Check exists, non-empty, and sections. Returns list of errors."""

def validate_artifacts(state_dir: Path, expected_outputs: list[str], config: dict) -> dict:
    """Validate all expected artifacts from a step contract.
    Returns {"passed": bool, "failures": list[str], "files_checked": int, "files_passed": int}.
    """
```

### Design Decision

- Test-first approach: wrote 29 tests before implementation code
- Section detection uses ATX-style heading parsing (not substring search) for correctness
- `validate_artifact` short-circuits on file not found / empty before checking sections
- `validate_artifacts` accepts a config dict with `section_requirements` mapping filenames to required sections

## Why It Matters

The file validators are the orchestrator's quality gate for task-state artifacts. After the harness executes a step, the orchestrator calls `validate_artifacts()` to verify that all expected output files exist, are non-empty, and contain required sections. This prevents corrupted or incomplete state from advancing the workflow.

Without this layer, the orchestrator would blindly accept any output, potentially continuing a workflow with missing or empty state files.

## How It Works

1. After harness execution, the orchestrator calls `validate_artifacts(state_dir, expected_outputs, config)`
2. For each expected file: check existence → check non-empty → check required sections
3. Early exit on first failure per file (no point checking sections of a missing file)
4. Returns a summary dict with pass/fail, failure details, and file counts
5. The orchestrator uses the result to decide: advance state, retry, or block

### Data Flow

```
orchestrator.py → validate_artifacts(state_dir, expected_outputs, config)
  ↓
  for each filename in expected_outputs:
    validate_artifact(file_path, required_sections)
      ↓
      validate_file_nonempty() → validate_required_sections()
        ↓
        _extract_sections(content) → compare with required sections
  ↓
{"passed": True/False, "failures": [...], "files_checked": N, "files_passed": N}
  ↓
orchestrator uses result for state transition
```

### For Small Models

- `_extract_sections` loops over lines looking for `##` prefix — that's it
- `validate_file_exists` is one `path.exists()` call
- `validate_file_nonempty` checks path exists, then `st_size == 0`
- `validate_artifact` chains: nonempty → sections (skips sections if nonempty fails)
- `validate_artifacts` iterates a list, collects results

**Common mistakes to avoid:**

- Don't check sections on a missing file — short-circuit before reading
- Section names in `required_sections` should match the text after `##` (not including `##`)
- Use `validate_artifacts` not individual validators from orchestrator.py

**What to check if something goes wrong:**

- `uv run pytest tests/test_validators.py -v` — all 29 tests should pass
- `uv run python -c "from orchestrator.validators import validate_artifacts"` — import works
- Check file paths are absolute or relative to state_dir, not current working directory
- Verify section names match exactly (case-sensitive, no `##` prefix)

---

# Educational Report: Phase 4b — Schema Validators

## What Was Done

### Files Modified

- `tests/test_validators.py` — appended 4 new test classes (10 tests) for schema validation
- `orchestrator/validators.py` — appended 4 new functions: validate_schema, validate_workflow_config, validate_agent_config, validate_checkpoint

### Key Functions Added

```python
def validate_schema(data: dict, schema_path: Path) -> list[str]:
    """Validate data against a JSON schema. Returns [] if valid, [errors] if not."""

def validate_workflow_config(config_path: Path) -> list[str]:
    """Validate a workflow config YAML file against workflow_config.schema.json."""

def validate_agent_config(config_path: Path) -> list[str]:
    """Validate an agent config YAML file against agent_config.schema.json."""

def validate_checkpoint(checkpoint_path: Path, config: dict | None = None) -> list[str]:
    """Validate a checkpoint JSON file against required structure."""
```

### Design Decisions

- All imports in the new functions are local (inside function body) to avoid circular imports
- `_SCHEMAS_DIR` computed from `Path(__file__).parent.parent / "schemas"` so validators work regardless of working directory
- `validate_schema` handles 4 failure modes: missing schema file, invalid schema JSON, ValidationError, SchemaError
- `validate_checkpoint` optionally accepts a config dict to validate phase/state names against known values
- Test-first: wrote 10 tests before writing implementation

## Why It Matters

Schema validation ensures workflow configurations and agent definitions are structurally valid before the orchestrator uses them. Without it, invalid YAML files, missing required fields, or unknown state references would cause runtime errors deep in the execution loop.

The checkpoint validator catches corrupted or inconsistent checkpoint files before the orchestrator attempts to resume from them, preventing silent data loss.

## How It Works

1. `validate_schema` reads a JSON schema file, parses it, and validates the data using jsonschema
2. `validate_workflow_config` reads a YAML config, loads the workflow_config.schema.json, and validates
3. `validate_agent_config` does the same with agent_config.schema.json
4. `validate_checkpoint` reads JSON directly (it's always JSON), checks for 5 required fields, validates version is int >= 1, and optionally checks phase/state names against the workflow config

### Data Flow

```
validate_workflow_config(config.yaml)
  → yaml.safe_load()
  → validate_schema(data, schemas/workflow_config.schema.json)
    → json.loads(schema)
    → jsonschema.validate(instance=data, schema=schema)
    → [] or ["Schema validation failed: ..."]

validate_checkpoint(checkpoint.json, config)
  → json.loads()
  → check required fields
  → check version is int >= 1
  → if config: validate phase/state names
  → [] or [errors]
```

### For Small Models

- `validate_schema` is the core: read schema JSON → jsonschema.validate → catch errors
- `validate_workflow_config` reads YAML → calls validate_schema with workflow_config.schema.json
- `validate_agent_config` same pattern with agent_config.schema.json
- `validate_checkpoint` does NOT use jsonschema (it's simple field checks)
- All functions return `list[str]` where `[]` = valid

**Common mistakes to avoid:**

- Don't import jsonschema at module level (import locally to avoid circular deps)
- Don't forget that `yaml.safe_load` can return None for empty files
- Schemas are relative to `orchestrator/` package root, not the working directory
- `validate_checkpoint` with config=None skips phase/state validation

**What to check if something goes wrong:**

- `uv run python -c "from orchestrator.validators import validate_schema"` — import works
- `uv run pytest tests/test_validators.py -v` — 39 tests pass
- PyYAML must be installed: `uv run python -c "import yaml"`
- Schema files must exist at `schemas/workflow_config.schema.json` and `schemas/agent_config.schema.json`

---

# Educational Report: Phase 4c — State Consistency Validator

## What Was Done

### Files Modified

- `tests/test_validators.py` — appended `TestValidateStateConsistency` class with 6 tests
- `orchestrator/validators.py` — appended `validate_state_consistency()` function

### Key Function Added

```python
def validate_state_consistency(
    status: dict, checkpoint: dict, config: dict
) -> list[str]:
    """Validate consistency between STATUS.md, checkpoint.json, and workflow config.
    
    Checks:
    1. STATUS.md current_phase matches checkpoint current_phase
    2. checkpoint current_phase is in config phase_order
    3. All completed_phases exist in config phase_order
    4. STATUS.md current_state matches checkpoint current_state
    5. checkpoint current_state is a valid state in config states
    """
```

### Design Decisions

- Pure dict-based: takes parsed dicts, not file paths — caller reads files before calling
- Error format: `"State inconsistency: ..."` prefix for all messages
- All five checks from the spec implemented
- Test-first: wrote 6 tests before implementation

## Why It Matters

State consistency is the orchestrator's integrity check. Before advancing a workflow, the orchestrator must confirm that STATUS.md, checkpoint.json, and the workflow config agree on where the workflow is. If they disagree, the orchestrator could skip steps, repeat completed phases, or get stuck in an invalid state.

This validator catches:

- A STATUS.md that was manually edited out of sync with the checkpoint
- A corrupted checkpoint with a wrong phase or state
- A workflow config change that invalidates the current position
- Completed phases referencing steps that no longer exist in the workflow

## How It Works

The function takes three dicts and runs five independent checks. Each check appends a string error to the result list. If all pass, the list is empty (consistent).

### Data Flow

```
validate_state_consistency(status, checkpoint, config)
  → compare status["current_phase"] vs checkpoint["current_phase"]
  → check checkpoint["current_phase"] in config["phase_order"]
  → for each cp in checkpoint["completed_phases"]: cp in config["phase_order"]
  → compare status["current_state"] vs checkpoint["current_state"]
  → check checkpoint["current_state"] in config states
  → [] or [error strings]
```

### Check Details

| # | Check | Error if |
| --- | ------- | ---------- |
| 1 | Phase match | status != checkpoint |
| 2 | Phase exists | phase not in phase_order |
| 3 | Completed phases exist | any completed phase not in phase_order |
| 4 | State match | status != checkpoint |
| 5 | State exists | state not in config states |

### For Small Models

- Takes three dicts, returns a list of strings
- Five independent if-statements, no loops except for completed_phases
- Error messages always start with "State inconsistency: "
- All five must pass for result to be empty
- Any single failure returns at least one error

**Common mistakes to avoid:**

- Don't pass file paths — this function takes parsed dicts
- Don't forget to read the files before calling (use state_reader or json.load/yaml.safe_load)
- All five checks run regardless — don't short-circuit on first failure (caller sees all issues)

**What to check if something goes wrong:**

- `uv run pytest tests/test_validators.py -v` — 45 tests pass
- `uv run python -c "from orchestrator.validators import validate_state_consistency"` — import works
- STATUS.md fields must be `current_phase` and `current_state` (from `## Current Phase` / `## Current State`)
- Checkpoint fields must be lowercase with underscores: `current_phase`, `current_state`, `completed_phases`

---

# Educational Report: Phase 4d — Wire Validators into Orchestrator

## What Was Done

### Files Modified

- `orchestrator/orchestrator.py` — added validator imports and 3 integration points
- `tests/test_orchestrator_integration.py` — created with 4 integration tests

### Integration Points Added

**1. Import** — Added `validate_artifacts`, `validate_workflow_config`, `validate_state_consistency` to imports from `orchestrator.validators`.

**2. Config validation at startup** — After loading the workflow config, the orchestrator now calls `validate_workflow_config(config_path)`. If the config fails schema validation, the run is blocked at startup with an error log.

**3. Artifact validation after harness execution** — The simple status-based validation was replaced with a full `validate_artifacts()` call that checks expected output files exist, are non-empty, and contain required sections. Each validation failure is logged individually.

**4. State consistency before transition** — Before resolving the next state, the orchestrator now calls `validate_state_consistency(status, checkpoint, config)`. If STATUS.md and checkpoint.json disagree on phase/state, the run is blocked.

### Design Decisions

- Config validation is a gate at startup (fail fast)
- State consistency is a gate before transition (prevent corrupted workflow advancement)
- Artifact validation feeds into the validation dict used by state resolution (not a hard gate — failures affect transition conditions)
- Integration tests use temporary state directories to avoid fixture-dependency issues

## Why It Matters

Without this wiring, the validators are dead code. The orchestrator would accept invalid configs, skip artifact validation, and transition on inconsistent state. These three integration points ensure the entire validator suite is enforced during execution.

## How It Works

```
run() flow with validators:
  1. Load config
  1b. validate_workflow_config(config_path) → block if invalid
  2. Read state
  3. validate_checkpoint (existing)
  4-10. Execute step via harness
  11. validate_artifacts(state_dir, expected_outputs, config) → validation dict
  12b. validate_state_consistency(status, checkpoint, config) → block if inconsistent
  12. Resolve next state
  13-17. Update checkpoint, status, logs
```

### For Small Models

- Three `if` blocks added to run(), each calling a validator function
- Each returns a list of error strings — if non-empty, log and block
- validate_artifacts feeds into the existing validation dict (soft check for transitions)
- validate_workflow_config and validate_state_consistency are hard gates (block on failure)

**Common mistakes to avoid:**

- validate_workflow_config takes a file path (returns errors on bad YAML), not a parsed dict
- validate_state_consistency takes parsed dicts, not file paths
- validate_artifacts checks files on disk after harness writes them

**What to check if something goes wrong:**

- `uv run pytest tests/test_orchestrator_integration.py -v` — 4 integration tests pass
- `uv run pytest tests/ -q` — no regressions in existing tests
- Check that `orchestrator.orchestrator` has all three validator functions in its namespace
