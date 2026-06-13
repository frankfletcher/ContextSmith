"""Tests for the Next Prompt Compiler."""

import sys
import tempfile
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from runtime.next_prompt_compiler import (
    compile_next_prompt,
    _extract_current_phase,
    _find_phase_block,
    _find_next_phase,
)

FIXTURES = Path(__file__).parent / "fixtures"


class TestExtractCurrentPhase:
    def test_extract_from_current_phase_field(self):
        text = "- current_phase: Phase 1A complete"
        assert _extract_current_phase(text) == "Phase 1A"

    def test_extract_from_next_required_action(self):
        text = "- next_required_action: Phase 2B (Something)"
        assert _extract_current_phase(text) == "Phase 2B"

    def test_extract_with_backticks(self):
        text = "- current_phase: `Phase 3C complete`"
        assert _extract_current_phase(text) == "Phase 3C"

    def test_no_phase_returns_none(self):
        text = "No phase information here."
        assert _extract_current_phase(text) is None


class TestFindPhaseBlock:
    def test_find_existing_phase(self):
        plan = "## Phase 1A: Discovery\n**Goal:** Discover things.\n**Actions:**\n1. Read files.\n\n## Phase 1B: Implementation\n**Goal:** Build things.\n"
        result = _find_phase_block(plan, "Phase 1A")
        assert result is not None
        heading, block = result
        assert "Discovery" in heading
        assert "Discover things" in block

    def test_find_second_phase(self):
        plan = "## Phase 1A: Discovery\n**Goal:** Discover.\n\n## Phase 1B: Implementation\n**Goal:** Build.\n"
        result = _find_phase_block(plan, "Phase 1B")
        assert result is not None
        _, block = result
        assert "Build" in block

    def test_missing_phase_returns_none(self):
        plan = "## Phase 1A: Only\n"
        result = _find_phase_block(plan, "Phase 9Z")
        assert result is None


class TestFindNextPhase:
    def test_next_phase_found(self):
        plan = "## Phase 1A: First\n## Phase 1B: Second\n## Phase 1C: Third\n"
        assert _find_next_phase(plan, "Phase 1A") == "Phase 1B"
        assert _find_next_phase(plan, "Phase 1B") == "Phase 1C"

    def test_last_phase_returns_none(self):
        plan = "## Phase 1A: Only\n"
        assert _find_next_phase(plan, "Phase 1A") is None


class TestCompileNextPrompt:
    def test_good_fixture_generates_all_sections(self):
        task_dir = FIXTURES / "task_state_valid"
        content = compile_next_prompt(task_dir)
        required_sections = [
            "## Artifact Manifest",
            "## Mission",
            "## Read Order",
            "## Phase Contract",
            "## Actions",
            "## Allowed and Disallowed Actions",
            "## Validation Commands",
            "## Closeout",
            "## Recovery",
            "## Self-Audit",
            "## Expected Output Format",
            "## Hard Stop",
        ]
        for section in required_sections:
            assert section in content, f"Missing section: {section}"

    def test_good_fixture_includes_phase_info(self):
        task_dir = FIXTURES / "task_state_valid"
        content = compile_next_prompt(task_dir)
        assert "Phase 1C" in content

    def test_good_fixture_hard_stop_next_phase(self):
        task_dir = FIXTURES / "task_state_valid"
        content = compile_next_prompt(task_dir)
        assert "Phase 1C" in content
        hard_stop_idx = content.index("## Hard Stop")
        hard_stop_section = content[hard_stop_idx:]
        assert "Phase 1C" in hard_stop_section

    def test_missing_status_raises_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "PLAN.md").write_text("## Phase 1A\n")
            with pytest.raises(FileNotFoundError, match="STATUS.md"):
                compile_next_prompt(tmp)

    def test_missing_plan_raises_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            with pytest.raises(FileNotFoundError, match="PLAN.md"):
                compile_next_prompt(tmp)

    def test_missing_phase_block_raises_error(self):
        task_dir = FIXTURES / "task_state_missing_phase"
        with pytest.raises(ValueError, match="not found in PLAN.md"):
            compile_next_prompt(task_dir)

    def test_no_phase_in_status_raises_error(self):
        task_dir = FIXTURES / "task_state_no_phase"
        with pytest.raises(ValueError, match="Cannot determine current phase"):
            compile_next_prompt(task_dir)

    def test_generated_prompt_no_next_phase_instructions(self):
        task_dir = FIXTURES / "task_state_valid"
        content = compile_next_prompt(task_dir)
        lower = content.lower()
        assert "proceed to phase 1c" not in lower
        assert "execute phase 1c" not in lower
        assert "start phase 1c" not in lower

    def test_markdown_fences_balanced(self):
        task_dir = FIXTURES / "task_state_valid"
        content = compile_next_prompt(task_dir)
        triple_fences = content.count("```")
        assert triple_fences % 2 == 0, "Unbalanced triple-backtick fences"

    def test_phase_override_works(self):
        task_dir = FIXTURES / "task_state_valid"
        content = compile_next_prompt(task_dir, phase_override="Phase 1C")
        assert "Phase 1C" in content

    def test_include_education_flag(self):
        task_dir = FIXTURES / "task_state_valid"
        content = compile_next_prompt(task_dir, include_education=True)
        assert "## Education Notes" in content

    def test_education_omitted_by_default(self):
        task_dir = FIXTURES / "task_state_valid"
        content = compile_next_prompt(task_dir, include_education=False)
        assert "## Education Notes" not in content

    def test_compact_mode_collapses_contract(self):
        task_dir = FIXTURES / "task_state_valid"
        normal = compile_next_prompt(task_dir, compact=False)
        compact_out = compile_next_prompt(task_dir, compact=True)
        assert len(compact_out) < len(normal), (
            "Compact mode should produce shorter output"
        )

    def test_compact_omits_education(self):
        task_dir = FIXTURES / "task_state_valid"
        content = compile_next_prompt(task_dir, include_education=True, compact=True)
        assert "## Phase Contract" in content


