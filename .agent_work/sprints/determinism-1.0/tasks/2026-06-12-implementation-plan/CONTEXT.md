# Context

## Project

ContextSmith — meta-skills package for model-aware agent instruction engineering.

## Task Directory

`.agent_work/sprints/determinism-1.0/tasks/2026-06-12-implementation-plan/`

## Key Files

### Schemas (done)

- `schemas/workflow_config.schema.json` — workflow config validation
- `schemas/agent_config.schema.json` — agent config validation

### Spec Files (in `.agent_work/ideation/deep_determinism/`)

- `orchestrator_idea.md` — state machine, CLI, checkpoint, error matrix
- `orchestrator_and_harness.md` — HarnessAdapter ABC, StepContract, HarnessResult
- `workflow_config_sketch.md` — config schema, examples, overlay mechanics
- `agent_start_and_communication.md` — LaunchPacket, artifact collection
- `communications_protocol_sketch.md` — message schemas, protocol flow
- `audit_and_ralph_state_machine.md` — transition matrix, counter management
- `harness_agnostic_distribution.md` — adapter lifecycle, reference loading
- `orchestrator_as_skill.md` — skill-only path, companion model
- `workflow_developer_skill.md` — plan generation, domain templates
- `orchestrator_skill_draft.md` — concrete SKILL.md for skill-only path
- `state_artifact_strategy.md` — artifact templates, validation
- `harness-opencode.md` — OpenCode CLI flags (verified)
- `domain-templates/` — 6 domain templates

### Runtime (exists)

- `runtime/validator.py` — structural validators
- `runtime/cli.py` — CLI entry point
- `runtime/domain_packs/` — domain validation rules

### Shared References (exists)

- `shared/persistent-task-state.md` — task state layout
- `shared/control-parameters-core.md` — parameter parsing
- `shared/run-configuration-preview.md` — confirmation pattern
- `shared/structured-questioning.md` — question tool usage

## Constraints

- Python 3.10+
- No new dependencies without approval
- PEP 8 for Python
- ATX headings for Markdown
- SKILL.md under 500 lines
- All schemas must validate existing examples
- All phases must produce validatable artifacts

## Assumptions

- PyYAML and jsonschema are available
- OpenCode is installed (for adapter testing)
- Existing tests in `tests/` will not break
- The orchestrator module will live at `orchestrator/` in the project root

## Skip Rules

- Do not modify existing schemas unless validation fails
- Do not modify existing runtime modules unless integration requires it
- Do not add new shared references unless the skill needs them
- Do not create harness adapters beyond OpenCode and generic
