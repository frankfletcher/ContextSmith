# ContextSmith Examples

These examples are meant to be copied, edited, and reused. You do not need every flag. Start with the closest example and remove what you do not need.

## Prompt engineering examples

### Optimize a prompt for Qwen3.6 under tight context

```bash
/local-model-prompt-engineer \
  --mode deep \
  --target-profile qwen36 \
  --context-length 32k \
  --domain coding \
  --artifact-verbosity compact \
  --education-level guided \
  --ralph 2
```

Use this when the prompt will drive a local coding agent or be reused.

Benefit: the model-facing prompt stays compact, while the human gets a useful explanation of what changed and why.

### Fast cleanup of a general prompt

```bash
/local-model-prompt-engineer \
  --mode fast \
  --target-profile generic-local \
  --no-ralph
```

Use this when you want a cleaner prompt without a full audit.

Benefit: low friction, minimal report, no iteration overhead.

### Build a prompt package for long document work

```bash
/local-model-prompt-engineer \
  --mode guided \
  --target-capability small-local \
  --context-length 64k \
  --domain document-processing \
  --output project-local
```

Use this when the prompt will operate on long documents, logs, transcripts, or retrieved context.

Benefit: adds source separation, evidence anchors, chunking or staged processing, and final task re-anchoring.

## AGENTS.md and repo instruction examples

### Create AGENTS.md for a Python data-science repo

```bash
/local-model-instruction-engineer \
  --project . \
  --mode guided \
  --target-profile qwen36 \
  --context-length 32k \
  --domain coding,data-science-ml \
  --harness opencode
```

Use this when you want repo-specific instructions for local agentic coding.

Benefit: scans the repo, proposes relevant instruction blocks, avoids duplicate safeguards, and adds data-science/ML guidance only when relevant.

### Improve existing AGENTS.md without duplicating safeguards

```bash
/local-model-instruction-engineer \
  --project . \
  --mode guided \
  --focus agents-md \
  --target-profile generic-local \
  --context-length 64k
```

Use this when your repo already has instruction files.

Benefit: detects existing loop safety, Git safety, context rules, coding standards, and strengthens only what is missing or vague.

### Create concise instructions for a small executor model

```bash
/local-model-instruction-engineer \
  --project . \
  --mode guided \
  --executor-profile qwen36 \
  --context-length 32k \
  --artifact-verbosity compact \
  --phase-review standard
```

Use this when a smaller model will carry out coding phases.

Benefit: produces compact repo instructions with loop safety, Git safety, phase closeout, and atomic execution guidance.

## Evaluation examples

### Audit an implementation plan

```bash
/local-model-agent-evaluator \
  --mode audit-only \
  --focus implementation-plan \
  --target IMPLEMENTATION_PLAN.md \
  --executor-profile qwen36 \
  --context-length 32k \
  --education-level guided
```

Use this before handing a plan to a smaller coding model.

Benefit: catches phases that are too broad, missing stop conditions, missing task memory, or unlikely to fit the targeted context length.

### Audit test quality

```bash
/local-model-agent-evaluator \
  --mode audit-only \
  --focus test-quality \
  --target tests/ \
  --domain coding \
  --education-level guided
```

Use this when tests pass but you want to know if they are meaningful.

Benefit: identifies weak assertions, fake edge cases, over-mocking, and tests that do not catch realistic regressions.

### Audit runtime stability notes

```bash
/local-model-agent-evaluator \
  --mode audit-only \
  --focus runtime-stability \
  --target ./runtime-notes.md \
  --target-profile qwen36 \
  --context-length 64k
```

Use this when tuning a local model runtime for long agentic coding.

Benefit: encourages one-variable-at-a-time experiments instead of folklore-driven config swaps.

## Skill engineering examples

### Convert one skill for local models

```bash
/local-model-skill-engineer \
  --source ./skills/my-skill/SKILL.md \
  --mode guided \
  --target-profiles generic-local,qwen36 \
  --context-length 32k \
  --reference-policy optimize \
  --output staging
```

Use this when converting a skill without changing its intended behavior.

Benefit: extracts the source contract, preserves commands/references, rejects unsupported additions, and reports a semantic diff.

### Audit a skill without editing

```bash
/local-model-skill-engineer \
  --source ./skills/my-skill/SKILL.md \
  --mode audit-only \
  --target-profile generic-local
```

Use this before deciding whether to convert.

Benefit: shows whether the skill actually needs changes.

## Skill migration examples

### Stage a safe migration of installed skills

```bash
/local-model-skill-migrator \
  --skills-dir ~/.agents/skills \
  --mode review-gate \
  --target-profiles generic-local,qwen36 \
  --context-length 32k \
  --backup \
  --stage \
  --no-apply
```

Use this when you want a batch migration but do not want in-place edits.

Benefit: creates a backup, staging directory, manifest, reports, and restore notes.

### Audit a skills directory only

```bash
/local-model-skill-migrator \
  --skills-dir ~/.agents/skills \
  --mode audit-only \
  --target-profile generic-local
```

Use this when you want to know which skills are risky, stale, or poorly suited for local models.

Benefit: no edits, just an inventory and recommendations.
