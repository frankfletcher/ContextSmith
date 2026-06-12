# OpenCode Harness Appendix

Load this reference when `--harness opencode` is specified. It maps ContextSmith concepts to opencode primitives and recommends configurations that improve determinism.

## Agent Selection

When working in opencode, select or recommend an agent that matches the ContextSmith role. If the user has configured ContextSmith agents (see **Agent Configs** below), mention them with `@`.

The value of custom agents is not temperature control but **permission boundaries**, **step limits**, and **model pinning**. These are the mechanisms that enforce determinism — the model cannot edit files it doesn't have permission for, cannot run arbitrary bash, and cannot exceed step limits.

| ContextSmith Role | Recommended Agent | Max Steps | Key Permissions |
|---|---|---|---|
| Agent Evaluator (audit) | `@contextsmith-auditor` or built-in `Plan` | 10 | edit deny, bash deny, webfetch deny |
| Skill Engineer (create/edit) | `@contextsmith-builder` or built-in `Build` | — | edit allow, bash allow, external_directory deny |
| Skill Migrator (batch migrate) | `@contextsmith-migrator` or built-in `Build` | — | edit allow, bash ask, git allow |
| Prompt Engineer (create/edit) | `@contextsmith-prompter` or built-in `Build` | — | edit allow, bash allow, external_directory deny |
| Instruction Engineer (AGENTS.md) | `@contextsmith-builder` or built-in `Build` | — | edit allow, bash allow |
| Run (execute handoff) | `@contextsmith-runner` or built-in `Build` | as declared | per handoff contract |

If custom agents are not available, use the built-in Plan agent for audit-only work and Build for file-changing work. Recommend the user set up custom agents for repeatable workflows.

## Agent Configs

Recommended opencode agent definitions for ContextSmith. These go in `.opencode/agents/` or `~/.config/opencode/agents/`:

### contextsmith-auditor.md

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
    "python -m runtime.cli*": allow
  webfetch: deny
---
```

### contextsmith-builder.md

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

### contextsmith-migrator.md

```yaml
---
description: Migrates skill directories between profiles or installations
mode: subagent
permission:
  edit: allow
  bash:
    "*": ask
    "cp *": allow
    "mkdir *": allow
    "python scripts/validate_skills.py": allow
    "git status*": allow
    "git diff*": allow
---
```

## Command Shortcuts

If the user has ContextSmith commands configured (see **Command Configs** below), use them as entry points:

| Command | Purpose | Equivalent |
|---|---|---|
| `/contextsmith-audit` | Audit an artifact | Load agent-evaluator skill |
| `/contextsmith-build` | Create or improve a skill | Load skill-engineer skill |
| `/contextsmith-migrate` | Migrate skills | Load skill-migrator skill |
| `/contextsmith-validate` | Run validation script | `python scripts/validate_skills.py` |

If commands are not available, proceed with the skill directly. Recommend the user set up commands for repeatable workflows.

## Command Configs

Recommended opencode command definitions. These go in `.opencode/commands/` or `~/.config/opencode/commands/`:

### contextsmith-audit.md

```yaml
---
description: Audit a prompt, skill, or instruction file
agent: contextsmith-auditor
---
Audit the artifact at $ARGUMENTS (or the current working directory if no path given).
Load the contextsmith-agent-evaluator skill and run a full audit.
Run `python scripts/validate_skills.py` if the artifact is a SKILL.md.
```

### contextsmith-build.md

```yaml
---
description: Create or improve a SKILL.md skill
agent: contextsmith-builder
---
Load the contextsmith-skill-engineer skill.
Target artifact: $ARGUMENTS
```

### contextsmith-migrate.md

```yaml
---
description: Migrate skills to a new profile or location
agent: contextsmith-migrator
---
Load the contextsmith-skill-migrator skill.
Source: $1
Target profile: $2
```

### contextsmith-validate.md

```yaml
---
description: Run the ContextSmith validation script
---
Run `python scripts/validate_skills.py` and report results.
If validation fails, suggest fixes without applying them unless the user asks.
```

## Custom Tools for Workflow Gates

If the user has ContextSmith custom tools installed (see **Tool Configs** below), enforce phase-gated workflows:

1. **Before completing a phase**, call `contextsmith_phase_complete` with the phase name and a list of artifacts produced.
2. **Before moving to the next phase**, call `contextsmith_artifact_check` to verify required files exist.
3. **After editing a SKILL.md**, call `contextsmith_validate` to run the validation script.

If tools are not available, fall back to inline bash commands:
- Phase validation: `python scripts/validate_skills.py`
- Artifact check: `ls <expected-path>` or `test -f <path>`

## Tool Configs

Recommended custom tool definitions. These go in `.opencode/tools/`:

### contextsmith-phase-complete.ts

```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Mark a ContextSmith workflow phase as complete. Call this before moving to the next phase.",
  args: {
    phase: tool.schema.string().describe("Phase name, e.g. 'extract-contract', 'rewrite-skill', 'validate'"),
    artifacts: tool.schema.array(tool.schema.string()).describe("List of artifact paths produced in this phase"),
  },
  async execute(args) {
    // Verify artifacts exist
    const fs = await import("fs/promises")
    const results = []
    for (const path of args.artifacts) {
      try {
        await fs.access(path)
        results.push(`${path}: exists`)
      } catch {
        results.push(`${path}: MISSING`)
      }
    }
    return `Phase "${args.phase}" complete.\nArtifacts:\n${results.join("\n")}`
  },
})
```

### contextsmith-artifact-check.ts

```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Verify that required artifacts exist before proceeding to the next phase.",
  args: {
    required: tool.schema.array(tool.schema.string()).describe("List of required file paths"),
    phase: tool.schema.string().describe("Phase that requires these artifacts"),
  },
  async execute(args, context) {
    const fs = await import("fs/promises")
    const path = await import("path")
    const missing = []
    const present = []
    for (const relPath of args.required) {
      const fullPath = path.resolve(context.worktree, relPath)
      try {
        await fs.access(fullPath)
        present.push(relPath)
      } catch {
        missing.push(relPath)
      }
    }
    if (missing.length > 0) {
      return `BLOCK: Phase "${args.phase}" cannot start. Missing artifacts:\n${missing.join("\n")}`
    }
    return `OK: All ${present.length} artifacts present for phase "${args.phase}".`
  },
})
```

### contextsmith-validate.ts

```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Run the ContextSmith skill validation script.",
  args: {},
  async execute(args, context) {
    const { execa } = await import("execa")
    try {
      const result = await execa("python3", ["scripts/validate_skills.py"], {
        cwd: context.worktree,
        reject: false,
      })
      return result.exitCode === 0
        ? `Validation passed.\n${result.stdout}`
        : `Validation failed (exit ${result.exitCode}).\n${result.stdout}\n${result.stderr}`
    } catch (error) {
      return `Error running validation: ${error.message}`
    }
  },
})
```

## Plugin for Workflow Enforcement

If the user has the ContextSmith workflow guard plugin installed, the following behaviors are enforced automatically:

- **SKILL.md edits trigger validation**: After any SKILL.md file is edited, `scripts/validate_skills.py` runs automatically.
- **Workflow state survives compaction**: When the session context is compacted, the current phase, completed phases, and pending validations are injected into the compaction summary.

If the plugin is not installed, remind the model to:
1. Write workflow state to `.agent_work/` files regularly (they survive compaction)
2. Run `python scripts/validate_skills.py` after editing SKILL.md files

## Plugin Config

Recommended plugin. Goes in `.opencode/plugins/contextsmith-guard.ts` or `~/.config/opencode/plugins/contextsmith-guard.ts`:

```typescript
import type { Plugin } from "@opencode-ai/plugin"

