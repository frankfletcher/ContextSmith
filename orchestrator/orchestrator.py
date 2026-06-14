"""Orchestrator main loop: executes workflow phases with state machine transitions."""

import json
import logging
import re
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
    EXIT_CONFIG_ERROR,
    EXIT_CONTINUE,
    EXIT_DONE,
    EXIT_INTERNAL_ERROR,
    EXIT_STATE_INCONSISTENCY,
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
from orchestrator.validators import (
    validate_append_only,
    validate_artifacts,
    validate_state_consistency,
    validate_workflow_config,
)

logger = logging.getLogger(__name__)

# Protected files that should never be overwritten, only appended to
PROTECTED_FILES = {
    "AUDIT_REPORT.md",
    "EDUCATIONAL_REPORT.md",
    "RESULT.json",
    "PHASE_LOG.md",
    "DECISIONS.md",
}

# Append-only files: orchestrator snapshots before dispatch,
# auto-repairs if overwritten by harness
APPEND_ONLY_FILES = {
    "EDUCATIONAL_REPORT.md",
    "AUDIT_REPORT.md",
    "PHASE_LOG.md",
    "DECISIONS.md",
}

# Snapshot storage: state_dir -> filename -> first N bytes
_append_snapshots: dict[str, dict[str, bytes]] = {}


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
        mode = "a"

    if mode == "w":
        path.write_text(content, encoding="utf-8")
    elif mode == "a":
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


def _rewrite_status_content(
    content: str,
    current_phase: str,
    next_state: str,
    current_subphase: str = "",
) -> str:
    """Rewrite STATUS.md section values while preserving file structure.

    If current_subphase is empty, removes the ## Current Sub-phase section
    entirely to avoid stale values after a phase transition.
    """
    replacement_by_section = {
        "Current Phase": current_phase,
        "Current State": next_state,
        "Next Action": f"Continue to {next_state}",
    }
    if current_subphase:
        replacement_by_section["Current Sub-phase"] = current_subphase

    in_section = None
    new_lines: list[str] = []
    skip_section = False

    for line in content.splitlines():
        if line.startswith("## "):
            in_section = line[3:].strip()
            if in_section == "Current Sub-phase" and not current_subphase:
                skip_section = True
                continue
            skip_section = False
            new_lines.append(line)
            continue

        if skip_section:
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


def _normalize_phase_name(name: str) -> str:
    """Strip phase numbering and labels for flexible matching."""
    cleaned = re.sub(
        r"^Phase\s+\d+[A-Z]?[:.]?\s*", "", name, flags=re.IGNORECASE
    ).strip()
    return cleaned


def _phase_name_matches(search: str, plan_name: str) -> bool:
    """Check if a search term matches a plan phase name.

    Tries direct substring match first, then normalized match
    (strips "Phase N:" prefix for comparison).
    """
    if search in plan_name or plan_name.startswith(search):
        return True
    norm_search = _normalize_phase_name(search)
    norm_plan = _normalize_phase_name(plan_name)
    if norm_search and norm_plan:
        return norm_search in norm_plan or norm_plan.startswith(norm_search)
    return False


def _find_phase_in_plan(plan: dict, phase_name: str) -> dict | None:
    """Find a phase in the plan by name, using multiple matching strategies."""
    if not phase_name or not plan:
        return None
    for phase in plan.get("phases", []):
        if _phase_name_matches(phase_name, phase.get("name", "")):
            return phase
    return None


def _find_first_subphase(plan: dict, phase_name: str) -> str:
    """Find the first pending sub-phase in a given phase."""
    phase = _find_phase_in_plan(plan, phase_name)
    if not phase:
        return ""
    for sp in phase.get("subphases", []):
        if sp.get("status") in ("pending", "in_progress"):
            return sp.get("name", "")
    return ""


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
        else EXIT_BLOCKED
        if next_state == "blocked"
        else EXIT_CONTINUE
    )


