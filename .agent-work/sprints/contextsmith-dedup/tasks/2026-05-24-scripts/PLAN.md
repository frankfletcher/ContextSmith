# Implementation Plan — ContextSmith Reference Deduplication Artifacts

**Created:** 2026-05-24
**Target executor:** Qwen 3.6 27B (local-model coding agent)
**Phases:** 8
**Repository root:** ContextSmith/
**Task state dir:** `.agent-work/sprints/contextsmith-dedup/tasks/2026-05-24-scripts/`

---

## Phase Outline

| Phase | Title | Primary Deliverable |
|---|---|---|
| P1 | Repo Inspection and State Setup | `CONTEXT.md`, `TASK.md`, `STATUS.md`, `DECISIONS.md`, `PLAN.md` (this file) |
| P2 | Manifest Specification + First Skill Manifest | YAML schema finalized + `skills/local-model-prompt-engineer/reference_manifest.yml` |
| P3 | All Remaining Skill Manifests | 4 `reference_manifest.yml` files for remaining skills + `help.md` relocation |
| P4 | Sync Script | `scripts/sync_shared_refs.py` |
| P5 | Sync Verification, Copy Removal, and .gitignore | Verified sync output; deleted copies; `.gitignore` rules; `.gitkeep` files |
| P6 | Package Script | `scripts/package_skill.sh` |
| P7 | Validation Enhancement and CI Workflow | Updated `scripts/validate_skills.py` + `.github/workflows/validate.yml` |
| P8 | End-to-End Validation, Documentation, and Handoff | `CONTRIBUTING.md`; full integration test; final report |

---

## Repository Context (from Inspection)

- **52 shared files**: 35 root-level `.md` + 8 in `shared/domain-profiles/` + 4 in `shared/model-profiles/`
- **5 skills**, each with 52 shared copies + 1 `help.md` in `references/` = 265 files total
- **No version metadata** in any shared file → use `git hash-object` SHA-1 blob hashes
- **No `help.md` in shared/** — it is per-skill, unique to each skill
- **`.gitignore`** is empty (0 bytes)
- **`.github/`** does not exist
- **`CONTRIBUTING.md`** does not exist

---

## Universal Phase Protocols

Every phase P1–P8 ends with the same three activities. The plan mentions them per phase, but this section defines HOW to execute them. Read this once before starting P1 — it applies to every phase.

---

### Protocol A: Deep Phase Review

After the phase's validation passes, perform a code review on the files changed this phase. Do NOT expand scope beyond what the phase delivered.

**Step 1 — Inspect the diff:**
```bash
git diff                    # unstaged changes
git diff --staged           # staged changes (if any)
git diff --stat             # compact file list
```

**Step 2 — Review only files changed this phase.** Unless a broader inspection is required to verify correctness, review only the files listed in `git diff --stat`. Do not re-read the whole repo.

**Step 3 — Check each file for:**
- Correctness: does it do what the phase intended?
- Edge cases: does it handle the edge cases listed in the phase's "Edge Case Catalog" or appendix?
- Test coverage: do the phase's validation commands actually exercise the code?
- Style: PEP 8 for Python, 4-space indent, no trailing whitespace, snake_case
- Security: no hardcoded paths, no secrets, no shell injection in subprocess calls
- Project conventions: matches `CONTEXT.md` skip rules, uses pathlib not string paths, no new dependencies

**Step 4 — Classify each finding:**
| Label | Meaning |
|---|---|
| `MUST FIX` | Breaks correctness, validation, or safety. Phase is NOT complete until fixed. |
| `SHOULD FIX` | Weakens maintainability or test strength. Fix in this phase if < 5 minutes. |
| `NOTE` | Acceptable now, flag for later. Mention in education report. |
| `ACCEPTABLE` | Intentional trade-off. Document in education report's "Trade-Offs" section. |

**Step 5 — Apply at most ONE focused improvement pass.** Fix MUST FIX items first. If no MUST FIX, fix the highest-impact SHOULD FIX. Do NOT expand scope, refactor unrelated code, or add features not in the plan.

**Step 6 — Re-run the phase's narrowest validation.** Confirm the fix did not regress. Re-run only the validation commands listed in the phase, not the full pipeline.

**Step 7 — Record review in `PHASE_LOG.md`:**
```markdown
## Phase N Code Review
- Files reviewed: <list>
- Validation run: <command and result>
- Overall: pass | fix-first | needs-human
- MUST FIX: <list or "none">
- SHOULD FIX: <list or "none">
- NOTES: <list or "none">
- Improvements applied: <what was fixed in step 5>
- Remaining risks: <what is still known to be imperfect>
```

---

### Protocol B: Education-Level Report

After the phase review, write one education report per phase. This is separate from the code review — it's for the human reading the project later.

**When:** After Protocol A is complete and validation re-passes.

**Where:** `reports/phase-N-education.md` under the task state directory.

**Template (defined in P2, reproduced here for completeness):**
```markdown
## Phase N — What You Need to Know

### What Changed
(new files, modified files — one line each)

### Design Decisions
(alternatives considered and reason for each choice — 1-2 sentences per decision)

### Trade-Offs
(what was sacrificed for simplicity, speed, or maintainability — 1-2 sentences)

### Key Lessons
(1 concept or pattern reusable beyond this project)

### Edge Cases Not Handled
(1-3 bullet points of known gaps)

### Next Phase Preview
(one sentence: what the next phase builds, why it depends on this phase)
```

**Constraints:**
- Keep the report under 500 words. It is educational, not operational.
- Do NOT paste code, raw output, or full file content. Summarize.
- If nothing educational happened (e.g., P1 is pure verification), write a 3-sentence summary: "This phase verified repo state. No design decisions needed. All assumptions confirmed."

---

### Protocol C: Ralph-Loop Iteration Gate

The Ralph loop rule applies to the deep phase review, not to the phase's primary work.

**Rule:** Re-iterate on the phase's deliverables only if it **materially improves a graded weakness**. Do not re-iterate for cosmetic polish, minor style, or "just in case" refactoring.

**Decision matrix:**
| If... | Then... |
|---|---|
| Any `MUST FIX` found | Re-iterate. Fix all MUST FIX. Then stop. |
| Any `SHOULD FIX` found that takes < 5 min | Fix it in the improvement pass (Protocol A, Step 5). |
| Only `NOTE` or `ACCEPTABLE` | Stop. Record and move on. |
| Phase validation fails | Fix and re-run validation. This is not a Ralph iteration — it's completing the phase. |

**Stop condition:** Stop iterating when all MUST FIX are resolved and re-validation passes. One improvement pass is the budget. Do not chain multiple "polish" passes.

---

### Protocol D: Phase Closeout Checklist

At the end of every phase, before updating STATUS.md to "complete," run this checklist:

1. [ ] Phase validation re-passes (after any review fixes).
2. [ ] `PHASE_LOG.md` has the phase review entry (Protocol A, step 7).
3. [ ] Education report written to `reports/phase-N-education.md` (Protocol B).
4. [ ] `STATUS.md` updated: phase marked complete, next phase listed, blockers recorded.
5. [ ] `NEXT_PROMPT.md` rewritten for the next phase. Format:
   ```markdown
   ## Resume Prompt
   Phase: <N> — <title>
   Completed: yes | partial | blocked
   Last validation: <command> — <result>
   Active files: <list of files created/modified this phase>
   Next action: <first task of next phase>
   Blockers: <list or "none">
   Start by reading STATUS.md, CONTEXT.md, and PLAN.md Phase <N+1>.
   ```
6. [ ] If scope, constraints, or decisions changed, update `TASK.md` or `DECISIONS.md`.
7. [ ] `git status --short` reviewed. Unstaged work from this phase is expected. No unrelated files are modified.

Only after all 7 items are checked: mark STATUS.md complete and begin the next phase.

---

## Phase 1: Repo Inspection and State Setup

### Goal
Capture complete repository state, initialize task state files, and verify all assumptions.

### Inputs
- This plan document (from user prompt)
- `AGENTS.md` (repo conventions)
- Repository directory structure (via glob)

### Likely Files
- `.agent-work/sprints/contextsmith-dedup/tasks/2026-05-24-scripts/TASK.md` — CREATE
- `.agent-work/sprints/contextsmith-dedup/tasks/2026-05-24-scripts/STATUS.md` — CREATE
- `.agent-work/sprints/contextsmith-dedup/tasks/2026-05-24-scripts/CONTEXT.md` — CREATE
- `.agent-work/sprints/contextsmith-dedup/tasks/2026-05-24-scripts/DECISIONS.md` — CREATE
- `.agent-work/sprints/contextsmith-dedup/tasks/2026-05-24-scripts/PLAN.md` — CREATE (this file)

### Tasks
1. Read the **Universal Phase Protocols** section above (Protocols A–D). These apply to every phase including this one.
2. Verify 5 skill directories exist and each has `SKILL.md` + `references/` directory.
3. Verify 52 files exist in `shared/` with the correct subdirectory structure.
4. Run `python scripts/validate_skills.py` to capture baseline validation state.
5. For each of the 5 skills, list every file under `references/` recursively.
6. For each shared file, compute `git hash-object` and record the blob hash. Store in `CONTEXT.md` as a reference table.
7. Identify files in `references/` that have NO counterpart in `shared/` (should only be `help.md`).
8. Verify `help.md` is skill-specific by diffing each skill's `help.md` against the others. Record whether they differ.
9. Confirm `.gitignore` is empty (0 bytes).
10. Confirm `.github/` does not exist.
11. Confirm `CONTRIBUTING.md` does not exist.

### Outputs
- `TASK.md` with objective, scope, constraints
- `STATUS.md` with current phase
- `CONTEXT.md` with file map, constraints, skip rules
- `DECISIONS.md` with versioning strategy and other design decisions
- `PLAN.md` (this file)

### Validation
1. `python scripts/validate_skills.py` runs without errors.
2. All 52 shared files exist and are readable.
3. All 5 skill `references/` directories contain the expected files.
4. `git hash-object` returns consistent SHA-1 hashes for each shared file.
5. `help.md` file differences recorded.

### Stop Condition
All task state files written. All repo verification checks pass. `STATUS.md` shows P1 complete and P2 as next phase.

### Do Not Carry Forward
- Do not carry forward any assumptions about file contents. Only file existence and paths are relevant.

---

## Phase 2: Manifest Specification + First Skill Manifest

### Goal
Create `reference_manifest.yml` for `local-model-prompt-engineer` with correct blob hashes. The complete YAML with placeholder hashes is provided below — the implementor fills in real hashes using the helper script.

### Inputs
- `skills/local-model-prompt-engineer/references/` — file listing from P1
- `shared/` — all 52 files (hash computation target)
- `DECISIONS.md` — D-001 (versioning), D-002 (help.md placement), D-003 (local field)

### Likely Files
- `skills/local-model-prompt-engineer/reference_manifest.yml` — CREATE

### Tasks

#### 2a. Compute Blob Hashes for All 52 Shared Files

Run this from the repo root. It produces the 52 `source`/`version` lines you paste into the manifest:

```bash
python -c "
import hashlib, glob
for f in sorted(glob.glob('shared/**/*.md', recursive=True)):
    content = open(f, 'rb').read()
    h = hashlib.sha1(f'blob {len(content)}\0'.encode() + content).hexdigest()
    print(f'  - source: {f}')
    print(f'    version: \"{h}\"')
