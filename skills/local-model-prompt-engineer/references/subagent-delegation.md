# Subagent Delegation

Use subagents to isolate context or perform independent validation. Do not use subagents as a default ritual.

## Use When

- many files or references
- large logs/transcripts/docs
- independent review criteria
- source/target comparison
- semantic drift risk
- high-risk validation
- long-running phase work

## Good Subagent Tasks

- extract a source contract
- inspect one directory or reference set
- audit for exposed chain-of-thought
- inventory commands, schemas, paths, or APIs
- validate a generated artifact against a checklist
- inspect domain-specific risks

## Bad Pattern

Do not give every subagent the entire repo, every file, or the full conversation.

## Report Schema

Require compact reports:

```markdown
## Scope
Files/directories inspected:

## Findings
- ...

## Must Preserve
- ...

## Risks
- ...

## Evidence
- path/section/line/excerpt

## Recommended Next Action
- ...
```

The main agent remains responsible for synthesis, conflict resolution, edits, state updates, and final decisions.
