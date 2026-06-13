# Run Configuration Preview

Before executing any non-trivial task, summarize the plan and parameters, then ask the user to confirm. This is the default behavior. Only skip it when the user explicitly opts out.

## Default Behavior

**Every skill that performs file changes, multi-step work, or side effects MUST:**
1. Summarize selected parameters (with explanations for inferred defaults)
2. Summarize the plan (what will be done, in what order)
3. Ask for confirmation before proceeding
4. If the user changes something, re-summarize and ask again
5. Only proceed on positive indication

This is the default. The user must explicitly opt out via flags or natural language.

## Opt-Out Flags

| Flag | Behavior |
|------|----------|
| `--mode yolo` | Skip all confirmations, proceed with defaults |
| `--no-preview-config` | Skip the preview (but still require approval for high-risk actions) |
| `--interaction silent` | Ask only when blocked or unsafe |
| "just do it", "don't ask", "skip confirmation" | Natural-language opt-out |

If the user says "build me a skill" without opting out, show the confirmation.

## Positive Indicators

Proceed when the user says any of:
- "yes", "y", "ok", "okay", "good", "go", "execute", "proceed", "do it", "run it", "start", "ship it", "looks good", "LGTM", "confirmed"

Do NOT proceed on:
- Silence or ambiguous responses
- "maybe", "I guess", "sure" (ask for explicit confirmation)
- Questions or change requests (re-summarize after addressing)

## Confirmation Format

The confirmation has three sections: Parameters, Plan, and Question.

### Section 1: Parameters

Show all selected parameters as CLI flags with inline explanations.

```markdown
## Parameters

| Flag | Value | Why |
|------|-------|-----|
| `--mode` | `guided` | Default for interactive work |
| `--target-profile` | `qwen36` | User mentioned Qwen/local model |
| `--context-length` | `64k` | Modern default, safe for most tasks |
| `--domain` | `coding` | Detected from project files |
| `--ralph` | `1` | One improvement pass for quality |
| `--validation` | `available` | Run checks when possible |
| `--self-audit` | `true` | Default: verify before complete |
| `--output` | `project-local` | Save under `<project>/.agent_work/` |
```

Rules:
- Show every parameter that affects behavior
- For inferred values, explain WHY (not just what)
- For defaults, say "Default" in the Why column
- Flag any low-confidence inferences

### Section 2: Plan

Summarize what will happen, in order. Keep it to 3-7 steps.

```markdown
## Plan

1. Read existing project structure and constraints
2. Generate SKILL.md with frontmatter, workflow, and references
3. Create reference_manifest.yml with shared dependencies
4. Run `python scripts/validate_skills.py` to verify
5. Present the skill for review before writing files
```

Rules:
- Steps are numbered and concrete
- Each step is one action, not a paragraph
- Include validation steps
- Include any approval gates

### Section 3: Question

Ask for confirmation. Use the structured question tool when available.

```markdown
## Ready?

[Yes, proceed] [No, let me modify] [Show me more detail]
```

Or using the question tool:
```
Question: "Ready to proceed with this plan?"
Header: "Confirm"
Options:
  - Label: "Yes, proceed"
    Description: "Execute the plan as summarized above"
  - Label: "No, let me modify"
    Description: "I want to change parameters or the plan"
  - Label: "Show me more detail"
    Description: "Expand the plan with more specifics before I decide"
```

## Re-Summarize on Change

If the user changes something after seeing the confirmation:

1. Update the changed parameter(s) in the Parameters table
2. If the change affects the plan, update the Plan section
3. Re-present the full confirmation (not just the diff)
4. Ask for confirmation again

Example:
```
User: "use gemma4 instead of qwen36"

→ Updated Parameters table (target-profile changed)
→ Re-present full confirmation
→ Ask: "Ready to proceed?"
```

## When to Skip

Skip the confirmation ONLY when ALL of these are true:
- User explicitly opted out (`--mode yolo`, "just do it", etc.)
- Task is low-risk (read-only, no file changes)
- No parameters were inferred (all explicitly provided)

Do NOT skip when:
- File changes are involved
- Parameters were inferred
- The task is multi-step
- Side effects exist
- The user hasn't explicitly opted out

## Skill Integration

Every ContextSmith skill that performs work should:

1. Load `references/run-configuration-preview.md` (this file) when the task involves file changes or multi-step work
2. Show the confirmation before executing
3. Wait for positive indication
4. Re-summarize on change

### Skills That Must Confirm

| Skill | Confirm When |
|-------|-------------|
| `contextsmith-prompt-engineer` | Always (creates/edits files) |
| `contextsmith-skill-engineer` | Always (creates/edits files) |
| `contextsmith-skill-migrator` | Always (moves/copies files) |
| `contextsmith-instruction-engineer` | Always (creates/edits files) |
| `contextsmith-workflow-developer` | Always (creates workflow config + task-state files) |
| `contextsmith-orchestrator` | Before first phase execution, unless `--interaction silent` |
| `contextsmith` (router) | After wizard completes, before dispatching |

### Skills That May Skip

| Skill | Skip When |
|-------|-----------|
| `contextsmith-agent-evaluator` | Audit-only (read-only), unless user asks for confirmation |

## Example: Full Confirmation Flow

```
User: "build me a skill for code review"

→ Skill infers parameters
→ Skill determines plan
→ Skill shows confirmation:

## Parameters

| Flag | Value | Why |
|------|-------|-----|
| `--mode` | `guided` | Default for interactive work |
| `--target-profile` | `generic-local` | No model specified |
| `--context-length` | `64k` | Default |
| `--domain` | `coding` | Code review is coding domain |
| `--ralph` | `1` | One improvement pass |
| `--validation` | `available` | Run checks when possible |
| `--output` | `project-local` | Save under .agent_work/ |

## Plan

1. Read existing project structure and conventions
2. Generate SKILL.md with code review workflow
3. Create reference_manifest.yml
4. Run validation script
5. Present skill for review before writing

## Ready?

[Yes, proceed] [No, let me modify]

→ User: "yes"
→ Skill executes

→ User: "use qwen36 and add ralph loops"
→ Skill re-summarizes with updated parameters
→ Skill asks again: "Ready to proceed?"
→ User: "go"
→ Skill executes
```

## Schema

The confirmation output follows this exact structure:

```yaml
confirmation:
  parameters:
    - flag: "--mode"
      value: "guided"
      reason: "Default for interactive work"
    - flag: "--target-profile"
      value: "qwen36"
      reason: "User mentioned Qwen/local model"
  plan:
    - step: 1
      action: "Read existing project structure"
    - step: 2
      action: "Generate SKILL.md"
    - step: 3
      action: "Run validation"
  question:
    text: "Ready to proceed?"
    options:
      - label: "Yes, proceed"
        description: "Execute the plan as summarized"
      - label: "No, let me modify"
        description: "Change parameters or plan"
```
