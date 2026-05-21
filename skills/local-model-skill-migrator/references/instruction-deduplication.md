# Instruction Scan and De-Duplication

Before adding safeguards, scan existing repo/agent instruction files and detect whether equivalent rules already exist.

## Files to Check

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `.github/copilot-instructions.md`
- `.cursorrules`
- `.windsurfrules`
- `.cursor/rules/*`
- `.continue/config.*`
- `.aider.conf.yml`
- harness-specific instruction files

## Detect Equivalent Safeguards

Check for existing coverage of:

- tool-call format discipline
- no identical consecutive tool calls
- retry budgets
- error recovery strategy
- no-op edit detection
- anti-brainstorming / act-after-planning rule
- phase stop conditions
- context economy
- persistent task state
- Git safety
- human escalation conditions

## Merge Policy

Use this priority order:

1. Preserve clear, specific, correct safeguards.
2. Strengthen vague safeguards.
3. Remove or consolidate duplicates only when editing that file is in scope.
4. Add missing safeguards in the most appropriate location.
5. Avoid repeating the same safeguard in multiple files unless one is root-level and one is genuinely subproject-specific.

## Token-Bloat Guard

Before finalizing, check whether the artifact contains duplicated or near-duplicated rules.

If duplicates exist:

- keep the most specific and testable version
- remove weaker variants
- consolidate related rules into one checklist

One crisp rule beats five similar reminders.
