# End-to-End Example: Building a Skill

This walkthrough shows what a user sees when running a complete workflow from start to finish.

## Scenario

User wants to build a new ContextSmith skill for code review. They're running in OpenCode with the orchestrator installed.

## Step 1: User Invokes Workflow Developer

```
User: /contextsmith-workflow-developer build me a skill for code review
```

## Step 2: Skill Gathers Input (Page-Flow)

**Question 1:**

```
Question: "What kind of workflow should I create?"
Header: "Workflow Type"
Options:

  - Label: "Coding"

    Description: "Software engineering: implement, test, review, deploy"

  - Label: "Writing"

    Description: "Content creation: draft, edit, review, publish"

  - Label: "Research"

    Description: "Analysis: gather sources, synthesize, audit, report"
```

**User selects:** "Coding"

**Question 2:**

```
Question: "How much review should the output get?"
Header: "Quality Level"
Options:

  - Label: "Quick"

    Description: "One pass, minimal review, fast delivery"

  - Label: "Standard"

    Description: "Audit gate + validation, balanced quality"

  - Label: "Thorough"

    Description: "Audit + Ralph loops + validation, highest quality"
```

**User selects:** "Standard"

## Step 3: Confirmation

```

## Parameters

| Flag | Value | Why |
| ------ | ------- | ----- |
| `--mode` | `guided` | Default for interactive work |
| `--target-profile` | `generic-local` | No model specified |
| `--context-length` | `64k` | Default |
| `--domain` | `coding` | Code review is coding domain |
| `--ralph` | `0` | Standard quality, no Ralph loops |
| `--validation` | `available` | Run checks when possible |
| `--output` | `project-local` | Save under .agent_work/ |

## Plan

1. Generate workflow_config.yaml with coding domain template
2. Create task-state directory at .agent_work/sprints/code-review/tasks/2026-06-12-code-review-skill/
3. Write TASK.md, PLAN.md, STATUS.md, CONTEXT.md, CHECKLIST.md
4. Validate config against schema

## Ready?

[Yes, proceed] [No, let me modify]
```

**User:** "yes"

## Step 4: Files Generated

```
Created: .agent_work/sprints/code-review/tasks/2026-06-12-code-review-skill/
  ├── workflow_config.yaml
  ├── TASK.md
  ├── PLAN.md
  ├── STATUS.md
  ├── CONTEXT.md
  └── CHECKLIST.md
```

## Step 5: User Invokes Orchestrator

```
User: /contextsmith-orchestrator run the workflow in .agent_work/sprints/code-review/tasks/2026-06-12-code-review-skill/
```

## Step 6: Orchestrator Confirmation

```

## Parameters

| Flag | Value | Why |
| ------ | ------- | ----- |
| `--mode` | `guided` | Default for interactive work |
| `--workflow` | `workflow_config.yaml` | User provided |
| `--state` | `.agent_work/.../2026-06-12-code-review-skill/` | User provided |

## Plan

1. Phase 1: load_context — read STATUS.md, PLAN.md, CONTEXT.md
2. Phase 2: implement_change — create the SKILL.md
3. Phase 3: audit_output — review the skill for reliability
4. Phase 4: validate — run validation script
5. Phase 5: close — write SUMMARY.md and NEXT_PROMPT.md

## Ready?

[Yes, proceed] [No, let me modify]
```

**User:** "go"

## Step 7: Orchestrator Executes Phase 1 (load_context)

```
[orchestrator] Phase: load_context
[orchestrator] Reading STATUS.md, PLAN.md, CONTEXT.md...
[orchestrator] State: init → pass → implement_change
[orchestrator] Checkpoint written
```

Agent reads task state, understands the project structure, writes STATUS.md update.

## Step 8: Orchestrator Executes Phase 2 (implement_change)

```
[orchestrator] Phase: implement_change
[orchestrator] Dispatching to contextsmith-builder...
```

Agent reads NEXT_PROMPT.md, which says:

```
Create a SKILL.md for a code review skill. Include:

- Frontmatter with name, description, metadata
- Workflow for reviewing code changes
- Validation gates
- Reference manifest
```

Agent creates the SKILL.md, writes ARTIFACTS.md and PHASE_LOG.md.

```
[orchestrator] Validating artifacts...
[orchestrator] SKILL.md: exists, 156 lines, has frontmatter
[orchestrator] ARTIFACTS.md: exists, 12 lines
[orchestrator] PHASE_LOG.md: exists, 8 lines
[orchestrator] Status: pass → audit_output
[orchestrator] Checkpoint written
```

## Step 9: Orchestrator Executes Phase 3 (audit_output)

```
[orchestrator] Phase: audit_output
[orchestrator] Dispatching to contextsmith-auditor...
```

Agent reads SKILL.md, checks for:

- Valid frontmatter
- Specific description
- Reference manifest
- No exposed chain-of-thought
- Loop safety

Agent writes AUDIT_REPORT.md:

```markdown

# Audit Report

## Summary
Skill passes structural and semantic checks.

## Findings

- Low: description could be more specific about review types
- Info: reference manifest includes 3 shared references

## Overall Verdict
pass
```

```
[orchestrator] Validating artifacts...
[orchestrator] AUDIT_REPORT.md: exists, 15 lines, has Summary and Verdict
[orchestrator] Status: pass → validate
[orchestrator] Checkpoint written
```

## Step 10: Orchestrator Executes Phase 4 (validate)

```
[orchestrator] Phase: validate
[orchestrator] Running validation script...
[orchestrator] python scripts/validate_skills.py
[orchestrator] OK code-review-skill: 156 lines, version=1.0.0, refs=True
[orchestrator] Status: pass → close
[orchestrator] Checkpoint written
```

## Step 11: Orchestrator Executes Phase 5 (close)

```
[orchestrator] Phase: close
[orchestrator] Writing SUMMARY.md and NEXT_PROMPT.md...
[orchestrator] Status: pass → done
[orchestrator] Checkpoint written
[orchestrator] Workflow complete!
```

## Final State

```
.agent_work/sprints/code-review/tasks/2026-06-12-code-review-skill/
├── workflow_config.yaml    # The workflow config
├── TASK.md                 # Task definition
├── PLAN.md                 # Phase plan
├── STATUS.md               # Current: done
├── CONTEXT.md              # Project context
├── CHECKLIST.md            # All items checked
├── ARTIFACTS.md            # Files created
├── PHASE_LOG.md            # 5 phase entries
├── AUDIT_REPORT.md         # Audit findings
├── SUMMARY.md              # Final summary
├── NEXT_PROMPT.md          # (empty, workflow complete)
├── RESULT.json             # Last phase result
└── checkpoint.json         # Final checkpoint
```

## What the User Sees

The user sees:

1. Two confirmation dialogs (workflow-developer, orchestrator)
2. Real-time progress as each phase executes
3. Validation results after each phase
4. Final summary when complete

The user can:

- Modify parameters at any confirmation
- Interrupt with Ctrl-C (checkpoint saved)
- Resume later (orchestrator reads checkpoint)
- Inspect state (STATUS.md, PHASE_LOG.md)
