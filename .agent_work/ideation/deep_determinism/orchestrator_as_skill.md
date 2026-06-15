# Orchestrator as Skill

This spec defines two execution paths for the same workflow contract: orchestrator-as-skill (universal, zero-infrastructure) and orchestrator-as-code (deterministic, harness-optimized). Both paths use identical workflow configs, artifact contracts, checkpoint formats, and validation rules. The difference is who runs the loop.

## Core Principle

The orchestrator logic is a SKILL.md. It works in any agent harness — OpenCode, Cursor, Copilot, Aider, Claude, ChatGPT, or a human pasting into a text box. No Python. No subprocess. No harness dependency.

Harness companions are thin reference files (40 lines each) that add harness-specific optimizations. They enhance the orchestrator skill but never gate it. The orchestrator skill must work without any companion loaded.

## Two Paths, One Contract

```
Path 1: Skill-only (universal)
  User → Orchestrator skill → Agent follows instructions → loops itself
  Requirements: an agent that can read files and follow instructions
  Determinism: low (LLM drives the loop)

Path 2: Harness-aware (optimized)
  User → Router skill → python -m orchestrator → Harness adapter → Agent subprocess
  Requirements: Python, a harness that can run bash, RESULT.json protocol
  Determinism: high (code drives the loop)
```

Both paths share:

- Same workflow config format (`workflow_config.schema.json`)
- Same artifact contracts (STATUS.md, PLAN.md, NEXT_PROMPT.md, etc.)
- Same checkpoint.json format
- Same validation rules
- Same RESULT.json contract (when harness-aware)

## Path 1: Orchestrator-as-Skill

### How It Works

The orchestrator SKILL.md instructs the agent to run a self-contained loop. The agent IS the executor. It reads the workflow config, tracks state, executes phases, validates artifacts, and loops.

### The Loop

```
1. Read workflow config (workflow_config.yaml or .json)
2. Read STATUS.md → determine current phase
3. Look up current phase in config → get step contract
4. Execute the phase:

   a. Read NEXT_PROMPT.md for the bounded task
   b. Read CONTEXT.md for constraints and file map
   c. Do the work (you are the agent)
   d. Write expected artifacts per the step contract

5. Validate artifacts:

   a. Check all expected_outputs exist and are non-empty
   b. Check required sections present per artifact templates
   c. If validation fails → record issue, retry (up to max_retries)

6. Update state:

   a. Write checkpoint.json (phase, status, counters)
   b. Update STATUS.md (current phase, next action)
   c. Append to PHASE_LOG.md
   d. Update CHECKLIST.md

7. Generate NEXT_PROMPT.md for the next phase
8. If current phase has a transition to done → complete
9. If current phase has a transition to blocked → stop, ask user
10. Otherwise → re-read STATUS.md, go to step 2
```

### State Management

The agent tracks state in files, not in its context window. On each loop iteration, it reads STATUS.md fresh. This means the loop survives context compaction, session boundaries, and model changes.

### Validation

The agent validates its own artifacts against the workflow config. This is less reliable than external validation (the agent might miss its own errors), but it's better than no validation. The Ralph loop compensates — the agent critiques its own output before moving on.

### Termination

The loop ends when:

- The workflow reaches a `done` state
- The workflow reaches a `blocked` state
- The agent detects it has exceeded max_retries for a phase
- The user interrupts (Ctrl-C, or stops responding)

### Limitations

- **Less deterministic**: The LLM decides when to loop, what to validate, and when to stop. It might skip validation, loop too many times, or stop prematurely.
- **No crash recovery**: If the session ends mid-phase, the agent must re-read state and figure out where it was. Checkpoint.json helps, but there's no code to enforce recovery.
- **Self-validation is weak**: The agent checking its own work is inherently less reliable than external validation.

These limitations are acceptable for the skill-only path. The tradeoff is: zero infrastructure requirements in exchange for less determinism.

---

## Path 2: Orchestrator-as-Code

This is the path described in `orchestrator_idea.md`, `orchestrator_and_harness.md`, and the rest of the deep_determinism specs. The orchestrator is a Python module. The harness adapter launches agents as subprocesses. RESULT.json is the structured result channel.

The harness-aware path adds:

- Deterministic loop (Python `while` loop, not LLM judgment)
- External validation (validators run after the agent, not by the agent)
- Crash recovery (checkpoint.json read at startup, resume from last valid state)
- Timeout enforcement (subprocess timeout, not agent self-regulation)
- Permission enforcement (harness-level, not instruction-level)

### When to Use

Use the harness-aware path when:

- You have Python available
- Your harness can run bash commands
- You need deterministic execution
- You need crash recovery
- You need external validation

Use the skill-only path when:

- You don't have Python
- Your harness can't run bash
- You're pasting into a chat interface
- You want zero setup
- You accept less determinism

---

## Harness Companion Model

### What a Companion Is

A harness companion is a small reference file (~40 lines) that tells the orchestrator skill how to optimize for a specific harness. It lives at `skills/contextsmith-orchestrator/references/harness-<name>.md`.

### What a Companion Contains

Each companion has exactly three sections:

1. **Agent launch**: How to start an agent in this harness (command, flags, agent config format)
2. **Permission model**: How this harness enforces permissions (agent config, tool restrictions)
3. **Result protocol**: How to communicate structured results (RESULT.json, inline response, or both)

### Companion Template

