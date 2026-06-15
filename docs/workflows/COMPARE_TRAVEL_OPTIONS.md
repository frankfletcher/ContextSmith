# Compare Travel Options: Step-by-Step

Use this workflow when you need to compare travel options (flights, hotels, trains) without making purchases. ContextSmith's runtime enforcement ensures no external actions occur without approval.

## Table of Contents

- [When to Use This Workflow](#when-to-use-this-workflow)
- [Inputs](#inputs)
- [Step 1: Define Constraints and Comparison Criteria](#step-1-define-constraints-and-comparison-criteria)
- [Step 2: Invoke the Skill with Travel Domain](#step-2-invoke-the-skill-with-travel-domain)
- [Step 3: Review Proposed Options](#step-3-review-proposed-options)
- [Step 4: Validate No External Actions](#step-4-validate-no-external-actions)
- [Step 5: Finalize Comparison with Evidence](#step-5-finalize-comparison-with-evidence)
- [Expected Artifacts](#expected-artifacts)
- [Common Failure Modes](#common-failure-modes)

## When to Use This Workflow

Use this workflow when:

- Comparing flights, hotels, or trains across dates and destinations
- Evaluating options against budget, timing, or preference constraints
- You want comparison results without triggering purchases or bookings

If you need to proceed to booking after comparison, see [Schedule with Approval Gates](SCHEDULE_WITH_APPROVAL_GATES.md).

## Inputs

- Travel constraints: dates, destinations, number of travelers
- Budget range or maximum price
- Comparison criteria: price, duration, convenience, amenities, or custom weights

## Step 1: Define Constraints and Comparison Criteria

Specify what you're comparing and the constraints that apply.

**Example:**

```
Compare round-trip flights from NYC to London, July 10-24.
Budget: under $900.
Criteria: prioritize total travel time, then price.
Constraints: no more than 1 layover, depart after 8am.
```

## Step 2: Invoke the Skill with Travel Domain

Use `contextsmith-orchestrator` with the travel/purchase domain. The domain pack enforces that comparison is read-only and purchasing requires explicit approval.

**Example prompt:**

```
Compare travel options for my trip.
--domain travel-purchase
--side-effects read-only
--ralph 2
```

The agent will:

1. Search or retrieve available options within constraints
2. Score options against your criteria
3. Present a ranked comparison without initiating any purchase

## Step 3: Review Proposed Options

Examine the comparison output for:

1. **Constraint satisfaction** — each option respects your stated constraints
2. **Price accuracy** — prices include taxes and fees, not base fares only
3. **Criteria alignment** — ranking reflects your stated priorities
4. **Completeness** — enough options to make a meaningful choice

If the comparison is missing options or misapplies criteria, ask the agent to refine before proceeding.

## Step 4: Validate No External Actions

Verify the comparison did not trigger external actions:

- No purchases, bookings, or reservations were made
- No email confirmations or calendar events were created
- The agent remained within `read-only` side-effect tier

Use `shared/side-effect-matrix.md` to confirm: financial/purchasing actions require `review-gate` mode with explicit approval every time. A read-only comparison should not cross into that tier.

## Step 5: Finalize Comparison with Evidence

Record the comparison results with supporting evidence:

- Save the comparison summary with timestamps
- Note the data source and retrieval time (prices may change)
- Record which constraints were applied and which options were excluded

## Expected Artifacts

| Artifact | Purpose |
| --- | --- |
| Comparison summary | Ranked options with prices, times, and constraint status |
| Price evidence | Source URLs or retrieval timestamps for each price |
| Constraint validation | Record of which constraints each option satisfies or violates |

## Common Failure Modes

| Problem | Fix |
| --- | --- |
| Missing constraints in comparison | Re-run with explicit constraint list in Step 1 |
| Stale or unverified prices | Check retrieval timestamps; re-run if data is older than 24 hours |
| Unapproved purchase attempt | Stop immediately. Review side-effect tier. Re-invoke with `--side-effects read-only` |
| Options don't match criteria weights | Re-specify criteria priorities and re-run Step 2 |
| Insufficient options for meaningful comparison | Broaden constraints (dates, airports, budget) and re-run |
