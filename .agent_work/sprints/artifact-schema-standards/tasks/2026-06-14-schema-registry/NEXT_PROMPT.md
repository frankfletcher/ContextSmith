# NEXT_PROMPT.md

You are continuing work on the ContextSmith artifact schema standards task.

## Current Status
- Phase: 9 of 10
- Sub-phase: 9.1
- State: execute

## Sub-phase
Sub-phase 9.1: Schema registry docs

## Sub-phase Tasks
- [ ] Write docs/reference/ARTIFACT_SCHEMAS.md
- [ ] Document PLAN.md hierarchical format
- [ ] Add examples of sub-phase structure

## Your Task
Write user-facing documentation for the artifact schema registry. Create `docs/reference/ARTIFACT_SCHEMAS.md` documenting:
- The purpose of the schema registry (`schemas/artifact_schemas.yaml`)
- How schemas are structured (phase_tree content rule, required/optional sections)
- PLAN.md hierarchical format (### Phase, #### Sub-phase, - [x] Task)
- Examples of sub-phase structure with tasks, metadata, and completion tracking
- STATUS.md Current Sub-phase optional section
- How validation uses schemas (via `validators.validate_artifact_schema()`)

## Input Files
- STATUS.md: Current workflow state
- PLAN.md: Phase plan with all 10 phases
- CONTEXT.md: Project context
- CHECKLIST.md: Task tracking
- schemas/artifact_schemas.yaml: Artifact schema registry
- orchestrator/validators.py: Schema loading and validation
- orchestrator/state_reader.py: Plan/status parsing logic
- shared/documentation-quality.md: Documentation quality reference
- docs/contributing/documentation-review-checklist.md: Review criteria
- docs/reference/VERSIONING.md: Existing doc for style reference

## Output Requirements
- Create `docs/reference/ARTIFACT_SCHEMAS.md`
- Document PLAN.md hierarchical format with examples
- Use the project voice from docs/contributing/
- Must pass markdownlint
- Update CHECKLIST.md
- Create .new segment files for EDUCATIONAL_REPORT.md, AUDIT_REPORT.md, PHASE_LOG.md

## Constraints
- Context Budget: 24k
- Do not modify orchestrator code or schemas
- Follow existing doc style from docs/reference/VERSIONING.md
- Must pass full validation suite on completion

### REPORT FILES: USE `.new` SEGMENTS — BUT MERGE MANUALLY

The orchestrator (with `.new` auto-merging) is part of the planned build, NOT the current runtime. Until it ships:

1. Write `.new` segment files as specified below (this prepares for orchestrator adoption).
2. **After writing**, manually merge the `.new` content into the parent file by appending.
3. **Then remove** the `.new` file.

This is a transitional requirement. See DECISIONS.md D12 for the full rationale.

Write these `.new` segment files (and merge manually):

- `EDUCATIONAL_REPORT.md.new` — new sub-phase explanation entry
- `AUDIT_REPORT.md.new` — new audit rubric entry
- `PHASE_LOG.md.new` — new phase log entry
- `DECISIONS.md.new` — new decision entry

## Ralph Loop Enforcement
3 iterations required. Each is critique+fix. Do not skip or collapse.

## Self-Audit
Before closeout, verify:
- Original phase goal satisfied or blocker recorded
- All validation commands executed or blocker documented
- Side-effect boundaries respected
- Task state updated with compact facts

## Hard Stop
Current phase is Phase 9: Documentation.
Do not proceed beyond it. Do not edit files outside this phase scope.

## Expected Output Format

```
## Result
[summary of changes]

## Evidence
[list of files modified]

## Validation
[validation checks performed and results]

## Risks / Next Action
[any risks or blockers, next sub-phase]
```
