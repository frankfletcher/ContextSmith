# PLAN.md

## Phases

### Phase 1: Schema Registry Design

- Status: completed

#### Sub-phase 1.1: YAML structure

- Status: completed
- Context Budget: 16k
- Validation: yaml_valid
- Tasks:
  - [x] Define YAML structure for artifact schemas
  - [x] Add metadata, descriptions, and examples

#### Sub-phase 1.2: All artifact schemas

- Status: completed
- Context Budget: 32k
- Tasks:
  - [x] Draft schemas for STATUS.md, PLAN.md, CONTEXT.md
  - [x] Draft schemas for PHASE_LOG.md, EDUCATIONAL_REPORT.md, AUDIT_REPORT.md
  - [x] Draft schemas for DECISIONS.md, ARTIFACTS.md, CHECKLIST.md
  - [x] Draft schemas for TASK.md, NEXT_PROMPT.md

### Phase 2: Validator Refactor

- Status: completed

#### Sub-phase 2.1: Schema loading

- Status: completed
- Context Budget: 24k
- Validation: |pytest tests/test_validators.py::TestLoadArtifactSchemas|
- Tasks:
  - [x] Add load_artifact_schemas()
  - [x] Add validate_artifact_schema()
  - [x] Add validate_artifacts_with_schemas()

#### Sub-phase 2.2: Phase tree validation

- Status: completed
- Context Budget: 24k
- Validation: |pytest tests/test_validators.py::TestValidatePhaseTreeStructure|
- Tasks:
  - [x] Add validate_phase_tree_structure()
  - [x] Add validate_plan_phase_order()

### Phase 3: State Reader Refactor

- Status: completed

#### Sub-phase 3.1: Hierarchical parsing

- Status: completed
- Context Budget: 24k
- Validation: |pytest tests/test_orchestrator_state.py::TestParsePhaseTree|
- Tasks:
  - [x] Add _parse_phase_tree() with 3-level hierarchy
  - [x] Preserve flat checkbox backward compatibility
  - [x] Add current_subphase to read_status()

### Phase 4: Step Compiler and StepContract

- Status: completed

#### Sub-phase 4.1: StepContract fields

- Status: completed
- Context Budget: 16k
- Tasks:
  - [x] Add subphase_name and subphase_context_budget to StepContract

#### Sub-phase 4.2: Sub-phase budget extraction

- Status: completed
- Context Budget: 16k
- Validation: |pytest tests/test_step_compiler.py::TestExtractSubphaseBudget|
- Tasks:
  - [x] Add _extract_subphase_budget() helper
  - [x] Pass current_subphase to compile_step_contract()

### Phase 5: Orchestrator Sub-phase Advancement

- Status: completed

#### Sub-phase 5.1: Status and prompt updates

- Status: completed
- Context Budget: 24k
- Tasks:
  - [x] Update _rewrite_status_content for Current Sub-phase
  - [x] Update _update_status for sub-phase parameter
  - [x] Update _generate_next_prompt with sub-phase task list

#### Sub-phase 5.2: Sub-phase dispatch loop

- Status: completed
- Context Budget: 24k
- Tasks:
  - [x] Add _try_advance_subphase()
  - [x] Add _find_phase_in_plan() and _find_first_subphase()
  - [x] Insert sub-phase advancement in run() after execution

### Phase 6: Unit Test Coverage

- Status: completed

#### Sub-phase 6.1: State reader tests

- Status: completed
- Context Budget: 16k
- Validation: |pytest tests/test_orchestrator_state.py::TestParsePhaseTree|
- Tasks:
  - [x] Test hierarchical parsing
  - [x] Test flat format backward compat
  - [x] Test context budget extraction

#### Sub-phase 6.2: Validator tests

- Status: completed
- Context Budget: 16k
- Validation: |pytest tests/test_validators.py::TestValidatePhaseTreeStructure tests/test_validators.py::TestValidatePlanPhaseOrder|
- Tasks:
  - [x] Test phase tree structure validation
  - [x] Test plan/config phase order cross-reference
  - [x] Test invalid status detection

#### Sub-phase 6.3: Step compiler tests

- Status: completed
- Context Budget: 16k
- Validation: |pytest tests/test_step_compiler.py::TestExtractSubphaseBudget|
- Tasks:
  - [x] Test budget extraction from metadata
  - [x] Test missing budget handling
  - [x] Test sub-phase not found

### Phase 7: Workflow Config Schema Update

- Status: completed

#### Sub-phase 7.1: artifact_schemas extension

- Status: completed
- Context Budget: 16k
- Tasks:
  - [x] Add artifact_schemas section to workflow_config.schema.json
  - [x] Define extension mechanism for workflow-specific overrides
  - [x] Validate JSON schema syntax

### Phase 8: Integration Tests

- Status: completed

#### Sub-phase 8.1: Sub-phase advancement test

