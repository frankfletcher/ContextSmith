"""Next Prompt Compiler - generates detailed phase prompts from task state.

Reads task-state files and produces NEXT_PROMPT.md with all required sections.
Does not run models, execute phases, or advance task state.
"""

import re
import sys
from pathlib import Path


def _read_file(task_dir: Path, filename: str) -> str | None:
    """Read a file from the task directory. Return None if not found."""
    path = task_dir / filename
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return None


def _extract_current_phase(status_text: str) -> str | None:
    """Extract the current phase from STATUS.md.

    Tries three formats in order:
    1. `current_phase:` inline field (YAML-style)
    2. `next_required_action:` inline field
    3. `## Current Phase` Markdown section (value is the next non-empty line)
    """
    # Try current_phase field first
    m = re.search(r"^\s*-?\s*current_phase\s*:\s*(.+)$", status_text, re.MULTILINE)
    if m:
        raw = m.group(1).strip()
        raw = raw.strip("`")
        phase_m = re.search(r"(Phase\s+[\w.]+)", raw, re.IGNORECASE)
        if phase_m:
            return phase_m.group(1)
        return raw

    # Try next_required_action field
    m = re.search(r"^\s*-?\s*next_required_action\s*:\s*(.+)$", status_text, re.MULTILINE)
    if m:
        raw = m.group(1).strip()
        phase_m = re.search(r"(Phase\s+[\w.]+)", raw, re.IGNORECASE)
        if phase_m:
            return phase_m.group(1)
        return raw

    # Fallback: parse ## Current Phase Markdown section
    lines = status_text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("## Current Phase"):
            # Value is the next non-empty, non-heading line
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                if next_line and not next_line.startswith("#"):
                    # Prefixed phase identifier: "Phase 1C", "Phase 2", etc.
                    # Must start at beginning of line with capital P
                    phase_m = re.match(r"(Phase\s+[\w.]+)", next_line)
                    if phase_m:
                        return phase_m.group(1)
                    # Short slug like "phase_1", "4b", "load_task_state"
                    if re.match(r"^[\w.]+$", next_line) and len(next_line) < 60:
                        return next_line
                    # Longer sentence = not a phase identifier
                    return None
                if next_line.startswith("## "):
                    break
            break

    return None


def _find_phase_block(plan_text: str, phase_id: str) -> tuple[str, str] | None:
    """Find the phase block in PLAN.md for the given phase id.

    Returns (heading, block_text) or None if not found.
    Also returns the next phase id if determinable.
    """
    # Normalize phase id for matching: "Phase 5B" -> match "## Phase 5B:"
    pattern = re.escape(phase_id)
    # Match heading like "## Phase 5B: Next Prompt Compiler Implementation"
    heading_re = re.compile(
        r"^(##\s+" + pattern + r":\s*.+)$", re.MULTILINE
    )

    match = heading_re.search(plan_text)
    if not match:
        return None

    heading = match.group(1)
    block_start = match.end()

    # Find next ## heading at same or higher level
    next_heading = re.search(r"^##\s+", plan_text[block_start:], re.MULTILINE)
    if next_heading:
        block_text = plan_text[block_start:block_start + next_heading.start()]
    else:
        block_text = plan_text[block_start:]

    return (heading.strip(), block_text.strip())


def _find_next_phase(plan_text: str, current_phase_id: str) -> str | None:
    """Determine the next phase id from PLAN.md ordering."""
    # Extract all phase headings in order
    phases = re.findall(r"^##\s+(Phase\s+[\w]+):", plan_text, re.MULTILINE)
    try:
        idx = phases.index(current_phase_id)
        if idx + 1 < len(phases):
            return phases[idx + 1]
    except ValueError:
        pass
    return None


