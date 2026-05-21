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
