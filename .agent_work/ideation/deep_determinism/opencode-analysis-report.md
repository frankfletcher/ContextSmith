# OpenCode Feature Analysis for ContextSmith

**Date:** 2026-06-09
**Purpose:** Assess which OpenCode features can improve ContextSmith reliability and determinism, and how they fit with the orchestrator idea.

---

## Executive Summary

The highest-impact opportunities for determinism are **Custom Tools** and **Plugins**, but the bigger architectural answer is the **orchestrator**: a script that owns state, retries, checkpoints, and transitions. OpenCode agents are best treated as leaf executors inside that orchestration layer. **Commands** are useful launchers, while **ACP** and
**MCP** are transport/integration layers rather than determinism mechanisms.

---

## 1. Custom Tools

**What it is:** TypeScript/JavaScript functions the LLM can call, defined in `.opencode/tools/` or `~/.config/opencode/tools/`. Can wrap scripts in any language.

### General Pattern Opportunity: Workflow Gate Tools

ContextSmith skills describe multi-phase workflows (e.g., prompt-engineer has phases: analyze, design, implement, validate). Currently, the model decides when to move between phases. Custom tools could enforce transitions:

- `phase_complete(phase_name)` — agent must call this to mark a phase done
- `phase_validate(phase_name)` — runs validation before allowing next phase
- `checklist_verify()` — confirms all required artifacts exist

This is a **general concept** (workflow enforcement via tool calls) that belongs in the deterministic orchestration layer. In an OpenCode setup, custom tools can become convenient gatekeepers, but the orchestrator should still own the actual workflow state machine.

### Determinism Value: HIGH

Without enforcement, models skip phases, merge steps, or produce incomplete outputs. A tool-gated workflow makes phase completion explicit and verifiable.

### Implementation Approach

Create an opencode-specific specialization only if the backing code exists. Until then, document the pattern and keep it concept-level. When implemented, the package could contain:

- `phase_gate.ts` — validates phase prerequisites before allowing continuation
- `artifact_check.ts` — verifies required files exist at each phase boundary
- `validation_run.ts` — executes `scripts/validate_skills.py` and gates progress on success

---

## 2. ACP (Agent Client Protocol)

**What it is:** OpenCode can run as an ACP-compatible subprocess, communicating via JSON-RPC over stdio. Works with Zed, JetBrains, Avante.nvim, CodeCompanion.nvim.

### General Pattern Opportunity: NONE

ACP is a transport protocol. It doesn't change what the agent can do, only how it connects to an editor. ContextSmith skills are already harness-agnostic at the instruction level.

### Determinism Value: LOW

No direct impact on workflow determinism. Relevant only if ContextSmith wants to document "these skills work in ACP-hosted editors."

### Recommendation

No action needed. If ContextSmith creates an opencode specialization, it naturally works via ACP since ACP exposes the same feature surface.

---

## 3. MCP Servers

**What it is:** Model Context Protocol servers (local or remote) that expose tools to the LLM. Configured in `opencode.jsonc`. Supports OAuth, environment variables, per-agent enable/disable.

### General Pattern Opportunity: External Validation as MCP

ContextSmith could define a general pattern: "use external tools for validation rather than asking the model to self-check." For opencode, this maps to MCP servers.

Specific use cases:

- A local MCP server that runs `scripts/validate_skills.py` and returns structured results
- A remote MCP server for checking skill compatibility against a registry

### Determinism Value: MEDIUM

MCP tools add context overhead (the docs warn about token bloat). For ContextSmith's use case, Custom Tools are a better fit — they're lighter weight and don't require a separate server process.

### Recommendation

Skip MCP for now. Custom Tools cover the same ground with less overhead. Revisit if ContextSmith needs to integrate with existing MCP infrastructure (e.g., a shared validation service).

---

## 4. Commands

**What it is:** Custom slash commands (`/my-command`) defined as markdown files or JSON config. Support arguments, shell output injection (`!`command``), file references (`@file`), and can target specific agents/models.