def _prepare_run_context(config_path: Path, state_dir: Path):
    """Load and validate config/state, returning context or an exit code."""
    try:
        config = _load_workflow_config(config_path)
    except Exception as e:
        logger.error(f"[orchestrator] Error loading config: {e}")
        return EXIT_CONFIG_ERROR

    if config_errors := validate_workflow_config(config_path):
        logger.error(f"[orchestrator] Config validation failed: {config_errors}")
        return EXIT_CONFIG_ERROR

    try:
        status, plan, context, checkpoint = _read_state_bundle(state_dir)
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"[orchestrator] Error reading state: {e}")
        return EXIT_STATE_INCONSISTENCY

    if checkpoint and (errors := validate_checkpoint(checkpoint, config)):
        logger.error(f"[orchestrator] State inconsistency: {errors}")
        return EXIT_STATE_INCONSISTENCY

    # Check for stale pre-dispatch marker (crash evidence)
    if checkpoint and checkpoint.get("pre_dispatch"):
        logger.warning(
            "[orchestrator] Pre-execution checkpoint found with pre_dispatch=true. "
            "Possible crash during agent dispatch. Check artifacts manually. "
            "Auto-recovery not implemented."
        )

    current_state = status.get("current_state", "init")
    current_phase = status.get("current_phase", "unknown")
    if current_state in TERMINAL_STATES:
        logger.info(f"[orchestrator] Already in terminal state: {current_state}")
        return _exit_code_for_state(current_state)

    return config, status, plan, context, checkpoint, current_state, current_phase


def _prepare_step_contract(
    current_state: str,
    config: dict,
    plan: dict,
    context: dict,
    current_subphase: str = "",
):
    """Compile step contract with state-specific validation."""
    try:
        return compile_step_contract(
            current_state, config, plan, context, current_subphase
        )
    except Exception as e:
        logger.error(f"[orchestrator] Error compiling step contract: {e}")
        return None


def _try_advance_subphase(
    state_dir: Path,
    plan: dict,
    status: dict,
    step_contract,
    config: dict,
    context: dict,
) -> int | None:
    """Advance to the next pending sub-phase in the current phase.

    Called after a successful execution. If the current phase has sub-phases
    and there are still pending ones, updates STATUS.md to point to the next
    sub-phase and returns EXIT_CONTINUE (skip state transition, same phase).

    If no sub-phases remain (all done) or no sub-phases defined, returns None
    so the caller proceeds with the normal state machine transition.

    Before advancing, checks each sub-phase's Dependency metadata. If a
    sub-phase depends on another that is not yet completed, it is skipped.

    Returns:
        EXIT_CONTINUE if advanced to next sub-phase.
        None if no more sub-phases (proceed with phase transition).
    """
    current_phase_name = status.get("current_phase", "")
    current_subphase = status.get("current_subphase", "")

    phase = _find_phase_in_plan(plan, current_phase_name)
    if not phase:
        logger.debug(f"[orchestrator] Phase '{current_phase_name}' not found in plan")
        return None

    subphases = phase.get("subphases", [])
    if not subphases:
        logger.debug(
            f"[orchestrator] Phase '{current_phase_name}' has no sub-phases "
            f"(flat format or legacy plan)"
        )
        return None

    idx = -1
    if current_subphase:
        for i, sp in enumerate(subphases):
            sp_name = sp.get("name", "")
            if current_subphase in sp_name or sp_name.startswith(current_subphase):
                idx = i
                break

    start = max(idx + 1, 0)
    for i in range(start, len(subphases)):
        sp = subphases[i]
        if sp.get("status") not in ("pending", "in_progress"):
            continue
        if not _check_subphase_dependency(subphases, sp):
            logger.info(
                f"[orchestrator] Skipping sub-phase '{sp.get('name')}': "
                f"unmet dependency '{sp.get('metadata', {}).get('Dependency', '?')}'"
            )
            continue

        sp_name = sp.get("name", "")
        step_contract.subphase_name = sp_name
        _update_status(
            state_dir,
            current_phase_name,
            status.get("current_state", ""),
            {"status": "pass"},
            current_subphase=sp_name,
        )
        _generate_next_prompt(
            state_dir,
            status.get("current_state", ""),
            step_contract,
            context,
            plan,
        )
        _write_phase_log(
            state_dir,
            status.get("current_state", ""),
            status.get("current_state", ""),
            {"status": "pass", "artifacts": [sp_name]},
            {"passed": True},
        )
        logger.info(f"[orchestrator] Advanced to sub-phase: {sp_name}")
        return EXIT_CONTINUE

    logger.info(
        f"[orchestrator] All sub-phases completed for phase '{current_phase_name}'"
    )
    return None


