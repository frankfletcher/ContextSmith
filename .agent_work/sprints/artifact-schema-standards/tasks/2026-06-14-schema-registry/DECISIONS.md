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
- Reason: PROTECTED_FILES causes _safe_write to force append mode. RESULT.json is written fresh each phase by the agent via the harness adapter (not via _safe_write), so the protection was misleading dead code. Keeping it creates risk if someone later uses _safe_write with RESULT.json — it would append instead of overwrite.
- Impact: No behavioral change. The agent continues to write RESULT.json directly. The protection set now contains only true append-only files.

## D11: extend_base Defaults to True for artifact_schemas Overrides

- Decision: The extend_base field in ArtifactSchemaOverride defaults to true
- Reason: Merge-by-default is least-surprise behavior. A workflow author adding required_sections to an override expects them to augment (not replace) the base schema sections. Explicit opt-in to replace mode prevents accidental section loss.
- Impact: Validators.py._build_artifact_overrides() unions override required_sections with base when extend_base is true; replaces entirely when false. additional_sections always merges regardless.

## D12: Orchestrator Gap — .new Merging Not Available at Runtime

- Decision: Document that the orchestrator (with `.new` file auto-merging) is part of the planned build, not the current runtime. Agents must manually merge `.new` segments into parent files for now.
- Reason: The orchestrator's `_merge_new_artifact_segments()` is implemented in `orchestrator/orchestrator.py` but the current production ContextSmith does not use the orchestrator. Agents using `.new` conventions will have orphaned segments unless they merge manually.
- Impact: Contradiction — agents are directed to write `.new` files (to prepare for orchestrator adoption) but must also manually merge them (because the orchestrator isn't running). When the orchestrator ships, agents must stop manually merging. CONTEXT.md now documents this as a known constraint.
- When to revisit: Remove this note and stop manual merging when the orchestrator is deployed as the production runtime (see PLAN.md Phase 5+).

## D13: ARTIFACT_SCHEMAS.md Content Scope

- **Decision**: Document all 6 required topics in a single reference file, with the validation pipeline documented in depth (loader → single-check → bulk-check → config override → phase-tree)
- **Reason**: The schema registry is a cross-cutting concern — documentation that covers only the YAML format would leave users guessing how validation works. Including the pipeline makes the doc self-contained.
- **Impact**: The document is more useful as a single reference but may need updating if the validation pipeline gains new functions

## D14: Orchestrator Adoption Gate

- **Decision**: Define the concrete condition for when orchestrator `.new` auto-merging activates and manual merging stops. The gate triggers when BOTH conditions are met:
  1. The orchestrator's `_merge_new_artifact_segments()` has been exercised by at least one end-to-end integration test that verifies auto-merge replaces manual `cat >>` correctly.
  2. A workflow config exists in the repo that routes through `orchestrator.run()` as the production entry point (not just unit-test invocation).
- **Reason**: Vague conditions ("when the orchestrator ships" from D12) leave ambiguity. Agents need a checkable rule they can evaluate without asking. EITHER condition alone is insufficient — the code could work in tests but lack a real config, or a config could exist but the auto-merge path could be untested.
- **Impact**: Until D14 gate passes, agents continue merging `.new` segments manually. After the gate fires, manual merging becomes a bug (the orchestrator handles it). D12 should be revisited when the gate fires — remove the "manually merge" instruction and remove D14 as resolved.
- **When to revisit**: Check at the start of each phase. If both conditions are met, remove D14, update D12 to simply state "orchestrator handles merging", remove manual-merge instructions from NEXT_PROMPT.md templates, and stop appending in this session.
