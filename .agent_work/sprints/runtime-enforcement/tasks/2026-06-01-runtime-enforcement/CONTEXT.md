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
- Pytest is pre-approved by the current user for validator and runner tests.

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
- Do not roll out across more than two skills in one phase without explicit approval.
- Do not carry raw search, validation, or fixture output across phases; compact to facts and commands.
- Do not ask a small model to make broad architecture decisions; use human/frontier review gates for universal protocol, domain-pack strategy, runner design, MCP design, and harness claims.
- Do not describe orchestrated runner behavior as hard enforcement; it only enforces workflows that opt into the runner.
- Do not continue after a blocked phase until the recovery procedure updates STATUS.md, PHASE_LOG.md, ARTIFACTS.md, and NEXT_PROMPT.md.
- Do not execute Phase 7B unless Phase 7A names an exact target count and exact skill or skills.
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
- Overstated enforcement: every design must label deterministic validation, advisory model behavior, and harness hard-blocking separately.
- Rollout blast radius: Phase 6 is split into scope selection and per-batch rollout.
- Validation gaps: fixture checks must include passing and failing cases before skill integration.
- Architecture sweep risk: phases are split into small-model implementation slices and human/frontier review gates.
- Generality risk: starter domain packs must cover software, writing, research, scheduling, travel/purchase, and general fallback before rollout.
- Rollout scope creep: Phase 7A must name an exact target count, and Phase 7B cannot touch deferred skills.
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

## Open Questions
- Does the release builder include non-markdown executable files from skill directories?
- Should the runtime live in each skill bundle, a separate installable package, or both?
- Can opencode require a successful validator call before finalization or risky actions?
- Which runtime surfaces belong in the first implementation slice: CLI only, CLI plus domain packs, CLI plus runner, MCP, or harness adapter?
