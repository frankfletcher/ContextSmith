# Context: Runtime Enforcement for ContextSmith Skills

## Artifact Manifest
- artifact_type: context
- parent_task: TASK.md
- context_scope: files, constraints, known facts, and skip rules for future sessions
- behavioral_contract: Keep this file compact and factual; do not paste transcripts or full command output.

## Known Facts
- ContextSmith skills currently appear to ship as markdown and YAML assets inside `skills/<skill>/`.
- Existing repo validation is build-time and package-structure oriented.
- Runtime behavior is mostly governed by skill instructions, evidence ledgers, self-audit, and declared-vs-enforced checks.
- Deterministic runtime validation requires executable checks or harness-enforced gates.
- Preliminary script inspection found individual skill packaging and release bundle packaging may include different file sets; Phase 0 must verify both paths before implementation.
- The revised plan treats the runtime as universal infrastructure for skills, agents, and prompts, not only coding skills.
- Pytest is pre-approved by the current user. YAML/PyYAML is not needed for the first runtime slice.

## Files to Inspect in Phase 0
| Path | Purpose |
|---|---|
| `scripts/build_release.py` | Determine release packaging flow |
| `scripts/package_skill.sh` | Determine individual skill zip behavior |
| `scripts/sync_shared_refs.py` | Determine what files enter staged skill packages |
| `scripts/token_budget.py` | Required release validation after skill/reference edits |
| `scripts/` | Find packaging, manifest, sync, and release helpers |
| `skills/contextsmith-run/` | Pilot skill for runtime enforcement |
| `skills/*/reference_manifest.yml` | Understand shipped reference declarations |
| `PACKAGE_SPEC.md` | Read-only design context unless approval is granted |
| `CHANGELOG.md` | User-facing changes if implementation modifies behavior |

## Candidate Runtime Concepts
| Concept | Runtime Role |
|---|---|
| Universal protocol | Shared requirements, phase, evidence, approval, and closeout artifacts |
| Domain pack | Domain-specific validation gates and approval boundaries as compact data |
| Artifact manifest validator | Checks generated artifacts expose required metadata |
| Parameter contract validator | Detects missing values and forbidden widenings |
| Evidence ledger validator | Checks declared obligations have evidence |
| Phase closeout validator | Checks validation status before completion |
| Orchestrated runner | Workflow-level gate loop that advances only after validation passes |
| Next prompt compiler | Generates detailed small-model phase prompts from task state without running the model |
| MCP wrapper | Lets agents call validators as tools |
| Harness gate | Optional hard-blocking integration where supported |

## Constraints
- Do not edit files outside the workspace without explicit approval.
- Do not add dependencies without approval.
- Do not edit `PACKAGE_SPEC.md` design decisions without approval.
- Do not modify user-level opencode configuration without approval.
- Do not claim hard enforcement unless the harness actually blocks bypass.
- Do not start validator implementation until Phase 0.5 records the provisional distribution model.
- Do not start validator implementation until Phase 0.5 records the runtime dependency policy and whether YAML/PyYAML is required, optional, or avoided.
- Do not roll out across more than two skills in one phase without explicit approval.
- Do not carry raw search, validation, or fixture output across phases; compact to facts and commands.
- Small models are enabled for all decisions including broad architecture; human/frontier review is optional for universal protocol, domain-pack strategy, runner design, MCP design, and harness claims.
- Do not describe orchestrated runner behavior as hard enforcement; it only enforces workflows that opt into the runner.
- Do not continue after a blocked phase until the recovery procedure updates STATUS.md, PHASE_LOG.md, ARTIFACTS.md, and NEXT_PROMPT.md.
- Do not execute Phase 8B unless Phase 8A names an exact target count and exact skill or skills.
- Do not let the Next Prompt Compiler execute phases or invoke models; it only generates safe handoff prompts.

## Validation Commands
- `python scripts/validate_skills.py` after skill or shared-reference changes.
- `python scripts/token_budget.py --strict` after skill or shared-reference changes.
- `python -m pytest tests/ -v` after runtime validator, domain-pack, CLI, or runner test changes.
- Future runtime validator commands after the validator exists.

## Risk Mitigations
- Packaging uncertainty: Phase 0 verifies individual packages, release bundle, and staged reference sync separately.
- Context overflow: every tool-heavy phase has a context contract, compaction trigger, and stop rule.
- Distribution rework: Phase 0.5 decides the provisional runtime distribution path before implementation.
- Dependency drift: Phase 0.5 decides runtime parsing/dependency policy before Phase 2A; Phase 2A must stop if parser implementation conflicts with that policy.
- Overstated enforcement: every design must label deterministic validation, advisory model behavior, and harness hard-blocking separately.
- Rollout blast radius: Phase 6 is split into scope selection and per-batch rollout.
- Validation gaps: fixture checks must include passing and failing cases before skill integration.
- Architecture sweep risk: phases are split into small-model implementation slices and optional human/frontier review gates.
- Generality risk: starter domain packs must cover software, writing, research, scheduling, travel/purchase, and general fallback before rollout.
- Rollout scope creep: Phase 8A must name an exact target count, and Phase 8B cannot touch deferred skills.
- Smoke-test fragility: if packaging cannot carry runtime files, Phase 2E records a fallback path instead of redesigning packaging mid-phase.
- Handoff drift: every phase closeout records carry-forward and do-not-carry-forward notes.
- Handoff quality: Next Prompt Compiler creates detailed phase prompts with validation, audit, closeout, recovery, and hard-stop sections.
- Documentation drift: docs phases focus on user tasks, examples, time to first value, and lookup paths; architecture details appear only when they help users operate the system.

