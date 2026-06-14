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
