# Control Phrases

Use these phrases to steer the skills. They may be combined naturally.

## Modes

- `fast path`: concise one-pass improvement; minimal questions and reports
- `deep path`: stronger analysis, richer audit, optional Ralph loop, saved iterations when useful
- `guided mode`: ask 1-3 high-impact questions before major choices
- `yolo mode`: proceed with reasonable assumptions unless blocked
- `review-gate mode`: plan/stage first; ask before applying changes
- `audit only`: analyze and report; do not modify files
- `stage only`: write output to staging; do not overwrite originals
- `apply`: apply already-staged changes after validation and approval

## Model / Harness / Domain

- `target profile: qwen36`
- `target profiles: generic-local, qwen36`
- `target model: Gemma 4 26B A4B`
- `harness: opencode`
- `domain: coding`
- `domain: data-science-ml`

## Context and Output

- `targeted context length: 32k`
- `context length: 64k`
- `project-local output`
- `chat-only output`
- `backup first`
- `do not apply`
- `no ralph loop`
- `ralph loop: 2`

## Recommended Defaults

- Important reusable artifact: `guided mode`
- Big/reusable/high-risk artifact: `deep path`
- Batch migration: `review-gate mode`, `stage only`, `backup first`
- Diagnosis before mutation: `audit only`
- Project work: `project-local output`
