# Schedule with Approval Gates: Step-by-Step

Use this workflow when scheduling tasks that require human approval before executing external actions (sending emails, booking meetings, making purchases). ContextSmith's runtime enforcement can enforce approval gates at these boundaries.

## Table of Contents

- [When to Use This Workflow](#when-to-use-this-workflow)
- [Inputs](#inputs)
- [Step 1: Define Approval Boundaries](#step-1-define-approval-boundaries)
- [Step 2: Invoke the Skill with Approval Gates](#step-2-invoke-the-skill-with-approval-gates)
- [Step 3: Review Proposed Actions](#step-3-review-proposed-actions)
- [Step 4: Approve or Reject Each Gated Action](#step-4-approve-or-reject-each-gated-action)
- [Step 5: Validate Phase Completion](#step-5-validate-phase-completion)
- [Expected Artifacts](#expected-artifacts)
- [Common Failure Modes](#common-failure-modes)

## When to Use This Workflow

Use this workflow for:
- Tasks requiring human approval before external actions
- Calendar operations (meeting scheduling, event creation)
- Email sending or message coordination
- Purchases, subscriptions, or financial transactions

If you need to run a task-state handoff without explicit approval gates, see [Run a Task-State Handoff](RUN_TASK_STATE_HANDOFF.md).

## Inputs

- Task description
- Approval boundaries (what requires approval vs. what doesn't)
- Domain selection (e.g., `scheduling`, `purchasing`)

## Step 1: Define Approval Boundaries

Identify which actions require explicit user approval and which don't. Use `shared/side-effect-matrix.md` to classify actions by risk tier.

**Examples:**
- **Requires approval**: Sending calendar invites, purchasing tickets, booking meetings
- **Does not require approval**: Drafting emails, listing available time slots, comparing travel options

## Step 2: Invoke the Skill with Approval Gates Configured

Use `contextsmith-orchestrator` with `--interaction review-gate` and the appropriate domain flag.

**Example prompt:**
```
Run the scheduling task to find meeting times and send invites:
.domain scheduling
.interaction review-gate
--ralph 2
```

This will pause before sending any calendar invites for explicit approval.

## Step 3: Review Proposed Actions

Before any external action, the skill will present a compact summary of proposed actions for review. This includes:
- Action description
- Side-effect tier
- Residual risks
- Required approval status

## Step 4: Approve or Reject Each Gated Action

For each action requiring approval:
- Review the proposed action and risks
- Explicitly approve or reject
- If rejected, the workflow pauses and records the decision

## Step 5: Validate Phase Completion

After all approval gates are processed:
- Verify approval ledger exists and is complete
- Check that no external actions occurred without approval
- Confirm phase evidence is recorded
- Review residual risks disclosure

## Expected Artifacts

| Artifact | Path | Purpose |
| --- | --- | --- |
| `approval_ledger.json` | `.agent_work/.../approval_ledger.json` | Record of all approval decisions (approved/denied/pending) |
| `phase_evidence.md` | `.agent_work/.../phase_evidence.md` | Evidence that validation gates passed |
| `updated_task_state/` | `.agent_work/sprints/<sprint>/tasks/<date-slug>/` | Task state with approval decisions recorded |
| `residual_risks.md` | `.agent_work/.../residual_risks.md` | Disclosure of any risks that remain after execution |

## Common Failure Modes

| Failure Mode | Detection | Recovery |
| --- | --- | --- |
| Missing approval boundaries | Validator flags undefined external actions | Define boundaries and re-run |
| Skipped approval gates | Evidence ledger missing approval records | Re-run with `--interaction review-gate` |
| Stale approvals | Approval timestamp older than action timestamp | Re-validate and re-approve if needed |
| Unclear action descriptions | User cannot understand proposed action | Improve action description clarity |
| External action without approval | Validator detects unapproved external action | Stop and require explicit approval |

**Stop Rule:** Stop when `SCHEDULE_WITH_APPROVAL_GATES.md` is created, `README.md` is updated, validations pass, and Ralph loop completes 2 iterations.
