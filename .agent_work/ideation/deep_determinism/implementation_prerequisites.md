# Implementation Prerequisites

This note documents the gaps we must resolve before writing a concrete implementation plan. The ideation documents define what we want to build. This note defines what we still need to decide.

## 1. Error and Recovery Model

### Problem

The current docs describe what happens when everything works. They do not describe what happens when the orchestrator crashes mid-phase, a file write is partial, a phase times out, or the harness returns an unexpected status.

### Required Decisions

#### Crash recovery

How does the orchestrator detect that a previous run was interrupted?

Options:
- check for a `.lock` or `checkpoint.json` file at startup
- compare `STATUS.md` current phase against `PHASE_LOG.md` last entry
- require explicit phase closeout; any unclosed phase at startup is treated as interrupted

Recovery action when interrupted:
- revert to the last validated checkpoint
- re-run the interrupted phase from scratch (permission: safe for read-only audit phases, risky for write phases)
- resume mid-phase if the phase is idempotent

#### Partial writes

If the agent writes 3 of 5 expected artifacts and then the harness stops it (step cap, crash, timeout), what happens?

Options:
- fail the phase; the orchestrator rejects partial output
- accept partial output if `CHECKLIST.md` confirms remaining items are incomplete
- require atomic output directories with a `.done` sentinel file

#### Phase timeouts

Should phases have wall-clock timeouts? If so:
- who enforces them (orchestrator, harness, or both)?
- what is the default timeout for each phase type (audit vs edit vs validate)?
- what happens on timeout (retry, skip, block)?

#### Retry policy

How many retries per phase before the workflow blocks permanently?

Options:
- 3 retries for validation failures, 1 for structural failures
- exponential backoff between retries
- human escalation after max retries (write a BLOCKED.md artifact)

### Skeleton Decision

```yaml
recovery:
  crash_detection: checkpoint.json
  resume_strategy: re-run-interrupted-phase
  max_retries: 3
  retry_backoff: exponential
  timeout_default_s: 300
  partial_output: reject-and-retry
```

## 2. Validation Schemas

### Problem

The ideation docs reference JSON schemas for workflow configs, phase contracts, audit results, and agent configs. None of these schemas exist as files. Code cannot be written against prose alone.

### Required Schemas

```text
schemas/
  workflow_config.schema.json     # baseline + overlay structure
  phase_contract.schema.json      # step-level inputs, outputs, permissions
  audit_result.schema.json        # findings, severity, evidence, fixes
  agent_config.schema.json        # OpenCode agent frontmatter validation
  task_state.schema.json          # required fields for TASK.md / STATUS.md
  checklist.schema.json           # checklist item shape
```

Each schema should be:
- valid JSON Schema (draft-07 or 2020-12)
- referenced by validation scripts
- versioned alongside the orchestrator

