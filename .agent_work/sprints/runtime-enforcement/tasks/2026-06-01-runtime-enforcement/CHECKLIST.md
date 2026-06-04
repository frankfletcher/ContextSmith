# Checklist: Runtime Enforcement for ContextSmith Skills

## Artifact Manifest
- artifact_type: checklist
- parent_task: TASK.md
- validation_level: planning strict; implementation available checks
- behavioral_contract: Use this checklist during phase closeout and final audit.

## Planning Quality
- [x] Problem is scoped to both repo-local validation AND installed-skill runtime enforcement (hybrid).
- [x] Plan separates deterministic validation from hard harness enforcement.
- [x] Plan includes CLI and MCP paths using shared validation logic.
- [x] Plan starts with packaging discovery before design-changing edits.
- [x] Plan includes validation evidence and task-state updates in every phase.
- [x] Tool-heavy phases include context contracts, compaction triggers, and stop rules.
- [x] Rollout is split into scope selection and per-batch execution.
- [x] Distribution model decision occurs before implementation.
- [x] Plan enables small models for all phases; human/frontier review is optional.
- [x] Plan supports general skill, agent, and prompt use cases beyond coding.
- [x] Plan labels deterministic validation, orchestrated workflow enforcement, harness hard blocking, and human approval separately.
- [x] Plan includes explicit recovery procedure for blocked phases.
- [x] Plan requires per-phase closeout updates to STATUS.md, PHASE_LOG.md, ARTIFACTS.md, and NEXT_PROMPT.md.
- [x] Phase 8 rollout is bounded by an exact skill count selected in Phase 8A.
- [x] Documentation workstream prioritizes how to use ContextSmith over architecture explanation.
- [x] Documentation plan includes README, quickstart, use-case workflows, examples, and quality audit before rollout.
- [x] Next Prompt Compiler is planned before the orchestrated runner.
- [x] Phase 0.5 requires distribution model, runtime dependency policy, first-slice scope, and Phase 1A authorization before implementation.

## Implementation Safety
- [x] Packaging behavior verified from source or built artifacts.
- [x] Distribution model recorded before implementation begins.
- [x] Runtime dependency policy recorded before validator implementation begins.
- [x] No dependency added without approval.
- [x] No `PACKAGE_SPEC.md` design edit made without approval.
- [x] No user-level opencode config modified without approval.
- [x] Skill changes validated with `python scripts/validate_skills.py`.
- [x] Skill/reference changes validated with `python scripts/token_budget.py --strict`.
- [ ] Rollout batch size stays within approved scope.
- [x] Small-model phases are capable of broad architecture decisions (frontier review optional).
- [x] Pytest is used only for approved phases; YAML/PyYAML is deferred.
- [ ] Blocked phases use the recovery procedure before any next-phase work begins.
- [x] Phase closeout records carry-forward and do-not-carry-forward notes.
- [x] Next Prompt Compiler does not execute phases, call models, or advance task state beyond writing handoff prompts.

