# Engineering Metadata

Mark generated or migrated artifacts so future users and tools know how they were targeted.

Use YAML `metadata` when the target system accepts it. Otherwise add a compact body section.

Recommended fields:

```yaml
metadata:
  version: "..."
  engineered_by: local-model-agent-engineering
  engineered_version: "..."
  target_model_profiles:
    - generic-local
    - qwen36
  targeted_context_length: "32k"
  context_tier: tight
  optimization_scope: local-open-weight
  source_artifact: "..."
  last_engineered: "YYYY-MM-DD"
```

Do not add arbitrary top-level frontmatter keys. Prefer `metadata` or a human-readable `Engineering Metadata` section.

Record targeted context length when the user provides it, because it materially affects phase granularity, verbosity, examples, report size, and context strategy.