def _check_subphase_dependency(subphases: list, subphase: dict) -> bool:
    """Check if a sub-phase's dependency is completed.

    Returns True if no dependency declared (satisfied by default).
    Returns False if dependency exists but the target is not completed
    or not found in the plan.
    """
    dependency = subphase.get("metadata", {}).get("Dependency", "")
    if not dependency:
        return True
    for sp in subphases:
        sp_name = sp.get("name", "")
        if dependency in sp_name or sp_name.startswith(dependency):
            return sp.get("status") == "completed"
    return False


def _validate_state_for_dispatch(
    status: dict, checkpoint: dict | None, config: dict
) -> int | None:
    """Validate state consistency before dispatching to a harness.

    Returns None if valid, or an exit code if validation fails.
    """
    if checkpoint and (
        state_errors := validate_state_consistency(status, checkpoint, config)
    ):
        logger.error(f"[orchestrator] State consistency errors: {state_errors}")
        return EXIT_STATE_INCONSISTENCY
    return None


def _get_ready_adapter(harness: str):
    """Get a harness adapter and validate its execution environment."""
    try:
        adapter = _get_harness_adapter(harness)
    except KeyError as e:
        logger.error(f"[orchestrator] Harness not found: {e}")
        return None

    if env_errors := adapter.validate_environment():
        logger.error(f"[orchestrator] Harness environment errors: {env_errors}")
        return None

    return adapter


def _apply_runtime_options(
    step_contract, force: bool, test_mode: bool, fixture: Optional[str]
) -> None:
    """Apply CLI/runtime flags to step contract extra payload."""
    if force:
        step_contract.extra["force"] = True
    if test_mode:
        step_contract.extra["test_mode"] = True
    if fixture:
        step_contract.extra["fixture"] = fixture


def _snapshot_append_only_files(state_dir: Path) -> None:
    """Snapshot full content of append-only files before harness dispatch.

    Stores snapshots in _append_snapshots keyed by state_dir string.
    """
    snapshot_key = str(state_dir)
    _append_snapshots[snapshot_key] = {}
    for filename in APPEND_ONLY_FILES:
        path = state_dir / filename
        if path.exists():
            _append_snapshots[snapshot_key][filename] = path.read_bytes()


def _verify_and_repair_append_only_files(state_dir: Path) -> list[str]:
    """Verify append-only files were not overwritten. Auto-repair if they were.

    If the file was overwritten, prepend the full original content before the
    new content to restore the append-only contract.

    Returns list of repair actions taken (empty = all clean).
    """
    snapshot_key = str(state_dir)
    snapshots = _append_snapshots.pop(snapshot_key, {})
    if not snapshots:
        return []

    repairs = []
    for filename, original_content in snapshots.items():
        path = state_dir / filename
        original_prefix = original_content[:512]
        if not validate_append_only(path, original_prefix):
            # File was overwritten — prepend full original content back
            current_content = path.read_bytes()
            path.write_bytes(original_content + current_content)
            repairs.append(
                f"Repaired overwritten append-only file: {filename} "
                f"(prepended {len(original_content)} original bytes)"
            )
            logger.warning(
                f"[orchestrator] Append-only file {filename} was overwritten. "
                f"Prepending full original content ({len(original_content)} bytes)."
            )
    return repairs


