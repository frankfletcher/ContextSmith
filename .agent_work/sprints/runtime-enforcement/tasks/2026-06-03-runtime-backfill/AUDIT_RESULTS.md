# Phase B0 Audit Results: Runtime Framing Deviations

**Canonical framing** (from PLAN.md Architecture Direction + Enforcement Levels):
- "first-class ContextSmith tool"
- "default execution path"
- "opt-out, not mandatory"
- "standard path goes through them"
- Enforcement levels: Deterministic validation, Orchestrated workflow enforcement, Harness hard blocking, Human approval

---

## Per-Artifact Classification

| Artifact | Classification | Deviations |
|----------|---------------|------------|
| `README.md` | **needs-update** | Missing "first-class", "default execution path", "opt-out" framing. Runtime section reads as a feature listing, not as the default execution model. |
| `docs/workflows/RUNTIME_ENFORCEMENT.md` | **needs-update** | Enforcement levels table uses different labels than PLAN.md: "Advisory" (not in PLAN), "Hard-blocked" (PLAN says "Harness hard blocking"). Missing "Human approval" as a level. Missing "first-class/default/opt-out" framing in introduction. |
| `docs/QUICKSTART.md` | **minor-fix** | "Next 30 Minutes" section mentions runtime enforcement but doesn't frame it as the default path. Reads as an optional advanced feature rather than the standard execution mode. |
| `docs/examples/EXAMPLES_LIBRARY.md` | **no-runtime-mentions** | Examples demonstrate runtime features but don't include framing language about default/opt-out. Acceptable — examples show usage, not positioning. |
| `docs/workflows/CREATE_A_PLAN.md` | **no-runtime-mentions** | Step 4 mentions "runtime enforcement artifacts" and CLI commands but doesn't frame runtime as the default execution path. Acceptable — workflow doc, not positioning doc. |
| `docs/workflows/BUILD_OR_IMPROVE_A_SKILL.md` | **no-runtime-mentions** | No runtime enforcement mentions. Acceptable — skill-building workflow doesn't need runtime framing. |
| `shared/` files | **no-runtime-mentions** | References to "runtime" in shared/ are about model runtime settings (KV cache, speculative decoding, chat templates), not the enforcement system. No deviation — different meaning of "runtime". |
| `skills/*/SKILL.md` files | **no-runtime-mentions** | Agent-facing implementation references (validators, execution contracts, stability notes). Not user-facing positioning docs — framing audit does not apply. |

## Specific Deviations

### README.md (needs-update)
- **L1:** Runtime section (lines 74-89) presents runtime as a feature with "Available:" / "Active development:" labels. Should frame as "the default execution path" with opt-out available.
- **L2:** Missing the four enforcement level labels entirely. Should reference or link to them.
- **Fix:** Rewrite Runtime Enforcement section to lead with "first-class, default execution path, opt-out" framing. Add enforcement levels reference.

### docs/workflows/RUNTIME_ENFORCEMENT.md (needs-update)
- **L1:** Enforcement levels table (lines 240-252) uses "Advisory" instead of PLAN.md's four levels. PLAN.md has: Deterministic validation, Orchestrated workflow enforcement, Harness hard blocking, Human approval. This doc has: Advisory, Deterministic, Orchestrated, Hard-blocked.
- **L2:** "Advisory" level has no PLAN.md equivalent. PLAN.md's lowest level is "Deterministic validation".
- **L3:** Missing "Human approval" as an enforcement level (it's covered in task 8 but not in the levels table).
- **L4:** Introduction doesn't establish "first-class, default, opt-out" framing.
- **Fix:** Replace enforcement levels table with PLAN.md's four levels and exact labels. Add "first-class/default/opt-out" to introduction. Move "Human approval" into the levels table.

### docs/QUICKSTART.md (minor-fix)
- **L1:** "Next 30 Minutes" section (line 46) says "use ContextSmith's runtime enforcement to create agent instructions" — frames it as a choice rather than the default.
- **Fix:** Minor wording change to frame runtime enforcement as the standard path, not an optional feature.

## Summary

- **2 artifacts need updates**: README.md, RUNTIME_ENFORCEMENT.md
- **1 artifact needs minor fix**: QUICKSTART.md
- **5 artifacts are acceptable** (no framing needed): EXAMPLES_LIBRARY.md, CREATE_A_PLAN.md, BUILD_OR_IMPROVE_A_SKILL.md, shared/, skills/
- **Core issue**: The "first-class, default execution path, opt-out" framing from PLAN.md is absent from user-facing docs. The enforcement levels table in RUNTIME_ENFORCEMENT.md uses different labels than the canonical PLAN.md.