"
```

Save the output to paste into the manifest template below.

#### 2b. Compute Hash for help.md

```bash
python -c "
import hashlib
content = open('skills/local-model-prompt-engineer/references/help.md', 'rb').read()
h = hashlib.sha1(f'blob {len(content)}\0'.encode() + content).hexdigest()
print(h)
"
```

Save this hash for the `help.md` entry.

#### 2c. Required Status — Concrete Answer

P1 verified all 5 skills copy all 52 shared files. Every skill's SKILL.md uses catch-all instructions like "use references/..." rather than naming individual files. **Mark ALL 52 shared entries as `required: true`.** The `required` field can be refined in a future profiling pass.

#### 2d. Write the Manifest

Use the template below. Paste the 52 computed hash lines over the placeholders. Paste the `help.md` hash into its `version` field:

```yaml
skill: local-model-prompt-engineer
version: 1.0.0
description: Shared reference dependencies for the Prompt Engineer skill.

references:
  # === Safety & safeguards ===
  - source: shared/git-safety.md
    version: "<PASTE-HASH>"
    required: true
    notes: Git safety rules for coding/repo prompts.

  - source: shared/loop-safety.md
    version: "<PASTE-HASH>"
    required: true
    notes: Agentic loop safety rules.

  - source: shared/evaluation-rubrics.md
    version: "<PASTE-HASH>"
    required: true
    notes: A-F grading for Ralph-loop iteration.

  - source: shared/side-effect-matrix.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/instruction-conflicts.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/instruction-deduplication.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/instruction-precedence.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/upstream-artifact-audit.md
    version: "<PASTE-HASH>"
    required: true

  # === Planning & execution ===
  - source: shared/phased-planning.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/phase-code-review.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/phase-compression.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/persistent-task-state.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/implementation-plan-audit.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/test-quality-audit.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/planner-executor-workflows.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/small-context-workflows.md
    version: "<PASTE-HASH>"
    required: false

  # === Context management ===
  - source: shared/context-management.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/targeted-context-length.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/reference-optimization.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/output-location.md
    version: "<PASTE-HASH>"
    required: true

  # === Model profiles ===
  - source: shared/model-profiles/qwen36.md
    version: "<PASTE-HASH>"
    required: true
    notes: Primary target model profile.

  - source: shared/model-profiles/gemma4.md
    version: "<PASTE-HASH>"
    required: false
    notes: Secondary target.

  - source: shared/model-profiles/llama3.md
    version: "<PASTE-HASH>"
    required: false
    notes: Secondary target.

  - source: shared/model-profiles/generic-local.md
    version: "<PASTE-HASH>"
    required: true
    notes: Default fallback profile.

  - source: shared/model-capability-tiers.md
    version: "<PASTE-HASH>"
    required: true

  # === Domain profiles ===
  - source: shared/domain-profiles/coding.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/domain-profiles/data-science-ml.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/domain-profiles/ai-modalities.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/domain-profiles/documents.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/domain-profiles/email.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/domain-profiles/research.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/domain-profiles/scheduling.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/domain-profiles/purchasing-tickets.md
    version: "<PASTE-HASH>"
    required: false

  # === Quality & standards ===
  - source: shared/documentation-quality.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/coding-standards.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/ui-standards.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/git-hygiene.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/engineering-metadata.md
    version: "<PASTE-HASH>"
    required: true

  # === Workflow & interaction ===
  - source: shared/ralph-loop.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/subagent-delegation.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/skill-interoperability.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/small-model-atomicity.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/interaction-modes.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/control-parameters.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/control-phrases.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/help-mode.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/usage-patterns.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/run-configuration-preview.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/runtime-stability.md
    version: "<PASTE-HASH>"
    required: false

  - source: shared/domain-intent.md
    version: "<PASTE-HASH>"
    required: true

  # === Education ===
  - source: shared/education-levels.md
    version: "<PASTE-HASH>"
    required: true

  - source: shared/educational-report.md
    version: "<PASTE-HASH>"
    required: true

  # === Skill-local file ===
  - source: skills/local-model-prompt-engineer/help.md
    version: "<PASTE-HELP-HASH>"
    required: true
    local: true
    notes: Skill-specific help documentation.
