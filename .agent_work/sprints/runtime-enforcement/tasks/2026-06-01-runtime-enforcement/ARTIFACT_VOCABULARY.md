# Universal Artifact Vocabulary

## Artifact Manifest
- artifact_type: artifact-vocabulary
- parent_task: TASK.md
- phase: 1A
- version: 1.0.0
- formats: json

## Purpose

Define the six artifact types used across all domains. Each artifact is a compact data structure a model can emit and a validator can check.

---

## 1. requirements_chain

**Purpose:** Traces original user requirements through phases and evidence so nothing is silently dropped.

**Required fields:**
- `id` — unique requirement identifier
- `source` — original text or path to source artifact
- `domain` — domain label (e.g., `software`, `writing`, `scheduling`, `general`)
- `phase_ids` — list of phase IDs that satisfy this requirement
- `evidence_ids` — list of evidence ledger entries that prove satisfaction
- `status` — one of `pending`, `passed`, `blocked`, `waived_by_user`

**Example:**
```json
{
  "artifact_type": "requirements_chain",
  "id": "req-001",
  "source": "User asked to schedule a meeting across three time zones",
  "domain": "scheduling",
  "phase_ids": ["phase-3c"],
  "evidence_ids": ["ev-012"],
  "status": "pending"
}
```

---

## 2. phase_contract

**Purpose:** Bounds a single execution phase so the model knows what it must accomplish and cannot drift.

**Required fields:**
- `phase_id` — unique phase identifier
- `objective` — one-sentence description of what this phase must produce
- `domain` — domain label matching the requirements chain
- `allowed_actions` — list of permitted action categories
- `disallowed_actions` — list of forbidden action categories
- `validation_commands` — commands or checks that must pass before the phase can close
- `max_artifacts` — upper bound on output artifacts to prevent scope creep
- `status` — one of `active`, `completed`, `blocked`, `cancelled`

**Example:**
{
  "artifact_type": "phase_contract",
  "phase_id": "phase-1a",
  "objective": "Define six universal artifact types with purpose, fields, and examples",
  "domain": "general",
  "allowed_actions": ["read", "write", "validate"],
  "disallowed_actions": ["execute_model", "external_api", "git_force"],
  "validation_commands": ["python scripts/validate_skills.py"],
  "max_artifacts": 6,
  "status": "active"
}

---

## 3. domain_pack

**Purpose:** Encapsulates domain-specific validation gates and approval boundaries without making the core domain-specific.

**Required fields:**
- `domain` — domain name (e.g., `software`, `travel_purchase`, `general_fallback`)
- `triggers` — conditions that activate this pack
- `required_artifacts` — artifact types this domain requires
- `validation_gates` — object of named validation checks specific to this domain
- `approval_gates` — actions that require explicit user approval
- `external_action_boundaries` — what external actions are allowed, blocked, or require approval
- `residual_risk` — domain-specific risk disclosures

**Example:**
```json
{
  "artifact_type": "domain_pack",
  "domain": "scheduling",
  "triggers": ["meeting", "calendar", "availability"],
  "required_artifacts": ["requirements_chain", "phase_contract", "evidence_ledger", "approval_record"],
  "validation_gates": {
    "participants_known": {
      "description": "All meeting participants identified",
      "required": true,
      "check_type": "field_presence"
    },
    "candidate_slots_listed": {
      "description": "Candidate time slots listed with availability status",
      "required": true,
      "check_type": "field_presence"
    }
  },
  "approval_gates": ["send_invite", "modify_calendar"],
  "external_action_boundaries": {
    "read_calendar": "allowed",
    "send_invite": "requires_approval",
    "delete_event": "blocked"
  },
  "residual_risk": "Time zone data may be stale; final invite should be verified by user before sending"
}
```

---

## 4. evidence_ledger

**Purpose:** Records declared obligations and the evidence that satisfies them, so validators can check claims against proof.

**Required fields:**
- `id` — unique evidence identifier
- `requirement_id` — requirement this evidence satisfies
- `phase_id` — phase that produced this evidence
- `claim` — what was declared or promised
- `evidence` — concrete proof (file path, command output, artifact reference, or observation)
- `evidence_type` — one of `file`, `command_output`, `artifact`, `observation`, `user_confirmation`
- `verified` — boolean, true if a validator or human confirmed the evidence
- `timestamp` — ISO 8601 timestamp or `pending`

**Example:**
```json
{
  "artifact_type": "evidence_ledger",
  "id": "ev-001",
  "requirement_id": "req-001",
  "phase_id": "phase-1a",
  "claim": "Six artifact types defined with purpose, fields, and examples",
  "evidence": ".agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/ARTIFACT_VOCABULARY.md",
  "evidence_type": "file",
  "verified": false,
  "timestamp": "pending"
}
```

---

## 5. approval_record

**Purpose:** Documents authorization for irreversible, external, private, costly, or high-risk actions.

**Required fields:**
- `id` — unique approval identifier
- `requirement_ids` — requirements this approval relates to
- `action` — description of the action requiring approval
- `side_effect_tier` — one of `read_only`, `local_write`, `external_read`, `external_write`, `irreversible`
- `requester` — who or what requested the action
- `approver` — who approved, or `not_yet_approved`
- `status` — one of `not_required`, `requested`, `approved`, `denied`, `waived_by_user`
- `timestamp` — ISO 8601 timestamp of approval or `pending`
- `evidence_id` — evidence ledger entry ID or source note for approval evidence
- `residual_risk` — risk disclosure for high-risk actions, or `none`

**Example:**
```json
{
  "artifact_type": "approval_record",
  "id": "appr-001",
  "requirement_ids": ["req-003"],
  "action": "Send calendar invite to three external participants",
  "side_effect_tier": "external_write",
  "requester": "scheduling-agent",
  "approver": "not_yet_approved",
  "status": "requested",
  "timestamp": "pending",
  "evidence_id": "ev-013",
  "residual_risk": "Invite cannot be recalled once sent; participants may have conflicting commitments"
}
```

---

## 6. phase_closeout

**Purpose:** Validates that a phase is complete before advancing, recording what was done, what evidence exists, and whether it's safe to proceed.

**Required fields:**
- `phase_id` — phase being closed out
- `objective_met` — boolean, true if the phase objective was achieved
- `artifacts_produced` — list of output artifact paths or IDs
- `evidence_ids` — evidence ledger entries for this phase
- `validation_results` — list of validation check results with pass/fail status
- `blockers` — list of unresolved blockers, or empty if none
- `carry_forward` — facts, files, and decisions needed by the next phase
- `next_phase_id` — ID of the next phase, or `none` if this is the final phase
- `status` — one of `passed`, `failed`, `blocked`, `waived_by_user`

**Example:**
```json
{
  "artifact_type": "phase_closeout",
  "phase_id": "phase-1a",
  "objective_met": true,
  "artifacts_produced": ["ARTIFACT_VOCABULARY.md"],
  "evidence_ids": ["ev-001"],
  "validation_results": [
    {"check": "six_artifacts_defined", "result": "pass"},
    {"check": "all_domain_neutral", "result": "pass"},
    {"check": "json_valid", "result": "pass"}
  ],
  "blockers": [],
  "carry_forward": ["artifact names and field sets for Phase 1B schema detail"],
  "next_phase_id": "phase-1b",
  "status": "passed"
}
```
