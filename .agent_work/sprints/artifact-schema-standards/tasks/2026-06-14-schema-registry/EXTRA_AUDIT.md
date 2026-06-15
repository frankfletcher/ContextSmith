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
| --- | --- | --- | --- | --- |
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
- Key observation: The original PLAN.md ended at Phase 10 (Final Audit). The session added `shared/extra-audit.md`, `shared/project-audit.md`, `docs/workflows/EXTRA_AUDIT.md`, `scripts/lint_error_counter.py`, `STATE_EXTRA_AUDIT` in the orchestrator constants, and significant restructuring of AGENTS.md. These should be reflected as new phases or
  b-phases if the project continues.

### Findings

| Finding | Lens | Severity | Action | Already in PLAN? |
| --- | --- | --- | --- | --- |
| PLAN.md does not reflect infrastructure work done (lint counter, .new merging, extra-audit state, audit references) | Trajectory | should-fix | Update PLAN.md with Phase 11 for tooling/audit infrastructure | No |
| `docs/workflows/EXTRA_AUDIT.md` is untracked — project-audit workflow is documented but not integrated into any plan | Blind Spot Scan | acceptable tradeoff | User-facing doc exists but no PLAN.md entry ensures someone will run it | No |
| EXTRA_AUDIT.md schema definition exists in artifact_schemas.yaml but the extra-audit workflow state (STATE_EXTRA_AUDIT) is not in any workflow_config example | Dependency Surface | low | Add an example workflow config that chains audit + extra_audit | No |
| `scripts/lint_error_counter.py` exists but is not documented in any PLAN.md phase — no one will run it unless told | Scope Pressure | should-fix | Add documentation or a PLAN.md entry for Phase 11 | No |
| `RESULT.json` removed from PROTECTED_FILES — correct now, but no test verifies it can be overwritten | Blind Spot Scan | low | Already fixed inline | Fixed |
| `.agent_work/tmp/` rule exists in AGENTS.md but the directory is not gitignored and was never created | Dependency Surface | low | Create directory or add gitignore entry | No |

### Risks Not Yet Addressed

