# Phase 0 Small-Model Executor Prompt

## Artifact Manifest

- artifact_type: phase-execution-prompt
- parent_task: `.agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/`
- phase: Phase 0 Packaging Discovery
- executor_profile: small/local model
- target_profile: qwen36
- context_length: 64k
- interaction: silent unless blocked
- validation: required
- audit: required
- education_level: deep
- side_effects: read-only except task-state closeout edits
- hard_stop: do not start Phase 0.5 or Phase 1

## Mission

Execute **Phase 0 only**.

Your job is to discover how ContextSmith packaging currently works so later phases can decide where runtime validator code, schemas, domain packs, fixtures, and metadata could live.

Do **not** make architecture decisions.

Do **not** implement runtime validators.

Do **not** edit package scripts.

Do **not** continue to Phase 0.5.

Stop after recording Phase 0 facts, validation evidence, audit results, and the next prompt for human/frontier review.

## Read First

Read only these files first:

1. `.agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/STATUS.md`
2. `.agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/PLAN.md`
3. `.agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/CONTEXT.md`
4. `.agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/CHECKLIST.md`
5. `.agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/DECISIONS.md`

Then inspect only the Phase 0 input files:

1. `scripts/build_release.py`
2. `scripts/package_skill.sh`
3. `scripts/sync_shared_refs.py`
4. `scripts/token_budget.py`
5. `skills/*/reference_manifest.yml`
6. `PACKAGE_SPEC.md` read-only only if needed for packaging context

## Phase 0 Contract

~~~yaml
context_contract:
  executor: small-model
  phase_type: discovery
  usable_phase_budget: moderate
  expected_tool_calls: 4-8 reads, optional 1 dry-run command, 0 source edits
  validation_output_budget: brief
  validation_output_reserve: reserve room for validation summaries and audit notes
  compaction_trigger: summarize include/exclude behavior for each packaging path
  stop_rule: stop if packaging behavior conflicts across scripts
~~~

## Questions To Answer

Answer these with file/path evidence:

1. What files are included in individual skill zip packages?
2. What files are included in the release bundle?
3. Does staging copy only `SKILL.md` and references, or arbitrary files too?
4. Can executable runtime files ship inside installed skills?
5. Can YAML schemas ship?
6. Can fixtures ship?
7. Can domain packs ship?
8. Does any script exclude files that runtime enforcement would need?
9. Is a separate runtime package likely needed?
10. What questions must Phase 0.5 decide?

## Allowed Actions

You may:

- read files;
- inspect directories;
- run one safe documented dry-run command if needed;
- update task-state files listed below;
- run required validation commands.

You may not:

- edit source files outside the task-state folder;
- edit `PACKAGE_SPEC.md`;
- add dependencies;
- change packaging behavior;
- start Phase 0.5;
- decide runtime surface scope;
- implement validators, MCP tools, runner code, or domain packs.

## Required Task-State Updates

At Phase 0 closeout, update these files compactly:

- `CONTEXT.md`: packaging facts, exact file evidence, include/exclude behavior.
- `DECISIONS.md`: only durable facts or pending decision requests. Do not choose architecture unless evidence makes it trivial and safe.
- `STATUS.md`: Phase 0 complete or blocked, validation status, next required action.
- `PHASE_LOG.md`: one compact Phase 0 entry.
- `ARTIFACTS.md`: files inspected, commands run, validation evidence.
- `CHECKLIST.md`: check only items supported by evidence.
- `NEXT_PROMPT.md`: prompt for Phase 0.5 human/frontier review.

## Required Validation

Run these before closeout:

~~~bash
python scripts/validate_skills.py
python scripts/token_budget.py --strict
~~~

If either fails:

1. Do not fix source files unless the fix is explicitly in Phase 0 scope.
2. Record the failure in `STATUS.md`, `PHASE_LOG.md`, and `ARTIFACTS.md`.
3. Use the recovery procedure in `PLAN.md`.
4. Stop.

Do not run pytest in Phase 0 unless runtime tests already exist and Phase 0 changed runtime/test files. Phase 0 should normally not need pytest.

## Required Audit

Before final response, perform a concise self-audit:

- Did I execute only Phase 0?
- Did I avoid Phase 0.5 decisions?
- Did every packaging claim cite evidence?
- Did I avoid editing source/package files?
- Did I update all required task-state files?
- Did validation pass or did I record a blocker?
- Did I keep raw command output out of task-state files?
- Did I write a clear `NEXT_PROMPT.md` for human/frontier review?

## Recovery Procedure

If blocked:

1. Stop Phase 0.
2. Set `STATUS.md` to blocked.
3. Record the failed gate and impact.
4. Add a `PHASE_LOG.md` entry.
5. Mark partial artifacts in `ARTIFACTS.md`.
6. Write `NEXT_PROMPT.md` with at most three options:
   - fix packaging discovery issue;
   - narrow Phase 0 scope;
   - ask human/frontier reviewer to decide.
7. Do not continue to Phase 0.5.

## Final Output Required

Return this format:

````markdown

## Phase 0 Result

- status: complete|blocked
- one-sentence summary

## Packaging Facts
| Area | Finding | Evidence |
| --- | --- | --- |
| Individual skill zip | ... | `path:line` or command |
| Release bundle | ... | `path:line` or command |
| Staging sync | ... | `path:line` or command |
| Runtime files | ... | `path:line` or command |
| Schemas/domain packs/fixtures | ... | `path:line` or command |

## Validation

- `python scripts/validate_skills.py`: passed|failed|not run with reason
- `python scripts/token_budget.py --strict`: passed|failed|not run with reason

## Task-State Updates

- `CONTEXT.md`: updated|not updated
- `DECISIONS.md`: updated|not updated
- `STATUS.md`: updated|not updated
- `PHASE_LOG.md`: updated|not updated
- `ARTIFACTS.md`: updated|not updated
- `CHECKLIST.md`: updated|not updated
- `NEXT_PROMPT.md`: updated|not updated

## Self-Audit

- Phase boundary honored: yes|no
- Source files unchanged: yes|no
- Evidence cited: yes|no
- Validation completed or blocker recorded: yes|no
- Raw output avoided in task state: yes|no

## Deep Education Notes
Explain briefly:

- why Phase 0 is discovery-only;
- why packaging facts must come before runtime design;
- why Phase 0.5 must be human/frontier review;
- what the next reviewer should decide.

## Hard Stop
I stopped after Phase 0. Phase 0.5 requires user/human/frontier review before continuing.
````

