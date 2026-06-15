# System Components for the Deterministic Workflow Stack

This note describes the core parts of the system we are ideating on and how they fit together. The goal is a workflow runner where the orchestrator owns process control, the harness executes bounded steps, and the artifacts on disk make the run resumable.

This is not a full implementation plan. It is the component map we need before we decide what to build first.

## Core Components

### 1. `orchestrator.py`

The orchestrator is the control plane (harness-aware path).

What it does:

- loads task state, workflow config, and schema documents
- decides which step comes next
- enforces required gates and max retries
- chooses the right agent role or validator
- records checkpoints and resume state

How it works:

- reads `STATUS.md`, `PLAN.md`, `CONTEXT.md`, and `NEXT_PROMPT.md`
- compiles the current phase contract
- compares the live workflow against the baseline config
- dispatches bounded work to the harness
- blocks progress if validation or review fails

### 1a. Orchestrator skill (SKILL.md)

The orchestrator-as-skill is the universal execution path. It works in any agent harness without Python or subprocess management.

What it does:

- instructs the agent to run a self-contained workflow loop
- reads the same workflow config, artifacts, and checkpoint format as orchestrator.py
- the agent IS the executor — it does the work, validates artifacts, updates state, and loops

How it works:

- agent reads STATUS.md → determines current phase
- agent reads workflow config → gets step contract
- agent executes the phase (writes artifacts)
- agent validates its own artifacts against the config
- agent updates checkpoint.json, STATUS.md, PHASE_LOG.md
- agent writes NEXT_PROMPT.md
- agent re-reads STATUS.md and loops

Tradeoffs vs orchestrator.py:

- less deterministic (LLM drives the loop, not code)
- no crash recovery (session boundary = potential state loss)
- self-validation is weaker than external validation
- but: zero infrastructure requirements, works in any harness

See `orchestrator_as_skill.md` for the full spec.

### 2. Workflow configuration files

These are the baseline definitions for a run.

Typical formats:

- YAML for human editing
- JSON for strict machine validation

What they contain:

- required steps
- required gates
- allowed overlays or optional branches
- file requirements
- step-level permissions and outputs

How they work:

- the orchestrator treats them as the source of truth
- plan artifacts may add optional steps, but cannot remove required ones without explicit approval
- configs let the same workflow be replayed or resumed consistently

### 3. A skill to develop workflows

This is the authoring layer.

What it does:

- generates workflow configs from a template or prompt
- emits schema-valid YAML or JSON
- creates companion docs for humans
- helps translate a rough idea into a runnable workflow definition

How it works:

- takes an intent such as "build a review loop" or "add a validation gate"
- writes the config plus supporting notes
- references the schema documents so the output is machine-checkable
- avoids freeform prose where the orchestrator needs deterministic structure

### 4. Schema documents

These define what valid input and output look like.

Examples:

- workflow config schema
- phase contract schema
- audit result schema
- review result schema
- task-state schema

What they do:

- constrain config shape and field names
- describe required and optional keys
- let validators reject malformed artifacts early
- give the orchestrator a stable contract to enforce

How they work:

- the skill writes schema-aware files
- the orchestrator checks emitted artifacts against the schema
- validation scripts use the same definitions to confirm the run is valid

### 5. Validation scripts

These are the enforcement layer.

What they do:

- verify file presence and required structure
- validate JSON/YAML against schemas
- check line-level or content-level constraints
- enforce that required steps happened in the right order

How they work:

- run after agent output or phase completion
- return pass/fail signals to the orchestrator
- prevent the workflow from advancing on partial or malformed output

### 6. Agent markdown configuration files

These are the human-readable runtime instructions.

Examples:

- `TASK.md`
- `PLAN.md`
- `STATUS.md`
- `CONTEXT.md`
- `DECISIONS.md`
- `CHECKLIST.md`
- `PHASE_LOG.md`
- `ARTIFACTS.md`
- `EVIDENCE.md`
- `AUDIT_REPORT.md`
- `EDUCATIONAL_REPORT.md`
- `SUMMARY.md`
- `NEXT_PROMPT.md`