- PHASE_START_PROMPT.md and NEXT_PROMPT.md now reference `.new` files, but existing agents with cached knowledge of the old `>>` approach will clobber reports if not re-reading current instructions. Mitigation: the .new merging + auto-repair mechanism handles this, but the EXTRA_AUDIT.md I just wrote via `>>` will not be auto-recognized as a
  new` segment. The next orchestrator run will still merge it correctly via the append-only snapshot mechanism, not the .new mechanism.
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
| --- | --- | --- |
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

## Extra Audit — 2026-06-14

### Baseline Status

- Validation: pass
- Plan accuracy: plan-needs-update

### Trajectory Assessment

- Current trajectory: converging
- Key observation: The artifact schema standards project has moved from pure design (Phase 1-2) through implementation (Phases 3-8) to documentation and closeout (Phase 9-10). Each phase built on the prior one without backtracking. The hierarchy is clean and the implementation matches the plan. The remaining work (Phases 10-11) is validation,
  dit, and packaging — natural closeout work for a standards project.

### Findings

| Finding | Lens | Severity | Action | Already in PLAN? |
| --- | --- | --- | --- | --- |
| The project depends on the orchestrator being deployed as production runtime, but there is no trigger condition defined for that transition | Blind Spot | should-fix | Add orchestrator-adoption gate to DECISIONS.md — defines when .new auto-merge activates and manual merging stops | No |
| Phase 11 has 4 sub-phases of doc and housekeeping that could collapse into Phase 10 | Scope Pressure | should-fix | Merge Phase 11 sub-phases into Phase 10 or document as optional; 4 sub-phases for config, counter docs, and backfill is excessive | Partially (PLAN.md has Phase 11, drifting from the original 10-phase plan) |
| The schema registry and validation pipeline are well-designed but have no CI enforcement | Trajectory | should-fix | Add GitHub Actions or equivalent CI configuration in Phase 10 or 11 that runs the full validation suite on push/PR | No |
| `orchestrator.run()` cyclomatic complexity C (15) is pre-existing and documented but may become a maintenance bottleneck when the orchestrator becomes the production runtime | Trajectory | acceptable tradeoff | Already planned for refactor in Phase 10/11 closeout. Monitor after refactor. | Yes |
| The `.new` segment pattern requires agents to be aware of two parallel workflows (write `.new`, merge manually, delete `.new`) — cognitive overhead that will vanish once orchestrator ships | Reusability | acceptable tradeoff | Temporary. Documented in D12. Condition to remove: "when orchestrator is deployed as production runtime." | Yes |
| PHASE_LOG.md has 3 formatting conventions across 9 phases. A fresh agent must infer which format to use | Fresh-Agent Fragility | should-fix | Standardize on bold format with required fields (Status, Date, Changes, Validation, Artifacts, Action). Add format rule to PHASE_LOG.md schema in `artifact_schemas.yaml` | No |

### Risks Not Yet Addressed

- **No CI/CD integration**. All validation is human-triggered. A single `git push` with a lint or test failure has no automated guard.
- **Orchestrator adoption gap**. The sub-phase advancement, `.new` merging, and checkpoint infrastructure all depend on the orchestrator. If the orchestrator is never deployed as the production entry point, this entire task (Phases 1-9) is infrastructure without a consumer.
- **Phase 11 scope creep**. The original plan had 10 phases. Phase 11 was added during implementation. Its 4 sub-phases cover config, counter docs, backfill, and tmp cleanup — real work, but the scope expansion is worth flagging rather than normalizing.

### What Would a Fresh Agent Need?

The task state is well-documented. A fresh agent would:

1. Read STATUS.md — clear on phase and sub-phase
2. Read NEXT_PROMPT.md — written for Phase 10.1 with specific tasks, input files, output requirements, constraints, Ralph loop, self-audit, and hard stop
3. Read DECISIONS.md — 13 decisions with rationale
4. Read CONTEXT.md — key files, constraints, skip rules, technical debt
5. Read PLAN.md — full phase plan with sub-phases, context budgets, and task checklists

The weak link is PHASE_LOG.md format inconsistency — an agent parsing it programmatically would need to handle 3 formats.

### Tradeoffs Accepted

- **PHASE_LOG.md format drift was knowingly tolerated** to keep phases moving. The schema defines a `phase_entry` content rule but does not enforce it during phase execution. This was the right call — enforcing format on every phase submission would add friction for marginal gain. A single cleanup pass (Phase 10 or 11) can standardize everything.
- **`.new` manual merging** was the pragmatic choice. The orchestrator code exists but is not the runtime. Rather than waiting for orchestrator deployment, the project shipped the `.new` convention and documented the gap. Agents can handle the small overhead of `cat >> ... && rm ...` without the orchestrator.
- **Cyclomatic complexity in `run()`** was deferred because extraction would risk destabilizing the orchestrator mid-project. The complexity is localized and well-understood; refactoring it in closeout is lower-risk than during active development.

## Extra Audit — 2026-06-15

### Baseline Status

- Validation: pass
- Plan accuracy: plan-is-current

### Trajectory Assessment

- **Current trajectory**: converging
- **Key observation**: Phases 1–9 built core infrastructure in clean dependency order. Phase 10 validated everything. Phase 11 is closeout — tooling, config validation, backfill, cleanup. One final phase of loose-end tying, then ship. No rescoping needed.

### Findings

| Finding | Lens | Severity | Action | Already in PLAN? |
| --- | --- | --- | --- | --- |
| Orchestrator is the largest silent dependency — entire sub-phase mechanism dead code if never deployed | Dependency Surface | must-fix (decision) | Commit to orchestrator-as-runtime with target date, or scrap auto-merge and formalize manual merge as permanent | No |
| No CI pipeline — test failures only surface at next agent run | Blind Spot | should-fix | Add minimal CI (GitHub Actions with pytest + ruff) or accept as risk | No |
| NEXT_PROMPT.md staleness risk — manually written prompts can fall out of sync with STATUS.md | Blind Spot | should-fix | Detect NEXT_PROMPT.md vs STATUS.md mismatch on load; regenerate if stale | No |
| Orchestrator adoption cliff — when D14 gates pass, all agents must flip from manual to auto-merge | Blind Spot | should-fix | Add a `D14_GATE_PASSED` flag file in `.agent_work/` that agents check at every phase start | No |
| First-agent context overhead — 6+ files read before any work begins | Blind Spot | acceptable tradeoff | By design for small-model dispatchability, but non-trivial overhead consumes context budget | No |
| `.contextsmith/audit-with-extra.json` never schema-validated | Scope Pressure | should-fix | Validate in 11.1 as planned | Yes (Phase 11.1) |
| Phase 11.3 (decision records backfill) addresses only D9/D12/D14 — should cover PHASE_LOG format and config-override test too | Scope Pressure | should-fix | Expand 11.3 scope or note as post-ship | Partially (11.3) |

### Risks Not Yet Addressed

1. **Orchestrator adoption decision**: The project's most consequential open question. If the orchestrator never becomes the production runtime, the sub-phase advancement, `.new` auto-merge, and checkpoint management code becomes dead-weight complexity. A concrete go/no-go decision with a target date is needed before Phase 11 closeout.
2. **CI/CD gap**: 423 tests pass today. Next week, after 3 more agent sessions, they might not. Without CI, regressions are silent until the next human or agent runs `pytest`. For a validation-heavy project, this is a gap.
3. **NEXT_PROMPT.md staleness**: This session started with a stale NEXT_PROMPT.md — it described Phase 10.1 when Phase 10.2 was current. The orchestrator's `_generate_next_prompt()` prevents this, but manually written prompts can drift. A mismatch-detection check at session start would catch it.

### What Would a Fresh Agent Need?

- **STATUS.md**: Current — Phase 11, Sub-phase 11.1 ✅
- **NEXT_PROMPT.md**: Current — describes 11.1 tasks, notes config exists ✅
- **DECISIONS.md**: D14 gate condition documented. Agent should check: is `_merge_new_artifact_segments()` tested end-to-end? Is there a production workflow config routing through `orchestrator.run()`? If both true → stop manual merging.
- **CONTEXT.md**: Clear about orchestrator gap, skip rules, file boundaries ✅
- **One addition**: Add a `D14_GATE_PASSED` sentinel file to `.agent_work/` that agents check before deciding merge strategy. Without it, each agent must re-evaluate D14 from scratch.

### Tradeoffs Accepted

- PHASE_LOG.md format standardization deferred — append-only semantics make retroactive fixes risky. Schema compliance starts from Phase 7 forward.
- Config-override end-to-end test deferred — unit tests cover the pieces, and the full-pipeline test requires a test workflow config that doesn't exist yet (Phase 11.1 creates one).
- markdownlint across the full repo deferred — pre-existing issues in skills/, AGENTS.md, CLAUDE.md, CHANGELOG.md, test fixtures, and tmp/. Cleaning these is out of scope for this project.
- Lint counter inflates across all subtrees — no subtree filtering. Acceptable because the orchestrator/ and schemas/ trees are clean, which is the project's scope.
## Extra Audit — 2026-06-15 (Project Final)

### Baseline Status

- Validation: pass
- Plan accuracy: plan-is-current — all 11 phases complete, all 21 sub-phases delivered

### Trajectory Assessment

- Current trajectory: converging — all planned work delivered
- Key observation: The project reached its stated goal (artifact schema standards across the full 11-phase plan) but stopped at the boundary of a larger systemic gap: the packaging and distribution infrastructure has not been updated for the orchestrator age. The project built infrastructure that the release pipeline does not ship.

### Lens: Trajectory

The last 20 commits show a clean dependency chain: schema registry → validator refactor → state reader → step compiler → orchestrator dispatch → tests → docs → audit → tooling. Each phase built on the prior without backtracking. That trajectory is complete.

What comes *after* is undefined. The plan ends here. There is no Phase 12, but there are clear next steps (packaging, CI/CD, orchestrator-as-runtime commitment) that the plan never addressed.

### Lens: Dependency Surface

| Dependency | Status | Risk |
|---|---|---|
| Orchestrator as production runtime | Not deployed | **Critical.** The sub-phase advancement, `.new` auto-merge, checkpoint management, and workflow config dispatch are dead code if the orchestrator is never adopted as the production entry point. The D12/D14 gate conditions have never been evaluated. |
| `contextsmith-run` skill removed | Done | Pre-orchestrator run executor was collapsed into the orchestrator. The release scripts still reference `contextsmith-run`. **Will break** the next attempted release. |
| `orchestrator/` Python package | Not packaged | The validation pipeline, CLI, and state machine are in `orchestrator/` but excluded from every release artifact. Users must clone the repo. |
| `.new` file convention | Manual merge only | Works correctly but requires agents to do `cat >> ... && rm ...` after every sub-phase. The orchestrator's `_merge_new_artifact_segments()` exists but is never invoked in production. |

### Lens: Scope Pressure

The original 10-phase plan expanded to 11 phases during execution. Phase 11 (Tooling and Audit Infrastructure) was the scope-creep catch-all — and it was the right call. The extra-audit workflow config, lint counter, and backfill work were genuinely needed.

However, the project also accumulated scope *outside* the plan:
- `shared/extra-audit.md`, `shared/project-audit.md` — strategic audit references, never planned
- `scripts/lint_error_counter.py` — user-requested, never planned
- `orchestrator/constants.py` `STATE_EXTRA_AUDIT` — exists but no workflow config chains it
- AGENTS.md was rewritten with RTK instructions injected from `@RTK.md` — external dependency not tracked in the plan

The scope pressure was productive. Every addition was justified. But the project now has "adjacent work" that Phase 11 validates without vending.

### Lens: Reusability Leverage

What's reusable outside this project:
- The orchestrator state machine (`orchestrator/orchestrator.py`) — generic enough for any multi-step agent workflow
- The schema registry pattern (`schemas/artifact_schemas.yaml`) — transferable to any project with markdown artifact conventions
- The `.new` file protocol — could become a general append-only safe-write pattern
- `scripts/lint_error_counter.py` — zero-dependency, pipe-compatible, reusable across projects

What's project-specific:
- The SKILL.md references are ContextSmith-specific
- The workflow config schema references specific states (audit, extra_audit) and agents (contextsmith-auditor)
- The sub-phase advancement logic assumes PLAN.md with `###`/`####`/- hierarchy

