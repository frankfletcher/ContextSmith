# Examples

Practical examples you can copy, adapt, and compare. Each example shows the input, the command or prompt, and the expected output.

## Table of Contents

- [Example 1: Run a Task-State Phase](#example-1-run-a-task-state-phase)
- [Example 2: Validate with a Domain Pack](#example-2-validate-with-a-domain-pack)
- [Example 3: Failure and Recovery](#example-3-failure-and-recovery)
- [Example 4: Prompt Engineering](#example-4-prompt-engineering)
- [Example 5: Implementation Plan Creation](#example-5-implementation-plan-creation)
- [Example 6: Plan Audit](#example-6-plan-audit)
- [Example 7: Meeting Scheduling](#example-7-meeting-scheduling)
- [Example 8: Travel Comparison](#example-8-travel-comparison)
- [Example 9: Skill Migration](#example-9-skill-migration)
- [Example 10: Custom Domain Pack](#example-10-custom-domain-pack)
- [Example 11: Agent Evaluation](#example-11-agent-evaluation)
- [Deferred Examples](#deferred-examples)

---

## Example 1: Run a Task-State Phase

**Status:** Implemented — uses contextsmith-orchestrator skill with NEXT_PROMPT.md handoff.

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

## Example 6: Plan Audit

**Status:** Implemented — uses contextsmith-agent-evaluator skill.

**Scenario:** You have an implementation plan and want to audit it for completeness and small-model reliability.

**Input:** A plan file (e.g., `PLAN.md`) or a task-state directory.

**Prompt:**
```
Audit the implementation plan at .agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/PLAN.md
for completeness and small-model reliability.
--target-profile qwen36 --domain coding --ralph 2
```

**What happens:**
1. The agent classifies the artifact as an implementation plan.
2. The agent selects the target model profile (qwen36).
3. The agent inspects the plan against rubric criteria (context contracts, phase budgets, validation gates, etc.).
4. The agent runs 2 Ralph loop iterations to review and fix material defects in the audit.
5. The agent delivers the audit report with grades, strengths, weaknesses, and recommended fixes.

**Expected output:**
```
## Summary Grade
B+ (Good overall structure, some minor weaknesses in phase budgeting clarity).

## Strengths
- Plan defines a clear universal protocol and domain packs.
- Phase contracts include context budgets and stop rules.
- Recovery procedure is well-defined.

## Weaknesses
- Phase 0 discovery budget (78k) exceeds baseline estimate (40k-45k).
- Some phase contracts lack explicit validation_output_reserve details.

## A-F Rubric
| Dimension | Grade | Reason | Recommended Fix |
|---|---|---|---|
| Context Strategy | A | Clear read order and session boundaries. | None. |
| Persistent Task State | B+ | Required files listed, but some phases missing explicit validation_output_reserve. | Add validation_output_reserve to all implementation phases. |
| Loop Safety | A | Ralph loop iterations required. | None. |
| Git/File Safety | A | Approval boundaries defined. | None. |

## Loop / Git / Context Safety
- Loop safety: Ralph loop iterations specified.
- Git safety: Destructive operations require approval.
- Context safety: Fresh session rules defined.

## Domain-Specific Risks
- None identified for this coding domain plan.

## Duplicate or Conflicting Instructions
- None identified.

## High-Risk Issues
- Phase 0 budget estimation might be too low for complex discovery tasks.

## Suggested Next Action
- Fix phase budget estimates and add validation_output_reserve to Phase 2A, 2B, 2C.
- Re-run audit.
```

**Recovery:** If the audit finds material defects, update the plan, then re-run the audit.

---

## Example 7: Meeting Scheduling

**Status:** Implemented — uses contextsmith-orchestrator with scheduling domain pack.

**Scenario:** You want to schedule a cross-timezone meeting with approval gates for calendar writes.

**Input:** Participants, time zones, duration, preferred dates.

**Prompt:**
```
Schedule a meeting with the following details:
- Participants: Alice (EST), Bob (PST)
- Duration: 1 hour
- Preferred dates: Tomorrow 2-4pm EST, day after 10am-12pm EST
--domain scheduling --ralph 2
```

**What happens:**
1. The agent classifies the request as a scheduling task.
2. The agent loads the scheduling domain pack.
3. The agent resolves time zones and finds candidate slots.
4. The agent requests approval before sending invites.
5. The agent records sent confirmation evidence.

**Expected output:**
```
## Candidate Slots
- Tomorrow 2:00 PM - 3:00 PM EST (11:00 AM - 12:00 PM PST)
- Tomorrow 3:00 PM - 4:00 PM EST (12:00 PM - 1:00 PM PST)
- Day after 10:00 AM - 11:00 AM EST (7:00 AM - 8:00 AM PST)

## Approval Request
Send calendar invite for Tomorrow 2:00 PM - 3:00 PM EST?
- Participants: Alice (EST), Bob (PST)
- Time zones resolved: EST, PST
- Duration: 1 hour
- Evidence: slots calculated from preferred dates

## Sent Confirmation
Calendar invite sent for Tomorrow 2:00 PM - 3:00 PM EST.
- Invite ID: 12345
- Participants notified: Alice, Bob
- Evidence: invite ID recorded
```

**Recovery:** If no suitable slots are found, adjust preferred dates or duration, then re-run.

---

## Example 8: Travel Comparison

**Status:** Implemented — uses contextsmith-orchestrator with travel_purchase domain pack.

**Scenario:** You want to compare flight options for a business trip without purchasing.

**Input:** Dates, airports, passenger count, budget constraint.

**Prompt:**
```
Compare flight options for a business trip:
- Departure: JFK (New York)
- Arrival: LAX (Los Angeles)
- Dates: 2026-06-15 to 2026-06-18
- Passengers: 1
- Budget: $500 max
--domain travel_purchase --ralph 2
```

**What happens:**
1. The agent classifies the request as a travel comparison task.
2. The agent loads the travel_purchase domain pack.
3. The agent searches for available flights matching the criteria.
4. The agent compares options by price, fees, refund terms, and residual risks.
5. The agent presents a comparison table without implying purchase capability.

**Expected output:**
```
## Flight Options Comparison

| Airline | Departure | Arrival | Price | Fees | Refund Terms | Notes |
|---------|-----------|---------|-------|------|--------------|-------|
| Delta | 2026-06-15 08:00 | 2026-06-15 11:00 | $420 | $35 | Non-refundable | Direct flight |
| United | 2026-06-15 10:00 | 2026-06-15 13:00 | $380 | $45 | Refundable ($50 fee) | 1 stop |
| American | 2026-06-15 14:00 | 2026-06-15 17:00 | $350 | $50 | Non-refundable | 1 stop |

## Residual Risk Disclosure
- Prices are timestamped: 2026-06-04 10:30 UTC
- Fees and baggage policies may change
- No booking or purchase is implied
- User approval required for any external action

## Recommendation
Option 1 (Delta) offers the best balance of price and convenience, but Option 3 (American) is cheapest if flexibility is needed.
```

**Recovery:** If no suitable options are found, adjust dates, airports, or budget, then re-run.

---

## Example 9: Skill Migration

**Status:** Implemented — uses contextsmith-skill-migrator skill.

**Scenario:** You have an existing skill and want to migrate it for small-model compatibility with target-profile metadata.

**Input:** Existing SKILL.md file, target profile (e.g., generic-local).

**Prompt:**
```
Migrate the skill at skills/contextsmith-prompt-engineer/SKILL.md for small-model compatibility.
--target-profile generic-local --ralph 2
```

**What happens:**
1. The agent classifies the request as a skill migration task.
2. The agent analyzes the source skill's structure and content.
3. The agent applies model profiles and context-aware workflows.
4. The agent adds loop safety rules and optimizes for small-model execution.
5. The agent validates the migrated skill against budget and validation constraints.

**Expected output:**
```
## Migration Summary
Source: skills/contextsmith-prompt-engineer/SKILL.md
Target profile: generic-local
Line count: 279 (within 3000 line budget)
Token count: 3797 (within 3800 token budget)

## Changes Made
- Added target-profile metadata to frontmatter
- Simplified complex workflows for small-model execution
- Added explicit context budget constraints
- Strengthened loop safety rules
- Optimized reference selection for local models

## Validation Results
- `python scripts/validate_skills.py`: OK
- `python scripts/token_budget.py --strict`: OK
- Skill preserves source behavior: PASS
- Line budget respected: PASS
- Token budget respected: PASS

## Ralph Summary
Iteration 1: tightened context budget constraints and added explicit reference selection rules.
Iteration 2: no-op by evidence.

## Residual Risks
- Some complex workflows may require further simplification for very small models
- Recommendation: test with actual local model execution before production use
```

**Recovery:** If migration fails validation or exceeds budget, adjust target profile or simplify further, then re-run.

---

## Example 10: Custom Domain Pack

**Status:** Implemented — uses the validator CLI.

**Scenario:** You want to create a custom domain pack for a new use case (e.g., education/lesson planning).

**Input:** Domain name, triggers, required artifacts, validation gates, approval boundaries.

**Command:**
```bash
python -m runtime.cli domain-pack runtime/domain_packs/education.json
```

**What happens:**
1. The agent defines the domain name and triggers (e.g., "education", "lesson-planning").
2. The agent lists required artifacts (e.g., `requirements_chain`, `phase_contract`).
3. The agent defines validation gates (e.g., check audience level, learning objectives).
4. The agent defines approval boundaries (e.g., external publication requires approval).
5. The agent writes the domain pack as a compact JSON file.
6. The agent validates the domain pack using the validator CLI.

**Expected output:**
```json
{
  "domain_name": "education",
  "triggers": ["education", "lesson-planning", "tutoring"],
  "required_artifacts": ["requirements_chain", "phase_contract"],
  "validation_gates": [
    {
      "name": "check_audience_level",
      "description": "Verify audience level is specified",
      "check_type": "deterministic"
    },
    {
      "name": "check_learning_objectives",
      "description": "Verify learning objectives are measurable",
      "check_type": "deterministic"
    }
  ],
  "approval_gates": [
    {
      "name": "external_publication",
      "description": "External publication or submission",
      "requires_approval": true,
      "side_effect_tier": "external_action"
    }
  ],
  "external_action_boundaries": [
    {
      "name": "publish_lesson_plan",
      "description": "Publish lesson plan to external platform",
      "requires_approval": true
    }
  ],
  "residual_risk_disclosures": [
    "Learning outcomes may vary based on student engagement",
    "External publication requires content review"
  ],
  "example_good_closeout": "Lesson plan created with audience level, objectives, and approval boundaries",
  "example_blocked_closeout": "Missing audience level specification"
}
```

**Validation Output:**
```
PASS  runtime/domain_packs/education.json
```

**Recovery:** If validation fails, check the violation messages and fix the JSON structure or missing fields, then re-run the validation command.

---

## Example 11: Agent Evaluation

**Status:** Implemented — uses contextsmith-agent-evaluator skill.

**Scenario:** You have an agent workflow file (such as an AGENTS.md or a custom workflow specification) and want to evaluate it for small-model reliability, context safety, and loop-safety before rolling it out to your team.

**Input:** An AGENTS.md file or agent workflow specification, target model profile.

**Prompt:**
```
Evaluate the agent workflow at AGENTS.md for small-model reliability and context safety.
--target-profile qwen36 --domain software-engineering --ralph 2
```

**What happens:**
1. The agent classifies the artifact as an agent instruction file (AGENTS.md) and runs in audit-only mode (no file modifications).
2. The agent selects the target model profile (qwen36) and detects the domain (software-engineering).
3. The agent inspects the workflow against rubric criteria: context strategy, persistent task state, loop safety, Git/file safety, side-effect boundaries, and no exposed chain-of-thought.
4. The agent checks for duplicate or conflicting instructions, upstream skill interoperability issues, and domain-specific risks.
5. The agent grades each dimension A-F using the evaluation rubrics.
6. The agent runs 2 Ralph loop iterations to review and fix material defects in the evaluation report.
7. The agent delivers the evaluation report with grades, strengths, weaknesses, and recommended fixes.

**Expected output:**
```
## Summary Grade
B+ (Good overall structure with clear safeguards. Minor weaknesses in context budget specification and state file requirements.)

## Strengths
- Git safety rules are explicit and cover destructive operations.
- Loop safety prevents repeated identical tool calls.
- Side-effect tiers are defined with approval boundaries.
- Coding standards reference PEP 8 and project conventions.

## Weaknesses
- Context budget limits are not specified for tool-heavy phases.
- Persistent task state section lists files but does not require compact factual content.
- No explicit compaction trigger when context approaches limits.
- Missing NEXT_PROMPT.md handoff requirement for multi-phase workflows.

## A-F Rubric
| Dimension | Grade | Reason | Recommended Fix |
|---|---|---|---|
| Context Strategy | B | Read order defined but no budget limits or compaction trigger. | Add usable_phase_budget and compaction_trigger to tool-heavy phases. |
| Persistent Task State | B+ | Required files listed but content guidelines vague. | Require compact factual state: paths, commands, results, decisions, next action. |
| Loop Safety | A | Explicit no-repeat rule and max retry limit. | None. |
| Git/File Safety | A | Destructive operations require approval. | None. |
| Side-Effect Boundaries | A | Tier matrix with approval gates. | None. |
| No Chain-of-Thought | A | No exposed reasoning requirements. | None. |

## Loop / Git / Context Safety
- Loop safety: Ralph loop iterations specified, no repeated identical calls.
- Git safety: Destructive operations (reset --hard, rebase, force push) require approval.
- Context safety: Fresh session rules for tool-heavy phases, but no explicit budget limit.

## Domain-Specific Risks
- Software engineering: no explicit test strategy or code review gate for multi-file changes.
- Recommendation: add pytest/lint validation requirement before phase closeout.

## Duplicate or Conflicting Instructions
- None identified. Git safety rules are consistent across sections.

## High-Risk Issues
- Missing NEXT_PROMPT.md handoff requirement could cause context drift in multi-phase workflows.
- No explicit stop rule for when validation fails twice.

## Suggested Next Action
- Add context budget limits and compaction triggers to tool-heavy phases.
- Require NEXT_PROMPT.md generation at phase closeout for resumable workflows.
- Add test strategy and code review gates for software engineering tasks.
- Re-run evaluation after fixes.
```

**Recovery:** If the evaluation finds material defects, update the agent workflow file to address the recommended fixes, then re-run the evaluation. Use `--education-level deep` for a detailed breakdown of each grading dimension and why specific scores were assigned.

---

## Deferred Examples

The following examples are planned for a later batch:

(none) — all starter examples are now implemented.
