# Evidence Ledger

The evidence ledger proves that declared controls were enforced.

## Required Fields

```yaml
evidence_ledger:
  parameters_applied:
    target_profile: qwen36
    context_length: 64k
    interaction: refine
    ralph: 2
    validation: strict
  domain:
    selected: frontend-ux
    source: repo_evidence_and_user_answer
  execution:
    run_mode: phase
    side_effects: file-editing
    changed_files: []
  validation:
    status: passed|failed|blocked|not_required
    commands_or_checks: []
  self_audit:
    status: passed|issues_found|blocked
    material_findings: []
  ralph:
    required: 2
    completed: 2
    material_changes: []
  declared_vs_enforced: []
  residual_risks: []
  next_action: ""
```

## Declared-Vs-Enforced Status

Use one of:

- `evidence_present`
- `not_required_by_contract`
- `blocked_with_reason`
- `missing_evidence`

If any required item is `missing_evidence`, the run is not complete.

## Compact Final Format

For normal user-facing output, summarize the ledger:

```markdown

## Evidence

- Parameters: qwen36, 64k, refine, ralph=2, validation=strict
- Validation: passed (`npm test`)
- Self-audit: passed, no material findings
- Ralph: 2 iterations, revised validation wording
- Declared vs enforced: all required controls evidenced
```

For task-state runs, put durable evidence in `ARTIFACTS.md` or `PHASE_LOG.md` and keep the final response shorter.
