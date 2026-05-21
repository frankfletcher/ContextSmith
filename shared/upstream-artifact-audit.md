# Upstream Artifact Audit

Use this when a prompt, skill, AGENTS.md file, implementation plan, spec, or instruction artifact has already been modified by another optimizer, skill, scaffolder, or agent.

## Audit Steps

1. Identify upstream artifacts and their likely source.
2. Extract requirements, suggestions, assumptions, tools, frameworks, dependencies, workflows, and constraints added by the upstream tool.
3. Verify each addition against user request, project evidence, source files, package/config files, and selected domain/model/harness profile.
4. Classify each addition as confirmed, likely, useful suggestion, unsupported, conflicting, or rejected.
5. Preserve confirmed requirements.
6. Downgrade unsupported requirements to suggestions or remove them.
7. Reject conflicting or hallucinated requirements.
8. Report what was preserved, modified, rejected, and why.

## Required Report Block

```markdown
## Upstream Artifact Audit

### Preserved
- ...

### Modified / Downgraded
- ...

### Rejected
- ...

### Conflict Resolution
- ...
```

## Red Flags

- Frontend frameworks added to backend/MCP/server-only projects without evidence.
- New dependencies added without package/config evidence or user request.
- Runtime settings treated as controllable when the harness cannot control them.
- Implementation workflow added that duplicates or conflicts with an existing workflow.
- Generic best practices promoted to hard requirements.