### Example Skeleton

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "title": "WorkflowConfig",
  "type": "object",
  "properties": {
    "workflow_id": { "type": "string" },
    "version": { "type": "integer", "minimum": 1 },
    "baseline": { "$ref": "#/definitions/BaselineBlock" },
    "overlay": { "$ref": "#/definitions/OverlayBlock" },
    "step_contracts": { "type": "object" },
    "validation": { "$ref": "#/definitions/ValidationBlock" }
  },
  "required": ["workflow_id", "version", "baseline"]
}
```

### Priority

Start with `workflow_config.schema.json` and `agent_config.schema.json` — everything else depends on these shapes.

## 3. MVP Build Order

### Problem

We have 12 ideation documents and at least 8 major components to build. Without a sequenced plan, the implementation will stall at the first ambiguous dependency.

### Proposed Order

#### Phase 1 — Schemas and Validation (days 1-3)

Why first: every other component references these contracts.

Deliverables:
- `schemas/workflow_config.schema.json`
- `schemas/phase_contract.schema.json`
- `schemas/agent_config.schema.json`
- `scripts/validate_workflow.py` (reads a config, validates against schema)
- `scripts/validate_artifacts.py` (checks required artifact existence)

Gate: validation script passes against the existing workflow_config_sketch.md examples.

#### Phase 2 — Core Orchestrator (days 4-10)

Why second: the orchestrator is the control plane. Without it, nothing runs.

Deliverables:
- `orchestrator.py` — step selection, checkpoint read/write, phase transitions
- stateless shell that reads state, prints next step, and exits
- state file read/write helpers
- checkpoint.json format

Gate: orchestrator can load a workflow config and task-state directory, print the next valid step, and exit 0.

#### Phase 3 — OpenCode Harness Adapter (days 11-15)

Deliverables:
- `adapters/opencode.py` — maps generic step contracts to OpenCode agent profiles
- launch packet construction
- result collection and validation
- `.opencode/agents/` file generation helpers

Gate: adapter can run an audit step end-to-end on an OpenCode agent and collect structured results.

#### Phase 4 — Skill integration (days 16-20)

Deliverables:
- wire orchestrator into `contextsmith-run` skill
- `workflow-developer` skill for generating workflow configs
- `--harness opencode` flag integration
- conditional reference loading in skill manifests

Gate: `contextsmith run <handoff>` executes the full cycle through orchestrator, adapter, agent, and validation.

#### Phase 5 — User-facing features (days 21-30)

Deliverables:
- `SUMMARY.md`, `AUDIT_REPORT.md`, `EDUCATIONAL_REPORT.md` generation
- `--dry-run` mode
- `inspect` subcommand for workflow state
- install guide and onboarding
- multi-project support

### Ordering Principles

- schemas before code
- orchestrator before adapter
- adapter before skill integration
- core before user-facing polish

## 4. Testing Strategy

### Problem

The orchestrator runs agents and harnesses. Without a real harness, how do we test the orchestrator's state machine? Without a real orchestrator, how do we test a harness adapter?

### Approach

#### Unit tests (no harness needed)

- `tests/test_orchestrator_state.py` — test state transitions with mock task-state directories
- `tests/test_validation.py` — test schema validation against known-good and known-bad configs
- `tests/test_launch_packet.py` — test packet construction from step contracts

#### Adapter tests (mock harness, real contracts)

```python
# tests/test_opencode_adapter.py
def test_adapter_builds_correct_packet():
    adapter = OpenCodeAdapter()
    packet = adapter.build_packet(step_contract=audit_step)
    assert packet.agent_profile == "contextsmith-auditor"
    assert packet.controls.permissions == "read-only"
    assert packet.controls.step_cap == 10
```

#### Integration tests (real orchestrator + real OpenCode agent)

These require an actual OpenCode installation. Run only in CI or on-demand.

```python
# tests/integration/test_full_audit_cycle.py
def test_audit_phase_completes():
    result = orchestrator.run_phase("audit-03", workdir=test_dir)
    assert result.status == "pass"
    assert Path(test_dir / "AUDIT_REPORT.md").exists()
