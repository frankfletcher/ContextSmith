# Documentation Quality Audit

Use this reference when generating, reviewing, or editing user-facing project documentation, README material, educational reports, prompt packages, AGENTS.md explanations, or changelog entries. Keep agent-facing references concise and operational; use this audit mainly for material that a person is expected to read.

## Purpose

Good documentation helps someone understand what ContextSmith does, choose the right workflow, run a useful command, review the result, and avoid common mistakes. The review should improve clarity and usefulness without turning every file into marketing copy.

## Review Checklist

Evaluate:

- **Clarity:** Can a new user tell what to do next?
- **Specificity:** Are claims backed by concrete examples, commands, or file paths?
- **Readability:** Are paragraphs short enough to scan? Are long bullet lists explained when needed?
- **Sentence variety:** Do repeated sentence openings or repeated sentence shapes make the doc feel mechanical?
- **Repeated phrasing:** Are the same ideas repeated in several forms? Keep the strongest version.
- **Overused contrast:** Flag repeated patterns such as “not just X, but Y” or “the goal is not X; the goal is Y.” Use contrast only when it clarifies a real misconception.
- **Tone:** Keep the voice practical, candid, and respectful. Avoid implying the user needs hand-holding.
- **Imperatives:** Use direct instructions for safety-critical or agent-facing rules. In user docs, prefer suggestions when the action is advisory.
- **Jargon density:** Define project terms such as targeted context length, Ralph loop, and review-gate mode before relying on them.
- **Example quality:** Every example should help the reader choose, run, review, or troubleshoot ContextSmith.
- **Factuality:** Do not imply tests, integrations, benchmarks, or harness support that have not been implemented.
- **Time to useful work:** Does the doc make it easy to try one real workflow quickly?

## Rewrite Patterns

Prefer:

> ContextSmith can infer a run configuration, explain the choices, and ask for correction before important work.

Avoid:

> This lowers cognitive load dramatically.

Prefer:

> When adjusting runtime settings, treat the process like an experiment. We suggest changing one setting at a time, recording the result, and keeping a known-stable baseline.

Avoid:

> Do not change every knob at once.

Prefer:

> ContextSmith helps create agent instructions that remain usable under context pressure, tool failures, long coding runs, and real project constraints.

Avoid overusing:

> The goal is not just better prompts. The goal is ...

## Output Format

When auditing documentation, return:

```markdown
## Documentation Quality Summary

## Strengths

## Issues to Fix

## Suggested Edits

## Factuality Check

## Tone and Style Notes

## Next-Step Clarity
```