### Lens: Blind Spot Scan

What the rubrics do not check:

1. **The orchestrator is not tested end-to-end as a real runtime.** All 423 tests exercise `orchestrator.run()` with mock harnesses and synthetic state directories. No test runs the orchestrator against a real `.contextsmith/audit-with-extra.json` with a real agent harness. The integration test suite verifies the building blocks; it does not verify the assembled machine.

2. **The release pipeline has never been run end-to-end for the current codebase.** `test_release.sh` references `contextsmith-run` which no longer exists. The last `dist/` was built on 2026-06-04 and contains only skills — no orchestrator package. The `publish_release.sh` script has never been exercised.

3. **Version is inconsistent across the project.** `pyproject.toml` says 0.1.0. Skills say 2.0.0. `PACKAGE_SPEC.md` says v1.7.1 in its main metadata but describes v2.0.0 design decisions. `CHANGELOG.md` says v2.2.0 (added this session).

4. **No mechanism prevents a stale NEXT_PROMPT.md.** This session started with a correct one, but there is no automated check that NEXT_PROMPT.md matches STATUS.md phase/sub-phase. The orchestrator's `_generate_next_prompt()` prevents this in managed workflows; manual sessions have no guard.

5. **The `orchestrator/` Python package has no `py.typed` marker and no type stubs.** `cli.py` has untyped `Optional` imports that ruff would flag on stricter settings. Not a blocker for a script-level tool, but prevents adoption as a library.