## Documentation Direction
- README should be catchy, practical, and clear about the pain point.
- README should act as the front door to quickstart, workflows, examples, and reference docs.
- User docs should teach how to use ContextSmith, not primarily explain internal architecture.
- Substantial Markdown docs should include a table of contents and stable headings for future website generation.
- Examples should show expected outputs and recovery paths, not only commands.

## Phase 0 Packaging Facts (2026-06-02)

### Individual skill zip (`package_skill.sh`)
1. Syncs references via `sync_shared_refs.py --skill <name>` into `.agent_work/staged_skills/<name>/`
2. Generates `MANIFEST.json` (sha256 checksums for every staged file)
3. Zips from staging, excluding `reference_manifest.yml` and `references/.gitkeep`
4. **Zip contents**: `SKILL.md`, `MANIFEST.json`, and all manifest-declared references under `references/`
5. Skill-root local files (e.g., `execution-contract.md`) are NOT included unless declared as `local: true` in the manifest — they end up under `references/`, not at the skill root
6. Evidence: `package_skill.sh:48-121`, `sync_shared_refs.py:43-111`

### Release bundle (`build_release.py step_bundle`)
1. Stages `README.md`, `CHANGELOG.md`, `docs/`, and `skills/<name>/SKILL.md` into `.agent_work/release_bundle/`
2. Runs `sync_shared_refs.py --all --staging-dir <bundle>/skills/` to populate references
3. Walks entire staging tree into `contextsmith-release.zip`
4. **Bundle contents**: top-level files, all docs, SKILL.md + synced references for each skill
5. Evidence: `build_release.py:256-345`

### Staging sync behavior (`sync_shared_refs.py`)
- Copies SKILL.md into staging (line 44-51)
- Iterates `reference_manifest.yml` entries; copies only `required: true` entries (line 60)
- Non-local sources must start with `shared/` (line 66-68)
- Local sources (`local: true`) copy by basename into `references/` (line 86-88)
- Non-local sources preserve subdirectory structure under `references/` (line 90-91)
- **Does NOT copy arbitrary files** — only manifest-declared references
- No file-type filtering: any file declared in the manifest can be copied
- Evidence: `sync_shared_refs.py:28-113`

### Can runtime files ship?
| File type | Can ship? | How |
|---|---|---|
| Executable `.py` / `.sh` | Yes, if added to `reference_manifest.yml` | Declare as `local: true` (skill-root) or `shared/` source |
| YAML schemas (`.yml`) | Yes, if added to manifest | Same mechanism |
| Fixtures (`.yml`, `.json`) | Yes, if added to manifest | Same mechanism |
| Domain packs (`.yml`) | Yes, if added to manifest | Same mechanism |
| `reference_manifest.yml` itself | **Excluded** from zip | `package_skill.sh:119` explicitly excludes it |

### Key constraint
The sync script is manifest-driven, not directory-driven. Any new file type (`.py`, `.yml`, `.json`) must be explicitly declared in each skill's `reference_manifest.yml` to ship. There is no wildcard or directory-sweep behavior.

### Separate runtime package likely needed?
The manifest mechanism can carry runtime files, but adding Python executables and YAML schemas to every skill's manifest would be repetitive. A separate `contextsmith-runtime` package (or a `shared/runtime/` directory with its own manifest) would avoid duplication. This is a Phase 0.5 decision.

### Phase 0.5 Decisions (2026-06-02)
- **Decision 1**: Hybrid enforcement — repo validation AND installed-skill enforcement.
- **Decision 4**: Pilot skills — `contextsmith-run` and `contextsmith-prompt-engineer`.
- **Decision 6**: Small model enabled for everything; frontier model optional.
- **Decision 8**: Per-skill manifest entries — runtime files declared in each skill's `reference_manifest.yml`, same as shared references.
- **Decision 9**: stdlib-only JSON for the first runtime slice; YAML/PyYAML deferred.
- **Decision 10**: Full stack first slice — CLI + MCP + runner + harness + domain packs, incremental testing OK.

## Phase Token Budgets (Actuals)
| Phase | Estimated | Actual | Notes |
|---|---|---|---|
| Phase 0 | 40k-60k | 78k | Discovery: 4-8 reads, 1 dry-run, 0 edits. Exceeded due to accumulated system/AGENTS.md/PLAN.md overhead. Use as baseline for discovery phases. |

## Open Questions
- Should runtime files be declared per-skill in each `reference_manifest.yml`, or shipped as a separate package? — Resolved: per-skill manifest entries (Decision 8, 2026-06-02).
- Which runtime surfaces belong in the first implementation slice? — Resolved: full stack (Decision 10, 2026-06-02).
- Can opencode require a successful validator call before finalization or risky actions?
