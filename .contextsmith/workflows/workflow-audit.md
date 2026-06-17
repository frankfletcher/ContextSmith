# Workflow Audit: .contextsmith/workflow.yaml

**Audit Date:** 2026-06-17
**Auditor:** contextsmith-auditor (automated validation)

---

## Check 1: Required fields (id, agent, task, expected_artifacts)

**Result: FAIL**

Every phase is missing the `task` field. Every phase uses `expected_outputs` instead of `expected_artifacts`.

| Phase | Line | id | agent | task | expected_artifacts |
|-------|------|----|-------|------|-------------------|
| load_context | 24 | ✅ (state key) | ✅ | ❌ MISSING | ❌ uses `expected_outputs` |
| add_dependencies | 41 | ✅ (state key) | ✅ | ❌ MISSING | ❌ uses `expected_outputs` |
| implement_script | 61 | ✅ (state key) | ✅ | ❌ MISSING | ❌ uses `expected_outputs` |
| implement_tests | 81 | ✅ (state key) | ✅ | ❌ MISSING | ❌ uses `expected_outputs` |
| audit_output | 101 | ✅ (state key) | ✅ | ❌ MISSING | ❌ uses `expected_outputs` |
| validate | 120 | ✅ (state key) | ✅ | ❌ MISSING | ❌ uses `expected_outputs` |
| close | 138 | ✅ (state key) | ✅ | ❌ MISSING | ❌ uses `expected_outputs` |

**Evidence:**
- Line 24-39: `load_context` state has no `task` field.
- Line 41-59: `add_dependencies` state has no `task` field.
- Line 61-79: `implement_script` state has no `task` field.
- Line 81-99: `implement_tests` state has no `task` field.
- Line 101-118: `audit_output` state has no `task` field.
- Line 120-136: `validate` state has no `task` field.
- Line 138-154: `close` state has no `task` field.
- All states: field is `expected_outputs` (lines 54, 74, 94, 114, 133, 149) instead of `expected_artifacts`.

---

## Check 2: Task achievable by single narrow-focus agent

**Result: INCONCLUSIVE (cannot verify)**

Since every phase lacks a `task` field (Check 1), there is no task description to evaluate for scope or single-agent feasibility.

Inference from phase names:
- `load_context` — reasonable single-agent read-only scope ✅
- `add_dependencies` — reasonable single-agent (add dep to pyproject.toml) ✅
- `implement_script` — reasonable single-agent (write healthcheck.py) ✅
- `implement_tests` — reasonable single-agent (write test_healthcheck.py) ✅
- `audit_output` — reasonable single-agent read-only audit ✅
- `validate` — reasonable single-agent validation ✅
- `close` — reasonable single-agent closeout ✅

No evidence of multi-phase tasks or handoffs embedded in a single description because no descriptions exist. **Add `task` fields, then re-evaluate.**

---

## Check 3: No cross-phase artifact instructions

**Result: PASS**

The file has no `task` fields, so there is nowhere for cross-phase artifact instructions to appear.

The `inputs` lists are orchestrator-level staging references (e.g., `audit_output` inputs `ARTIFACTS.md` at line 117, `validate` inputs `ARTIFACTS.md` at line 135). These are structural dependencies for the orchestrator to stage, not agent-level instructions saying "read X from phase Y." This is proper behavior.

**Caution:** When `task` fields are added, ensure they do NOT say things like "read ARTIFACTS.md from implement_script and then..." — the orchestrator handles sequencing and artifact staging.

---

## Overall Verdict

| Check | Result |
|-------|--------|
| 1. Required fields (id, agent, task, expected_artifacts) | **FAIL** |
| 2. Single-agent task scope | **INCONCLUSIVE** (blocked by Check 1 failure) |
| 3. No cross-phase artifact instructions | **PASS** |
| **Overall** | **FAIL** |

---

## Recommendations

1. **Add `task` fields to every phase.** Reference `.contextsmith/workflows/generate.yaml` for the pattern (lines 12-16, 27-30, 39-45). Each task should describe what the agent should do in concrete terms. Example for `load_context`:
   ```yaml
   task: >
     Read requirements from .contextsmith/workflows/requirements.md.
     Load STATUS.md, PLAN.md, and CONTEXT.md. Produce NEXT_PROMPT.md
     with the first actionable phase step.
   ```

2. **Rename `expected_outputs` to `expected_artifacts`** to match the convention used in `.contextsmith/workflows/generate.yaml` (line 18).

3. **After adding tasks, re-run Check 2** to verify each task is scoped to a single narrow-focus agent with no embedded handoffs.

4. **After adding tasks, re-run Check 3** to verify no task says "read X from phase Y" — the orchestrator handles sequencing via `inputs`.
