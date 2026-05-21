# Domain Intent Detection

Before engineering a prompt, skill, or instruction file, classify what the artifact is meant to accomplish and which domain risks apply.

## Domain Questions

1. What does the user want the agent to accomplish?
2. What domain is this in?
3. What tools or external systems are involved?
4. What can go wrong in this domain?
5. What needs human approval?
6. What evidence or validation is required?

## Common Domains

- coding/software engineering
- data analysis
- research
- writing/editing
- email/communication
- calendar/scheduling
- shopping/purchasing/tickets
- travel/reservations
- personal knowledge management
- finance/legal/medical high-stakes support
- creative generation
- document/file processing
- workflow automation

## Domain Guardrails

- **Email**: draft by default; send only with explicit approval; do not invent commitments.
- **Purchasing/tickets**: never buy without explicit approval; surface total price, dates, refund rules, quantity, location, and fees.
- **Research**: separate evidence from inference; cite sources; flag uncertainty.
- **Coding**: inspect structure first; make narrow changes; run relevant tests; summarize changed files.
- **Scheduling/calendar**: verify timezone, date, attendees, duration, and recurrence before creating or changing events.
- **High-stakes domains**: include uncertainty, recommend professional review when appropriate, and avoid overclaiming.
