"""ContextSmith runtime validator CLI.

Usage:
    python -m runtime.cli <subcommand> <artifact_path>
    python runtime/cli.py <subcommand> <artifact_path>

Exit codes:
    0  Validation passed
    1  Validation failed (violations found)
    2  Usage error or file-read error
"""

import argparse
import json
import sys
from pathlib import Path

# Support both `python runtime/cli.py` and `python -m runtime.cli`
_cli_dir = Path(__file__).resolve().parent
_project_root = _cli_dir.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from runtime.validator import (
    validate_requirements_chain,
    validate_phase_contract,
    validate_evidence_ledger,
    validate_approval_record,
    validate_phase_closeout,
    validate_domain_pack,
)
from runtime.next_prompt_compiler import compile_next_prompt_cli
from runtime.runner import plan_status, next_gate


# Map subcommand name -> (validator function, description)
SUBCOMMANDS = {
    "requirements": (validate_requirements_chain, "Validate a requirements_chain artifact"),
    "phase-contract": (validate_phase_contract, "Validate a phase_contract artifact"),
    "evidence": (validate_evidence_ledger, "Validate an evidence_ledger artifact"),
    "approval": (validate_approval_record, "Validate an approval_record artifact"),
    "closeout": (validate_phase_closeout, "Validate a phase_closeout artifact"),
    "domain-pack": (validate_domain_pack, "Validate a domain_pack artifact"),
}

# Runner commands (read-only)
RUNNER_COMMANDS = {
    "plan-status": (plan_status, "Get current plan status"),
    "next-gate": (next_gate, "Determine next validation gate"),
}


def _print_result(result: dict, path: str) -> int:
    """Print validation result to stdout. Return exit code."""
    if result["passed"]:
        print(f"PASS  {path}")
    else:
        print(f"FAIL  {path}")
        for v in result["violations"]:
            print(f"  violation: {v}")

    for w in result.get("warnings", []):
        print(f"  warning: {w}")

    return 0 if result["passed"] else 1


def _handle_subcommand(cmd: str, validator, args: argparse.Namespace) -> int:
    """Dispatch a subcommand to its validator. Return exit code."""
    path = args.path
    try:
        result = validator(path)
    except FileNotFoundError as e:
        print(f"ERROR  {e}", file=sys.stderr)
        return 2
    except (json.JSONDecodeError, ValueError) as e:
        print(f"ERROR  Invalid JSON in {path}: {e}", file=sys.stderr)
        return 2
    return _print_result(result, str(path))


def build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="contextsmith-validator",
        description="ContextSmith runtime artifact validator and runner",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name, (validator_fn, description) in SUBCOMMANDS.items():
        sp = subparsers.add_parser(name, help=description)
        sp.add_argument("path", help="Path to the artifact file to validate")
        sp.set_defaults(func=validator_fn)

    # Runner commands
    for name, (runner_fn, description) in RUNNER_COMMANDS.items():
        sp = subparsers.add_parser(name, help=description)
        sp.add_argument("task_dir", nargs="?", default=".", help="Task directory (default: current dir)")
        sp.set_defaults(func=runner_fn)

    # next-prompt subcommand
    np_parser = subparsers.add_parser(
        "next-prompt",
        help="Generate NEXT_PROMPT.md from task-state files",
    )
    np_parser.add_argument(
        "task_dir", nargs="?", default=".",
        help="Task directory containing state files (default: current dir)",
    )
    np_parser.add_argument(
        "--output", "-o", default=None,
        help="Output file path (default: NEXT_PROMPT.md in task dir)",
    )
    np_parser.add_argument(
        "--phase", "-p", default=None,
        help="Override current phase (default: read from STATUS.md)",
    )
    np_parser.add_argument(
        "--include-education", action="store_true", default=False,
        help="Include deep education notes section",
    )
    np_parser.add_argument(
        "--dry-run", "-n", action="store_true", default=False,
        help="Print to stdout without writing file",
    )
    np_parser.add_argument(
        "--compact", action="store_true", default=False,
        help="Omit education notes and collapse phase contract",
    )
    np_parser.set_defaults(func=_handle_next_prompt)

    return parser


def _handle_next_prompt(args: argparse.Namespace) -> int:
    """Handle the next-prompt subcommand. Return exit code."""
    return compile_next_prompt_cli(
        task_dir=args.task_dir or ".",
        output=args.output,
        phase=args.phase,
        include_education=args.include_education,
        dry_run=args.dry_run,
        compact=args.compact,
    )


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Return exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    validator_fn = getattr(args, "func", None)
    if validator_fn is None:
        parser.print_help()
        return 2

    if args.command == "next-prompt":
        return _handle_next_prompt(args)

    # Check if this is a runner command (returns dict instead of int)
    if args.command in RUNNER_COMMANDS:
        result = validator_fn(args.task_dir if hasattr(args, 'task_dir') else ".")
        if isinstance(result, dict):
            import json
            print(json.dumps(result, indent=2))
            return 0
        return result

    return _handle_subcommand(args.command, validator_fn, args)


if __name__ == "__main__":
    sys.exit(main())
