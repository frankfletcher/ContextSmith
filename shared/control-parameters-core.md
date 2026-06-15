# Control Parameters Core

Use this core reference for routine parsing. Use `control-parameters.md` only for the full flag catalog, examples, or skill-specific flag discovery.

## Parse Rules

1. Parse CLI-style flags and natural-language controls.
2. Normalize aliases before applying behavior.
3. Latest explicit current-user instruction wins over inherited or older artifact values.
4. If flags and prose conflict and priority is unclear, ask one concise question only when the conflict changes side effects, output location, target model/profile, domain, validation, permission boundaries, or output format.
5. Record important active controls in the artifact manifest, evidence ledger, assumptions, or audit section.

## Confirmation Default

**Confirmation before execution is the default.** Every skill that performs file changes, multi-step work, or side effects must summarize parameters and plan, then ask the user to confirm before proceeding.

Opt-out:

- `--mode yolo` — skip all confirmations
- `--no-preview-config` — skip the parameter/plan preview
- `--interaction silent` — ask only when blocked or unsafe
- Natural language: "just do it", "don't ask", "skip confirmation"

See `run-configuration-preview.md` for the confirmation format and rules.

## Core Aliases

| Alias | Normalized control |
| --- | --- |
| `--ctx` | `--context-length` |
| `--no-ralph` | `--ralph 0` |
| `silent-unless-blocked` | `silent` |
| `--preview-config` | `--review-config` |
| `--no-preview-config` | `--no-review-config` |

## Conflict Examples

- `--mode yolo` plus "ask before changes": require guided/review-gate behavior unless user confirms YOLO.
- `--apply` plus "do not apply": do not apply; ask before applying.
- `--context-length 32k` plus "use full 128k": ask which budget to target.

## Education and Verbosity

If `--education-level deep` conflicts with `--artifact-verbosity compact`, keep model-facing artifacts compact and put teaching detail in a separate report.