```

#### 2e. Verify Manifest

```bash
python -c "import yaml; yaml.safe_load(open('skills/local-model-prompt-engineer/reference_manifest.yml'))"
```
- No YAML parse errors.
- No `<PASTE-HASH>` placeholders remain (all replaced with real hashes).
- Total entries: 53. No duplicate sources.

### Outputs
- `skills/local-model-prompt-engineer/reference_manifest.yml` — created and validated

### Validation
```bash
python -c "import yaml; yaml.safe_load(open('skills/local-model-prompt-engineer/reference_manifest.yml'))" && echo "OK"
```
- YAML parses. No placeholders. 53 entries.

### Stop Condition
Manifest created with all hashes filled. `STATUS.md` shows P2 complete.

### Do Not Carry Forward
- Do not carry forward the assumption that all files are `required: true` to other skills without verification. (But P3 will verify and find the same answer.)

### Education Report Template

Use this template for ALL phase education reports (P2 through P8). Write to `reports/phase-N-education.md`:

```markdown
## Phase N — What You Need to Know

### What Changed
(new files, modified files — one line each)

### Design Decisions
(alternatives considered and reason for each choice — 1-2 sentences per decision)

### Trade-Offs
(what was sacrificed for simplicity, speed, or maintainability — 1-2 sentences)

### Key Lessons
(1 concept or pattern reusable beyond this project)

### Edge Cases Not Handled
(1-3 bullet points of known gaps)

### Next Phase Preview
(one sentence: what the next phase builds, why it depends on this phase)
```

### Deep Phase Review (P2)

**Files reviewed:** `skills/local-model-prompt-engineer/reference_manifest.yml`

**Review checklist:**
- [ ] YAML parses without error
- [ ] No `<PASTE-HASH>` placeholders remain
- [ ] All 52 shared files present (check against appendix list)
- [ ] `help.md` entry has `local: true` and source points to skill root
- [ ] Hash algorithm matches `compute_blob_hash` in P4 (git-compatible: `blob <size>\0` prefix)
- [ ] All `required: true` (per 2c concrete answer)
- [ ] `notes` present for: git-safety, loop-safety, evaluation-rubrics, qwen36
- [ ] Manifest `version` field is `1.0.0`

**Unusual checks:**
- Pick 3 random shared files. Verify: `git hash-object <file>` matches manifest `version`.

**Record review in `PHASE_LOG.md`.**

### Deep Education-Level Report (P2)
Write to `reports/phase-2-education.md` using the template above.

---

## Phase 3: All Remaining Skill Manifests

### Goal
Create `reference_manifest.yml` for the remaining 4 skills. Handle `help.md` relocation for all 5 skills (move from `references/` to skill root).

### Inputs
- `skills/local-model-prompt-engineer/reference_manifest.yml` — template from P2
- Remaining 4 skill `references/` directories — file listings from P1
- `skills/*/references/help.md` for each skill
- Blob hash table from P2

### Likely Files
- `skills/local-model-skill-engineer/reference_manifest.yml` — CREATE
- `skills/local-model-skill-migrator/reference_manifest.yml` — CREATE
- `skills/local-model-instruction-engineer/reference_manifest.yml` — CREATE
- `skills/local-model-agent-evaluator/reference_manifest.yml` — CREATE
- `skills/*/help.md` (5 files) — MOVE from `references/help.md` to skill root

### Tasks

#### 3a. Copy and Modify the P2 Manifest

P1 confirmed all 5 skills have identical reference sets. For each remaining skill:

1. Copy `skills/local-model-prompt-engineer/reference_manifest.yml` to the new skill directory.
2. Change the `skill` field to match the directory name.
3. Change the `help.md` entry's `source` to `skills/<skill>/help.md`.
4. Update `description` to match the skill's purpose.
5. Do NOT change the 52 shared file entries — same paths, same hashes, same `required: true`.

#### 3b. Relocate help.md Files

For each of the 5 skills:
1. Read `skills/<skill>/references/help.md` — note the content.
2. Write identical content to `skills/<skill>/help.md` (skill root).
3. Compute the blob hash of the NEW `skills/<skill>/help.md` using the same helper from P2:
   ```bash
   python -c "
   import hashlib
   content = open('skills/<skill>/help.md', 'rb').read()
   h = hashlib.sha1(f'blob {len(content)}\0'.encode() + content).hexdigest()
   print(h)
   "
   ```
4. Update the `help.md` entry's `version` in that skill's manifest to the computed hash.
5. Do NOT delete `references/help.md` — that happens in P5.

#### 3c. Validate All 5 Manifests

For each manifest:
1. Parse as YAML — no errors.
2. Every shared `source` path resolves to an existing file in `shared/`.
3. Every local `source` path resolves to an existing file in the skill root.
4. All blob hashes match freshly computed hashes.
5. No duplicate `source` entries within any manifest.
6. Total entries: 53 per manifest.

### Outputs
- 4 new `reference_manifest.yml` files
- 5 `help.md` files moved from `references/` to skill roots

### Validation
```bash
for skill in local-model-prompt-engineer local-model-skill-engineer local-model-skill-migrator local-model-instruction-engineer local-model-agent-evaluator; do
  python -c "
import yaml
with open('skills/$skill/reference_manifest.yml') as f:
    data = yaml.safe_load(f)
