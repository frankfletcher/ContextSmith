# Decisions: Runtime Enforcement for ContextSmith Skills

## Artifact Manifest
- artifact_type: decisions
- parent_task: TASK.md
- status: initial decisions recorded
- behavioral_contract: Record durable choices with reasons; separate facts from assumptions.

## Decisions

### 1. Hybrid: repo validation AND installed-skill enforcement
Decision: Both paths must work. Repository-local validation for development quality. Installed-skill validators for runtime enforcement when skills run outside the repo.

Reason: Repo-local checks catch issues during package development. Installed validators ensure deterministic behavior during actual skill use. Both are needed for a complete enforcement story.

### 2. Separate deterministic validation from hard blocking
Decision: Use validators for deterministic pass/fail evidence, and use harness integration only where available for hard blocking.

Reason: CLI and MCP tools can make the checks deterministic, but a model can still ignore advisory results unless the harness enforces them.

### 3. Prefer one validator core with CLI and MCP frontends
Decision: Design one shared validation core and expose it through both CLI and MCP.

Reason: CLI is portable across harnesses. MCP is better for agent-native calls. Duplicating logic would create drift.

### 4. Pilot with `contextsmith-run`
Decision: Use `contextsmith-run` as the first skill integration candidate.

Reason: It already defines execution contracts, validation levels, evidence ledgers, self-audit, and runtime obligations.

### 5. Treat pytest as approved for runtime tests
Decision: Pytest is approved for validator, CLI, domain-pack, and runner tests.

Reason: The current user explicitly approved pytest for this plan. Other new dependencies still require approval.

### 6. Separate planner review from small-model execution
Decision: Broad architecture choices require human or stronger-model review gates. Small/local models should execute only atomic implementation or test phases.

Reason: The runtime architecture is sweeping. The plan should be executable by small models without asking them to make system-level design decisions.

### 7. Generalize through domain packs
Decision: Keep the validator core universal and express domain-specific rules as compact domain packs where possible.

Reason: The system should work for skills, agents, and prompts across coding, writing, research, scheduling, purchase/travel, education, and unknown fallback tasks.

## Phase 0 Durable Facts (2026-06-02)
- **Packaging is manifest-driven**: `sync_shared_refs.py` only copies files declared in `reference_manifest.yml`. No wildcard or directory-sweep behavior.
- **No file-type filtering**: the sync script can copy `.py`, `.yml`, `.json`, or any other extension if declared in the manifest.
- **`reference_manifest.yml` excluded from zips**: `package_skill.sh:119` explicitly excludes it. Installed skills rely on `MANIFEST.json` (auto-generated with sha256 checksums).
- **Skill-root local files don't ship at their original path**: they're declared as `local: true` and land under `references/`, not at the skill root.
- **Release bundle stages selectively**: only `README.md`, `CHANGELOG.md`, `docs/`, and `SKILL.md` + synced references. Scripts, tests, and non-declared files are excluded.
- **Install script verifies checksums**: `install_skill.sh` reads `MANIFEST.json` and verifies every file's sha256 before installing.

## Phase 0.5 Decisions (2026-06-02)

### 8. Distribution model: Per-skill manifest entries (same as references)
Decision: Runtime files ship declared in each skill's `reference_manifest.yml`, using the same manifest-driven sync mechanism as shared references.

Reason: Each installed skill must be self-contained. A separate runtime package introduces install ordering, version coupling, and path resolution problems the current system avoids. The manifest model already handles arbitrary file types (`.py`, `.json`, `.yml`) — runtime files are just another reference category. Duplication is acceptable for the first slice given the small file sizes.

Packaging implication: No packaging script changes needed. Runtime files are declared in each skill's `reference_manifest.yml` and synced via `sync_shared_refs.py` like existing references.

### 9. Runtime dependency policy: stdlib-only JSON for the first slice
Decision: The first implementation slice uses only Python stdlib JSON parsing. No PyYAML, no new dependencies.

Reason: All runtime artifacts (requirements chain, phase contract, evidence ledger, approval record, phase closeout, domain packs) are structured data that can be represented as JSON. This keeps the first slice dependency-free and avoids the PyYAML approval path. YAML support can be added later with explicit approval.

Constraint on Phase 2A: The validator core must parse JSON only. If a fixture or domain pack requires YAML, Phase 2A must stop and record a blocker rather than importing PyYAML.