def _extract_context_contract(block_text: str) -> dict:
    """Extract the context_contract YAML block from a phase block."""
    # Find YAML block between ```yaml and ```
    yaml_match = re.search(r"```yaml\s*\n(.*?)\n```", block_text, re.DOTALL)
    if not yaml_match:
        return {}
    yaml_text = yaml_match.group(1).strip()
    result = {}
    for line in yaml_text.split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def _extract_actions(block_text: str) -> list[str]:
    """Extract numbered actions from the phase block."""
    actions = []
    # Look for ## Actions section
    actions_section = re.search(r"##\s*Actions\s*\n(.*?)(?=##\s|\Z)", block_text, re.DOTALL)
    if not actions_section:
        return actions
    text = actions_section.group(1)
    # Extract numbered list items
    for m in re.finditer(r"^\s*(?:\d+[.)]\s+|-)\s+(.+)$", text, re.MULTILINE):
        actions.append(m.group(1).strip())
    return actions


def _extract_inputs(block_text: str) -> list[str]:
    """Extract inputs from the phase block."""
    inputs = []
    inputs_section = re.search(r"##\s*Inputs\s*\n(.*?)(?=##\s|\Z)", block_text, re.DOTALL)
    if not inputs_section:
        return inputs
    text = inputs_section.group(1)
    for m in re.finditer(r"^\s*[-*]\s+(.+)$", text, re.MULTILINE):
        inputs.append(m.group(1).strip())
    return inputs


def _extract_validation(block_text: str) -> list[str]:
    """Extract validation items from the phase block."""
    items = []
    val_section = re.search(r"##\s*Validation\s*\n(.*?)(?=##\s|\Z)", block_text, re.DOTALL)
    if not val_section:
        return items
    text = val_section.group(1)
    for m in re.finditer(r"^\s*[-*]\s+(.+)$", text, re.MULTILINE):
        items.append(m.group(1).strip())
    return items


def _extract_stop_rule(context_contract: dict) -> str:
    """Extract stop_rule from context contract."""
    return context_contract.get("stop_rule", "")


def _extract_education(block_text: str) -> str | None:
    """Extract education section from the phase block."""
    edu_section = re.search(r"##\s*Education\s*\n(.*?)(?=##\s|\Z)", block_text, re.DOTALL)
    if edu_section:
        return edu_section.group(1).strip()
    return None


def _extract_validation_commands(context_text: str) -> list[str]:
    """Extract validation commands from CONTEXT.md."""
    commands = []
    val_section = re.search(r"##\s*Validation Commands\s*\n(.*?)(?=##\s|\Z)", context_text, re.DOTALL)
    if not val_section:
        return commands
    text = val_section.group(1)
    for m in re.finditer(r"^\s*[-*]\s+(.+)$", text, re.MULTILINE):
        commands.append(m.group(1).strip())
    return commands


def _extract_constraints(context_text: str) -> list[str]:
    """Extract constraints from CONTEXT.md."""
    constraints = []
    con_section = re.search(r"##\s*Constraints\s*\n(.*?)(?=##\s|\Z)", context_text, re.DOTALL)
    if not con_section:
        return constraints
    text = con_section.group(1)
    for m in re.finditer(r"^\s*[-*]\s+(.+)$", text, re.MULTILINE):
        constraints.append(m.group(1).strip())
    return constraints


def _extract_phase_goal(heading: str, block_text: str) -> str:
    """Extract the phase goal from heading and block text."""
    # Try ## Goal section first
    goal_m = re.search(r"##\s*Goal\s*\n(.*?)(?=##\s|\Z)", block_text, re.DOTALL)
    if goal_m:
        return goal_m.group(1).strip()
    # Try ## Purpose section
    purpose_m = re.search(r"##\s*Purpose\s*\n(.*?)(?=##\s|\Z)", block_text, re.DOTALL)
    if purpose_m:
        return purpose_m.group(1).strip()
    # Fall back to heading text (strip "## Phase X:" prefix)
    clean = re.sub(r"^##\s*Phase\s+[\w]+:\s*", "", heading).strip()
    return clean