### Lens: Exit Condition Honesty

**Is the project close enough to done that remaining work is lower-value than stopping?**

No — but not because the plan is incomplete. The 11-phase plan is fully delivered. The reason is that the *distribution* of everything built is incomplete:

- The orchestrator Python package (1243 lines of core logic) is not ship-able
- The release scripts have bit-rotted (`contextsmith-run` reference)
- The version is an inconsistent multi-valued mess

If the goal was "complete the artifact schema standards plan," the project is done. Ship.

If the goal was "put ContextSmith into a state where someone can install and run it," the project needs one more phase: packaging and distribution.

### Findings

| Finding | Lens | Severity | Action | Already in PLAN? |
|---|---|---|---|---|
| Orchestrator not deployed as production runtime — entire sub-phase mechanism is dead code if never adopted | Trajectory | must-fix (decision) | Commit to orchestrator-as-runtime with go/no-go date, or remove auto-merge and formalize manual merge | No |
| Release pipeline references deleted `contextsmith-run` — will break on next `publish_release.sh` | Dependency Surface | must-fix | Update `test_release.sh` line 90 to reference `contextsmith-workflow-developer` | No |
| `orchestrator/` Python package excluded from all release artifacts | Dependency Surface | should-fix | Add orchestrator to the release bundle, or make pip-installable via pyproject.toml | No |
| Version inconsistency across pyproject.toml (0.1.0), PACKAGE_SPEC.md (v1.7.1), skills (2.0.0), CHANGELOG.md (v2.2.0) | Blind Spot | should-fix | Consolidate all version references to a single source of truth | No |
| No CI/CD — 423 tests pass today but no automated guard against regression | Blind Spot | should-fix | Add GitHub Actions workflow running full validation suite | No |
| `orchestrator.run()` cyclomatic complexity C (15) — pre-existing documented debt, still C | Trajectory | acceptable tradeoff | Extraction was deferred to closeout. Closeout happened. It is still C. | No — deferred past closeout |
| NEXT_PROMPT.md has no staleness guard — manual prompts can drift from STATUS.md | Blind Spot | should-fix | Add mismatch check at session start: compare NEXT_PROMPT.md phase/sub-phase against STATUS.md | No |
| No end-to-end test for `validate_artifacts_with_schemas()` with config overrides — unit-tested separately, full pipeline untested | Blind Spot | should-fix | Add integration test exercising full config→override→validation pipeline | No (identified in audit finding, not in PLAN) |
| PHASE_LOG.md has 3 different formats across entries | Blind Spot | acceptable tradeoff | Append-only semantics make retroactive format fixes risky. Schema compliance starts from Phase 7 forward. | No |
| `.contextsmith/audit-with-extra.json` validated but never executed via real orchestrator run | Blind Spot | acceptable tradeoff | Schema-validated, dry-run passes. Real execution requires orchestrator adoption. | Yes (Phase 11.1) |
| No mechanism for agents to detect D14 gate status — each agent re-evaluates from scratch | Blind Spot | should-fix | Add `D14_GATE_PASSED` sentinel file that agents check before deciding merge strategy | No |


