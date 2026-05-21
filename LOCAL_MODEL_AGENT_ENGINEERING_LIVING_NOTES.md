# Local Model Agent Engineering — Living Design Notes

Status: living backlog / design notebook  
Purpose: capture future improvements before implementation so the package does not grow by ad hoc patching.

## Package Thesis

Local and smaller open-weight models perform best when agent instructions are explicit, staged, validated, context-aware, and durable across interruptions. The package should help users engineer prompts, skills, repo instruction files, and skill migrations that work reliably under limited context, imperfect reasoning, and varied agent harnesses.

## Current Core Skills

- `local-model-prompt-engineer`
- `local-model-skill-engineer`
- `local-model-skill-migrator`
- Proposed: `local-model-instruction-engineer`

Use Option C for package structure:
- Keep canonical shared references under `shared/`.
- Copy the required reference subset into each skill’s `references/` directory so each skill remains standalone-installable.

## Future Ideas Backlog

### 1. Ralph Improvement Loop

Add an optional bounded iterative improvement loop.

Purpose:
- Passing minimum validation does not mean the artifact is excellent.
- The loop should ask how to make the output more reliable for smaller/local models.

Default:
- Max iterations: 2
- Hard max: 3 unless user explicitly overrides

Iteration questions:
- Is the output atomic enough for a smaller model?
- Are any instructions too abstract?
- Are assumptions explicit?
- Is the output contract deterministic enough?
- Is the context strategy sufficient?
- Are examples helpful but not bloated?
- Is the target model/profile applied correctly?
- Does the artifact avoid exposed chain-of-thought?
- Is another iteration likely to materially improve reliability?

A–F grading dimensions:
- Small-model atomicity
- Instruction clarity
- Output contract quality
- Context strategy
- Assumption control
- Domain fit
- Validation strength
- Bloat / cognitive load

Iteration storage:
```text
iterations/
├── iteration-01/
│   ├── artifact
│   ├── audit.md
│   └── improvement-notes.md
├── iteration-02/
│   ├── artifact
│   ├── audit.md
│   └── improvement-notes.md
└── FINAL/
```

Guardrail:
- Do not iterate for cosmetic polishing.
- Create another iteration only if it improves execution reliability, clarity, model fit, validation strength, context handling, semantic preservation, or user value.

### 2. Educational Change Reports

Each engineering skill should teach the user what improved.

Output pattern:
```markdown
## Original Strengths
- ...

## Original Weaknesses
- ...

## Changes Made
- ...

## Why These Changes Improve Local-Model Reliability
- ...

## Remaining Risks
- ...
```

Purpose:
- Build user trust.
- Teach better prompt/skill/instruction design.
- Make the value of the engineer skill visible.

### 3. Domain Intent Detection

Before editing or creating an artifact, infer the domain and operational intent.

Potential domains:
- coding / software engineering
- data analysis
- research
- writing / editing
- email / communication
- calendar / scheduling
- shopping / purchasing
- travel / tickets / reservations
- personal knowledge management
- finance / legal / medical high-stakes guidance
- creative generation
- workflow automation
- file/document processing

Domain questions:
- What does the user want the agent to accomplish?
- What tools or external systems are involved?
- What can go wrong in this domain?
- What requires human approval?
- What evidence or validation is needed?
- What safety or privacy boundaries apply?

Examples:
- Email: draft by default; send only with approval.
- Purchasing/tickets: never buy without explicit approval; surface total cost and refund rules.
- Research: cite evidence; separate source facts from inference.
- Coding: inspect structure before editing; run tests when available; avoid unrelated changes.

### 4. Interaction Modes

Add explicit operating modes across the package.

Modes:
- `yolo`: proceed with assumptions; ask only if blocked.
- `guided`: ask 1–3 high-impact questions before major changes.
- `review-gate`: produce plan/staged output first; wait for approval before applying.
- `audit-only`: analyze and report, do not modify.
- `stage`: write outputs to staging, do not apply.
- `apply`: apply staged changes after explicit approval.
- `restore`: restore from backup/migration manifest.

Recommended defaults:
- Prompt improvement: YOLO or guided.
- Skill creation/conversion: guided.
- Recursive migration: review-gate.
- Repo instruction files: guided.
- High-side-effect domains: review-gate.

Clarification rule:
- Ask only when the missing answer materially changes output, side effects, target model/profile, validation, or safety.
- Otherwise proceed with stated assumptions.

### 5. Local Model Agent Evaluator

Potential future skill:
- `local-model-agent-evaluator`

Purpose:
- Audit prompts, skills, AGENTS.md, or instruction files without modifying them.
- Return grades, risks, and recommended changes.
- Useful before mutation or for code review-style feedback.

### 6. Model Profile Builder

Potential future skill:
- `local-model-profile-builder`

Purpose:
- Create or update model profiles based on user tests, model cards, runtime behavior, and known failure modes.

Profile fields:
- model family
- context limits
- runtime quirks
- structured-output behavior
- reasoning/thinking behavior
- sampling guidance
- known failure modes
- recommended prompt patterns

### 7. Agent Task State Manager

Potential future skill:
- `agent-task-state-manager`