def _apply_result_fallback(harness_result, step_contract, state_dir: Path) -> None:
    """Infer step status from artifact presence when RESULT.json is missing."""
    if harness_result.status not in ("", "unknown", "pending") and (
        harness_result.artifacts_written or (state_dir / "RESULT.json").exists()
    ):
        return
    expected = step_contract.expected_outputs
    all_present = all((state_dir / name).exists() for name in expected)
    if all_present and expected:
        harness_result.status = "pass"
        harness_result.reason = (
            "RESULT.json missing: inferred pass from artifact presence"
        )
    elif expected:
        missing = [n for n in expected if not (state_dir / n).exists()]
        harness_result.status = "fail"
        harness_result.reason = (
            f"RESULT.json missing: inferred fail from missing artifacts: {missing}"
        )
        harness_result.issues.append(harness_result.reason)
    else:
        harness_result.status = "fail"
        harness_result.reason = "RESULT.json missing: no artifacts written"
        harness_result.issues.append(harness_result.reason)
    logger.warning(
        f"[orchestrator] RESULT.json missing for step {step_contract.step_id} "
        f"— using artifact presence fallback. Status: {harness_result.status}"
    )


def _build_validation_strict(
    harness_passed: bool, file_validation: dict, all_failures: list
) -> dict:
    """Build validation result for strict mode."""
    return {
        "passed": harness_passed and file_validation["passed"],
        "failures": all_failures,
        "files_checked": file_validation["files_checked"],
        "files_passed": file_validation["files_passed"],
    }


def _build_validation_relaxed(
    harness_passed: bool, file_validation: dict, all_failures: list
) -> dict:
    """Build validation result for relaxed mode — warnings not blocks."""
    if not harness_passed:
        return {
            "passed": False,
            "failures": all_failures,
            "files_checked": file_validation["files_checked"],
            "files_passed": file_validation["files_passed"],
        }
    return {
        "passed": True,
        "failures": [],
        "files_checked": file_validation["files_checked"],
        "files_passed": file_validation["files_passed"],
    }


def _build_validation_none(harness_passed: bool) -> dict:
    """Build validation result for none mode — skip artifact checks entirely."""
    return {
        "passed": harness_passed,
        "failures": [],
        "files_checked": 0,
        "files_passed": 0,
    }


def _execute_and_validate_step(
    adapter, step_contract, state_dir: Path, current_state: str, config: dict
):
    """Execute the step via harness and build unified validation results.

    Respects step_contract.validation_mode:
    - strict (default): Block on any validation failure.
    - relaxed: Log warnings but pass if some artifacts exist.
    - none: Skip artifact validation entirely.
    """
    logger.info(f"[{current_state}] Dispatching to harness: {adapter.name}")
    logger.info(f"  Step: {step_contract.step_id}, state: {step_contract.state}")

    try:
        harness_result = adapter.execute(step_contract, state_dir)
        logger.info(f"[{current_state}] Harness result: {harness_result.status}")
    except Exception as e:
        logger.error(f"[{current_state}] Harness execution failed: {e}")
        return None

    _apply_result_fallback(harness_result, step_contract, state_dir)
    harness_passed = harness_result.status == "pass"
    validation_mode = getattr(step_contract, "validation_mode", "strict")

    if validation_mode == "none":
        logger.info(
            f"[{current_state}] Validation mode: none — skipping artifact check"
        )
        return harness_result, _build_validation_none(harness_passed)

    logger.info(f"[{current_state}] Validating artifacts...")
    file_validation = validate_artifacts(
        state_dir, step_contract.expected_outputs, config
    )
    all_failures = list(file_validation["failures"])
    all_failures.extend(harness_result.issues)

    if validation_mode == "relaxed":
        validation = _build_validation_relaxed(
            harness_passed, file_validation, all_failures
        )
        if all_failures:
            logger.warning(
                f"[{current_state}] Relaxed validation warnings: {all_failures}"
            )
    else:
        validation = _build_validation_strict(
            harness_passed, file_validation, all_failures
        )

    logger.info(
        f"[{current_state}] Validation: {'PASS' if validation['passed'] else 'FAIL'}"
    )
    if not validation["passed"]:
        for err in validation["failures"]:
            logger.warning(f"  - {err}")

    return harness_result, validation