What they do:

- store the current objective and phase state
- keep durable decisions visible to the next run
- track per-phase checklist progress
- communicate what the agent should do next
- preserve a resumable record of work

How they work:

- the orchestrator reads them to reconstruct state
- the agent writes them as part of the workflow
- validators check that required files exist and contain the right shape of content

Example:

```md

# Status

Current phase: validate
Next action: run schema validation and update `NEXT_PROMPT.md`
Blocked by: none
```

### 7. OpenCode agent definition markdown files

These define the actual agents the runtime will invoke in OpenCode.

Where they live:

- `.opencode/agents/`
- `~/.config/opencode/agents/`

What they do:

- declare agent name, mode, and step limits
- define permissions for edit, bash, webfetch, and external directories
- pin a role-specific behavior profile for repeatable runs

How they work:

- the orchestrator selects the right role
- OpenCode loads the matching agent definition by name
- the agent runs with the permission envelope declared in the file

Example:

```yaml
---
description: Audits prompts, skills, and agent artifacts for reliability
mode: subagent
steps: 10
permission:
  edit: deny
  bash:
    "*": deny
    "python scripts/validate_skills.py": allow
  webfetch: deny
---
```

Another example:

```yaml
---
description: Creates and edits SKILL.md skills, prompts, and instruction files
mode: subagent
permission:
  edit: allow
  bash: allow
  external_directory: deny
---
```

### 8. OpenCode command definitions

These are the user-facing shortcuts that launch the right agent with the right intent.

Where they live:

- `.opencode/commands/`
- `~/.config/opencode/commands/`

What they do:

- provide consistent entry points like `/contextsmith-audit`
- reduce user error when selecting a workflow
- inject a standard initial prompt body

Example:

```yaml
---
description: Run the ContextSmith validation script
---
Run `python scripts/validate_skills.py` and report results.
If validation fails, suggest fixes without applying them unless the user asks.
```

### 9. Custom tools and plugins

These are the enforcement hooks for workflow gates and integrations.

What they do:

- check artifacts before advancing a phase
- run validations automatically
- keep steps bounded in the harness

How they work:

- the agent calls a tool instead of improvising a check
- the tool inspects files or runs a command
- the orchestrator reads the result and decides whether to continue

Example:

```ts
export default tool({
  description: "Verify that required artifacts exist before proceeding",
  args: {
    required: tool.schema.array(tool.schema.string()),
    phase: tool.schema.string(),
  },
  async execute(args, context) {
    // verify artifacts under the worktree
  },
})
```

### 10. Checkpoints and persistent task state

These files make the workflow resumable after interruption.

What they do:

- record the current phase and next action
- preserve decisions and artifacts
- make retries explicit instead of implicit

How they work:

- the orchestrator writes checkpoints after validation
- the next run loads the same state files
- the workflow resumes at the last confirmed step

Example layout:

```text
.agent_work/sprints/<sprint>/tasks/<date-slug>/
  TASK.md
  PLAN.md
  STATUS.md
  CONTEXT.md
  DECISIONS.md
  PHASE_LOG.md
  NEXT_PROMPT.md
```

### 11. Validation entrypoints and scripts

These are the reusable commands that enforce consistency.

What they do:

- validate skill metadata
- validate workflow configuration
- verify generated artifacts match schema
- fail fast when required files are missing

Example:

```bash
python scripts/validate_skills.py
```

Example workflow-specific validator:

```bash
python scripts/validate_workflow.py .agent_work/ideation/deep_determinism/workflow_config_sketch.md
```

### 12. Metadata and manifest files

These tie the system together at packaging time.

What they do:

- connect `SKILL.md` files to their reference content
- describe versioning and compatibility
- keep installable skills self-contained

Example:

```yaml
references:

  - harness-opencode.md
  - documentation-quality.md
```

Example frontmatter in a skill file:

```yaml
---
name: contextsmith-run
description: Execute task-state handoffs with bounded phases
metadata:
  version: 1.0.0
---
```

## How They Work Together

### Path 1: Harness-aware (orchestrator-as-code)

