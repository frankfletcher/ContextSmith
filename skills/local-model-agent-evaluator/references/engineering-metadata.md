# Engineering Metadata

Mark generated or modified artifacts so future agents can identify target model/profile and engineering policy.

## For SKILL.md Files

Use `metadata` frontmatter when the target skill system allows it:

```yaml
metadata:
  version: "1.3"
  engineered_by: local-model-skill-engineer
  engineered_version: "1.3"
  target_model_profiles:
    - generic-local
    - qwen36
  optimization_scope: local-open-weight
  last_engineered: "YYYY-MM-DD"
```

If frontmatter metadata is not allowed, add a compact body section instead.

## For Prompt Packages

Include:

```markdown
## Engineering Metadata
- Engineered by:
- Engineer version:
- Target model/profile:
- Optimization scope:
- Runtime settings controllable by this prompt: yes/no/unknown
```

## For Batch Migrations

Record authoritative metadata in `MANIFEST.json`: source hash, converted hash, profile, status, risk, validation result, and modified files.
