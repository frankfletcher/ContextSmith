# Interaction Modes

Use interaction modes to avoid pure fire-and-forget behavior without making every task tedious.

## YOLO Mode

Proceed with explicit assumptions. Ask only when blocked. Use for low-risk, reversible, one-shot tasks.

## Guided Mode

Ask 1-3 high-impact questions before major changes when answers materially affect target model, output format, side effects, context strategy, validation criteria, or domain behavior. Use for reusable prompts, skills, AGENTS.md, or complex edits.

## Review-Gate Mode

Create a plan or staged output first. Do not apply changes until the user approves. Use for batch migration, high-risk domains, destructive changes, external side effects, purchasing, sending messages, deployment, or production systems.

## Audit-Only Mode

Inspect and report. Do not modify files.

## Stage/Apply Mode

Stage writes to a separate folder and generate a manifest. Apply only with explicit approval.

## Question-or-Proceed Rule

Ask only when the answer materially changes correctness, safety, side effects, target profile, or output. Otherwise proceed and record assumptions.
