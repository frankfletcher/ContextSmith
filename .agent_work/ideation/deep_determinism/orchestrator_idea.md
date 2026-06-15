# Orchestrator Idea

## Problem Statement

Agent-driven workflows are non-deterministic. The model forgets steps, gets cut off, and spends tokens re-deriving its own control flow. That control flow should live in code. OpenCode should be the execution substrate, not the workflow brain.

## Goal

- Deterministic execution: every action item completes or produces a clear error
- Token reduction: remove orchestration from prompts and reference material
- Resilience: retry and resume after interruptions without losing state
- Simplicity: give the agent one bounded task at a time

## System Model

Four layers:

1. **Router** - ContextSmith skill that interprets user intent, generates/loads a workflow config, and calls the orchestrator. The user stays in OpenCode.
2. **Orchestrator** - Python state machine that owns workflow state, transitions, retries, and checkpoints. Has the outer loop built in (`run_workflow`).
3. **Harness** - Executes one bounded step with permissions, tools, and validation hooks. Launches agents as subprocesses.
4. **Artifacts** - task-state files, validation outputs, and phase closeouts that make the run resumable.

The user never leaves OpenCode. The router skill is the human interface. The orchestrator is the control plane. The harness is the execution boundary.

Baseline workflow shape should live in YAML or JSON config, with agent-generated plans acting as overlays that can add or remove optional steps but cannot redefine the required workflow on their own.

## Execution Flow

1. User invokes the router skill in OpenCode (e.g., `/contextsmith` or natural language).
2. Router interprets intent and generates/loads a workflow config YAML.
3. Router calls `python -m orchestrator <config> <state_dir>` via bash tool.
4. Orchestrator runs the outer loop (`run_workflow`): loads state, compiles step contract, dispatches to harness, validates result, transitions state, repeats.
5. Agent output streams to the user in real-time (stdout is not captured).
6. Agent writes structured result to `RESULT.json` on disk (not stdout).
7. Orchestrator reads `RESULT.json` and artifact presence to determine next state.
8. User can interrupt at any time via Ctrl-C (clean shutdown with checkpoint) or STOP file (finish current phase, then stop).
9. On completion or blocking, orchestrator exits and router presents results to the user.

## Responsibilities

### Router

- interprets user intent
- generates or loads workflow config
- calls the orchestrator via bash tool
- presents results to the user
- lives in OpenCode as a skill

### Orchestrator

- owns workflow graph
- owns retry policy
- owns checkpoint timing
- owns loop detection
- owns resume semantics
- streams progress to stdout for user visibility
- checks for interrupt signals (Ctrl-C, STOP file)

### Harness

- enforces permissions
- limits step count
- invokes agents and tools
- runs validation hooks
- blocks bad operations before execution
- lets agent output stream to user (does not capture stdout)
- reads structured result from RESULT.json on disk

### Agent

- completes one bounded task
- writes artifacts to known files
- does not decide the workflow shape

## OpenCode Role

OpenCode is the user's environment. The user stays in OpenCode throughout. The router skill lives in OpenCode and calls the orchestrator as a tool. OpenCode agents are the leaf executors that the harness invokes for each bounded step.

- **Agent profiles** map to states like audit, fix, review, migrate
- **Permissions** define what the model can touch
- **Step caps** keep one invocation from looping forever
- **Custom tools** can enforce gates, but do not replace the orchestrator
- **Plugins** can validate edits and preserve state across compaction
- **Commands** are launchers, not control flow
- **Router skill** is the user's entry point — it calls the orchestrator

## Failure Model

- Agent invocation failure -> retry with backoff
- Structural validation failure -> retry the same state
- Review failure -> transition to a fix/retry state
- Loop detection failure -> abort with a clear error
- Missing checkpoint or task-state file -> stop and request recovery

## Design Rule

