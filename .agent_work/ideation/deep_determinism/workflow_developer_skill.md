# Workflow Developer Skill

Generates workflow configs from natural language intent. Uses structured questions to gather requirements, then produces a schema-validated config YAML plus companion task-state files.

## Quick Use

```
/contextsmith-workflow-developer
```

The skill asks structured questions to determine the workflow shape, then generates the config.

## Input Gathering (Page-Flow)

The skill gathers input through structured questions, one at a time. Uses the harness's question tool (e.g., `AskUserQuestion` in OpenCode) for multiple-choice questions.

### Step 1: Understand Intent

If the user provides a clear intent (e.g., "implement error recovery"), skip to Step 2. Otherwise, ask:

```
Question: "What kind of workflow should I create?"
Header: "Workflow Type"
Options:
  - Label: "Coding"
    Description: "Software engineering: implement, test, review, deploy"
  - Label: "Writing"
    Description: "Content creation: draft, edit, review, publish"
  - Label: "Research"
    Description: "Analysis: gather sources, synthesize, audit, report"
  - Label: "Migration"
    Description: "Refactoring: plan, execute, validate, rollback"
  - Label: "Audit"
    Description: "Review existing work: evaluate, report, recommend"
```

### Step 2: Gather Parameters

Ask 2-3 questions to fill in missing parameters. Skip any the user already provided.

**Domain (if not clear from intent):**
```
Question: "What domain does this work fall into?"
Header: "Domain"
Options:
  - Label: "Coding"
    Description: "Software engineering, repo work, scripts"
  - Label: "Writing"
    Description: "Documentation, content, copy"
  - Label: "Research"
    Description: "Analysis, investigation, synthesis"
  - Label: "General"
    Description: "Doesn't fit a specific domain"
```

**Quality level:**
```
Question: "How much review should the output get?"
Header: "Quality Level"
Options:
  - Label: "Quick"
    Description: "One pass, minimal review, fast delivery"
  - Label: "Standard"
    Description: "Audit gate + validation, balanced quality"
  - Label: "Thorough"
    Description: "Audit + Ralph loops + validation, highest quality"
```

**Harness (if not detected):**
```
Question: "Which agent harness will run this workflow?"
Header: "Harness"
Options:
  - Label: "OpenCode"
    Description: "Full orchestrator support, agent profiles, RESULT.json"
  - Label: "Generic"
    Description: "Any harness, skill-only mode, no infrastructure"
  - Label: "Cursor"
    Description: "Cursor with .cursorrules, inline results"
```

### Step 3: Confirm

Present a summary table and ask for approval.

```
→ Workflow config will be generated:

  ┌──────────────────┬────────────────────────────────────────┐
  │ Intent           │ Implement error recovery               │
  │ Domain           │ coding                                 │
  │ Quality          │ standard                               │
  │ Harness          │ opencode                               │
  │ Phases           │ load → implement → audit → validate → close │
  │ Gates            │ audit, validate                        │
  │ Ralph cycles     │ 0                                      │
  │ Permissions      │ read-only (audit), edit (implement)    │
  └──────────────────┴────────────────────────────────────────┘

  [Yes, generate it] [No, let me modify → restart at Step 2]
```

**Yes**: generate the config and task-state files.
**No**: re-enter at Step 2 (not Step 1 — the user already chose their workflow type).

## Workflow Shape Determination

Select a domain template, then customize based on the user's answers.

### Domain Templates

Each template defines default phases, gates, permissions, and outputs.

**Coding:**
```yaml
phases: load_context → implement_change → audit_output → validate → close
gates: audit, validate
permissions: read-only (audit), edit (implement), read-only (validate)
```

**Writing:**
```yaml
phases: load_context → draft → review → revise → close
gates: review
permissions: edit (draft), read-only (review), edit (revise)
```

**Research:**
```yaml
phases: load_context → research → synthesize → audit → close
gates: audit
permissions: read-only (research), edit (synthesize), read-only (audit)
```

**Migration:**
```yaml
phases: load_context → plan_migration → execute_migration → validate → close
gates: validate
permissions: read-only (plan), edit (execute), read-only (validate)
```

**Audit:**
```yaml
phases: load_context → audit_output → report → close
gates: audit
permissions: read-only (audit), edit (report)
```

### Customization

Based on the user's quality level answer:
- **Quick**: skip audit gate, reduce max_retries to 1
- **Standard**: keep defaults
- **Thorough**: add Ralph loops (ralph_critique → ralph_revise), increase max_retries

Based on the user's intent:
- If the intent mentions "review" or "evaluate" → add audit gate
- If the intent mentions "test" or "validate" → add validate gate
- If the intent mentions "deploy" or "publish" → add external-action permission to close phase
- If the intent mentions "approval" → add human_approval_gate overlay

## Output

The skill produces:

1. `workflow_config.yaml` — schema-validated workflow config
2. `TASK.md` — task definition (objective, scope, constraints)
3. `PLAN.md` — human-readable phase plan (derived from the config)
4. `STATUS.md` — initial status (state = init)
5. `CONTEXT.md` — file map and constraints
6. `CHECKLIST.md` — validation checklist

These files form the initial task-state directory.

## Validation

Before presenting the config, validate:
1. Schema validation against `workflow_config.schema.json`
2. Required phases present (init, execute, closeout)
3. At least one path to `done` (reachability)
4. All transitions reference valid states
5. Permissions are consistent

If validation fails, revise and retry (up to 3 times). If all retries fail, present the errors to the user.

## Overlay Generation

When the user wants to modify an existing workflow:
- Read the existing workflow config
- Generate an overlay that adds/removes steps
- Validate the overlay against the base config
- Present the resolved phase_order for approval

## After Generation

After generating the config, offer:
1. **Run now** — invoke the orchestrator (skill-only or harness-aware)
2. **Edit first** — present the config for manual editing
3. **Save only** — write files to task-state directory, user runs later

## Reference Loading

| Need | Read |
|------|------|
| Every run | `shared/structured-questioning.md`, `shared/persistent-task-state.md` |
| Schema detail | `workflow_config_sketch.md` (in deep_determinism) |
| Domain templates | `references/domain-templates/<domain>.yaml` |
| Overlay mechanics | `workflow_config_sketch.md` overlay section |

## Token Budget

Target: under 250 lines for the skill itself. Domain templates loaded conditionally.
- Skill: ~250 lines (~700 tokens)
- One domain template: ~50 lines (~150 tokens)
- Structured questioning reference: ~100 lines (~300 tokens, shared)
- Total on invocation: ~1150 tokens

## Related Docs

- `shared/structured-questioning.md` for the questioning pattern
- `workflow_config_sketch.md` for the config schema
- `orchestrator_as_skill.md` for the two execution paths
- `implementation_prerequisites.md` section 9 for the plan generation gap
