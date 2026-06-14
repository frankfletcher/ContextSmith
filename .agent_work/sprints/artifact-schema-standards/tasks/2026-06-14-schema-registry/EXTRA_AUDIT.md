# EXTRA_AUDIT.md

## Extra Audit — 2026-06-14

### Baseline Status
- Validation: pass
- Plan accuracy: plan-needs-update — session scope expanded beyond Phase 7

### Trajectory Assessment
- Current trajectory: converging with scope pressure
- Key observation: The `.new` file merging and lint error counter are new infrastructure that was not in the original PLAN.md. Both are high-leverage additions that reduce agent-side risk, but they shift the project toward tooling work that Phase 8-10 did not account for.

### Findings

| Finding | Lens | Severity | Action | Already in PLAN? |
|---|---|---|---|---|
| RESULT.json was in PROTECTED_FILES, causing `_safe_write` to force append mode. Agent never uses `_safe_write` so it was harmless, but misleading — removed. | Blind Spot Scan | Low | Removed from PROTECTED_FILES | No — fixed inline |
| PHASE_START_PROMPT.md step 5 still said "Append... using >>" instead of PHASE_LOG.md.new | Blind Spot Scan | Medium | Updated to "Write PHASE_LOG.md.new" | No — fixed inline |
| `scripts/lint_error_counter.py` added as new infrastructure not in PLAN.md | Scope Pressure | Low | Justified — user-requested, enables data-driven standards updates | No — defer documentation |
| Per-skill coding-standards.md copies diverge from shared source | Dependency Surface | Low | Already synced in this session | No — already synced |
| Lint counter file location (.agent_work/) is not explicitly gitignored | Dependency Surface | Low | Not blocking — file is transient build data | No — add to .gitignore if committed |

### Risks Not Yet Addressed
- `.new` file merging is only tested via unit tests, not end-to-end integration with the actual agent harness. Phase 8 should cover this.
- `RESULT.json` removal from PROTECTED_FILES means no protection if someone calls `_safe_write(path, content, "w")` with a RESULT.json path. Low risk since `_safe_write` is only used internally by orchestrator.py for STATUS.md and PHASE_LOG.md.
- Lint counter will accumulate test injection data. Users must know to delete `.agent_work/lint_error_counts.json` to reset.

### What Would a Fresh Agent Need?
- NEXT_PROMPT.md for Phase 8.1 exists and specifies sub-phase advancement tests. It uses the `.new` file convention and references the lint error counter.
- The agent should read PHASE_START_PROMPT.md for the full sub-phase workflow (`.new` files, validation pipeline, counters).

### Tradeoffs Accepted
- `RESULT.json` removed from PROTECTED_FILES: the protection was misleading dead code. Removing it makes the intent clear even though no actual behavior changes.
- Lint counter script location in `.agent_work/` rather than project root: follows the existing convention for transient task artifacts. Not explicitly gitignored but unlikely to be committed.
- `.new` file merging does not cover `PHASE_START_PROMPT.md` or `CONTEXT.md` — these are not append-only. They should be overwritten each time. Correct behavior.

## Extra Audit — 2026-06-14 (Project-Level)

### Baseline Status
- Validation: pass (408 tests, ruff clean, 8 skills validate)
- Plan accuracy: plan-needs-update — session added infrastructure not in PLAN.md

### Trajectory Assessment
- Current trajectory: needs-course-correction — the artifact schema standards task has expanded beyond its original 10-phase plan into tooling infrastructure (lint counter, .new file merging, extra-audit state, shared audit references). The project is converging on a more reliable system, but the PLAN.md no longer reflects actual scope.
- Key observation: The original PLAN.md ended at Phase 10 (Final Audit). The session added `shared/extra-audit.md`, `shared/project-audit.md`, `docs/workflows/EXTRA_AUDIT.md`, `scripts/lint_error_counter.py`, `STATE_EXTRA_AUDIT` in the orchestrator constants, and significant restructuring of AGENTS.md. These should be reflected as new phases or sub-phases if the project continues.

### Findings