### 10. First-slice scope: CLI validator + universal protocol + 1-2 domain packs
Decision: The first implementation slice covers the universal protocol (Phases 1A-1C), minimal validator core (2A), domain pack validator (2B), CLI adapter (2C), pytest tests (2D), smoke test (2E), and starter domain packs (3A-3F). Runner, MCP, and harness adapters are deferred.

Reason: The core must be stable and proven before adapters multiply behavior. The CLI is portable across harnesses. Domain packs demonstrate the system works for non-coding tasks.

### 11. Phase 1A authorized: yes
Authorization: Phase 1A (Universal Artifact Vocabulary) is authorized to proceed.

Reason: The distribution model, dependency policy, and first-slice scope are recorded. Phase 1A is a small-model design phase that defines artifact names and fields — it requires no new dependencies, no package changes, and no implementation. It is bounded to six artifact types with a 20k-30k token budget.

## Phase 1A Decisions (2026-06-02)

### 12. Universal Artifact Vocabulary — six types defined
Decision: Six artifact types are sufficient for the universal protocol: `requirements_chain`, `phase_contract`, `domain_pack`, `evidence_ledger`, `approval_record`, `phase_closeout`.

Reason: These cover the full lifecycle — requirements trace, phase bounding, domain rules, evidence recording, authorization tracking, and completion validation. No artifact requires hidden reasoning. Each is representable as JSON and YAML. All examples are domain-neutral.

Artifact: `ARTIFACT_VOCABULARY.md` in this task directory.

### 13. Phase 1A complete, Phase 1B authorized
Authorization: Phase 1B (Requirements Chain Schema) is authorized to proceed.

Reason: The vocabulary is defined and validated. Phase 1B will detail the requirements chain schema with exact field semantics and trace examples.

## Phase 1B Decisions (2026-06-02)

### 14. Requirements Chain Schema — linear trace model
Decision: The requirements chain uses a linear trace model with eight required fields: `id`, `source`, `domain`, `side_effect_tier`, `validation_method`, `phase_ids`, `evidence_ids`, `status`.

Reason: A linear model is sufficient for tracing requirements through phases. No graph logic is needed. Parent-child relationships use an optional `parent_id` field. The schema is compact enough for a local model to emit without carrying long instructions.

Artifact: `REQUIREMENTS_CHAIN_SCHEMA.md` in this task directory.

### 15. Phase 1B complete, Phase 1B.5 authorized
Authorization: Phase 1B.5 (Approval Record Schema) is authorized to proceed.

Reason: The requirements chain schema is defined and validated. Phase 1B.5 will detail the approval record schema with exact field semantics and an external-action example.

## Phase 1B.5 Decisions (2026-06-02)

### 16. Approval Record Schema — ten required fields, five status values
Decision: The approval record uses ten required fields: `id`, `requirement_ids`, `action`, `side_effect_tier`, `requester`, `approver`, `status`, `timestamp`, `evidence_id`, `residual_risk`. Status values: `not_required`, `requested`, `approved`, `denied`, `waived_by_user`.

Reason: Approval records must document authorization without automating external actions. The five status values cover the full lifecycle from no-approval-needed through explicit denial. The ten fields provide enough traceability for a validator to check that high-risk actions have evidence before proceeding.

Artifact: `APPROVAL_RECORD_SCHEMA.md` in this task directory.

### 17. Phase 1B.5 complete, Phase 1C authorized
Authorization: Phase 1C (Domain Pack Schema) is authorized to proceed.

Reason: The approval record schema is defined and validated. Phase 1C will detail the domain pack schema with starter domain pack outlines.

## Phase 1D Architecture Review Gate (2026-06-02)

### 18. Architecture Review — schemas approved with corrections

Decision: The Phases 1A-1C schemas pass the architecture review gate with four recorded findings. Two are corrections for Phase 1C, one is a documentation gap, and one is a design note for Phase 2A.

**Review Q1 — Universal applicability: PASS**
The six artifact types are structurally domain-neutral. The `domain` field and domain-pack triggers provide extension points. All six starter packs demonstrate coverage across coding, writing, research, scheduling, travel/purchase, and general fallback.

