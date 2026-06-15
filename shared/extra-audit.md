# Extra Audit

An open-ended review step to run *after* the baseline audit. The codified audit answers "is it valid?" This answers "is it headed in the right direction?"

## When to Use

Run after all validators, linters, tests, and A-F rubrics pass or are accounted for. Do not skip the baseline — extra-audit without ground truth is speculation.

## Core Principle

Baseline validation answers "does it work?" Extra-audit answers "are we building the right thing, in the right order, with the right scope?" These are different questions. Do not collapse them.

## Strategic Lenses

After baseline passes, step back and apply these lenses. Use each only if relevant — the list is exhaustive, your application should not be.

### Trajectory

Look at the project as a sequence of decisions, not a snapshot of files.

- What trajectory are the recent commits on? Are we converging on something coherent, or accumulating unrelated fixes?
- Are later phases still viable given what was learned in earlier phases? Does PLAN.md need re-scoping?
- If a phase keeps growing in scope, what is the stopping condition? Is it stated anywhere?
- Is there a simpler path to the same goal that avoids cumulative complexity?

### Dependency Surface

The visible work may hide hidden dependencies.

- What does the current work silently depend on that is not yet built, not yet tested, or not yet understood?
- Are any assumptions about the runtime, the harness, the model, the data, or the user's environment untested?
- Is there a chain where one unknown (e.g., "does this library support that feature?") blocks multiple downstream phases without a probing phase?

### Scope Pressure

Scope creeps. Surface it openly.

- Did this phase do more than planned? If yes, was that scope expansion justified or should it have been deferred?
- Is there work in the current diff that belongs in a different phase or a different task entirely?
- Are we over-building for the stated goal? Are we under-building and creating tech debt?
- What could be cut without breaking the stated objective?

### Reusability Leverage

One-off work today is repeated work tomorrow.

- Are the patterns in this work specific to this task, or would they benefit from extraction into shared references, a skill, a reusable script, or a template?
- If the same problem appeared in another project, would the solution be findable and reusable?
- Is there a general case hiding behind a specific implementation?

### Blind Spot Scan

Rubrics are systematic but limited. They cannot catch what they do not name.

- What does the rubric not check that you suspect matters? (Test flakiness? Error message quality? Onboarding time for a new contributor? Silent failure modes?)
- What would surprise someone who read the plan but not the code?
- If you had to hand this to a different agent with no chat history, what would break or confuse them? (Revisit NEXT_PROMPT.md and DECISIONS.md.)
- What would you change if you knew you only had one more phase to ship something useful?

### Exit Condition Honesty

- Is the project close enough to done that the remaining work is lower-value than stopping? Or is there still high-leverage work to do?
- Are we polishing things that do not matter while real risks remain unaddressed?
- What would a "good enough to ship" state look like? How far from it are we really?

## Applying Findings

For each finding from the extra audit:

1. **If complex and not already planned**: add a new phase to PLAN.md or a new entry to DECISIONS.md. Do not implement inline.
2. **If simple and within current phase scope**: apply it, then re-run the narrowest validation.
3. **If it invalidates an earlier decision**: update DECISIONS.md, note the reversal, and adjust downstream phases.
4. **If it is a risk with no clear fix**: capture it in a risk register section of STATUS.md or CONTEXT.md so it surfaces in the next phase.

Do not let extra-audit findings bloat the current phase. The purpose is to redirect, not to expand.

## Persistent Artifact: EXTRA_AUDIT.md

Every extra-audit step writes `EXTRA_AUDIT.md` to the task state directory. This file is append-only — each audit run adds a new section, never overwrites previous entries. The orchestrator recognizes `EXTRA_AUDIT.md` as a protected append-only file.

The orchestrator merges `.new` segments (see `orchestrator.orchestrator:PROTECTED_FILES`). Agents should write `EXTRA_AUDIT.md.new` instead of appending directly.

```markdown

## Extra Audit — YYYY-MM-DD

### Baseline Status

- Validation: pass / partial / fail
- Plan accuracy: plan-is-current / plan-needs-update / plan-is-blocking

### Trajectory Assessment

- Current trajectory: converging / drifting / needs-rescoping
- Key observation:

### Findings

| Finding | Lens | Severity | Action | Already in PLAN? |
| --- | --- | --- | --- | --- |

### Risks Not Yet Addressed

- ...

### What Would a Fresh Agent Need?

- ...

### Tradeoffs Accepted

- What was knowingly deferred or left imperfect, and why that was the right call.
```

Keep the review shorter than the baseline audit. Extra audit adds direction; it does not re-litigate correctness.

## Orchestrator Integration

Add `extra_audit` as a state in the workflow config when this step is desired:

```yaml
extra_audit:
  state: extra_audit
  agent: contextsmith-auditor
  permissions: read-only
  max_retries: 2
  timeout_s: 300
  transitions:

    - condition: pass

      target: closeout

    - condition: fail

      target: extra_audit

    - condition: max_retries

      target: blocked
  expected_outputs:

    - EXTRA_AUDIT.md

  inputs:

    - AUDIT_REPORT.md
    - PLAN.md
    - STATUS.md
```

The orchestrator constants define `STATE_EXTRA_AUDIT = "extra_audit"` and include it in `CANONICAL_STATES`. Include `extra_audit` in `phase_order` after the baseline audit step.
