# DECISIONS.md

## D1: Schema Registry Format

- Decision: Use YAML for artifact schema registry
- Reason: YAML is human-readable, supports comments, and aligns with existing workflow config format
- Impact: Schemas are easy to review and edit manually

## D2: Schema Location

- Decision: Place schema registry at `schemas/artifact_schemas.yaml`
- Reason: Co-locates with other schemas (`workflow_config.schema.json`, `agent_config.schema.json`)
- Impact: Clear separation of concerns, easy to find

## D3: Backward Compatibility

- Decision: Preserve `section_requirements` in workflow config as an override mechanism
- Reason: Existing workflows use this; breaking change would require migration
- Impact: Workflows can extend base schemas without modifying the registry

## D4: Validation Strictness

- Decision: Required sections are enforced; optional sections are not; additional sections are allowed
- Reason: LLMs need flexibility to add structure; required sections ensure parseability
- Impact: Validators check for required sections, ignore extras

## D5: Phase → Sub-phase → Task Hierarchy

- Decision: PLAN.md uses 3-level hierarchy with ### phases, #### sub-phases, and checkbox tasks
- Reason: Small models need fine-grained execution units; sub-phases have independent context budgets
- Impact: Orchestrator dispatches one sub-phase at a time with fresh sessions; tasks are progress markers within sub-phases

## D6: Orchestrator Controls Sub-phase Advancement

- Decision: Orchestrator tracks current sub-phase via STATUS.md Current Sub-phase field and auto-advances after successful execution
- Reason: Keeps execution in sync with plan; agent never chooses its own next sub-phase
- Impact: State machine transitions only fire when all sub-phases in a phase are complete; EXIT_CONTINUE is returned between sub-phases

## D7: Agent Owns PLAN.md Tasks, Orchestrator Owns STATUS.md Sub-phase

- Decision: Orchestrator never writes PLAN.md; agent checks off tasks. Orchestrator only updates STATUS.md Current Sub-phase field
- Reason: Clear separation of concerns; avoids format-preservation complexity
- Impact: Orchestrator advances sub-phases via STATUS.md; agent reads both STATUS.md and PLAN.md to determine work

## D8: `.new` File Segments Replace Direct Agent Appends

- Decision: Agents write `.new` segment files (EDUCATIONAL_REPORT.md.new); orchestrator merges them into parent files after execution
- Reason: Removes the agent from the append operation entirely — agents cannot overwrite accumulated history if they never touch the parent file. The existing snapshot/repair mechanism was detective (catches overwrites), this is preventive (prevents them).
- Impact: Orchestrator.orchestrator._merge_new_artifact_segments() scans for .new files matching APPEND_ONLY_FILES entries, validates content (non-empty, section heading check), appends to parent, removes .new segment. PHASE_START_PROMPT.md steps 6-8 direct agents to write .new files instead of appending directly.

## D9: Persistent Lint Error Counter

- Decision: Accumulate lint error frequencies in .agent_work/lint_error_counts.json across all validation runs
- Reason: A one-liner per run shows current errors only. Accumulating across multiple subphases surfaces trends (e.g., "MD022 fired 47 times across 9 subphases") which tells you which rule to add to coding standards.
- Impact: scripts/lint_error_counter.py is a 60-line stdin filter with no dependencies. Piped after ruff and markdownlint in AGENTS.md validation commands. View top 10 with: python -c "import json; d=json.load(open('.agent_work/lint_error_counts.json')); [print(f'{v:4d} {k}') for k,v in sorted(d.items(), key=lambda x:-x[1])[:10]]"

## D10: RESULT.json Removed from PROTECTED_FILES

- Decision: Remove RESULT.json from the PROTECTED_FILES set in orchestrator.py
- Reason: PROTECTED_FILES causes `_safe_write` to force append mode. RESULT.json is written fresh each phase by the agent via the harness adapter (not via `_safe_write`), so the protection was misleading dead code. Keeping it creates risk if someone later uses `_safe_write` with RESULT.json — it would append instead of overwrite.
- Impact: No behavioral change. The agent continues to write RESULT.json directly. The protection set now contains only true append-only files.

## D11: extend_base Defaults to True for artifact_schemas Overrides

