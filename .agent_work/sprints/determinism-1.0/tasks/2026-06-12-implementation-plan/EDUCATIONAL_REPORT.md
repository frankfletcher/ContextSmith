# Educational Report: Phase 3 — Harness Adapters

## What Was Done

Phase 3 implemented the harness adapter layer, which bridges the orchestrator and the agent execution runtime. Four files were created:

### 1. `orchestrator/adapters/base.py` (144 lines)
- **StepContract** dataclass: bounded step definition with step_id, state, agent_profile, permissions, inputs, expected_outputs, timeout_s, max_retries, and optional fields
- **HarnessResult** dataclass: structured result with status, reason, artifacts, validation, issues, next_action
- **HarnessAdapter** ABC: abstract base class with name, validate_environment(), execute(), cancel(), get_capabilities()
- **HarnessRegistry** class: adapter discovery and registration with register(), get(), list_available(), _detect_auto()
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

**Adapters register at import time**: This allows the registry to discover adapters without explicit registration calls. The __init__.py maintains a manifest (ADAPTER_REGISTRY) and imports all listed modules.

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
- `HarnessRegistry` — class-level registry with register(), get(), list_available(), _detect_auto()
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
