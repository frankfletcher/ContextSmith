# Evidence Ledger Core

Use this core reference for every ContextSmith run. Use `evidence-ledger.md` only when the full YAML shape or examples are needed.

## Required Evidence

Every completed run records compact evidence for:

- active parameters and their sources
- selected domain and interaction mode
- run mode and side-effect tier
- validation result, command/check, or blocker
- self-audit result when required
- Ralph required/completed count and material changes/no-op reason
- changed files or produced artifacts
- declared-vs-enforced status for each required obligation
- residual risks and next action

## Allowed Status Values

- `evidence_present`
- `not_required_by_contract`
- `blocked_with_reason`
- `missing_evidence`

If any required item is `missing_evidence`, the run is not complete.

## Compact Final Evidence

```markdown

## Evidence

- Parameters: ...
- Validation: passed|failed|blocked|not_required (...)
- Self-Audit: passed|issues_found|blocked|not_required
- Ralph: required N, completed M (...)
- Declared vs Enforced: all evidenced | blocked with reason | missing evidence
```
