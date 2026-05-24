# Model Profiles and Capability Tiers

ContextSmith is small/local-model-first, but it supports model-aware instruction generation through profiles and capability tiers.

Use specific profiles when known:

- `qwen36`
- `gemma4`
- `llama3`
- `generic-local`

Use capability tiers when a specific profile is not enough:

- `small-local`
- `mid-local`
- `large-local`
- `frontier-cloud`
- `reasoning-specialized`
- `coding-specialized`
- `multimodal`

See `shared/model-capability-tiers.md` for details.
