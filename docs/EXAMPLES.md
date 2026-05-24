# ContextSmith Examples

## Optimize a prompt for a tight local coding model

```bash
/local-model-prompt-engineer   --mode deep   --target-profile qwen36   --context-length 32k   --domain coding   --harness opencode   --ralph 2   --education-level guided   --artifact-verbosity compact   --output project-local
```

Benefit: compact model-facing prompt, stronger report for the human, saved iterations.

## Create AGENTS.md for a Python data-science repo

```bash
/local-model-instruction-engineer   --project .   --mode guided   --target-profile qwen36   --context-length 32k   --domain coding,data-science-ml   --harness opencode   --phase-review standard
```

Benefit: repo-aware instructions with Git safety, loop safety, PEP 8, ML leakage prevention, test-quality guidance, and phase closeout.

## Audit an implementation plan before giving it to a small model

```bash
/local-model-agent-evaluator   --mode audit-only   --focus implementation-plan   --target IMPLEMENTATION_PLAN.md   --executor-profile qwen36   --context-length 32k
```

Benefit: catches plans that are too broad, insufficiently atomic, or missing phase memory.

## Audit tests for usefulness

```bash
/local-model-agent-evaluator   --mode audit-only   --focus test-quality   --target tests/   --domain coding   --education-level guided
```

Benefit: identifies performative tests, missing edge cases, weak assertions, and over-mocking.

## Migrate installed skills safely

```bash
/local-model-skill-migrator   --skills-dir ~/.agents/skills   --mode review-gate   --target-profiles generic-local,qwen36   --context-length 32k   --backup   --stage   --no-apply
```

Benefit: backs up first, stages changes, writes reports, and avoids in-place overwrite.
