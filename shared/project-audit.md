# Project Audit Prompt

A reusable prompt for auditing "the project so far" — runs codified validation, then gives the agent structured leeway to think strategically about gaps and direction.

## Instructions (agent-facing)

Run a baseline check first — validators, linters, tests, any configured A-F rubrics. Note failures. Do not skip this step.

Then audit the work across these dimensions. Use each only if relevant to the current project stage.

### 1. What Actually Happened vs. What Was Planned?

Check git log, file diffs, task state files. Are we ahead, behind, or drifting? If no PLAN.md exists, note that as a finding.

### 2. What Is Incomplete, Fragile, or Unresolved?

Do not limit yourself to what linters catch. Look for: half-finished logic, missing edge cases, hardcoded paths or secrets, inconsistent naming, dead code, untested paths, silent failure modes, over-engineering, under-engineering. Point to specific files and lines.

### 3. What Is Actually Good?

Be specific. If something is solid, say so. Honest praise is as important as critique — it prevents needless rework.

### 4. What Is the Risk Profile?

Classify each finding:

- **must-fix**: blocks correctness or safety
- **should-fix**: will cause pain or accumulate debt
- **acceptable tradeoff**: knowingly imperfect, right call for now
- **future-phase**: already scheduled in PLAN.md

### 5. Cross-Reference with PLAN.md

For each gap, check whether PLAN.md already addresses it in a later phase. If yes, note that. If no, consider whether it should be added. Also audit PLAN.md itself — is it still accurate, or does it need updating based on what you learned?

### 6. Fresh-Agent Fragility Check

If someone picked up `.agent_work/` task state tomorrow with no chat history, what would confuse or block them? Are NEXT_PROMPT.md and DECISIONS.md clear enough to resume without context loss?

### 7. Extra Audit

After the codified audit is done, load and apply `shared/extra-audit.md`. Step back and ask the harder questions — trajectory, dependency surface, scope pressure, reusability leverage, blind spots, exit condition honesty. This is where you have full leeway. The rubrics and validators are done; now think.

Write findings to `EXTRA_AUDIT.md` (or `EXTRA_AUDIT.md.new` for orchestrator-managed task state). This file is append-only — each audit run adds a new section.

## Output Format

```markdown
## Audit Summary

Assessment: on-track / needs-course-correction / off-track
Baseline validation: pass / partial / fail
Plan accuracy: plan-is-current / plan-needs-update

## Findings

| Finding | Severity | Location | Already in PLAN? | Note |
|---|---|---|---|---|

## Strengths

- ...

## Risks Not Yet Addressed

- ...

## Plan for Gaps (do not execute)

1. ...
```

The extra-audit findings (from `shared/extra-audit.md`) go into `EXTRA_AUDIT.md` as a separate persistent artifact. Keep it shorter than the baseline audit — it adds direction, it does not re-litigate correctness.

## Constraints

- Be honest over agreeable. If nothing is wrong, say so. If everything is wrong, say that too. Do not pad.
- Do not implement fixes during the audit. Produce the plan only.
- If the extra audit identifies a complex cross-cutting change, add it to PLAN.md as a new phase — do not implement inline.