```

#### Test harness

The orchestrator should accept a `--test-mode` flag that:
- disables real agent invocation
- simulates agent responses from fixture files
- validates the state machine transitions regardless of agent availability

```bash
python orchestrator.py --test-mode --fixture tests/fixtures/audit_pass.json
```

### Test data strategy

- fixture task-state directories under `tests/fixtures/`
- known-good and known-bad workflow configs
- mock result envelopes for each status type (pass, fail, blocked)

### Required test cases

| Test | Input | Expected Output |
|------|-------|-----------------|
| Config validation pass | valid workflow YAML | exit 0 |
| Config validation fail | missing required field | exit 3, error message |
| Fresh start | config + empty state dir | STATUS.md created, state = init |
| Resume after crash | checkpoint.json + partial artifacts | resumes from last valid state |
| Audit pass | execute → audit (pass) | advances to next state |
| Audit fail → fix | execute → audit (fail) → fix | fix state entered |
| Ralph loop complete | 2 cycles of critique/revise | advances to closeout |
| Max retries exceeded | 3 consecutive failures | state = blocked |
| Step cap reached | agent hits step limit | partial output collected, retry |
| Partial artifact write | 3 of 5 artifacts written | status = fail, retry |
| Missing checkpoint | no checkpoint.json | fresh start |
| Corrupted checkpoint | invalid JSON | exit 4 (--repair needed) |

## 5. Installation and Onboarding

### Problem

The user needs a clear path from "never used ContextSmith" to "running a workflow." Currently there is no install guide, no package, and no first-run experience.

### Requirements

#### Python package

Core should be installable as:
```bash
pip install contextsmith          # universal core
pip install contextsmith[opencode] # with OpenCode extras
```

Or for development:
```bash
git clone <repo>
pip install -e .
```

#### Dependencies

- Minimum: Python 3.10+, PyYAML, jsonschema
- Optional (opencode extras): none beyond core
- No Bash, Makefile, or platform-specific tools in the critical path

#### First-run experience

After install, the user should be able to run:

```bash
contextsmith init                  # creates .contextsmith/ with default configs
contextsmith init --harness opencode  # also creates .opencode/agents/ stubs
contextsmith validate              # checks installation is correct
```

#### Documentation entry point

A single `INSTALL.md` at the repo root covering:
- system requirements
- pip install command(s)
- first-run init
- harness-specific setup
- upgrading

## 6. Upgrade and Migration

### Problem

The artifact set will grow over time (e.g., adding `CHECKLIST.md`). Existing task-state directories will be missing the new files. The orchestrator must handle this gracefully.

### Migration Strategies

#### Forward-compatible baseline

The orchestrator should tolerate missing optional artifacts:
- if `CHECKLIST.md` does not exist, treat all items as incomplete
- if `AUDIT_REPORT.md` does not exist, skip the audit review gate
- required artifacts are declared per workflow config, not hardcoded

#### Schema versioning

- workflow configs carry a `version` field
- the orchestrator rejects configs with newer versions than it understands
- schema files are versioned (e.g., `workflow_config.v2.schema.json`)

#### Migration script

For breaking changes:

```bash
contextsmith migrate --from v1 --to v2 --dir .agent_work/
```

This script:
- reads each task-state directory
- adds missing required files with sensible defaults
- updates artifact references
- writes a migration log

#### What does NOT need migration

- `TASK.md`, `STATUS.md`, `NEXT_PROMPT.md` should remain stable
- new checklist items should not break existing phases
- the orchestrator should never silently delete an artifact

## 7. Security and Trust Boundaries

### Problem

The orchestrator decides what gets executed. The harness enforces permissions. But what protects the orchestrator itself? What if a harness adapter or agent corrupts state files?

### Threat Model

| Threat | Impact | Mitigation |
|--------|--------|------------|
| Agent writes garbage to state files | Orchestrator reads invalid state | Schemas: orchestrator re-validates state files after agent writes |
| Harness adapter ignores permissions | Agent can edit files it shouldn't | Boundary: orchestrator runs harness in subprocess with limited permissions |
| Orchestrator config is tampered | Workflow bypasses required gates | Config is trusted input owned by the user, not by the agent |
| Malicious workflow config | Agent runs with unexpected permissions | Config validation against schema before execution |

### Rules

1. The orchestrator re-validates all agent output before accepting it.
2. The orchestrator does not read `NEXT_PROMPT.md` from an external source without validation.
3. The harness adapter runs in-process with the orchestrator; the agent runtime (e.g., OpenCode CLI) runs as a subprocess launched by the adapter.
4. Task-state directories are owned by the orchestrator; agents write via the harness only.
5. Permissions cascade: orchestrator → harness → agent. Each layer can only narrow, never widen.

### Tool integrity

Custom tools and plugins (`.opencode/tools/`) must be treated as executable code:
- warn the user if tools are modified between runs
- do not load tools from untrusted paths
- tool outputs are validated against schemas, not trusted by contents alone

## 8. Observability

### Problem

When a workflow is stuck, the user needs to understand why without re-reading the entire task-state directory manually.

### Requirements

#### Orchestrator log file

The orchestrator writes a structured log:

```text
.agent_work/sprints/<sprint>/tasks/<date-slug>/orchestrator.log
```

Log lines are plain text with timestamps:

```text
[2026-06-10T14:30:01] state=audit-03 status=started
[2026-06-10T14:30:02] state=audit-03 status=dispatched agent=contextsmith-auditor
[2026-06-10T14:30:12] state=audit-03 status=validation_failed reason=missing_evidence
[2026-06-10T14:30:12] state=audit-03 status=retry attempt=1/3
```

#### `--dry-run` mode

The orchestrator accepts `--dry-run` to print what it would do without executing anything:

```bash
python orchestrator.py --config workflow.yaml --state .agent_work/.../ --dry-run
```

Output:

```text
NEXT STEP: audit-03
  agent: contextsmith-auditor
  input: .agent_work/.../tasks/.../NEXT_PROMPT.md
  expected outputs: AUDIT_REPORT.md, CHECKLIST.md, PHASE_LOG.md
  permissions: read-only
  step cap: 10
