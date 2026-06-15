# Harness Adapter Design: Phase 6B

## Artifact Manifest

- artifact_type: design-document
- phase: Phase 6B
- parent_plan: PLAN.md
- target_harness: opencode
- version: 1.0.0

## Purpose
Design a harness adapter for opencode that maps ContextSmith runtime validation gates to opencode's native control mechanisms. This is a design-only phase — no source files edited, no config modified.

## Opencode Capabilities Analysis

### Permissions System (allow/ask/deny)
| Capability | Description | Hard Block? |
| --- | --- | --- |
| Tool allow | Tool can be used without restriction | No (permissive) |
| Tool ask | Tool requires user confirmation before each use | Partial (human approval gate) |
| Tool deny | Tool cannot be used at all | Yes (hard block) |
| Pattern matching | Wildcards, home directory expansion | Yes |
| Agent-level overrides | Per-agent permission rules | Yes |

### Policies (Experimental)
| Policy | Description | Status |
| --- | --- | --- |
| provider.use | Restrict which providers can be used | Experimental |
| Custom policies | Not yet supported | N/A |

### Custom Tools
| Capability | Description | Hard Block? |
| --- | --- | --- |
| Override built-in tools | Replace `edit`, `read`, `write`, `shell` with custom implementations | Yes (can intercept and block) |
| Custom tool definitions | Add new tools with custom logic | Yes |

## Harness Capability Matrix

### Gate 1: Phase Boundary Enforcement
| Field | Value |
| --- | --- |
| Trigger point | Agent attempts to proceed to next phase |
| Enforcement mechanism | Custom tool override for `write`/`edit` on task-state files |
| Validator input | `plan_status()` from runner |
| Pass behavior | Allow write to task-state files |
| Fail behavior | Block write, return violation message |
| Bypass limitations | Agent can use raw bash commands to write files |
| Classification | **Orchestrated** (not hard-blocked) |

### Gate 2: Validation Command Execution
| Field | Value |
| --- | --- |
| Trigger point | Phase closeout requires validation commands |
| Enforcement mechanism | Custom tool that wraps `shell` with pre-validation check |
| Validator input | Validation commands from CONTEXT.md |
| Pass behavior | Allow phase closeout |
| Fail behavior | Block closeout, require validation first |
| Bypass limitations | Agent can skip closeout and proceed |
| Classification | **Orchestrated** (not hard-blocked) |
| Circular validation risk | **RESOLVED**: The shell wrapper maintains a whitelist of validation commands (from `CONTEXT.md` validation_commands list). Whitelisted commands bypass the pre-validation check, allowing the agent to run `pytest`, `validate_skills.py`, and other validation commands without triggering the gate. Non-whitelisted shell commands are intercepted. This prevents the wrapper from blocking the very commands needed to satisfy the gate. |

### Gate 3: Artifact Validation
| Field | Value |
| --- | --- |
| Trigger point | Agent creates or modifies runtime artifacts |
| Enforcement mechanism | Custom tool override for `write`/`edit` with validation dispatch |
| Validator input | `runtime.validator` functions |
| Pass behavior | Allow write |
| Fail behavior | Block write, return violations |
| Bypass limitations | Agent can use raw bash commands |
| Classification | **Orchestrated** (not hard-blocked) |

### Gate 4: External Action Approval
| Field | Value |
| --- | --- |
| Trigger point | Agent attempts external_write or irreversible action |
| Enforcement mechanism | Tool deny for risky tools + ask for approval-gated tools |
| Validator input | Domain pack `external_action_boundaries` |
| Pass behavior | Allow tool use |
| Fail behavior | Deny tool use, require human approval |
| Bypass limitations | None if tools are denied |
| Classification | **Hard-blocked** (via tool deny) |

### Gate 5: Domain-Specific Constraints
| Field | Value |
| --- | --- |
| Trigger point | Agent operates in a specific domain |
| Enforcement mechanism | Custom tool with domain pack validation |
| Validator input | Domain pack JSON file |
| Pass behavior | Allow action |
| Fail behavior | Block action, return domain-specific violation |
| Bypass limitations | Agent can ignore domain pack |
| Classification | **Orchestrated** (not hard-blocked) |

### Gate 6: Evidence Ledger Requirements
| Field | Value |
| --- | --- |
| Trigger point | Phase closeout requires evidence |
| Enforcement mechanism | Custom tool that checks evidence before closeout |
| Validator input | `validate_evidence_ledger()` |
| Pass behavior | Allow closeout |
| Fail behavior | Block closeout, require evidence |
| Bypass limitations | Agent can skip closeout |
| Classification | **Orchestrated** (not hard-blocked) |