```markdown

# Harness: <name>

## Agent Launch

Describe how to launch a bounded agent step in this harness.

- Command or mechanism: ...
- Agent profile format: ...
- Step cap mechanism: ...
- Timeout mechanism: ...

## Permission Model

Describe how permissions are enforced.

- Read-only: ...
- Edit: ...
- External action: ...

## Result Protocol

Describe how the agent communicates structured results.

- Primary: RESULT.json on disk (if supported)
- Fallback: structured section in agent response
- Format: { "status": "pass|fail|blocked", "reason": "...", "artifacts": [...], "issues": [...], "next_action": "..." }
```

### Existing Companions

| Companion | File | Harness |
| ----------- | ------ | --------- |
| OpenCode | `references/harness-opencode.md` | OpenCode CLI with agent profiles, --max-steps, RESULT.json |
| Cursor | `references/harness-cursor.md` | Cursor with .cursorrules, inline results |
| Generic | `references/harness-generic.md` | Any harness, no optimizations, inline results |

### Loading Rules

The orchestrator skill loads companions conditionally:

```yaml

# In reference_manifest.yml

- source: shared/harness-opencode.md

  load: conditional
  when: harness is opencode or agent is running in OpenCode

- source: shared/harness-cursor.md

  load: conditional
  when: harness is cursor or agent is running in Cursor

- source: shared/harness-generic.md

  load: conditional
  when: harness is unknown or no other companion matches
```

The companion is loaded ONLY when the harness is detected or specified. If no companion matches, the orchestrator skill works with its base instructions (skill-only mode).

---

## Installation Methods

### Method 1: Skill-only (zero setup)

Copy the orchestrator skill into your agent's skills directory. No Python, no packages, no config.

```

# For any harness
Copy skills/contextsmith-orchestrator/ → your agent's skills directory
Copy shared/ → your agent's references directory (optional, for richer context)
```

Works in: any harness that supports skills or custom instructions.

### Method 2: Harness-optimized (pip install)

Install the Python package. The orchestrator runs as code. The harness adapter manages agent subprocesses.

```bash
pip install contextsmith
contextsmith init --harness opencode
```

Creates:

- `.contextsmith/` with default workflow configs
- `.opencode/agents/contextsmith-*.md` with agent profiles
- `.opencode/commands/contextsmith-*.md` with user-facing commands

Works in: OpenCode, Cursor (with terminal), any harness with bash access.

### Method 3: Hybrid (skill + code)

Install the orchestrator as code, but use the skill for the router and workflow-developer. The skill generates the workflow config; the orchestrator code runs it.

```bash
pip install contextsmith

# Use /contextsmith to generate a workflow config
# Use python -m orchestrator to run it deterministically
```

Works in: OpenCode, Cursor, any harness with both skills and bash.

---

## What Each Installation Method Weighs

| Component | Skill-only | Harness-optimized | Hybrid |
| ----------- | ----------- | ------------------- | -------- |
| Orchestrator SKILL.md | ~200 lines | — | ~200 lines |
| Harness companion | ~40 lines | — | ~40 lines |
| Python orchestrator | — | ~500 lines | ~500 lines |
| Harness adapter | — | ~200 lines | ~200 lines |
| Agent configs | — | ~15 lines each | ~15 lines each |
| Shared references | optional | ~2000 lines | ~2000 lines |
| **Total agent context** | **~240 lines** | **~0 (code runs)** | **~240 lines** |
| **Total disk** | **~240 lines** | **~700 lines + shared** | **~940 lines + shared** |
| **Determinism** | **low** | **high** | **high** |
| **Infrastructure** | **none** | **Python + harness** | **Python + harness** |

---

## Relationship to Existing Skills

### contextsmith-run

`contextsmith-run` is the current execution skill (342 lines). It has its own execution contract compilation, evidence ledger, validation gates, and Ralph loops. The orchestrator-as-skill replaces its internal loop logic with the workflow-config-driven loop.

Two options:

1. **contextsmith-run becomes the orchestrator skill**: Rewrite its loop to use workflow configs. Keep its existing references (execution-contract, evidence-ledger, domain-packs).
2. **Orchestrator is a new skill, contextsmith-run delegates to it**: contextsmith-run detects when a workflow config exists and routes to the orchestrator. For simple prompts without configs, it uses its existing logic.

Option 2 is safer — it preserves backward compatibility for existing contextsmith-run users.

### contextsmith (router)

The router skill dispatches to the orchestrator instead of directly to contextsmith-run when a workflow config exists. The router's routing table becomes:

| User Intent | Sub-Skill |
| --- | --- |
| Execute a workflow config | `contextsmith-orchestrator` |
| Execute a simple prompt | `contextsmith-run` |
| Generate a workflow config | `contextsmith-workflow-developer` |
| Create or improve a prompt | `contextsmith-prompt-engineer` |
| (other existing routes) | (unchanged) |

### contextsmith-workflow-developer (new)

The missing skill that generates workflow configs from natural language. This is the plan generation gap (item 10 in prerequisites). See `workflow_developer_skill.md` for the design.

---

## Implementation Priority

1. **Write the orchestrator SKILL.md** — the universal loop instructions
2. **Write harness-opencode.md companion** — OpenCode-specific optimizations
3. **Write harness-generic.md companion** — fallback for unknown harnesses
4. **Update contextsmith router** — add orchestrator to routing table
5. **Design workflow-developer skill** — plan generation from natural language
6. **Decide contextsmith-run relationship** — delegate or replace

Steps 1-3 can be done immediately. Steps 4-6 need more design work.

---

## Related Docs

- `orchestrator_idea.md` for the orchestrator-as-code design
- `orchestrator_and_harness.md` for the HarnessAdapter ABC and HarnessResult
- `harness_agnostic_distribution.md` for the adapter model
- `workflow_config_sketch.md` for the workflow config schema
- `state_artifact_strategy.md` for artifact templates
- `implementation_prerequisites.md` for the full gap analysis