assert data['skill'] == '$skill', 'skill field mismatch'
assert len(data['references']) == 53, f'expected 53 entries, got {len(data[\"references\"])}'
sources = [r['source'] for r in data['references']]
assert len(sources) == len(set(sources)), 'duplicate sources'
print(f'$skill: OK — {len(data[\"references\"])} references')
"
done
```
- All 5 manifests parse and validate.
- All 5 skill roots contain `help.md` (moved).

### Stop Condition
All 5 manifests created and validated. `help.md` moved to all 5 skill roots. `STATUS.md` shows P3 complete.

### Do Not Carry Forward
- Do not carry forward the old `references/help.md` copies. They are stale after relocation. P5 will delete them.

### Deep Phase Review (P3)

**Files reviewed:** 4 new manifest files, 5 moved `help.md` files.

**Review checklist:**
- [ ] All 5 manifests have correct `skill` field matching directory name
- [ ] All 52 shared sources appear in all 5 manifests
- [ ] Blob hashes are consistent across manifests (same shared file = same hash)
- [ ] `local: true` on all `help.md` entries, `local: false` or absent on shared entries
- [ ] `help.md` content matches between old `references/help.md` and new `skills/<skill>/help.md`
- [ ] Help files differ between skills (or confirmed identical if same content)
- [ ] Manifest `version` is `1.0.0` for all

**Record review in `PHASE_LOG.md`.**

### Deep Education-Level Report (P3)
Write to `reports/phase-3-education.md` using the P2 education report template.

---

## Phase 4: Sync Script

### Goal
Create `scripts/sync_shared_refs.py` that reads manifests, copies shared files into `references/`, and handles local files. Verify with `--dry-run` and full sync against existing copies.

### Inputs
- All 5 `reference_manifest.yml` files from P2/P3
- All 52 `shared/` files
- All 5 `skills/*/help.md` files (moved to skill roots in P3)
- Blob hash table for comparison
- `DECISIONS.md` — D-004 (force flag), D-005 (dry-run)

### Likely Files
- `scripts/sync_shared_refs.py` — CREATE

### Tasks

#### 4a. Script Skeleton and Argument Parsing

Create the script with `argparse`:
```python
#!/usr/bin/env python3
"""sync_shared_refs.py — Populate skill references/ from shared/ via manifests."""

import argparse, os, shutil, sys
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description="Sync shared references to skill directories")
    parser.add_argument("--skill", help="Sync only one skill (directory name)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be copied")
    parser.add_argument("--verbose", action="store_true", help="Print each file operation")
    parser.add_argument("--force", action="store_true", help="Overwrite even if versions match")
    args = parser.parse_args()
    # ...
```

#### 4b. Core Copy Algorithm

```python
def compute_blob_hash(filepath):
    """Compute git-compatible blob hash."""
    import hashlib
    content = filepath.read_bytes()
    header = f'blob {len(content)}\0'.encode()
    return hashlib.sha1(header + content).hexdigest()

def sync_skill(skill_dir, args):
    manifest_path = skill_dir / 'reference_manifest.yml'
    if not manifest_path.exists():
        if args.verbose:
            print(f"SKIP {skill_dir.name}: no reference_manifest.yml")
        return {'copied': 0, 'skipped': 0, 'warnings': 1, 'errors': 0}

    try:
        manifest = yaml.safe_load(manifest_path.read_text())
    except yaml.YAMLError as e:
        print(f"ERROR {skill_dir.name}: invalid YAML in manifest: {e}")
        return {'copied': 0, 'skipped': 0, 'warnings': 0, 'errors': 1}

    stats = {'copied': 0, 'skipped': 0, 'warnings': 0, 'errors': 0}
    refs_dir = skill_dir / 'references'

    for entry in manifest.get('references', []):
        source = entry.get('source', '')
        required = entry.get('required', True)
        is_local = entry.get('local', False)

        if not required:
            continue

        src_path = REPO_ROOT / source
        if not is_local and not source.startswith('shared/'):
            print(f"ERROR {skill_dir.name}: source '{source}' not in shared/")
            stats['errors'] += 1
            continue

        if not src_path.exists():
            if required:
                print(f"ERROR {skill_dir.name}: required source not found: {source}")
                stats['errors'] += 1
            else:
                print(f"WARN {skill_dir.name}: optional source not found: {source}")
                stats['warnings'] += 1
            continue

        # Compute source hash and check manifest version freshness
        src_hash = compute_blob_hash(src_path)
        manifest_version = entry.get('version', '')
        if manifest_version and manifest_version != src_hash:
            print(f"WARN {skill_dir.name}: manifest version stale for {source} "
                  f"(stored={manifest_version[:8]}..., current={src_hash[:8]}...)")

        # Determine relative path under references/
        if is_local:
            dest_rel = src_path.name
        else:
            dest_rel = Path(source).relative_to('shared')
        dest_path = refs_dir / dest_rel

        if args.dry_run:
            print(f"WOULD COPY: {source} -> {dest_path}")
            stats['copied'] += 1
            continue

        # Check if destination exists and content matches source
        if not args.force and dest_path.exists():
            dest_hash = compute_blob_hash(dest_path)
            if dest_hash == src_hash:
                if args.verbose:
                    print(f"SKIP {source} -> {dest_path} (unchanged)")
                stats['skipped'] += 1
                continue

        # Create parent directories and copy
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dest_path)
        if args.verbose:
            print(f"COPY {source} -> {dest_path}")
        stats['copied'] += 1

    return stats
```

#### 4c. Main Loop

```python
def main():
    parser = argparse.ArgumentParser(...)
    args = parser.parse_args()

    skills_dir = REPO_ROOT / 'skills'
    total = {'copied': 0, 'skipped': 0, 'warnings': 0, 'errors': 0}

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        if args.skill and skill_dir.name != args.skill:
            continue

        stats = sync_skill(skill_dir, args)
        for k in total:
            total[k] += stats[k]

    print(f"Synced: {total['copied']} copied, {total['skipped']} skipped, "
          f"{total['warnings']} warnings, {total['errors']} errors")
    if total['errors'] > 0:
        sys.exit(1)
```

#### 4d. Key Implementation Details

1. **Path resolution**: `REPO_ROOT = Path(__file__).resolve().parents[1]` — works regardless of CWD.
2. **Subdirectory preservation**: `shared/model-profiles/qwen36.md` → `references/model-profiles/qwen36.md`. Use `Path(source).relative_to('shared')`.
3. **Local file destination**: `skills/<skill>/help.md` → `references/help.md` (just the filename).
4. **Manifest version check**: Compare `compute_blob_hash(source)` against `entry['version']`. Warn if mismatch. This catches stale manifests in CI.
5. **Copy skip logic**: Compare source hash against destination hash. If identical, skip (unless `--force`). Content-based, not manifest-version-based.
6. **Empty references/ creation**: `mkdir(parents=True, exist_ok=True)` — works on fresh clone.

#### 4e. Test Sync Script

1. Run `python scripts/sync_shared_refs.py --dry-run --verbose` against all skills.
2. Verify output shows copy operations for all 53 files per skill (52 shared + help.md).
3. Run `python scripts/sync_shared_refs.py --skill local-model-prompt-engineer --verbose`.
4. Verify all files were copied to `references/`.
5. Run sync again — should show all SKIP (unchanged).
6. Run sync with `--force` — should show all COPY again.
7. Compare generated `references/` files byte-for-byte against the existing copies.
8. Test error cases: missing manifest, missing source file, file outside shared/.

### Outputs
- `scripts/sync_shared_refs.py` — created, tested, byte-for-byte verified

### Validation
```bash
# 1. Dry-run reports correct file list
python scripts/sync_shared_refs.py --dry-run --skill local-model-prompt-engineer | wc -l
# Expect: 53 lines (one per file)

# 2. Full sync runs without error
python scripts/sync_shared_refs.py --verbose

# 3. Byte-for-byte comparison
for skill in skills/*/; do
  for f in shared/**/*.md; do
    rel=$(echo "$f" | sed 's|^shared/||')
    diff "$f" "$skill/references/$rel" || echo "MISMATCH: $skill $rel"
  done
done