**Review Q2 — Approval boundaries explicit: PASS with correction**
The approval_record schema provides five status values with explicit proceed/do-not-proceed semantics. Domain packs' `external_action_boundaries` map actions to `allowed`/`requires_approval`/`blocked`. However, validation rule 9 requires that every `requires_approval` boundary has a corresponding `approval_gates` entry. The `software_engineering` starter pack violates this: `external_action_boundaries` lists `deploy_staging: requires_approval` and `deploy_production: requires_approval`, but `approval_gates` only contains `deploy_to_production` (missing `deploy_staging`).

*Correction for Phase 1C:* Add `deploy_staging` to the `software_engineering` `approval_gates` list, or rename `deploy_to_production` to match the boundary key `deploy_production`.

**Review Q3 — Small-model emit feasibility: PASS with documentation gap**
All six artifact types are compact with explicit required fields and JSON examples. A small model can emit each without carrying long instructions. However, `phase_contract` and `evidence_ledger` have vocabulary entries (Phase 1A) but lack dedicated schema files with validation rules, unlike `requirements_chain`, `approval_record`, and `domain_pack`.

*Recommendation:* Phase 1C.5 (or equivalent) should produce `PHASE_CONTRACT_SCHEMA.md` and `EVIDENCE_LEDGER_SCHEMA.md` with field semantics and validation rules to match the other schema files. Keep the active validator format JSON-only unless a later phase explicitly adds YAML support.

**Review Q4 — Validator determinism: PASS with design note**
The validation rules for requirements_chain (8 rules), approval_record (12 rules), and domain_pack (10 rules) are all field-presence, value-check, or enum-check operations — easily implementable as deterministic Python. However, the domain pack `validation_gates` structure supports `check_type: artifact_check` and `check_type: user_confirmation`, which are not deterministic (they require content inspection or human interaction).

*Design note for Phase 2A:* The validator core should distinguish between deterministic structural checks (always pass/fail) and domain-specific content checks (may require heuristics, external tools, or human input). This affects how the CLI reports results and how the runner handles partial validation.

### 19. Phase 1D complete, Phase 2A authorized

Authorization: Phase 2A (Minimal Validator Core) is authorized to proceed after the Phase 1C correction is applied.

Reason: The architecture review confirms the schemas are universally applicable, have explicit approval boundaries, are small-model emit-friendly, and have deterministic validation rules. The one correction (software_engineering approval_gates consistency) is a data fix, not a schema redesign.
- Whether package design changes require a `PACKAGE_SPEC.md` update.
- Whether opencode can enforce validator success as a closeout or permission gate.
- Which additional domain packs should be added after the starter set.
- Whether the install script needs extension to support the separate runtime package (Phase 2E smoke-test concern).

## Tracked Issues

### ISSUE-1: Packaging flattening breaks runtime module paths (medium risk)
Discovered: Phase 4 audit, 2026-06-02
Status: Open — blocks Phase 8B rollout

**Problem:** `sync_shared_refs.py` flattens all `local: true` files into `references/`, stripping their directory structure. Phase 4A declares `runtime/validator.py`, `runtime/cli.py`, `runtime/__init__.py`, and `runtime/domain_packs/*.json` as local entries. After sync, these become `references/validator.py`, `references/cli.py`, etc. — breaking `python -m runtime.cli` because the `runtime/` Python package no longer exists.

**Impact:** The Phase 2E smoke test worked by manually copying files with preserved paths, not through manifest-driven sync. An installed `contextsmith-run` skill will have runtime files in the wrong location, making the CLI invocations in SKILL.md step 9 and the Runtime Validators subsection non-functional.

**Options:**
1. **Separate runtime package** — ship `contextsmith-runtime` as its own installable package, not per-skill. Requires install ordering and path resolution.
2. **Post-install path rewrite** — add a post-install hook that reconstructs the `runtime/` directory from flattened `references/` files. Fragile and adds complexity.
3. **Extend sync script** — modify `sync_shared_refs.py` to preserve directory structure for `local: true` entries. Changes packaging behavior for all skills.
4. **Inline CLI** — rewrite the CLI as a single-file script that doesn't need a package structure. Loses modularity.

**Decision needed before:** Phase 8B rollout. This is a blocker for any skill that ships runtime files via per-skill manifest entries.

**Phase 0.5 Decision 8 reference:** Chose per-skill manifest entries over separate runtime package. This issue is a consequence of that choice combined with the sync script's flattening behavior.