### General Pattern Opportunity: Phase Commands

ContextSmith workflows could map to commands:

- `/contextsmith-audit` — triggers the agent-evaluator skill with pre-loaded criteria
- `/contextsmith-migrate` — triggers the skill-migrator with backup and staging
- `/contextsmith-validate` — runs the validation script and reports results

This is a **general concept** (shortcut commands for common workflows) that improves usability but not determinism.

### Determinism Value: MEDIUM (for usability, not correctness)

Commands reduce friction for starting a workflow correctly (the right skill, right agent, right model). They don't prevent mid-workflow drift.

### Implementation Approach

Create an opencode-specific commands package:

```
.opencode/commands/
├── contextsmith-audit.md
├── contextsmith-migrate.md
├── contextsmith-validate.md
└── contextsmith-create.md
```

Each command frontmatter specifies the appropriate agent, model, and temperature. The body loads the relevant skill and provides structured initial instructions.

---

## 5. Agents

**What it is:** Specialized AI configurations with custom prompts, models, temperatures, permissions, and max steps. Two types: primary (direct interaction) and subagent (invoked by primary).

### General Pattern Opportunity: Role-Specific Agent Profiles

ContextSmith skills already define roles (evaluator, engineer, migrator, prompt-engineer). These map naturally to opencode agents, but not because of temperature. The useful agent features are permissions, step limits, model pinning, and role-specific system prompts:

| ContextSmith Skill | Agent Config | Key Controls | Permissions |
| --- | --- | --- | --- |
| agent-evaluator | `contextsmith-auditor` | `steps`, model pinning | read-only, no bash |
| skill-engineer | `contextsmith-builder` | model pinning, repo access | edit allow, bash allow |
| skill-migrator | `contextsmith-migrator` | `steps`, retry policy | edit + bash for backup ops |
| prompt-engineer | `contextsmith-prompter` | model pinning | edit, no external_directory |

### Determinism Value: HIGH

This is the most useful harness-level control for deterministic execution, but not because of low temperature. The real wins are: read-only audit profiles, step caps to prevent looping, and permissions that stop unsafe side effects. The model can keep its normal agentic temperature while the harness enforces boundaries.

### Implementation Approach

Create an opencode-specific agents package only when the runtime is ready:

```
.opencode/agents/
├── contextsmith-auditor.md    # read-only, step-capped, review-only
├── contextsmith-builder.md    # edit-capable, repo-aware
├── contextsmith-migrator.md   # edit + bash for staged migration
└── contextsmith-prompter.md   # edit-only, no external directories
```

Each agent's prompt file should load the corresponding ContextSmith skill content and add only harness-specific behavior: permission boundaries, step caps, and agent role clarity.

---

## 6. Plugins

**What it is:** JavaScript/TypeScript modules that hook into events: tool execution (before/after), session lifecycle, file edits, compaction, etc.

### General Pattern Opportunity: Workflow Enforcement Plugin

This is the most powerful mechanism for enforced determinism. A plugin can:

1. **Enforce phase completion** — `tool.execute.after` hook checks if the agent is trying to move to phase N without completing phase N-1
2. **Run validation gates** — `file.edited` hook triggers `validate_skills.py` when SKILL.md files change
3. **Persist state across compaction** — `experimental.session.compacting` hook injects workflow state into the compaction summary
4. **Block dangerous operations** — `tool.execute.before` hook prevents destructive Git commands without explicit approval

### Determinism Value: VERY HIGH

Plugins operate at the harness level, not the instruction level. They can enforce the orchestrator's invariants: file edits trigger validation, state survives compaction, and blocked operations are blocked before the model can pretend they succeeded. That makes them a natural companion to the orchestrator, not a replacement for it.

### Implementation Approach

Create an opencode plugin: `contextsmith-workflow-guard.ts`

