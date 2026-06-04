# Runner Specification

## Artifact Manifest
- artifact_type: specification
- phase: 5E
- target_profile: qwen36
- version: 1.0.0

## Purpose

The Runner is a read-only CLI tool that provides orchestration support for ContextSmith task-state phases. It does not execute models or advance phases; instead, it provides gate-checking and status reporting capabilities that an orchestrator can use to control workflow progression.

## Inputs

| Input | Required | Source |
|---|---|---|
| `STATUS.md` | Yes | Current phase name, next action, blockers, validation state |
| `PLAN.md` | Yes | Current phase block: goal, actions, validation, context contract |
| `CONTEXT.md` | Yes | File map, constraints, validation commands, skip rules |
| `CHECKLIST.md` | No | Completed items for context |
| `DECISIONS.md` | No | Durable decisions affecting current phase |
| `ARTIFACTS.md` | No | Changed artifacts from prior phases |
| `PHASE_LOG.md` | No | Prior phase outcomes for carry-forward |

## Commands

### plan-status

**Purpose**: Get the current plan status for a task directory.

**Usage**: `python -m runtime.cli plan-status <task_dir>`

**Output**: JSON with the following structure:
```json
{
  "phase": "Phase 5E",
  "status": {
    "current_phase": "Phase 5E",
    "next_action": "Phase 5E (Runner Skeleton)",
    "validation_state": "PASS"
  },
  "has_status": true,
  "has_plan": true,
  "has_context": true
}
```

**Exit Code**: 0 (success)

### next-gate

**Purpose**: Determine the next validation gate or blocker for a task directory.

**Usage**: `python -m runtime.cli next-gate <task_dir>`

**Output**: JSON with the following structure:
```json
{
  "phase": "Phase 5E",
  "blockers": ["- **ISSUE-1:** Packaging flattening breaks runtime module paths."],
  "validation_commands": [
    "- `python scripts/validate_skills.py`",
    "- `python -m pytest tests/ -v`"
  ],
  "next_action": "Run validation commands"
}
```

**Exit Code**: 0 (success)

## Interface Design

### Read-Only Commands

The runner provides two read-only commands:
1. **plan-status**: Returns current phase and task state summary
2. **next-gate**: Returns next validation gate or blocker information

Both commands are read-only and do not modify task state.

### Validation Dispatch

The runner dispatches validation to the existing CLI validator:
- Uses `runtime/validator.py` functions for artifact validation
- Does not implement custom validation logic
- Reuses existing domain packs and validation rules

### Output Format

Both commands output JSON for programmatic consumption:
- Human-readable when printed to stdout
- Machine-parseable for integration with other tools
- Compact and focused on essential information

## Safety Constraints

### Disallowed Actions

- **No Model Invocation**: Runner does not call any language models
- **No Phase Advancement**: Runner does not modify STATUS.md or advance phases
- **No File Editing**: Runner does not edit task-state files
- **No External Actions**: Runner does not perform external API calls or send messages

### Allowed Actions

- **Read Task State**: Read STATUS.md, PLAN.md, CONTEXT.md, and other task files
- **Output Status**: Return current phase and validation state as JSON
- **Check Gates**: Report next validation gate or blocker

## Implementation Notes

### Code Structure

```
runtime/
├── runner.py          # Core runner functions
├── cli.py             # CLI integration with plan-status/next-gate subcommands
└── validator.py       # Existing validation functions (reused)
```

### Function Signatures

```python
def plan_status(task_dir: Path | str) -> Dict[str, Any]:
    """Get the current plan status."""
    ...

def next_gate(task_dir: Path | str) -> Dict[str, Any]:
    """Determine the next validation gate or blocker."""
    ...
```

### Integration with CLI

The runner commands are integrated into the existing `runtime/cli.py`:
- Added `plan-status` and `next-gate` subcommands
- Uses the same argparse infrastructure as validator commands
- Returns JSON output for programmatic consumption

## Validation

### Test Coverage

- `test_plan_status_basic`: Tests basic phase information retrieval
- `test_next_gate_basic`: Tests gate and blocker detection
- `test_plan_status_missing_files`: Tests graceful handling of missing files
- `test_next_gate_missing_files`: Tests graceful handling of missing files
- `test_runner_cli_plan_status`: Tests CLI invocation via subprocess
- `test_runner_cli_next_gate`: Tests CLI invocation via subprocess
- `test_runner_cli_help`: Tests help output
- `test_runner_cli_subcommand_help`: Tests subcommand help output

### Validation Commands

- `python scripts/validate_skills.py` after skill or shared-reference changes
- `python scripts/token_budget.py --strict` after skill or shared-reference changes
- `python -m pytest tests/ -v` after runner test changes

## Future Extensions

### Planned Extensions

- **MCP Adapter**: Expose runner commands as MCP tools (Phase 6A)
- **Orchestrated Runner**: Add workflow sequencing logic (Phase 6B+)
- **Harness Integration**: Hard-blocking integration where supported (Phase 6B+)

### Not Planned for This Phase

- Model invocation or generation
- Phase advancement or state modification
- External API calls or actions
- Complex workflow orchestration

## References

- Phase 5E in PLAN.md: Runner Skeleton specification
- STATUS.md: Current phase and validation state
- runtime/runner.py: Implementation
- tests/test_runner.py: Test suite
