# Help Mode

Each ContextSmith skill supports help/describe modes. If the user asks for help, do not run the normal engineering workflow.

## Supported Help Commands

Natural-language forms:

- `help`
- `describe`
- `examples`
- `modes`
- `parameters`
- `quickstart`

CLI-style forms:

- `--help`
- `--examples`
- `--modes`
- `--parameters`
- `--quickstart`

## Behavior

- `help`: return a concise usage page for the skill.
- `describe`: explain what the skill does and when to use it.
- `examples`: show copy-paste invocation examples.
- `modes`: explain fast/deep/guided/yolo/review-gate/audit-only/stage/apply.
- `parameters`: list supported natural-language controls and CLI-style flags.
- `quickstart`: show the shortest useful invocation.

Help output should be concise, practical, and example-heavy. Do not include the full README unless the user asks for detailed documentation.