def _resolve_transition(
    current_state: str,
    current_phase: str,
    checkpoint: dict | None,
    validation: dict,
    harness_result,
    config: dict,
):
    """Resolve next state and result payload from execution outcome."""
    counters = checkpoint.get("counters", {}) if checkpoint else {}
    result = {
        "status": "pass" if validation["passed"] else "fail",
        "artifacts": harness_result.artifacts_written,
        "validation_passed": validation["passed"],
    }
    next_state = resolve_next_state(
        current_state,
        current_phase,
        result,
        validation,
        config,
        counters,
    )
    return result, next_state


def _persist_transition(
    state_dir: Path,
    checkpoint: dict | None,
    config: dict,
    current_phase: str,
    current_state: str,
    next_state: str,
    result: dict,
    validation: dict,
    step_contract,
    context: dict,
    plan: dict,
) -> None:
    """Persist checkpoint and generated workflow artifacts after a transition."""
    checkpoint = (
        update_checkpoint(checkpoint, current_phase, current_state, next_state, result)
        if checkpoint
        else _build_initial_checkpoint(config, current_phase, next_state, result)
    )
    write_checkpoint(state_dir, checkpoint)

    _update_status(state_dir, current_phase, next_state, result)
    _write_phase_log(state_dir, current_state, next_state, result, validation)

    if next_state not in TERMINAL_STATES:
        first_sp = _find_first_subphase(plan, current_phase)
        if first_sp:
            step_contract.subphase_name = first_sp
            _update_status(
                state_dir, current_phase, next_state, result, current_subphase=first_sp
            )
        _generate_next_prompt(state_dir, next_state, step_contract, context, plan)


def _run_predispatch_checks(
    checkpoint, step_contract, current_phase, current_state, config, state_dir
) -> int | None:
    """Run pre-dispatch checks: counter limit and checkpoint-before-run.

    Returns an exit code if the dispatch should be skipped, or None to proceed.
    """
    if checkpoint:
        current_retries = (
            checkpoint.get("counters", {}).get(current_phase, {}).get("retries", 0)
        )
        if current_retries >= step_contract.max_retries:
            logger.info(
                f"[{current_state}] Max retries ({step_contract.max_retries}) reached"
                f" for {current_phase}. Transitioning to blocked."
            )
            return EXIT_BLOCKED

    if step_contract.checkpoint_before_run:
        _write_predispatch_checkpoint(
            checkpoint, config, current_phase, current_state, state_dir
        )
    return None


def _write_predispatch_checkpoint(
    checkpoint, config, current_phase, current_state, state_dir
) -> None:
    """Write a pre-dispatch checkpoint marker for crash evidence."""
    pre = checkpoint
    if pre is None:
        pre = _build_initial_checkpoint(
            config, current_phase, current_state, {"status": "pending"}
        )
    pre["pre_dispatch"] = True
    pre["pre_dispatch_at"] = (
        datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    )
    write_checkpoint(state_dir, pre)
    logger.info(
        f"[{current_state}] Pre-dispatch checkpoint written for {current_phase}"
    )


def _complete_step_flow(
    execution,
    current_state,
    current_phase,
    checkpoint,
    config,
    step_contract,
    context,
    state_dir,
    plan,
) -> int:
    """Resolve next state, persist artifacts, return exit code."""
    harness_result, validation = execution
    try:
        result, next_state = _resolve_transition(
            current_state,
            current_phase,
            checkpoint,
            validation,
            harness_result,
            config,
        )
    except Exception as e:
        logger.error(f"[{current_state}] Internal error during transition: {e}")
        return EXIT_INTERNAL_ERROR

    logger.info(f"[{current_state}] {harness_result.status} -> {next_state}")

    try:
        _persist_transition(
            state_dir,
            checkpoint,
            config,
            current_phase,
            current_state,
            next_state,
            result,
            validation,
            step_contract,
            context,
            plan,
        )
    except Exception as e:
        logger.error(f"[{current_state}] Internal error during persistence: {e}")
        return EXIT_INTERNAL_ERROR

    return _exit_code_for_state(next_state)