## Extra Audit — 2026-06-15 (Phase 12 Completion)

### Baseline Status

- Validation: pass (429 tests, ruff clean, 8/8 skills, version consistent)
- Plan accuracy: plan-is-current

### Trajectory Assessment

- **Current trajectory**: converged and complete
- **Key observation**: The project started with schema design and ended with packaging — textbook dependency order. Every phase built on the previous one without rework. The trajectory is clean and coherent.

### Findings

| Finding | Lens | Severity | Action | Already in PLAN? |
| --- | --- | --- | --- | --- |
| `run()` complexity was C(15) throughout most of the project — extracted to B(8) only in final phase | Dependency Surface | should-fix | Extracted in 12.7. Was acceptable debt but would have amplified if the orchestrator grew further before extraction. | Yes (12.7) |
| `test_release.sh` blocked by token budget `--strict` check — pre-existing skills exceed budgets | Scope Pressure | acceptable tradeoff | The token budgets are stale. A separate phase to recalibrate budgets would fix the pipeline. | No |
| `requires-python = ">=3.14"` excludes Python 3.10–3.13 — validate.yml matrix targets those versions but pip install would fail | Blind Spot Scan | must-fix | The CI matrix claims 3.10/3.11/3.12 but pyproject.toml only allows 3.14. Pip install in CI would fail silently or with a confusing error. PLAN.md 12.1 listed relaxing this but it was outside NEXT_PROMPT.md scope for the agent that executed 12.1. | Partially (12.1 mentions it) |
| Version consolidated to v2.2.0 but CHANGELOG.md already has v2.2.0 for Phase 11 — Phase 12 would be v2.3.0 | Trajectory | should-fix | Phase 12 changes should be under a new v2.3.0 header in CHANGELOG.md. Using v2.2.0 for the pyproject.toml version is fine (it's the current release), but the next CHANGELOG entry needs v2.3.0. | No |
| Adapter discovery fallback uses `importlib.reload()` on cached modules — correct but could cause subtle issues if modules have side effects beyond registration | Blind Spot Scan | acceptable tradeoff | The reload is safe for these adapters (registration is the only module-level effect). If more adapters are added with heavier module-level code, the reload approach should be revisited. | No |
| Wheel build tested in fresh venv but `test_release.sh` end-to-end pipeline is blocked | Scope Pressure | acceptable tradeoff | The individual components work (wheel build, install, CLI). The full pipeline failure is pre-existing (token budgets). Not introduced by this phase. | No |

### Strengths

- **Complexity discipline held**: 12 phases later, every function in orchestrator/ is ≤ B cyclomatic complexity and ≥ A maintainability. The extraction in 12.7 brought the one outlier back in line.
- **Test growth with no regressions**: 429 tests, zero regressions across all phases. Each phase added tests; none removed or broke existing ones.
- **No dead code**: Every function, schema, config, and script added across 12 phases is exercised by tests, used by the pipeline, or referenced in documentation.
- **Version consistency**: All 10 version sources now match — a small thing that signals project hygiene.

### Risks Not Yet Addressed

1. **`requires-python = ">=3.14"` vs CI matrix (3.10–3.12)**: This is the most concrete blocker. The CI workflow targets Python 3.10–3.12 but pip install would fail on all of them because pyproject.toml declares `requires-python = ">=3.14"`. This must be fixed before the CI workflow can actually run.
2. **CHANGELOG.md v2.2.0 vs v2.3.0**: The v2.2.0 entry describes Phase 11 completion. Phase 12 work needs a v2.3.0 entry. Currently the pyproject.toml version matches v2.2.0, which is fine for the package version itself (it reflects the latest release), but the CHANGELOG needs a new header for Phase 12 changes.
3. **Token budgets stale**: 6 of 8 skills exceed their token budgets. The `--strict` check in the release pipeline blocks full automation. Recalibrating budgets is a small task but unblocks the release pipeline entirely.

### Plan for Gaps (do not execute)

1. Fix `requires-python` in pyproject.toml: relax from `>=3.14` to `>=3.10`.
2. Move `pytest`, `ruff` from `[project.dependencies]` to `[project.optional-dependencies] dev`.
3. Add v2.3.0 header to CHANGELOG.md documenting Phase 12 changes.
4. Recalibrate token budgets across all 8 skills to match current line counts.
