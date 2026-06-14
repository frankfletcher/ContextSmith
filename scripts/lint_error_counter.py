"""Accumulate lint error frequencies across runs.

    Pipes stdin through to stdout while extracting error codes (MD... or A...)
    and incrementing persistent counters in .agent_work/lint_error_counts.json.

Usage:
    markdownlint . --ignore node_modules 2>&1 | uv run python scripts/lint_error_counter.py
    ruff check orchestrator/ --select E,F,W,I 2>&1 | uv run python scripts/lint_error_counter.py

Combined:
    (markdownlint . --ignore node_modules; ruff check orchestrator/) 2>&1 |
        uv run python scripts/lint_error_counter.py

View accumulated counts:
    cat .agent_work/lint_error_counts.json
"""

import json
import re
import sys
from pathlib import Path

COUNTER_PATH = Path(".agent_work/lint_error_counts.json")


def _load_counts() -> dict[str, int]:
    if COUNTER_PATH.exists():
        try:
            data = json.loads(COUNTER_PATH.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_counts(counts: dict[str, int]) -> None:
    COUNTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    COUNTER_PATH.write_text(
        json.dumps(counts, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _extract_error_codes(line: str) -> list[str]:
    codes: list[str] = []
    # markdownlint: "file.md:12 error MD022/blanks-around-headings"
    for m in re.finditer(r"\bMD\d+\b", line):
        codes.append(m.group(0))
    # ruff: "file.py:1:1: E501 Line too long"
    for m in re.finditer(r"\b([A-Z]\d+)\b", line):
        code = m.group(1)
        if code[0].isalpha() and code[1:].isdigit():
            codes.append(code)
    return codes


def main() -> None:
    counts = _load_counts()

    for line in sys.stdin:
        sys.stdout.write(line)
        for code in _extract_error_codes(line):
            counts[code] = counts.get(code, 0) + 1

    _save_counts(counts)

    total = sum(counts.values())
    if total:
        top = sorted(counts.items(), key=lambda x: -x[1])[:5]
        summary = ", ".join(f"{k}={v}" for k, v in top)
        print(f"[lint-error-counter] {total} total errors | top: {summary}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
