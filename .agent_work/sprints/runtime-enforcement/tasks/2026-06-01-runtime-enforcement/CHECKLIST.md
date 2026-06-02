# Checklist: Runtime Enforcement for ContextSmith Skills

## Artifact Manifest
- artifact_type: checklist
- parent_task: TASK.md
- validation_level: planning strict; implementation available checks
- behavioral_contract: Use this checklist during phase closeout and final audit.

## Planning Quality
- [x] Problem is scoped to installed-skill runtime behavior, not repo-local validation only.
- [x] Plan separates deterministic validation from hard harness enforcement.
- [x] Plan includes CLI and MCP paths using shared validation logic.
- [x] Plan starts with packaging discovery before design-changing edits.
- [x] Plan includes validation evidence and task-state updates in every phase.
- [x] Tool-heavy phases include context contracts, compaction triggers, and stop rules.
- [x] Rollout is split into scope selection and per-batch execution.
- [x] Distribution model decision occurs before implementation.
- [x] Plan separates small-model implementation phases from human/frontier architecture review gates.
- [x] Plan supports general skill, agent, and prompt use cases beyond coding.
- [x] Plan labels deterministic validation, orchestrated workflow enforcement, harness hard blocking, and human approval separately.
- [x] Plan includes explicit recovery procedure for blocked phases.
- [x] Plan requires per-phase closeout updates to STATUS.md, PHASE_LOG.md, ARTIFACTS.md, and NEXT_PROMPT.md.
- [x] Phase 7 rollout is bounded by an exact skill count selected in Phase 7A.
- [x] Documentation workstream prioritizes how to use ContextSmith over architecture explanation.
- [x] Documentation plan includes README, quickstart, use-case workflows, examples, and quality audit before rollout.
- [x] Next Prompt Compiler is planned before the orchestrated runner.

## Implementation Safety
- [ ] Packaging behavior verified from source or built artifacts.
- [ ] Distribution model recorded before implementation begins.
- [ ] No dependency added without approval.
- [ ] No `PACKAGE_SPEC.md` design edit made without approval.
- [ ] No user-level opencode config modified without approval.
- [ ] Skill changes validated with `python scripts/validate_skills.py`.
- [ ] Skill/reference changes validated with `python scripts/token_budget.py --strict`.
- [ ] Rollout batch size stays within approved scope.
- [ ] Small-model phases do not require broad architecture decisions.
- [ ] Pytest is used only for approved runtime/test phases.
- [ ] Blocked phases use the recovery procedure before any next-phase work begins.
- [ ] Phase closeout records carry-forward and do-not-carry-forward notes.
- [ ] Next Prompt Compiler does not execute phases, call models, or advance task state beyond writing handoff prompts.

## Runtime Enforcement Quality
- [ ] Validator checks are executable and deterministic.
- [ ] Validator output has stable exit codes or structured MCP results.
- [ ] Artifacts expose machine-readable fields for validation.
- [ ] Advisory validation and hard blocking are clearly labeled.
- [ ] Pilot workflow demonstrates a passing and failing runtime check.
- [ ] Fixture set covers baseline, missing-field, widened-parameter, missing-evidence, and failed-closeout cases.
- [ ] Sample installed-skill workflow proves the validator can run outside the repo-local planning context.
- [ ] Universal protocol validates requirements chains, phase contracts, evidence ledgers, approval records, and closeouts.
- [ ] Starter domain packs cover software, writing, research, scheduling, travel/purchase, and general fallback.
- [ ] Orchestrated runner claims are limited to workflow-level enforcement unless a harness hard-block is proven.
- [ ] Installed-workflow smoke test records a fallback path if packaging cannot carry runtime files.
- [ ] Harness adapter design includes positive completion criteria, not only stop rules.
- [ ] Generated next prompts include validation, audit, closeout, recovery, and hard-stop sections.
- [ ] Generated next prompts render cleanly as Markdown with balanced fences.

## Documentation Quality
- [ ] README explains the pain point, sells ContextSmith clearly, and routes readers to deeper docs.
- [ ] Quickstart includes a fastest useful path and expected outputs.
- [ ] Use-case docs show how to create plans, run phases, validate, recover, and use domain packs.
- [ ] Examples cover coding and non-coding workflows.
- [ ] Every substantial Markdown file has a table of contents.
- [ ] Docs are website-ready Markdown with stable headings.
- [ ] Docs avoid generic AI marketing and repeated contrastive phrasing.
- [ ] Docs label planned/runtime features honestly.

## Final Closeout
- [ ] `TASK.md`, `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `CONTEXT.md`, `CHECKLIST.md`, `ARTIFACTS.md`, `PHASE_LOG.md`, and `NEXT_PROMPT.md` are current.
- [ ] Final report lists files changed and validation evidence.
- [ ] `NEXT_PROMPT.md` can resume the next session without chat history.
