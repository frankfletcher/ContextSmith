# Task: Implement Deep Determinism Orchestrator

## Objective

Implement the ContextSmith deterministic execution system as specified in `.agent_work/ideation/deep_determinism/`. The system has two execution paths (skill-only and harness-aware) that share identical workflow configs, artifact contracts, checkpoint formats, and validation rules.

## Scope

### In Scope

1. **Schemas** — workflow config and agent config JSON schemas (done, verify + test fixtures)
2. **Core orchestrator** — Python state machine with outer loop, state reader, step compiler, checkpoint manager
3. **Harness adapters** — HarnessAdapter ABC, OpenCode adapter, generic adapter
4. **Validators** — file existence, schema validation, content checks
5. **Orchestrator skill** — SKILL.md for skill-only execution path
6. **Workflow developer skill** — SKILL.md for generating workflow configs from intent
7. **Integration** — wire orchestrator into contextsmith-run, router integration
8. **Testing** — unit tests, integration tests, test fixtures

### Out of Scope

- GUI or web interface
- MCP adapter
- ACP adapter
- Additional harness adapters beyond OpenCode and generic
- Production deployment
- Performance optimization

## Constraints

- Python 3.10+
- No new dependencies without approval (PyYAML and jsonschema already required)
- Follow existing code conventions (PEP 8 for Python, ATX headings for Markdown)
- Keep SKILL.md under 500 lines
- All schemas must validate against existing examples
- All phases must produce artifacts that can be validated by the runtime validator

## Success Criteria

1. `python scripts/validate_skills.py` passes
2. `python -m runtime.cli` validates all artifact types
3. Orchestrator can load a workflow config and execute it end-to-end
4. Skill-only path works without Python infrastructure
5. Harness-aware path works with OpenCode adapter
6. All existing tests pass
7. New tests cover orchestrator, adapters, and validators

## Dependencies

- `schemas/workflow_config.schema.json` — done
- `schemas/agent_config.schema.json` — done
- `runtime/validator.py` — exists, may need updates
- `runtime/cli.py` — exists, may need updates
- `shared/` references — exist, used by skills
