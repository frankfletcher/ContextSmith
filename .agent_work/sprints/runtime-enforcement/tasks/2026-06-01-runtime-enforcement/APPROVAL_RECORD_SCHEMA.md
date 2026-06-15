# Approval Record Schema

## Artifact Manifest

- artifact_type: artifact-schema
- parent_task: TASK.md
- phase: 1B.5
- version: 1.0.0
- formats: json

## Purpose

The approval record documents authorization for irreversible, external, private, costly, or high-risk actions. It does not automate the action — it records whether approval exists, who granted or denied it, and what residual risk remains. An approval record with status `requested` or `denied` means the action must not proceed.

## Schema

Each approval record corresponds to a single action requiring authorization.

### Required Fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Unique approval identifier (e.g., `appr-001`) |
| `requirement_ids` | string[] | Requirement chain IDs this approval relates to |
| `action` | string | Description of the action requiring approval |
| `side_effect_tier` | string | One of `read_only`, `local_write`, `external_read`, `external_write`, `irreversible` |
| `requester` | string | Agent, skill, or user that requested the action |
| `approver` | string | User or system that approved, or `not_yet_approved` |
| `status` | string | One of `not_required`, `requested`, `approved`, `denied`, `waived_by_user` |
| `timestamp` | string | ISO 8601 timestamp of the approval decision, or `pending` |
| `evidence_id` | string | Evidence ledger entry ID (e.g., `ev-078`) or a free-text source note describing the approval evidence |
| `residual_risk` | string | Risk disclosure for high-risk actions, or `none` |

### Optional Fields

| Field | Type | Description |
| --- | --- | --- |
| `domain` | string | Domain label (e.g., `travel_purchase`, `scheduling`, `software`) |
| `denial_reason` | string | Explanation when status is `denied` |
| `waiver_notes` | string | Explanation when status is `waived_by_user` |
| `expires_at` | string | ISO 8601 timestamp after which the approval is no longer valid |

## Status Semantics

| Status | Meaning | Action may proceed? |
| --- | --- | --- |
| `not_required` | The action does not require approval (e.g., read-only, low-risk) | Yes, no approval needed |
| `requested` | Approval has been requested but not yet granted | No — must wait |
| `approved` | A user or authorized system has granted approval | Yes — with evidence |
| `denied` | A user or authorized system has rejected the action | No — do not proceed |
| `waived_by_user` | The user explicitly waived the approval requirement | Yes — with waiver evidence |

## Complete Example: Travel Purchase

### Step 1: Agent requests approval for a flight purchase

```json
{
  "artifact_type": "approval_record",
  "id": "appr-001",
  "requirement_ids": ["req-010"],
  "action": "Purchase round-trip flight: SFO to LAX on 2026-06-15, return 2026-06-20, 1 passenger, $342.50",
  "side_effect_tier": "irreversible",
  "requester": "travel-agent",
  "approver": "not_yet_approved",
  "status": "requested",
  "timestamp": "pending",
  "evidence_id": "ev-078",
  "residual_risk": "Fare may change before checkout. Refund policy: non-refundable within 24 hours of departure. Baggage fee of $40 per checked bag not included in quoted price.",
  "domain": "travel_purchase"
}
```

### Step 2: User explicitly approves the purchase

```json
{
  "artifact_type": "approval_record",
  "id": "appr-001",
  "requirement_ids": ["req-010"],
  "action": "Purchase round-trip flight: SFO to LAX on 2026-06-15, return 2026-06-20, 1 passenger, $342.50",
  "side_effect_tier": "irreversible",
  "requester": "travel-agent",
  "approver": "user:frank",
  "status": "approved",
  "timestamp": "2026-06-02T14:23:00Z",
  "evidence_id": "ev-079",
  "residual_risk": "Fare may change before checkout. Refund policy: non-refundable within 24 hours of departure. Baggage fee of $40 per checked bag not included in quoted price.",
  "domain": "travel_purchase"
}
```

### Step 3: Alternative — user denies the purchase

```json
{
  "artifact_type": "approval_record",
  "id": "appr-001",
  "requirement_ids": ["req-010"],
  "action": "Purchase round-trip flight: SFO to LAX on 2026-06-15, return 2026-06-20, 1 passenger, $342.50",
  "side_effect_tier": "irreversible",
  "requester": "travel-agent",
  "approver": "user:frank",
  "status": "denied",
  "timestamp": "2026-06-02T14:25:00Z",
  "evidence_id": "ev-079",
  "residual_risk": "none",
  "denial_reason": "User prefers to book manually after comparing additional airlines",
  "domain": "travel_purchase"
}
```

## Validation Rules

1. `id` must be unique within the approval set.
2. `requirement_ids` must be non-empty — every approval traces to at least one requirement.
3. `action` must be non-empty and specific enough to identify the action without additional context.
4. `side_effect_tier` must be one of the five allowed values.
5. `status` must be one of `not_required`, `requested`, `approved`, `denied`, `waived_by_user`.
6. If `status` is `approved`, `approver` must not be `not_yet_approved` and `timestamp` must not be `pending`.
7. If `status` is `denied`, `approver` must not be `not_yet_approved` and `timestamp` must not be `pending`.
8. If `status` is `requested`, `approver` must be `not_yet_approved` and `timestamp` must be `pending`.
9. If `status` is `not_required`, `approver` may be `none` and `timestamp` may be `none`.
10. If `side_effect_tier` is `external_write` or `irreversible`, `residual_risk` must not be empty.
11. If `status` is `waived_by_user`, `waiver_notes` is recommended.
12. An approval record with `status` other than `approved` or `waived_by_user` does not imply permission to proceed.

## YAML Representation (Deferred)

The Phase 2 validator accepts JSON only. This YAML shape is a documentation aid for future parser support and is not currently accepted by `runtime/validator.py`.

```yaml
artifact_type: approval_record
id: appr-001
requirement_ids:

  - req-010

action: "Purchase round-trip flight: SFO to LAX on 2026-06-15, return 2026-06-20, 1 passenger, $342.50"
side_effect_tier: irreversible
requester: travel-agent
approver: not_yet_approved
status: requested
timestamp: pending
evidence_id: ev-078
residual_risk: >
  Fare may change before checkout. Refund policy: non-refundable within
  24 hours of departure. Baggage fee of $40 per checked bag not included
  in quoted price.
domain: travel_purchase
```
