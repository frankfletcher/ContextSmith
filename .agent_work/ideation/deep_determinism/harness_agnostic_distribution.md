# Harness-Agnostic Distribution and Targeted Harness Adapters

This note describes how ContextSmith can stay harness-agnostic while still delivering best-in-class behavior on specific harnesses like OpenCode.

The main idea is to keep the core system universal and move harness-specific behavior into optional adapters, references, and install targets.

## Design Goal

We want one system that:

- works for users on different shells and operating systems
- runs without assuming Bash exists
- can target specific harnesses when the runtime is known
- avoids bloating every skill with every harness detail
- keeps the core workflow model stable across environments

## What Is Universal

These parts should be shared across all harnesses:

- workflow state model: `TASK.md`, `PLAN.md`, `STATUS.md`, `CONTEXT.md`, `CHECKLIST.md`, `AUDIT_REPORT.md`, `EDUCATIONAL_REPORT.md`, `SUMMARY.md`, `NEXT_PROMPT.md`
- orchestrator logic: step selection, retries, checkpoints, transitions
- workflow config schema: baseline steps, required gates, validation shape
- agent result schema: status, artifacts, validation, next action
- validation logic: schema checks, required-file checks, output checks
- skill metadata format: `SKILL.md` frontmatter and reference manifests
- Python-first command execution and file operations
- portable path handling and subprocess calls

These pieces should behave the same no matter which harness is in use.

## What Is Harness-Specific

These parts should vary by harness:

- how agents are launched
- how permissions are expressed
- how max steps are enforced
- how commands are invoked
- how custom agents or subagents are declared
- how tools and plugins are wired in
- how harness-specific references are loaded

OpenCode is one example. Another harness may use a different agent format, permission model, or launch mechanism.

## Python First, Not Bash First

Bash is useful on Unix-like systems, but it is not universal. Windows users may not have Bash available by default.

So the system should prefer Python for:

- orchestrator entrypoints
- validation scripts
- file checks
- process launching
- portable command execution

Python gives us one runtime story across Windows, macOS, and Linux.

Example:

```python
from pathlib import Path
from subprocess import run

root = Path.cwd()
result = run(
    ["python", "scripts/validate_skills.py"],
    cwd=root,
    capture_output=True,
    text=True,
    check=False,
)
```

If shell commands are needed, they should be wrapped in Python and kept optional.

## Harness Adapter Model

Think of the system as two layers:

1. a universal core
2. a harness adapter

The core owns the workflow contract. The adapter translates that contract into harness-native behavior.

### Core Responsibilities

- read and validate workflow state
- choose the next step
- build a bounded launch packet
- validate outputs
- write checkpoints
- resume after interruption

### Adapter Responsibilities

- map a generic step to a harness-specific agent/profile
- translate permissions into harness syntax
- invoke the harness runtime
- expose harness-specific tools or plugins when available
- report structured results back to the orchestrator

## OpenCode As A Target Adapter

OpenCode gets special handling only where it adds value:

- custom agents in `.opencode/agents/`
- commands in `.opencode/commands/`
- tools in `.opencode/tools/`
- plugins in `.opencode/plugins/`

The core workflow should not depend on these files existing.
If the run is on OpenCode, the adapter can use them.
If not, the core still works with a generic launch path.

Example:

```text
generic step -> orchestrator -> adapter -> harness runtime
OpenCode step -> orchestrator -> OpenCode adapter -> @contextsmith-auditor
```

## Distribution Model

### 1. Generic distribution

Ship a core package that works without any harness-specific extras.

Contains:

- orchestrator
- schemas
- validation scripts
- universal references
- generic agent/task-state docs

Good for:

- users who want the workflow model but not a specific harness
- CI or automation environments
- future harnesses not yet supported directly

### 2. Harness-specific extras

Ship optional packages or install targets for specific harnesses.

Contains:

- OpenCode agent definitions
- OpenCode command files
- OpenCode tool/plugin snippets
- harness-specific reference files

Good for:

- users already on that harness
- harness-native best practices
- richer permissions and launch behavior

