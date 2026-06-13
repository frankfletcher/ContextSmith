# Harness: Generic

Load this reference when no specific harness companion matches. The generic companion is the fallback for unknown harnesses — skill-only mode, no optimizations, inline results.

## Agent Launch

The generic harness has no agent runtime. Execution is skill-only:

- **Mechanism**: The orchestrator skill executes phases directly — no subprocess, no agent CLI
- **Agent profile**: Not applicable (no agent runtime)
- **Step cap**: Self-managed via the orchestrator loop and max_retries/ralph_max_cycles counters
- **Timeout**: Self-managed via phase-level timeout tracking

Results are communicated via task-state artifacts (RESULT.json on disk). The orchestrator writes and reads these files directly.

## Permission Model

Permissions are self-enforced by the skill instructions — no harness-level enforcement:

- **Read-only**: Skill instructions prohibit writes. No external mechanism prevents writes.
- **Edit**: Skill instructions allow edits per the workflow config. No harness gating.
- **External action**: Skill instructions prohibit external actions. No harness gating.

For harness-level permission enforcement, use OpenCode or another runtime that supports agent profiles with restricted permissions.

## Result Protocol

Results follow the standard task-state protocol:

- **Primary**: RESULT.json on disk, written by the orchestrator skill after phase completion
- **Fallback**: Structured section in next phase handoff (NEXT_PROMPT.md) when RESULT.json is unavailable
- **Format**: `{ "status": "pass|fail|blocked", "reason": "...", "artifacts": [...], "issues": [...], "next_action": "..." }`
