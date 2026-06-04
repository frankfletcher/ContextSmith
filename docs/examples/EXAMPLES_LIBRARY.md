# Examples

Practical examples you can copy, adapt, and compare. Each example shows the input, the command or prompt, and the expected output.

## Table of Contents

- [Example 1: Run a Task-State Phase](#example-1-run-a-task-state-phase)
- [Example 2: Validate with a Domain Pack](#example-2-validate-with-a-domain-pack)
- [Example 3: Failure and Recovery](#example-3-failure-and-recovery)
- [Example 4: Prompt Engineering](#example-4-prompt-engineering)
- [Example 5: Implementation Plan Creation](#example-5-implementation-plan-creation)
- [Deferred Examples](#deferred-examples)

---

## Example 1: Run a Task-State Phase

**Status:** Implemented — uses contextsmith-run skill with NEXT_PROMPT.md handoff.

**Scenario:** You have a multi-phase task in `.agent_work/` and want the agent to execute the current phase with validation gates and a Ralph loop.

**Input:** A task directory with `STATUS.md`, `PLAN.md`, `CONTEXT.md`, and `NEXT_PROMPT.md`.

**Prompt:**
```
Run the prompt in this file:
.agent_work/sprints/my-project/tasks/2026-06-01-setup/NEXT_PROMPT.md
--ralph 2 --validation available
```

**What happens:**
1. The agent reads `STATUS.md` to determine the current phase.
2. The agent reads `PLAN.md` for the phase requirements.
3. The agent reads `CONTEXT.md` for constraints and known facts.
4. The agent executes the phase per the `NEXT_PROMPT.md` instructions.
5. The agent runs validation commands listed in the prompt.
6. The agent runs self-audit against the prompt's checklist.
7. The agent runs 2 Ralph loop iterations to review and fix material defects.
8. The agent updates task-state files and generates the next `NEXT_PROMPT.md`.

**Expected output:**
```
## Result
Phase 2A (Validator Core) complete. Created runtime/validator.py with 6 validators.
26 pytest tests pass.

## Validation
python scripts/validate_skills.py — OK
python scripts/token_budget.py --strict — OK
python -m pytest tests/ -v — 26 passed

## Ralph Summary
Iteration 1: fixed missing domain_pack rule 9 test and added warnings support.
Iteration 2: no-op by evidence.

## Risks / Next Action
Phase 2B (Domain Pack Validator) is next.
```

**Recovery:** If the phase fails validation, the agent updates `STATUS.md` with the blocker, records the failure in `PHASE_LOG.md`, and stops for human input.

---

## Example 2: Validate with a Domain Pack

**Status:** Implemented — uses the validator CLI and domain packs.

**Scenario:** You want to check whether an artifact (phase contract, evidence ledger, approval record, etc.) passes structural validation for your domain.

**Input:** A JSON artifact file and a domain pack.

**Command — validate a domain pack itself:**
```bash
python -m runtime.cli domain-pack runtime/domain_packs/software_engineering.json
```

**Expected output:**
```
PASS  runtime/domain_packs/software_engineering.json
```

**Command — validate a phase contract:**
```bash
python -m runtime.cli phase-contract tests/fixtures/phase_contract_good.json
```

**Expected output:**
```
PASS  tests/fixtures/phase_contract_good.json
```

**Command — validate an evidence ledger:**
```bash
python -m runtime.cli evidence tests/fixtures/evidence_ledger_good.json
```

**Expected output:**
```
PASS  tests/fixtures/evidence_ledger_good.json
```

**When validation fails:**
```bash
python -m runtime.cli phase-contract tests/fixtures/phase_contract_bad_missing_fields.json
```

**Expected output:**
```
FAIL  tests/fixtures/phase_contract_bad_missing_fields.json
  Rule 1: artifact_type must be "phase_contract" — got "wrong_type"
```

**Available domain packs:**
| Domain | Use When |
|--------|----------|
| `software_engineering` | Coding, testing, refactoring |
| `writing_editing` | Drafting, editing, rewriting |
| `research_summary` | Literature review, fact-checking |
| `scheduling` | Calendar operations, meetings |
| `travel_purchase` | Flight comparison, purchase planning |
| `general_fallback` | Any task not matching a specific domain |

---

## Example 3: Failure and Recovery

**Status:** Implemented — uses the recovery procedure from NEXT_PROMPT.md.

**Scenario:** A phase fails validation. Instead of continuing blindly, the workflow records the failure and stops for human input.

**What triggers recovery:**
- Validation command fails and cannot be fixed within the phase scope.
- Required context is missing or inconsistent.
- Side effects exceed permission boundaries.
- The phase hits a hard stop rule.

**Recovery procedure (from NEXT_PROMPT.md):**
1. Update `STATUS.md` with the blocker and current state.
2. Update `PHASE_LOG.md` with the failure and what was attempted.
3. Update `NEXT_PROMPT.md` with recovery instructions.
4. Stop and await human input.

**Example — validation failure:**

The agent attempts Phase 3C but `python -m pytest tests/ -v` reports 2 failures.

**Agent updates `STATUS.md`:**
```markdown
## Current Phase
Phase 3C blocked. pytest reports 2 failures in test_validator.py.
Blocker: Rule 9 test expects approval_gates to match external_action_boundaries,
but scheduling domain pack has a mismatched entry.

## Next Action
Fix the scheduling domain pack, then re-run Phase 3C.
```

**Agent updates `PHASE_LOG.md`:**
```markdown
### Phase 3C — Blocked (2026-06-02)
- Attempted: created scheduling domain pack and fixture, added validator tests
- Result: pytest fails — 2 tests in TestDomainPackScheduling
- Root cause: approval_gates entry "send_calendar_invite" has no matching
  external_action_boundaries entry
- Action: stop and await human input
```

**Human fix:**
Edit `runtime/domain_packs/scheduling.json` to add the missing `external_action_boundaries` entry, then resume:
```
Run the prompt in this file:
.agent_work/sprints/my-project/tasks/2026-06-01-my-task/NEXT_PROMPT.md
--ralph 2
```

---

## Example 4: Prompt Engineering

**Status:** Implemented — uses contextsmith-prompt-engineer skill.

**Scenario:** You have a task description and want to create a model-aware prompt optimized for a specific model profile with context controls and validation.

**Input:** Task description, target model profile, and domain.

**Prompt:**
```
Create a model-aware prompt for code review assistance.
--target-profile qwen36 --domain software-engineering --ralph 2
```

**What happens:**
1. The agent classifies the request: target model, domain, source mode, and side-effect tier.
2. The agent checks prompt-control feasibility for the requested improvements.
3. The agent selects relevant references from the skill's reference library.
4. The agent builds a prompt package with system prompt, user prompt template, context strategy, and validation plan.
5. The agent runs 2 Ralph loop iterations to review and fix material defects.
6. The agent audits the prompt package for chain-of-thought exposure, model-specific assumptions, and output contract testability.
7. The agent delivers the prompt package with an educational report.

**Expected output:**
```
## Engineering Metadata
Target: qwen36 | Domain: software-engineering | Mode: guided

## System Prompt
You are a code review assistant for Python projects. For each pull request:
1. Identify logic errors, security issues, and performance concerns
2. Reference specific line numbers and file paths
3. Suggest concrete fixes with code diffs
4. Flag items requiring human approval (dependency changes, API modifications)

## User Prompt Template
Review the following changes in {file_path}:
{diff_content}

Focus areas: {focus_areas}
Risk level: {risk_level}

## Context Strategy
Source mode: file-based. Load only changed files and test fixtures.
Re-anchor after each review section to maintain file context.

## Validation and Test Plan
- Review output includes line references for all findings
- No exposed chain-of-thought in review comments
- Risk classifications match side-effect matrix tiers

## Ralph Summary
Iteration 1: tightened context strategy and added loop-safety rules.
Iteration 2: no-op by evidence.

## Risks / Next Action
Prompt is ready for use. Test with actual PR diffs before production use.
```

**Recovery:** If the prompt doesn't meet requirements, adjust the target profile, domain, or context parameters and re-run. Use `--education-level deep` for a detailed report on what was changed and why.

---

## Example 5: Implementation Plan Creation

**Status:** Implemented — uses contextsmith-instruction-engineer skill.

**Scenario:** You have a multi-step project and want the agent to generate a phased implementation plan with validation gates, task-state tracking, and model-aware instructions.

**Input:** Project description, scope, and target model profile.

**Prompt:**
```
Create an implementation plan for migrating our Python project from unittest to pytest.
--target-profile qwen36 --domain software-engineering --ralph 2
```

**What happens:**
1. The agent classifies the instruction target: implementation plan for a coding migration.
2. The agent inspects the repository selectively — existing test files, build config, and instruction files.
3. The agent scans existing safeguards to reuse or strengthen them rather than duplicate.
4. The agent detects coding standards from the repo stack and applies relevant references.
5. The agent builds a phased plan with validation gates, phase debriefs, and task-state directory structure.
6. The agent creates task-state files: `TASK.md`, `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `CONTEXT.md`, `PHASE_LOG.md`, and `NEXT_PROMPT.md`.
7. The agent runs 2 Ralph loop iterations to review and fix material defects in the plan.

**Expected output:**
```
## Detected Project Profile
Language: Python | Tests: unittest (42 files) | Framework: none
Existing instruction files: AGENTS.md (loop safety present, no phase plan)

## Changes Made
- Added phased implementation plan with 5 phases
- Required task-state directory at .agent_work/sprints/migration/tasks/2026-06-03-pytest/
- Added validation gates: pytest dry-run, coverage check, lint pass per phase
- Added phase debrief and do-not-carry-forward notes

## Safeguards Reused / Strengthened / Added
- Reused: existing loop-safety rules from AGENTS.md
- Strengthened: Git safety now requires approval before branch deletion
- Added: persistent task state with required artifact list
- Added: phase closeout validation requiring test pass before advancement

## Validation Notes
- All 5 phases have explicit stop rules and validation commands
- Task-state directory structure matches persistent-task-state.md spec
- Plan includes test strategy and phase code review gates

## Ralph Summary
Iteration 1: added coverage threshold to Phase 3 validation gate.
Iteration 2: no-op by evidence.

## Remaining Risks / Assumptions
Phase 4 (fixture migration) may require manual fixture rewrites for parametrized tests.
Plan assumes no third-party test fixtures with custom unittest subclasses.

## Files Written
.agent_work/sprints/migration/tasks/2026-06-03-pytest/TASK.md
.agent_work/sprints/migration/tasks/2026-06-03-pytest/PLAN.md
.agent_work/sprints/migration/tasks/2026-06-03-pytest/STATUS.md
.agent_work/sprints/migration/tasks/2026-06-03-pytest/CONTEXT.md
.agent_work/sprints/migration/tasks/2026-06-03-pytest/PHASE_LOG.md
.agent_work/sprints/migration/tasks/2026-06-03-pytest/NEXT_PROMPT.md
```

**Recovery:** If the plan doesn't meet requirements, adjust the scope, add domain-specific constraints, or request a different phasing granularity. Use `--education-level deep` for a detailed breakdown of how each phase was designed.

---

## Deferred Examples

The following examples are planned for a later batch:

- **Plan audit** — use contextsmith-agent-evaluator to review a plan for completeness and small-model reliability.
- **Meeting scheduling** — non-coding example: schedule a meeting with approval gates for calendar writes.
- **Travel comparison** — non-coding example: compare flight options with travel_purchase domain pack boundaries.
