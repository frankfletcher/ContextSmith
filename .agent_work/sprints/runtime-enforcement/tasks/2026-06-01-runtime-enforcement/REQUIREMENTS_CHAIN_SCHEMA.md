# Requirements Chain Schema

## Artifact Manifest

- artifact_type: artifact-schema
- parent_task: TASK.md
- phase: 1B
- version: 1.0.0
- formats: json

## Purpose

The requirements chain traces original user requirements through phases and evidence. It prevents a model from satisfying only the current prompt while forgetting earlier requirements.

## Schema

Each entry in the requirements chain is a single requirement with trace fields.

### Required Fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Unique requirement identifier (e.g., `req-001`) |
| `source` | string | Original user text or path to source artifact |
| `domain` | string | Domain label (e.g., `software`, `writing`, `scheduling`, `general`) |
| `side_effect_tier` | string | One of `read_only`, `local_write`, `external_read`, `external_write`, `irreversible` |
| `validation_method` | string | How satisfaction is verified: `command`, `artifact_check`, `evidence_review`, `user_confirmation`, `none` |
| `phase_ids` | string[] | Phase IDs that satisfy this requirement |
| `evidence_ids` | string[] | Evidence ledger entry IDs that prove satisfaction |
| `status` | string | One of `pending`, `passed`, `blocked`, `waived_by_user` |

### Optional Fields

| Field | Type | Description |
| --- | --- | --- |
| `parent_id` | string | ID of a parent requirement this refines |
| `approval_id` | string | Linked approval record for high-risk requirements |
| `notes` | string | Additional context for the validator or next-phase executor |

## Trace Model

The trace model is linear. A requirement starts as `pending`, accumulates `phase_ids` and `evidence_ids` as phases complete, and transitions to `passed`, `blocked`, or `waived_by_user`.

```
Task request
  -> requirements_chain created (status: pending)
  -> Phase executes, adds phase_id
  -> Phase produces evidence, adds evidence_id
  -> Validator checks evidence against validation_method
  -> status transitions to passed, blocked, or waived_by_user
```

No graph logic is needed. Each requirement is independent. Parent-child relationships use `parent_id` for optional grouping.

## Complete Trace Example

### Step 1: Task request creates the requirement

```json
{
  "artifact_type": "requirements_chain",
  "id": "req-001",
  "source": "User asked to summarize three research papers on prompt engineering and produce a comparison table",
  "domain": "research",
  "side_effect_tier": "read_only",
  "validation_method": "artifact_check",
  "phase_ids": [],
  "evidence_ids": [],
  "status": "pending"
}
```

### Step 2: Phase 3F executes and adds phase_id

```json
{
  "artifact_type": "requirements_chain",
  "id": "req-001",
  "source": "User asked to summarize three research papers on prompt engineering and produce a comparison table",
  "domain": "research",
  "side_effect_tier": "read_only",
  "validation_method": "artifact_check",
  "phase_ids": ["phase-3f"],
  "evidence_ids": [],
  "status": "pending"
}
```

### Step 3: Phase produces evidence and adds evidence_id

```json
{
  "artifact_type": "requirements_chain",
  "id": "req-001",
  "source": "User asked to summarize three research papers on prompt engineering and produce a comparison table",
  "domain": "research",
  "side_effect_tier": "read_only",
  "validation_method": "artifact_check",
  "phase_ids": ["phase-3f"],
  "evidence_ids": ["ev-045"],
  "status": "pending"
}
```

### Step 4: Validator confirms evidence, status transitions

```json
{
  "artifact_type": "requirements_chain",
  "id": "req-001",
  "source": "User asked to summarize three research papers on prompt engineering and produce a comparison table",
  "domain": "research",
  "side_effect_tier": "read_only",
  "validation_method": "artifact_check",
  "phase_ids": ["phase-3f"],
  "evidence_ids": ["ev-045"],
  "status": "passed"
}
```

## Validation Rules

1. `id` must be unique within the chain.
2. `source` must be non-empty.
3. `domain` must match a known domain pack or `general`.
4. `side_effect_tier` must be one of the five allowed values.
5. `validation_method` must be one of the five allowed values.
6. `status` must be one of `pending`, `passed`, `blocked`, `waived_by_user`.
7. If `status` is `passed`, at least one `phase_id` and one `evidence_id` must be present.
8. If `status` is `waived_by_user`, a `notes` field explaining the waiver is recommended.

## YAML Representation (Deferred)

The Phase 2 validator accepts JSON only. This YAML shape is a documentation aid for future parser support and is not currently accepted by `runtime/validator.py`.

```yaml
artifact_type: requirements_chain
id: req-001
source: "User asked to summarize three research papers on prompt engineering and produce a comparison table"
domain: research
side_effect_tier: read_only
validation_method: artifact_check
phase_ids:

  - phase-3f

evidence_ids:

  - ev-045

status: passed
```
