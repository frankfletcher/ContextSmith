# Extra Audit Workflow

Run the extra-audit step on your project task state. This runs the strategic-lens review from `shared/extra-audit.md` after baseline validation.

## Prerequisites

- A task state directory with `STATUS.md`, `PLAN.md`, `CONTEXT.md`
- The orchestrator dependencies installed (`uv sync`)

## CLI Path

Create a workflow config that chains the baseline audit and extra-audit:

```yaml

# .contextsmith/audit-with-extra.yaml
workflow_id: audit-with-extra
version: 1
domain: audit
harness: opencode

states:
  audit_current_phase:
    state: audit
    agent: contextsmith-auditor
    permissions: read-only
    max_retries: 2
    timeout_s: 300
    transitions:

      - condition: pass

        target: extra_audit

      - condition: fail

        target: audit_current_phase

      - condition: max_retries

        target: blocked
    expected_outputs:

      - AUDIT_REPORT.md

    inputs:

      - STATUS.md
      - PLAN.md

  extra_audit:
    state: extra_audit
    agent: contextsmith-auditor
    permissions: read-only
    max_retries: 2
    timeout_s: 300
    transitions:

      - condition: pass

        target: done

      - condition: fail

        target: extra_audit

      - condition: max_retries

        target: blocked
    expected_outputs:

      - EXTRA_AUDIT.md

    inputs:

      - AUDIT_REPORT.md
      - PLAN.md

phase_order:

  - audit_current_phase
  - extra_audit
```

Run it:

```bash
uv run python -m orchestrator \
  .contextsmith/audit-with-extra.yaml \
  .agent_work/sprints/<sprint>/tasks/<task>/ \
  --harness opencode
```

For a single-step dry run:

```bash
uv run python -m orchestrator \
  .contextsmith/audit-with-extra.yaml \
  .agent_work/sprints/<sprint>/tasks/<task>/ \
  --harness opencode \
  --single-step --dry-run
```

## Skill System Path

1. Invoke `/contextsmith-orchestrator` with a task-state directory that has a workflow config including the `extra_audit` state.
2. The orchestrator skill runs the state machine loop, executing the extra-audit step after the baseline audit.
3. The output is `EXTRA_AUDIT.md` in the task-state directory (append-only, merged from `EXTRA_AUDIT.md.new`).

## Ad-Hoc Path (No Task State)

If you do not have task state set up, just load the project-audit prompt directly:

```
Apply shared/project-audit.md to this project. Run the baseline checks, then load shared/extra-audit.md for the strategic review. Write findings to EXTRA_AUDIT.md.
```

## Output

The extra-audit step produces `EXTRA_AUDIT.md` in the task state directory. This file is append-only — each run adds a new section. The orchestrator auto-recovers it if overwritten and merges `.new` segments.
