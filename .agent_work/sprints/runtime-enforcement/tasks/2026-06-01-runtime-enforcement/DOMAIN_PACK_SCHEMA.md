# Domain Pack Schema

## Artifact Manifest
- artifact_type: artifact-schema
- parent_task: TASK.md
- phase: 1C
- version: 1.0.0
- formats: json

## Purpose

A domain pack encapsulates domain-specific validation gates and approval boundaries without making the core domain-specific. It is a compact data structure that tells a validator what to check and what requires human approval for a given domain.

## Schema

Each domain pack corresponds to a single domain.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `domain` | string | Domain name (e.g., `software_engineering`, `travel_purchase`, `general_fallback`) |
| `triggers` | string[] | Keywords or conditions that activate this pack (e.g., `["meeting", "calendar"]`) |
| `required_artifacts` | string[] | Artifact types this domain requires from the universal vocabulary |
| `validation_gates` | object | Named validation checks with pass/fail criteria |
| `approval_gates` | string[] | Actions that require explicit user approval before proceeding |
| `external_action_boundaries` | object | External actions mapped to `allowed`, `requires_approval`, or `blocked` |
| `residual_risk` | string | Domain-specific risk disclosures, or `none` |

### Optional Fields

| Field | Type | Description |
|---|---|---|
| `example_good_closeout` | object | Minimal example of a passing phase closeout for this domain |
| `example_blocked_closeout` | object | Minimal example of a blocked phase closeout for this domain |
| `notes` | string | Additional context for validators or domain pack authors |

### validation_gates Structure

Each entry in `validation_gates` is a named check:

```json
{
  "gate_name": {
    "description": "What this check verifies",
    "required": true,
    "check_type": "field_presence"
  }
}
```

The `check_type` field accepts one of: `field_presence`, `value_check`, `command`, `artifact_check`, `user_confirmation`.

### external_action_boundaries Structure

Maps action descriptions to permission levels:

```json
{
  "read_calendar": "allowed",
  "send_invite": "requires_approval",
  "delete_event": "blocked"
}
```

Allowed values: `allowed`, `requires_approval`, `blocked`.

## Starter Domain Packs

### 1. software_engineering

```json
{
  "artifact_type": "domain_pack",
  "domain": "software_engineering",
  "triggers": ["code", "implement", "refactor", "bug", "test", "deploy"],
  "required_artifacts": ["requirements_chain", "phase_contract", "evidence_ledger", "phase_closeout"],
  "validation_gates": {
    "changed_files_listed": {
      "description": "All modified source files are listed in the phase closeout",
      "required": true,
      "check_type": "field_presence"
    },
    "validation_command_run": {
      "description": "Project validation command (lint, test, build) executed or blocker recorded",
      "required": true,
      "check_type": "command"
    },
    "tests_addressed": {
      "description": "Tests added, updated, or test gap explained",
      "required": true,
      "check_type": "artifact_check"
    },
    "no_destructive_git": {
      "description": "No destructive git operations without explicit approval",
      "required": true,
      "check_type": "value_check"
    }
  },
  "approval_gates": ["deploy_staging", "deploy_production", "destructive_git_operation", "dependency_addition"],
  "external_action_boundaries": {
    "read_source_files": "allowed",
    "write_source_files": "allowed",
    "run_tests": "allowed",
    "deploy_staging": "requires_approval",
    "deploy_production": "requires_approval",
    "git_force_push": "blocked"
  },
  "residual_risk": "Code changes may have unintended side effects not caught by automated tests. Deployment to production requires explicit approval."
}
```

### 2. writing_editing

```json
{
  "artifact_type": "domain_pack",
  "domain": "writing_editing",
  "triggers": ["write", "edit", "rewrite", "draft", "proofread", "summarize"],
  "required_artifacts": ["requirements_chain", "phase_contract", "evidence_ledger", "phase_closeout"],
  "validation_gates": {
    "source_preserved": {
      "description": "Original source material or user intent preserved in output",
      "required": true,
      "check_type": "artifact_check"
    },
    "audience_tone_recorded": {
      "description": "Target audience, tone, and format are recorded or blocker noted",
      "required": true,
      "check_type": "field_presence"
    },
    "no_unsupported_facts": {
      "description": "Final draft does not introduce facts not present in source material",
      "required": true,
      "check_type": "artifact_check"
    },
    "constraints_traced": {
      "description": "Requested constraints (length, format, style) traced to output evidence",
      "required": true,
      "check_type": "artifact_check"
    }
  },
  "approval_gates": ["publish_externally", "send_to_third_party", "represent_as_final"],
  "external_action_boundaries": {
    "read_source_documents": "allowed",
    "write_drafts": "allowed",
    "publish_externally": "requires_approval",
    "send_to_third_party": "requires_approval"
  },
  "residual_risk": "Generated text may contain subtle factual errors or tone mismatches. External publication requires user review."
}
```

