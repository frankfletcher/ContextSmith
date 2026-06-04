# Plan: Runtime Framing Backfill



# Important Note

1. There are 2 PLAN.md files - make sure you know or have inferred which PLAN is being referred to at all times.  
   1. the first one is the plan we are trying to match and is located here: /home/frank/00-Code/ContextSmith/.agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/PLAN.md
   2. The second one is the plan we are currently enacting, which backfills the codebase to match the reframing of runtime orchestration as a default/first-class mechanism for the ContextSmith skills.  That plan is located here:  /home/frank/00-Code/ContextSmith/.agent_work/sprints/runtime-enforcement/tasks/2026-06-03-runtime-backfill/PLAN.md

## Phase B0: Audit Scope
**Goal:** Identify which artifacts currently frame the runtime and how they deviate from /home/frank/00-Code/ContextSmith/.agent_work/sprints/runtime-enforcement/tasks/2026-06-01-runtime-enforcement/PLAN.md's "first-class, optional but default" framing.

```yaml
context_contract:
  executor: small-model
  phase_type: audit
  usable_phase_budget: 20k-35k
  expected_tool_calls: 6-10 reads, 1 task artifact edit
  validation_output_budget: brief
  compaction_trigger: summarize findings per artifact
  stop_rule: stop if audit requires reading more than 10 files
```

**Actions:**
1. Read PLAN.md Architecture Direction and Enforcement Levels sections for the canonical framing.
2. Read each artifact in scope and check for runtime framing language.
3. Record deviations in `AUDIT_RESULTS.md`.
4. Classify each artifact as: `aligned`, `minor-fix`, `needs-update`, or `no-runtime-mentions`.

**Outputs:**
- `AUDIT_RESULTS.md` with per-artifact deviation notes.
- `STATUS.md` updated with next phase.
- `NEXT_PROMPT.md` for Phase B1.

**Validation:**
- All scoped artifacts are classified.
- Deviations are specific and actionable.

## Phase B1: README.md Backfill
**Goal:** Update README.md runtime framing to match PLAN.md.

```yaml
context_contract:
  executor: small-model
  phase_type: fix
  usable_phase_budget: 20k-35k
  expected_tool_calls: 2-3 reads, 1-2 edits, 2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize changes before validation
  stop_rule: stop if README needs more than 2 edits or becomes broader than runtime framing
```

**Actions:**
1. Read current README.md runtime section.
2. Compare against PLAN.md Architecture Direction framing.
3. Apply minimal edits to align framing.
4. Run validation commands.

**Validation:**
- `python scripts/validate_skills.py` passes.
- `python scripts/token_budget.py --strict` passes.

## Phase B2: Runtime Enforcement Doc Backfill
**Goal:** Update docs/workflows/RUNTIME_ENFORCEMENT.md to match PLAN.md framing.

```yaml
context_contract:
  executor: small-model
  phase_type: fix
  usable_phase_budget: 20k-35k
  expected_tool_calls: 2-3 reads, 1-2 edits, 2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize changes before validation
  stop_rule: stop if doc needs more than 2 edits or becomes broader than runtime framing
```

**Actions:**
1. Read current RUNTIME_ENFORCEMENT.md.
2. Compare against PLAN.md framing.
3. Apply minimal edits to align framing.
4. Run validation commands.

**Validation:**
- `python scripts/validate_skills.py` passes.
- `python scripts/token_budget.py --strict` passes.

## Phase B3: Quickstart Backfill
**Goal:** Update docs/QUICKSTART.md if it frames the runtime in a way that deviates from PLAN.md.

```yaml
context_contract:
  executor: small-model
  phase_type: fix
  usable_phase_budget: 20k-35k
  expected_tool_calls: 2-3 reads, 0-2 edits, 2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize changes before validation
  stop_rule: stop if quickstart needs more than 2 edits or becomes broader than runtime framing
```

**Actions:**
1. Read current QUICKSTART.md.
2. Check if runtime framing deviates from PLAN.md.
3. Apply minimal edits if needed.
4. Run validation commands.

**Validation:**
- `python scripts/validate_skills.py` passes.
- `python scripts/token_budget.py --strict` passes.

