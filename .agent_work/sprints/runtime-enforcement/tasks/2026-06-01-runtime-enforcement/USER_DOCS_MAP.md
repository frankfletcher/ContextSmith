# User Documentation Map — Phase 7A

## Artifact Manifest
- artifact_type: documentation_map
- generated_by: Phase 7A execution
- phase: 7A
- scope: design only (no documentation content written)

---

## 1. Documentation Inventory

### Existing User-Facing Docs
| File | Purpose | Status | Assessment |
|------|---------|--------|------------|
| `README.md` | Landing page, capabilities, quick commands, installation | Exists | Needs refresh: reorganize for reader journey, add runtime enforcement section, update project status |
| `docs/QUICKSTART.md` | Fastest path to first useful result | Exists | Verify covers a single complete workflow end-to-end |
| `docs/USER_GUIDE.md` | General usage guide | Exists | May overlap with QUICKSTART; assess whether to merge or specialize |
| `docs/USER_MANUAL.md` | Comprehensive reference manual | Exists | Likely too broad; evaluate against reader journey |
| `docs/WHICH_SKILL.md` | Skill selection guide | Exists | Keep as "choose a workflow" step |
| `docs/FAQ.md` | Common questions | Exists | Verify answers are current |
| `docs/EXAMPLES.md` | Example workflows | Exists | Expand with runtime enforcement examples |
| `docs/RELEASE_PROCESS.md` | Build and install guide | Exists | Technical but user-facing for self-hosters |
| `docs/RUNTIME_STABILITY.md` | Runtime enforcement overview | Exists | New feature; needs user-facing framing |

### Existing Workflow Docs (`docs/workflows/`)
| File | Purpose | Status |
|------|---------|--------|
| `docs/workflows/README.md` | Workflows index | Exists |
| `docs/workflows/AGENTS_MD_GUIDE.md` | How to use AGENTS.md engineering | Exists |
| `docs/workflows/SMALL_CONTEXT_WORKFLOWS.md` | Small context coding workflow | Exists |
| `docs/workflows/TEST_QUALITY_AUDIT.md` | Test audit workflow | Exists |
| `docs/workflows/PHASE_CODE_REVIEW.md` | Phase code review workflow | Exists |
| `docs/workflows/IMPLEMENTATION_PLAN_AUDIT.md` | Plan audit workflow | Exists |
| `docs/workflows/SKILL_MIGRATION.md` | Skill migration workflow | Exists |
| `docs/workflows/RUNTIME_STABILITY.md` | Runtime stability workflow | Exists |

### Existing Concept Docs (`docs/concepts/`)
| File | Purpose | Status |
|------|---------|--------|
| `docs/concepts/README.md` | Concepts index | Exists |
| `docs/concepts/MODEL_PROFILES.md` | Model profile explanations | Exists |
| `docs/concepts/RALPH_LOOP.md` | Ralph improvement loop | Exists |

### Existing Reference Docs (`docs/reference/`)
| File | Purpose | Status |
|------|---------|--------|
| `docs/reference/README.md` | Reference index | Exists |
| `docs/reference/CONTROL_PARAMETERS.md` | Parameter reference | Exists |
| `docs/reference/EXAMPLES.md` | Reference examples | Exists |
| `docs/reference/VERSIONING.md` | Version history and policy | Exists |

### Contributing Docs (`docs/contributing/`)
| File | Purpose | Audience |
|------|---------|----------|
| `docs/contributing/documentation-style.md` | Voice and style guide | Contributors |
| `docs/contributing/documentation-review-checklist.md` | Quality review criteria | Contributors |

### Identified Gaps
| Gap | Priority | Phase Assignment |
|-----|----------|------------------|
| Runtime enforcement user guide (what it is, how to use CLI/MCP) | High | Phase 7D |
| Domain packs user guide (what they are, how to create one) | High | Phase 7D |
| Next Prompt Compiler user guide | Medium | Phase 7D |
| Recovery and troubleshooting guide | Medium | Phase 7E |
| "Create a plan" use-case walkthrough | High | Phase 7E |
| "Run a phase with enforcement" use-case walkthrough | High | Phase 7E |
| Non-coding workflow examples (writing, research, scheduling) | Medium | Phase 7F |
| Runner and orchestrated workflow guide | Low | Phase 7E (deferred if runner not yet complete) |

### Duplication Issue
Several files exist at both `docs/` root and in subdirectories (e.g., `docs/AGENTS_MD_GUIDE.md` and `docs/workflows/AGENTS_MD_GUIDE.md`). This needs resolution in Phase 7B+ — either consolidate to one location per file or clarify the distinction between root-level summaries and subdirectory deep-dives.

---

## 2. Reader Journey

```
README.md
  |
  v
docs/QUICKSTART.md  (fastest path to first value)
  |
  v
docs/WHICH_SKILL.md  (choose a workflow)
  |
  v
docs/workflows/<specific-workflow>.md  (detailed how-to)
  |
  v
docs/reference/  (parameter reference, versioning)
  |
  v
docs/concepts/  (model profiles, Ralph loop, etc.)
```