# 4. Idempotent — second run skips all
python scripts/sync_shared_refs.py --verbose 2>&1 | grep -c "SKIP"
# Expect: 260 (5 skills x 52 shared) if all skipped
```

### Stop Condition
Sync script runs, produces byte-identical output to existing copies, idempotent on second run, handles error cases gracefully. `STATUS.md` shows P4 complete.

### Do Not Carry Forward
- Do not carry forward test output files. The `references/` content is not committed.
- Do not carry forward any assumptions about which files are optional. Use manifest data.

### Deep Phase Review (P4)

**Files reviewed:** `scripts/sync_shared_refs.py`

**Review checklist:**
- [ ] Blob hash uses `f'blob {len(content)}\0'.encode()` prefix (git-compatible)
- [ ] Manifest version is checked against `compute_blob_hash(source)` — warns on mismatch
- [ ] By default, re-copies if source content differs from destination content (content-based check)
- [ ] `--force` overwrites regardless of content match
- [ ] Subdirectory structure preserved (model-profiles/, domain-profiles/)
- [ ] Local files: source from skill root, dest as filename only
- [ ] `required: false` entries are skipped entirely
- [ ] Non-`shared/` source without `local: true` → error
- [ ] Missing required source → error (not silent)
- [ ] Missing optional source → warning (not error)
- [ ] `mkdir(parents=True, exist_ok=True)` for destination dirs
- [ ] `shutil.copy2` used (preserves metadata)
- [ ] Exit code 1 on errors, 0 otherwise (warnings are non-fatal)
- [ ] Works from any CWD (uses `REPO_ROOT`)
- [ ] No dependencies beyond stdlib + PyYAML
- [ ] PEP 8: 4-space indent, snake_case, docstring on compute_blob_hash

**Unusual checks:**
- Test from wrong CWD: `cd /tmp && python /path/to/ContextSmith/scripts/sync_shared_refs.py --dry-run --skill local-model-prompt-engineer`
- Test that `--dry-run` does NOT write files (check file mtimes unchanged).
- Test that empty manifest (missing `references` key) doesn't crash.
- Test stale manifest: change a shared file, run sync, verify WARN about stale version appears.

**Record review in `PHASE_LOG.md`.**

### Deep Education-Level Report (P4)
Write to `reports/phase-4-education.md` using the P2 education report template.

---

## Phase 5: Sync Verification, Copy Removal, and .gitignore

### Goal
Verify sync reproduces existing copies byte-for-byte, then safely remove all committed copies from `skills/*/references/` and add `.gitignore` rules. This is the irreversible transition phase — execution order is critical.

### Inputs
- `scripts/sync_shared_refs.py` from P4
- All 5 `reference_manifest.yml` from P2/P3
- Existing `skills/*/references/` directories with committed copies
- Empty `.gitignore`

### Likely Files
- `skills/*/references/` — DELETE all contents (keep directories)
- `skills/*/references/.gitkeep` — CREATE empty placeholder in each
- `.gitignore` — MODIFY (append rules)

### Tasks

#### 5a. Byte-for-Byte Verification (Pre-Removal Gate)

**CRITICAL: Do NOT proceed past this step unless every file matches.**

1. Run `python scripts/sync_shared_refs.py --verbose` to populate references from manifests.
2. For each skill, for each shared file, diff the newly synced copy against the original committed copy:
   ```bash
   for skill in local-model-prompt-engineer local-model-skill-engineer local-model-skill-migrator local-model-instruction-engineer local-model-agent-evaluator; do
     for f in shared/**/*.md; do
       rel="${f#shared/}"
       if ! diff -q "$f" "skills/$skill/references/$rel"; then
         echo "MISMATCH: skills/$skill/references/$rel"
       fi
     done
   done
   ```
3. Verify `help.md` copies: compare `skills/$skill/references/help.md` against `skills/$skill/help.md` (the moved file from P3).
4. If ANY diff output: **STOP. Do not proceed.** Record the mismatched files in `PHASE_LOG.md`. Inspect the sync script for the bug. Fix the discrepancy. Re-run verification from step 5a-1. **Do NOT delete copies until 100% match.**

#### 5b. Delete Copies from references/

**Only after 5a passes completely.**

For each of the 5 skills:
```bash
# Keep the references/ directory, remove all contents
for skill in skills/*/; do
  find "$skill/references" -mindepth 1 -delete
done
```

This deletes all files and subdirectories under `references/` but keeps the `references/` directory itself.

Verify deletion:
```bash
find skills/*/references -type f | wc -l
# Expected: 0
```

#### 5c. Create .gitkeep Placeholders

For each skill:
```bash
for skill in skills/*/; do
  touch "$skill/references/.gitkeep"
done
```

This ensures the `references/` directory is preserved in git even though all contents are gitignored.

#### 5d. Add .gitignore Rules

Append to `.gitignore`:
```
# Generated reference files — populated by scripts/sync_shared_refs.py
skills/*/references/
!skills/*/references/.gitkeep
```

Explanation:
- `skills/*/references/` — ignore all reference files (they are generated by sync)
- `!skills/*/references/.gitkeep` — except the .gitkeep placeholder (keeps dir in git)

#### 5e. Verify .gitignore Works

```bash
git status --short skills/*/references/
```
Expected output: Only `.gitkeep` files should appear as untracked/modified (or nothing, if already tracked).
Actual reference files should NOT appear.

#### 5f. Run Sync to Repopulate

```bash
python scripts/sync_shared_refs.py --verbose
```
Expected: All files copied to `references/`. No errors.

Then verify the repopulated files match shared:
```bash
for skill in skills/*/; do
  for f in shared/**/*.md; do
    rel="${f#shared/}"
    diff -q "$f" "$skill/references/$rel" || echo "MISMATCH: ${skill}references/$rel"
  done
done
```
Expected: zero diffs.

### Outputs
- Empty `skills/*/references/` directories with `.gitkeep` files
- Deleted 265 committed copies
- Updated `.gitignore` with ignore rules
- Verified sync re-population

### Validation
```bash
# 1. No committed copies remain
find skills/*/references -name '*.md' | wc -l
# Expected: 0

# 2. .gitkeep files exist
find skills/*/references -name '.gitkeep' | wc -l
# Expected: 5

# 3. .gitignore has the rules
grep -c "skills/\*/references/" .gitignore
# Expected: 1

# 4. After sync, all references are populated and byte-identical
python scripts/sync_shared_refs.py --verbose
# All COPY, no errors

for skill in skills/*/; do
  for f in shared/**/*.md; do
    rel="${f#shared/}"
    diff -q "$f" "$skill/references/$rel"
  done
done
# Expected: no output (all identical)

# 5. validate_skills.py still passes
python scripts/validate_skills.py
```

### Stop Condition
All copies deleted. `.gitignore` active. Sync re-populates identical content. `validate_skills.py` passes. `STATUS.md` shows P5 complete.

### Do Not Carry Forward
- Do not carry forward any doubt about sync correctness. P5 verification is the gate. If it passes, sync is trusted.
- Do not carry forward the committed copies. They are gone.

### Deep Phase Review (P5)

**Files reviewed:** Deleted content (verified by git diff), `.gitignore`, `.gitkeep` files.

**Review checklist:**
- [ ] ALL 265 committed copies confirmed deleted (check `git status --short`)
- [ ] All 5 `.gitkeep` files exist
- [ ] `.gitignore` rule correctly excludes `skills/*/references/` but allows `.gitkeep`
- [ ] Byte-for-byte verification passed BEFORE deletion
- [ ] Sync re-population produces identical content AFTER deletion
- [ ] `validate_skills.py` still reports `refs=True` for all skills (the directory exists with `.gitkeep`)
- [ ] No SKILL.md files were modified
- [ ] No shared/ files were modified
- [ ] `git status` shows only expected changes (deletions, new .gitkeep, modified .gitignore)

**Unusual checks:**
- Run `git status --short skills/*/references/`. Only `.gitkeep` files should appear. No `.md` files should appear.
- Confirm `python scripts/sync_shared_refs.py --verbose` repopulates all 265 files after deletion.
- Test fresh-clone resilience: delete one skill's `references/` entirely, run sync, verify it re-creates the dir and all files.

**Record review in `PHASE_LOG.md`.**

### Deep Education-Level Report (P5)
Write to `reports/phase-5-education.md` using the P2 education report template.

---

## Phase 6: Package Script

### Goal
Create `scripts/package_skill.sh` that produces a self-contained zip of a skill with populated references, suitable for standalone distribution.

### Inputs
- `scripts/sync_shared_refs.py` from P4
- `reference_manifest.yml` files from P2/P3
- All 5 skill directories with `SKILL.md` and populated `references/`
- `DECISIONS.md` — no specific decision for this phase, but D-002 (help.md) is relevant

### Likely Files
- `scripts/package_skill.sh` — CREATE

### Tasks

#### 6a. Script Structure

```bash
#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="${1:-}"
OUTPUT_DIR="${2:-dist}"

if [ -z "$SKILL_NAME" ]; then
    echo "Usage: $0 <skill-name> [output-dir]"
    echo "Example: $0 local-model-prompt-engineer"
    exit 1
fi

SKILL_DIR="skills/$SKILL_NAME"
if [ ! -d "$SKILL_DIR" ]; then
    echo "ERROR: skill directory not found: $SKILL_DIR"
    exit 1
fi

if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "ERROR: SKILL.md not found in $SKILL_DIR"
    exit 1
