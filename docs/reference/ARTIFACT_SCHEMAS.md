# Artifact Schema Registry

The artifact schema registry defines the structural contracts for all markdown artifacts used in ContextSmith workflows. It lives at `schemas/artifact_schemas.yaml` and is the canonical source of truth for what each artifact type requires.

## Purpose

Every task-state artifact — STATUS.md, PLAN.md, PHASE_LOG.md, and the rest — follows a documented structure. The schema registry makes that structure explicit, machine-validatable, and extensible per workflow. It serves three functions:

- **Validation**: The orchestrator checks artifacts against their schema after every phase transition.
- **Documentation**: Anyone writing or maintaining task-state files can look up what sections are required and which content rules apply.
- **Extension**: Workflow configs can override required sections without modifying the registry itself.

## Schema Structure

Each artifact schema in the registry is a YAML map with these fields:

```yaml
ARTIFACT_NAME.md:
  description: "Human-readable explanation of the artifact's purpose"
  append_only: true|false
  required_sections:

    - "Section Name"        # ## headings that must exist

  optional_sections:

    - "Section Name"        # ## headings that may exist

  content_rules:

    - type: "rule_type"     # What kind of validation to apply

      description: "..."    # Explanation of the rule

      # type-specific fields follow
```

### Field Reference

| Field | Required | Description |
| --- | --- | --- |
| `description` | yes | What the artifact is for |
| `append_only` | yes | If true, the orchestrator checks that the file prefix is preserved (was appended to, not overwritten) |
| `required_sections` | no | List of `##` headings that must be present. Empty list means no structural heading requirement |
| `optional_sections` | no | List of `##` headings that may appear but are not enforced |
| `content_rules` | no | Validation rules that go beyond section presence checks |

### Content Rule Types

The registry supports several content rule types for deeper validation:

- **`key_value`**: Validates that a section contains `- Key: Value` lines matching a regex pattern. Used for STATUS.md metadata and file maps.
- **`phase_tree`**: Validates the hierarchical phase/sub-phase/task structure in PLAN.md. `state_reader._parse_phase_tree()` parses this format into structured dicts, using the same heading-level conventions defined in the schema. This is the most complex rule (see below).
- **`phase_entry`**: Validates append-only phase log entries with required and optional key-value fields.
- **`phase_report`**: Validates educational report entries with required subsection headings.
- **`audit_entry`**: Validates audit report entries with required fields.
- **`decision_entry`**: Validates decision entries with required Decision and Reason fields.
- **`checklist_items`**: Validates that a section contains well-formed markdown checkboxes.

## PLAN.md Hierarchical Format

PLAN.md uses a three-level hierarchy enforced by the `phase_tree` content rule:

```

### Phase N: Name

- Status: pending|in_progress|completed|blocked
- Context Budget: NNk

#### Sub-phase N.M: Description

- Status: pending
- Context Budget: NNk
- Dependency: optional
- Validation: optional
  - [ ] Task description
  - [x] Completed task
```

### Level 1: Phase (`###`)

Each phase is a `###` heading. Required metadata: `Status`. Optional: `Agent`, `Context Budget`.

```markdown

### Phase 2: Validator Refactor

- Status: completed
- Context Budget: 24k
```

### Level 2: Sub-phase (`####`)

Each sub-phase is a `####` heading under its parent phase. Required metadata: `Status`. Optional: `Context Budget`, `Dependency`, `Validation`.

```markdown

#### Sub-phase 2.1: Schema loading

- Status: completed
- Context Budget: 24k
- Validation: |pytest tests/test_validators.py::TestLoadArtifactSchemas|
```

### Level 3: Task (`- [ ]` / `- [x]`)

Tasks are checkbox list items under a sub-phase. A checked box (`[x]`) marks it complete.

```markdown
  - [ ] Add load_artifact_schemas()
  - [x] Add validate_artifact_schema()
  - [x] Add validate_artifacts_with_schemas()
```

### Completion Tracking

Task completion is calculated automatically by `state_reader._calc_completion()` as the ratio of checked to total tasks in a sub-phase. When all tasks are checked, the sub-phase is functionally complete.

```markdown

#### Sub-phase 6.1: State reader tests

- Status: completed
- Context Budget: 16k
  - [x] Test hierarchical parsing
  - [x] Test flat format backward compat
  - [x] Test context budget extraction
```

Task completion: 3/3 = 100%.