| Finding | Lens | Severity | Action | Already in PLAN? |
|---|---|---|---|---|
| PLAN.md does not reflect infrastructure work done (lint counter, .new merging, extra-audit state, audit references) | Trajectory | should-fix | Update PLAN.md with Phase 11 for tooling/audit infrastructure | No |
| `docs/workflows/EXTRA_AUDIT.md` is untracked — project-audit workflow is documented but not integrated into any plan | Blind Spot Scan | acceptable tradeoff | User-facing doc exists but no PLAN.md entry ensures someone will run it | No |
| EXTRA_AUDIT.md schema definition exists in artifact_schemas.yaml but the extra-audit workflow state (STATE_EXTRA_AUDIT) is not in any workflow_config example | Dependency Surface | low | Add an example workflow config that chains audit + extra_audit | No |
| `scripts/lint_error_counter.py` exists but is not documented in any PLAN.md phase — no one will run it unless told | Scope Pressure | should-fix | Add documentation or a PLAN.md entry for Phase 11 | No |
| `RESULT.json` removed from PROTECTED_FILES — correct now, but no test verifies it can be overwritten | Blind Spot Scan | low | Already fixed inline | Fixed |
| `.agent_work/tmp/` rule exists in AGENTS.md but the directory is not gitignored and was never created | Dependency Surface | low | Create directory or add gitignore entry | No |

### Risks Not Yet Addressed
- PHASE_START_PROMPT.md and NEXT_PROMPT.md now reference `.new` files, but existing agents with cached knowledge of the old `>>` approach will clobber reports if not re-reading current instructions. Mitigation: the .new merging + auto-repair mechanism handles this, but the EXTRA_AUDIT.md I just wrote via `>>` will not be auto-recognized as a `.new` segment. The next orchestrator run will still merge it correctly via the append-only snapshot mechanism, not the .new mechanism.
- The extra-audit state (STATE_EXTRA_AUDIT) was added to constants.py but no workflow config file actually chains it after the baseline audit. The example in docs/workflows/EXTRA_AUDIT.md shows how, but no actual config exists.
- The lint counter accumulates test injection data. There's no reset mechanism beyond manual deletion.

### What Would a Fresh Agent Need?
- NEXT_PROMPT.md for Phase 8.1 exists and is current. It uses `.new` file convention.
- PHASE_START_PROMPT.md has been updated with `.new` file instructions and lint counter integration.
- DECISIONS.md does not capture the `.new` file merging decision or the lint counter addition — a fresh agent would not know why these exist.
- The agent should read: NEXT_PROMPT.md → PHASE_START_PROMPT.md → CONTEXT.md. The new scripts/ and shared/ references are not in CONTEXT.md's Key Files section.

### Tradeoffs Accepted
- `.new` file merging and lint counter were built as additive infrastructure on top of existing PLAN.md phases, not as their own phase. This avoids restructuring the plan mid-task but creates a documentation gap.
- EXTRA_AUDIT.md schema added to artifact_schemas.yaml even though no orchestrator workflow config chains the extra_audit state yet. Forward-looking — the schema definition is the prerequisite, the workflow config is the follow-up.
- Lint counter lives in scripts/ following the existing convention. No test coverage for the counter script — acceptable for a utility script that is not part of the orchestrator core.

## Extra Audit — 2026-06-14 (Post-Fix Verification)

### Baseline Status
- Validation: pass (408 tests, ruff clean, 8 skills validate)
- Plan accuracy: plan-is-current (Phase 11 added, STATUS.md count updated)

### Findings Resolved

| Finding (from previous audit) | Fix | Status |
|---|---|---|
| PLAN.md does not reflect infrastructure work | Phase 11 added with 4 sub-phases | FIXED |
| No workflow config chains extra_audit state | .contextsmith/audit-with-extra.json created, validates against schema | FIXED |
| scripts/lint_error_counter.py undocumented | Phase 10.2 and 11.2 tasks reference it; AGENTS.md validation commands now pipe through it | FIXED |
| DECISIONS.md does not capture .new merging, lint counter, PROTECTED_FILES cleanup | D8, D9, D10, D11 appended | FIXED |
| CONTEXT.md Key Files outdated | scripts/, shared/, .contextsmith/ refs added | FIXED |
| .agent_work/tmp/ referenced but not created/gitignored | Directory created, .gitignore entry added | FIXED |
| RESULT.json in PROTECTED_FILES | Removed in earlier session; verified no regression | FIXED |

### Residual Risk
- Lint counter `.agent_work/lint_error_counts.json` is not gitignored. If accidentally committed, it carries test-injection data. Mitigation: add to .gitignore on first commit of that file, or delete before committing.
- The audit-with-extra workflow config has never been executed by a real orchestrator run — only schema-validated. Phase 11.1 should test it with a dry run.