### Gate 7: Requirements Chain Traceability
| Field | Value |
| --- | --- |
| Trigger point | Agent claims requirement satisfied |
| Enforcement mechanism | Structural validator checks artifact fields; no custom tool interception |
| Validator input | `validate_requirements_chain()` |
| Pass behavior | Requirements chain has valid structure with evidence_ids and phase_ids |
| Fail behavior | Validator returns violations; agent must correct artifact before closeout |
| Bypass limitations | Agent can claim requirement satisfied without creating a valid artifact |
| Classification | **Deterministic-only** (structural validation) — corrected from "Custom tool" to clarify this gate relies on structural validation of the requirements_chain artifact, not on intercepting agent actions. The validator checks that evidence_ids and phase_ids are present and referenced, but cannot enforce truthfulness of agent claims. |

## Enforcement Classification Summary

| Classification | Gates | Description |
| --- | --- | --- |
| **Hard-blocked** | Gate 4 | Tool deny prevents action entirely |
| **Orchestrated** | Gates 1, 2, 3, 5, 6 | Custom tools can intercept and block, but agent can bypass |
| **Deterministic-only** | Gate 7 | Structural validation only, no enforcement |
| **Human approval** | Gate 4 (ask mode) | Requires user confirmation |

## Key Findings

### Hard Blocking Is Limited
Opencode's permissions system can hard-block specific tools (e.g., deny `shell`, `write`, `edit`), but cannot conditionally block based on validation results. The `ask` mode requires human approval but doesn't integrate with our validator.

### Custom Tools Can Intercept
Custom tool overrides for `edit`, `read`, `write`, and `shell` can wrap the built-in tools with validation logic. This allows us to:

1. Check validation before allowing the action
2. Return violations to the agent
3. Block the action if validation fails

### Bypass Limitations
Even with custom tools, the agent can:

1. Use raw bash commands to write files
2. Skip closeout procedures
3. Ignore domain pack guidance
4. Lie about status or evidence

### Custom Tool Bypass Analysis

The "raw bash bypass" applies to Gates 1, 3, and 5. Evaluating whether denying `shell` closes this gap:

| Scenario | Deny `shell`? | Effect | Trade-off |
| --- | --- | --- | --- |
| Agent uses `bash -c 'echo ... > file'` | Blocks bash writes | Closes raw bash bypass for Gates 1, 3 | Agent cannot run validation commands (pytest, lint, etc.) |
| Agent uses `tee` or `dd` | Blocks alternative tools | Closes alias bypass | Same trade-off: blocks legitimate shell use |
| Agent uses Python `-c` | Blocks Python shell invocations | Closes scripting bypass | Blocks legitimate one-liners |
| Agent uses built-in `write`/`edit` tools | Custom tool intercepts | Already handled by Gates 1, 3 | No additional trade-off |

**Conclusion**: Denying `shell` would close the raw bash bypass but also block validation command execution (Gate 2). The recommended approach is to keep `shell` available with the whitelisted validation commands from Gate 2, and accept that the raw bash bypass exists for Gates 1, 3, and 5. This is consistent with the orchestrated (not hard-blocked) classification. Agents operating outside the orchestrated workflow can bypass these gates by design.

**Mitigation**: The runner's `next_gate()` command provides visibility into which gates are satisfied. Human reviewers can use this to detect bypass attempts. Gate 4 (external action approval) remains hard-blocked via tool deny, providing a safety net for irreversible actions.

### Recommended Approach
Given the bypass limitations, the recommended approach is:

1. **Gate 4 (External Action Approval)**: Use tool deny/ask for hard blocking of risky actions
2. **Gates 1-3, 5-6**: Use custom tool overrides for orchestrated validation
3. **Gate 7**: Rely on deterministic structural validation only

This aligns with Decision 1 (hybrid enforcement) and Decision 10 (full stack first slice).

## Integration Points

### Custom Tool Definition

```json
{
  "name": "contextsmith_write",
  "description": "Write file with ContextSmith validation",
  "parameters": {
    "path": {"type": "string"},
    "content": {"type": "string"}
  }
}
```

### Validation Dispatch
```python
def contextsmith_write(path: str, content: str) -> dict:

    # Check if path is a runtime artifact
    if is_runtime_artifact(path):

        # Validate before write
        result = validate_artifact(artifact_type, content)
        if not result["passed"]:
            return {
                "success": False,
                "violations": result["violations"],
                "message": "Validation failed. Fix violations before writing."
            }

    # Proceed with write
    return {"success": True, "path": path}
```

