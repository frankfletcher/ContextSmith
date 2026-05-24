# Phase Code Review

A long-running coding task should not move from one phase to the next just because the agent says “done.”

At the end of each coding phase, ContextSmith recommends a phase-local code review. This is not a broad rewrite. It is a bounded check of the changes made in that phase.

## Why this matters

Coding agents often make a plausible change, run a narrow validation, and move on. The problem is that a hidden issue can compound in later phases.

A post-phase review asks:

> Is this phase safe to build on?

## Default behavior

For coding domains, use:

```bash
--phase-review standard --code-review-iterations 1
```

That means:

- review the phase diff
- identify must-fix issues
- optionally apply one focused improvement pass
- rerun narrow validation
- record findings in the phase debrief

## Review checklist

Review only the phase changes unless broader inspection is needed.

Check:

- correctness
- edge cases
- test coverage
- test usefulness
- regressions
- simplicity
- maintainability
- security/secrets
- performance risks
- typing/lint/style issues
- project convention alignment

## Finding categories

Classify findings as:

- **Must fix before continuing**
- **Should fix if low risk**
- **Note for later phase**
- **Acceptable tradeoff**

Do not let “should fix” become an unbounded refactor.

## Focused improvement pass

Apply at most one improvement pass unless the user asks for deeper iteration.

Only change code if the improvement:

- fixes correctness
- strengthens a weak test
- removes unnecessary complexity
- aligns with project conventions
- reduces likely regression risk
- improves maintainability without broad refactor

Do not perform cosmetic refactors during phase review.

## Report format

```markdown
# Phase Code Review

## Scope
- Phase:
- Files reviewed:
- Validation run:

## Summary
- Overall assessment:
- Main risk:
- Recommendation: proceed / fix first / needs human review

## Findings

### Must Fix
- ...

### Should Fix
- ...

### Notes for Later
- ...

## Test Quality
- Baseline tests:
- Edge cases:
- Missing tests:
- Weak assertions:

## Improvements Applied
- ...

## Remaining Risks
- ...

## User Learning Notes
- ...
```

## Education level

Use `--education-level` to control how much explanation appears in the review report.

For tight context, keep model-facing notes compact and put deeper explanation in a separate human report.
