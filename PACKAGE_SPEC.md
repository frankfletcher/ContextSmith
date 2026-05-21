# Package Spec

## Goal

Provide a coherent toolkit for engineering agent-facing instructions for local/open-weight models.

## Non-Goals

- Do not force one model family on all artifacts.
- Do not automatically apply destructive changes.
- Do not use exposed chain-of-thought prompting.
- Do not turn persistent state into a junk drawer.

## Shared Components

- model profiles
- domain intent profiles
- context management
- persistent task state
- subagent delegation
- Ralph loop
- evaluation rubrics
- phased planning
- engineering metadata
- educational reporting

## Versioning

- Existing generalized skills advance to v1.3.
- Migrator advances to v1.1.
- New instruction/evaluator skills start at v1.0.

## Future Backlog

- model profile builder
- harness adapter for OpenCode/OpenClaw/Hermes/etc.
- task-state manager
- package sync script for shared references
- richer examples and test fixtures
