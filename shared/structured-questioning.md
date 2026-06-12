# Structured Questioning

Use the harness's structured question tool (e.g., `AskUserQuestion` in OpenCode, `question` tool) to gather user input through multiple-choice questions. Do this one question at a time unless questions are tightly related.

## When to Use Structured Questions

Use structured questions when:
- Presenting mutually exclusive options with clear trade-offs
- Gathering domain, harness, or profile selection
- Confirming a plan before execution
- Choosing between alternative approaches

Use open-ended questions when:
- Asking for freeform feedback on a design
- Asking the user to describe their intent
- Asking "does this look right?"

## Question Format

```yaml
Question: "<clear, specific question>"
Header: "<short label, max 30 chars>"
Options:
  - Label: "<option name>"
    Description: "<one-line trade-off or explanation>"
  - Label: "<option name>"
    Description: "<one-line trade-off or explanation>"
```

Rules:
- 2-5 options per question (3 is ideal)
- Each option has a one-line description explaining the trade-off
- Include a recommended default when applicable
- Header is a short label for the question topic

## Page-Flow Pattern

For multi-step input gathering, use a page-flow pattern:

```
Step 1: Understand intent (1-2 questions)
Step 2: Gather parameters (2-3 questions)
Step 3: Confirm before execution (1 summary question)
```

Each step is one question. After each answer, proceed to the next. After all steps, present a confirmation table and ask for approval.

### Confirmation Table Format

```
→ Summary:

  Parameters:
  ┌──────────────────┬────────────────────────────────────────┐
  │ Parameter        │ Value                                  │
  │ Parameter        │ Value                                  │
  └──────────────────┴────────────────────────────────────────┘

  [Yes, proceed] [No, let me modify → restart at step 2]
```

## Example: Workflow Config Generation

**Step 1: Understand intent**
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
  - Label: "Migration"
    Description: "Refactoring: plan, execute, validate, rollback"
```

**Step 2: Gather parameters**
```
Question: "Which model will run this workflow?"
Header: "Target Model"
Options:
  - Label: "Generic local"
    Description: "Default profile for any local/open-weight model"
  - Label: "Qwen 3 (6B)"
    Description: "Optimized for Qwen3 27B and nearby models"
  - Label: "Gemma 4"
    Description: "Optimized for Gemma 4 variants"
```

**Step 3: Confirm**
```
→ Workflow config will be generated:

  ┌──────────────────┬────────────────────────────────────────┐
  │ Domain           │ coding                                 │
  │ Target profile   │ generic-local                          │
  │ Phases           │ load → implement → audit → validate → close │
  │ Gates            │ audit, validate                        │
  │ Ralph cycles     │ 1                                      │
  └──────────────────┴────────────────────────────────────────┘

  [Yes, generate it] [No, let me modify]
```

## Backtracking

If the user's response to a later question reveals a constraint that invalidates an earlier answer, go back to the earlier question. Don't force linear progression.

## Integration

This pattern applies to:
- `contextsmith-workflow-developer` — gathering workflow intent
- `contextsmith` (router) — wizard mode
- `contextsmith-run` — refinement questions
- Any skill that needs structured user input
