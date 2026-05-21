# Domain Intent Detection

Before engineering a prompt, skill, migration, or instruction file, infer what the user wants the agent to accomplish and which domain risks apply.

## Detect

Identify:

- domain: coding, data science/ML, research, writing, email, calendar, purchasing/tickets, travel, documents, automation, finance/legal/medical, personal knowledge, creative
- side effects: read-only, local write, external write, financial, destructive, production
- harness: coding agent, browser agent, email/calendar agent, shell agent, RAG/search agent, mixed
- target model/profile and context risk

Use `references/side-effect-matrix.md` to choose interaction mode.

## Domain Defaults

- Coding: inspect structure, protect Git/user changes, run narrow validation, avoid unrelated refactors.
- Data science/ML: prevent leakage, preserve reproducibility, track metrics/artifacts, avoid committing large data/model files.
- Email: draft by default; send only after explicit approval.
- Purchasing/tickets: never purchase without explicit approval; show total price, fees, date, quantity, refund rules.
- Research: cite evidence; separate source facts from inference.
- Scheduling: confirm attendees, time zone, recurrence, and external invites before creating events.
- Documents: preserve formatting and cite source sections when relevant.
- High-stakes finance/legal/medical: use conservative guidance, cite sources when factual, and avoid definitive professional advice.

## Report

Include a compact domain report when useful:

```markdown
## Detected Domain and Intent
- Domain:
- Confidence:
- Side-effect risk:
- Safeguards applied:
```