- Status: completed
- Context Budget: 32k
- Tasks:
  - [x] Add test for _try_advance_subphase with pending sub-phases
  - [x] Add test for _try_advance_subphase returns None on all done
  - [x] Add test for backward compat with flat plan

### Phase 9: Documentation

- Status: completed

#### Sub-phase 9.1: Schema registry docs

- Status: completed
- Context Budget: 24k
- Tasks:
  - [x] Write docs/reference/ARTIFACT_SCHEMAS.md
  - [x] Document PLAN.md hierarchical format
  - [x] Add examples of sub-phase structure

#### Sub-phase 9.2: Changelog

- Status: completed
- Context Budget: 8k
- Tasks:
  - [x] Update CHANGELOG.md
  - [x] Run markdownlint on all docs

### Phase 10: Final Audit and Validation

- Status: completed

#### Sub-phase 10.1: Implementation plan audit

- Status: completed
- Context Budget: 16k
- Tasks:
  - [x] Run implementation plan audit
  - [x] Fix any must-fix items

#### Sub-phase 10.2: Full validation

- Status: completed
- Context Budget: 16k
- Tasks:
  - [x] uv run python scripts/validate_skills.py
  - [x] uv run ruff check orchestrator/ --select E,F,W,I | uv run python scripts/lint_error_counter.py
  - [x] uv run ruff format orchestrator/ --check
  - [x] uv run pytest tests/ -v
  - [x] markdownlint . --ignore node_modules | uv run python scripts/lint_error_counter.py

### Phase 11: Tooling and Audit Infrastructure

- Status: completed

#### Sub-phase 11.1: Extra-audit workflow config

- Status: completed
- Context Budget: 8k
- Tasks:
  - [x] Create .contextsmith/audit-with-extra.json workflow config [PRE-EXISTING]
  - [x] Validate config against schema — PASS
  - [x] Test with dry run — PASS

#### Sub-phase 11.2: Lint counter integration

- Status: completed
- Context Budget: 8k
- Tasks:
  - [x] Document lint_error_counter.py usage — AGENTS.md Repository Map + description
  - [x] Verify AGENTS.md validation commands include counter piping — confirmed
  - [x] Add reset/view instructions — reset command added

#### Sub-phase 11.3: Decision records backfill

- Status: completed
- Context Budget: 8k
- Tasks:
  - [x] Add DECISIONS.md entries — D9/D10/D12/D14 all present
  - [x] Update CONTEXT.md Key Files — all present

#### Sub-phase 11.4: Documentation and cleanup

- Status: completed
- Context Budget: 16k
- Tasks:
  - [x] Verify .agent_work/tmp/ exists and is gitignored
  - [x] Run full validation suite — all 5 pass
  - [x] Update CHANGELOG.md — v2.2.0

### Phase 12: Packaging and Distribution

- Status: completed
- Architecture: Layer-based packaging — core → distribution → plugin system → CI/CD → version → runtime commitment → refactor

#### Sub-phase 12.1: Core packaging

- Status: completed
- Context Budget: 16k
- Validation: |pip install -e . && contextsmith --help && python -m orchestrator --help|
- Tasks:
  - [ ] Fix `requires-python` in pyproject.toml: relax from `>=3.14` to `>=3.10`
  - [ ] Move `pytest`, `ruff` from `[project.dependencies]` to `[project.optional-dependencies] dev`
  - [ ] Add `[build-system]` with hatchling backend
  - [ ] Add `[project.scripts]`: `contextsmith = "orchestrator.cli:main"`
  - [ ] Add `[project.urls]`: Homepage, Repository, Documentation, Issues
  - [ ] Verify `contextsmith --help` works after `pip install -e .`
  - [ ] Verify `python -m orchestrator --help` same output
  - [ ] Add README.md install section: `pip install contextsmith`, `pipx install contextsmith`, adapter extras note
  - [ ] Test install from clean venv (not just dev venv)

#### Sub-phase 12.2: Distribution packaging

- Status: completed
- Context Budget: 16k
- Validation: |bash scripts/test_release.sh|
- Tasks:
  - [x] Update `build_release.py`:
    - [x] Add `--wheel` flag that builds Python wheel via `pyproject-build`
    - [x] Ensure wheel goes to `dist/` alongside skill zips (no conflict)
    - [x] Ensure existing skill-zip logic unchanged
  - [x] Fix `test_release.sh`:
    - [x] Replace `contextsmith-run` with `contextsmith-workflow-developer` in expected skills list
    - [x] Add Step 10: wheel install test — fresh venv, `pip install` the wheel, `contextsmith --help`, uninstall
  - [x] Add `.github/workflows/publish.yml`:
    - [x] Trigger: tag push `v*.*.*`
    - [x] Build wheel + sdist via `pypa/build`
    - [x] Publish to PyPI using trusted publishing
    - [x] Run skill-zip pipeline, attach zips to GitHub release
  - [x] Run `test_release.sh` end-to-end — all steps pass
  - [x] Run `build_release.py --package --individual --wheel` and verify `dist/` output

