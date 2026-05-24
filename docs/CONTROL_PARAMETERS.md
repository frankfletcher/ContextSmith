# Control Parameters

ContextSmith accepts both natural language and CLI-style controls.

## Common Flags

```bash
--mode fast|deep|guided|yolo|review-gate|audit-only
--target-profile qwen36|gemma4|llama3|generic-local
--target-profiles generic-local,qwen36
--target-capability small-local|mid-local|large-local|frontier-cloud|reasoning-specialized|coding-specialized|multimodal
--planner-profile frontier-cloud
--executor-profile qwen36
--context-length 32k
--domain coding,data-science-ml
--harness opencode
--ralph 2
--education-level none|brief|guided|deep|teaching
--artifact-verbosity compact|normal|detailed
--phase-review off|brief|standard|deep
--code-review-iterations 0|1|2
--output chat|project-local|staging
--backup
--stage
--no-apply
```

## Natural Language Equivalents

- “deep path”
- “guided mode”
- “target profile: qwen36”
- “targeted context length: 32k”
- “education level: deep”
- “artifact verbosity: compact”
- “phase review: standard”

## Conflict Handling

If prose conflicts with flags, the user’s current explicit prose wins unless ambiguous. Ask one concise clarification question only when the conflict materially changes the output or safety boundary.
