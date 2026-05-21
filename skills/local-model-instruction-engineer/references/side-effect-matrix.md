# Side-Effect Matrix

Use this reference to choose interaction mode and approval requirements.

| Action Type | Examples | Default Mode | Approval |
|---|---|---|---|
| Read-only | inspect files, summarize docs, audit prompt | YOLO or guided | not required |
| Local reversible write | edit prompt, create AGENTS.md, stage skill output | guided | usually not required if staged |
| Local risky write | overwrite source files, modify dirty repo files | guided/review-gate | required when user work may be overwritten |
| Destructive local | delete files, reset Git, clean build dirs | review-gate | explicit approval required |
| External write | send email, create calendar event, open PR, publish package | review-gate | explicit approval required |
| Financial/purchasing | buy tickets, place order, subscribe | review-gate | explicit approval every time |
| Identity/auth/secrets | credentials, account changes, private data transfer | review-gate | explicit approval and privacy warning |
| Production/deployment | deploy, migrate DB, rotate keys | review-gate | explicit approval and rollback plan |

When in doubt, choose the safer mode and ask one high-leverage question.