```

#### `inspect` subcommand

The orchestrator should support a read-only inspection mode:

```bash
contextsmith inspect .agent_work/sprints/current/tasks/2026-06-10-task/
```

Output:

```text
Task: Implement error recovery model
Phase: 3 of 5 (audit-03)
Status: blocked
Blocked by: validation_failed (missing EVIDENCE.md)
Checklist: 3/5 complete
Last action: 2026-06-10T14:30:12
Retries remaining: 2
```

#### Debug verbosity levels

- `--quiet`: only errors and blocking conditions
- `--verbose`: step transitions, validation results, skipped items
- `--debug`: full state dumps, raw envelopes, schema validation details

## 9. Plan Generation From Natural Language

### Problem

The entire deterministic workflow stack assumes a valid workflow config already exists. There is no ideation on how a user's messy intent ("implement error recovery", "add a validation gate") becomes a structured, schema-validated workflow config. The `workflow-developer` skill is named in `system_components.md` but never designed. Without this, the system can only execute pre-built workflows — it cannot bootstrap itself from a prompt.

### Required Decisions

#### Intent-to-config pipeline

How does the system go from user prompt to validated workflow config?

Options:
- LLM generates a YAML config directly against the schema, then the orchestrator validates it and refuses to start on schema-failure
- multi-step: LLM produces a freeform plan, a validator skill converts it to structured YAML, orchestrator validates
- human writes the config, the orchestrator only validates (current implicit assumption)

#### Plan completeness checking

How does the system know a generated plan covers all necessary aspects?

Options:
- schema validation only (structural, not semantic)
- checklist of required phase types (audit, edit, validate, closeout) — plan must include at least one of each
- reference to a domain template: "for skill-engineering workflows, these phases are required"
- allow the plan to be incomplete and let the orchestrator fail fast at the missing phase

#### Validation loop

Should plan generation be a single shot or a generate-validate-refine loop?

Options:
- single shot — if validation fails, reject and stop
- loop — generate, validate, feed errors back to the generator, retry (N attempts)
- loop with human escalation — after N retries, present the failure to the user with options

### Skeleton Decision

```yaml
plan_generation:
  pipeline: llm-generate-then-validate
  max_generation_retries: 3
  completeness_check: required-phase-types
  required_phase_types:
    - audit
    - edit
    - validate
    - closeout
  validation: schema-plus-checklist