def compile_next_prompt(
    task_dir: str | Path,
    phase_override: str | None = None,
    include_education: bool = False,
    compact: bool = False,
) -> str:
    """Compile a NEXT_PROMPT.md from task-state files.

    Args:
        task_dir: Directory containing STATUS.md, PLAN.md, CONTEXT.md, etc.
        phase_override: Optional phase id to override STATUS.md detection.
        include_education: Include deep education notes section.
        compact: Omit education notes and collapse phase contract.

    Returns:
        Generated NEXT_PROMPT.md content.

    Raises:
        FileNotFoundError: If required state files are missing.
        ValueError: If phase cannot be determined or phase block is missing.
    """
    task_dir = Path(task_dir)

    # --- Read required files ---
    status_text = _read_file(task_dir, "STATUS.md")
    if status_text is None:
        raise FileNotFoundError("STATUS.md not found in task directory")

    plan_text = _read_file(task_dir, "PLAN.md")
    if plan_text is None:
        raise FileNotFoundError("PLAN.md not found in task directory")

    context_text = _read_file(task_dir, "CONTEXT.md") or ""

    # --- Determine current phase ---
    current_phase = phase_override or _extract_current_phase(status_text)
    if not current_phase:
        raise ValueError(
            "Cannot determine current phase from STATUS.md. "
            "Ensure 'current_phase:' or 'next_required_action:' field is present."
        )

    # --- Find phase block in PLAN.md ---
    phase_info = _find_phase_block(plan_text, current_phase)
    if phase_info is None:
        raise ValueError(
            f"Phase block for '{current_phase}' not found in PLAN.md. "
            f"Ensure PLAN.md has a '## {current_phase}:' heading."
        )

    heading, block_text = phase_info

    # --- Check STATUS/PLAN agreement (spec hard-stop rule 7) ---
    # If STATUS says one phase but PLAN marks a different one as current, flag it
    # We detect this by checking if STATUS mentions a different phase as "current"
    status_phase = _extract_current_phase(status_text)
    if phase_override and status_phase and status_phase != phase_override:
        # User override, allow but note
        pass

    # --- Extract phase data ---
    context_contract = _extract_context_contract(block_text)
    actions = _extract_actions(block_text)
    inputs = _extract_inputs(block_text)
    validation_items = _extract_validation(block_text)
    stop_rule = _extract_stop_rule(context_contract)
    education = _extract_education(block_text) if include_education else None
    validation_commands = _extract_validation_commands(context_text)
    _extract_constraints(context_text)
    phase_goal = _extract_phase_goal(heading, block_text)
    next_phase = _find_next_phase(plan_text, current_phase)

    # Extract target profile from PLAN.md artifact manifest
    target_profile = "qwen36"
    manifest_m = re.search(
        r"##\s*Artifact Manifest\s*\n(.*?)(?=##\s|\Z)", plan_text, re.DOTALL
    )
    if manifest_m:
        tp_m = re.search(r"target_profile\s*:\s*(\S+)", manifest_m.group(1))
        if tp_m:
            target_profile = tp_m.group(1).strip("`")

    # --- Build sections ---
    lines: list[str] = []

    # 1. Artifact Manifest
    lines.append(f"# Next Prompt: {current_phase}")
    lines.append("")
    lines.append("## Artifact Manifest")
    lines.append("- artifact_type: next_prompt")
    lines.append(f"- phase: {current_phase}")
    lines.append(f"- target_profile: {target_profile}")
    lines.append("- parent_plan: PLAN.md")
    lines.append("- version: 1.0.0")
    lines.append("")

    # 2. Mission
    lines.append("## Mission")
    lines.append("")
    # Build mission from goal with negative constraint
    negative_parts = []
    if stop_rule:
        negative_parts.append(stop_rule)
    if next_phase:
        negative_parts.append(f"Do not proceed to {next_phase}.")
    negative_parts.append("Do not invoke models or execute phases.")

    lines.append(phase_goal)
    lines.append("")
    if negative_parts:
        lines.append("**Hard boundary:** " + "  ".join(negative_parts))
        lines.append("")

    # 3. Read Order
    lines.append("## Read Order")
    lines.append("")
    read_order = [
        "STATUS.md — current phase and next action",
        f"{current_phase} section in PLAN.md — goal, actions, validation",
        "CONTEXT.md — constraints and validation commands",
    ]
    # Add phase-specific files from inputs
    for inp in inputs:
        # Clean up input entries that look like file paths
        clean_inp = inp.strip("- ").strip()
        if clean_inp.endswith(".md") or clean_inp.endswith(".py") or clean_inp.endswith(".json"):
            read_order.append(f"{clean_inp} — phase-specific input")
        else:
            read_order.append(f"{clean_inp}")
    # Add CHECKLIST.md, DECISIONS.md if they exist
    for optional in ["CHECKLIST.md", "DECISIONS.md", "ARTIFACTS.md", "PHASE_LOG.md"]:
        if _read_file(task_dir, optional) is not None:
            read_order.append(f"{optional} — optional context")
    for i, item in enumerate(read_order, 1):
        lines.append(f"{i}. {item}")
    lines.append("")

    # 4. Phase Contract
    lines.append("## Phase Contract")
    lines.append("")
    if compact:
        # Compact: only stop_rule and validation commands
        if stop_rule:
            lines.append(f"- **stop_rule:** {stop_rule}")
        if validation_commands:
            lines.append("- **validation:** " + "; ".join(validation_commands))
    else:
        # Include executor-relevant fields only (spec says omit executor, phase_type, compaction_trigger)
        contract_fields = [
            ("usable_phase_budget", "**budget**"),
            ("expected_tool_calls", "**expected_tool_calls**"),
            ("stop_rule", "**stop_rule**"),
            ("validation_output_reserve", "**validation_reserve**"),
        ]
        has_contract = False
        for key, label in contract_fields:
            if key in context_contract:
                lines.append(f"- {label}: {context_contract[key]}")
                has_contract = True
        if not has_contract:
            lines.append("- (no context contract defined for this phase)")
    lines.append("")

    # 5. Actions
    lines.append("## Actions")
    lines.append("")
    if actions:
        for i, action in enumerate(actions, 1):
            lines.append(f"{i}. {action}")
    else:
        lines.append("(no explicit actions defined for this phase)")
    lines.append("")

    # 6. Allowed and Disallowed Actions
    lines.append("## Allowed and Disallowed Actions")
    lines.append("")
    lines.append("| Allowed | Disallowed |")
    lines.append("|---|---|")
    allowed_entries = [a for a in actions[:3]] if actions else ["Read task-state files"]
    disallowed_entries = []
    if stop_rule:
        disallowed_entries.append(stop_rule)
    disallowed_entries.extend([
        "Editing files outside workspace",
        "Proceeding to the next phase",
        "Invoking models",
    ])
    for i in range(max(len(allowed_entries), len(disallowed_entries))):
        allowed = allowed_entries[i] if i < len(allowed_entries) else ""
        disallowed = disallowed_entries[i] if i < len(disallowed_entries) else ""
        lines.append(f"| {allowed} | {disallowed} |")
    lines.append("")

    # 7. Validation Commands
    lines.append("## Validation Commands")
    lines.append("")
    has_markdownlint = False
    if validation_commands:
        for cmd in validation_commands:
            lines.append(f"- {cmd}")
            if "markdownlint" in cmd:
                has_markdownlint = True
    elif validation_items:
        for item in validation_items:
            lines.append(f"- {item}")
    else:
        lines.append("- Run available project validation commands")

    # Add standard validators if not already included
    if not has_markdownlint:
        lines.append(
            "- `markdownlint . --ignore node_modules` (Markdown formatting)"
        )
    lines.append("")

    # 8. Task-State Closeout Requirements
    lines.append("## Closeout")
    lines.append("")
    lines.append(
        "Update `STATUS.md`, `PHASE_LOG.md`, `ARTIFACTS.md`, `CONTEXT.md`, "
        "`CHECKLIST.md`, and `NEXT_PROMPT.md` with compact facts only. "
        "Record changed files, commands run, validation result, blockers, "
        "carry-forward, do-not-carry-forward, and next action."
    )
    lines.append("")

    # 9. Recovery Procedure
    lines.append("## Recovery")
    lines.append("")
    lines.append("If validation fails or the phase cannot complete:")
    lines.append("1. Stop. Do not widen scope or start the next phase.")
    lines.append(
        "2. Set `STATUS.md` to `Blocked` with the failed gate and exact reason."
    )
    lines.append(
        "3. Add a `PHASE_LOG.md` entry with attempted action and validation result."
    )
    lines.append(
        "4. Write `NEXT_PROMPT.md` for human/frontier review with at most three options: "
        "fix, narrow scope, or abandon."
    )
    lines.append("")

    # 10. Self-Audit Requirements
    lines.append("## Self-Audit")
    lines.append("")
    lines.append("Before closeout, verify:")
    lines.append("- Original phase goal satisfied or blocker recorded")
    lines.append("- All validation commands executed or blocker documented")
    lines.append("- Side-effect boundaries respected")
    lines.append("- Task state updated with compact facts")
    lines.append("- No broad architecture decisions made without evidence")
    lines.append("")

    # 11. Ralph Loop Enforcement
    lines.append("## Ralph Loop Enforcement")
    lines.append("")
    lines.append("3 iterations required. Each is critique+fix; do not skip or collapse.")
    lines.append("")
    lines.append("1. **Critique** — Review against contract, find defects, fix them")
    lines.append("2. **Re-check** — After fixes, if no new defects → no-op; else fix")
    lines.append("3. **Final check** — If no defects → no-op; do not invent changes")
    lines.append("")
    lines.append("Each iteration needs a compact log entry in Ralph Summary.")
    lines.append("Ralph loops are critique/revision, not repeated tool calls.")

    # 12. Expected Final Output Format
    lines.append("## Expected Output Format")
    lines.append("")
    lines.append("```")
    lines.append("## Result")
    lines.append("## Evidence")
    lines.append("## Self-Audit")
    lines.append("## Ralph Summary")
    lines.append("## Validation")
    lines.append("## Declared vs Enforced")
    lines.append("## Risks / Next Action")
    lines.append("```")
    lines.append("")

    # 13. Hard Stop
    lines.append("## Hard Stop")
    lines.append("")
    if next_phase:
        lines.append(f"Do not proceed to {next_phase}.")
    lines.append(f"Current phase is {current_phase}. Do not move beyond it.")
    lines.append("Do not implement features outside this phase.")
    lines.append("Do not invoke models or execute phases.")
    lines.append("Do not edit files outside the current phase scope.")
    lines.append("")

    # 14. Deep Education Notes (optional)
    if include_education:
        lines.append("## Education Notes")
        lines.append("")
        if education:
            lines.append(education)
        else:
            lines.append(
                "Review the phase contract carefully. Focus on the stop_rule and "
                "validation commands before proceeding. Keep context budget in mind."
            )
        lines.append("")

    return "\n".join(lines)


def compile_next_prompt_cli(
    task_dir: str,
    output: str | None = None,
    phase: str | None = None,
    include_education: bool = False,
    dry_run: bool = False,
    compact: bool = False,
) -> int:
    """CLI handler for next-prompt subcommand.

    Returns exit code: 0=success, 2=error.
    """
    try:
        content = compile_next_prompt(
            task_dir=task_dir,
            phase_override=phase,
            include_education=include_education,
            compact=compact,
        )
    except FileNotFoundError as e:
        print(f"ERROR  {e}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"ERROR  {e}", file=sys.stderr)
        return 2

    if dry_run:
        print(content)
    else:
        out_path = Path(output) if output else Path(task_dir) / "NEXT_PROMPT.md"
        out_path.write_text(content, encoding="utf-8")
        print(f"OK  Generated {out_path} ({len(content)} chars, {content.count(chr(10))} lines)")

    return 0
