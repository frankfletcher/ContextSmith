# Model Capability Tiers

ContextSmith is small/local-model-first, but its operational discipline applies across model sizes. Use capability tiers to adapt artifact shape to the model's actual operating envelope.

## Core Principle

ContextSmith is model-aware agent instruction engineering. It started with small local models, where instruction quality matters most, but the same discipline improves larger-model agent workflows too.

## Tiers

### small-local

Examples: smaller local/open-weight models, quantized models, constrained VRAM, tight context.

Use:
- atomic steps
- more phases
- compact artifacts
- fewer examples
- strict output contracts
- persistent task state
- loop safety
- explicit validation

### mid-local

Use:
- moderate phase size
- compact but less micro-managed instructions
- selective references
- persistent state for long tasks

### large-local

Use:
- richer context when justified
- still avoid full-repo dumps
- maintain loop/Git safety and validation gates

### frontier-cloud

Use:
- broader planning and synthesis
- richer tradeoff analysis
- fewer but more substantial phases when context permits
- still maintain safety, evidence, and side-effect boundaries

### reasoning-specialized

Use for:
- architecture planning
- debugging hypotheses
- implementation plan audits
- risk analysis
- semantic diffs
- test strategy

Do not request exposed chain-of-thought by default. Request concise rationale, decision criteria, tests, and verification.

### coding-specialized

Use for:
- repo edits
- code review
- test generation
- refactoring
- build/test diagnosis

Require Git safety, test-quality audit, and post-phase code review when relevant.

### multimodal

Use model/runtime-specific profile guidance for media order, visual token budget, OCR/chart/table handling, and evidence anchors.

## Metadata

Generated artifacts may include:

```yaml
metadata:
  target_model_profiles:
    - qwen36
  target_model_capability: small-local
  targeted_context_length: 32k
  context_tier: tight
```
