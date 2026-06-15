# Next Prompt Compiler Specification

## Artifact Manifest

- artifact_type: specification
- phase: 5A
- target_profile: qwen36
- version: 1.0.0

## Purpose

The Next Prompt Compiler is a read-only tool that reads task-state files and generates a detailed `NEXT_PROMPT.md` for the current phase. It prepares safe handoffs for small-model executors. It does not run models, execute phases, or advance task state.

## Inputs

| Input | Required | Source |
| --- | --- | --- |
| `STATUS.md` | Yes | Current phase name, next action, blockers |
| `PLAN.md` | Yes | Current phase block: goal, actions, validation, context contract |
| `CONTEXT.md` | Yes | File map, constraints, validation commands, skip rules |
| `CHECKLIST.md` | No | Completed items for context |
| `DECISIONS.md` | No | Durable decisions affecting current phase |
| `ARTIFACTS.md` | No | Changed artifacts from prior phases |
| `PHASE_LOG.md` | No | Prior phase outcomes for carry-forward |

The compiler extracts the current phase from `STATUS.md`'s `current_phase` or `next_required_action` field, then locates the matching phase block in `PLAN.md`.

## Output: NEXT_PROMPT.md Template

The compiler generates a `NEXT_PROMPT.md` with these sections in order:

### 1. Artifact Manifest

```markdown

# Next Prompt: <phase name>

## Artifact Manifest

- artifact_type: next_prompt
- phase: <phase id>
- target_profile: <from PLAN.md artifact manifest or default qwen36>
- parent_plan: PLAN.md
- version: 1.0.0
```

### 2. Mission

A single paragraph stating the phase goal and hard boundary. Derived from the PLAN.md phase `## Goal` and `## Purpose` fields. Must include a negative constraint: what the phase must NOT do.

### 3. Read Order

Ordered list of files the executor should read first. Derived from:

- `STATUS.md` (always first)
- Current phase block in `PLAN.md` (always second)
- `CONTEXT.md` (always third)
- Phase-specific files named in the PLAN.md phase `## Inputs` or `## Actions` sections

### 4. Phase Contract

Extracted from the PLAN.md phase `context_contract` YAML block. For small-model prompts, include only the fields the executor needs to self-regulate: `usable_phase_budget`, `expected_tool_calls`, `stop_rule`, and `validation_output_reserve`. Omit `executor`, `phase_type`, and `compaction_trigger` (these are compiler concerns, not executor concerns). This keeps the generated prompt compact.

### 5. Actions

Numbered list of concrete actions from the PLAN.md phase `## Actions` section. Each action must reference a specific file path, command, or artifact. Abstract actions are rewritten to name the exact file or command.

### 6. Allowed and Disallowed Actions

| Allowed | Disallowed |
| --- | --- |
| <from phase actions> | <from phase stop_rule> |
| <from CONTEXT.md validation commands> | editing files outside workspace |
|  | proceeding to next phase |
|  | invoking models |

Disallowed actions are derived from the phase `stop_rule`, CONTEXT.md constraints, and the universal hard-stop rule (no phase advancement).

### 7. Validation Commands

Exact commands from CONTEXT.md `## Validation Commands` section, filtered to those relevant to the current phase type. For implementation/test phases, include `python -m pytest tests/ -v`. For design phases, include `python scripts/validate_skills.py` and `python scripts/token_budget.py --strict` if skill files may change.

### 8. Task-State Closeout Requirements

```markdown

## Closeout

Update `STATUS.md`, `PHASE_LOG.md`, `ARTIFACTS.md`, `CONTEXT.md`, `CHECKLIST.md`, and `NEXT_PROMPT.md` with compact facts only. Record changed files, commands run, validation result, blockers, carry-forward, do-not-carry-forward, and next action.
```

This section is generated from PLAN.md's `## Required Phase Closeout` template, specialized to the current phase's expected outputs.

### 9. Recovery Procedure

```markdown

## Recovery

If validation fails or the phase cannot complete:

1. Stop. Do not widen scope or start the next phase.
2. Set `STATUS.md` to `Blocked` with the failed gate and exact reason.
3. Add a `PHASE_LOG.md` entry with attempted action and validation result.
4. Write `NEXT_PROMPT.md` for human/frontier review with at most three options: fix, narrow scope, or abandon.
```

Derived from PLAN.md's `## Recovery Procedure` section.

### 10. Self-Audit Requirements

