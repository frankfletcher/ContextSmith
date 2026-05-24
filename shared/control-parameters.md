# Control Parameters

ContextSmith skills accept both natural-language controls and CLI-style flags. CLI-style flags are recommended for repeatable workflows and future CLI/UI compatibility.

## Parsing Rules

1. Parse CLI-style flags first.
2. Treat explicit user prose as higher priority when it clearly contradicts a flag.
3. If a flag and prose conflict and the intended priority is unclear, ask one concise clarification question.
4. Normalize aliases before applying behavior.
5. Record important parsed controls in the output under `Assumptions`, `Engineering Metadata`, or the relevant audit section.

## Common Flags

```bash
--mode fast|deep|guided|yolo|review-gate|audit-only
--target-profile qwen36|gemma4|llama3|generic-local
--target-profiles generic-local,qwen36
--context-length 32k|64k|100k|128k|256k
--targeted-context-length 32k
--ctx 32k
--domain coding,data-science-ml,frontend,research,email,document-processing
--harness opencode,codex,cursor,aider,openclaw,hermes,generic-agent
--ralph 0|1|2|3
--no-ralph
--output chat|project-local|staging
--project /path/to/project
--source /path/to/artifact
--backup
--no-apply
--stage
--apply
--help
--examples
--modes
--parameters
--quickstart
```

## Normalization

- `--mode deep` = `deep path`
- `--mode fast` = `fast path`
- `--mode guided` = `guided mode`
- `--mode yolo` = `yolo mode`
- `--mode review-gate` = `review-gate mode`
- `--mode audit-only` = `audit only`
- `--context-length`, `--targeted-context-length`, and `--ctx` all set `targeted_context_length`.
- `--ralph 0` and `--no-ralph` disable the Ralph loop.
- `--output project-local` means durable outputs belong under `<project>/.agent-work/`.
- `--output chat` means do not write files unless the task requires artifacts.
- `--output staging` means write staged outputs without overwriting originals.

## Conflict Handling

Examples:

- `--mode yolo` plus “ask before making changes” conflicts. Use guided/review-gate behavior for file changes unless the user confirms YOLO.
- `--apply` plus “do not apply” conflicts. Prefer `do not apply` and ask before applying.
- `--context-length 32k` plus “use the full 128k context” conflicts. Ask which context budget to target.

## Skill-Specific Flags

### Prompt Engineer

```bash
--prompt-file ./prompt.md
--structured-output json|markdown|none
--test-cases 5
--runtime-recommendations
```

### Skill Engineer

```bash
--source ./my-skill/SKILL.md
--reference-policy inspect|optimize|preserve
--metadata on|off
--in-place
```

### Skill Migrator

```bash
--skills-dir ~/.agents/skills
--migration-dir ~/.agents/skill-migrations/<id>
--batch-size 3
--restore <migration-id>
```

### Instruction Engineer

```bash
--project .
--instruction-file AGENTS.md
--scan-existing
--suggest-gitignore
```

### Agent Evaluator

```bash
--target ./AGENTS.md
--grade-only
--recommend-fixes
```

## Extended Parameters Added in v1.4.0

These parameters are accepted in CLI-style or natural language form.

| Parameter | Values | Purpose |
|---|---|---|
| `--education-level` | `none`, `brief`, `guided`, `deep`, `teaching` | Controls how much the tool explains its decisions to the user. |
| `--artifact-verbosity` | `compact`, `normal`, `detailed` | Controls verbosity of generated artifacts separately from educational explanation. |
| `--phase-review` | `off`, `brief`, `standard`, `deep` | Adds a post-phase code review gate for coding phases. |
| `--code-review-iterations` | `0`, `1`, `2` | Bounds focused post-phase code review improvement passes. |
| `--target-capability` | `small-local`, `mid-local`, `large-local`, `frontier-cloud`, `reasoning-specialized`, `coding-specialized`, `multimodal` | Selects a model capability tier when a specific model profile is not enough. |
| `--planner-profile` | model/profile name | Model/profile intended for planning, audits, and high-level design. |
| `--executor-profile` | model/profile name | Model/profile intended for carrying out atomic implementation phases. |
| `--focus` | `implementation-plan`, `test-quality`, `runtime-stability`, `agents-md`, `prompt`, `skill` | Focuses evaluator or engineer behavior on a specific review dimension. |

Aliases:

- `education level: deep`
- `explain level: guided`
- `artifact verbosity: compact`
- `phase review: standard`
- `planner profile: frontier-cloud`
- `executor profile: qwen36`
- `target capability: small-local`

Conflict rule: if `--education-level deep` conflicts with `--artifact-verbosity compact`, preserve compact artifacts and put educational detail in reports.



## Run Configuration Preview Flags

Use these when the user wants to see or skip the inferred configuration before work begins:

- `--review-config` / `--preview-config`: show inferred parameters, assumptions, and planned approach before proceeding.
- `--no-review-config` / `--no-preview-config`: skip the preview unless the task is blocked or approval is required.

Guided, deep, review-gate, AGENTS.md generation, migrations, and file-changing work should normally show a compact run configuration preview when important parameters were inferred.

## Documentation and Review Focus Values

`--focus` may include:

- `documentation-quality` — audit README/docs/user-facing explanations for clarity, tone, factuality, examples, repeated phrasing, overused contrast, and next-step usefulness.
- `implementation-plan`
- `test-quality`
- `runtime-stability`
- `agents-md`
- `prompt`
- `skill`