## Example: Full Phase in PLAN.md

```markdown

### Phase 9: Documentation

- Status: pending

#### Sub-phase 9.1: Schema registry docs

- Status: pending
- Context Budget: 24k
  - [ ] Write docs/reference/ARTIFACT_SCHEMAS.md
  - [ ] Document PLAN.md hierarchical format
  - [ ] Add examples of sub-phase structure

#### Sub-phase 9.2: Changelog

- Status: pending
- Context Budget: 8k
  - [ ] Update CHANGELOG.md
  - [ ] Run markdownlint on all docs
```

## STATUS.md Current Sub-phase

STATUS.md has an optional `Current Sub-phase` section that tracks the active sub-phase within the current phase. It follows the pattern `Sub-phase N.M: Description` or `none` when the phase has no sub-phases defined.

```markdown

## Current Sub-phase
Sub-phase 9.1: Schema registry docs
```

The content rule enforces the pattern with regex: `^(Sub-phase|SP)\s+[\d.]+:?\s+.+|none$`.

When the orchestrator advances a sub-phase, it updates this field. If the sub-phase is the last one in a phase, the orchestrator transitions to the next phase and resets this to the first sub-phase of the new phase.

## How Validation Uses Schemas

Validation follows a layered approach:

### 1. Schema Loading

`validators.load_artifact_schemas()` reads `schemas/artifact_schemas.yaml` and returns a dict of artifact schemas keyed by filename.

```python
schemas = load_artifact_schemas()

# Returns: {"STATUS.md": {...}, "PLAN.md": {...}, ...}
```

### 2. Single Artifact Validation

`validators.validate_artifact_schema()` checks a single file against its schema:

```python
errors = validate_artifact_schema(
    file_path=state_dir / "STATUS.md",
    schema=schemas["STATUS.md"]
)

# Returns: [] if valid, ["Missing required section '...' in STATUS.md"] if not
```

It checks:

- File exists and is non-empty
- All required sections listed in the schema are present as `##` headings
- Optional sections are allowed but not enforced

### 3. Bulk Validation

`validators.validate_artifacts_with_schemas()` validates all expected outputs for a step:

```python
result = validate_artifacts_with_schemas(
    state_dir=state_dir,
    expected_outputs=["STATUS.md", "PLAN.md", "PHASE_LOG.md"],
    config=workflow_config
)

# Returns: {"passed": True, "failures": [], "files_checked": 3, "files_passed": 3}
```

### 4. Config Overrides

Workflow configs can override required sections without modifying the registry. The `_build_artifact_overrides()` helper merges config-level overrides with base schemas, supporting `extend_base` (add to base required sections) and standalone overrides (replace entirely).

### 5. Phase Tree Validation

For PLAN.md specifically, `validate_phase_tree_structure()` validates the parsed phase hierarchy:

- At least one phase must exist
- Phase and sub-phase status values must be valid (`pending`, `in_progress`, `completed`, `blocked`)
- Task checkboxes must be well-formed

And `validate_plan_phase_order()` cross-references PLAN.md phases against the workflow config's `phase_order` to detect mismatches.

## Schema Registry File

The full registry is at `schemas/artifact_schemas.yaml`. It covers these artifact types:

| Artifact | Required Sections | Append-Only | Content Rule |
| --- | --- | --- | --- |
| STATUS.md | Current Phase, Current State, Next Action | no | key_value |
| PLAN.md | Phases | no | phase_tree |
| CONTEXT.md | Project, Known Constraints | no | key_value |
| PHASE_LOG.md | (none required) | yes | phase_entry |
| EDUCATIONAL_REPORT.md | (none required) | yes | phase_report |
| AUDIT_REPORT.md | (none required) | yes | audit_entry |
| DECISIONS.md | (none required) | yes | decision_entry |
| ARTIFACTS.md | Files to Create, Files to Modify, Commands to Run | no | (none) |
| CHECKLIST.md | (none required) | no | checklist_items |
| TASK.md | Objective, Scope, Constraints | no | (none) |
| NEXT_PROMPT.md | Current Status, Your Task, Input Files, Output Requirements | no | (none) |

## Validation Modes

The registry has a top-level `validation_mode` field (currently `strict`):

- **strict**: All rules are enforced — required sections, content rules, and append-only checks.
- **relaxed**: Only required section presence is checked. Content rules and optional section checks are skipped.
