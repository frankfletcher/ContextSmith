# DECISIONS.md

## D1: Schema Registry Format
**Decision**: Use YAML for artifact schema registry
**Reason**: YAML is human-readable, supports comments, and aligns with existing workflow config format
**Impact**: Schemas are easy to review and edit manually

## D2: Schema Location
**Decision**: Place schema registry at `schemas/artifact_schemas.yaml`
**Reason**: Co-locates with other schemas (`workflow_config.schema.json`, `agent_config.schema.json`)
**Impact**: Clear separation of concerns, easy to find

## D3: Backward Compatibility
**Decision**: Preserve `section_requirements` in workflow config as an override mechanism
**Reason**: Existing workflows use this; breaking change would require migration
**Impact**: Workflows can extend base schemas without modifying the registry

## D4: Validation Strictness
**Decision**: Required sections are enforced; optional sections are not; additional sections are allowed
**Reason**: LLMs need flexibility to add structure; required sections ensure parseability
**Impact**: Validators check for required sections, ignore extras

## D5: Phase → Sub-phase → Task Hierarchy
**Decision**: PLAN.md uses 3-level hierarchy with ### phases, #### sub-phases, and checkbox tasks
**Reason**: Small models need fine-grained execution units; sub-phases have independent context budgets
**Impact**: Orchestrator dispatches one sub-phase at a time with fresh sessions; tasks are progress markers within sub-phases

## D6: Orchestrator Controls Sub-phase Advancement
**Decision**: Orchestrator tracks current sub-phase via STATUS.md "Current Sub-phase" field and auto-advances after successful execution
**Reason**: Keeps execution in sync with plan; agent never chooses its own next sub-phase
**Impact**: State machine transitions only fire when all sub-phases in a phase are complete; EXIT_CONTINUE is returned between sub-phases

## D7: Agent Owns PLAN.md Tasks, Orchestrator Owns STATUS.md Sub-phase
**Decision**: Orchestrator never writes PLAN.md; agent checks off tasks. Orchestrator only updates STATUS.md "Current Sub-phase" field
**Reason**: Clear separation of concerns; avoids format-preservation complexity
**Impact**: Orchestrator advances sub-phases via STATUS.md; agent reads both STATUS.md and PLAN.md to determine work