- Decision: The extend_base field in ArtifactSchemaOverride defaults to true
- Reason: Merge-by-default is least-surprise behavior. A workflow author adding required_sections to an override expects them to augment (not replace) the base schema sections. Explicit opt-in to replace mode prevents accidental section loss.
- Impact: Validators.py._build_artifact_overrides() unions override required_sections with base when extend_base is true; replaces entirely when false. additional_sections always merges regardless.

## D12: Orchestrator Gap — .new Merging Not Available at Runtime (SUPERSEDED by D15)

- Decision: Document that the orchestrator (with `.new` file auto-merging) is part of the planned build, not the current runtime. Agents must manually merge `.new` segments into parent files for now.
- Reason: The orchestrator's `_merge_new_artifact_segments()` is implemented in `orchestrator/orchestrator.py` but the current production ContextSmith does not use the orchestrator. Agents using `.new` conventions will have orphaned segments unless they merge manually.
- Impact: Contradiction — agents are directed to write `.new` files (to prepare for orchestrator adoption) but must also manually merge them (because the orchestrator isn't running). When the orchestrator ships, agents must stop manually merging. CONTEXT.md now documents this as a known constraint.
- When to revisit: Resolved. See D15. The orchestrator IS the production runtime. Agents must NOT merge `.new` files manually — `_merge_new_artifact_segments()` handles it.

## D13: ARTIFACT_SCHEMAS.md Content Scope

- **Decision**: Document all 6 required topics in a single reference file, with the validation pipeline documented in depth (loader → single-check → bulk-check → config override → phase-tree)
- **Reason**: The schema registry is a cross-cutting concern — documentation that covers only the YAML format would leave users guessing how validation works. Including the pipeline makes the doc self-contained.
- **Impact**: The document is more useful as a single reference but may need updating if the validation pipeline gains new functions

## D14: Orchestrator Adoption Gate (RESOLVED — see D15)

- **Decision**: Define the concrete condition for when orchestrator `.new` auto-merging activates and manual merging stops. The gate triggers when BOTH conditions are met:
  1. The orchestrator's `_merge_new_artifact_segments()` has been exercised by at least one end-to-end integration test that verifies auto-merge replaces manual `cat >>` correctly.
  2. A workflow config exists in the repo that routes through `orchestrator.run()` as the production entry point (not just unit-test invocation).
- **Reason**: Vague conditions ("when the orchestrator ships" from D12) leave ambiguity. Agents need a checkable rule they can evaluate without asking.
- **Resolution**: Condition 1 was met during Phase 8 (5 tests in test_orchestrator_integration.py). Condition 2 is met by D15 commitment — the orchestrator IS the production runtime. D14 gate is now considered passed. See D15 for the commitment and migration plan.
- **When to revisit**: Resolved. Agents should check D14_GATE_PASSED sentinel in .agent_work/ to determine merge strategy.

## D15: Orchestrator-as-Runtime Commitment

- **Decision**: The orchestrator is the production runtime for ContextSmith. `.new` file auto-merging activates. Manual merging stops. The orchestrator CLI (`contextsmith-orchestrator` / `python -m orchestrator`) is the primary entry point, and skills may also invoke it programmatically.
- **Reason**: The project built elaborate infrastructure (sub-phase advancement, auto-merge, checkpoint management, workflow config dispatch) that depends on the orchestrator being the runtime. The D14 gate conditions are met (end-to-end tests exist, commitment is now explicit). Continuing manual merging would maintain a known gap indefinitely.
- **Impact**:
  - `.new` file auto-merging via `_merge_new_artifact_segments()` is now the production path. Agents must NOT merge `.new` files manually.
  - D12 is superseded — the orchestrator gap is closed.
  - A `D14_GATE_PASSED` sentinel file in `.agent_work/` provides a machine-checkable flag.
  - AGENTS.md, CONTEXT.md updated to reflect orchestrator-as-runtime.
  - NEXT_PROMPT.md templates updated: remove manual-merge instructions, rely on orchestrator merge.
- **Unresolved**: The orchestrator CLI must be installed via `pip install -e .` or equivalent (Phase 12.1). Until then, the runtime is available from the repo checkout but not from a release install.
