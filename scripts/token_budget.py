#!/usr/bin/env python3
"""Report approximate token budgets for ContextSmith skills and references."""

from argparse import ArgumentParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILL_BUDGETS = {
    "contextsmith": 1000,
    "contextsmith-agent-evaluator": 1900,
    "contextsmith-skill-migrator": 2500,
    "contextsmith-skill-engineer": 3200,
    "contextsmith-instruction-engineer": 3400,
    "contextsmith-prompt-engineer": 3600,
    "contextsmith-run": 4000,
}

COMMON_LOAD_SETS = {
    "contextsmith-run:minimal": [
        "skills/contextsmith-run/SKILL.md",
        "skills/contextsmith-run/execution-contract-core.md",
        "skills/contextsmith-run/evidence-ledger-core.md",
        "shared/control-parameters-core.md",
    ],
    "contextsmith-run:ralph-validation": [
        "skills/contextsmith-run/SKILL.md",
        "skills/contextsmith-run/execution-contract-core.md",
        "skills/contextsmith-run/evidence-ledger-core.md",
        "shared/control-parameters-core.md",
        "shared/ralph-loop.md",
        "shared/evaluation-rubrics.md",
    ],
    "contextsmith-run:task-state": [
        "skills/contextsmith-run/SKILL.md",
        "skills/contextsmith-run/execution-contract-core.md",
        "skills/contextsmith-run/evidence-ledger-core.md",
        "shared/control-parameters-core.md",
        "skills/contextsmith-run/task-state-execution.md",
        "shared/persistent-task-state.md",
    ],
    "prompt-engineer:manifest-core": [
        "skills/contextsmith-prompt-engineer/SKILL.md",
        "shared/control-parameters-core.md",
        "shared/artifact-manifest-core.md",
        "shared/behavioral-contracts.md",
    ],
    "instruction-engineer:manifest-core": [
        "skills/contextsmith-instruction-engineer/SKILL.md",
        "shared/control-parameters-core.md",
        "shared/artifact-manifest-core.md",
        "shared/behavioral-contracts.md",
    ],
    "skill-engineer:manifest-core": [
        "skills/contextsmith-skill-engineer/SKILL.md",
        "shared/control-parameters-core.md",
        "shared/artifact-manifest-core.md",
        "shared/behavioral-contracts.md",
    ],
}


def estimate_tokens(text):
    """Estimate tokens conservatively without external dependencies."""
    by_chars = len(text) / 4
    by_words = len(text.split()) * 1.33
    return int(max(by_chars, by_words) + 0.5)


def read_text(path):
    return path.read_text(encoding="utf-8")


def report_skill_budgets(strict):
    print("Skill always-loaded budgets")
    print("| Skill | Lines | Est. tokens | Budget | Status |")
    print("|---|---:|---:|---:|---|")
    failures = 0

    for skill_dir in sorted((ROOT / "skills").iterdir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        text = read_text(skill_file)
        tokens = estimate_tokens(text)
        lines = len(text.splitlines())
        budget = DEFAULT_SKILL_BUDGETS.get(skill_dir.name, 3000)
        status = "OK" if tokens <= budget else "WARN"
        if strict and tokens > budget:
            failures += 1
        print(f"| {skill_dir.name} | {lines} | {tokens} | {budget} | {status} |")

    return failures


def report_reference_budgets():
    print("\nLargest shared references")
    print("| Reference | Lines | Est. tokens |")
    print("|---|---:|---:|")

    refs = []
    for path in (ROOT / "shared").rglob("*.md"):
        text = read_text(path)
        refs.append((estimate_tokens(text), len(text.splitlines()), path.relative_to(ROOT)))

    for tokens, lines, rel_path in sorted(refs, reverse=True)[:15]:
        print(f"| {rel_path} | {lines} | {tokens} |")


def report_common_load_sets():
    print("\nCommon load-set estimates")
    print("| Load set | Files | Est. tokens |")
    print("|---|---:|---:|")

    for name, rel_paths in COMMON_LOAD_SETS.items():
        total = 0
        missing = []
        for rel_path in rel_paths:
            path = ROOT / rel_path
            if not path.exists():
                missing.append(rel_path)
                continue
            total += estimate_tokens(read_text(path))
        suffix = "" if not missing else f" MISSING: {', '.join(missing)}"
        print(f"| {name}{suffix} | {len(rel_paths)} | {total} |")


def main():
    parser = ArgumentParser(description="Estimate ContextSmith token budgets.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when a SKILL.md exceeds its budget.")
    args = parser.parse_args()

    failures = report_skill_budgets(args.strict)
    report_common_load_sets()
    report_reference_budgets()
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