export const ContextSmithGuard: Plugin = async ({ $, worktree }) => {
  return {
    // Validate SKILL.md on every edit
    "file.edited": async (input, output) => {
      if (input.filePath?.includes("SKILL.md")) {
        try {
          const result = await $`python3 ${worktree}/scripts/validate_skills.py`.text()
          // Validation runs silently; results appear in tool output
        } catch (e) {
          // Validation script not available — non-blocking
        }
      }
    },

    // Preserve workflow state across context compaction
    "experimental.session.compacting": async (input, output) => {
      const fs = await import("fs/promises")
      const path = await import("path")
      try {
        const statusFile = path.join(worktree, ".agent_work", "current-status.txt")
        const status = await fs.readFile(statusFile, "utf-8")
        output.context.push(
          "## ContextSmith Workflow State (survives compaction)\n" +
          status +
          "\nCRITICAL: Do not skip phases. Complete all pending validations before proceeding."
        )
      } catch {
        // No status file — not in a ContextSmith workflow
      }
    },
  }
}
```

## Determinism Checklist

When `--harness opencode` is active, verify these conditions for maximum determinism:

1. **Agent permissions**: Read-only agents cannot edit files. This prevents accidental changes during audit. Bash restrictions prevent destructive commands.
2. **Max steps**: Audit agents have `steps` limits to prevent runaway loops.
3. **Validation gates**: SKILL.md edits trigger `scripts/validate_skills.py` (via plugin or explicit tool call).
4. **Persistent state**: Long workflows write state to `.agent_work/` to survive compaction.
5. **Phase ordering**: If custom tools are available, phases are gated by `contextsmith_phase_complete`.
6. **Model pinning**: For consistent results, pin the agent to a specific model rather than relying on the harness default.

If any of these are missing, note the gap and recommend the corresponding opencode configuration.

## What to Tell the User

When recommending opencode-specific setup, be concrete:

- "Create `.opencode/agents/contextsmith-auditor.md` with read-only permissions and a 10-step limit to prevent runaway loops during audit."
- "Add `.opencode/commands/contextsmith-audit.md` so you can run `/contextsmith-audit` next time."
- "Install the workflow guard plugin at `.opencode/plugins/contextsmith-guard.ts` to auto-validate SKILL.md edits."

Do not recommend MCP servers for ContextSmith workflows — custom tools are lighter weight and cover the same needs.
