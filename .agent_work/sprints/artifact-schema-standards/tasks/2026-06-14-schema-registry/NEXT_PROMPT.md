# NEXT_PROMPT.md

You are continuing work on the ContextSmith artifact schema standards task.

## Current Status
- Phase: 10 of 11
- Sub-phase: 10.1
- State: execute

## Sub-phase
Sub-phase 10.1: Implementation plan audit

## Sub-phase Tasks
- [ ] Run implementation plan audit
- [ ] Fix any must-fix items

## Your Task
Run the implementation plan audit across all phases of the artifact schema standards project. Review:

1. Whether Phases 1-9 were delivered to spec
2. Whether the implementation plan (PLAN.md) accurately reflects what was built
3. Whether any must-fix gaps exist
4. Whether the validation pipeline documents are consistent with the implementation

Fix any must-fix items found during the audit. Record findings in the audit report.

## Input Files
- STATUS.md: Current workflow state
- PLAN.md: Phase plan with all phases and tasks
- CONTEXT.md: Project context and constraints
- CHECKLIST.md: Task tracking
- ARTIFACTS.md: Artifact inventory
- PHASE_LOG.md: Phase history
- EDUCATIONAL_REPORT.md: Per-phase educational reports
- AUDIT_REPORT.md: Audit findings
- DECISIONS.md: Design decisions
- schemas/artifact_schemas.yaml: Artifact schema registry
- schemas/workflow_config.schema.json: Workflow config schema
- orchestrator/validators.py: Validation functions
- orchestrator/state_reader.py: State parsing
- orchestrator/orchestrator.py: Main orchestrator
- shared/implementation-plan-audit.md: Audit reference
- shared/project-audit.md: Full project audit prompt

## Output Requirements
- Run the audit and record findings
- Fix any must-fix items found
- Update CHECKLIST.md
- Create .new segment files for EDUCATIONAL_REPORT.md, AUDIT_REPORT.md, PHASE_LOG.md

## Constraints
- Context Budget: 16k
- Do not introduce new features or scope
- Do not modify schemas or orchestrator code unless fixing a must-fix bug
- Follow existing doc style

### REPORT FILES: USE `.new` SEGMENTS — BUT MERGE MANUALLY

The orchestrator (with `.new` auto-merging) is part of the planned build, NOT the current runtime. Until it ships:

1. Write `.new` segment files as specified below (this prepares for orchestrator adoption).
2. **After writing**, manually merge the `.new` content into the parent file by appending.
3. **Then remove** the `.new` file.

Write these `.new` segment files (and merge manually):
- `EDUCATIONAL_REPORT.md.new` — new sub-phase explanation entry
- `AUDIT_REPORT.md.new` — new audit rubric entry
- `PHASE_LOG.md.new` — new phase log entry
- `DECISIONS.md.new` — new decision entry (if any)

## Ralph Loop Enforcement
3 iterations required. Each is critique+fix. Do not skip or collapse.

## Self-Audit
Before closeout, verify:
- Original phase goal satisfied or blocker recorded
- All validation commands executed or blocker documented
- Side-effect boundaries respected
- Task state updated with compact facts

## Hard Stop
Current phase is Phase 10: Final Audit and Validation.
Do not proceed beyond it. Do not edit files outside this phase scope.
Do not fix nice-to-have items — only must-fix.

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
