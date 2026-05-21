# Optional Ralph Improvement Loop

The Ralph loop is a bounded improve-after-validation loop. It exists because passing minimum validation does not mean an artifact is good enough for smaller/local models.

## When to Use

Use only when the user asks for extra quality, the artifact will be reused, the task is high-risk, or the output is likely to run on a smaller model with limited context.

Default maximum iterations: **2**. Hard maximum: **3** unless the user explicitly asks for more.

## Iteration Protocol

For each iteration:

1. Write the candidate output to `iterations/iteration-NN/`.
2. Run baseline validation.
3. Grade the candidate using `evaluation-rubrics.md`.
4. Answer:
   - What is strong?
   - What is weak?
   - What is too abstract for a smaller model?
   - What should be more atomic?
   - What assumptions remain?
   - What context, persistence, or subagent support is missing?
   - What can be simplified without losing behavior?
5. Produce another iteration only if it materially improves execution reliability, semantic preservation, context handling, validation strength, or domain fit.
6. Write `ITERATION_REPORT.md` with grades and changes.

## Output Layout

For prompts:

```text
iterations/
├── iteration-01/prompt-package.md
├── iteration-01/audit.md
├── iteration-02/prompt-package.md
├── iteration-02/audit.md
└── FINAL.md
```

For skills:

```text
iterations/
├── iteration-01/SKILL.md
├── iteration-01/references/
├── iteration-01/audit.md
├── iteration-02/SKILL.md
├── iteration-02/references/
└── FINAL/
```

For instruction files:

```text
iterations/
├── iteration-01/AGENTS.md
├── iteration-01/audit.md
├── iteration-02/AGENTS.md
└── FINAL_AGENTS.md
```

## Stop Rules

Stop when maximum iterations are reached, no material improvement remains, validation requires user input, or further changes risk semantic drift.
