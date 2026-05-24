# AGENTS.md Guide

AGENTS.md is the operating backbone of an agentic coding project. Treat it as a high-impact artifact.

## Recommended Defaults

- Use guided mode by default for creating or rewriting AGENTS.md.
- Scan the repo before adding rules.
- Scan existing instruction files before injecting safeguards.
- Add only relevant, non-duplicative instruction blocks.
- Keep project-facing rules concise and testable.

## Common Blocks

- Project overview
- Setup/build/test/lint commands
- Coding standards
- Git safety
- Loop safety
- Context management
- Persistent task state
- Phase debrief
- Code review and test-quality gates
- Domain-specific standards
- `.agent-work/` gitignore suggestion

## Anti-Patterns

- Generic manifestos
- Duplicate safety rules
- Long philosophy sections
- Commands not verified from the repo
- Destructive Git permissions
- Exposed chain-of-thought requests
- Raw logs or generated artifacts committed to the repo
