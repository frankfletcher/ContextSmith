# Decisions: ContextSmith v1.5.1 Audit Remediation

## Decision 1: Create separate minimal behavioral contracts file
**Rationale:** Appending to `shared/behavioral-contracts.md` makes the problem worse. The audit finding was about model-specific guidance being too large. Creating a separate file keeps the original intact while providing small-model-specific guidance.

## Decision 2: Use comment-before-YAML for context budget parameterization
**Rationale:** The `<USER_CONTEXT_TARGET>` placeholder from the original plan is not YAML-idiomatic. Using `{{CONTEXT_BUDGET}}` with HTML comments is more standard and easier to parse.

## Decision 3: Per-phase git commits
**Rationale:** Each phase is atomic and should be committed separately. This allows rollback of individual phases if needed and provides better audit trail.

## Decision 4: CHANGELOG version v1.5.2
**Rationale:** v1.5.1 was released 2026-05-30. This is a patch release addressing audit findings, so v1.5.2 is the next version.

## Decision 5: Check per-skill reference copies after shared/ edits
**Rationale:** Skills may have copied shared/ files to their references/ directories for standalone installation. After editing a shared/ file, we must check if the per-skill copies need updating to stay in sync.

## Decision 6: Task state updates after each phase
**Rationale:** STATUS.md, PHASE_LOG.md, and ARTIFACTS.md must be updated after each phase to enable fresh session resumption. Without these updates, the executor cannot know where to continue.
