# Phase 6 Audit Report

## Artifact Manifest
- artifact_type: audit-report
- parent_task: TASK.md
- phase: 6A-6B
- auditor: contextsmith-agent-evaluator
- rubric: implementation-plan-audit.md (A-F scale)

## Scope

Audit of Phase 6A (MCP Adapter Design) and Phase 6B (Harness Adapter Design) for plan executability, design quality, and small-model readiness.

## Verdict: PASS (both A-level)

Both designs pass A-F rubric audit after targeted fixes. Ready to proceed to Phase 6C (MCP/Harness Adapter Implementation).

---

## A-F Rubric Grades

| Phase | Initial Grade | Post-Fix Grade | Rubric Dimensions |
|---|---|---|---|
| 6A MCP Adapter | B+ | A | Executability, Completeness, Small-Model Readiness, Risk Awareness |
| 6B Harness Adapter | B | A | Executability, Completeness, Small-Model Readiness, Risk Awareness |

## Phase 6A Audit Findings

### Defects (Initial B+)

1. **Missing dispatch registry mapping** — dispatch function described but no explicit tool-to-wrapper mapping. Small model would need to infer registry entries.
2. **Missing batch validation tool** — agents calling 5+ validators sequentially waste tool calls. No `validate_all` batch tool specified.
3. **Path resolution underspecified** — relative path handling, symlink safety, and path escape rejection not documented.
4. **Tool versioning absent** — no version field in tool outputs; API stability not addressed.
5. **Implementation test strategy missing** — no test categories for Phase 6C implementation.

### Fixes Applied

| Finding | Fix | Location |
|---|---|---|
| Dispatch registry | Added explicit 8-entry registry table mapping tool names to wrapper functions and source modules | `MCP_ADAPTER_DESIGN.md` §Dispatch Registry Mapping |
| Batch validation | Added `validate_all` tool with JSON schema, input/output shapes, and sequential aggregation semantics | `MCP_ADAPTER_DESIGN.md` §Batch Validation |
| Path resolution | Added 4 rules: absolute preferred, relative resolved against CWD, symlink safety via pathlib, `..` escape rejection | `MCP_ADAPTER_DESIGN.md` §Path Resolution |
| Tool versioning | Added `version` field to tool output schema for API stability tracking | `MCP_ADAPTER_DESIGN.md` §Error Handling |
| Test strategy | Added 6 test categories: dispatch registry, error format, JSON-RPC compliance, path resolution, batch validation, wrapper patterns | `MCP_ADAPTER_DESIGN.md` §Implementation Test Strategy |

### Post-Fix Verification

- All 5 findings addressed with concrete specifications
- No new dependencies introduced
- Design remains within scope (wraps existing runtime, no validation logic duplication)
- Small-model executable: registry table, JSON schemas, and test categories provide explicit targets

## Phase 6B Audit Findings

### Defects (Initial B)

1. **Gate 2 circular validation** — wrapping `shell` with pre-validation check would block the validation commands needed to satisfy the gate.
2. **Gate 7 classification mismatch** — labeled "Deterministic-only" but mechanism listed as "Custom tool", creating confusion about enforcement.
3. **Custom tool bypass gap** — missing analysis of whether denying `shell` closes raw bash bypass, and what trade-offs that introduces.
4. **Ralph loop iteration history not recorded** — iteration 1 identified 3 defects but iteration details not preserved in design document.
5. **Packaging manifest entries unspecified** — `runtime/harness_config.json` mentioned but no manifest declaration format provided.
6. **Gate priority ordering missing** — no guidance on which gates to implement first in Phase 6C.
7. **Implementation test strategy missing** — no test categories for Phase 6C implementation.

### Fixes Applied