```

### Recommended Implementation

The plan generation pipeline should work as follows:

1. User provides a natural-language intent (e.g., "implement error recovery model")
2. The `workflow-developer` skill generates a YAML workflow config against `workflow_config.schema.json`
3. The orchestrator validates the config at startup (schema check + required-phase-types check)
4. If validation fails, the orchestrator reports errors and refuses to start
5. If validation passes, the orchestrator enters the main loop

The key insight: the plan generation loop is a **skill-level concern**, not an orchestrator concern. The orchestrator only validates the config it receives. The skill that generates the config is responsible for retrying on validation failure.

This means the orchestrator spec does not need to change. Only the `workflow-developer` skill needs to be designed and implemented.

---

## 10. Deviation Protocol — Unexpected But Valid Output

### Problem

The ideation assumes agents produce exactly the expected artifacts with expected content. In practice, agents are creative. They may produce output that is structurally valid (passes schema checks) but doesn't match the plan's expected structure, file set, or content shape. The current design has no protocol for handling this — it either accepts anything valid (drift) or rejects valid work (brittle).

### Required Decisions

#### What counts as a deviation

When is an agent's output "unexpected"?

Options:
- missing expected artifact (clear deviation)
- extra artifact that changes the task scope (deviation)
- valid artifact with different internal structure than expected (deviation)
- artifact that solves the task differently than the plan described (judgment call)
- any output that passes schema validation is accepted by definition (no deviation possible)

#### Resolution path

When a deviation is detected, what happens?

Options:
- log and continue — treat deviations as normal, the plan was approximate
- block and escalate — deviations require human review
- route to a deviation-review phase — a second agent evaluates whether the deviation is acceptable
- reject and retry — force the agent to match the plan exactly

#### Plan-relative vs schema-relative validity

Which is authoritative: the plan's expected shape or the schema's valid shape?

Options:
- schema is authoritative — if it passes schema, it's valid regardless of the plan
- plan is authoritative — the agent must match the plan's expected outputs even if other shapes are schema-valid
- hybrid — schema is the floor, plan expectations add additional constraints

### Skeleton Decision

```yaml
deviation:
  detection: missing-artifacts-plus-structural-drift
  resolution: log-and-continue
  validity_authority: hybrid
  escalation_after: 3-consecutive-deviations
```

---

## 11. Human Escalation Protocol

### Problem

The current design has a single "blocked" terminal state. There is no protocol for requesting human input mid-workflow, presenting options, or resuming after intervention. Real workflows get stuck on ambiguous decisions, policy questions, and edge cases the agent cannot resolve alone. Without a human escalation protocol, the workflow either dead-ends or the agent guesses, undermining determinism.

### Required Decisions

#### Escalation triggers

What events cause a human escalation?

Options:
- max retries exceeded (current: write BLOCKED.md)
- validation failure that cannot be resolved by retry
- deviation detected and deviation policy says escalate
- agent explicitly requests clarification
- phase requires human approval gate
- config drift detected (file modified outside orchestration)

#### Escalation format

How is the human presented with the request?

Options:
- write a `HUMAN_INPUT_REQUESTED.md` with question, options, and context
- write a structured JSON request that a CLI tool can render
- surface via orchestrator stdout/stderr with a `--await-human` flag
- send via notification (email, message) — out of scope for MVP

#### Resume semantics

After the human responds, how does the workflow continue?

Options:
- human edits a file (e.g., fills in `HUMAN_DECISION.md` with the chosen option), orchestrator detects the file change and resumes
- human runs `contextsmith resume --decision <path>` with the decision file
- human provides input directly via orchestrator stdin
- human restarts the orchestrator with modified task-state files

#### Timeout on human

What if the human doesn't respond?

Options:
- wait indefinitely (blocked until input arrives)
- timeout after N hours, mark as stale, require explicit resume
- apply a default decision after timeout

### Skeleton Decision

```yaml
human_escalation:
  triggers:
    - max-retries-exceeded
    - unresolvable-validation-failure
    - human-approval-gate
    - agent-requested-clarification
  format: HUMAN_INPUT_REQUESTED.md
  resume: contextsmith-resume --decision <path>
  timeout: 24h
  timeout_action: mark-stale
