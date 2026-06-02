# Next Prompt: Phase 5A Next Prompt Compiler Specification

## Artifact Manifest
- artifact_type: next_prompt
- phase: 5A
- target_profile: qwen36
- parent_plan: PLAN.md
- version: 1.0.0

## Mission

Specify a small tool that compiles the current phase into a detailed small-model execution prompt. The compiler reads task state and generates `NEXT_PROMPT.md` files. It does not run the model or execute phases.

## Read Order

1. `STATUS.md` — current phase and next action
2. `PLAN.md` — Phase 5A section
3. `CONTEXT.md` — constraints and validation commands
4. `ARTIFACTS.md` — Phase 4B changed artifacts and validation evidence
5. `THIN_SKILL_WRITING_GUIDE.md` — thin-skill patterns for reference

## Actions

1. Review the Phase 5A specification requirements in PLAN.md.
2. Design the compiler spec: inputs, output sections, template structure, and hard-stop rules.
3. Prove the spec can generate a prompt shape matching the NEXT_PROMPT.md format used in this task.
4. Include validation, audit, closeout, recovery, and hard-stop sections in the generated prompt spec.

## Validation

- `python scripts/validate_skills.py` passes
- `python scripts/token_budget.py --strict` passes
- `python -m pytest tests/ -v` passes

## Closeout

Update `STATUS.md`, `PHASE_LOG.md`, `ARTIFACTS.md`, `CONTEXT.md`, `CHECKLIST.md`, and `NEXT_PROMPT.md` with compact facts only. Record changed files, commands run, validation result, blockers, carry-forward, do-not-carry-forward, and next action.

## Hard Stop

Do not proceed to Phase 5B. Do not implement the compiler. Do not invoke models or execute phases. Do not edit other skills or add new domain packs.
