# ContextSmith User Manual

This manual expands on the README. The README is the quick-start landing page; this file is the deeper guide.

## Core Idea

ContextSmith engineers prompts, skills, AGENTS.md files, implementation plans, and agent workflows around the model and context you actually have.

Use it to:

- optimize prompts for local/open-weight models
- create or improve SKILL.md-based skills
- safely migrate skill directories
- create repo-aware AGENTS.md files
- audit prompts, tests, plans, workflows, and instruction files

## Recommended Workflow

1. Pick the right skill.
2. Specify target profile or capability.
3. Specify `targeted_context_length`.
4. Choose mode: fast, deep, guided, review-gate, or audit-only.
5. Select domain and harness when relevant.
6. Use project-local output for durable artifacts.
7. Use audit/evaluator before high-risk changes.

See `CONTROL_PARAMETERS.md` and `EXAMPLES.md` for copy-paste invocations.
