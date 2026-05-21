# Control Phrases and CLI-Style Parameters

ContextSmith supports both natural-language controls and CLI-style flags. Use either style; CLI-style flags are easiest to repeat and copy into README examples.

## Natural-Language Controls

- `fast path`: concise one-pass improvement; minimal questions and reports
- `deep path`: stronger analysis, richer audit, optional Ralph loop, saved iterations when useful
- `guided mode`: ask 1-3 high-impact questions before major choices
- `yolo mode`: proceed with reasonable assumptions unless blocked
- `review-gate mode`: plan or stage first; ask before applying changes
- `audit only`: analyze and report; do not modify files
- `stage only`: write output to staging; do not overwrite originals
- `apply`: apply already-staged changes after approval
- `no ralph loop`: disable iterative refinement
- `ralph loop: 2`: run up to two Ralph iterations
- `target profile: qwen36`: use one model profile
- `target profiles: generic-local, qwen36`: optimize for multiple profiles
- `context length: 32k`, `targeted context length: 32k`, `ctx: 32k`: optimize for actual local context budget
- `domain: coding,data-science-ml`: apply domain-specific rules
- `harness: opencode`: apply harness-aware guidance when known
- `project-local output`: use `<project>/.agent-work/` for durable artifacts
- `chat-only output`: return in chat; avoid writing files unless needed
- `backup first`: back up before edits or migrations
- `do not apply`: do not overwrite originals or perform in-place changes

## CLI-Style Equivalent

```bash
--mode deep \
--target-profile qwen36 \
--context-length 32k \
--domain coding,data-science-ml \
--harness opencode \
--ralph 2 \
--output project-local \
--no-apply
```

See `control-parameters.md` for full parsing rules and per-skill flags.