1. A user or higher-level agent starts a workflow run.
2. `orchestrator.py` loads the workflow config, schemas, agent definitions, and markdown state files.
3. The orchestrator determines the next valid step.
4. The workflow skill generates or updates the config when needed.
5. The harness resolves the right OpenCode agent definition and runs it with the configured permissions and limits.
6. The agent writes or updates markdown artifacts.
7. Validation scripts check the result against the schema documents and workflow rules.
8. The orchestrator records success, retry, or failure and updates the next handoff.

### Path 2: Skill-only (orchestrator-as-skill)

1. A user loads the orchestrator skill in any agent harness.
2. The agent reads the workflow config and STATUS.md to determine the current phase.
3. The agent executes the phase — it IS the executor.
4. The agent validates its own artifacts against the config.
5. The agent updates checkpoint.json, STATUS.md, PHASE_LOG.md.
6. The agent writes NEXT_PROMPT.md for the next phase.
7. The agent re-reads STATUS.md and loops until done or blocked.

Both paths use the same workflow config, artifacts, checkpoint, and validation rules. The difference is who runs the loop.

### Interface Contracts Between Components

**Harness-aware path (orchestrator-as-code):**

```
orchestrator.py ──→ workflow_config.schema.json   (validates config at startup)
orchestrator.py ──→ state files (STATUS.md, PLAN.md, CONTEXT.md)  (reads current state)
orchestrator.py ──→ StepContract                  (compiles for each step)
orchestrator.py ──→ HarnessAdapter.execute()       (dispatches to harness)
orchestrator.py ←── HarnessResult                  (receives execution result)
orchestrator.py ──→ validators                     (runs post-execution checks)
orchestrator.py ──→ checkpoint.json                (writes after each phase)
orchestrator.py ──→ NEXT_PROMPT.md                 (generates for next step)

HarnessAdapter  ──→ agent subprocess               (launches agent)
HarnessAdapter  ←── agent stdout + filesystem       (collects output)
HarnessAdapter  ──→ HarnessResult                   (returns to orchestrator)

validators      ──→ artifact files                  (checks existence, content, schema)
validators      ──→ ValidationResult                (returns pass/fail to orchestrator)
```

**Skill-only path (orchestrator-as-skill):**

```
Agent (following SKILL.md) ──→ workflow_config.yaml  (reads phase definitions)
Agent ──→ STATUS.md                                   (reads current phase)
Agent ──→ NEXT_PROMPT.md                              (reads bounded task)
Agent ──→ artifact files                              (writes task output)
Agent ──→ checkpoint.json                             (writes after validation)
Agent ──→ STATUS.md, PHASE_LOG.md, CHECKLIST.md       (updates state)
Agent ──→ NEXT_PROMPT.md                              (writes for next phase)
Agent ──→ STATUS.md (re-read)                         (loops)
```

## Why This Split Matters

- the orchestrator owns logic, not memory
- the workflow config owns structure, not prose
- the skill owns authoring, not execution
- the schemas own validity, not judgment
- the validators own enforcement, not interpretation
- the markdown files own continuity, not control
- the OpenCode agent files own runtime role declarations, not workflow policy
- the orchestrator skill works everywhere; harness companions optimize for specific runtimes

## Practical File Layout

```text
orchestrator.py
schemas/
  workflow_config.schema.json
  phase_contract.schema.json
  audit_result.schema.json
  agent_config.schema.json
skills/
  workflow-developer/
    SKILL.md
    references/
  contextsmith-run/
    SKILL.md
    references/
state/
  TASK.md
  PLAN.md
  STATUS.md
  CONTEXT.md
  DECISIONS.md
  PHASE_LOG.md
  NEXT_PROMPT.md
scripts/
  validate_workflow.py
  validate_skills.py
  sync_shared_refs.py
```

## Related Notes

- `orchestrator_and_harness.md` for the runtime split
- `workflow_config_sketch.md` for the config shape
- `audit_and_ralph_state_machine.md` for loop enforcement
- `communications_protocol_sketch.md` for the message flow
- `shared/harness-opencode.md` for OpenCode agent, command, and tool patterns
