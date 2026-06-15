# File Operation Safety

Use this reference when a prompt, skill, or repo instruction file guides a tool-using agent that creates, reads, or modifies files. File operations are a common source of data loss in agent workflows — this reference prevents accidental overwrites and ensures agents verify before acting.

## Read Before Writing

Always read a file before modifying it. This is the single most important file safety rule.

- To check if a file exists, use `test -f <path>` or the `read` tool. Do NOT use `ls` for existence checks — `ls` can produce false negatives.
- Before creating or overwriting any file, read it first. If the read succeeds (returns content), use `edit` to modify it or `>>` to append — never use `write` on a file whose current content you haven't verified.
- When a `write` call is necessary (new file that definitely doesn't exist), first confirm with `test -f` that the path is clear.

## Records vs. One-Shot Files

Identify each file's purpose before writing. Different file types need different write strategies:

**Append-only records** — always use `>>` heredoc, never `write`:

- Report files: `*_REPORT.md` (EDUCATIONAL_REPORT.md, AUDIT_REPORT.md, etc.)
- Persistent state: DECISIONS.md, PHASE_LOG.md, STATUS.md, and any file expected to preserve prior entries
- Log files and cumulative artifacts

**Standard files** — use `edit` for modifications, `write` only for new files:

- Source code, configuration, documentation
- Any file where replacing all content is the intended operation

As a general rule: if the purpose is to maintain a record — history, decisions, logs, phase notes, reports, or any cumulative artifact — use append (`>>` heredoc) to add new entries and never clobber prior records.

## Verify After Operations

After any file operation, confirm the result:

- Read the file to verify content is as expected.
- Check with `test -f` or `stat` to confirm the file exists.
- After a delete, confirm the file is gone.

## Compact AGENTS.md Block

```markdown

## File Operation Safety

1. To check if a file exists, use `test -f <path>` or the `read` tool. Do NOT use `ls` for existence checks.
2. Before creating or overwriting any file, read it first. If the read returns content, use `edit` to modify or `>>` to append — never `write` a file whose content you haven't verified.
3. For append-only report files (`*_REPORT.md`) and persistent state files (DECISIONS.md, PHASE_LOG.md, and similar), use `>>` heredoc. Never `write` the whole file.
4. When a `write` call is necessary (new file that doesn't exist), first confirm with `test -f` that the path is clear.
5. After any file operation, verify the result: read the file or check with `test -f`/`stat`.
```
