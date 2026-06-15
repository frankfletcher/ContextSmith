---
name: contextsmith-workflow-developer
description: Generate workflow configs from natural language intent. Delegates to the orchestrator using its own meta-config. Use when you need to create a workflow config YAML, plan a multi-phase project, or generate task-state files for structured execution.
metadata:
  version: "2.2.0"
  package: ContextSmith
  target: local-open-weight-models
---

# ContextSmith Workflow Developer

Generate workflow configs from natural language intent. This skill invokes the orchestrator with its own meta-config at `workflow_config.yaml`, which defines 6 phases for config generation: gather requirements, select domain template, customize config, validate, confirm, and output.

## Quick Use

```
/contextsmith-workflow-developer
```

## How It Works

The skill delegates to `contextsmith-orchestrator` with the meta-config at `workflow_config.yaml`. The orchestrator executes the 6-phase workflow defined there, which handles all structured questioning, template selection, customization, validation, confirmation, and output.

The meta-config phases:

| Phase | What Happens |
| ------- | ------------- |
| `gather_requirements` | Ask 4 structured questions about domain, task, inputs, and success criteria |
| `select_domain_template` | Pick the best domain template from references/domain-templates/ |
| `customize_config` | Fill in the selected template with gathered requirements |
| `validate_config` | Validate against workflow_config.schema.json; re-enter customize on failure |
| `confirm_config` | Show config to user for yes/no/modify decision |
| `output_config` | Write final config and companion task-state files |

## Output

The orchestrator produces:

1. `workflow_config.yaml` — schema-validated workflow config
2. `TASK.md` — task definition (objective, scope, constraints)
3. `PLAN.md` — human-readable phase plan (derived from the config)
4. `STATUS.md` — initial status (state = init)
5. `CONTEXT.md` — file map and constraints
6. `CHECKLIST.md` — validation checklist

## After Generation

After generating the config, offer:

1. **Run now** — invoke `contextsmith-orchestrator` with the new config
2. **Edit first** — present the config for manual editing
3. **Save only** — write files to task-state directory, user runs later

## Reference Loading

| Need | Read |
| ------ | ------ |
| Meta-config details | `workflow_config.yaml` |
| Domain templates | `references/domain-templates/<domain>.yaml` |
| Config schema detail | `schemas/workflow_config.schema.json` |
| Structured questioning | `shared/structured-questioning.md` |