If a behavior can be enforced in code, put it in the orchestrator.
If a behavior is about model permissions, put it in the harness agent profile.
If a behavior is about blocking tool misuse, put it in a plugin or custom tool.

## Next Implementation Slice

**Prerequisites:** Before any code, write the JSON schemas listed in `implementation_prerequisites.md` section 2. The orchestrator cannot validate configs or artifacts without them.

- define baseline workflow config schema (YAML/JSON) → `schemas/workflow_config.schema.json`
- define workflow DSL
- define task-state contract
- define OpenCode agent profiles
- define validator registry
- define checkpoint format
- define resume semantics from `NEXT_PROMPT.md`
- define audit and Ralph loop state machine ([audit_and_ralph_state_machine.md](audit_and_ralph_state_machine.md))
- define communications protocol between orchestrator, harness, and agent ([communications_protocol_sketch.md](communications_protocol_sketch.md))

---

## Orchestrator State Machine

The orchestrator runs a deterministic state machine. Every phase of every workflow is one of these states. The orchestrator reads the current state from STATUS.md and transitions according to the workflow config's state machine definition.

### Canonical States

| State | Purpose | Agent Role | Validates? | Terminal? |
| ------- | --------- | ----------- | ------------ | ----------- |
| `init` | Load config, validate task state, check prerequisites | none (orchestrator-internal) | Yes (schema) | No |
| `plan` | Generate or update the phase plan | contextsmith-planner | Yes (checklist schema) | No |
| `execute` | Run the primary action (edit, create, migrate) | contextsmith-builder | Yes (output schema) | No |
| `audit` | Review outputs for structural and semantic correctness | contextsmith-auditor | Yes (audit schema) | No |
| `fix` | Repair issues found during audit | contextsmith-builder | No (delegates to audit) | No |
| `validate` | Run automated checks (schema, commands, file presence) | validator script | Yes (pass/fail) | No |
| `ralph_critique` | Run structured critique of draft outputs | contextsmith-auditor | Yes (critique schema) | No |
| `ralph_revise` | Revise based on critique | contextsmith-builder | No (delegates to critique) | No |
| `closeout` | Write summary, checkpoint, next prompt | contextsmith-closer | Yes (closeout schema) | No |
| `done` | Workflow completed successfully | none | No | Yes |
| `blocked` | Workflow cannot continue without intervention | none | No | Yes |

### State Transitions

Each state declares its valid exits. The orchestrator enforces these — the agent cannot change state.

```
init
  └── on config valid → plan
  └── on config invalid → blocked

plan
  └── on plan valid → execute
  └── on plan invalid → plan (retry, up to N)
  └── on max retries → blocked

execute
  └── on output valid → audit (if audit required) | validate (if no audit)
  └── on output invalid → execute (retry)
  └── on max retries → blocked

audit
  └── on pass → validate (if validate required) | ralph_critique (if ralph enabled) | closeout
  └── on fail → fix (if fix state defined) | execute (retry phase, if no fix state)
  └── on unstructured output → audit (retry)

fix
  └── on fix complete → audit (always routes back to verify)
  └── note: some workflows skip fix entirely and route audit fail → execute (retry)

validate
  └── on pass → ralph_critique (if ralph enabled) | closeout
  └── on fail → execute (retry phase) | fix
  └── on max retries → blocked

ralph_critique
  └── on pass and max_cycles reached → closeout
  └── on pass and max_cycles not reached → ralph_revise
  └── on fail → ralph_revise (even on fail, revise happens)
  └── on max_cycles exceeded → blocked

ralph_revise
  └── always → ralph_critique (loop counter increments here)

closeout
  └── on closeout valid → done
  └── on closeout invalid → closeout (retry)
```

### Transition Decision Logic

The orchestrator decides which transition to take based on:

1. **Current state** — read from STATUS.md `current_phase` field
2. **Step result** — the structured result from the harness (status, validation, issues)
3. **Workflow config** — the baseline config defines which states are required, which are optional, and which gates must pass
4. **Retry counters** — tracked in checkpoint.json, per-state retry budget

