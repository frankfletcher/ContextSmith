---
name: contextsmith-agent-evaluator
description: Audit prompts, skills, AGENTS.md files, repo instructions, agent workflows, model profiles, migration outputs, and long-running plans for local/open-weight model reliability without modifying them by default. Use when the user wants grades, strengths, weaknesses, A-F rubric scoring, context-risk review, loop-safety review, Git/file safety review, data science/ML safeguard review, small-model atomicity review, no-chain-of-thought validation, or targeted context fit review, upstream artifact audits, skill interoperability grading, or recommendations before using an engineer or migrator skill.
metadata:
  version: "1.7.1"
  package: ContextSmith
  target: local-open-weight-models
---

# ContextSmith Agent Evaluator

Audit prompts, skills, AGENTS.md files, agent workflows, migration outputs, and instruction packages for local/open-weight model reliability without modifying them by default.

## Quick Use

Invoke with no flags to use safe defaults. Point at any artifact and get an audit report:

```
/contextsmith-agent-evaluator
```

Defaults: `--target-profile generic-local --context-length 64k --mode audit-only --ralph 1 --output chat`. The target profile is inferred from your agent harness when available. Provide flags or natural-language instructions to override.

## Help Mode

If the user invokes this skill with `help`, `describe`, `examples`, `modes`, `parameters`, `quickstart`, or CLI-style equivalents such as `--help`, do not run the normal workflow.

Return the requested usage guidance from `references/help.md` and `references/help-mode.md`.

## Control Parameter Parsing

Accept both natural-language controls and CLI-style flags. Use `references/control-parameters-core.md` for routine parsing and `references/control-parameters.md` only for the full flag catalog.

When `--harness opencode` is specified, load `references/harness-opencode.md` for opencode-specific agent, command, tool, and plugin configurations.

Examples:

```bash
--mode deep --target-profile qwen36 --context-length 32k --domain coding --harness opencode --ralph 2 --output project-local --no-apply
```

When CLI flags and prose conflict, prefer explicit current-user prose or ask one concise clarification question if the intended priority is unclear.

## Default Mode

Audit-only. Do not edit files unless the user explicitly asks.

## Targeted Context and Interoperability Checks

When evaluating an artifact, grade targeted context fit using `references/targeted-context-length.md` and skill interoperability using `references/skill-interoperability.md`.

Check whether upstream tools or skills introduced unsupported requirements, duplicate workflows, conflicting instructions, or hallucinated dependencies. Recommend rejection or downgrade of unsupported additions.



## Model Capability and Planner/Executor Profiles

When the user provides `--target-capability`, `--planner-profile`, or `--executor-profile`, load `references/model-capability-tiers.md` and `references/planner-executor-workflows.md`.

Use stronger/planner profiles for planning, audits, architecture, test strategy, and final review. Use smaller/executor profiles for atomic phase execution when the plan and task state are explicit.



## Education Level and Artifact Verbosity

If the user provides `--education-level` or `--artifact-verbosity`, load `references/education-levels.md`.

Keep model-facing artifacts compact when `targeted_context_length` is tight. Put teaching detail in separate reports instead of bloating prompts, skills, AGENTS.md files, or phase instructions.



## Implementation Plan, Test, and Phase Review Audits

When generating or auditing coding plans, tests, or phase workflows, use:

- `references/implementation-plan-audit.md`
- `references/test-quality-audit.md`
- `references/phase-code-review.md`
- `references/small-context-workflows.md`
- `references/phased-planning.md`
- `references/persistent-task-state.md`
- `references/output-location.md`

For coding domains, implementation plans should include test strategy, code review gates, and phase debriefs. Tests should be audited for usefulness, not just pass/fail status.

