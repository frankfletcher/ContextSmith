## Phase 7 — What You Need to Know

### What Changed
This phase introduced automated validation for the skill manifests and set up Continuous Integration (CI) to ensure code quality.

1.  **Modified `scripts/validate_skills.py`**:
    *   Added a new `validate_manifest()` function.
    *   This function reads the `reference_manifest.yml` file for each skill.
    *   It checks that the manifest is valid YAML, has the correct structure, lists all required files, and ensures no duplicate file references.
    *   It verifies that every file listed in the manifest actually exists on disk (either in `shared/` or the skill's local directory).

2.  **Created `.github/workflows/validate.yml`**:
    *   This is a GitHub Actions workflow file.
    *   It automatically runs every time code is pushed to the `main` branch or a pull request is opened.
    *   It installs Python dependencies (PyYAML) and runs two critical scripts: `sync_shared_refs.py` (to populate reference files) and `validate_skills.py` (to check everything is correct).

### Design Decisions
*   **Why validate the manifest structure?**
    A manifest is a "contract" defining what a skill needs. If the contract is broken (e.g., missing a file or having duplicate entries), the skill might not work correctly. Automated validation catches these errors before they reach users.
*   **Why run `sync_shared_refs.py` before validation in CI?**
    The validation script checks if files exist in the `references/` directory. Since that directory is gitignored (generated content), it's empty on a fresh clone. Syncing ensures the directory is populated before we try to validate it.
*   **Why not check file content versions?**
    The plan (D-006) specifies that the validation script checks *structure*, not *freshness*. Freshness is handled by the sync script, which compares file hashes. This separation of concerns keeps the validation script simple and fast.

### Trade-Offs
*   **No Linting in CI**: We did not add a Python linter (like `ruff` or `flake8`) to the CI workflow. This keeps the setup simple and avoids adding new dependencies. Code style is enforced during manual code review.
*   **Simple Error Reporting**: The validation script prints errors to the console but doesn't generate a detailed report file. For a large project, you might want to output JSON or XML for CI dashboards, but for this scope, console output is sufficient.

### Key Lessons for a New Intern
1.  **The "Manifest Pattern"**:
    You will see this pattern often in software engineering: a file (the manifest) lists dependencies, and a script reads that list to perform actions (copying, validating, installing).
    *   **Why use it?** It separates *what* is needed from *how* to get it. This makes automation possible.
    *   **Real-world example**: `package.json` in Node.js or `requirements.txt` in Python.

2.  **Continuous Integration (CI)**:
    The `.github/workflows/validate.yml` file is a CI configuration.
    *   **Why use it?** It prevents "it works on my machine" syndrome. By running tests and validation on a clean environment every time code changes, you catch bugs early.
    *   **Lesson**: Always add CI to a project as soon as possible. It saves hours of debugging later.

3.  **Validation Layers**:
    We have three layers of validation:
    *   **Layer 1 (Manifest)**: Defines the requirements.
    *   **Layer 2 (Sync Script)**: Enforces requirements by copying files.
    *   **Layer 3 (Validation Script)**: Verifies that the requirements are met.
    *   **Lesson**: Redundant checks seem tedious but are crucial for reliability. If one layer fails, the next catches it.

### Edge Cases Not Handled
*   **Path Conventions**: The validation assumes `source` paths in the manifest are relative to the repository root. This works for our structure but could break if the manifest format changes.
*   **CI Linting**: As mentioned, we don't lint the Python code itself in CI. A syntax error in the validation script would cause the CI to fail, but we rely on human review to prevent syntax errors.

### Next Phase Preview
Phase 8 is the final phase. We will run a full end-to-end test of the entire system, create a `CONTRIBUTING.md` file for future developers, and prepare the final handoff report. This phase depends on Phase 7 because the CI workflow is essential for the final end-to-end validation.