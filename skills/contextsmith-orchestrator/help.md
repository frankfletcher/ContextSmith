# contextsmith-orchestrator Help

`contextsmith-orchestrator` executes workflow configs, raw prompts, and task-state handoffs through a deterministic state machine loop with full contract enforcement.

## Use It For

- running a workflow config YAML through phased execution with validation gates
- executing `NEXT_PROMPT.md` from a `.agent_work/.../tasks/<task>/` folder
- running one phase of an implementation plan
- running raw prompts with contract enforcement (target profile, validation, self-audit, Ralph)
- resuming a blocked or paused workflow from checkpoint

## Common Commands

```bash
/contextsmith-orchestrator --target workflow_config.yaml --state-dir .agent_work/.../tasks/my-task
```

```bash
/contextsmith-orchestrator --run-mode phase --target .agent_work/sprints/example/tasks/task-name --validation strict
```

```bash
/contextsmith-orchestrator --interaction refine --domain software-engineering --validation available
```

## Key Parameters

| Parameter | Purpose |
|-----------|---------|
| `--run-mode` | `single`, `single-with-state`, `phase`, `phased-run`, `dry-run`, or `audit-only` |
| `--interaction` | `silent`, `confirm`, `refine`, `collaborative`, or `review-gate` |
| `--domain` | task domain for validation and audit lenses |
| `--validation` | `none`, `basic`, `available`, or `strict` |
| `--ralph` | required bounded critique/revision iterations |
| `--self-audit` | `true` or `false` |

## Output

The skill reports result, evidence, validation, self-audit, Ralph summary, declared-vs-enforced status, and next action.