```typescript
export const ContextSmithGuard = async ({ $, worktree }) => {
  return {
    // Validate SKILL.md on every edit
    "file.edited": async (input, output) => {
      if (input.filePath.includes("SKILL.md")) {
        const result = await $`python3 ${worktree}/scripts/validate_skills.py`.text()
        // Log validation result
      }
    },
    // Preserve workflow state across context compaction
    "experimental.session.compacting": async (input, output) => {
      output.context.push(
        "## Workflow State\n" +
        "- Current phase: [phase]\n" +
        "- Completed phases: [list]\n" +
        "- Pending validations: [list]\n" +
        "CRITICAL: Do not skip phases. Complete all pending validations before proceeding."
      )
    },
  }
}
```

---

## How This Fits the Orchestrator

The orchestrator idea and the OpenCode harness idea are complementary:

1. **The orchestrator owns workflow state.** It decides what state comes next, when to retry, and when to stop.
2. **OpenCode agents execute one bounded step at a time.** The orchestrator chooses which agent profile to invoke for each step.
3. **Custom tools become optional gate checks.** They can validate preconditions or outputs, but they do not replace the orchestrator's checkpoint file.
4. **Plugins enforce invariants at the harness boundary.** They are useful for validation-on-edit and compaction-state injection.
5. **Commands are entry points only.** They help users start the right workflow with the right agent, but they are not the source of truth for progression.

In practice, this means the cleanest design is:

- `Workflow DSL` in Python for the deterministic state machine
- `AgentInvoker` to call OpenCode with the correct role profile
- `Validator Registry` to check files and command results
- `Checkpoint file` in `.agent_work/` for crash recovery
- OpenCode `agents`, `tools`, and `plugins` only as runtime accelerators

The baseline workflow itself should be represented as YAML or JSON config owned by the orchestrator. Agent-generated plans can add or remove optional steps, but they should not be the authoritative source for required gates.

That keeps the model-facing instructions smaller and moves determinism into code where it belongs.

---

## Recommended Implementation Priority

### Phase 1: General Patterns (harness-agnostic)

These go into ContextSmith skills and shared references:

1. **Workflow Phase Gates** — Document the pattern of using tool calls to mark phase completion, but keep the actual gate in the orchestrator.
2. **Validation-First Principle** — Skills should specify that validation commands must run before declaring a phase complete.
3. **Persistent State for Compaction** — Document that long workflows should write state to disk (`.agent_work/`) so it survives context compaction.

### Phase 2: OpenCode Specialization (harness-specific)

Create `skills/contextsmith-opencode/` or `docs/reference/opencode-integration.md`:

1. **Agents** — Pre-configured agent profiles for each ContextSmith role (highest practical value)
2. **Commands** — Workflow shortcut commands
3. **Custom Tools** — Optional phase gate tools for enforced workflow progression

### Phase 3: Advanced (optional)

4. **Plugin** — Workflow guard plugin for automatic validation and state preservation
5. **MCP** — Only if external validation services become relevant

---

## Key Insight: What Makes Workflows Deterministic

The core problem ContextSmith tries to solve is: **models skip steps**. There are three layers of defense:

| Layer | Mechanism | Can Model Ignore? |
| --- | --- | --- |
| **Instructions** (SKILL.md) | "Follow these phases in order" | Yes — model can skip |
| **Tools** (Custom Tools) | Must call `phase_complete()` to proceed | Partially — model can call out of order |
| **Plugins** (Event Hooks) | Intercepts tool calls, runs validation | No — runs outside model control |

For maximum determinism, all three layers are needed. ContextSmith currently only has layer 1. Adding opencode-specific custom tools (layer 2) and plugins (layer 3) would close the gap.

---

## What's NOT Worth Doing

- **ACP specialization** — no behavioral difference, just transport
- **MCP servers** — custom tools are lighter weight for the same purpose
- **Over-engineering the plugin** — start with agents + commands; add the plugin only if phase-skipping remains a problem after Phase 2
