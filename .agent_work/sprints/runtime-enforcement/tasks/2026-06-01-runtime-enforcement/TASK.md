# Task: Runtime Enforcement for ContextSmith Skills

## Artifact Manifest

- artifact_type: task-state
- parent_request: Create an implementation plan for deterministic runtime behavior enforcement in installed ContextSmith skills.
- target_profile: qwen36 (default)
- harness: opencode (default)
- context_length: 64k (default)
- mode: guided (default)
- ralph: 2 (default)
- references: AGENTS.md, contextsmith-prompt-engineer, persistent task state, phased planning, implementation plan audit, git safety
- behavioral_contract: Keep work resumable from files; do not rely on chat memory; validate with evidence before reporting completion.

## Objective
Plan the work needed to make ContextSmith skill behavior more deterministic at runtime after skills are installed and used outside this repository.

## Problem Statement
Current runtime enforcement is mostly instruction-based. Installed skills ship as `SKILL.md`, `help.md`, `reference_manifest.yml`, and `references/`, so user-facing behavior depends on the model reading and following natural-language obligations. Repository-local validators check package structure but do not enforce behavior during real skill use.

## Scope

- Design a runtime enforcement architecture that works when users install ContextSmith skills.
- Keep the implementation plan executable by small/local models through atomic phases and explicit review gates.
- Generalize the runtime protocol for skills, agents, and prompts across many domains, not only coding.
- Support domain packs for domain-specific validation and approval boundaries.
- Prefer deterministic validators over self-audit prose.
- Provide a portable CLI path and an MCP path using shared validation logic.
- Consider an orchestrated runner as workflow-level enforcement, while clearly labeling bypass limits.
- Identify harness-gated enforcement opportunities for opencode without making them the only path.
- Produce an implementation plan before code changes.

## Out of Scope

- Implementing the runtime validator in this planning task.
- Editing `PACKAGE_SPEC.md` without explicit approval.
- Adding new dependencies without explicit approval, except pytest is pre-approved by current user for test phases.
- Removing or renaming existing skills.
- Claiming hard enforcement where the harness can only provide advisory tool output.

## Success Criteria

- All sprint artifacts are present in this task directory.
- `PLAN.md` defines atomic phases with inputs, actions, outputs, validation, and closeout gates.
- The plan distinguishes deterministic validation from harness-enforced blocking.
- The plan distinguishes deterministic validation, orchestrated workflow enforcement, harness hard blocking, and human approval.
- The first implementation phase verifies packaging and installation constraints before design-changing edits.
- Universal artifacts and starter domain packs support coding, writing, research, scheduling, travel/purchase, and general fallback tasks.
- A future session can resume from `NEXT_PROMPT.md` without the original chat transcript.
