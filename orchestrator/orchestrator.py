"""Orchestrator main loop: executes workflow phases with state machine transitions."""

import json
import logging
import signal
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from orchestrator.adapters import discover_adapters
from orchestrator.adapters.base import HarnessRegistry
from orchestrator.checkpoint import (
    read_checkpoint,
    update_checkpoint,
    validate_checkpoint,
    write_checkpoint,
)
from orchestrator.constants import (
    EXIT_BLOCKED,
    EXIT_CONTINUE,
    EXIT_DONE,
    TERMINAL_STATES,
)
from orchestrator.state_reader import (
    read_context,
    read_plan,
    read_status,
)
from orchestrator.step_compiler import (
    compile_step_contract,
    resolve_next_state,
)

logger = logging.getLogger(__name__)

# Protected files that should never be overwritten, only appended to
PROTECTED_FILES = {
    "AUDIT_REPORT.md",
    "EDUCATIONAL_REPORT.md",
    "RESULT.json",
    "PHASE_LOG.md",  # Append-only by design
}


def _is_protected_file(filename: str) -> bool:
    """Check if a file is protected from overwrites."""
    return filename in PROTECTED_FILES


def _safe_write(path: Path, content: str, mode: str = "w") -> None:
    """Write to a file with protection for report files.

    For protected files, always append. For other files, use the specified mode.

    Args:
        path: File path to write to
        content: Content to write
        mode: Write mode ('w' for write, 'a' for append)
    """
    if _is_protected_file(path.name) and mode == "w":
        # Protected files should only be appended to
        mode = "a"

    path.write_text(content, encoding="utf-8") if mode == "w" else None
    if mode == "a":
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)


def _log_dry_run_step(current_state: str, current_phase: str, step_contract) -> None:
    """Log the next step details for dry-run execution."""
    logger.info("[orchestrator] DRY RUN: Next step")
    logger.info(f"  State: {current_state}")
    logger.info(f"  Phase: {current_phase}")
    logger.info(f"  Step ID: {step_contract.step_id}")
    logger.info(f"  Agent: {step_contract.agent_profile}")
    logger.info(f"  Permissions: {step_contract.permissions}")
    logger.info(f"  Expected outputs: {step_contract.expected_outputs}")


def _rewrite_status_content(content: str, current_phase: str, next_state: str) -> str:
    """Rewrite STATUS.md section values while preserving file structure."""
    replacement_by_section = {
        "Current Phase": current_phase,
        "Current State": next_state,
        "Next Action": f"Continue to {next_state}",
    }

    in_section = None
    new_lines: list[str] = []

    for line in content.splitlines():
        if line.startswith("## "):
            in_section = line[3:].strip()
            new_lines.append(line)
            continue

        if (
            in_section in replacement_by_section
            and line.strip()
            and not line.startswith("#")
        ):
            new_lines.append(replacement_by_section[in_section])
            continue

        new_lines.append(line)

    return "\n".join(new_lines)


def _load_workflow_config(config_path: Path) -> dict:
    """Load workflow config from JSON or YAML."""
    with open(config_path, "r", encoding="utf-8") as f:
        if config_path.suffix in {".yaml", ".yml"}:
            if not YAML_AVAILABLE:
                raise RuntimeError("PyYAML not installed, cannot load YAML")
            return yaml.safe_load(f)
        return json.load(f)


def _read_state_bundle(state_dir: Path) -> tuple[dict, dict, dict, dict | None]:
    """Read status, plan, context, and optional checkpoint from state dir."""
    status = read_status(state_dir)
    plan = read_plan(state_dir)
    context = read_context(state_dir)
    checkpoint = read_checkpoint(state_dir, required=False)
    return status, plan, context, checkpoint


def _get_harness_adapter(harness: str):
    """Discover and return the requested harness adapter."""
    discover_adapters()
    return HarnessRegistry.get(harness)


def _build_initial_checkpoint(
    config: dict,
    current_phase: str,
    next_state: str,
    result: dict,
) -> dict:
    """Create an initial checkpoint payload when one does not exist."""
    return {
        "workflow_id": config.get("workflow_id", "unknown"),
        "version": 1,
        "current_phase": current_phase,
        "current_state": next_state,
        "last_updated": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "completed_phases": [],
        "counters": {current_phase: {"retries": 0, "ralph_cycles": 0}},
        "last_result": result,
    }


def _exit_code_for_state(next_state: str) -> int:
    """Map state machine next state to orchestrator exit code."""
    return (
        EXIT_DONE
        if next_state == "done"
        else EXIT_BLOCKED if next_state == "blocked" else EXIT_CONTINUE
    )