## Runtime Enforcement Quality
- [x] Universal artifact vocabulary defined with six types.
- [x] Each artifact has purpose, required fields, and domain-neutral JSON example.
- [x] Requirements chain schema defined with eight required fields and linear trace model.
- [x] Requirements chain trace example covers pending -> passed lifecycle.
- [x] Approval record schema defined with ten required fields and five status values.
- [x] Approval record example shows travel purchase remains requested/denied without explicit user approval.
- [x] Validator checks are executable and deterministic.
- [x] Validator output has stable exit codes or structured MCP results.
- [x] Artifacts expose machine-readable fields for validation.
- [x] Advisory validation and hard blocking are clearly labeled.
- [x] Pilot workflow demonstrates a passing and failing runtime check.
- [x] Fixture set covers baseline, missing-field, widened-parameter, missing-evidence, and failed-closeout cases.
- [x] Sample installed-skill workflow proves the validator can run outside the repo-local planning context.
- [x] Universal protocol validates requirements chains, phase contracts, evidence ledgers, approval records, and closeouts.
- [x] Starter domain packs cover software, writing, research, scheduling, travel/purchase, and general fallback.
- [x] Phase 3G review confirms starter packs are compact, approval-boundary aligned, and fallback-capable.
- [x] Architecture review gate confirms schemas are universally applicable, approval-boundary-explicit, small-model-emit-friendly, and validator-deterministic.
- [x] Orchestrated runner claims are limited to workflow-level enforcement unless a harness hard-block is proven.
- [x] Installed-workflow smoke test records a fallback path if packaging cannot carry runtime files.
- [x] Harness adapter design includes positive completion criteria, not only stop rules.
- [x] Generated next prompts include validation, audit, closeout, recovery, and hard-stop sections.
- [x] Generated next prompts render cleanly as Markdown with balanced fences.
- [x] Phase 2A parser behavior matches the Phase 0.5 dependency policy.
- [x] Phase 3F research-summary pack validates sources, unsupported claims, uncertainty/limitations, evidence traceability, and external-use approval boundaries.
- [x] Phase 7D runtime workflow docs cover all 8 required user tasks with TOC, enforcement levels, and non-coding examples.
- [x] Phase 7D runtime workflow docs mark unimplemented adapters as active development.
- [x] Phase 7D Ralph loop: 2 iterations (iteration 1: added quickstart reference and expected output; iteration 2: no-op).
- [x] Phase 7E use-case workflow docs: 2 workflow pages created (CREATE_A_PLAN.md, BUILD_OR_IMPROVE_A_SKILL.md).
- [x] Phase 7E workflows have table of contents.
- [x] Phase 7E workflows include inputs, commands/prompts, expected artifacts, validation, and common failure modes.
- [x] Phase 7E remaining workflow ideas recorded as deferred.
- [x] Phase 7E Ralph loop: 2 iterations (iteration 1: added Next Prompt Compiler ref and budget fix guidance; iteration 2: no-op).
- [x] Phase 7F examples library: 3 examples created (task-state run, domain pack validation, failure and recovery).
- [x] Phase 7F examples labeled as implemented, planned, or illustrative.
- [x] Phase 7F examples show expected outputs, not only inputs.
- [x] Phase 7F examples do not perform irreversible external actions.
- [x] Phase 7F deferred examples listed for a later batch.
- [x] Phase 7F Ralph loop: 2 iterations (iteration 1: no material defects; iteration 2: no-op).
- [x] Phase 7G documentation quality audit: 6 docs audited, all PASS, 3 targeted fixes applied.
- [x] Phase 7G fixes: QUICKSTART.md 30-min path coherence, README.md directory links, RUNTIME_ENFORCEMENT.md quickstart link.
- [x] Phase 7G Ralph loop: 2 iterations (iteration 1: no additional defects; iteration 2: no-op).

## Phase 8A: Rollout Scope Selection
- [x] All 7 skills listed in rollout matrix.
- [x] Each skill classified as selected, deferred, or skipped with one-line reason.
- [x] Phase 8B target count is explicit and not greater than two.
- [x] Phase 8B target skill named: `contextsmith-prompt-engineer`.
- [x] ISSUE-1 resolution path documented (Option 3: extend sync script).

### Phase 8C Sub-Phases (Docs/Examples after Skill Rollout)
- [x] Phase 8C.1: Run task-state handoff workflow doc.
- [x] Phase 8C.2: Schedule with approval gates workflow doc.
- [ ] Phase 8C.3: Compare travel options workflow doc.
- [ ] Phase 8C.4: Prompt engineering example.
- [ ] Phase 8C.5: Implementation plan creation example.
- [ ] Phase 8C.6: Plan audit example.
- [ ] Phase 8C.7: Meeting scheduling example.
- [ ] Phase 8C.8: Travel comparison example.
- [ ] Phase 8C.9: Skill migration example.
- [ ] Phase 8C.10: Custom domain pack example.
- [ ] Phase 8C.11: Agent evaluation example.
- [x] `python scripts/validate_skills.py` passes.
- [x] `python scripts/token_budget.py --strict` passes.
- [x] Phase 8A Ralph loop: 2 iterations (iteration 1: no material defects; iteration 2: no-op).

## Documentation Quality
- [x] Documentation map covers first-value path, use-case lookup, examples, recovery help, and reference details.
- [x] No documentation implementation begins before the map is approved.
- [x] Map distinguishes user-facing docs from agent-facing references.
- [x] Map includes table-of-contents requirements for substantial Markdown files.
- [x] Map records website-readiness constraints (stable headings, clear page purpose, examples as website sections).
- [x] README explains the pain point, sells ContextSmith clearly, and routes readers to deeper docs.
- [x] Quickstart includes a fastest useful path and expected outputs.
- [x] Runtime workflow docs show how to create plans, run phases, validate, recover, and use domain packs.
- [x] Runtime workflow docs include non-coding examples with expected outputs.
- [x] Every substantial Markdown file has a table of contents.
- [x] Docs are website-ready Markdown with stable headings.
- [x] Docs avoid generic AI marketing and repeated contrastive phrasing.
- [x] Docs label planned/runtime features honestly.

## Final Closeout
- [ ] `TASK.md`, `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `CONTEXT.md`, `CHECKLIST.md`, `ARTIFACTS.md`, `PHASE_LOG.md`, and `NEXT_PROMPT.md` are current.
- [ ] Final report lists files changed and validation evidence.
- [ ] `NEXT_PROMPT.md` can resume the next session without chat history.
