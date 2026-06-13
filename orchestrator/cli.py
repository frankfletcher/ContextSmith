"""CLI interface for the orchestrator.

Provides command-line argument parsing and subcommand dispatch for running
workflows, inspecting state, validating artifacts, and managing workflow runs.
"""

import argparse
import json
import sys
from pathlib import Path

from orchestrator.checkpoint import read_checkpoint, validate_checkpoint
from orchestrator.orchestrator import run, run_workflow
from orchestrator.state_reader import read_context, read_plan, read_status


def _print_phase_log_diff(content_a: str, content_b: str) -> None:
    """Print a compact phase-log diff summary and first differing lines."""
    print("Phase logs differ:")
    lines_a = content_a.splitlines()
    lines_b = content_b.splitlines()

    print(f"\nRun A: {len(lines_a)} lines")
    print(f"Run B: {len(lines_b)} lines")

    max_lines = min(len(lines_a), len(lines_b), 20)
    for i in range(max_lines):
        if lines_a[i] != lines_b[i]:
            print(f"\nLine {i + 1} differs:")
            print(f"  A: {lines_a[i]}")
            print(f"  B: {lines_b[i]}")


def main():
    """CLI entry point. Parse args and dispatch to appropriate function."""
    parser = argparse.ArgumentParser(
        prog="orchestrator",
        description="Execute deterministic workflows with state machine transitions",
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Default command: run workflow
    parser.add_argument(
        "config", nargs="?", help="Path to workflow config file (YAML or JSON)"
    )
    parser.add_argument("state_dir", nargs="?", help="Task-state directory")
    parser.add_argument(
        "--harness", default="generic", help="Harness adapter to use (default: generic)"
    )
    parser.add_argument(
        "--single-step", action="store_true", help="Run one phase transition and exit"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print next step without executing"
    )
    parser.add_argument(
        "--repair", action="store_true", help="Attempt to repair state inconsistency"
    )
    parser.add_argument(
        "--force", action="store_true", help="Allow re-running a completed phase"
    )
    parser.add_argument(
        "--test-mode", action="store_true", help="Use mock harness responses"
    )
    parser.add_argument("--fixture", help="Test fixture file (requires --test-mode)")
    parser.add_argument(
        "--verbose", action="store_true", help="Forward agent stdout to user"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only orchestrator progress, no agent output",
    )

    # init subcommand
    init_parser = subparsers.add_parser(
        "init", help="Create .contextsmith/ with default configs"
    )
    init_parser.add_argument(
        "--harness", default="generic", help="Harness adapter to use"
    )

    # validate subcommand
    validate_parser = subparsers.add_parser(
        "validate", help="Validate task-state artifacts"
    )
    validate_parser.add_argument("--state", required=True, help="Task-state directory")

    # inspect subcommand
    inspect_parser = subparsers.add_parser(
        "inspect", help="Display current workflow state"
    )
    inspect_parser.add_argument("path", help="Task-state directory")

    # diff subcommand
    diff_parser = subparsers.add_parser("diff", help="Compare two workflow runs")
    diff_parser.add_argument("path_a", help="First run state directory")
    diff_parser.add_argument("path_b", help="Second run state directory")

    # resume subcommand
    resume_parser = subparsers.add_parser("resume", help="Resume a blocked workflow")
    resume_parser.add_argument("path", help="Task-state directory")
    resume_parser.add_argument("--decision", help="Human decision file")

    args = parser.parse_args()

    # Dispatch to appropriate function
    if args.command == "init":
        return cmd_init(args)
    elif args.command == "validate":
        return cmd_validate(args)
    elif args.command == "inspect":
        return cmd_inspect(args)
    elif args.command == "diff":
        return cmd_diff(args)
    elif args.command == "resume":
        return cmd_resume(args)
    elif args.config and args.state_dir:
        # Default command: run workflow
        return cmd_run(args)
    else:
        parser.print_help()
        return 1


def cmd_run(args):
    """Run workflow or single step."""
    if args.single_step:
        return run(
            config_path=args.config,
            state_dir=args.state_dir,
            harness=args.harness,
            dry_run=args.dry_run,
            force=args.force,
            test_mode=args.test_mode,
            fixture=args.fixture,
        )
    else:
        return run_workflow(
            config_path=args.config,
            state_dir=args.state_dir,
            harness=args.harness,
            verbose=args.verbose,
            quiet=args.quiet,
        )


def cmd_init(args):
    """Create .contextsmith/ with default configs."""
    contextsmith_dir = Path(".contextsmith")
    contextsmith_dir.mkdir(exist_ok=True)

    # Create default workflow config
    config = {
        "workflow_id": "default-workflow",
        "version": 1,
        "states": {
            "execute": {
                "agent": "contextsmith-builder",
                "permissions": "edit",
                "max_retries": 3,
                "transitions": [
                    {"condition": "output_valid", "target": "audit"},
                    {"condition": "output_invalid", "target": "execute"},
                    {"condition": "max_retries", "target": "blocked"},
                ],
            },
            "audit": {
                "agent": "contextsmith-auditor",
                "permissions": "read-only",
                "max_retries": 2,
                "transitions": [
                    {"condition": "pass", "target": "done"},
                    {"condition": "fail", "target": "execute"},
                ],
            },
            "done": {
                "agent": "none",
                "permissions": "read-only",
                "transitions": [],
            },
            "blocked": {
                "agent": "none",
                "permissions": "read-only",
                "transitions": [],
            },
        },
    }

    config_path = contextsmith_dir / "workflow.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print(f"Created {config_path}")
    print(f"Harness: {args.harness}")
    return 0


def _validate_required_files(state_dir: Path) -> list[str]:
    """Check required task-state files exist."""
    errors = []
    errors.extend(
        f"Missing required file: {filename}"
        for filename in ["STATUS.md", "PLAN.md", "CONTEXT.md"]
        if not (state_dir / filename).exists()
    )
    return errors


def _validate_checkpoint(state_dir: Path) -> list[str]:
    """Read and validate checkpoint.json."""
    errors = []
    checkpoint_path = state_dir / "checkpoint.json"
    if not checkpoint_path.exists():
        return errors
    try:
        cp = read_checkpoint(state_dir, required=False)
        errors.extend(validate_checkpoint(cp, {}))
    except Exception as e:
        errors.append(f"Error reading checkpoint.json: {e}")
    return errors


def _validate_state_files(state_dir: Path) -> list[str]:
    """Read and validate STATUS.md, PLAN.md, CONTEXT.md."""
    errors = []
    try:
        status = read_status(state_dir)
        if not status.get("current_phase"):
            errors.append("STATUS.md missing current_phase")
        if not status.get("current_state"):
            errors.append("STATUS.md missing current_state")
    except Exception as e:
        errors.append(f"Error reading STATUS.md: {e}")

    try:
        read_plan(state_dir)
    except Exception as e:
        errors.append(f"Error reading PLAN.md: {e}")

    try:
        read_context(state_dir)
    except Exception as e:
        errors.append(f"Error reading CONTEXT.md: {e}")
    return errors


def cmd_validate(args):
    """Validate task-state artifacts against schemas."""
    state_dir = Path(args.state)
    if not state_dir.exists():
        print(f"Error: State directory does not exist: {state_dir}")
        return 1

    errors = []
    errors.extend(_validate_required_files(state_dir))
    errors.extend(_validate_checkpoint(state_dir))
    errors.extend(_validate_state_files(state_dir))

    if errors:
        print("Validation FAILED:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Validation PASSED")
    return 0


def cmd_inspect(args):
    """Read-only display of current workflow state."""
    state_dir = Path(args.path) if hasattr(args, "path") and args.path else None

    if not state_dir:
        print("Error: path is required")
        return 1

    if not state_dir.exists():
        print(f"Error: State directory does not exist: {state_dir}")
        return 1

    print(f"=== Workflow State: {state_dir} ===\n")

    # Read and display STATUS.md
    try:
        status = read_status(state_dir)
        print("STATUS.md:")
        print(f"  Current Phase: {status.get('current_phase', 'unknown')}")
        print(f"  Current State: {status.get('current_state', 'unknown')}")
        print(f"  Next Action: {status.get('next_action', 'unknown')}")
        print()
    except Exception as e:
        print(f"Error reading STATUS.md: {e}\n")

    # Read and display checkpoint
    try:
        checkpoint = read_checkpoint(state_dir)
        print("checkpoint.json:")
        print(f"  Workflow ID: {checkpoint.get('workflow_id', 'unknown')}")
        print(f"  Current Phase: {checkpoint.get('current_phase', 'unknown')}")
        print(f"  Current State: {checkpoint.get('current_state', 'unknown')}")
        print(f"  Last Updated: {checkpoint.get('last_updated', 'unknown')}")
        print(f"  Completed Phases: {len(checkpoint.get('completed_phases', []))}")
        print()
    except FileNotFoundError:
        print("checkpoint.json: not found\n")
    except Exception as e:
        print(f"Error reading checkpoint.json: {e}\n")

    # Read and display PLAN.md summary
    try:
        plan = read_plan(state_dir)
        phases = plan.get("phases", [])
        print("PLAN.md:")
        print(f"  Total Phases: {len(phases)}")
        completed = sum(p.get("status") == "done" for p in phases)
        print(f"  Completed: {completed}")
        print(f"  Pending: {len(phases) - completed}")
        print()
    except Exception as e:
        print(f"Error reading PLAN.md: {e}\n")

    return 0


def _require_path(path: Path, label: str) -> int | None:
    """Check a path exists. Returns exit code 1 if not, None otherwise."""
    if not path:
        print(f"Error: {label} is required")
        return 1
    if not path.exists():
        print(f"Error: {label} does not exist: {path}")
        return 1
    return None


def cmd_diff(args):
    """Compare two workflow runs phase by phase."""
    run_a = Path(args.path_a) if hasattr(args, "path_a") and args.path_a else None
    run_b = Path(args.path_b) if hasattr(args, "path_b") and args.path_b else None

    for path, label in [(run_a, "path_a"), (run_b, "path_b")]:
        if (code := _require_path(path, label)) is not None:
            return code

    print("=== Comparing Runs ===\n")
    print(f"Run A: {run_a}")
    print(f"Run B: {run_b}\n")

    phase_log_a, phase_log_b = run_a / "PHASE_LOG.md", run_b / "PHASE_LOG.md"
    if not phase_log_a.exists():
        print("Error: Run A missing PHASE_LOG.md")
        return 1
    if not phase_log_b.exists():
        print("Error: Run B missing PHASE_LOG.md")
        return 1

    content_a = phase_log_a.read_text(encoding="utf-8")
    content_b = phase_log_b.read_text(encoding="utf-8")

    if content_a == content_b:
        print("Phase logs are identical")
    else:
        _print_phase_log_diff(content_a, content_b)
    return 0


def _find_workflow_config(state_dir: Path) -> Path | None:
    """Find workflow.json in parent or .contextsmith directory."""
    c1 = state_dir.parent / "workflow.json"
    c2 = Path(".contextsmith") / "workflow.json"
    candidates = [c1, c2]
    return next(
        (candidate for candidate in candidates if candidate.exists()), None
    )


def cmd_resume(args):
    """Resume a blocked workflow."""
    state_dir = Path(args.path) if hasattr(args, "path") and args.path else None
    if (code := _require_path(state_dir, "State directory")) is not None:
        return code

    try:
        status = read_status(state_dir)
        if status.get("current_state", "unknown") != "blocked":
            print(
                f"Warning: Workflow is not blocked"
                f" (current state: {status.get('current_state')})"
            )
    except Exception as e:
        print(f"Error reading state: {e}")
        return 1

    if args.decision and not Path(args.decision).exists():
        print(f"Error: Decision file does not exist: {args.decision}")
        return 1

    config_path = _find_workflow_config(state_dir)
    if config_path is None:
        print("Error: Cannot find workflow.json")
        return 1

    print("Resuming workflow...")
    return run_workflow(
        config_path=str(config_path),
        state_dir=str(state_dir),
        harness="generic",
        verbose=True,
        quiet=False,
    )


if __name__ == "__main__":
    sys.exit(main())