```markdown

## Self-Audit

Before closeout, verify:

- Original phase goal satisfied or blocker recorded
- All validation commands executed or blocker documented
- Side-effect boundaries respected
- Task state updated with compact facts
- No broad architecture decisions made without evidence
```

Derived from the domain pack's self-audit lens (defaults to `general_fallback` if domain unspecified).

### 11. Expected Final Output Format

```markdown

## Result
## Evidence
## Self-Audit
## Ralph Summary
## Validation
## Declared vs Enforced
## Risks / Next Action
```

Standardized output format for the executor's final response.

### 12. Hard Stop

```markdown

## Hard Stop

Do not proceed to <next phase>. Do not implement features outside this phase. Do not invoke models or execute phases. Do not edit files outside the current phase scope.
```

The next phase is determined from PLAN.md phase ordering. This section always includes the universal constraints: no model invocation, no phase advancement, no out-of-scope edits.

### 13. Deep Education Notes (Optional)

When the PLAN.md phase includes an `## Education` section, the compiler extracts it as a collapsible or clearly separated section at the end of the prompt. These notes are for the human operator's understanding and are not execution instructions.

## Template Rendering Rules

1. **Markdown fence safety**: Use `~~~` for inner code blocks within the generated prompt. Use four-backtick fences (````) for Markdown template blocks. This prevents nested fence collisions.
2. **No nested execution instructions**: The compiler never generates instructions that tell the executor to run another phase or invoke a model.
3. **Concrete file paths**: All file references use paths relative to the task directory. No relative navigation like "the file above" or "see earlier".
4. **Compact facts only**: The generated prompt carries forward decisions, constraints, and commands. It does not carry raw output, search results, or resolved dead ends.
5. **Phase isolation**: The prompt only references the current phase's actions and validation. Prior phases appear only as context in the read order.

## Compiler CLI Interface

When implemented (Phase 5B), the compiler will be a CLI subcommand:

```bash
python -m runtime.cli next-prompt [OPTIONS]

Options:
  --task-dir PATH    Task directory containing state files (default: current dir)
  --output PATH      Output file path (default: NEXT_PROMPT.md)
  --phase PHASE_ID   Override current phase (default: read from STATUS.md)
  --include-education  Include deep education notes section
  --dry-run          Print to stdout without writing file
```

## Hard-Stop Rules for the Compiler Itself

1. The compiler must not execute phases.
2. The compiler must not invoke models.
3. The compiler must not advance task state (no writing to STATUS.md, PHASE_LOG.md, etc.).
4. The compiler must not modify source files outside the output `NEXT_PROMPT.md`.
5. If `STATUS.md` cannot determine the current phase, the compiler must exit with a clear error, not guess.
6. If the current phase block is missing from `PLAN.md`, the compiler must exit with a clear error.
7. If `STATUS.md` and `PLAN.md` disagree on the current phase (e.g., STATUS says Phase 5A but PLAN.md has no Phase 5A block, or the PLAN.md phase marks a different phase as current), the compiler must exit with an error naming both values and require human resolution.

## Validation

- Compiler spec proves it can generate a prompt matching the `NEXT_PROMPT.md` format used in this task (verified by comparing against the Phase 4B NEXT_PROMPT.md).
- Generated prompt includes all 12 required sections.
- Generated prompt does not contain instructions to execute the next phase.
- Generated prompt uses safe Markdown fence nesting.

## Verification Against Existing NEXT_PROMPT.md

Comparing this spec's output template against the Phase 4B NEXT_PROMPT.md file:

| Spec Section | NEXT_PROMPT.md Section | Match |
| --- | --- | --- |
| 1. Artifact Manifest | `## Artifact Manifest` | Yes |
| 2. Mission | `## Mission` | Yes |
| 3. Read Order | `## Read Order` | Yes |
| 4. Phase Contract | (implicit in phase context) | Covered |
| 5. Actions | `## Actions` | Yes |
| 6. Allowed/Disallowed | (implicit in hard stop) | Covered |
| 7. Validation Commands | `## Validation` | Yes |
| 8. Closeout | `## Closeout` | Yes |
| 9. Recovery | (from PLAN.md) | Added |
| 10. Self-Audit | (from domain pack) | Added |
| 11. Output Format | (standardized) | Added |
| 12. Hard Stop | `## Hard Stop` | Yes |

The spec covers all existing sections and adds recovery, self-audit, and output format sections that were previously implicit in the skill instructions.
