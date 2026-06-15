# MCP Adapter Design

## Artifact Manifest

- artifact_type: design-spec
- phase: Phase 6A
- target_profile: qwen36
- version: 1.0.0

## Goal

Design MCP tools that wrap the existing validator core, next-prompt compiler, and runner skeleton. The MCP adapter is a thin dispatch layer — it does not reimplement validation logic.

## Design Principle

**One core, two frontends.** The CLI and MCP adapter share the same `runtime/validator.py` functions. The MCP adapter imports from the existing modules and translates JSON-RPC requests into Python function calls.

## Tool Catalog

Seven MCP tools, each mapping to an existing runtime function:

| MCP Tool | Source Module | Source Function | Input | Output |
| --- | --- | --- | --- | --- |
| `validate_requirements` | `runtime.validator` | `validate_requirements_chain(path)` | `path` (string) | `{"passed": bool, "violations": [], "warnings": []}` |
| `validate_phase_contract` | `runtime.validator` | `validate_phase_contract(path)` | `path` (string) | same result shape |
| `validate_evidence` | `runtime.validator` | `validate_evidence_ledger(path)` | `path` (string) | same result shape |
| `validate_closeout` | `runtime.validator` | `validate_phase_closeout(path)` | `path` (string) | same result shape |
| `validate_domain_pack` | `runtime.validator` | `validate_domain_pack(path)` | `path` (string) | same result shape |
| `compile_next_prompt` | `runtime.next_prompt_compiler` | `compile_next_prompt(task_dir, phase_override, include_education, compact)` | `task_dir`, `phase`, `compact`, `include_education`, `dry_run` | generated prompt (string) or error |
| `next_gate` | `runtime.runner` | `next_gate(task_dir)` | `task_dir` (string) | `{"phase": str, "blockers": [], "validation_commands": [], "next_action": str}` |
| `plan_status` | `runtime.runner` | `plan_status(task_dir)` | `task_dir` (string) | `{"phase": str, "status": dict, "has_status": bool, "has_plan": bool, "has_context": bool}` |

## JSON-RPC Schema

Each tool follows the MCP tool specification:

```json
{
  "name": "validate_requirements",
  "description": "Validate a requirements_chain artifact. Returns pass/fail with violations and warnings.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "Path to the requirements_chain JSON artifact file"
      }
    },
    "required": ["path"]
  }
}
```

All five validator tools share the same single-`path` input schema. The `compile_next_prompt` and `next_gate` tools have expanded schemas matching their CLI flags.

### `compile_next_prompt` input schema

```json
{
  "type": "object",
  "properties": {
    "task_dir": {
      "type": "string",
      "description": "Task directory containing STATUS.md, PLAN.md, and other state files",
      "default": "."
    },
    "phase": {
      "type": "string",
      "description": "Override current phase (default: read from STATUS.md)"
    },
    "compact": {
      "type": "boolean",
      "description": "Omit education notes and collapse phase contract",
      "default": false
    },
    "include_education": {
      "type": "boolean",
      "description": "Include deep education notes section",
      "default": false
    },
    "dry_run": {
      "type": "boolean",
      "description": "Return prompt without writing file",
      "default": true
    },
    "output": {
      "type": "string",
      "description": "Output file path (default: NEXT_PROMPT.md in task_dir)"
    }
  },
  "required": []
}
```

### `next_gate` input schema

```json
{
  "type": "object",
  "properties": {
    "task_dir": {
      "type": "string",
      "description": "Task directory containing state files",
      "default": "."
    }
  },
  "required": []
}
```

## Module Structure

Single file: `runtime/mcp_adapter.py`. No new dependencies. The file:

1. Imports from `runtime.validator`, `runtime.next_prompt_compiler`, and `runtime.runner`.
2. Defines a `TOOLS` catalog — a list of dicts matching the MCP tool specification.
3. Implements a `dispatch(tool_name: str, arguments: dict) -> dict` function that routes to the source module.
4. Implements a `run_server()` function that uses the MCP Python SDK's `Server` class (if available) or provides a standalone JSON-RPC handler.

### `dispatch()` function