fi
```

#### 6b. Extract Version from Manifest

```bash
MANIFEST="$SKILL_DIR/reference_manifest.yml"
if [ -f "$MANIFEST" ]; then
    VERSION=$(python -c "
import yaml
with open('$MANIFEST') as f:
    print(yaml.safe_load(f).get('version', '0.0.0'))
")
else
    VERSION="0.0.0"
fi
```

#### 6c. Sync and Verify

```bash
echo "Syncing references for $SKILL_NAME..."
python scripts/sync_shared_refs.py --skill "$SKILL_NAME" --verbose
if [ $? -ne 0 ]; then
    echo "ERROR: sync failed, aborting package"
    exit 1
fi
```

#### 6d. Create Output Directory and Zip

```bash
mkdir -p "$OUTPUT_DIR"
ZIP_NAME="$OUTPUT_DIR/${SKILL_NAME}-${VERSION}.zip"

if [ -f "$ZIP_NAME" ]; then
    echo "WARN: overwriting existing $ZIP_NAME"
fi

# Check for zip command
if ! command -v zip &> /dev/null; then
    echo "ERROR: zip command not found. Install zip to use this script."
    exit 1
fi

# Zip the skill directory, excluding the manifest
zip -r "$ZIP_NAME" "$SKILL_DIR/" \
    -x "${SKILL_DIR}/reference_manifest.yml" \
    -x "${SKILL_DIR}/references/.gitkeep"

FILE_COUNT=$(unzip -l "$ZIP_NAME" | tail -1 | awk '{print $2}')
echo "Packaged $ZIP_NAME ($FILE_COUNT files)"
```

**Exclusions explained:**
- `reference_manifest.yml` — development artifact, not needed at runtime
- `references/.gitkeep` — empty placeholder, no value in distribution

#### 6e. Verify the Zip Contents

For each skill:
```bash
./scripts/package_skill.sh local-model-prompt-engineer
unzip -l dist/local-model-prompt-engineer-1.0.0.zip | head -20
# Verify: SKILL.md is present, references/ contains expected files, manifest is NOT present
```

Check specific files:
- SKILL.md is in the zip
- `references/git-safety.md` is in the zip
- `references/model-profiles/qwen36.md` is in the zip
- `references/help.md` is in the zip
- `reference_manifest.yml` is NOT in the zip
- `.gitkeep` is NOT in the zip

### Outputs
- `scripts/package_skill.sh` — created, tested

### Validation
```bash
# 1. Package script runs without error
./scripts/package_skill.sh local-model-prompt-engineer
# Expected: "Packaged dist/local-model-prompt-engineer-1.0.0.zip (N files)"

# 2. Zip contains SKILL.md
unzip -l dist/local-model-prompt-engineer-1.0.0.zip | grep "SKILL.md"

# 3. Zip does NOT contain manifest
unzip -l dist/local-model-prompt-engineer-1.0.0.zip | grep "reference_manifest.yml" && echo "FAIL" || echo "PASS"

# 4. Zip contains key reference files
unzip -l dist/local-model-prompt-engineer-1.0.0.zip | grep "git-safety.md"
unzip -l dist/local-model-prompt-engineer-1.0.0.zip | grep "help.md"
unzip -l dist/local-model-prompt-engineer-1.0.0.zip | grep "model-profiles/qwen36.md"

# 5. Test with missing skill (error case)
./scripts/package_skill.sh nonexistent-skill && echo "FAIL" || echo "PASS"
```

### Stop Condition
Package script works for all 5 skills. Zips contain expected content. Error cases handled. `STATUS.md` shows P6 complete.

### Do Not Carry Forward
- Do not carry forward generated zip files. They are not committed.

### Deep Phase Review (P6)

**Files reviewed:** `scripts/package_skill.sh`

**Review checklist:**
- [ ] `set -euo pipefail` at top (strict error handling)
- [ ] `zip` command existence check before use
- [ ] Exit code 1 on errors, 0 on success
- [ ] Manifest version extraction handles missing manifest gracefully
- [ ] Sync runs before zipping (ensures references are populated)
- [ ] Manifest excluded from zip (verify with `unzip -l`)
- [ ] `.gitkeep` excluded from zip
- [ ] Output directory created if needed
- [ ] Overwrite warning for existing zip
- [ ] Usage message when no arguments provided
- [ ] Shell script is executable (`chmod +x`)

**Unusual checks:**
- Test with each of the 5 skill names.
- Test with custom output directory: `./scripts/package_skill.sh local-model-prompt-engineer /tmp/test-dist`.

**Record review in `PHASE_LOG.md`.**

### Deep Education-Level Report (P6)
Write to `reports/phase-6-education.md` using the P2 education report template.

---

## Phase 7: Validation Enhancement and CI Workflow

### Goal
Enhance `scripts/validate_skills.py` to check manifests, and create `.github/workflows/validate.yml` for CI. The CI pipeline syncs references then validates.

### Inputs
- `scripts/validate_skills.py` — existing file to modify
- `scripts/sync_shared_refs.py` from P4
- `reference_manifest.yml` files from P2/P3
- `DECISIONS.md` — D-006 (validate checks structure, not version freshness)

### Likely Files
- `scripts/validate_skills.py` — MODIFY
- `.github/workflows/validate.yml` — CREATE
- `.github/` directory — CREATE

### Tasks

#### 7a. Enhance validate_skills.py

Add manifest validation checks AFTER the existing SKILL.md checks. The new checks run for each skill:

```python
def validate_manifest(skill_dir, skill_name):
    """Validate reference_manifest.yml. Returns (warnings, errors)."""
    manifest_path = skill_dir / 'reference_manifest.yml'
    if not manifest_path.exists():
        print(f"WARN {skill_name}: no reference_manifest.yml")
        return 1, 0

    try:
        manifest = yaml.safe_load(manifest_path.read_text())
    except yaml.YAMLError as e:
        print(f"ERROR {skill_name}: manifest YAML error: {e}")
        return 0, 1

    if not isinstance(manifest, dict):
        print(f"ERROR {skill_name}: manifest is not a dict")
        return 0, 1

    # Check skill field
    if manifest.get('skill') != skill_name:
        print(f"ERROR {skill_name}: manifest skill field '{manifest.get('skill')}' != dir name '{skill_name}'")
        return 0, 1

    # Check version field
    if not manifest.get('version'):
        print(f"WARN {skill_name}: manifest version missing")

    # Check references list
    refs = manifest.get('references', [])
    if not isinstance(refs, list):
        print(f"ERROR {skill_name}: manifest references is not a list")
        return 0, 1

    warn = 0
    err = 0
    sources_seen = set()

    for i, ref in enumerate(refs):
        if not isinstance(ref, dict):
            print(f"ERROR {skill_name}: reference entry {i} is not a dict")
            err += 1
            continue

        source = ref.get('source', '')
        if not source:
            print(f"ERROR {skill_name}: reference entry {i} missing source")
            err += 1
            continue

        # Check duplicate sources
        if source in sources_seen:
            print(f"ERROR {skill_name}: duplicate source '{source}'")
            err += 1
        sources_seen.add(source)

        # Check shared/ prefix for non-local entries
        is_local = ref.get('local', False)
        if not is_local and not source.startswith('shared/'):
            print(f"ERROR {skill_name}: source '{source}' not in shared/ and not local")
            err += 1

        # Check source file exists
        src_path = root / source
        if not src_path.exists():
            if ref.get('required', True):
                print(f"ERROR {skill_name}: required source not found: {source}")
                err += 1
            else:
                print(f"WARN {skill_name}: optional source not found: {source}")
                warn += 1

        # Check version field present
        if not ref.get('version'):
            print(f"WARN {skill_name}: reference '{source}' missing version")

    return warn, err
```

**Checks performed:**
1. Manifest file exists (warn if missing)
2. Valid YAML
3. `skill` field matches directory name
4. `version` field present (warn if missing)
5. `references` is a list
6. Each entry has `source` field
7. No duplicate `source` entries
8. Non-local `source` starts with `shared/`
9. Source file exists on disk (error if required, warn if optional)
10. `version` field present on each entry (warn if missing)

**What is NOT checked** (by design, per D-006):
- Version freshness against actual shared file content (requires git context, done by CI sync step)

#### 7b. Integrate Into Existing validate_skills.py

Modify the existing script to call `validate_manifest()` for each skill AFTER the existing SKILL.md validation. Preserve ALL existing checks.

Existing script structure (preserved):
1. Iterate skills, check SKILL.md exists
2. Parse frontmatter, validate name/description/metadata
3. Check line count
4. Check references/ directory existence

New additions (inserted after line count check):
5. Call `validate_manifest()` → adds warnings and errors separately from SKILL.md errors.

**Important:** The manifest function returns `(warnings, errors)`. Only errors set `errors += 1` on the global counter. Warnings print but do NOT cause exit code 1. This preserves the transition-period behavior where a missing manifest is a warning, not a failure.

After this phase, update `TASK.md` if scope changed (e.g., new validation dimensions were added).

#### 7c. Create GitHub Actions Workflow

Create `.github/workflows/validate.yml`:

```yaml
name: Validate

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install pyyaml

      - name: Sync shared references
        run: python scripts/sync_shared_refs.py --verbose

      - name: Validate skills and manifests
        run: python scripts/validate_skills.py
```

#### 7d. Test Validation

1. Run `python scripts/validate_skills.py` — should pass with all skills.
2. Temporarily break a manifest (remove a source file, add duplicate entry, change skill name) and verify validation catches it.
3. Verify all existing checks still work (SKILL.md validation, line counts, refs/ existence).
4. Run the full validation from a clean state:
   ```bash
   rm -rf skills/*/references/*
   python scripts/sync_shared_refs.py --verbose
   python scripts/validate_skills.py
   ```

### Outputs
- `scripts/validate_skills.py` — modified with manifest checks
- `.github/workflows/validate.yml` — created

### Validation
```bash
# 1. Normal validation passes
python scripts/validate_skills.py
# Expected: all skills OK, no errors, exit code 0

# 2. Validation catches broken manifests
# (manual test: temporarily corrupt a manifest and re-run)
python scripts/validate_skills.py
# Expected: ERROR for corrupted skill

# 3. Workflow file is valid YAML
python -c "import yaml; yaml.safe_load(open('.github/workflows/validate.yml'))"
# Expected: no error

# 4. Workflow references correct script paths
grep "sync_shared_refs.py" .github/workflows/validate.yml
grep "validate_skills.py" .github/workflows/validate.yml
# Expected: both found
```

### Stop Condition
Validation script enhanced and tested. CI workflow created and valid. `STATUS.md` shows P7 complete.

### Do Not Carry Forward
- Do not carry forward test corruptions of manifests. Restore all files to valid state.

### Deep Phase Review (P7)

**Files reviewed:** `scripts/validate_skills.py`, `.github/workflows/validate.yml`

**Review checklist:**
- [ ] All existing SKILL.md checks preserved (name, description, metadata.version, line count, refs/ existence)
- [ ] New manifest checks do not break on:
  - Missing manifest (warn, not error — transition period)
  - Invalid YAML (error)
  - Missing `source` (error)
  - Duplicate `source` (error)
  - Non-shared source without `local: true` (error)
  - Missing required source file (error)
  - Missing optional source file (warn)
- [ ] Manifest check runs for all 5 skills
- [ ] Exit code: 0 when all checks pass, 1 when errors exist
- [ ] Workflow file: valid YAML, `checkout@v4`, `setup-python@v5`, python 3.11
- [ ] Workflow runs sync before validation
- [ ] Workflow triggers on PR to main and push to main

**Record review in `PHASE_LOG.md`.**

### Deep Education-Level Report (P7)
Write to `reports/phase-7-education.md` using the P2 education report template.

---

## Phase 8: End-to-End Validation, Documentation, and Handoff

### Goal
Perform a full integration test. Create `CONTRIBUTING.md`. Produce final educational report and handoff artifacts.

### Inputs
- All artifacts from P1-P7
- Repository conventions from `AGENTS.md`
- Documentation standards from `shared/documentation-quality.md` and `docs/contributing/documentation-style.md`

### Likely Files
- `CONTRIBUTING.md` — CREATE
- `reports/phase-8-integration-test.md` — CREATE
- `reports/phase-8-education.md` — CREATE
- `NEXT_PROMPT.md` — CREATE
- `PHASE_LOG.md` — UPDATE (phase 8 entry)

### Tasks

#### 8a. Full Integration Test

Run the complete pipeline from a simulated fresh clone:

```bash
# Step 1: Simulate fresh clone by removing all generated references
find skills/*/references -mindepth 1 -not -name '.gitkeep' -delete

# Step 2: Verify references/ is empty (only .gitkeep)
find skills/*/references -type f
# Expected: 5 .gitkeep files only

# Step 3: Run sync to populate
python scripts/sync_shared_refs.py --verbose

# Step 4: Verify all files populated
find skills/*/references -name '*.md' | wc -l
# Expected: 265 (5 skills x 53 files)

# Step 5: Run validation
python scripts/validate_skills.py
# Expected: exit 0, all skills OK

# Step 6: Package each skill
for skill in local-model-prompt-engineer local-model-skill-engineer local-model-skill-migrator local-model-instruction-engineer local-model-agent-evaluator; do
  ./scripts/package_skill.sh "$skill"
done

# Step 7: Inspect one zip
unzip -l dist/local-model-prompt-engineer-1.0.0.zip | wc -l
# Expected: SKILL.md + 53 reference files = 54 files
# (plus 2 header/footer lines from unzip -l)

# Step 8: Byte-for-byte check: extract zip and compare references against shared/
mkdir -p /tmp/zip-test
unzip -o dist/local-model-prompt-engineer-1.0.0.zip -d /tmp/zip-test
for f in shared/**/*.md; do
  rel="${f#shared/}"
  diff -q "$f" "/tmp/zip-test/skills/local-model-prompt-engineer/references/$rel" || \
    echo "ZIP MISMATCH: $rel"
done
# Expected: no output (all match)
```

#### 8b. Check All Files Created by Sync Are Git-Ignored

```bash
git status --short skills/*/references/
```
Expected: Only `.gitkeep` files appear. No `.md` files.

#### 8c. Create CONTRIBUTING.md

Create a concise `CONTRIBUTING.md` documenting the new development workflow:

```markdown
# Contributing to ContextSmith

## Prerequisites
- Python 3.9+ with PyYAML (`pip install pyyaml`)
- `zip` command (for packaging skills)

## Development Workflow

### Editing shared reference files
1. Edit the file in `shared/`.
2. If the change is significant, update the version field in any affected `reference_manifest.yml` files.
3. Run `python scripts/sync_shared_refs.py --verbose` to verify references sync correctly.
4. Run `python scripts/validate_skills.py` to confirm all checks pass.

### Adding a new shared reference
1. Create the file in `shared/`.
2. Compute its blob hash.
3. Add it to each skill's `reference_manifest.yml` that needs it.
4. Run sync and validation.

### Packaging a skill for distribution
```bash
./scripts/package_skill.sh <skill-name>
```

### Validation
```bash
python scripts/validate_skills.py
```

### CI
All PRs to `main` run `sync_shared_refs.py` then `validate_skills.py`. Failures block merge.
```

#### 8d. Production Readiness Checklist

Walk through and confirm:

| Check | Expected |
|---|---|
| `python scripts/sync_shared_refs.py --dry-run` reports correct counts | 53 per skill |
| `python scripts/sync_shared_refs.py` runs without error | 0 exit code |
| `python scripts/validate_skills.py` passes all checks | 0 exit code, all skills OK |
| `./scripts/package_skill.sh <skill>` produces valid zip | zip exists, correct contents |
| `git status` shows no unexpected changes | Only .gitkeep, .gitignore, scripts, manifests |
| Shared files unchanged | `git diff shared/` is empty |
| SKILL.md files unchanged | `git diff -- skills/*/SKILL.md` is empty |
| Generated references are gitignored | `git status skills/*/references/*.md` shows nothing |
| Manifests are tracked | `git status skills/*/reference_manifest.yml` shows untracked (or staged) |

#### 8e. Write Final Handoff Artifacts

1. Update `PHASE_LOG.md` with P8 entry.
2. Write `NEXT_PROMPT.md` for session handoff.
3. Write `reports/phase-8-education.md` using the P2 education report template.

### Outputs
- `CONTRIBUTING.md` — created
- `reports/phase-8-integration-test.md` — created
- `reports/phase-8-education.md` — created
- `NEXT_PROMPT.md` — created
- `PHASE_LOG.md` — updated
- `STATUS.md` — updated to P8 complete

### Validation
```bash
# Full pipeline test (same as 8a)
find skills/*/references -mindepth 1 -not -name '.gitkeep' -delete
python scripts/sync_shared_refs.py --verbose && \
python scripts/validate_skills.py && \
./scripts/package_skill.sh local-model-prompt-engineer && \
echo "=== ALL CHECKS PASSED ==="
```
Expected: "ALL CHECKS PASSED" with exit code 0.

### Stop Condition
Integration test passes. All artifacts created. Handoff files written. Project complete.

### Do Not Carry Forward
- This is the final phase. All work is complete.

### Deep Phase Review (P8)

**Files reviewed:** All new and modified files across the entire project.

**Review checklist:**
- [ ] Integration test passes from simulated fresh clone
- [ ] `CONTRIBUTING.md` is concise, accurate, follows project voice
- [ ] All 5 manifests are valid YAML
- [ ] Sync script handles all edge cases (tested in P4, re-verified here)
- [ ] Package script produces valid zips for all 5 skills
- [ ] Validation script catches all defined error conditions
- [ ] CI workflow file references correct paths
- [ ] `git status` shows only expected changes
- [ ] No shared file was modified
- [ ] No SKILL.md was modified
- [ ] All generated references are gitignored

**Record review in `PHASE_LOG.md`.**

### Deep Education-Level Report (P8)
Write to `reports/phase-8-education.md` using the P2 education report template. This is the **project-level summary** covering architecture, decisions, lessons learned, and maintenance guidance.

---

## Appendix: Edge Case Catalog

### E1: Missing Manifest
**Behavior:** Sync skips the skill with a warning. Validation warns but does not error. This allows gradual adoption — a skill can be added to manifests later.

### E2: Invalid YAML in Manifest
**Behavior:** Sync reports error and skips the skill. Validation reports error. CI fails.

### E3: Source File Does Not Exist (Required)
**Behavior:** Sync reports error for that entry, continues with remaining entries. Validation reports error. CI fails.

### E4: Source File Does Not Exist (Optional)
**Behavior:** Sync skips that entry with a warning. Sync continues. Validation warns. CI passes (warnings are non-fatal).

### E5: Non-shared/ Source Without local:true
**Behavior:** Sync reports error. Validation reports error. CI fails.

### E6: Duplicate Source in Manifest
**Behavior:** Validation reports error, but sync copies the first occurrence and ignores duplicates (may cause subtle bugs). Treat as error.

### E7: Shared File Renamed
**Behavior:** Manifest `source` points to old path. Sync reports error (file not found). Developer must update manifest.

### E8: New Shared File Added
**Behavior:** No manifest references it yet. Sync does nothing. Validation does nothing. Developer must add it to manifests. This is normal — not every shared file is needed by every skill.

### E9: Skill Root Does Not Exist
**Behavior:** Sync script iterates `skills_dir.iterdir()` — nonexistent skill is simply not found. Package script checks and errors.

### E10: zip Command Not Installed
**Behavior:** Package script exits with error message. CI does not run package script, so this only affects local development.

### E11: Script Invoked from Wrong Directory
**Behavior:** `REPO_ROOT = Path(__file__).resolve().parents[1]` ensures all paths resolve relative to the script location, not CWD. This is handled.

### E12: Destination Is a Directory
**Behavior:** If `references/model-profiles/` is a directory but the source is also a directory, this is a problem. Sync script does not handle directory destinations — only files. The existing structure has no directory-to-directory copies, so this is not a current concern.

---

## Appendix: Full File Manifest

This is the complete list of reference entries every skill's manifest must contain (minus the small `help.md` variation):

```
shared/coding-standards.md
shared/context-management.md
shared/control-parameters.md
shared/control-phrases.md
shared/documentation-quality.md
shared/domain-intent.md
shared/domain-profiles/ai-modalities.md
shared/domain-profiles/coding.md
shared/domain-profiles/data-science-ml.md
shared/domain-profiles/documents.md
shared/domain-profiles/email.md
shared/domain-profiles/purchasing-tickets.md
shared/domain-profiles/research.md
shared/domain-profiles/scheduling.md
shared/education-levels.md
shared/educational-report.md
shared/engineering-metadata.md
shared/evaluation-rubrics.md
shared/git-hygiene.md
shared/git-safety.md
shared/help-mode.md
shared/implementation-plan-audit.md
shared/instruction-conflicts.md
shared/instruction-deduplication.md
shared/instruction-precedence.md
shared/interaction-modes.md
shared/loop-safety.md
shared/model-capability-tiers.md
shared/model-profiles/gemma4.md
shared/model-profiles/generic-local.md
shared/model-profiles/llama3.md
shared/model-profiles/qwen36.md
shared/output-location.md
shared/persistent-task-state.md
shared/phase-code-review.md
shared/phase-compression.md
shared/phased-planning.md
shared/planner-executor-workflows.md
shared/ralph-loop.md
shared/reference-optimization.md
shared/run-configuration-preview.md
shared/runtime-stability.md
shared/side-effect-matrix.md
shared/skill-interoperability.md
shared/small-context-workflows.md
shared/small-model-atomicity.md
shared/subagent-delegation.md
shared/targeted-context-length.md
shared/test-quality-audit.md
shared/ui-standards.md
shared/upstream-artifact-audit.md
shared/usage-patterns.md
```

Plus one local entry per skill:
```
skills/<skill>/help.md  (local: true)
```

---

## Appendix: Implementation Notes for Qwen 3.6 27B

### Constraints for the executing agent
- **Context window**: ~128K tokens recommended. Load one manifest or one script at a time.
- **No chain-of-thought**: Write code directly. Verify with tests after.
- **File operations**: Use Read tool for existing files, Write tool for new files, Edit tool for modifications.
- **YAML**: Use the `yaml` module (PyYAML). Always parse after writing to verify validity.
- **Path handling**: Use `pathlib.Path`, never string concatenation.
- **Testing**: Run the validation command after each phase. Do not write separate test files unless the plan explicitly requires it.

### Phase execution order
- P1 → P2 → P3 → P4 → P5 → P6 → P7 → P8.
- P5 is the critical gate — do NOT delete copies unless byte-for-byte verification passes.
- P2 and P3 can merge into one continuous session if token budget allows.

### After each phase
1. Run validation commands.
2. Write review findings to `PHASE_LOG.md`.
3. Write education report to `reports/phase-N-education.md`.
4. Update `STATUS.md` with next phase.
5. Write `NEXT_PROMPT.md` for session handoff.