```

---

## 12. Idempotency and Partial Execution

### Problem

Sections 1 (Error Recovery) and 4 (Testing) touch on idempotency but do not resolve it. The orchestrator needs a clear answer to: "If I run this phase twice, do I get the same result?" Without idempotency, crash recovery means redoing work that may already be partially complete, and retries risk duplicate side effects.

### Required Decisions

#### Phase idempotency levels

Should phases be classified by idempotency?

Options:
- read-only phases are inherently idempotent (audit, review, validate)
- write phases are not idempotent unless explicitly designed to be (edit, create, migrate)
- every phase should declare its idempotency in the step contract
- all phases must be made idempotent via snapshots or sentinel files

#### Completion detection

How does the orchestrator detect that a phase has already been completed?

Options:
- checkpoint.json contains a `completed_phases` list — if the phase id is present, skip it
- each phase writes a `.phase_done` sentinel file on completion
- the orchestrator re-runs validation on the phase's outputs; if valid, treat as complete
- hybrid: checkpoint for crash recovery, validation for resume-after-compaction

#### Re-entrance guard

Should the orchestrator prevent running a completed phase again?

Options:
- hard block — orchestrator refuses to dispatch a completed phase
- soft block — warns but allows if `--force` is passed
- no guard — phases are always re-runnable (idempotent by design)

### Skeleton Decision

```yaml
idempotency:
  default: write-phases-not-idempotent
  declaration: step-contract-idempotency-field
  completion_detection: checkpoint-list-plus-validation
  re_entrance: hard-block-with-force-flag
```

---

## 13. Multi-Phase Dependencies and Parallel Execution

### Problem

The entire ideation models execution as strictly sequential (one phase → one agent → one output). Many real workflows have independent phases that could run in parallel, or phases that depend on specific outputs from earlier phases (not just "the previous phase finished"). Without dependency resolution, the orchestrator either serializes everything (slow) or cannot express phase ordering that isn't linear.

### Required Decisions

#### Dependency model

How do phases declare dependencies?

Options:
- sequential only — phase N runs after phase N-1, no other model needed
- artifact-level dependencies — phase B depends on `AUDIT_REPORT.md` from phase A, not on phase A having "run"
- tag-based — phases declare `depends_on: [audit-complete, schema-validated]` using named gates
- DAG-based — workflow config contains an explicit dependency graph between phases

#### Parallel execution

Should the orchestrator support running independent phases concurrently?

Options:
- no — sequential is simpler and safer for MVP
- yes, within a subprocess pool — independent phases run in parallel, orchestrator waits for all to complete before advancing the DAG
- yes, with resource limits — configurable max-concurrent-phases, respect shared resource locks

#### Artifact conflict resolution

What happens when two parallel phases write to the same file?

Options:
- detect and block — orchestrator checks for write-conflicts before dispatching parallel phases
- last-writer-wins — accept but log the conflict
- require disjoint output directories — parallel phases must write to separate subdirectories

### Skeleton Decision

```yaml
dependencies:
  model: sequential-for-mvp
  declaration: phase-contract-depends-on-field
  parallel_execution: false
  artifact_conflict: detect-and-block