Purpose:
- Initialize, clean, audit, or resume persistent task-state folders.
- Useful if durable phase memory becomes a frequent workflow.

### 8. Agent Harness Adapter

Potential future skill:
- `local-model-agent-harness-adapter`

Purpose:
- Adapt instructions for specific harnesses such as OpenCode, Codex, OpenClaw, Hermes, Aider-like tools, etc.

Do not implement immediately. First stabilize the four core skills.

## Phased Execution Plan Improvements

Problem observed:
- A prompt builder generated a nice three-phase plan for porting a large Windows/macOS application to Linux.
- Three phases were too coarse for a small model.
- The task caused context churn.
- The plan lacked durable memory/progress documentation.

### Principle: Phase Granularity Must Scale With Task Complexity

For small local models, large phases are dangerous because they require too much implicit state. Prefer smaller phases with explicit stop conditions.

Complex tasks should be broken into 6–12 phases, not 3 broad phases.

Large porting/migration tasks should usually include phases such as:
1. Repository inventory and build-system discovery
2. Platform-dependency inventory
3. Runtime/environment assumptions
4. Build bootstrap on Linux
5. Dependency replacement strategy
6. Filesystem/path/process/shell compatibility
7. UI/windowing/input/audio/network compatibility, if relevant
8. Test harness setup
9. Incremental port of core modules
10. Incremental port of platform-specific modules
11. Packaging/distribution work
12. Validation, regression testing, and cleanup

### Phase Design Rules

Each phase should include:
- goal
- inputs
- files/directories likely involved
- explicit tasks
- outputs/artifacts
- validation checks
- stop condition
- handoff notes for next phase

Avoid phases like:
- “Port platform-specific code”
- “Fix Linux compatibility”
- “Test everything”

Prefer atomic phases like:
- “Inventory platform-specific APIs and write `platform-compat-inventory.md`.”
- “Get dependency installation and build bootstrap working on Linux.”
- “Replace Windows/macOS path handling with cross-platform path abstractions.”
- “Run the narrowest available test suite and record failures.”

### Required Memory Documentation for Long Plans

Every long-running implementation plan should include a durable task-state protocol.

Recommended task folder:
```text
.agent-work/
└── sprints/<sprint-or-subproject>/tasks/<YYYY-MM-DD-short-slug>/
    ├── TASK.md
    ├── PLAN.md
    ├── STATUS.md
    ├── DECISIONS.md
    ├── CONTEXT.md
    ├── CHECKLIST.md
    ├── ARTIFACTS.md
    ├── PHASE_LOG.md
    └── NEXT_PROMPT.md
```

File roles:
- `TASK.md`: objective, scope, constraints, success criteria. Do not rewrite unless task changes.
- `PLAN.md`: phase checklist. Update checkboxes only.
- `STATUS.md`: current phase, completed work, in-progress work, next steps. Keep short.
- `DECISIONS.md`: durable architectural or behavioral decisions only.
- `CONTEXT.md`: compressed context, file map, important constraints, do-not-load guidance.
- `CHECKLIST.md`: validation gates.
- `ARTIFACTS.md`: changed/generated files, commands run, outputs produced.
- `PHASE_LOG.md`: compact phase-by-phase notes, not raw logs.
- `NEXT_PROMPT.md`: resume prompt for crash/context loss.

Junk-drawer prevention:
- Do not paste full files, full logs, transcripts, or command output into task state.
- Store summaries, paths, commands, decisions, evidence snippets, and validation results.
- Replace stale status instead of appending forever.
- Keep `STATUS.md`, `CONTEXT.md`, and `NEXT_PROMPT.md` short.
- Do not mix unrelated tasks in one task folder.

### Phase Memory in Generated Plans

When a generated prompt or instruction file asks for a long implementation plan, it should require:

```markdown
## Persistent Phase Memory

Before implementation, create or update the task-state folder.

At the start of each phase:
- Read `TASK.md`, `PLAN.md`, `STATUS.md`, `DECISIONS.md`, and `CHECKLIST.md`.
- Confirm the current phase and stop condition.
- Avoid restarting completed phases.

At the end of each phase:
- Update `STATUS.md`.
- Check off completed items in `PLAN.md`.
- Add durable decisions to `DECISIONS.md`.
- Add changed files and commands to `ARTIFACTS.md`.
- Add compact notes to `PHASE_LOG.md`.
- Update `NEXT_PROMPT.md`.
```

### Ralph Loop for Phase Plans

The Ralph loop should evaluate phase plans with A–F grades:
- Phase granularity
- Small-model suitability
- Memory/documentation support
- Stop conditions
- Validation strength
- Context-risk handling
- Domain fit
- Human approval gates

A three-phase plan for a large application port should usually fail phase granularity unless each phase contains well-defined subphases.

## Future Package Implementation Notes

Before next implementation:
1. Add shared `evaluation-rubrics.md`.
2. Add shared `interaction-modes.md`.
3. Add shared `small-model-atomicity.md`.
4. Add shared `phase-planning.md`.
5. Add shared `domain-profiles/`.
6. Update prompt/skill/migrator skills to reference these.
7. Create `local-model-instruction-engineer`.
8. Package the repository with README, examples, and install instructions.
