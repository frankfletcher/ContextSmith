# Decisions

## 2026-06-13: Phase 5.5 Post-Completion Review

### Cross-reference improvements with future phases

During Phase 5.5 completion review, the following improvements were identified and mapped to future phases:

| Finding | Classification | Action |
|---------|---------------|--------|
| `shared/harness-opencode.md` + all skill copies reference `@contextsmith-runner` agent | Already partially covered by Phase 6e step 5 | Enriched Phase 6e step 5 with explicit file list |
| `shared/run-configuration-preview.md:158` references contextsmith-run | Already covered by Phase 6e grep step 7b | No enrichment needed — grep catches it |
| `shared/structured-questioning.md:116` references contextsmith-run | Already covered by Phase 6e grep step 7b | No enrichment needed — grep catches it |
| `AGENTS.md:16` has contextsmith-run in repo map | Already covered by Phase 6e grep step 7d | Enriched Phase 6e step 5 with explicit mention |
| Missing unit tests for state_reader, checkpoint, step_compiler | Already planned in Phase 7a | No action needed — Phase 7a creates them |
| jsonschema deprecation warning (draft-07 metaschema) | Pre-existing, non-blocking | Resolution deferred — not affecting correctness |
| markdownlint MD013 line length in NEXT_PROMPT.md | Fixed during review | Wrapped long line at 350 chars |
| markdownlint MD032 blank lines in AUDIT_REPORT.md | Fixed during review | Added blank line before list |

### Ralph loop flat structure

Simplified the Ralph Loop Configuration from #1/#2/#3 role-distinct iterations to a single flat per-iteration structure (critique, strategic review, cross-reference, fix, record). Applied to both PLAN.md Ralph Loop Configuration and shared/ralph-loop.md (synced to all 7 skill copies).

Reason: Each iteration does the same thing — identify improvements and fix them. Explicit roles for specific iteration numbers added unnecessary cognitive overhead.

### Cross-reference pattern in shared/ralph-loop.md

Added Strategic Review with Cross-Reference section to the canonical Ralph loop reference. This ensures all skills that use Ralph iterations check future plans before acting on improvement ideas.

Reason: Prevents scope creep in the current phase while evolving the plan with discovered requirements.

## 2026-06-13: Phase 6 — Collapse + Determinism Hardening

### contextsmith-run deletion
Deleted skills/contextsmith-run/ after absorbing all 18 sections and 8 local refs into the orchestrator skill. Router updated, all dangling refs in shared/, docs/, AGENTS.md, PACKAGE_SPEC.md, README.md updated.

### Version 2.0.0 applied
All 7 surviving skills stamped to 2.0.0. This is the project-level version mandated by Phase 5.5e.

### Append-only auto-repair
Orchestrator now snapshots EDUCATIONAL_REPORT.md, AUDIT_REPORT.md, PHASE_LOG.md, and DECISIONS.md before harness dispatch. If the agent overwrites, the orchestrator prepends original content back. This protects the append-only contract from agent mistakes.

### Exit code expansion
Exit codes 0-5 provide distinct signals for callers:
- 0: done, 1: blocked, 2: continue, 3: config error, 4: state inconsistency, 5: internal error

### Pre-dispatch counter check
Counter check moved to before adapter.execute() as a fast-fail optimization. The transition resolver still checks counters as a second layer. This prevents unnecessary agent dispatch when max_retries is already reached.

### validation_mode sources of truth
validation_mode appears in 3 places: StepContract dataclass, workflow_config.schema.json StateDefinition, and orchestrator.py _execute_and_validate_step branch. All 3 must be kept in sync.

### RESULT.json fallback scope
Fallback is backward-compatible only. Phase 6e ensured no pre-orchestrator RESULT.json-absent directories exist in active use, but the fallback protects against the edge case.

### model_pin field
model_pin is in schema now but the step_compiler already reads it. The full pipeline (schema → step_compiler → StepContract → harness adapter) is now complete. Before this phase, model_pin was settable only through StepContract directly.
