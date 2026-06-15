# Thin-Skill Writing Guide

## Artifact Manifest

- artifact_type: reference-guide
- phase: 4B
- target_profile: qwen36
- version: 1.0.0

## Core Principle

A thin skill is a routing contract, not an instruction manual. The SKILL.md tells the model what to do and where to check. Validators enforce the rules. Runtime artifacts hold the schemas.

## Five Patterns

### 1. Point to Runtime Artifacts, Don't Duplicate Schemas

**Before (fat):** Paste the full domain pack schema, validation rules, and examples into SKILL.md.

**After (thin):** Reference the runtime artifact and let the validator check it.

```markdown

## Validation Gate
When `runtime/` is available, use `python -m runtime.cli <subcommand> <artifact.json>`.
Subcommands: `requirements`, `phase-contract`, `evidence`, `approval`, `closeout`, `domain-pack`.
```

The schema lives in `runtime/validator.py`. The domain packs live in `runtime/domain_packs/*.json`. SKILL.md only needs the invocation pattern.

### 2. Reference Validator Gates, Not Pass/Fail Rules

**Before (fat):** List every validation rule, violation message, and edge case in the skill.

**After (thin):** Name the validator and its exit codes.

```markdown
Exit codes: `0` pass, `1` violations, `2` error.
```

The validator owns the rules. The skill owns the instruction to call it.

### 3. Use a Manifest for Shipped Files, Not Inline Lists

**Before (fat):** Maintain a list of required files in SKILL.md that drifts from the actual package.

**After (thin):** Declare files in `reference_manifest.yml`. The packaging scripts use the manifest.

```yaml
- source: runtime/validator.py

  version: local
  required: true
  local: true
  notes: Runtime validator core.
```

### 4. Add a Step, Not a Section

When integrating a new capability, add a single execution step rather than a multi-paragraph section.

**Phase 4A example:** Added step 9 to the Execution Workflow:

```markdown
9. When runtime validators are available, validate emitted artifacts with `python -m runtime.cli` before proceeding.
```

One line. The validator handles the rest.

### 5. Stay Within Token Budgets

ContextSmith skills have a 4000-token budget (500-line cap). Use it for:

- Routing instructions (what to do when)
- Control parameters (what the model can configure)
- Invocation patterns (how to call external tools)
- Behavioral contracts (what the model must not do)

Don't use it for:

- Schema definitions (live in runtime artifacts)
- Validation rules (live in the validator)
- Full examples (live in test fixtures or docs)
- Architecture explanations (live in PLAN.md or docs)

## Checklist

Before marking a skill integration complete, verify:

- [ ] SKILL.md added at most a few lines or one step per integration
- [ ] SKILL.md stays under 500 lines and 4000 tokens
- [ ] New capability is referenced, not duplicated
- [ ] `reference_manifest.yml` declares new shipped files
- [ ] `python scripts/validate_skills.py` passes
- [ ] `python scripts/token_budget.py --strict` passes
- [ ] Runtime validator tests pass (if runtime files changed)

## Example: Phase 4A Integration

The `contextsmith-run` skill integration added exactly three compact elements:

1. **Validation Gate subsection** — compact CLI reference table (4 lines)
2. **Evidence Ledger subsection** — instruction to emit JSON artifacts (2 lines)
3. **Execution Workflow step 9** — runtime validation step (1 line)

Total addition: ~7 lines. The validator and domain packs handle the enforcement.

## When Thin Is Not Enough

Some skills genuinely need more instruction — new workflows, complex decision trees, or domain-specific behavior. In these cases:

1. Write the detailed instruction in a separate reference file
2. Add a single SKILL.md paragraph pointing to the reference
3. Declare the reference in `reference_manifest.yml`

The skill remains thin. The detail lives in a shipped reference.
