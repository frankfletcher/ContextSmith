# Package Spec

## Name

ContextSmith Skills

## Version

v1.7.1

## Thesis

ContextSmith is local/open-weight first: smaller models do best when instructions are explicit, staged, validated, context-aware, loop-safe, and durable across interruptions. The same discipline also improves frontier-model agent workflows. Artifacts must be sized and structured for the user's targeted context length, not the model card maximum.

## Core Skills

- `contextsmith-prompt-engineer`
- `contextsmith-skill-engineer`
- `contextsmith-skill-migrator`
- `contextsmith-instruction-engineer`
- `contextsmith-agent-evaluator`
- `contextsmith-orchestrator`
- `contextsmith`

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

## v1.7.0 Design Additions

- Rename public skill entry points from `local-model-*` to `contextsmith-*` to align the package surface with the project name.
- Add `contextsmith` as the top-level router skill for discovery and intent-based dispatch.
- Keep the methodology local/open-weight first while documenting that the practices transfer to frontier-model agents.
- Treat `contextsmith-orchestrator` as the unified execution skill (absorbed contextsmith-run).

## v2.0.0 Design Decisions

- Move to project-level versioning. After the determinism sprint, all ContextSmith skills move to 2.0.0.
- Per-skill version metadata is deprecated in favor of the single project version in PACKAGE_SPEC.md.
- Individual skills may still carry `metadata.version` in SKILL.md frontmatter, but it should match the project version and is no longer independently meaningful.
- Version 2.0.0 applied in Phase 6e — contextsmith-run removed, orchestrator absorbed its patterns.
- See `docs/reference/VERSIONING.md` for the full versioning policy.