| Finding | Fix | Location |
|---|---|---|
| Gate 2 circular validation | Added shell whitelist mechanism: validation commands from CONTEXT.md bypass pre-validation check | `HARNESS_ADAPTER_DESIGN.md` §Gate 2 |
| Gate 7 classification | Corrected mechanism to "Structural validator checks artifact fields; no custom tool interception" | `HARNESS_ADAPTER_DESIGN.md` §Gate 7 |
| Bypass analysis | Added 4-row analysis table evaluating shell deny trade-offs with conclusion and mitigation strategy | `HARNESS_ADAPTER_DESIGN.md` §Custom Tool Bypass Analysis |
| Ralph loop history | Recorded iteration 1 findings (3 defects) and iteration 2 (no-op by evidence) | `HARNESS_ADAPTER_DESIGN.md` §Ralph Loop History |
| Packaging manifest | Added YAML examples for `runtime/harness_config.json` and `runtime/runner.py` manifest entries | `HARNESS_ADAPTER_DESIGN.md` §Packaging Manifest Entries |
| Gate priority ordering | Defined priority: Gate 4 > Gate 3 > Gate 1 > Gate 2 > Gate 5 > Gate 6 > Gate 7 | `HARNESS_ADAPTER_DESIGN.md` §Gate Priority Ordering |
| Test strategy | Added 4 test categories: gate integration, bypass detection, policy compliance, domain pack integration | `HARNESS_ADAPTER_DESIGN.md` §Implementation Test Strategy |

### Post-Fix Verification

- All 7 findings addressed with concrete specifications
- Gate 2 whitelist prevents circular blocking without weakening enforcement
- Gate 7 classification now matches mechanism (structural validator, not custom tool)
- Bypass analysis table provides traceable trade-off reasoning
- Gate priority ordering gives Phase 6C clear implementation sequence
- Small-model executable: priority ordering, test categories, and whitelist mechanism provide explicit targets

## Design Quality Assessment

### Phase 6A (MCP Adapter)
- **One-core-two-frontends principle**: MCP adapter wraps existing runtime functions without duplicating validation logic
- **Mode 1/Mode 2**: MCP SDK (optional) and stdlib JSON-RPC fallback align with Phase 0.5 dependency policy
- **Tool catalog**: 8 tools covering all runtime validators, next-prompt compiler, and runner commands
- **Error handling**: Consistent MCP error format with `error_code`, `message`, and `details` fields

### Phase 6B (Harness Adapter)
- **Enforcement classification**: Hard-blocked (Gate 4), orchestrated (Gates 1-3, 5-6), deterministic-only (Gate 7) — honest about limitations
- **Capability matrix**: 7 gates mapped to opencode allow/ask/deny permissions with explicit bypass limitations
- **No user config modification**: Design identifies integration points without claiming unsupported hard blocking

## Validation Evidence

- **204 pytest tests**: All pass (`python -m pytest tests/ -v`)
- **`validate_skills.py`**: All 7 skills OK
- **`token_budget.py --strict`**: All skills within budget
- **CLI `domain-pack validate`**: All 6 runtime packs PASS

## File Sizes

| File | Lines | Status |
|---|---|---|
| `MCP_ADAPTER_DESIGN.md` | 325 | A-level |
| `HARNESS_ADAPTER_DESIGN.md` | 287 | A-level |

## Carry-Forward to Phase 6C

- Follow gate priority ordering: Gate 4 > Gate 3 > Gate 1 > Gate 2 > Gate 5 > Gate 6 > Gate 7
- Implement MCP dispatch registry from explicit 8-entry mapping table
- Implement `validate_all` batch tool with sequential aggregation
- Implement shell whitelist for Gate 2 validation commands
- Test against all 6 runtime domain packs
- ISSUE-1 (packaging flattening) remains unresolved; blocks Phase 8B rollout

## Observations

1. **MCP adapter is thin by design** — wraps existing runtime functions without adding validation logic. This keeps the one-core-two-frontends principle intact and avoids drift between CLI and MCP validation behavior.

2. **Harness adapter is honest about limitations** — only Gate 4 can be hard-blocked. Other gates are orchestrated or deterministic-only. This aligns with Decision 1 (hybrid enforcement) and avoids overstating enforcement capabilities.

3. **Custom tool bypass is accepted by design** — denying `shell` would close raw bash bypass but also block validation commands. The recommended approach accepts the bypass and provides runner visibility for human reviewers.

4. **Gate priority ordering reflects risk** — Gate 4 (external action approval) is highest priority because it provides hard blocking for irreversible actions. Lower-priority gates are orchestrated or advisory.