### 3. research_summary

```json
{
  "artifact_type": "domain_pack",
  "domain": "research_summary",
  "triggers": ["research", "summarize", "papers", "literature", "compare", "analyze"],
  "required_artifacts": ["requirements_chain", "phase_contract", "evidence_ledger", "phase_closeout"],
  "validation_gates": {
    "sources_listed": {
      "description": "All source materials listed with paths or URLs",
      "required": true,
      "check_type": "field_presence"
    },
    "unsupported_claims_flagged": {
      "description": "Claims not supported by sources are flagged or removed",
      "required": true,
      "check_type": "artifact_check"
    },
    "uncertainty_recorded": {
      "description": "Limitations and uncertainty in the research are recorded",
      "required": true,
      "check_type": "field_presence"
    },
    "claims_trace_to_evidence": {
      "description": "Quotes, statistics, and factual claims trace back to source evidence",
      "required": true,
      "check_type": "artifact_check"
    }
  },
  "approval_gates": ["publish_research", "submit_for_review", "cite_in_external_work"],
  "external_action_boundaries": {
    "read_source_materials": "allowed",
    "write_summaries": "allowed",
    "publish_research": "requires_approval",
    "submit_for_review": "requires_approval"
  },
  "residual_risk": "Summaries may oversimplify nuanced findings. Quotes and statistics should be verified against original sources before external use."
}
```

### 4. scheduling

```json
{
  "artifact_type": "domain_pack",
  "domain": "scheduling",
  "triggers": ["meeting", "calendar", "schedule", "availability", "timezone"],
  "required_artifacts": ["requirements_chain", "phase_contract", "evidence_ledger", "approval_record", "phase_closeout"],
  "validation_gates": {
    "participants_known": {
      "description": "All meeting participants identified",
      "required": true,
      "check_type": "field_presence"
    },
    "timezones_resolved": {
      "description": "Time zones for all participants resolved or blocker recorded",
      "required": true,
      "check_type": "value_check"
    },
    "duration_known": {
      "description": "Meeting duration specified",
      "required": true,
      "check_type": "field_presence"
    },
    "candidate_slots_listed": {
      "description": "Candidate time slots listed with availability status",
      "required": true,
      "check_type": "field_presence"
    }
  },
  "approval_gates": ["send_invite", "modify_calendar", "cancel_event"],
  "external_action_boundaries": {
    "read_calendar": "allowed",
    "propose_slots": "allowed",
    "send_invite": "requires_approval",
    "modify_calendar": "requires_approval",
    "delete_event": "blocked"
  },
  "residual_risk": "Time zone data may be stale. Calendar availability may change between check and send. Final invites should be verified by user before sending."
}
```

### 5. travel_purchase

```json
{
  "artifact_type": "domain_pack",
  "domain": "travel_purchase",
  "triggers": ["flight", "hotel", "book", "travel", "fare", "purchase"],
  "required_artifacts": ["requirements_chain", "phase_contract", "evidence_ledger", "approval_record", "phase_closeout"],
  "validation_gates": {
    "constraints_recorded": {
      "description": "Dates, airports, passenger count, and travel constraints recorded",
      "required": true,
      "check_type": "field_presence"
    },
    "price_source_recorded": {
      "description": "Price source and timestamp recorded for each option",
      "required": true,
      "check_type": "field_presence"
    },
    "fees_terms_recorded": {
      "description": "Fees, baggage, and refund/cancellation terms recorded or unavailable noted",
      "required": true,
      "check_type": "field_presence"
    },
    "no_purchase_without_approval": {
      "description": "No purchase, payment, or irreversible action without explicit user approval",
      "required": true,
      "check_type": "value_check"
    }
  },
  "approval_gates": ["purchase_ticket", "make_payment", "book_hotel", "modify_booking"],
  "external_action_boundaries": {
    "search_flights": "allowed",
    "search_hotels": "allowed",
    "compare_prices": "allowed",
    "purchase_ticket": "requires_approval",
    "make_payment": "requires_approval",
    "book_hotel": "requires_approval",
    "cancel_booking": "blocked"
  },
  "residual_risk": "Fares and availability change rapidly. Prices at search time may not be available at booking time. Refund and cancellation policies vary by carrier and fare class."
}
```

### 6. general_fallback