def run(
    config_path: str,
    state_dir: str,
    harness: str = "generic",
    dry_run: bool = False,
    force: bool = False,
    test_mode: bool = False,
    fixture: Optional[str] = None,
) -> int:
    """Execute one phase transition. Returns exit code (0=done, 1=blocked, 2=continue).

    Args:
        config_path: Path to workflow config file
        state_dir: Path to task state directory
        harness: Harness adapter name (default: generic)
        dry_run: If True, print next step without executing
        force: If True, allow re-running completed phases
        test_mode: If True, use mock harness responses
        fixture: Path to test fixture file (requires test_mode)

    Returns:
        Exit code: EXIT_DONE (0), EXIT_BLOCKED (1), or EXIT_CONTINUE (2)
    """
    config_path = Path(config_path)
    state_dir = Path(state_dir)
    _ = (force, test_mode, fixture)

    # 1. Load workflow config
    try:
        config = _load_workflow_config(config_path)
    except Exception as e:
        logger.error(f"[orchestrator] Error loading config: {e}")
        return EXIT_BLOCKED

    # 2. Read state
    try:
        status, plan, context, checkpoint = _read_state_bundle(state_dir)
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"[orchestrator] Error reading state: {e}")
        return EXIT_BLOCKED

    # 3. Validate state consistency
    if checkpoint and (errors := validate_checkpoint(checkpoint, config)):
        logger.error(f"[orchestrator] State inconsistency: {errors}")
        return EXIT_BLOCKED

    # 4. Determine current state
    current_state = status.get("current_state", "init")
    current_phase = status.get("current_phase", "unknown")

    if current_state in TERMINAL_STATES:
        logger.info(f"[orchestrator] Already in terminal state: {current_state}")
        return EXIT_DONE if current_state == "done" else EXIT_BLOCKED

    # 5. Compile step contract
    try:
        step_contract = compile_step_contract(current_state, config, plan, context)
    except Exception as e:
        logger.error(f"[orchestrator] Error compiling step contract: {e}")
        return EXIT_BLOCKED

    # 6. Dry run: print next step and return
    if dry_run:
        _log_dry_run_step(current_state, current_phase, step_contract)
        return EXIT_CONTINUE

    # 7. Discover adapters and get the requested harness
    try:
        adapter = _get_harness_adapter(harness)
    except KeyError as e:
        logger.error(f"[orchestrator] Harness not found: {e}")
        return EXIT_BLOCKED

    # 8. Validate harness environment
    if env_errors := adapter.validate_environment():
        logger.error(f"[orchestrator] Harness environment errors: {env_errors}")
        return EXIT_BLOCKED

    # 9. Set task_state_dir on contract
    step_contract.task_state_dir = str(state_dir)

    # 10. Dispatch to harness adapter
    logger.info(f"[{current_state}] Dispatching to harness: {harness}")
    logger.info(f"  Step: {step_contract.step_id}, state: {step_contract.state}")

    try:
        harness_result = adapter.execute(step_contract, state_dir)
        logger.info(f"[{current_state}] Harness result: {harness_result.status}")
    except Exception as e:
        logger.error(f"[{current_state}] Harness execution failed: {e}")
        return EXIT_BLOCKED

    # 11. Validate result
    logger.info(f"[{current_state}] Validating artifacts...")
    validation = {
        "passed": harness_result.status == "pass",
        "failures": harness_result.issues,
    }
    logger.info(
        f"[{current_state}] Validation: {'PASS' if validation['passed'] else 'FAIL'}"
    )

    # 12. Resolve next state
    counters = checkpoint.get("counters", {}) if checkpoint else {}
    result = {
        "status": harness_result.status,
        "artifacts": harness_result.artifacts_written,
        "validation_passed": validation["passed"],
    }
    next_state = resolve_next_state(
        current_state, current_phase, result, validation, config, counters
    )
    logger.info(f"[{current_state}] {harness_result.status} -> {next_state}")

    # 13. Update checkpoint
    checkpoint = (
        update_checkpoint(checkpoint, current_phase, current_state, next_state, result)
        if checkpoint
        else _build_initial_checkpoint(config, current_phase, next_state, result)
    )

    write_checkpoint(state_dir, checkpoint)

    # 14. Update STATUS.md
    _update_status(state_dir, current_phase, next_state, result)

    # 15. Write PHASE_LOG.md entry
    _write_phase_log(state_dir, current_state, next_state, result, validation)

    # 16. Generate NEXT_PROMPT.md if continuing
    if next_state not in TERMINAL_STATES:
        _generate_next_prompt(state_dir, next_state, step_contract, context)

    # 17. Return exit code
    return _exit_code_for_state(next_state)


