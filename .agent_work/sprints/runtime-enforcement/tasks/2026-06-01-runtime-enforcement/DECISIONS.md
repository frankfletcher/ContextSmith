# Decisions: Runtime Enforcement for ContextSmith Skills

## Artifact Manifest
- artifact_type: decisions
- parent_task: TASK.md
- status: initial decisions recorded
- behavioral_contract: Record durable choices with reasons; separate facts from assumptions.

## Decisions

### 1. Treat runtime enforcement as an installed-skill problem
Decision: Do not rely on repository-local `validate_skills.py` as the runtime enforcement mechanism.

Reason: Users run installed skills outside this repository. Repo-local checks improve package quality but do not make behavior deterministic during skill use.

### 2. Separate deterministic validation from hard blocking
Decision: Use validators for deterministic pass/fail evidence, and use harness integration only where available for hard blocking.

Reason: CLI and MCP tools can make the checks deterministic, but a model can still ignore advisory results unless the harness enforces them.

### 3. Prefer one validator core with CLI and MCP frontends
Decision: Design one shared validation core and expose it through both CLI and MCP.

Reason: CLI is portable across harnesses. MCP is better for agent-native calls. Duplicating logic would create drift.

### 4. Pilot with `contextsmith-run`
Decision: Use `contextsmith-run` as the first skill integration candidate.

Reason: It already defines execution contracts, validation levels, evidence ledgers, self-audit, and runtime obligations.

### 5. Treat pytest as approved for runtime tests
Decision: Pytest is approved for validator, CLI, domain-pack, and runner tests.

Reason: The current user explicitly approved pytest for this plan. Other new dependencies still require approval.

### 6. Separate planner review from small-model execution
Decision: Broad architecture choices require human or stronger-model review gates. Small/local models should execute only atomic implementation or test phases.

Reason: The runtime architecture is sweeping. The plan should be executable by small models without asking them to make system-level design decisions.

### 7. Generalize through domain packs
Decision: Keep the validator core universal and express domain-specific rules as compact domain packs where possible.

Reason: The system should work for skills, agents, and prompts across coding, writing, research, scheduling, purchase/travel, education, and unknown fallback tasks.

## Pending Decisions
- Whether the runtime ships as a separate package, files copied into each skill bundle, or both.
- Whether package design changes require a `PACKAGE_SPEC.md` update.
- Whether opencode can enforce validator success as a closeout or permission gate.
- Which runtime surfaces are in the first implementation slice: CLI only, CLI plus domain packs, CLI plus runner, MCP, or harness adapter.
- Which additional domain packs should be added after the starter set.