Decision pseudocode:

```
function next_state(current_state, step_result, config, counters):
    valid_transitions = config.states[current_state].transitions

    for transition in valid_transitions:
        if matches_condition(transition.condition, step_result):
            if transition.target == "retry-same-state" and counters[current_state] >= config.max_retries:
                return "blocked"
            return transition.target

    return "blocked"  # no matching transition → blocked
```

### State Configuration in Workflow Config

Each state in the workflow config declares:

```yaml
states:
  execute:
    agent: contextsmith-builder
    permissions: edit
    max_retries: 3
    timeout_s: 600
    transitions:

      - condition: output_valid

        target: audit

      - condition: output_invalid

        target: execute

      - condition: max_retries

        target: blocked
    expected_outputs:

      - ARTIFACTS.md
      - PHASE_LOG.md

  audit:
    agent: contextsmith-auditor
    permissions: read-only
    max_retries: 2
    timeout_s: 300
    transitions:

      - condition: pass

        target: closeout

      - condition: fail

        target: fix

      - condition: unstructured

        target: audit
```

---

## Orchestrator Main Loop

The orchestrator is invoked as a Python function. It does not stay running between steps — it executes one phase transition per call, then returns an exit code. The outer loop is a Python runner that calls the orchestrator repeatedly until the workflow reaches a terminal state.

**The outer loop must be pure code (no LLM, no agent).** An LLM managing the outer loop would reintroduce the non-determinism the orchestrator exists to prevent.

### Outer Loop (Python Runner)

```python
import sys
from orchestrator import run as orchestrator_run

EXIT_DONE = 0
EXIT_BLOCKED = 1
EXIT_CONTINUE = 2

def run_workflow(config_path: str, state_dir: str) -> int:
    """Run a workflow to completion. Returns the final exit code."""

    # Register signal handlers for clean shutdown on Ctrl-C
    register_signal_handlers(state_dir)

    while True:

        # Check for STOP file (user wants to stop after current phase)
        if should_stop(state_dir):
            print("[orchestrator] STOP file detected, halting after current phase")
            return EXIT_BLOCKED

        code = orchestrator_run(config_path, state_dir)

        if code == EXIT_CONTINUE:
            continue  # next step ready, loop again
        elif code == EXIT_DONE:
            return EXIT_DONE
        elif code == EXIT_BLOCKED:
            return EXIT_BLOCKED
        else:

            # Exit codes 3-5 are errors, not retryable
            return code

def should_stop(state_dir: str) -> bool:
    """Check if a STOP file exists in the state directory."""
    stop_file = Path(state_dir) / ".STOP"
    if stop_file.exists():
        stop_file.unlink()  # consume the signal
        return True
    return False

def register_signal_handlers(state_dir: str):
    """Register SIGINT handler for clean shutdown on Ctrl-C."""
    import signal
    def handle_interrupt(signum, frame):
        print("\n[orchestrator] Interrupted, writing checkpoint...")

        # checkpoint is already written after each step, so just exit
        sys.exit(EXIT_BLOCKED)
    signal.signal(signal.SIGINT, handle_interrupt)

if __name__ == "__main__":
    sys.exit(run_workflow(sys.argv[1], sys.argv[2]))
```

### Inner Loop (Single Step)

Each call to `orchestrator_run` does exactly one phase transition. The orchestrator prints progress to stdout (which streams to the user via the router). Agent output also streams to stdout — the harness does not capture it.