#### Sub-phase 12.3: Adapter plugin system

- Status: completed
- Context Budget: 16k
- Validation: |pytest tests/test_adapter_discovery.py -v|
- Tasks:
  - [x] Add `[project.entry-points."contextsmith.adapters"]` in pyproject.toml:
    - [x] `opencode = "orchestrator.adapters.opencode"`
    - [x] `generic = "orchestrator.adapters.generic"`
  - [x] Add `[project.optional-dependencies]` harness extras (establishes convention):
    - [x] `opencode = []`
    - [x] `generic = []`
  - [x] Rewrite `discover_adapters()` in `adapters/__init__.py`:
    - [x] Iterate `importlib.metadata.entry_points(group="contextsmith.adapters")`
    - [x] Call `ep.load()` on each to import module and trigger self-registration
    - [x] Remove hardcoded `ADAPTER_REGISTRY` list entirely
  - [x] Add `tests/test_adapter_discovery.py`:
    - [x] Test `discover_adapters()` registers both built-in adapters via entry points
    - [x] Test `HarnessRegistry.get("opencode")` returns OpenCodeAdapter
    - [x] Test `HarnessRegistry.get("generic")` returns GenericAdapter
    - [x] Test unknown harness name raises KeyError
  - [x] Run full test suite — all pass

#### Sub-phase 12.4: CI/CD full pipeline

- Status: completed
- Context Budget: 16k
- Validation: |act pull_request -W .github/workflows/validate.yml|
- Tasks:
  - [x] Add `.github/workflows/validate.yml`:
    - [x] Trigger: push to main, pull_request to main
    - [x] Strategy matrix: python-version [3.10, 3.11, 3.12] on ubuntu-latest
    - [x] Steps: checkout → setup-python → pip install .[dev] → validate_skills → ruff check → ruff format --check → pytest → markdownlint (scoped .agent_work/ orchestrator/ docs/ --ignore node_modules) → changelog lint
    - [x] Dependency caching for pip
    - [x] Cancel-in-progress: true
  - [x] Add `.pre-commit-config.yaml`:
    - [x] Repos: ruff (check + format), pre-commit-hooks (trailing-whitespace, check-yaml, end-of-file-fixer)
    - [x] Document `pre-commit install` in AGENTS.md
  - [x] Add changelog lint script `scripts/lint_changelog.py`:
    - [x] Regex-based keepachangelog format validation
    - [x] Checks: top-level sections present, version headers match semver, no unreleased section empty
    - [x] Add to validate.yml step list
  - [x] Verify validate.yml syntax with `act` or manual review

#### Sub-phase 12.5: Version consolidation

- Status: completed
- Context Budget: 8k
- Validation: |python scripts/validate_version_consistency.py|
- Tasks:
  - [x] Set pyproject.toml `version` as canonical source
  - [x] Update PACKAGE_SPEC.md version to match pyproject.toml
  - [x] Update all skill metadata.version to match project version
  - [x] Update CHANGELOG.md header if needed
  - [x] Add `scripts/validate_version_consistency.py`:
    - [x] Reads pyproject.toml for canonical version
    - [x] Checks PACKAGE_SPEC.md, all skill SKILL.md frontmatter match
    - [x] Returns non-zero exit on mismatch
  - [x] Add version consistency check to validate.yml

#### Sub-phase 12.6: Orchestrator-as-runtime commitment

- Status: completed
- Context Budget: 16k
- Validation: |pytest tests/test_orchestrator_integration.py::TestMergeNewArtifactSegments|
- Tasks:
  - [x] Evaluate D14 gate: condition 1 MET (5 end-to-end tests exist for _merge_new_artifact_segments)
  - [x] Evaluate D14 gate: condition 2 MET (user commitment — orchestrator is production runtime)
  - [x] Add D14_GATE_PASSED sentinel to .agent_work/ (checked by agents on session start)
  - [x] Update AGENTS.md: stop manual .new merging, orchestrator handles it
  - [x] Update CONTEXT.md: orchestrator gap note → orchestrator IS the runtime
  - [x] Update DECISIONS.md: mark D12/D14 as resolved, add D15 commitment
  - [x] Verify `_merge_new_artifact_segments` fires in production path in orchestrator.run()

#### Sub-phase 12.7: Complexity refactor

- Status: completed
- Context Budget: 16k
- Validation: |uvx radon cc orchestrator/ -s -a | grep -E " - [CDEF] "| (must find none)|
- Tasks:
  - [x] Extract sub-phase dispatch from `orchestrator.run()` (lines ~940-960)
  - [x] Extract checkpoint persistence from `orchestrator.run()` (lines ~713-745)
  - [x] Verify cyclomatic complexity drops to ≤ B across all orchestrator/
  - [x] Run full test suite — all pass