### Domain Pack Integration
```python
def get_domain_pack(domain: str) -> dict:

    # Load domain pack for current domain
    pack_path = f"runtime/domain_packs/{domain}.json"
    return load_json(pack_path)

def check_action_allowed(domain: str, action: str) -> bool:
    pack = get_domain_pack(domain)
    boundaries = pack.get("external_action_boundaries", {})
    level = boundaries.get(action, "allowed")
    return level != "blocked"
```

## Packaging Notes

### Per-Skill Distribution
The harness adapter files should be declared in each skill's `reference_manifest.yml`:

```yaml
- name: harness_adapter.py

  local: true
  required: true
  version: local

- name: harness_config.json

  local: true
  required: true
  version: local
```

After `sync_shared_refs.py`, these flatten to `references/harness_adapter.py` and `references/harness_config.json`. This is expected behavior (Phase 0 packaging fact). Resolution of ISSUE-1 is deferred to Phase 8B.

### ISSUE-1 Consideration
The packaging flattening issue (ISSUE-1) affects harness adapter files. After sync, `runtime/harness_adapter.py` becomes `references/harness_adapter.py`, breaking module imports. Resolution options from DECISIONS.md should be applied.

## Gate Priority Ordering

For Phase 6C implementation, gates should be implemented in this order:

1. **Gate 4 (External Action Approval)** — highest priority; uses existing tool deny/ask mechanisms; provides hard blocking for irreversible actions
2. **Gate 3 (Artifact Validation)** — medium priority; wraps existing validator functions; provides structured feedback on artifact quality
3. **Gate 1 (Phase Boundary)** — medium priority; prevents phase advancement without validation; relies on custom tool overrides
4. **Gate 2 (Validation Commands)** — medium priority; requires whitelist implementation; depends on Gate 1 for phase context
5. **Gate 5 (Domain-Specific Constraints)** — lower priority; domain pack integration; builds on Gate 3 infrastructure
6. **Gate 6 (Evidence Ledger)** — lower priority; closeout gate; depends on Gate 1 for phase context
7. **Gate 7 (Requirements Traceability)** — lowest priority; structural validation only; no enforcement mechanism needed

## Ralph Loop Iteration History

- **Iteration 1**: Identified 3 design-quality defects: (1) Gate 2 circular validation: wrapping shell could block validation commands — resolved with whitelist mechanism, (2) Gate 7 classification mismatch: "Deterministic-only" label conflicts with "Custom tool" mechanism — corrected to structural validator, (3) custom tool bypass gap: missing analysis for alternative tool names and aliases — resolved with bypass analysis table and mitigation strategy.
- **Iteration 2**: No material defects. All 7 gates verified with required fields. Stop rule respected. No unsupported claims.

## Implementation Test Strategy

Phase 6C implementation must include these test categories:

### Gate Integration Tests

- Gate 4 tool deny blocks external_write actions when domain pack marks them as blocked.
- Gate 4 ask mode requires human approval for requires_approval actions.
- Gate 3 artifact validation intercepts writes to runtime artifact paths.
- Gate 3 allows writes to non-artifact paths without validation.

### Bypass Detection Tests

- Raw bash write bypass is detected by runner's `next_gate()` command.
- Custom tool override intercepts `write` and `edit` on artifact paths.
- Shell whitelist allows validation commands but blocks arbitrary writes.

### Policy Compliance Tests

- Tool deny policy prevents denied tools from executing.
- Tool ask policy requires human confirmation before execution.
- Custom tool override replaces built-in tool behavior.

### Domain Pack Integration Tests

- Domain pack boundaries are loaded and applied to Gate 5.
- Unknown domain falls back to `general_fallback` pack.
- Missing domain pack returns error with pack name in message.

**Test file**: `tests/test_harness_adapter.py` (estimated 25-35 tests).
**Validation command**: `python -m pytest tests/test_harness_adapter.py -v`

## Validation State

- Design phase: no source files edited
- `python scripts/validate_skills.py` passes
- `python scripts/token_budget.py --strict` passes
- `python -m pytest tests/ -v` passes (204 tests)
- **Audit fixes applied**: Gate 2 circular validation resolved (whitelist), Gate 7 classification corrected (structural validator), bypass analysis added, Ralph loop history recorded, packaging manifest entries specified, gate priority ordering defined, implementation test strategy added.

## Next Steps

- Phase 6C (Harness Adapter Implementation) - implement the adapter based on this design, following gate priority ordering
- Address ISSUE-1 before Phase 8B rollout