```
function orchestrator_main(config_path, state_dir):

    # 1. Load state
    config = load_workflow_config(config_path)
    status = read_status(state_dir / "STATUS.md")
    plan = read_plan(state_dir / "PLAN.md")
    context = read_context(state_dir / "CONTEXT.md")
    checkpoint = read_checkpoint(state_dir / "checkpoint.json")

    # 2. Validate current state is consistent
    if not validate_state_consistency(status, checkpoint, config):
        write_error(state_dir, "state_inconsistency")
        return EXIT_BLOCKED

    # 3. Determine current state
    current_state = status.current_phase

    if current_state in config.terminal_states:
        return EXIT_DONE

    # 4. Compile step contract
    step_contract = compile_step_contract(current_state, config, plan, context)

    # 5. Dispatch to harness
    print(f"[{current_state}] Dispatching to {step_contract.agent_profile}...")
    harness = resolve_harness(config.harness)
    result = harness.execute(step_contract, state_dir)

    # 6. Validate result
    if not result.structured:
        result = HarnessResult(status="fail", reason="unstructured_output")

    validation = run_validators(result, config.states[current_state].expected_outputs, state_dir)

    # 7. Decide next state
    next_state = resolve_next_state(current_state, result, validation, config, checkpoint.counters)
    print(f"[{current_state}] {result.status} -> {next_state}")

    # 8. Update state
    checkpoint = update_checkpoint(checkpoint, current_state, next_state, result)
    write_checkpoint(state_dir / "checkpoint.json", checkpoint)
    update_status(state_dir / "STATUS.md", next_state, result)
    write_phase_log(state_dir / "PHASE_LOG.md", current_state, next_state, result, validation)

    # 9. Generate next prompt if continuing
    if next_state not in config.terminal_states:
        generate_next_prompt(state_dir, next_state, step_contract, context)

    return EXIT_CONTINUE if next_state not in config.terminal_states else EXIT_DONE
```

### Exit Codes

| Code | Meaning | Next Action |
| ------ | --------- | ------------- |
| 0 | Workflow complete (terminal state reached) | Done |
| 1 | Workflow blocked (cannot continue) | Human intervention required |
| 2 | Step completed, next step ready | Re-invoke orchestrator (loop) |
| 3 | Config validation error | Fix config and re-run |
| 4 | State inconsistency (checkpoint/status mismatch) | Manual repair or `--repair` flag |
| 5 | Internal error (unexpected exception) | Check logs |

---

## CLI Interface

The orchestrator is a Python package. It is called by the router skill, not directly by the user. The user stays in OpenCode; the router calls the orchestrator as a bash tool.

```
python -m orchestrator <config> <state_dir> [options]

positional arguments:
  config                Path to workflow config file (YAML or JSON)
  state_dir             Task-state directory

optional arguments:
  --harness <name>      Harness adapter to use (default: auto-detect)
  --single-step         Run one phase transition and exit (for debugging)
  --dry-run             Print next step without executing
  --repair              Attempt to repair state inconsistency
  --force               Allow re-running a completed phase
  --test-mode           Use mock harness responses (for testing)
  --fixture <file>      Test fixture file (requires --test-mode)
  --verbose             Forward agent stdout to user (default: on)
  --quiet               Only orchestrator progress, no agent output
```

When called without `--single-step`, the orchestrator runs the full workflow to completion (done, blocked, or error). The `--single-step` flag runs exactly one phase transition and exits — useful for debugging.

The orchestrator streams progress to stdout. Agent output also streams to stdout (the harness does not capture it). The user sees everything in real-time in their OpenCode terminal.

Subcommands:

```
contextsmith init [--harness <name>]
    Create .contextsmith/ with default configs and harness adapter stubs.

contextsmith validate [--state <dir>]
    Validate task-state artifacts against schemas. No execution.

contextsmith inspect <state-dir>
    Read-only display of current workflow state.

contextsmith diff <run-a> <run-b>
    Compare two workflow runs phase by phase.

contextsmith resume <state-dir> [--decision <file>]
    Resume a blocked workflow, optionally with a human decision file.
```

---

## Checkpoint Format

The checkpoint file (`checkpoint.json`) is the orchestrator's source of truth for crash recovery. It is written AFTER a phase completes and BEFORE the next phase begins.