```

---

## 14. Run Comparison and Regression Tracking

### Problem

When a workflow is stuck or produces unexpected results, the user has no way to compare the current run against a previous run of the same workflow. There are no metrics, no run history, and no way to replay a specific phase with the same inputs. Debugging a stuck workflow currently requires re-reading the entire task-state directory manually.

### Required Decisions

#### Run identity

How does the orchestrator identify a specific run?

Options:
- directory path is the identity (`.agent_work/sprints/<sprint>/tasks/<date-slug>/`)
- manifest file in the task directory records run metadata (run_id, workflow_id, start_time, end_time, status)
- git commit hash (if the directory is version-controlled)
- UUID written at workflow start

#### What to record per phase

For each phase execution, what should the orchestrator persist?

Options:
- status, duration, retry count, agent used, exit reason
- input checksum (hash of NEXT_PROMPT.md + STATUS.md at dispatch time)
- output checksum (hash of all produced artifacts)
- full input and output copies (expensive but allows exact replay)
- structured log (section 8 covers this partially)

#### Comparison interface

How does the user compare two runs?

Options:
- `contextsmith diff <run-a> <run-b>` — prints phase-by-phase status diff
- `contextsmith history <task-dir>` — lists all runs with summary stats
- `contextsmith replay <run-id> <phase-id>` — re-executes a specific phase using the recorded input

#### Regression detection

Should the orchestrator flag when a phase that previously passed now fails?

Options:
- manual only — user compares runs
- automatic — orchestrator checks previous run results before retry and warns on regression
- gate-on-history — workflow config can require "this phase has never passed in any prior run" before allowing a different path

### Skeleton Decision

```yaml
run_comparison:
  run_identity: manifest-file-with-uuid
  recorded_per_phase:
    - status
    - duration
    - retry_count
    - agent
    - input_checksum
    - output_checksum
  comparison_tool: contextsmith-diff
  regression_detection: manual-initial
```

---

## 15. Skill-to-Orchestrator Contract

### Problem

ContextSmith skills are pure instruction files (SKILL.md). They describe what a skill does for an agent, but they do not describe their workflow shape in machine-readable terms. The orchestrator has no way to ask "what phases does this skill require?" or "what are the step contracts for this skill's workflow?" Currently, workflow configs and skills are disconnected — the config hardcodes phase details that the skill already describes in prose. This duplication drifts over time and prevents dynamic skill integration.

### Required Decisions

#### Skill workflow export

Should skills export a machine-readable workflow shape?

Options:
- SKILL.md frontmatter gains a `workflow` key with phase names, required gates, and output artifacts
- a separate `workflow.yaml` lives alongside SKILL.md in each skill directory
- the orchestrator derives the workflow shape by analyzing the skill's reference manifest
- no export — workflow configs are written independently and manually kept in sync with skills

#### Dynamic skill resolution

Should the orchestrator discover available skills and their workflows at runtime?

Options:
- no — workflow config pins the skill by name, orchestrator loads it from a known path
- yes — orchestrator scans `skills/` for SKILL.md files with workflow frontmatter and builds a registry
- hybrid — skill registry built at install time, cached for runtime use

#### Phase contract inheritance

When a workflow config references a skill, should the skill's default phase contracts be inherited?

Options:
- no — workflow config must define all phase contracts explicitly
- yes — skill defines defaults, workflow config can override specific fields
- skill defines required contracts that the workflow config must include (schema validation)

### Skeleton Decision

```yaml
skill_orchestrator_contract:
  export_method: skill-metadata-phase-contracts
  dynamic_resolution: install-time-registry
  inheritance: skill-defaults-with-workflow-override