def _clear_predispatch_marker(step_contract, checkpoint, config, state_dir) -> None:
    """Clear the pre-dispatch marker after a caught exception."""
    if step_contract.checkpoint_before_run:
        pre = checkpoint
        if pre is None:
            pre = _build_initial_checkpoint(
                config, state_dir.name, "init", {"status": "error"}
            )
        pre["pre_dispatch"] = False
        write_checkpoint(state_dir, pre)


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
    prepared = _prepare_run_context(config_path, state_dir)
    if isinstance(prepared, int):
        return prepared

    config, status, plan, context, checkpoint, current_state, current_phase = prepared
    current_subphase = status.get("current_subphase", "")
    step_contract = _prepare_step_contract(
        current_state, config, plan, context, current_subphase
    )
    if step_contract is None:
        return EXIT_BLOCKED

    if step_contract.subphase_context_budget > 0:
        budget_k = step_contract.subphase_context_budget // 1000
        if step_contract.subphase_context_budget > 64000:
            logger.warning(
                f"[{current_state}] Sub-phase '{step_contract.subphase_name}' "
                f"budget ({budget_k}k) exceeds typical usable window (64k). "
                f"Consider splitting into smaller sub-phases."
            )
        else:
            logger.info(f"[{current_state}] Sub-phase budget: {budget_k}k")

    dispatch_validation = _validate_state_for_dispatch(status, checkpoint, config)
    if dispatch_validation is not None:
        return dispatch_validation

    _apply_runtime_options(step_contract, force, test_mode, fixture)

    if dry_run:
        _log_dry_run_step(current_state, current_phase, step_contract)
        return EXIT_CONTINUE

    code = _run_predispatch_checks(
        checkpoint, step_contract, current_phase, current_state, config, state_dir
    )
    if code is not None:
        return code

    adapter = _get_ready_adapter(harness)
    if adapter is None:
        return EXIT_BLOCKED

    step_contract.task_state_dir = str(state_dir)

    _snapshot_append_only_files(state_dir)

    try:
        execution = _execute_and_validate_step(
            adapter, step_contract, state_dir, current_state, config
        )
    except Exception as e:
        logger.error(f"[{current_state}] Internal error during execution: {e}")
        _clear_predispatch_marker(step_contract, checkpoint, config, state_dir)
        return EXIT_INTERNAL_ERROR

    for repair in _verify_and_repair_append_only_files(state_dir):
        logger.warning(f"[orchestrator] {repair}")

    if execution is None:
        return EXIT_BLOCKED

    harness_result, validation = execution
    if validation.get("passed", False):
        subphase_code = _try_advance_subphase(
            state_dir, plan, status, step_contract, config, context
        )
        if subphase_code is not None:
            return subphase_code

    return _complete_step_flow(
        execution,
        current_state,
        current_phase,
        checkpoint,
        config,
        step_contract,
        context,
        state_dir,
        plan,
    )


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
    register_signal_handlers(state_dir)
    if not quiet:
        logger.info(f"[orchestrator] Starting workflow: {config_path}")
        logger.info(f"[orchestrator] State directory: {state_dir}")
        logger.info(f"[orchestrator] Harness: {harness}")

    max_iterations = 1000
    for iteration in range(1, max_iterations + 1):
        if should_stop(state_dir):
            logger.info("[orchestrator] STOP file detected, halting")
            return EXIT_BLOCKED

        code = run(config_path, state_dir, harness=harness)
        if not quiet:
            logger.info(f"[orchestrator] Iteration {iteration}: exit code {code}")

        if code == EXIT_CONTINUE:
            continue
        return _finalize_workflow_exit(code, quiet)

    return _finalize_workflow_exit(EXIT_BLOCKED, quiet)


