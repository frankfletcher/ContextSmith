# Instruction Precedence

Use this hierarchy when instructions, generated specs, skill outputs, repo rules, user preferences, or generic best practices conflict.

## Priority Order

1. User's current explicit request
2. Safety, privacy, permission, destructive-action, and external side-effect boundaries
3. Actual project/repo/source evidence
4. Existing repo instructions such as `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursorrules`, and nested instruction files
5. Target model/profile constraints
6. Domain-specific requirements
7. External skill artifacts/specs/plans
8. Optional style preferences
9. Generic best practices

## Conflict Resolution

When instructions conflict:

1. Identify the conflicting rules.
2. Apply the priority order.
3. Prefer the more specific and evidence-backed rule.
4. Prefer the safer rule for side effects, Git, external actions, privacy, secrets, or destructive operations.
5. Preserve valid domain-specific artifacts when they do not conflict.
6. Report the resolved conflict in the educational report or audit.

Do not average conflicting instructions. Resolve by evidence, priority, and safety.
