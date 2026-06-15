# Help Mode

Each ContextSmith skill supports help/discovery modes and a wizard for first-time users.

## Wizard Mode

When the `contextsmith` meta-skill is invoked with no clear intent, no flags, and no sub-skill name, it enters wizard mode. The wizard asks three questions to determine the right sub-skill and parameters, then shows a confirmation table before dispatching.

Wizard questions:

1. "What are you working on?" — maps to sub-skill
2. "Which model will use the result?" — maps to `--target-profile`
3. "How much context can it work with?" — maps to `--context-length`

Skip the wizard when the user provides flags, sub-skill names, or clear natural-language intent.

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
