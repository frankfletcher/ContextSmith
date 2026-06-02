# Artifact Manifest Core

Use this core reference when generating or executing artifacts. Use `artifact-manifest.md` only for full schema details, default reference matrices, or examples.

## Placement

- Generated artifacts include `## Artifact Manifest` immediately after the artifact title.
- Use ATX headings, not YAML frontmatter, inside generated artifacts.
- Put the manifest before artifact instructions so downstream agents see active constraints first.

## Required Fields

```markdown
## Artifact Manifest

**type:** prompt | implementation-plan | next-prompt | skill | instruction-file | run
**version:** 1.0
**chain-of:** root | <parent artifact id or path>

### Parameters

| Parameter | Value | Source |
|---|---|---|

### References Applied

| Reference | Version | Contract Summary |
|---|---|---|

### Behavioral Contracts

**Contract name:** One or two actionable sentences.
```

## Source Values

| Source | Meaning |
|---|---|
| `user-set` | Explicitly provided by current user |
| `inherited` | Copied from parent artifact |
| `default` | Set by SKILL.md or control parameter defaults |
| `narrowed` | Constrained for child scope; include reason |

## Propagation Rules

- Child artifacts inherit parent parameters and references unless current user overrides.
- Child artifacts may narrow context, validation, scope, or side effects with a reason.
- Do not widen context use, side effects, target model assumptions, validation strictness, or external actions without explicit current-user approval. A model-generated justification is not enough.
- Embed only concise behavioral contracts needed for standalone operation.
