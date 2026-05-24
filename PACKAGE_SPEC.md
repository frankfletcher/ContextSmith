# Package Spec

## Name

Local Model Agent Engineering Skills

## Version

v1.4.2

## Thesis

Local and smaller open-weight models do best when instructions are explicit, staged, validated, context-aware, loop-safe, and durable across interruptions. Artifacts must also be sized and structured for the user's targeted context length, not the model card maximum.

## Core Skills

- `local-model-prompt-engineer`
- `local-model-skill-engineer`
- `local-model-skill-migrator`
- `local-model-instruction-engineer`
- `local-model-agent-evaluator`

## Shared Principles

- Preserve the user's real objective.
- Optimize for the selected model profile and targeted context length.
- Ask only when blocked or when the answer materially changes the output.
- Detect upstream skill/tool artifacts and reject unsupported requirements.
- Resolve conflicts using instruction precedence.
- Prefer atomic instructions, checklists, and validation gates.
- Avoid exposed chain-of-thought instructions.
- Use context management, persistent state, subagents, and phase debriefs when complexity warrants them.
- Avoid duplicated safeguards and token bloat.
- Use review-gate mode for destructive, external, or batch actions.

## Packaging

Use Option C: canonical shared references plus copied per-skill references for standalone installation.


## Parameterization and Help Mode

All skills support both natural-language controls and CLI-style flags. The canonical parser reference is `shared/control-parameters.md`; user-facing discovery is provided by `shared/help-mode.md` and per-skill `references/help.md` files.

Every skill must support: `help`, `describe`, `examples`, `modes`, `parameters`, and `quickstart`, plus CLI-style equivalents such as `--help` and `--examples`.

CLI-style flags are not a separate runtime implementation. They are a compact instruction convention for agent skills and a future-compatible interface for a possible `contextsmith` CLI/UI.

## v1.4.0 Design Additions

- Add implementation-plan audit as a first-class evaluation focus.
- Add test-quality audit for agent-generated tests.
- Add phase code review as a post-phase coding gate.
- Add `education-level` and `artifact-verbosity` as separate controls.
- Add model capability tiers and planner/executor profile split.
- Add runtime stability guidance for long local agentic coding runs.
- Rewrite README as a landing page and move the long manual into `docs/`.
- Adopt SemVer-style versioning going forward without renumbering history.

## Project Documentation vs Agent References

ContextSmith keeps two documentation layers:

- `docs/` contains project documentation: onboarding, guides, examples, concepts, workflow guides, and reference material for users.
- `shared/` and `skills/*/references/` contain concise agent reference material used by the skills.

The README should remain a project landing page and quick orientation path, not a complete manual. Detailed usage belongs in `docs/`.


## v1.4.2 Design Additions

- Add run configuration previews so generated skills can show inferred parameters before important work.
- Add documentation-quality review for user guides, README updates, AGENTS.md explanations, and educational reports.
- Keep project documentation warm, practical, and factual while keeping agent references concise and operational.
- Organize docs into `workflows/`, `concepts/`, `reference/`, and `contributing/` sections where appropriate.
- Avoid overused AI-sounding contrast patterns and avoid language that implies the user needs hand-holding.