```

---

## Updated Summary of Blockers

Before writing implementation code, we need decisions on:

| # | Item | Depends on | Minimum viable | Status |
|---|------|------------|----------------|--------|
| 1 | Error recovery policy | — | Accept current decisions; refine later | **Partially resolved** — skeleton decisions in section 1 are sufficient for MVP |
| 2 | Workflow config schema | — | Write `workflow_config.schema.json` | **Resolved** — `schemas/workflow_config.schema.json` created, validates both examples |
| 3 | Agent config schema | — | Write `agent_config.schema.json` | **Resolved** — `schemas/agent_config.schema.json` created, validates both examples |
| 4 | MVP build order | 2, 3 | Accept proposed order | **Resolved** — proposed order accepted |
| 5 | Test fixtures | 2, 3 | Create `tests/fixtures/` with known-good configs | **Unblocked** — schemas done, can create fixtures during implementation |
| 6 | Install guide | — | Write `INSTALL.md` | **Deferred** — not blocking MVP |
| 7 | Migration approach | 2 | Accept forward-compatible baseline | **Resolved** — forward-compatible baseline accepted |
| 8 | Orchestrator test mode | — | Add `--test-mode` flag to orchestrator spec | **Resolved** — spec includes `--test-mode` |
| 9 | Observability log format | — | Accept structured-log format | **Resolved** — format defined in section 8 |
| 10 | Plan generation pipeline | 2 | Accept skeleton; refine later | **Designed** — `workflow_developer_skill.md` spec complete, domain templates defined, generation process specified |
| 11 | Deviation protocol | 2 | Accept skeleton; refine later | **Deferred** — log-and-continue is sufficient for MVP |
| 12 | Human escalation protocol | 1 | Accept skeleton; refine later | **Deferred** — HUMAN_INPUT_REQUESTED.md is sufficient for MVP |
| 13 | Idempotency and partial execution | 1 | Accept skeleton; refine later | **Partially resolved** — checkpoint-based detection is specified |
| 14 | Multi-phase dependencies | 2, 4 | Accept sequential-for-MVP; refine later | **Resolved** — sequential for MVP |
| 15 | Run comparison and regression | 8 | Accept skeleton; refine later | **Deferred** — not blocking MVP |
| 16 | Skill-to-orchestrator contract | 2, 3 | Accept skeleton; refine later | **Deferred** — manual config is sufficient for MVP |

**Critical path:** All design gaps are resolved. Item 10 (plan generation) has a complete spec with domain templates. OpenCode CLI flags are verified. The orchestrator SKILL.md is drafted. An end-to-end example exists. The remaining work is implementation — no blocking design decisions remain.

**Resolved architecture decisions (this pass):**
- Transport model: harness adapter runs in-process, agent runtime runs as subprocess (section 7 updated)
- OpenCode CLI flags: **verified** (2026-06-12) — `--agent`, `--model`, `--prompt`, `--file`, `--format json` confirmed. `--max-steps` does not exist — use agent config `steps` field instead.
- Fix state transition: clarified in `audit_and_ralph_state_machine.md`
- Overlay rules: clarified in `workflow_config_sketch.md`
- Outer loop: built into orchestrator module (`run_workflow`), not a separate script
- Entry point: router skill in OpenCode calls orchestrator via bash tool, user stays in harness
- Agent output: streams to user via stdout (NOT captured by harness)
- Structured result: agent writes RESULT.json to disk, orchestrator reads it after subprocess exits
- User interrupt: Ctrl-C (SIGINT) or STOP file between phases, clean shutdown with checkpoint
- Schemas: workflow_config.schema.json and agent_config.schema.json created and validated
- **Two execution paths**: orchestrator-as-skill (universal, zero-infrastructure) and orchestrator-as-code (deterministic, harness-optimized) — both share identical workflow configs, artifact contracts, checkpoint formats, and validation rules. See `orchestrator_as_skill.md`.
- **Harness companion model**: thin per-harness reference files (~40 lines) that add harness-specific optimizations. Companions enhance but never gate — the orchestrator skill works without any companion loaded.
- **Installation methods**: skill-only (copy SKILL.md), harness-optimized (pip install), hybrid (skill + code). The orchestrator skill is the universal base.
- **Orchestrator SKILL.md drafted**: concrete agent-facing instructions for the skill-only loop. See `orchestrator_skill_draft.md`.
- **Domain templates created**: 6 templates (coding, writing, research, migration, audit, general) with default phases, gates, states, and transitions. See `domain-templates/`.
- **Harness-opencode.md created**: verified CLI flags, agent config format, permission model, step limiting strategy.
- **End-to-end example**: complete walkthrough from user request to workflow completion. See `end_to_end_example.md`.
- **Confirmation as default**: all skills summarize parameters and plan, then ask for confirmation before executing. Opt-out via `--mode yolo` or "just do it".

All design gaps are resolved. The remaining work is implementation.

## Related Notes

- `system_components.md` for the full component map
- `workflow_config_sketch.md` for the config shape
- `agent_start_and_communication.md` for runtime messaging
- `harness_agnostic_distribution.md` for Python-first and portability
- `state_artifact_strategy.md` for artifact taxonomy and handoffs
