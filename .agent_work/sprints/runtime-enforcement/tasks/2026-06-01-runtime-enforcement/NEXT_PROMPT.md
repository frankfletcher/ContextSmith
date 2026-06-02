# Next Prompt: Runtime Enforcement for ContextSmith Skills

## Artifact Manifest
- artifact_type: next-prompt
- parent_task: TASK.md
- next_phase: Phase 0 baseline discovery
- behavioral_contract: Resume from files, not chat memory.

## Resume Prompt
Continue the runtime enforcement task for ContextSmith skills from `.agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/`.

Read these files first:
- `STATUS.md`
- `PLAN.md`
- `CONTEXT.md`
- `DECISIONS.md`
- `CHECKLIST.md`

Start with Phase 0 from `PLAN.md`: inspect release and packaging scripts to verify how installed skills can carry runtime validator code, universal protocol schemas, domain packs, fixtures, and metadata. Verify individual skill packages, release bundle behavior, and staged reference sync separately. Record exact packaging facts in `CONTEXT.md`, update `DECISIONS.md` only if evidence supports a distribution path, then update `STATUS.md`, `PHASE_LOG.md`, `ARTIFACTS.md`, and this `NEXT_PROMPT.md`.

After Phase 0, run Phase 0.5 before implementation: choose the first runtime surface slice. Default recommendation is CLI validator plus universal protocol plus one or two domain packs. Stop for human/frontier review if the best path includes runner, MCP, harness adapters, package design changes, or dependencies beyond pytest.

Respect approval boundaries:
- Do not edit `PACKAGE_SPEC.md` without explicit approval.
- Do not add dependencies without explicit approval, except pytest is pre-approved by current user for test phases.
- Do not modify user-level opencode configuration without explicit approval.
- Do not claim hard enforcement unless the harness actually blocks bypass.
- Do not ask a small model to make broad architecture decisions; use the review gates in `PLAN.md`.

Run `python scripts/validate_skills.py` after any skill or shared-reference changes. For Phase 0, avoid source changes unless discovery shows a safe, necessary metadata update.

Also run `python scripts/token_budget.py --strict` after any skill or shared-reference changes. Use each phase's `context_contract`; stop and compact if tool use exceeds the forecast.

Run `python -m pytest tests/ -v` after runtime validator, domain-pack, CLI, or runner test changes.

At every phase closeout, update `STATUS.md`, `PHASE_LOG.md`, `ARTIFACTS.md`, and this `NEXT_PROMPT.md`. Include carry-forward facts and do-not-carry-forward notes. If a phase blocks, use the recovery procedure in `PLAN.md` before any next-phase work.