```
{
  "workflow_id": "runtime-enforcement",
  "version": 1,
  "run_id": "550e8400-e29b-41d4-a716-446655440000",
  "workflow_start": "2026-06-10T14:30:00Z",
  "last_updated": "2026-06-10T15:45:00Z",

  "current_phase": "audit-03",
  "current_state": "audit",
  "phase_started": "2026-06-10T15:30:00Z",

  "completed_phases": [
    {"phase": "init", "state": "done", "completed_at": "2026-06-10T14:31:00Z"},
    {"phase": "plan-01", "state": "done", "completed_at": "2026-06-10T14:35:00Z"},
    {"phase": "execute-02", "state": "done", "completed_at": "2026-06-10T15:30:00Z"}
  ],

  "counters": {
    "audit-03": {"retries": 1, "ralph_cycles": 0},
    "execute-02": {"retries": 0, "ralph_cycles": 0}
  },

  "last_result": {
    "state": "audit",
    "status": "fail",
    "reason": "validation_failed",
    "artifacts_written": ["audit.md", "PHASE_LOG.md", "CHECKLIST.md"],
    "validation_passed": false
  },

  "errors": [
    {"phase": "audit-03", "attempt": 1, "error": "missing_evidence", "timestamp": "2026-06-10T15:45:00Z"}
  ],

  "metadata": {
    "harness": "opencode",
    "model_profile": "qwen36",
    "agent_version": "1.0.0"
  }
}
```

### Checkpoint Fields

| Field | Type | Required | Description |
| ------- | ------ | ---------- | ------------- |
| workflow_id | string | yes | Matches workflow config |
| version | int | yes | Schema version (must match config) |
| run_id | UUID | yes | Unique run identifier |
| workflow_start | ISO 8601 | yes | When the workflow started |
| last_updated | ISO 8601 | yes | When this checkpoint was written |
| current_phase | string | yes | Phase identifier (e.g., "audit-03") |
| current_state | string | yes | State machine state name |
| phase_started | ISO 8601 | yes | When current phase started |
| completed_phases | array | yes | Ordered list of completed phases |
| counters | object | yes | Per-phase retry and cycle counters |
| last_result | object | yes | Most recent phase execution result |
| errors | array | yes | All errors encountered (append-only) |
| metadata | object | no | Environment/context metadata |

---

## Startup Procedure

When invoked with `contextsmith run <config> --state <dir>`:

```
Step 1: Validate config

  - Read workflow config file
  - Validate against workflow_config.schema.json
  - If invalid → print errors, exit code 3

Step 2: Validate state directory exists

  - If --state dir does not exist → create it with default task-state files
  - If --state dir exists → proceed

Step 3: Check for checkpoint.json

  - If checkpoint.json exists → this is a resume → go to Resume Procedure
  - If no checkpoint.json → this is a fresh start

Step 4: Fresh start initialization

  - Read STATUS.md → get current_phase
  - If STATUS.md does not exist or is empty → write initial STATUS.md with state = "init"
  - If PLAN.md does not exist → state = "plan" (generate plan first)
  - If PLAN.md exists → state = first execution phase from plan

Step 5: Validate state consistency

  - STATUS.md current_phase must be a valid state in the workflow config
  - If valid → enter main loop
  - If invalid → exit code 4 (state inconsistency)

Step 6: Enter main loop

  - run_workflow() calls orchestrator run() in a while loop
  - On exit code 2 → call run() again (loop)
  - On exit codes 0, 1, 3, 4, 5 → return that code
```

---

## Resume Procedure

When checkpoint.json exists at startup:

```
Step 1: Load checkpoint.json

  - Parse and validate checkpoint fields
  - If checkpoint is corrupted or schema-invalid → exit code 4

Step 2: Detect interruption

  - Compare checkpoint.last_updated with STATUS.md last_modified
  - If checkpoint.last_updated is older → phase was interrupted
  - If checkpoint.last_result.status == "in_progress" → phase was interrupted

Step 3: Determine resume action

  - If last completed phase == current_phase → phase was fully done, advance to next
  - If last_result.status == "fail" and retries < max → retry current phase
  - If last_result.status == "fail" and retries >= max → blocked
  - If last_result.validation_passed == false → retry validation
  - If last_result.status == "in_progress" → retry from start of phase

Step 4: Validate artifact state

  - Check that artifacts listed in checkpoint.last_result.artifacts_written exist on disk
  - If artifacts are missing → log warning, treat phase as incomplete regardless of checkpoint

Step 5: Re-enter main loop

  - STATUS.md is updated to reflect resume decision
  - Orchestrator proceeds from determined state
```

### Resume Decision Table

| Checkpoint State | Artifacts Present | Action |
| ----------------- | ------------------- | -------- |
| Phase marked done | All expected exist | Advance to next phase |
| Phase marked done | Some missing | Re-run phase (partial write) |
| Phase failed, retries remain | Any | Retry phase |
| Phase failed, no retries | Any | Blocked |
| Phase in progress | None | Re-run from start |
| Phase in progress | Some exist | Re-run from start (reject partial) |

---

## Error Handling Matrix

| Error | Detection | Orchestrator Response | Exit Code |
| ------- | ----------- | ---------------------- | ----------- |
| Config file not found | FileNotFoundError | Print error, stop | 3 |
| Config schema invalid | jsonschema.exceptions.ValidationError | Print validation errors, stop | 3 |
| State directory missing | os.path.isdir() returns False | Create directory, continue | 2 |
| STATUS.md missing | FileNotFoundError | Write default STATUS.md, continue | 2 |
| STATUS.md malformed | Parse failure | Exit with state inconsistency | 4 |
| Checkpoint.json corrupted | JSON decode failure or schema mismatch | Log error, treat as fresh start (--repair needed) | 4 |
| Harness not found | ImportError | Print available harnesses, stop | 5 |
| Harness execution timeout | subprocess.TimeoutExpired | Log timeout, mark phase as failed | 2 |
| Harness returns non-JSON | JSON decode failure | Treat as unstructured output, retry | 2 |
| Agent writes 0 of N artifacts | File not found after execution | Mark phase as failed | 2 |
| Agent writes N of N artifacts but some are empty | os.path.getsize() returns 0 | Log warning, validate content | 2 |
| Step cap exceeded | Harness reports step_cap_reached | Treat as incomplete, retry with stricter controls | 2 |
| Orchestrator internal exception | Any unhandled Exception | Log traceback, exit with code 5 | 5 |
| Disk full during checkpoint write | IOError | Log critical error, previous checkpoint intact | 5 |
| Two orchestrator processes on same state dir | Checkpoint locked | Second process exits with "already running" error | 5 |
| Human escalation timeout (24h) | Timer expiry | Mark phase as stale, exit blocked | 1 |
| User Ctrl-C | SIGINT caught | Write checkpoint, exit blocked | 1 |
| STOP file present | File check between phases | Write checkpoint, exit blocked | 1 |

---

## orchestrator.py Function Reference

### Public API (called by CLI)

```
orchestrator.run_workflow(config_path, state_dir, harness=None, verbose=False, quiet=False)
    → int (exit code)
    Runs the full workflow loop. Calls run() repeatedly until terminal state.
    This is the primary entry point for `contextsmith run`.

orchestrator.run(config_path, state_dir, harness=None, dry_run=False, force=False, test_mode=False, fixture=None)
    → int (exit code)
    Executes ONE phase transition and returns. Called by run_workflow().
    Use --single-step flag or call directly for debugging.

orchestrator.init(state_dir, harness=None)
    → None

orchestrator.validate(state_dir)
    → List[str] (validation errors, empty = valid)

orchestrator.inspect(state_dir)
    → dict (workflow state summary)

orchestrator.diff(run_a_dir, run_b_dir)
    → str (diff text)

orchestrator.resume(state_dir, decision_file=None)
    → int (exit code)

orchestrator.should_stop(state_dir) -> bool
    Check for STOP file, consume it if found.

orchestrator.register_signal_handlers(state_dir) -> None
    Register SIGINT handler for clean shutdown on Ctrl-C.
```

