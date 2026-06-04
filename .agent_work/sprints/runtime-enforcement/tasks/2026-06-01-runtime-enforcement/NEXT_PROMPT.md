# Phase 8C.6: Plan Audit Example

## Objective
Create the plan audit example for `docs/examples/EXAMPLES_LIBRARY.md` — a copy-paste example showing how to use contextsmith-agent-evaluator to review a plan for completeness and small-model reliability.

## Context
Phase 8C.6 is the third of 5 deferred examples from Phase 7F. The example should show a realistic plan audit workflow with expected output.

## Pattern
Follow the same structure as the existing 5 examples in `docs/examples/EXAMPLES_LIBRARY.md`:
- Status label (Implemented)
- Scenario description
- Input
- Prompt or command
- What happens (numbered steps)
- Expected output (with Result, Validation, Ralph Summary, Risks sections)
- Recovery note

## Steps
1. Read `docs/examples/EXAMPLES_LIBRARY.md` for the existing example pattern.
2. Read `skills/contextsmith-agent-evaluator/SKILL.md` for agent evaluation workflow details.
3. Create the plan audit example covering:
   - Scenario: auditing an implementation plan for completeness and small-model reliability
   - Input: plan file or task-state directory, audit scope
   - Prompt: invoke contextsmith-agent-evaluator with controls
   - What happens: the agent audits the plan against rubric criteria
   - Expected output: shows Result, Validation, Ralph Summary sections
   - Recovery: what to do if the plan has material defects
4. Update `docs/examples/EXAMPLES_LIBRARY.md` to add the new example and remove it from the Deferred Examples section.
5. Validate: `python scripts/validate_skills.py`, `python scripts/token_budget.py --strict`.
6. Self-audit: project voice, practical and copyable, expected outputs, no marketing language, stable headings.
7. Ralph loop: 2 iterations.

## Constraints
- Bounded to one example. Do not create additional examples in this phase.
- Do not modify existing examples.
- Use the project voice from `shared/documentation-quality.md`.
- Example must show expected outputs and be copy-paste usable.

## Validation
- `python scripts/validate_skills.py`
- `python scripts/token_budget.py --strict`
- Self-audit: follows established example pattern, shows expected output, practical scenario

## Stop Rule
Stop when the plan audit example is added to EXAMPLES_LIBRARY.md, the deferred section is updated, validations pass, and Ralph loop completes 2 iterations.