## Phase B4: Examples Library Backfill
**Goal:** Update docs/examples/EXAMPLES_LIBRARY.md if it frames the runtime in a way that deviates from PLAN.md.

```yaml
context_contract:
  executor: small-model
  phase_type: fix
  usable_phase_budget: 20k-35k
  expected_tool_calls: 2-3 reads, 0-2 edits, 2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize changes before validation
  stop_rule: stop if examples needs more than 2 edits or becomes broader than runtime framing
```

**Actions:**
1. Read current EXAMPLES_LIBRARY.md.
2. Check if runtime framing deviates from PLAN.md.
3. Apply minimal edits if needed.
4. Run validation commands.

**Validation:**
- `python scripts/validate_skills.py` passes.
- `python scripts/token_budget.py --strict` passes.

## Phase B5: Workflow Docs Backfill
**Goal:** Update CREATE_A_PLAN.md and BUILD_OR_IMPROVE_A_SKILL.md if they frame the runtime in a way that deviates from PLAN.md.

```yaml
context_contract:
  executor: small-model
  phase_type: fix
  usable_phase_budget: 20k-35k
  expected_tool_calls: 3-4 reads, 0-3 edits, 2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize changes before validation
  stop_rule: stop if workflow docs need more than 3 edits total or become broader than runtime framing
```

**Actions:**
1. Read both workflow docs.
2. Check if runtime framing deviates from PLAN.md.
3. Apply minimal edits if needed.
4. Run validation commands.

**Validation:**
- `python scripts/validate_skills.py` passes.
- `python scripts/token_budget.py --strict` passes.

## Phase B6: Shared References Backfill
**Goal:** Update shared/ references if they frame the runtime in a way that deviates from PLAN.md.

```yaml
context_contract:
  executor: small-model
  phase_type: fix
  usable_phase_budget: 20k-35k
  expected_tool_calls: 3-5 reads, 0-3 edits, 2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize changes before validation
  stop_rule: stop if shared refs need more than 3 edits total or become broader than runtime framing
```

**Actions:**
1. Grep shared/ for runtime-related framing.
2. Read relevant files.
3. Apply minimal edits if needed.
4. Run validation commands.

**Validation:**
- `python scripts/validate_skills.py` passes.
- `python scripts/token_budget.py --strict` passes.

## Phase B7: SKILL.md Files Backfill
**Goal:** Update SKILL.md files if they frame the runtime in a way that deviates from PLAN.md.

```yaml
context_contract:
  executor: small-model
  phase_type: fix
  usable_phase_budget: 20k-35k
  expected_tool_calls: 4-6 reads, 0-4 edits, 2 validation commands
  validation_output_budget: brief
  validation_output_reserve: at least 25 percent for validation output and one targeted correction
  compaction_trigger: summarize changes before validation
  stop_rule: stop if SKILL.md files need more than 4 edits total or become broader than runtime framing
```

**Actions:**
1. Grep skills/*/SKILL.md for runtime-related framing.
2. Read relevant sections.
3. Apply minimal edits if needed.
4. Run validation commands.

**Validation:**
- `python scripts/validate_skills.py` passes.
- `python scripts/token_budget.py --strict` passes.

## Phase B8: Final Backfill Audit
**Goal:** Verify all artifacts are aligned with PLAN.md framing.

```yaml
context_contract:
  executor: small-model
  phase_type: validation
  usable_phase_budget: 20k-35k
  expected_tool_calls: 4-6 reads, 2 validation commands
  validation_output_budget: brief
  compaction_trigger: summarize alignment status
  stop_rule: stop if audit finds new deviations
```

**Actions:**
1. Re-read PLAN.md Architecture Direction and Enforcement Levels.
2. Spot-check each artifact that was updated.
3. Confirm framing is consistent.
4. Record final alignment status.

**Validation:**
- `python scripts/validate_skills.py` passes.
- `python scripts/token_budget.py --strict` passes.
- All artifacts are classified as `aligned` or `no-runtime-mentions`.

## Plan Completion Criteria
- All scoped artifacts are audited.
- Deviations are fixed with minimal edits.
- Validation passes after each phase.
- Final audit confirms alignment.
