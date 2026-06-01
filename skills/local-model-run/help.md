# local-model-run Help

`local-model-run` executes prompts, prompt files, and ContextSmith task-state handoffs under explicit runtime controls.

## Use It For

- running a prompt while enforcing `--target-profile`, `--context-length`, `--ralph`, validation, and self-audit
- executing `NEXT_PROMPT.md` from a `.agent_work/.../tasks/<task>/` folder
- running one phase of an implementation plan
- running non-code prompts such as research, email rewriting, data analysis, or business memos with domain-specific validation
- asking refinement questions before execution so important assumptions are not silently guessed

## Common Commands

```bash
/local-model-run --run-mode single --target-profile qwen36 --ralph 1
```

```bash
/local-model-run --run-mode phase --target .agent_work/sprints/contextsmith-1.0/tasks/example --validation strict
```

```bash
/local-model-run --interaction refine --domain frontend-ux --validation available
```

```bash
/local-model-run --run-mode dry-run --target NEXT_PROMPT.md
```

## Key Parameters

| Parameter | Purpose |
|-----------|---------|
| `--run-mode` | `single`, `single-with-state`, `phase`, `phased-run`, `dry-run`, or `audit-only` |
| `--interaction` | `silent`, `confirm`, `refine`, `collaborative`, or `review-gate` |
| `--question-budget` | maximum refinement questions |
| `--domain` | task domain such as `frontend-ux`, `research`, `writing-editing`, or `data-science-ml` |
| `--validation` | `none`, `basic`, `available`, or `strict` |
| `--ralph` | required bounded critique/revision iterations |
| `--self-audit` | `true` or `false`; false is only for explicit low-risk, nonpersistent work |

## Output

The skill reports result, evidence, validation, self-audit, Ralph summary, declared-vs-enforced status, and next action.