Example install shape:

```text
contextsmith
contextsmith[opencode]
contextsmith[harness-agnostic]
```

The exact packaging mechanism can vary, but the principle stays the same: core first, adapters optional.

## Conditional Reference Loading

Skills should not be bloated with every harness reference by default.

Instead:

- load only universal references for all runs
- load harness-specific references only when the selected harness matches
- optionally load harness-specific references when the projected output target is that harness

That keeps context small and avoids confusing the model with irrelevant runtime details.

### Loading Rule

Load harness-specific references only when one of these is true:

- the skill is running on that harness
- the artifact being created will be used on that harness
- the user explicitly requests that harness

Example policy:

```yaml
references:
  - shared/documentation-quality.md
  - shared/control-parameters.md

conditional_references:
  opencode:
    when: harness == "opencode" or target == "opencode"
    files:
      - shared/harness-opencode.md
      - skills/contextsmith-run/references/harness-opencode.md
```

## Skill Packaging Strategy

Skills should be split into:

- universal skill logic
- optional harness appendix files
- manifest rules for conditional loading

This avoids copying harness-specific details into every skill file.

Preferred pattern:

```text
skills/contextsmith-run/
  SKILL.md
  references/
    core.md
    harness-opencode.md   # loaded conditionally
```

The skill remains portable. The harness appendix is only pulled in when relevant.

## Example Agent Selection Flow

```text
1. Orchestrator reads workflow config.
2. Orchestrator detects the current harness.
3. Core skill loads universal references.
4. Harness adapter loads optional harness references.
5. Orchestrator resolves the agent profile.
6. Harness launches the agent.
7. Validation runs through portable Python scripts.
```

## Why This Works Well

- universal logic stays small and portable
- harness adapters can be optimized without polluting the core
- Python avoids shell portability problems
- users get better harness-native behavior when available
- users on other harnesses still get a complete working system

## OpenCode Example

If the selected harness is OpenCode, the system can load:

- `shared/harness-opencode.md`
- `skills/<skill>/references/harness-opencode.md`
- `.opencode/agents/contextsmith-*.md`
- `.opencode/commands/contextsmith-*.md`

If the harness is not OpenCode, none of those files should be required for the core workflow to work.

## Practical Rule Set

1. The orchestrator is universal.
2. The workflow config is universal.
3. Validation is universal.
4. The harness adapter is optional and isolated.
5. Python is the default runtime for orchestration and validation.
6. Bash is only an optional convenience layer.
7. Harness-specific references are conditional, not always-on.
8. The generic distribution must work without harness extras.
9. Harness-specific distributions can add better defaults without changing the core model.

## Related Notes

- `system_components.md` for the full component map
- `agent_start_and_communication.md` for runtime messaging
- `communications_protocol_sketch.md` for protocol envelopes
- `shared/harness-opencode.md` for OpenCode-specific runtime patterns

---

## Adapter Base Class (Concrete Specification)

Every harness adapter must implement `HarnessAdapter` from `orchestrator_and_harness.md`. Below is the concrete contract every adapter must satisfy.

### Required Methods

