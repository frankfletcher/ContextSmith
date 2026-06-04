"""ContextSmith orchestrated runner skeleton.

This module provides a minimal runner skeleton for executing task-state phases
with validation dispatch and gate checking, without model invocation.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add project root to path for imports
_project_root = Path(__file__).resolve().parent.parent
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


def read_task_state(task_dir: Path | str) -> Dict[str, Any]:
    """Read task-state files from the given directory.
    
    Returns:
        Dictionary with task state contents.
    """
    task_dir = Path(task_dir)
    state = {}
    state_files = [
        "STATUS.md",
        "PLAN.md",
        "CONTEXT.md",
        "DECISIONS.md",
        "CHECKLIST.md",
        "ARTIFACTS.md",
        "PHASE_LOG.md",
        "NEXT_PROMPT.md",
    ]
    
    for filename in state_files:
        filepath = task_dir / filename
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    state[filename] = f.read()
            except Exception as e:
                state[filename] = f"ERROR: {e}"
        else:
            state[filename] = None
    
    return state


def get_current_phase(task_dir: Path | str) -> Optional[str]:
    """Get the current phase from STATUS.md.
    
    Returns:
        Phase name or None if not found.
    """
    task_dir = Path(task_dir)
    status_path = task_dir / "STATUS.md"
    if not status_path.exists():
        return None
    
    with open(status_path, 'r') as f:
        content = f.read()
    
    # Look for "current_phase: Phase X"
    for line in content.split('\n'):
        if 'current_phase:' in line.lower():
            # Extract phase name
            parts = line.split(':', 1)
            if len(parts) > 1:
                return parts[1].strip()
    
    return None


def plan_status(task_dir: Path | str) -> Dict[str, Any]:
    """Get the current plan status.
    
    Returns:
        Dictionary with phase info and next action.
    """
    task_dir = Path(task_dir)
    state = read_task_state(task_dir)
    current_phase = get_current_phase(task_dir)
    
    # Parse STATUS.md for more details
    status_info = {}
    if state["STATUS.md"]:
        lines = state["STATUS.md"].split('\n')
        for line in lines:
            if 'current_phase:' in line.lower():
                status_info['current_phase'] = line.split(':', 1)[1].strip()
            elif 'next_required_action:' in line.lower():
                status_info['next_action'] = line.split(':', 1)[1].strip()
            elif 'validation_state:' in line.lower():
                status_info['validation_state'] = 'PASS' if 'pass' in line.lower() else 'UNKNOWN'
    
    return {
        'phase': current_phase,
        'status': status_info,
        'has_status': state["STATUS.md"] is not None,
        'has_plan': state["PLAN.md"] is not None,
        'has_context': state["CONTEXT.md"] is not None,
    }


def next_gate(task_dir: Path | str) -> Dict[str, Any]:
    """Determine the next validation gate or blocker.
    
    Returns:
        Dictionary with next gate info or blocker details.
    """
    task_dir = Path(task_dir)
    state = read_task_state(task_dir)
    current_phase = get_current_phase(task_dir)
    
    # Check for blockers in STATUS.md
    blockers = []
    if state["STATUS.md"]:
        lines = state["STATUS.md"].split('\n')
        in_blockers = False
        for line in lines:
            if '## blockers' in line.lower():
                in_blockers = True
                continue
            if in_blockers and line.strip().startswith('##'):
                in_blockers = False
            if in_blockers and line.strip():
                blockers.append(line.strip())
    
    # Check for validation commands in CONTEXT.md
    validation_commands = []
    if state["CONTEXT.md"]:
        lines = state["CONTEXT.md"].split('\n')
        in_validation = False
        for line in lines:
            if '## validation commands' in line.lower():
                in_validation = True
                continue
            if in_validation and line.strip().startswith('##'):
                in_validation = False
            if in_validation and line.strip():
                validation_commands.append(line.strip())
    
    return {
        'phase': current_phase,
        'blockers': blockers,
        'validation_commands': validation_commands,
        'next_action': 'Run validation commands' if validation_commands else 'Check for blockers',
    }


def validate_artifact(artifact_type: str, artifact_path: Path) -> Dict[str, Any]:
    """Validate a single artifact using the appropriate validator.
    
    Args:
        artifact_type: Type of artifact (requirements, phase-contract, evidence, approval, closeout, domain-pack)
        artifact_path: Path to the artifact file
    
    Returns:
        Validation result dictionary
    """
    validators = {
        'requirements': validate_requirements_chain,
        'phase-contract': validate_phase_contract,
        'evidence': validate_evidence_ledger,
        'approval': validate_approval_record,
        'closeout': validate_phase_closeout,
        'domain-pack': validate_domain_pack,
    }
    
    if artifact_type not in validators:
        return {
            'passed': False,
            'violations': [f'Unknown artifact type: {artifact_type}'],
            'warnings': []
        }
    
    try:
        return validators[artifact_type](artifact_path)
    except Exception as e:
        return {
            'passed': False,
            'violations': [f'Validation error: {e}'],
            'warnings': []
        }


def main():
    """CLI entry point for the runner skeleton."""
    import argparse
    
    parser = argparse.ArgumentParser(
        prog='contextsmith-runner',
        description='ContextSmith orchestrated runner skeleton'
    )
    
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # plan-status command
    status_parser = subparsers.add_parser('plan-status', help='Get current plan status')
    status_parser.add_argument('task_dir', nargs='?', default='.', help='Task directory')
    
    # next-gate command
    gate_parser = subparsers.add_parser('next-gate', help='Determine next validation gate')
    gate_parser.add_argument('task_dir', nargs='?', default='.', help='Task directory')
    
    # validate command
    validate_parser = subparsers.add_parser('validate', help='Validate an artifact')
    validate_parser.add_argument('artifact_type', choices=['requirements', 'phase-contract', 'evidence', 'approval', 'closeout', 'domain-pack'], help='Artifact type')
    validate_parser.add_argument('artifact_path', help='Path to artifact file')
    
    args = parser.parse_args()
    
    if args.command == 'plan-status':
        result = plan_status(Path(args.task_dir))
        print(json.dumps(result, indent=2))
        return 0
    
    elif args.command == 'next-gate':
        result = next_gate(Path(args.task_dir))
        print(json.dumps(result, indent=2))
        return 0
    
    elif args.command == 'validate':
        result = validate_artifact(args.artifact_type, Path(args.artifact_path))
        if result['passed']:
            print(f"PASS {args.artifact_path}")
        else:
            print(f"FAIL {args.artifact_path}")
            for v in result.get('violations', []):
                print(f"  violation: {v}")
        for w in result.get('warnings', []):
            print(f"  warning: {w}")
        return 0 if result['passed'] else 1
    
    return 2


if __name__ == '__main__':
    sys.exit(main())
