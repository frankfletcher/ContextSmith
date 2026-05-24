# Versioning Policy

ContextSmith uses a SemVer-inspired policy from this point forward.

## Package Version

Use `MAJOR.MINOR.PATCH`:

- MAJOR: breaking changes to skill names, folder layout, invocation semantics, or output contracts.
- MINOR: backward-compatible new capabilities, new references, new skills, or meaningful workflow additions.
- PATCH: documentation updates, typo fixes, small reference refinements, validation script fixes, and non-breaking polish.

Minor versions are numeric and can grow: `1.9.0` is followed by `1.10.0`, not `2.0.0`.

## Skill Versions

Individual skills may have their own versions, but package releases are the main public version. Avoid bumping every skill for docs-only changes unless that skill's behavior changed.

## Changelog Format

```markdown
## v1.4.0

**Released:** YYYY-MM-DD

### Added
### Changed
### Fixed
### Notes
```

## No Backfill Rule

Do not renumber historical releases. Apply the policy going forward.