def run_workflow(
    config_path: str,
    state_dir: str,
    harness: str = "generic",
    verbose: bool = False,
    quiet: bool = False,
) -> int:
    """Run workflow to completion. Returns final exit code.

    Args:
        config_path: Path to workflow config file
        state_dir: Path to task state directory
        harness: Harness adapter name (default: generic)
        verbose: If True, print detailed progress
        quiet: If True, suppress output

    Returns:
        Final exit code: EXIT_DONE (0), EXIT_BLOCKED (1), or error code
    """
    # Register signal handlers
    register_signal_handlers(state_dir)

    if not quiet:
        logger.info(f"[orchestrator] Starting workflow: {config_path}")
        logger.info(f"[orchestrator] State directory: {state_dir}")
        logger.info(f"[orchestrator] Harness: {harness}")

    iteration = 0
    max_iterations = 1000  # Safety limit

    while iteration < max_iterations:
        iteration += 1

        # Check for STOP file
        if should_stop(state_dir):
            if not quiet:
                logger.info(
                    "[orchestrator] STOP file detected, halting after current phase"
                )
            return EXIT_BLOCKED

        # Execute one step
        code = run(config_path, state_dir, harness=harness)

        if not quiet:
            logger.info(f"[orchestrator] Iteration {iteration}: exit code {code}")

        if code == EXIT_CONTINUE:
            continue
        elif code == EXIT_DONE:
            if not quiet:
                logger.info("[orchestrator] Workflow complete: done")
            return EXIT_DONE
        elif code == EXIT_BLOCKED:
            if not quiet:
                logger.info("[orchestrator] Workflow blocked")
            return EXIT_BLOCKED
        else:
            # Error codes 3-5
            if not quiet:
                logger.info(f"[orchestrator] Workflow error: exit code {code}")
            return code

    # Safety limit reached
    if not quiet:
        logger.info(f"[orchestrator] Safety limit reached: {max_iterations} iterations")
    return EXIT_BLOCKED


def should_stop(state_dir: str) -> bool:
    """Check if STOP file exists. Returns True if should stop.

    Args:
        state_dir: Path to task state directory

    Returns:
        True if .STOP file exists, False otherwise
    """
    stop_file = Path(state_dir) / ".STOP"
    if stop_file.exists():
        stop_file.unlink()  # Consume the signal
        return True
    return False


def register_signal_handlers(state_dir: str) -> None:
    """Register SIGINT handler for clean shutdown on Ctrl-C.

    Args:
        state_dir: Path to task state directory
    """

    def handle_interrupt(signum, frame):
        logger.warning("\n[orchestrator] Interrupted, writing checkpoint...")
        # Checkpoint is already written after each step, so just exit
        sys.exit(EXIT_BLOCKED)

    signal.signal(signal.SIGINT, handle_interrupt)


def _update_status(
    state_dir: Path, current_phase: str, next_state: str, result: dict
) -> None:
    """Update STATUS.md with new state, preserving existing structure.

    Args:
        state_dir: Path to task state directory
        current_phase: Current phase identifier
        next_state: Next state machine state
        result: Step execution result
    """
    status_path = state_dir / "STATUS.md"

    if status_path.exists():
        content = status_path.read_text(encoding="utf-8")
        content = _rewrite_status_content(content, current_phase, next_state)
    else:
        # Create new STATUS.md if it doesn't exist
        content = f"""# Status

## Current Phase
{current_phase}

## Current State
{next_state}

## Progress
- Status: {result.get("status", "unknown")}

## Next Action
Continue to {next_state}

## Blocked By
none
"""

    status_path.write_text(content, encoding="utf-8")


def _write_phase_log(
    state_dir: Path,
    from_state: str,
    to_state: str,
    result: dict,
    validation: dict,
) -> None:
    """Append entry to PHASE_LOG.md.

    Args:
        state_dir: Path to task state directory
        from_state: Previous state
        to_state: Next state
        result: Step execution result
        validation: Validation result
    """
    log_path = state_dir / "PHASE_LOG.md"
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    entry = f"""
## Phase {from_state} -> {to_state}
Date: {timestamp}
State: {from_state} -> {to_state}
Action: Execute phase
Result: {result.get("status", "unknown")}
Validation: {"PASS" if validation.get("passed") else "FAIL"}
Artifacts: {", ".join(result.get("artifacts", []))}
"""

    # PHASE_LOG.md is append-only by design
    if log_path.exists():
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(entry)
    else:
        log_path.write_text(f"# Phase Log\n{entry}", encoding="utf-8")


def _generate_next_prompt(
    state_dir: Path,
    next_state: str,
    step_contract,
    context: dict,
) -> None:
    """Generate NEXT_PROMPT.md for the next agent.

    Args:
        state_dir: Path to task state directory
        next_state: Next state machine state
        step_contract: Current step contract
        context: Parsed context dict
    """
    prompt_path = state_dir / "NEXT_PROMPT.md"
    content = f"""# Next Prompt

You are continuing a workflow on {context.get("project", "unknown")}.

## Current Status
- Phase: {step_contract.step_id}
- State: {next_state}

## Your Task
Execute the next phase of the workflow.

## Input Files
- STATUS.md: Current workflow state
- PLAN.md: Phase plan
- CONTEXT.md: Project context

## Output Requirements
- Update STATUS.md with results
- Write artifacts to disk
- Update PHASE_LOG.md

## Constraints
- Follow the step contract
- Validate outputs
- Write structured results

## Context
Continue from previous phase.
"""
    prompt_path.write_text(content, encoding="utf-8")
