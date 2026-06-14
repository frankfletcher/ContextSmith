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


_PHASE_HEADING = re.compile(r"^###\s+(.+)")
_SUBPHASE_HEADING = re.compile(r"^####\s+(.+)")
_TASK_DONE = re.compile(r"^- \[x\]\s+(.+)")
_TASK_PENDING = re.compile(r"^- \[ \]\s+(.+)")
_KV_LINE = re.compile(r"^- ([^:]+):\s*(.*)")


def _make_phase(match) -> dict:
    """Create a new phase dict from a heading match."""
    return {
        "name": match.group(1).strip(),
        "status": "pending",
        "metadata": {},
        "subphases": [],
    }


def _make_subphase(match) -> dict:
    """Create a new sub-phase dict from a heading match."""
    return {
        "name": match.group(1).strip(),
        "status": "pending",
        "metadata": {},
        "tasks": [],
        "task_completion": 0.0,
    }


def _parse_phase_tree(content: str) -> list[dict]:
    """Parse hierarchical phase structure from Phases section content.

    Supports three levels:
      ### Phase N: Name      (phase)
      #### Sub-phase N.M: ...  (sub-phase)
      - [x] Task             (checkbox task within sub-phase)

    Falls back to flat checkbox parsing (### headings not found).

    Returns:
        List of phase dicts. Each phase has:
          name, status, metadata (dict), subphases (list)
        Each sub-phase has:
          name, status, metadata (dict), tasks, task_completion (float)
        Each task has: text (str), done (bool)
    """
    lines = content.splitlines()

    has_hierarchical = any(_PHASE_HEADING.match(line.strip()) for line in lines)
    if not has_hierarchical:
        return _parse_flat_phases(lines)

    phases = []
    current_phase = None
    current_subphase = None

    for line in lines:
        stripped = line.strip()
        _dispatch_line(stripped, phases, current_phase, current_subphase)
        current_phase = _update_current(phases, current_phase)
        current_subphase = _update_current_subphase(current_phase)

    return phases


def _dispatch_line(
    stripped: str,
    phases: list,
    current_phase: dict | None,
    current_subphase: dict | None,
) -> None:
    """Dispatch a single line to the appropriate handler.

    Mutates phases/current_phase/current_subphase in place.
    """
    m = _PHASE_HEADING.match(stripped)
    if m:
        phases.append(_make_phase(m))
        return

    if current_phase is None:
        return

    m = _SUBPHASE_HEADING.match(stripped)
    if m:
        current_phase["subphases"].append(_make_subphase(m))
        return

    if current_subphase is None:
        _handle_phase_metadata(stripped, current_phase)
        return

    _handle_subphase_content(stripped, current_subphase)


def _handle_phase_metadata(stripped: str, phase: dict) -> None:
    """Parse metadata for a phase from a key:value line."""
    m = _KV_LINE.match(stripped)
    if not m:
        return
    key, val = m.group(1).strip(), m.group(2).strip()
    phase["metadata"][key] = val
    if key == "Status":
        phase["status"] = val


def _handle_subphase_content(stripped: str, subphase: dict) -> None:
    """Parse task or metadata for a sub-phase from a line."""
    m = _TASK_DONE.match(stripped)
    if m:
        subphase["tasks"].append({"text": m.group(1).strip(), "done": True})
        subphase["task_completion"] = _calc_completion(subphase["tasks"])
        return

    m = _TASK_PENDING.match(stripped)
    if m:
        subphase["tasks"].append({"text": m.group(1).strip(), "done": False})
        subphase["task_completion"] = _calc_completion(subphase["tasks"])
        return

    m = _KV_LINE.match(stripped)
    if m:
        key, val = m.group(1).strip(), m.group(2).strip()
        subphase["metadata"][key] = val
        if key == "Status":
            subphase["status"] = val


def _update_current(phases: list, current: dict | None) -> dict | None:
    """Return the last phase in the list, or None."""
    return phases[-1] if phases else None


def _update_current_subphase(current_phase: dict | None) -> dict | None:
    """Return the last sub-phase in the current phase, or None."""
    if not current_phase:
        return None
    subphases = current_phase.get("subphases", [])
    return subphases[-1] if subphases else None


def _calc_completion(tasks: list[dict]) -> float:
    """Calculate task completion ratio (0.0 to 1.0)."""
    if not tasks:
        return 0.0
    return sum(1 for t in tasks if t["done"]) / len(tasks)


_FLAT_PHASE = re.compile(r"^- \[([ x])\]\s+(.+)")


def _parse_flat_phases(lines: list[str]) -> list[dict]:
    """Parse flat checkbox list into phase dicts (backward compat)."""
    phases = []
    for line in lines:
        stripped = line.strip()
        m = _FLAT_PHASE.match(stripped)
        if m:
            done = m.group(1) == "x"
            phases.append(
                {
                    "name": m.group(2).strip(),
                    "status": "completed" if done else "pending",
                    "metadata": {},
                    "subphases": [],
                }
            )
    return phases


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
        "current_subphase": s.get("Current Sub-phase", ""),
        "progress": _kv(s.get("Progress", "")),
        "completed": _list(s.get("Completed", "")),
        "next_action": s.get("Next Action", ""),
        "blocked_by": s.get("Blocked By", "none"),
    }


def read_plan(dir: Path) -> dict:
    """Parse PLAN.md into structured dict.

    Supports both hierarchical (### Phase → #### Sub-phase → [x] Task)
    and flat (- [x] Phase) formats. Auto-detects by checking for ### headings.

    Returns:
        Dict with:
          phases: list of phase dicts (from _parse_phase_tree)
          dependencies: dict from ## Dependencies section
          validation_gates: dict from ## Validation Gates section
    """
    path = Path(dir) / "PLAN.md"
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path.name}")
    s = _sections(path.read_text(encoding="utf-8"))
    return {
        "phases": _parse_phase_tree(s.get("Phases", "")),
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