```json
{
  "artifact_type": "domain_pack",
  "domain": "general_fallback",
  "triggers": ["*"],
  "required_artifacts": ["requirements_chain", "phase_contract", "evidence_ledger", "phase_closeout"],
  "validation_gates": {
    "requirement_trace_exists": {
      "description": "Requirements chain exists and traces user intent",
      "required": true,
      "check_type": "field_presence"
    },
    "phase_contract_exists": {
      "description": "Phase contract bounds the current execution",
      "required": true,
      "check_type": "field_presence"
    },
    "evidence_ledger_exists": {
      "description": "Evidence ledger records declared obligations and proof",
      "required": true,
      "check_type": "field_presence"
    },
    "validation_result_exists": {
      "description": "Validation result or blocker is recorded",
      "required": true,
      "check_type": "field_presence"
    },
    "claims_within_evidence": {
      "description": "Final claims do not exceed available evidence",
      "required": true,
      "check_type": "artifact_check"
    }
  },
  "approval_gates": ["external_write", "irreversible_action", "payment", "data_deletion"],
  "external_action_boundaries": {
    "read_files": "allowed",
    "write_local_files": "allowed",
    "external_api_read": "requires_approval",
    "external_api_write": "requires_approval",
    "irreversible_action": "blocked"
  },
  "residual_risk": "General fallback has no domain-specific knowledge. Complex tasks should use a domain-specific pack when available."
}
```

## Example Good Closeout

```json
{
  "artifact_type": "phase_closeout",
  "phase_id": "phase-3c",
  "objective_met": true,
  "artifacts_produced": ["meeting_invite_draft.md"],
  "evidence_ids": ["ev-034"],
  "validation_results": [
    {"check": "participants_known", "result": "pass"},
    {"check": "timezones_resolved", "result": "pass"},
    {"check": "duration_known", "result": "pass"},
    {"check": "candidate_slots_listed", "result": "pass"}
  ],
  "blockers": [],
  "carry_forward": ["Three candidate slots for user selection"],
  "next_phase_id": "phase-3d",
  "status": "passed"
}
```

## Example Blocked Closeout

```json
{
  "artifact_type": "phase_closeout",
  "phase_id": "phase-3c",
  "objective_met": false,
  "artifacts_produced": [],
  "evidence_ids": [],
  "validation_results": [
    {"check": "participants_known", "result": "pass"},
    {"check": "timezones_resolved", "result": "fail"},
    {"check": "duration_known", "result": "pass"},
    {"check": "candidate_slots_listed", "result": "fail"}
  ],
  "blockers": [
    "Time zone for participant sarah@example.com unknown — requires user input",
    "Cannot list candidate slots without resolved time zones"
  ],
  "carry_forward": ["Participant list confirmed. Duration: 60 minutes. Need time zone for sarah@example.com."],
  "next_phase_id": "none",
  "status": "blocked"
}
```

## Validation Rules

1. `domain` must be a non-empty, lowercase string with underscores (e.g., `software_engineering`).
2. `triggers` must be a non-empty list of strings.
3. `required_artifacts` must only contain types from the universal artifact vocabulary.
4. Each `validation_gates` entry must have `description`, `required`, and `check_type` fields.
5. `check_type` must be one of `field_presence`, `value_check`, `command`, `artifact_check`, `user_confirmation`.
6. `approval_gates` must be a list of strings describing actions requiring approval.
7. `external_action_boundaries` values must be one of `allowed`, `requires_approval`, `blocked`.
8. `residual_risk` must be a non-empty string or `none`.
9. Actions with `requires_approval` in `external_action_boundaries` must have corresponding entries in `approval_gates`. Actions with `blocked` do not need approval gate entries (they are simply forbidden).
10. The `general_fallback` pack must have `triggers: ["*"]` to match any unknown domain.

## YAML Representation (Deferred)

The Phase 2 validator accepts JSON only. This YAML shape is a documentation aid for future parser support and is not currently accepted by `runtime/validator.py`.

```yaml
artifact_type: domain_pack
domain: scheduling
triggers:
  - meeting
  - calendar
  - schedule
  - availability
  - timezone
required_artifacts:
  - requirements_chain
  - phase_contract
  - evidence_ledger
  - approval_record
  - phase_closeout
validation_gates:
  participants_known:
    description: All meeting participants identified
    required: true
    check_type: field_presence
  timezones_resolved:
    description: Time zones for all participants resolved or blocker recorded
    required: true
    check_type: value_check
  duration_known:
    description: Meeting duration specified
    required: true
    check_type: field_presence
  candidate_slots_listed:
    description: Candidate time slots listed with availability status
    required: true
    check_type: field_presence
approval_gates:
  - send_invite
  - modify_calendar
  - cancel_event
external_action_boundaries:
  read_calendar: allowed
  propose_slots: allowed
  send_invite: requires_approval
  modify_calendar: requires_approval
  delete_event: blocked
residual_risk: >
  Time zone data may be stale. Calendar availability may change between
  check and send. Final invites should be verified by user before sending.
```
