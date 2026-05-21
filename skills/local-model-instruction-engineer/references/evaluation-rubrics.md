# Evaluation Rubrics

Use A-F grading. Validation pass/fail is separate from quality.

## Core Dimensions

| Dimension | A | C | F |
|---|---|---|---|
| Small-model atomicity | Instructions are concrete, ordered, and testable | Some abstraction remains | Requires large inference leaps |
| Instruction clarity | Direct, unambiguous, scoped | Several vague rules | Conflicting or generic |
| Output contract | Exact enough to validate | Partial format | No usable output definition |
| Context strategy | Source mode, selection, compression, and re-anchor defined | Some strategy | Dumps or assumes all context |
| Assumption control | Assumptions explicit and low-risk | Some hidden assumptions | Risky or invented assumptions |
| Domain fit | Domain intent and side effects handled | Generic safeguards only | Domain risks ignored |
| Validation strength | Evidence-backed tests/checks | Minimal validation | Claims without evidence |
| Loop safety | Retry/stop rules prevent loops | Partial retry handling | Repeats or encourages loops |
| Git/file safety | Protects user work and risky operations | Some protection | Can destroy or overwrite work |
| Bloat/cognitive load | Concise, de-duplicated | Some repetition | Wall of repeated rules |
| Progressive disclosure | Main file lean, refs clear | Some inlining | Monolithic and hard to load |
| Testability | Pass/fail criteria present | Some checks | Not testable |

## Ralph Loop Iteration Rule

Run another iteration only if at least one category is C or worse, or a B-grade issue is high-risk. Do not iterate for cosmetic polishing.

## Final Recommendation Labels

- `ship`: good enough; no high-risk gaps.
- `iterate`: material improvement likely.
- `ask-user`: blocked by missing requirement or approval.
- `reject`: unsafe, semantically broken, or too vague to use.
