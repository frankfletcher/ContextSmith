# Run Configuration Preview

Use this reference when a ContextSmith skill has inferred important parameters and the run is not a simple fast-path action. The preview keeps the workflow transparent without requiring the user to remember every flag in advance.

## When To Use

Show a run configuration preview when:

- mode is `guided`, `deep`, or `review-gate`;
- the skill inferred several parameters;
- the task is long-running, file-changing, high-impact, or batch-oriented;
- `AGENTS.md` or repo-level instructions are being created or changed;
- side effects, migrations, staged outputs, or project-local task state are involved;
- the user asks to review the configuration first.

Skip the preview for low-risk fast-path tasks unless a blocking assumption exists.

## Preview Format

```markdown
I’m ready to proceed with this run configuration.

## Inferred Context

- Project/domain:
- User intent:
- Target artifact:
- Risk level:
- Existing instruction files or upstream artifacts found:
- Low-confidence assumptions:

## Parameters

```bash
--mode guided                  # Ask before major decisions.
--target-profile qwen36         # Selected because the user named Qwen/local model work.
--context-length 32k            # Tight target; use compact artifacts, smaller phases, and task state.
--domain coding,data-science-ml # Detected from project files or user request.
--harness generic-agent         # No harness was specified or detected.
--ralph 1                       # One bounded improvement pass for a reusable artifact.
--education-level guided        # Explain key choices without bloating the artifact.
--artifact-verbosity compact    # Keep model-facing instructions concise.
--output project-local          # Save reports under <project>/.agent-work/.
```

## Planned Approach

1. Reuse existing safeguards when they are already clear.
2. Strengthen missing or vague safeguards.
3. Avoid duplicate instruction bloat.
4. Generate or update the target artifact.
5. Provide an educational change report.

Proceed with this configuration, or tell me what to change.
```

## Rules

- Treat CLI-style flags as the canonical preview language because they are easy to copy into future runs.
- Explain inferred values briefly. Do not produce a long essay.
- Call out low-confidence assumptions instead of burying them.
- If the user changes one parameter, update that parameter and continue when safe.
- For review-gate and migration workflows, do not apply changes until the user approves.
