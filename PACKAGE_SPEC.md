# Package Spec

Package: `local-model-agent-engineering`  
Version: `1.1`

## Goal

Provide a cohesive set of agent skills for engineering prompts, skills, migrations, evaluations, and repo instruction files for local/open-weight models.

## Non-Goals

- Do not guarantee model capability.
- Do not bypass harness limitations.
- Do not automate destructive Git, financial, external-write, or production actions without explicit approval.
- Do not require every task to use Ralph loops, task state, or subagents.

## Skills

- `local-model-prompt-engineer`
- `local-model-skill-engineer`
- `local-model-skill-migrator`
- `local-model-instruction-engineer`
- `local-model-agent-evaluator`

## Shared Principles

- atomic small-model instructions
- no exposed chain-of-thought
- model and domain profiles
- context engineering
- loop prevention
- Git/file safety
- persistent task state for long work
- phase compression and do-not-carry-forward notes
- bounded Ralph improvement loop
- educational change reports
- progressive disclosure
- standalone-installable skills