### Internal Functions (used by run)

```
_load_config(path) → dict
    Read and validate workflow config.

_read_status(dir) → dict
    Parse STATUS.md into structured dict.

_read_checkpoint(dir) → dict | None
    Read checkpoint.json, return None if missing.

_write_checkpoint(dir, checkpoint_data) → None
    Atomic write (write to temp, rename).

_compile_step_contract(state_name, config, plan, context) → StepContract
    Merge config defaults with plan overlays.

_resolve_harness(name) → HarnessAdapter
    Import and instantiate harness adapter.

_run_validators(result, expected_outputs, state_dir) → ValidationResult
    Check file presence, schemas, commands.

_resolve_next_state(current, result, validation, config, counters) → str
    Apply transition rules from config.

_update_status(dir, next_state, result) → None
    Rewrite STATUS.md with new state.

_write_phase_log(dir, from_state, to_state, result, validation) → None
    Append entry to PHASE_LOG.md.

_generate_next_prompt(dir, next_state, contract, context) → None
    Write NEXT_PROMPT.md for the next agent.
```

### StepContract Data Structure

(See `orchestrator_and_harness.md` for the canonical Python dataclass definition. The JSON representation below is for reference.)

```
{
  "step_id": str,
  "state": str,
  "agent_profile": str,
  "permissions": "read-only" | "edit" | "external-action",
  "inputs": [str],          # file paths relative to state_dir
  "expected_outputs": [str], # file paths relative to state_dir
  "timeout_s": int,
  "max_retries": int,
  "ralph_max_cycles": int,
  "validation_mode": "strict" | "relaxed" | "none",
  "model_pin": str | None,
  "checkpoint_before_run": bool,
  "prompt_template": str | None  # override NEXT_PROMPT.md if set
}
```

### ValidationResult Data Structure

```
{
  "passed": bool,
  "schema_valid": bool,
  "command_exit_codes": {str: int},  # command → exit code
  "file_checks": {str: bool},         # file → exists
  "content_checks": {str: bool},      # check name → passed
  "failures": [str],                  # human-readable failure messages
  "warnings": [str]
}
```

---

## Integration With Other Components

### Harness

The orchestrator calls `harness.execute(step_contract, state_dir)` and receives a `HarnessResult`. The harness is resolved by name from a registry. The OpenCode adapter is the default. See `communications_protocol_sketch.md` for message formats and `orchestrator_and_harness.md` for the interface contract.

### Validators

Validators run after the harness returns. They check:

1. Expected files exist (`os.path.exists`)
2. Files are non-empty (`os.path.getsize > 0`)
3. JSON/YAML files match their schema
4. Any commands specified in the step contract return exit code 0
5. Regex content checks where specified

Validators are Python functions registered in `scripts/validators/`. Each validator takes `(state_dir, step_contract)` and returns `ValidationResult`.

### Task-Artifact Contract

The orchestrator reads and writes these files in the state directory:

- `STATUS.md` — must contain `## Current Phase` with the phase name and `## Next Action` with the next state
- `PLAN.md` — must contain `## Phases` with checkboxes
- `CONTEXT.md` — must contain `## File Map` and `## Constraints`
- `CHECKLIST.md` — must contain `## Checklist` with `- [x]` and `- [ ]` items
- `PHASE_LOG.md` — append-only log with `## Phase <name>` sections
- `NEXT_PROMPT.md` — the bounded prompt for the next agent

See `state_artifact_strategy.md` for exact required sections per file.