```python
class HarnessAdapter(ABC):
    """All harness adapters must implement these five methods."""

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique short name. Used in workflow config's `harness` field.
        Must match ^[a-z0-9_-]+$.
        Examples: "opencode", "generic", "acp"
        """
        ...

    @abstractmethod
    def validate_environment(self) -> list[str]:
        """
        Check if this harness can run in the current environment.
        Return [] if ready. Return [error messages] if not.
        Called during startup to select the correct adapter.
        """
        ...

    @abstractmethod
    def execute(self, contract: StepContract, state_dir: Path) -> HarnessResult:
        """
        Execute one bounded step.

        CONTRACT:
        - Must raise HarnessTimeoutError if timeout_s is exceeded.
        - Must raise HarnessExecutionError if the harness runtime itself fails.
        - Must never raise for agent-level failures (use HarnessResult.status).
        - Must collect ALL files in contract.expected_outputs from state_dir.
        - Must write result artifacts to state_dir (not a temp location).
        - Must be thread-safe if the adapter is used concurrently.
        - Must not modify checkpoint.json (orchestrator owns this).
        - Caller (orchestrator) may call cancel() from another thread.
        """
        ...

    @abstractmethod
    def cancel(self, step_id: str) -> bool:
        """
        Cancel a running step execution.

        Returns True if the step was successfully cancelled.
        Returns False if the step could not be cancelled (already done, unknown step_id).
        Must be safe to call even if no step is running.
        Must not raise exceptions.
        """
        ...

    @abstractmethod
    def get_capabilities(self) -> dict:
        """
        Declare what this harness supports.

        Standard capability keys:
        - supports_model_pinning: bool (can pin to a specific model)
        - supports_step_caps: bool (can limit tool calls)
        - supports_permission_levels: bool (can enforce read-only/edit/external)
        - max_concurrent_steps: int (default 1)
        - supports_structured_output: bool (can return structured agent output)
        - supports_cancellation: bool (can cancel running steps)
        """
        ...
```

### Registration

Adapters register themselves at import time:

```python
# In adapters/opencode.py
class OpenCodeAdapter(HarnessAdapter):
    @property
    def name(self) -> str:
        return "opencode"

    # ... implement all methods ...

# Register at module level
HarnessRegistry.register(OpenCodeAdapter)
```

### Discovery Path

The orchestrator discovers adapters by scanning:

```
adapters/
├── opencode.py        # name = "opencode"
├── generic.py         # name = "generic"
└── __init__.py        # imports all adapters listed in ADAPTER_REGISTRY
```

The `adapters/__init__.py` maintains a manifest:

```python
# adapters/__init__.py
# Add new adapters here to register them with the orchestrator.
ADAPTER_REGISTRY = [
    "opencode",  # adapters/opencode.py
    "generic",   # adapters/generic.py
]

def discover_adapters() -> None:
    """Import all registered adapters to trigger their HarnessRegistry.register() calls."""
    for name in ADAPTER_REGISTRY:
        importlib.import_module(f"adapters.{name}")
```

---

## Adapter Lifecycle

Each adapter goes through these states during a workflow run:

```
REGISTERED → DISCOVERED → VALIDATED → EXECUTING → COMPLETED
                                         ↓
                                      ERROR → FAILED
```

| Phase | What Happens | When |
|-------|-------------|------|
| REGISTERED | `HarnessRegistry.register(AdapterClass)` called | At import time |
| DISCOVERED | `HarnessRegistry.get(name)` or `_detect_auto()` called | At orchestrator startup |
| VALIDATED | `adapter.validate_environment()` called | After discovery, must return [] |
| EXECUTING | `adapter.execute(contract, dir)` called | Per step |
| COMPLETED | Adapter returns `HarnessResult` | After each step |
| ERROR | `HarnessTimeoutError` or `HarnessExecutionError` raised | During execution |
| FAILED | After max retries or unrecoverable error | No more execution |

### Lifecycle Rules

1. Once VALIDATED, an adapter instance is reused for all steps in a workflow run.
2. The orchestrator does not re-validate the environment between steps.
3. After ERROR, the orchestrator may retry the same step (new `execute()` call) or block.
4. After FAILED, the adapter is not called again (orchestrator exits with code 1).
5. `cancel()` may be called at any time from EXECUTING state.

---

## Reference Loading Protocol

When the orchestrator or harness loads skill references, it follows this protocol:

### Loading Order

```
1. Universal references (always loaded, no conditions)
   - shared/documentation-quality.md
   - shared/control-parameters-core.md
   - shared/loop-safety.md
   - shared/git-safety.md (if coding project)

2. Domain-specific references (loaded if domain matches)
   - domain: coding → shared/coding-standards.md
   - domain: data-science → shared/domain-profiles/data-science-ml.md
   - domain: documentation → shared/documentation-quality.md

3. Harness-specific references (loaded only for the active harness)
   - harness: opencode → shared/harness-opencode.md
   - harness: acp → shared/harness-acp.md

4. Workflow-specific references (loaded from workflow config metadata)
   - metadata.references → [list of additional references]
```

