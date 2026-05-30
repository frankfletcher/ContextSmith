# Top 5 Ideas to Implement Next

**Generated:** 2026-05-29  
**Source:** Review of `LOCAL_MODEL_AGENT_ENGINEERING_LIVING_NOTES.md` unimplemented backlog

---

## 1. `scripts/sync_shared_refs.py` + `scripts/build_release.py` (Repo & Release Tooling) **[DONE]**

You have 42 files in `shared/` that get copied into each skill's `references/` for standalone installation. This is Option C — canonical shared refs plus per-skill copies. Right now, keeping them in sync is a manual process. Every time you edit a shared reference, you have to decide whether each of the 5 skills needs an updated copy. That's 42 × 5 = 210 potential copy operations, and drift is inevitable.

The sync script automates propagation. The release builder packages everything for distribution. These are **force multipliers** — they make every future edit safer and faster. Without them, the package grows harder to maintain as it matures.

**Backlog items:**
- [x] `scripts/sync_shared_refs.py` — sync shared references to per-skill copies with SHA-1 hash comparison and `--update-manifests` flag.
- [x] `scripts/build_release.py` — full release pipeline: sync, validate, version bump, package, bundle, summary.
- [x] `scripts/package_skill.sh` — individual skill packaging with MANIFEST.json and SHA-256 checksums.
- [x] `scripts/install_skill.sh` — install single skill with checksum verification and backup.
- [x] `scripts/install_all.sh` — batch install all skills from dist/.
- [x] `scripts/test_release.sh` — 74-assertion end-to-end integration test.
- [x] `scripts/publish_release.sh` — create and publish GitHub releases with gh CLI.
- [x] `docs/RELEASE_PROCESS.md` — maintainer guide with prerequisites, step-by-step checklist, and troubleshooting.

---

## 2. Harness Profiles (`references/harness-profiles/`)

The whole thesis of ContextSmith is that local models need explicit, harness-aware instructions. But right now there are zero harness-specific profiles. You mention OpenCode, Codex, Cursor, Aider, Continue, Hermes, and OpenClaw in the backlog — these are real tools users are running with. Adding harness profiles means skills can adapt their output format, tool-call conventions, and instruction structure to match what each harness actually understands. This directly improves the **core value proposition**: reliable agent instructions across different tools.

Start with `generic-agent.md`, `cursor.md`, and `aider.md` — those have the largest user bases.

**Backlog items:**
- [ ] Add `references/harness-profiles/`
- [ ] Add `generic-agent.md`
- [ ] Add `opencode.md`
- [ ] Add `codex.md`
- [ ] Add `aider.md`
- [ ] Add `openclaw.md`
- [ ] Add `hermes.md`
- [ ] Add `cursor.md`
- [ ] Add `continue.md`
- [ ] Add `cli-only.md`

---

## 3. `local-model-profile-builder` Skill

You currently ship 4 model profiles (`generic-local`, `qwen36`, `gemma4`, `llama3`). The model landscape moves fast — new models ship weekly, and users are testing models you don't have profiles for yet. A profile-builder skill lets users create and refine profiles from their own runtime observations, model cards, and failure-mode notes. This turns the package from a static set of profiles into a **living, user-extensible system**. It also creates a feedback loop: users who build profiles surface real-world data about what works.

**Backlog items:**
- [ ] `local-model-profile-builder` — create/update model profiles based on user tests, model cards, runtime behavior, and known failure modes.

---

## 4. Automated Analysis Scripts (Duplicate Rules, Reference Checker, Exposed-CoT Scanner)

With 42 shared references and 5 skills each with their own reference copies, **rule duplication and contradiction drift** is a real risk. An automated duplicate-rule detector catches when the same concept is defined in multiple places with slightly different wording. A reference checker validates that all SKILL.md references actually point to existing files. An exposed-CoT scanner flags phrases that leak reasoning. These are **quality gates** — they turn manual review into automated validation, which pairs naturally with the GitHub Actions workflow you have in the backlog.

**Backlog items:**
- [ ] `scripts/check_no_duplicate_rules.py`
- [ ] `scripts/check_references.py`
- [ ] Automated exposed-CoT phrase scanner
- [ ] GitHub Actions validation workflow

---

## 5. `agent-task-state-manager` Skill

Persistent task state is a core feature of your workflows — `.agent_work/` folders with TASK.md, PLAN.md, STATUS.md, etc. But there's no tool to initialize, clean, audit, or resume these folders systematically. A dedicated skill for task-state management would handle folder initialization, cleanup of stale state, size-limit enforcement (which you already have in the backlog), and phase summary compaction. This is useful because **long-running projects accumulate state bloat**, and users need a way to prune and reorganize without losing durable decisions.

**Backlog items:**
- [ ] `agent-task-state-manager` — initialize, clean, audit, or resume persistent task-state folders.
- [ ] Task-state cleanup skill
- [ ] State file size-limit enforcement
- [ ] Phase summary compaction command

---

## Honorable Mentions

- **Domain profiles** (travel, finance-sensitive, legal-sensitive, medical-sensitive, PKM, workflow automation) — valuable but narrower audience.
- **Real `contextsmith` CLI** — ambitious; better to wait until CLI semantics stabilize per your own notes.
- **GitHub Actions workflow** — important for CI/CD, but lower priority than the sync script it would run.
- **Screenshots / terminal-output examples** — great for onboarding, but documentation polish vs functional gap.
