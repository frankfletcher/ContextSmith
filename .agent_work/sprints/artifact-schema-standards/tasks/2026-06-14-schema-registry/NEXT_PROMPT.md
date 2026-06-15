# NEXT_PROMPT.md

You are continuing work on the ContextSmith artifact schema standards task.

## Current Status

- Phase: 11 of 11
- Sub-phase: 11.1
- State: execute

## Sub-phase
Sub-phase 11.1: Extra-audit workflow config

## Sub-phase Tasks

- [x] Create .contextsmith/audit-with-extra.json workflow config [ALREADY EXISTS — verified in Phase 10.1]
- [ ] Validate config against schema
- [ ] Test with dry run

## Your Task
The `.contextsmith/audit-with-extra.json` workflow config already exists. It chains `audit_current_phase` → `extra_audit` with read-only permissions. Your job is to:

1. **Validate** the config against `schemas/workflow_config.schema.json` — at minimum check that it satisfies the schema (all required fields, valid transitions, valid phase_order, valid domain enum).
2. **Test with a dry run** — use a safe command to verify the orchestrator can parse and validate the config. If no dry-run command exists, verify by running structural validation and recording the result.
3. **Document findings** — if the config passes validation, record that. If there are schema violations, fix them.

## Input Files

- `.contextsmith/audit-with-extra.json`: Existing workflow config (audit + extra_audit chaining)
- `.contextsmith/workflow.json`: Reference workflow config (for comparison)
- `schemas/workflow_config.schema.json`: Schema definition
- `STATUS.md`: Current workflow state
- `PLAN.md`: Phase plan with all phases and tasks
- `CONTEXT.md`: Project context and constraints
- `CHECKLIST.md`: Task tracking
- `ARTIFACTS.md`: Artifact inventory
- `PHASE_LOG.md`: Phase history
- `shared/extra-audit.md`: Extra-audit reference (strategic lenses)
- `shared/project-audit.md`: Full project audit prompt

## Output Requirements

- Validate config against schema — record result in CHECKLIST.md
- Test with dry run or structural validation — record result
- Create .new segment files for EDUCATIONAL_REPORT.md, AUDIT_REPORT.md, PHASE_LOG.md

## Constraints

- Context Budget: 8k
- Do not introduce new features or scope
- Do not modify schemas or orchestrator code unless fixing a must-fix bug
- Follow existing doc and JSON style conventions

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
Current phase is Phase 11: Tooling and Audit Infrastructure.
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