### Reference Location

```
shared/
├── documentation-quality.md       # universal
├── control-parameters-core.md     # universal
├── loop-safety.md                 # universal
├── git-safety.md                  # coding domain
├── coding-standards.md            # coding domain
├── harness-opencode.md            # opencode harness
├── harness-acp.md                 # acp harness
├── domain-profiles/
│   ├── data-science-ml.md
│   └── ...
└── skills/
    ├── contextsmith-run/
    │   └── references/
    │       ├── harness-opencode.md  # skill-specific harness appendix
    │       └── ...
    └── ...
```

### Conditional Loading Rule

Load harness-specific references only when `workflow_config.harness == "opencode"` (or matching harness name). Never load references for harnesses that are not active. This keeps context size small for the orchestrator.

---

## Adding a New Harness Adapter: Step-by-Step

```
1. Create adapters/<name>.py
2. Implement HarnessAdapter with all required methods
3. Register with HarnessRegistry.register()
4. Add to adapters/__init__.py ADAPTER_REGISTRY
5. Create harness-specific reference files in shared/harness-<name>.md
6. Add conditional loading rule to reference loading logic
7. Add harness name to workflow_config.schema.json enum for `harness` field
8. Test: adapter.validate_environment() returns [] on target system
9. Test: adapter.execute() returns valid HarnessResult with real or mock agent
10. Test: adapter.cancel() returns True when step is running
11. Test: adapter raises HarnessTimeoutError when timeout is exceeded
```

## Generic Adapter (Default Fallback)

The `generic` adapter is always available. It does not launch an external agent runtime. Instead, it:

1. Reads the `NEXT_PROMPT.md` from the step contract
2. Writes the prompt to a `.pending_prompt.md` file in the task-state directory
3. If `--test-mode` is active, loads a fixture response from the fixture file and writes expected artifacts
4. If `--await-human` is active, waits for the user to write a `.human_response.md` file, then treats it as the agent output
5. Reads `RESULT.json` from the state directory if present
6. Returns `HarnessResult` with artifact validation results

This lets the orchestrator run in environments without OpenCode or any other agent harness. Human operators can execute the steps manually using the `.pending_prompt.md` file, or tests can inject fixture responses.

```python
class GenericAdapter(HarnessAdapter):
    @property
    def name(self) -> str:
        return "generic"

    def validate_environment(self) -> list[str]:
        return []  # always available

    def execute(self, contract: StepContract, state_dir: Path) -> HarnessResult:
        prompt_path = Path(state_dir) / ".pending_prompt.md"
        prompt_path.write_text(self._load_prompt(contract))

        if contract.extra.get("test_mode"):
            return self._run_test_mode(contract, state_dir)
        if contract.extra.get("await_human"):
            return self._await_human(contract, state_dir)

        # Read RESULT.json if present (agent or human wrote it)
        result_file = Path(state_dir) / "RESULT.json"
        envelope = None
        if result_file.exists():
            try:
                envelope = json.loads(result_file.read_text())
            except (json.JSONDecodeError, OSError):
                pass

        # Collect existing artifacts
        artifacts = self._collect_existing(contract, state_dir)

        if envelope:
            status = envelope.get("status", "pass")
            reason = envelope.get("reason", "")
            issues = envelope.get("issues", [])
            next_action = envelope.get("next_action", "done")
        else:
            status = "pass" if len(artifacts) == len(contract.expected_outputs) else "fail"
            reason = "generic adapter: no agent runtime, checked existing artifacts"
            issues = [] if artifacts else ["no agent runtime available, no artifacts found"]
            next_action = "done"

        return HarnessResult(
            status=status,
            step_id=contract.step_id,
            reason=reason,
            artifacts={},
            artifacts_written=list(artifacts.keys()),
            validation={"files_found": len(artifacts), "expected": len(contract.expected_outputs)},
            issues=issues,
            next_action=next_action,
        )
```
