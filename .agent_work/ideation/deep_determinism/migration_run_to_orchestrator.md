# Migration: contextsmith-run to Orchestrator

This doc explains how existing `contextsmith-run` users transition to the orchestrator model (either path). It covers what changes, what stays the same, and how to migrate without breaking existing workflows.

## What Stays the Same

The orchestrator inherits most of its contracts from `contextsmith-run`. These are unchanged:

| Component | Status |
| ----------- | -------- |
| Task-state directory layout | Unchanged |
| Artifact files (STATUS.md, PLAN.md, NEXT_PROMPT.md, etc.) | Unchanged |
| Execution contract format | Unchanged |
| Evidence ledger format | Unchanged |
| Domain packs | Unchanged |
| Ralph loop behavior | Unchanged |
| Validation gates (runtime + domain) | Unchanged |
| Control parameters (--mode, --target-profile, etc.) | Unchanged |
| Reference manifest format | Unchanged |

Users who have task-state directories from `contextsmith-run` can use them with the orchestrator without modification.

## What Changes

### 1. Workflow config becomes the source of truth

`contextsmith-run` infers workflow shape from the input type (prompt, plan, task-state folder). The orchestrator reads a workflow config YAML that declares the shape explicitly.

**Before (contextsmith-run):**

```
User: /contextsmith-run the prompt in NEXT_PROMPT.md
→ Skill detects task-state handoff
→ Skill infers phases from PLAN.md
→ Skill executes current phase
```

**After (orchestrator):**

```
User: /contextsmith-orchestrator the workflow in workflow_config.yaml
→ Orchestrator reads config
→ Orchestrator reads STATUS.md for current phase
→ Orchestrator executes according to config
```

### 2. Loop control moves out of the skill

`contextsmith-run` has its own loop logic (phased-run mode, Ralph loops, self-audit). The orchestrator moves this logic into either:

- Python code (harness-aware path)
- A separate orchestrator skill (skill-only path)

`contextsmith-run` becomes a simpler skill that handles single prompts and one-shot tasks. Phased work goes to the orchestrator.

### 3. Validation becomes external

`contextsmith-run` validates artifacts within the skill (the agent checks its own work). The orchestrator validates externally:

- Harness-aware: validators run after the agent subprocess exits
- Skill-only: the agent validates per the orchestrator skill's instructions (less reliable, but still structured)

### 4. RESULT.json protocol

The orchestrator expects agents to write `RESULT.json` to the task-state directory. `contextsmith-run` doesn't use this — it infers status from artifact presence and validation results.

**Migration:** Existing agents don't need to write RESULT.json immediately. The orchestrator falls back to artifact presence + exit code when RESULT.json is missing. RESULT.json can be added incrementally.

## Migration Paths

### Path A: Keep contextsmith-run, add orchestrator for new work

No changes to existing setup. Use the orchestrator for new phased workflows. Keep `contextsmith-run` for simple prompts and one-shot tasks.

**When to use:** You have existing workflows that work. You want to try the orchestrator without risk.

### Path B: Migrate existing task-state directories

Existing task-state directories from `contextsmith-run` work with the orchestrator as-is. The only addition needed is a workflow config file.

**Steps:**

1. Create a `workflow_config.yaml` that describes your workflow's phases
2. Place it in the task-state directory (or reference it from the orchestrator)
3. Run the orchestrator instead of `contextsmith-run`

**Example config for a simple audit workflow:**

```yaml
workflow_id: my-audit
version: 1
domain: coding
mode: phased-run

baseline:
  required_steps:

    - load_context
    - audit_output
    - close

  required_gates:

    - audit

  required_files:

    - STATUS.md
    - PLAN.md
    - CONTEXT.md

states:
  load_context:
    state: init
    agent: contextsmith-planner
    permissions: read-only
    max_retries: 2
    timeout_s: 30
    transitions:

      - condition: pass

        target: audit_output

      - condition: fail

        target: blocked
    expected_outputs: []
    inputs:

      - STATUS.md
      - PLAN.md

  audit_output:
    state: audit
    agent: contextsmith-auditor
    permissions: read-only
    max_retries: 3
    timeout_s: 300
    transitions:

      - condition: pass

        target: close

      - condition: fail

        target: audit_output

      - condition: max_retries

        target: blocked
    expected_outputs:

      - AUDIT_REPORT.md

    inputs:

      - PLAN.md
      - CONTEXT.md

  close:
    state: closeout
    agent: contextsmith-closer
    permissions: edit
    max_retries: 2
    timeout_s: 60
    transitions:

      - condition: pass

        target: done

      - condition: fail

        target: close
    expected_outputs:

      - SUMMARY.md
      - NEXT_PROMPT.md

    inputs:

      - STATUS.md
      - AUDIT_REPORT.md

phase_order:

  - load_context
  - audit_output
  - close

validation:
  schema: schemas/workflow_config.schema.json
  required_checks:

    - file_exists
    - json_schema
```

### Path C: Full migration (orchestrator-only)

Replace all `contextsmith-run` usage with the orchestrator. This is the long-term goal but not required for MVP.

**Steps:**

1. Install the orchestrator (pip install or skill-only)
2. Create workflow configs for all recurring workflows
3. Update router to dispatch to orchestrator for phased work
4. Keep `contextsmith-run` only for simple one-shot prompts

## Backward Compatibility

The orchestrator is backward-compatible with `contextsmith-run` in these ways:

- **Task-state directories:** Identical format. No migration needed.
- **Artifacts:** Identical templates. No migration needed.
- **References:** All shared references are unchanged.
- **Domain packs:** Unchanged.
- **Control parameters:** Unchanged (the orchestrator reads the same flags).

The only breaking change is that the orchestrator expects a workflow config. If you don't have one, the orchestrator can generate a default from the task-state directory (reading phases from PLAN.md), but this is less reliable than an explicit config.

## Coexistence Model

During the transition, both skills can coexist:

```
/contextsmith-run        → simple prompts, one-shot tasks
/contextsmith-orchestrator → phased workflows, long-running work
/contextsmith-workflow-developer → generates configs for the orchestrator
```

The router skill (`contextsmith`) dispatches to the right one based on intent:

- "Run this prompt" → `contextsmith-run`
- "Execute this workflow" → `contextsmith-orchestrator`
- "Create a workflow for..." → `contextsmith-workflow-developer`

## Timeline

| Phase | What | When |
| ------- | ------ | ------ |
| MVP | Orchestrator skill + OpenCode companion | Immediate |
| Transition | Router dispatches to orchestrator for phased work | After MVP |
| Full migration | Orchestrator replaces contextsmith-run for phased work | After validation |
| Deprecation | contextsmith-run becomes single-prompt-only | Optional |

## Related Docs

- `orchestrator_as_skill.md` for the two execution paths
- `workflow_developer_skill.md` for config generation
- `workflow_config_sketch.md` for the config schema
- `implementation_prerequisites.md` for the full gap analysis
