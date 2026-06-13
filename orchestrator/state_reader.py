"""Parse task-state artifacts into structured dicts."""

import re
from pathlib import Path


def _sections(content: str) -> dict[str, str]:
    """Split markdown into sections by ## headings."""
    sections, current, lines = {}, None, []
    for line in content.splitlines():
        if line.startswith("## "):
            if current:
                sections[current] = "\n".join(lines).strip()
            current, lines = line[3:].strip(), []
        elif current:
            lines.append(line)
    if current:
        sections[current] = "\n".join(lines).strip()
    return sections


def _list(content: str) -> list[str]:
    """Parse markdown list items into strings."""
    items = []
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
    return items


def _kv(content: str) -> dict[str, str]:
    """Parse key: value pairs from markdown."""
    result = {}
    for line in content.splitlines():
        line = line.strip().lstrip("- ")
        if ":" in line:
            k, _, v = line.partition(":")
            result[k.strip()] = v.strip()
    return result


def read_status(dir: Path) -> dict:
    """Parse STATUS.md into structured dict."""
    path = Path(dir) / "STATUS.md"
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path.name}")
    s = _sections(path.read_text(encoding="utf-8"))
    for req in ["Current Phase", "Current State", "Next Action"]:
        if req not in s:
            raise ValueError(f"Missing required section '## {req}'")
    return {
        "current_phase": s.get("Current Phase", ""),
        "current_state": s.get("Current State", ""),
        "progress": _kv(s.get("Progress", "")),
        "completed": _list(s.get("Completed", "")),
        "next_action": s.get("Next Action", ""),
        "blocked_by": s.get("Blocked By", "none"),
    }


def read_plan(dir: Path) -> dict:
    """Parse PLAN.md into structured dict."""
    path = Path(dir) / "PLAN.md"
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path.name}")
    s = _sections(path.read_text(encoding="utf-8"))
    phases = []
    for line in s.get("Phases", "").splitlines():
        line = line.strip()
        if line.startswith("- ["):
            status = "done" if line.startswith("- [x]") else "pending"
            name = re.sub(r"^- \[[ x]\] ", "", line)
            phases.append({"name": name, "status": status})
    return {
        "phases": phases,
        "dependencies": _kv(s.get("Dependencies", "")),
        "validation_gates": _kv(s.get("Validation Gates", "")),
    }


def read_context(dir: Path) -> dict:
    """Parse CONTEXT.md into structured dict."""
    path = Path(dir) / "CONTEXT.md"
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path.name}")
    s = _sections(path.read_text(encoding="utf-8"))
    return {
        "project": s.get("Project", ""),
        "task_directory": s.get("Task Directory", ""),
        "key_files": _kv(s.get("Key Files", "")),
        "constraints": _list(s.get("Known Constraints", "")),
        "assumptions": _list(s.get("Assumptions", "")),
        "harness": s.get("Harness", ""),
    }