When auditing implementation plans, planner prompts, generated skills, or repo instruction files for long-running, multi-file, migration, release, refactor, validation-heavy, or coding work, grade whether persistent task state is concrete. A passing artifact must make the work resumable from files, not from chat memory. Flag as a high-risk issue when the artifact only describes a "Persistent Task State" section but does not require or create `TASK.md`, `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `CONTEXT.md`, `CHECKLIST.md`, `ARTIFACTS.md`, `PHASE_LOG.md`, and `NEXT_PROMPT.md` in a canonical `.agent_work/sprints/.../tasks/.../` directory.

For planning-only workflows, verify that the artifact distinguishes allowed planning artifacts from forbidden source-code edits. For phased execution, verify that each closeout refreshes state files and `NEXT_PROMPT.md`.

Also grade state hygiene. The artifact should require compact, factual state files containing paths, commands, validation results, decisions, constraints, and next actions. Penalize artifacts that encourage raw transcript dumps, full logs, full source copies, or hidden reasoning in task state. Treat a missing or vague `NEXT_PROMPT.md` handoff as a context-continuity failure.


## Run Configuration Preview

For audit-only work (read-only), confirmation is optional — proceed with the audit unless the user asks to review first.

For any work that modifies files (e.g., applying fixes after audit), summarize parameters and plan, then ask the user to confirm before proceeding. This is the default behavior — do not skip it unless the user explicitly opts out (`--mode yolo`, "just do it", "skip confirmation").

Use `references/run-configuration-preview.md` for the confirmation format when modifications are involved.

## Workflow

Use `reference_manifest.yml` to determine which references to load. References with `load: always` are loaded on every invocation. References with `load: conditional` are loaded only when the `when` condition is met. References with `load: never` are called (not read into context).

1. Identify artifact type: prompt, skill, instruction file, workflow, model profile, migration output, phase plan.
2. Select target model profile or use `generic-local`.
3. Detect domain intent and side-effect risk using `domain-intent.md` and `side-effect-matrix.md`.
4. Inspect existing safeguards and duplicate rules using `instruction-deduplication.md`.
5. Evaluate context strategy, persistent task state, subagent use, assumptions, loop safety, Git/file safety, and no exposed chain-of-thought.
6. For coding or repo artifacts, check coding standards, validation evidence, Git safety, and gitignore hygiene.
7. For data science/ML/AI artifacts, check leakage prevention, evaluation, reproducibility, artifact handling, and modality-specific rules.
8. Grade each dimension A-F using `evaluation-rubrics.md`.
9. Recommend improvements in priority order.
10. State whether a Ralph loop, prompt engineer, skill engineer, instruction engineer, or migrator should be used next.



## Runtime Validation

Validate audited artifacts with `python -m runtime.cli <subcommand> <artifact.json>`. Subcommands: `requirements`, `phase-contract`, `evidence`, `approval`, `closeout`, `domain-pack`. Exit codes: `0` pass, `1` violations, `2` error. Domain packs under `runtime/domain_packs/`. Use `--validation none` to opt out. If runtime module unavailable, record blocker.

## Runtime Stability Notes

If the user asks about local model loops, server settings, speculative decoding, KV cache precision, or long agentic coding instability, use `references/runtime-stability.md`. Treat runtime settings as experimental deployment guidance unless the harness can control them.

## Required Output

```markdown
## Summary Grade
## Strengths
## Weaknesses
## A-F Rubric
| Dimension | Grade | Reason | Recommended Fix |
## Loop / Git / Context Safety
## Domain-Specific Risks
## Duplicate or Conflicting Instructions
## High-Risk Issues
## Suggested Next Action
```

Use constructive critique. Do not rewrite the artifact unless requested.


## Documentation Quality

When generating or editing README material, user guides, educational reports, AGENTS.md explanations, or other reader-facing documentation, use `references/documentation-quality.md`. Keep generated artifacts factual, practical, and easy to act on. Avoid overused generated-writing patterns, unsupported claims, and unnecessary imperatives in user documentation.

Support `--focus documentation-quality` for README/docs/user-guide audits.