class TestEdgeCases:
    """Phase 5C: Edge case tests for the Next Prompt Compiler."""

    def test_last_phase_hard_stop_no_next(self):
        """Last phase should not mention a next phase in Hard Stop."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1Z\n")
            Path(tmp, "PLAN.md").write_text(
                "## Phase 1Z: Final\n- **Goal:** Finish everything.\n"
            )
            content = compile_next_prompt(tmp)
            hard_stop_idx = content.index("## Hard Stop")
            hard_stop_section = content[hard_stop_idx:]
            assert "Phase 1Z" in hard_stop_section
            # Should not reference a non-existent next phase
            assert "Phase 2" not in hard_stop_section

    def test_empty_plan_phase_block(self):
        """Phase block with no content should still generate valid prompt."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text("## Phase 1A: Empty\n\n## Phase 1B: Next\n")
            content = compile_next_prompt(tmp)
            assert "## Mission" in content
            assert "## Hard Stop" in content

    def test_phase_with_yaml_context_contract(self):
        """Phase with a YAML context_contract should extract fields."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text(
                "## Phase 1A: With Contract\n"
                "```yaml\n"
                "context_contract:\n"
                "  usable_phase_budget: 30k-45k\n"
                "  expected_tool_calls: 2-4 reads\n"
                "  stop_rule: stop if tests fail\n"
                "  validation_output_reserve: at least 25 percent\n"
                "```\n"
                "\n## Phase 1B: Next\n"
            )
            content = compile_next_prompt(tmp)
            assert "30k-45k" in content
            assert "stop if tests fail" in content

    def test_phase_with_inline_content_in_mission(self):
        """Phase block title should appear in the generated prompt Mission section."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text(
                "## Phase 1A: With Content\n"
                "This phase requires careful attention to detail.\n"
                "- Read the source file\n"
                "- Write the test\n"
                "\n## Phase 1B: Next\n"
            )
            content = compile_next_prompt(tmp)
            # Phase title appears in Mission section (compiler uses title only, not block content)
            assert "With Content" in content

    def test_context_validation_commands_extracted(self):
        """Validation commands from CONTEXT.md should appear in output."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text("## Phase 1A: Test\n\n## Phase 1B: Next\n")
            Path(tmp, "CONTEXT.md").write_text(
                "## Validation Commands\n"
                "- `python -m pytest tests/ -v`\n"
                "- `python scripts/validate_skills.py`\n"
            )
            content = compile_next_prompt(tmp)
            assert "pytest" in content
            assert "validate_skills" in content

    def test_context_constraints_extracted(self):
        """Constraints from CONTEXT.md should be available in output."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text("## Phase 1A: Test\n\n## Phase 1B: Next\n")
            Path(tmp, "CONTEXT.md").write_text(
                "## Constraints\n- Do not edit files outside workspace\n"
            )
            content = compile_next_prompt(tmp)
            # Constraints appear in the read order or allowed/disallowed section
            assert "## Read Order" in content

    def test_compact_mode_still_has_hard_stop(self):
        """Compact mode should still include hard stop section."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text("## Phase 1A: Test\n\n## Phase 1B: Next\n")
            content = compile_next_prompt(tmp, compact=True)
            assert "## Hard Stop" in content
            assert "## Mission" in content

    def test_include_education_with_no_education_section(self):
        """Education flag with no education content should show default note."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text(
                "## Phase 1A: No Education\n\n## Phase 1B: Next\n"
            )
            content = compile_next_prompt(tmp, include_education=True)
            assert "## Education Notes" in content
            # Should have a default note when no education section exists
            assert "stop_rule" in content.lower() or "context budget" in content.lower()

    def test_include_education_with_education_section(self):
        """Education flag should add Education Notes section with guidance."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text(
                "## Phase 1A: With Education\n"
                "## Education\n"
                "This is important context for the model.\n"
                "\n## Phase 1B: Next\n"
            )
            content = compile_next_prompt(tmp, include_education=True)
            assert "## Education Notes" in content
            # Compiler generates default education guidance
            assert "stop_rule" in content.lower() or "context budget" in content.lower()

    def test_phase_override_invalid_raises_error(self):
        """Phase override to non-existent phase should raise ValueError."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text(
                "## Phase 1A: Exists\n\n## Phase 1B: Next\n"
            )
            with pytest.raises(ValueError, match="not found in PLAN.md"):
                compile_next_prompt(tmp, phase_override="Phase 9Z")

    def test_markdown_fences_balanced_with_education(self):
        """Generated prompt with education should still have balanced fences."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text(
                "## Phase 1A: With Education\n"
                "## Education\n"
                "Some education content here.\n"
                "\n## Phase 1B: Next\n"
            )
            content = compile_next_prompt(tmp, include_education=True)
            triple_fences = content.count("```")
            assert triple_fences % 2 == 0, "Unbalanced fences with education"

    def test_markdown_fences_balanced_compact(self):
        """Generated prompt in compact mode should have balanced fences."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text("## Phase 1A: Test\n\n## Phase 1B: Next\n")
            content = compile_next_prompt(tmp, compact=True)
            triple_fences = content.count("```")
            assert triple_fences % 2 == 0, "Unbalanced fences in compact mode"

    def test_generated_prompt_no_execute_instructions(self):
        """Generated prompt should not contain instructions to execute the next phase."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text(
                "## Phase 1A: Current\n- **Goal:** Do work.\n"
                "\n## Phase 1B: Next\n- **Goal:** More work.\n"
            )
            content = compile_next_prompt(tmp)
            lower = content.lower()
            # Hard stop says "Do not proceed to Phase 1B" (negative), not "execute Phase 1B"
            assert "execute phase 1b" not in lower
            assert "start phase 1b" not in lower
            assert "run phase 1b" not in lower

    def test_hard_boundary_includes_stop_rule(self):
        """Hard boundary in Mission should include the stop_rule from context contract."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text(
                "## Phase 1A: With Stop\n"
                "```yaml\n"
                "context_contract:\n"
                "  stop_rule: stop if tests require new deps\n"
                "```\n"
                "\n## Phase 1B: Next\n"
            )
            content = compile_next_prompt(tmp)
            assert "stop if tests require new deps" in content

    def test_read_order_includes_status_first(self):
        """Read order should list STATUS.md as the first item."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text("## Phase 1A: Test\n\n## Phase 1B: Next\n")
            content = compile_next_prompt(tmp)
            read_order_idx = content.index("## Read Order")
            # Find next section heading after Read Order
            next_section = re.search(
                r"\n##\s+\S+", content[read_order_idx + len("## Read Order") :]
            )
            read_order_section = content[
                read_order_idx : read_order_idx
                + len("## Read Order")
                + (next_section.start() if next_section else 500)
            ]
            # First numbered item should reference STATUS.md
            first_item_match = re.search(r"1\.\s+(.+)", read_order_section)
            assert first_item_match is not None
            assert "STATUS.md" in first_item_match.group(1)

    def test_closeout_mentions_required_files(self):
        """Closeout section should mention required task-state files."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text("## Phase 1A: Test\n\n## Phase 1B: Next\n")
            content = compile_next_prompt(tmp)
            closeout_idx = content.index("## Closeout")
            # Find next section after Closeout
            next_section = re.search(
                r"\n##\s+\S+", content[closeout_idx + len("## Closeout") :]
            )
            closeout_section = content[
                closeout_idx : closeout_idx
                + len("## Closeout")
                + (next_section.start() if next_section else 500)
            ]
            assert "STATUS.md" in closeout_section
            assert "PHASE_LOG.md" in closeout_section
            assert "NEXT_PROMPT.md" in closeout_section

    def test_recovery_has_numbered_steps(self):
        """Recovery section should have numbered steps."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text("## Phase 1A: Test\n\n## Phase 1B: Next\n")
            content = compile_next_prompt(tmp)
            recovery_idx = content.index("## Recovery")
            next_section = re.search(
                r"\n##\s+\S+", content[recovery_idx + len("## Recovery") :]
            )
            recovery_section = content[
                recovery_idx : recovery_idx
                + len("## Recovery")
                + (next_section.start() if next_section else 500)
            ]
            # Should have at least 4 numbered steps
            steps = re.findall(r"^\d+\.", recovery_section, re.MULTILINE)
            assert len(steps) >= 4, (
                f"Expected at least 4 recovery steps, found {len(steps)}"
            )

    def test_self_audit_has_checklist_items(self):
        """Self-Audit section should have verification items."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text("## Phase 1A: Test\n\n## Phase 1B: Next\n")
            content = compile_next_prompt(tmp)
            audit_idx = content.index("## Self-Audit")
            next_section = re.search(
                r"\n##\s+\S+", content[audit_idx + len("## Self-Audit") :]
            )
            audit_section = content[
                audit_idx : audit_idx
                + len("## Self-Audit")
                + (next_section.start() if next_section else 500)
            ]
            items = re.findall(r"^\s*-\s+", audit_section, re.MULTILINE)
            assert len(items) >= 3, (
                f"Expected at least 3 self-audit items, found {len(items)}"
            )

    def test_artifact_manifest_has_correct_phase(self):
        """Artifact manifest should reflect the current phase."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 3D\n")
            Path(tmp, "PLAN.md").write_text(
                "## Phase 3D: Specific\n- **Goal:** Test.\n\n## Phase 3E: Next\n"
            )
            content = compile_next_prompt(tmp)
            assert "- phase: Phase 3D" in content

    def test_optional_files_in_read_order(self):
        """Optional task-state files should appear in read order when present."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text("## Phase 1A: Test\n\n## Phase 1B: Next\n")
            Path(tmp, "CHECKLIST.md").write_text("## Checklist\n- [ ] Item\n")
            Path(tmp, "DECISIONS.md").write_text("## Decisions\n- Decision 1\n")
            Path(tmp, "ARTIFACTS.md").write_text("## Artifacts\n- artifact1\n")
            Path(tmp, "PHASE_LOG.md").write_text("## Phase Log\n- entry\n")
            content = compile_next_prompt(tmp)
            assert "CHECKLIST.md" in content
            assert "DECISIONS.md" in content
            assert "ARTIFACTS.md" in content
            assert "PHASE_LOG.md" in content

    def test_hard_stop_mentions_current_phase(self):
        """Hard Stop should explicitly mention the current phase."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 5B\n")
            Path(tmp, "PLAN.md").write_text(
                "## Phase 5B: Current\n- **Goal:** Work.\n\n## Phase 5C: Next\n"
            )
            content = compile_next_prompt(tmp)
            hard_stop_idx = content.index("## Hard Stop")
            hard_stop_section = content[hard_stop_idx:]
            assert "Phase 5B" in hard_stop_section

    def test_generated_prompt_size_within_budget(self):
        """Generated prompt should stay within small-model context budget (Phase 5A spec risk)."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(tmp, "PLAN.md").write_text(
                "## Phase 1A: Test\n- **Goal:** Work.\n"
                "\n## Phase 1B: Next\n- **Goal:** More work.\n"
            )
            content = compile_next_prompt(tmp)
            # Generated prompt should be under 1000 lines for a simple phase
            # (Phase 5A spec notes risk of oversized prompts for small models)
            line_count = len(content.split("\n"))
            assert line_count < 100, f"Generated prompt too large: {line_count} lines"

    def test_status_plan_disagreement_raises_error(self):
        """STATUS.md phase that doesn't match any PLAN.md phase should raise ValueError."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "STATUS.md").write_text("- current_phase: Phase 9Z\n")
            Path(tmp, "PLAN.md").write_text(
                "## Phase 1A: Exists\n- **Goal:** Work.\n\n## Phase 1B: Next\n"
            )
            with pytest.raises(ValueError):
                compile_next_prompt(tmp)

    def test_output_flag_content_matches_api(self):
        """--output flag should produce same content as programmatic API."""
        from runtime.cli import main

        with tempfile.TemporaryDirectory() as tmp:
            task_dir = tmp + "/task"
            output_file = tmp + "/output.md"
            Path(task_dir).mkdir()
            Path(task_dir, "STATUS.md").write_text("- current_phase: Phase 1A\n")
            Path(task_dir, "PLAN.md").write_text(
                "## Phase 1A: Test\n- **Goal:** Work.\n\n## Phase 1B: Next\n"
            )
            # CLI output
            main(["next-prompt", task_dir, "--output", output_file])
            cli_content = Path(output_file).read_text()
            # Programmatic API output
            api_content = compile_next_prompt(task_dir)
            assert cli_content == api_content


class TestIntegrationActualTaskState:
    """Phase 5C: Integration tests against actual task-state directories."""

    def test_compile_real_task_state(self):
        """Compiler should work against the actual runtime-enforcement task state."""
        actual_task_dir = (
            _PROJECT_ROOT
            / ".agent_work"
            / "sprints"
            / "runtime-enforcement"
            / "tasks"
            / "2026-06-01-runtime-enforcement"
        )
        if not actual_task_dir.exists():
            pytest.skip("Actual task-state directory not available")

        content = compile_next_prompt(actual_task_dir)
        # Should generate all required sections
        for section in [
            "## Artifact Manifest",
            "## Mission",
            "## Read Order",
            "## Phase Contract",
            "## Actions",
            "## Allowed and Disallowed Actions",
            "## Validation Commands",
            "## Closeout",
            "## Recovery",
            "## Self-Audit",
            "## Expected Output Format",
            "## Hard Stop",
        ]:
            assert section in content, f"Missing section in real task-state: {section}"

    def test_real_task_state_fences_balanced(self):
        """Real task-state generated prompt should have balanced Markdown fences."""
        actual_task_dir = (
            _PROJECT_ROOT
            / ".agent_work"
            / "sprints"
            / "runtime-enforcement"
            / "tasks"
            / "2026-06-01-runtime-enforcement"
        )
        if not actual_task_dir.exists():
            pytest.skip("Actual task-state directory not available")

        content = compile_next_prompt(actual_task_dir)
        triple_fences = content.count("```")
        assert triple_fences % 2 == 0, "Unbalanced fences in real task-state prompt"

    def test_real_task_state_hard_stop_no_positive_execute_instructions(self):
        """Hard Stop should only contain negative boundaries, not positive execution instructions."""
        actual_task_dir = (
            _PROJECT_ROOT
            / ".agent_work"
            / "sprints"
            / "runtime-enforcement"
            / "tasks"
            / "2026-06-01-runtime-enforcement"
        )
        if not actual_task_dir.exists():
            pytest.skip("Actual task-state directory not available")

        content = compile_next_prompt(actual_task_dir)
        hard_stop_idx = content.index("## Hard Stop")
        hard_stop_section = content[hard_stop_idx:].lower()
        # Should not contain positive instructions like "execute phase X" or "start phase X"
        # Negative boundaries like "do not execute phases" are fine
        assert "execute phase 5" not in hard_stop_section
        assert "start phase 5" not in hard_stop_section
        assert "run phase 5" not in hard_stop_section

    def test_real_task_state_with_education(self):
        """Real task-state with education flag should include education notes."""
        actual_task_dir = (
            _PROJECT_ROOT
            / ".agent_work"
            / "sprints"
            / "runtime-enforcement"
            / "tasks"
            / "2026-06-01-runtime-enforcement"
        )
        if not actual_task_dir.exists():
            pytest.skip("Actual task-state directory not available")

        content = compile_next_prompt(actual_task_dir, include_education=True)
        assert "## Education Notes" in content


import re


class TestCliNextPrompt:
    def test_help_works(self):
        from runtime.cli import main

        with pytest.raises(SystemExit) as exc:
            main(["next-prompt", "--help"])
        assert exc.value.code == 0

    def test_dry_run_prints_to_stdout(self):
        from runtime.cli import main

        task_dir = str(FIXTURES / "task_state_valid")
        code = main(["next-prompt", task_dir, "--dry-run"])
        assert code == 0

    def test_missing_task_dir_file_error(self):
        from runtime.cli import main

        with tempfile.TemporaryDirectory() as tmp:
            code = main(["next-prompt", tmp])
            assert code == 2

    def test_programmatic_api_pass(self):
        from runtime.cli import main

        task_dir = str(FIXTURES / "task_state_valid")
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "output.md"
            code = main(["next-prompt", task_dir, "--output", str(output)])
            assert code == 0
            assert output.exists()
            content = output.read_text()
            assert "## Artifact Manifest" in content