def _finalize_workflow_exit(code: int, quiet: bool) -> int:
    """Log and return the final workflow exit code."""
    messages = {
        EXIT_DONE: "[orchestrator] Workflow complete: done",
        EXIT_BLOCKED: "[orchestrator] Workflow blocked",
    }
    default = f"[orchestrator] Workflow error: exit code {code}"
    if not quiet:
        logger.info(messages.get(code, default))
    return code


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
    state_dir: Path,
    current_phase: str,
    next_state: str,
    result: dict,
    current_subphase: str = "",
) -> None:
    """Update STATUS.md with new state, preserving existing structure.

    Args:
        state_dir: Path to task state directory
        current_phase: Current phase identifier
        next_state: Next state machine state
        result: Step execution result
        current_subphase: Active sub-phase (or empty to leave unchanged)
    """
    status_path = state_dir / "STATUS.md"

    if status_path.exists():
        content = status_path.read_text(encoding="utf-8")
        content = _rewrite_status_content(
            content, current_phase, next_state, current_subphase
        )
    else:
        # Create new STATUS.md if it doesn't exist
        subphase_line = (
            f"\n## Current Sub-phase\n{current_subphase}" if current_subphase else ""
        )
        content = f"""# Status

## Current Phase
{current_phase}

## Current State
{next_state}{subphase_line}

## Progress
- Status: {result.get("status", "unknown")}

## Next Action
Continue to {next_state}

## Blocked By
none
"""

    _safe_write(status_path, content, "w")


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
        _safe_write(log_path, entry, "a")
    else:
        _safe_write(log_path, f"# Phase Log\n{entry}", "w")


def _generate_next_prompt(
    state_dir: Path,
    next_state: str,
    step_contract,
    context: dict,
    plan: dict | None = None,
) -> None:
    """Generate NEXT_PROMPT.md for the next agent.

    Args:
        state_dir: Path to task state directory
        next_state: Next state machine state
        step_contract: Current step contract
        context: Parsed context dict
        plan: Parsed plan dict (optional, used for sub-phase task lists)
    """
    prompt_path = state_dir / "NEXT_PROMPT.md"

    subphase_section = ""
    subphase_name = getattr(step_contract, "subphase_name", "")
    if subphase_name and plan:
        tasks = _find_subphase_tasks(plan, subphase_name)
        task_lines = "\n".join(
            f"  - [{'x' if t.get('done') else ' '}] {t.get('text', '')}" for t in tasks
        )
        subphase_section = f"""
## Sub-phase
{subphase_name}

## Sub-phase Tasks
{task_lines}
"""
    elif subphase_name:
        subphase_section = f"""
## Sub-phase
{subphase_name}
"""

    content = f"""# Next Prompt

You are continuing a workflow on {context.get("project", "unknown")}.

## Current Status
- Phase: {step_contract.step_id}
- State: {next_state}{f"\\n- Sub-phase: {subphase_name}" if subphase_name else ""}

## Your Task
Execute the next phase of the workflow.
{subphase_section}
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
- Run `markdownlint . --ignore node_modules` on any changed Markdown files

## Ralph Loop Enforcement

3 iterations required. Each is critique+fix. Do not skip or collapse.
1. **Critique** — Review against contract, find material defects, fix them
2. **Re-check** — After fixes, if no new defects → no-op; else fix
3. **Final check** — If no defects → no-op; do not invent changes
Each iteration needs a compact log entry in Ralph Summary.
Ralph loops are critique/revision, not repeated tool calls.

## Self-Audit
Before closeout, verify:
- Original phase goal satisfied or blocker recorded
- All validation commands executed or blocker documented
- Side-effect boundaries respected
- Task state updated with compact facts

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

## Hard Stop
Current phase is {step_contract.step_id}. Do not proceed beyond it.
Do not implement features outside this phase scope.
Do not edit files outside the current phase scope.

## Context
Continue from previous phase.
"""
    prompt_path.write_text(content, encoding="utf-8")


def _find_subphase_tasks(plan: dict, subphase_name: str) -> list[dict]:
    """Find the task list for a named sub-phase in the plan."""
    for phase in plan.get("phases", []):
        for sp in phase.get("subphases", []):
            if subphase_name in sp.get("name", ""):
                return sp.get("tasks", [])
    return []