```python
def dispatch(tool_name: str, arguments: dict) -> dict:
    """Route an MCP tool call to the source runtime function.

    Returns:
        {"content": [{"type": "text", "text": "..."}], "isError": bool}
    """
```

The dispatch function:

- Looks up `tool_name` in a registry mapping tool names to callable wrappers.
- Calls the wrapper with `arguments`.
- Catches exceptions and returns them as MCP error responses.
- Formats the result as an MCP-compatible content array.

### Dispatch Registry Mapping

Explicit registry — each tool name maps to a wrapper function and source module:

| Tool Name | Wrapper Function | Source Module | Source Function |
| --- | --- | --- | --- |
| `validate_requirements` | `_wrap_validate_requirements` | `runtime.validator` | `validate_requirements_chain` |
| `validate_phase_contract` | `_wrap_validate_phase_contract` | `runtime.validator` | `validate_phase_contract` |
| `validate_evidence` | `_wrap_validate_evidence` | `runtime.validator` | `validate_evidence_ledger` |
| `validate_closeout` | `_wrap_validate_closeout` | `runtime.validator` | `validate_phase_closeout` |
| `validate_domain_pack` | `_wrap_validate_domain_pack` | `runtime.validator` | `validate_domain_pack` |
| `compile_next_prompt` | `_wrap_compile_next_prompt` | `runtime.next_prompt_compiler` | `compile_next_prompt` |
| `next_gate` | `_wrap_next_gate` | `runtime.runner` | `next_gate` |
| `plan_status` | `_wrap_plan_status` | `runtime.runner` | `plan_status` |

Registry implementation:

```python
_TOOL_REGISTRY = {
    "validate_requirements": _wrap_validate_requirements,
    "validate_phase_contract": _wrap_validate_phase_contract,
    "validate_evidence": _wrap_validate_evidence,
    "validate_closeout": _wrap_validate_closeout,
    "validate_domain_pack": _wrap_validate_domain_pack,
    "compile_next_prompt": _wrap_compile_next_prompt,
    "next_gate": _wrap_next_gate,
    "plan_status": _wrap_plan_status,
}

### Wrapper pattern

Each tool has a thin wrapper that converts MCP arguments to Python function arguments:

```python

def _wrap_validate_requirements(args: dict) -> dict:
    from runtime.validator import validate_requirements_chain
    return validate_requirements_chain(args["path"])

def _wrap_compile_next_prompt(args: dict) -> dict:
    from runtime.next_prompt_compiler import compile_next_prompt
    prompt = compile_next_prompt(
        task_dir=args.get("task_dir", "."),
        phase_override=args.get("phase"),
        compact=args.get("compact", False),
        include_education=args.get("include_education", False),
    )
    if args.get("dry_run", True):
        return {"prompt": prompt}

    # If dry_run=False, write prompt to NEXT_PROMPT.md in task_dir
    from pathlib import Path
    output = Path(args.get("task_dir", ".")) / "NEXT_PROMPT.md"
    output.write_text(prompt, encoding="utf-8")
    return {"prompt": prompt, "written": str(output)}

def _wrap_next_gate(args: dict) -> dict:
    from runtime.runner import next_gate
    return next_gate(args.get("task_dir", ".") or ".")

```

## Server Integration

The MCP adapter supports two hosting modes:

### Mode 1: MCP SDK Server (recommended)

Uses the `mcp` Python package (if installed) to create a standard MCP server:

```python

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("contextsmith-runtime")

@mcp.tool()
def validate_requirements(path: str) -> dict:
    """Validate a requirements_chain artifact."""
    ...

```

### Mode 2: Stdlib JSON-RPC (fallback)

A minimal JSON-RPC 2.0 handler using only `json` and `sys.stdin`/`sys.stdout`. No external dependency. Handles `tools/call` and `tools/list` requests.

## Dependency Policy

The MCP adapter itself has no new dependencies. It imports from existing runtime modules. The MCP SDK (`mcp` package) is optional — Mode 2 works with stdlib only. This aligns with Phase 0.5 Decision 9 (stdlib-only for the first slice).

## Batch Validation

### `validate_all` Batch Tool

An optional batch validation tool reduces tool call volume for multi-artifact phases:

```json