**Alternative paths:**
- `README.md` -> `docs/EXAMPLES.md` (inspiration-first users)
- `README.md` -> `docs/FAQ.md` (question-driven users)
- `README.md` -> `docs/RUNTIME_STABILITY.md` (runtime enforcement interested)

---

## 3. Primary User Jobs

| User Job | Entry Point | Supporting Docs |
|----------|-------------|-----------------|
| Create a plan | `WHICH_SKILL.md` -> `workflows/IMPLEMENTATION_PLAN_AUDIT.md` | `concepts/MODEL_PROFILES.md`, `reference/CONTROL_PARAMETERS.md` |
| Run a plan | `QUICKSTART.md` -> `workflows/` | `concepts/RALPH_LOOP.md` |
| Validate a phase | `workflows/PHASE_CODE_REVIEW.md` | `RUNTIME_STABILITY.md` |
| Recover from a blocker | GAP — needs troubleshooting guide | `FAQ.md` |
| Use a domain pack | GAP — needs domain packs guide | `RUNTIME_STABILITY.md` |
| Review examples | `EXAMPLES.md` | `workflows/` |
| Install and set up | `README.md` Installation section | `RELEASE_PROCESS.md` |
| Migrate skills | `WHICH_SKILL.md` -> `workflows/SKILL_MIGRATION.md` | `reference/VERSIONING.md` |

---

## 4. User-Facing vs Agent-Facing Classification

### User-Facing (polish for readability)
- `README.md`
- `docs/QUICKSTART.md`
- `docs/USER_GUIDE.md`
- `docs/USER_MANUAL.md`
- `docs/WHICH_SKILL.md`
- `docs/FAQ.md`
- `docs/EXAMPLES.md`
- `docs/RELEASE_PROCESS.md`
- `docs/RUNTIME_STABILITY.md`
- `docs/workflows/` (all)
- `docs/concepts/` (all)
- `docs/reference/` (all)
- `docs/contributing/` (all)

### Agent-Facing (keep imperative, do not soften)
- `skills/*/SKILL.md`
- `skills/*/references/`
- `shared/` (42 reference files)
- `AGENTS.md`
- `PACKAGE_SPEC.md`
- `.agent_work/` (task state — internal)

---

## 5. Table-of-Contents Requirements

Every substantial Markdown file (more than 5 sections) should include a table of contents immediately after the top-level heading:

```markdown
# Title

- [Section 1](#section-1)
- [Section 2](#section-2)
  - [Subsection 2.1](#subsection-21)
- [Section 3](#section-3)
```

**Files that need TOC added:** `README.md`, `docs/QUICKSTART.md`, `docs/USER_GUIDE.md`, `docs/USER_MANUAL.md`, `docs/RUNTIME_STABILITY.md`, and any workflow doc exceeding 5 sections.

---

## 6. Website-Readiness Constraints

- **Stable headings:** Use ATX headings (`##`, `###`) consistently. Avoid heading levels that would break when extracted as standalone pages.
- **Clear page purpose:** Each file should have a single, scannable purpose statement in the first paragraph.
- **Examples as website sections:** Code blocks and examples should be self-contained — they should not reference "the above" or "as mentioned earlier" in a way that depends on reading a specific prior page.
- **No hidden chat-only context:** Avoid phrases like "as the agent will do" or "when you invoke the skill" without explaining what that means to a reader who hasn't used the system yet.
- **Cross-links:** Use relative Markdown links (`[link](../concepts/model-profiles.md)`) that work both in GitHub and when rendered as a flat static site.

---

## 7. Phase Assignment

| Phase | Focus | Files |
|-------|-------|-------|
| **7B** | README refresh | `README.md` — reorganize for reader journey, add runtime section, fix links, add TOC |
| **7C** | Quickstart polish | `docs/QUICKSTART.md` — single complete workflow, expected output, add TOC |
| **7D** | Runtime workflow docs | `docs/RUNTIME_STABILITY.md` (user-facing rewrite), new domain packs guide, new Next Prompt Compiler guide |
| **7E** | Use-case walkthroughs | New: "Create a plan" guide, "Run with enforcement" guide, troubleshooting/recovery guide |
| **7F** | Examples library | `docs/EXAMPLES.md` — expand with runtime enforcement and non-coding examples |
| **7G** | Quality audit | Run documentation review checklist against all edited files |

---

## 8. Runtime Enforcement Feature Labeling

Per NEXT_PROMPT.md guidance:
- **Implemented (available):** Validator CLI (`runtime/validator.py`), 6 domain packs, Next Prompt Compiler, Runner skeleton, contextsmith-run pilot integration
- **Active development:** MCP adapter (design complete, Phase 6C pending), Harness adapter (design complete, Phase 6C pending)
- **Design only:** Orchestrated runner (full implementation), cross-harness benchmarks, automated behavioral tests