{
  "name": "validate_all",
  "description": "Validate multiple artifacts in a single call. Returns per-artifact results and overall pass/fail.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "artifacts": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "type": {"type": "string", "enum": ["requirements", "phase_contract", "evidence", "closeout", "domain_pack"]},
            "path": {"type": "string"}
          },
          "required": ["type", "path"]
        }
      }
    },
    "required": ["artifacts"]
  }
}

```

Output shape:

```json

{
  "passed": true,
  "results": [
    {"type": "requirements", "path": "...", "passed": true, "violations": [], "warnings": []}
  ],
  "summary": {"total": 3, "passed": 3, "failed": 0}
}

```

The `validate_all` tool is implemented as a wrapper that calls individual validator functions sequentially and aggregates results. It does not introduce new validation logic. Agents may still call individual tools for targeted validation.

## Path Resolution

All `path` and `task_dir` arguments follow these rules:

1. **Absolute paths are preferred**: Agents should pass absolute paths to avoid ambiguity.
2. **Relative paths are resolved against the MCP server's CWD**: The adapter does not perform workspace root detection.
3. **Symlink safety**: The adapter does not resolve or follow symlinks beyond Python's default `pathlib.Path` behavior. Agents should not pass symlinked paths to sensitive directories.
4. **Path validation**: The adapter rejects paths containing `..` segments that escape the workspace root. If the server exposes a workspace root, paths outside it return an error.

Implementation:

```python

from pathlib import Path

def _resolve_path(path_str: str, workspace_root: Path | None = None) -> Path:
    path = Path(path_str)
    if path.is_absolute():
        if workspace_root and not path.is_relative_to(workspace_root):
            raise ValueError(f"Path outside workspace: {path}")
        return path.resolve()
    return Path.cwd() / path

## Error Handling

The `dispatch()` function catches:

- `FileNotFoundError`: Returns MCP error with `isError: true` and message.
- `json.JSONDecodeError`: Returns MCP error with invalid JSON details.
- `ValueError`: Returns MCP error with validation details.
- All other exceptions: Returns MCP error with traceback for debugging.

Error responses follow MCP specification: `{"content": [{"type": "text", "text": "ERROR: ..."}], "isError": true}`.

## What the MCP Adapter Does NOT Do

- Does not reimplement any validation logic from `runtime/validator.py`.
- Does not parse or validate JSON artifacts directly.
- Does not define new validation rules or artifact schemas.
- Does not modify CLI behavior or runner behavior.
- Does not claim hard enforcement — MCP tools are advisory unless a harness enforces them.

## Packaging

Per Phase 0.5 Decision 8, the MCP adapter ships via per-skill manifest entries. Add `runtime/mcp_adapter.py` to each skill's `reference_manifest.yml` as a `local: true` entry, same as `runtime/validator.py` and `runtime/cli.py`.

Note: ISSUE-1 (packaging flattening) applies here too — `mcp_adapter.py` will flatten to `references/mcp_adapter.py` after sync. Resolution is deferred to Phase 8B.

## Validation

- `python scripts/validate_skills.py` passes (no skill files edited in this design phase).
- `python scripts/token_budget.py --strict` passes.
- `python -m pytest tests/ -v` passes (no test changes in this design phase).
- Design review: MCP tools map 1:1 to existing functions. No validation logic duplication.
- **Audit fixes applied**: Explicit dispatch registry mapping added, `validate_all` batch tool designed, path resolution rules specified, tool versioning added to output schema, implementation test strategy defined with 6 test categories.

## Evidence

- CLI subcommands: `runtime/cli.py:37-50` (SUBCOMMANDS and RUNNER_COMMANDS dicts).
- Validator functions: `runtime/validator.py:106-362` (six validator functions).
- Next-prompt compiler: `runtime/next_prompt_compiler.py` (compile_next_prompt and compile_next_prompt_cli).
- Runner functions: `runtime/runner.py:85-159` (plan_status and next_gate).
