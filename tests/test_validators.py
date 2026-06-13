"""Tests for orchestrator validators."""

from pathlib import Path

from orchestrator.validators import (
    _extract_sections,
    validate_artifact,
    validate_artifacts,
    validate_file_exists,
    validate_file_nonempty,
    validate_required_sections,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"
SCHEMAS_DIR = Path(__file__).parent.parent / "schemas"


class TestExtractSections:
    """Tests for _extract_sections helper."""

    def test_extract_sections_from_valid_status(self):
        """Test extracting sections from a valid STATUS.md."""
        content = (FIXTURES_DIR / "task_state_valid" / "STATUS.md").read_text()
        sections = _extract_sections(content)
        assert "Current Phase" in sections
        assert "Current State" in sections
        assert "Progress" in sections
        assert "Next Action" in sections
        assert "Blocked By" in sections

    def test_extract_sections_empty_content(self):
        """Test extracting sections from empty content returns empty list."""
        assert _extract_sections("") == []

    def test_extract_sections_no_headings(self):
        """Test extracting sections from content without headings."""
        assert _extract_sections("Some plain text\nwithout headings.") == []

    def test_extract_sections_skips_non_atx_headings(self):
        """Test only ## headings are extracted, not # or ###."""
        content = "# Top\n\n## Section 1\n\n### Sub\n\n## Section 2"
        sections = _extract_sections(content)
        assert "Section 1" in sections
        assert "Section 2" in sections
        assert "Top" not in sections
        assert "Sub" not in sections


class TestValidateFileExists:
    """Tests for validate_file_exists."""

    def test_success(self):
        """Test returns [] when file exists."""
        path = FIXTURES_DIR / "task_state_valid" / "STATUS.md"
        assert validate_file_exists(path) == []

    def test_failure(self):
        """Test returns error when file does not exist."""
        path = FIXTURES_DIR / "task_state_missing_status" / "STATUS.md"
        errors = validate_file_exists(path)
        assert len(errors) == 1
        assert "Missing required file" in errors[0]
        assert "STATUS.md" in errors[0]

    def test_nonexistent_path(self):
        """Test returns error for path that doesn't exist at all."""
        path = FIXTURES_DIR / "nonexistent_file.txt"
        errors = validate_file_exists(path)
        assert len(errors) == 1
        assert "Missing required file" in errors[0]


class TestValidateFileNonempty:
    """Tests for validate_file_nonempty."""

    def test_success(self):
        """Test returns [] when file has content."""
        path = FIXTURES_DIR / "task_state_valid" / "STATUS.md"
        assert validate_file_nonempty(path) == []

    def test_failure(self):
        """Test returns error when file is empty."""
        path = FIXTURES_DIR / "task_state_empty_plan" / "PLAN.md"
        errors = validate_file_nonempty(path)
        assert len(errors) == 1
        assert "File is empty" in errors[0]
        assert "PLAN.md" in errors[0]

    def test_nonexistent_file(self):
        """Test returns error when file doesn't exist."""
        path = FIXTURES_DIR / "task_state_valid" / "NONEXISTENT.md"
        errors = validate_file_nonempty(path)
        assert len(errors) == 1
        assert "Missing required file" in errors[0]


class TestValidateRequiredSections:
    """Tests for validate_required_sections."""

    def test_all_present(self):
        """Test returns [] when all required sections are present."""
        path = FIXTURES_DIR / "task_state_valid" / "STATUS.md"
        errors = validate_required_sections(
            path, ["Current Phase", "Current State", "Next Action"]
        )
        assert errors == []

    def test_some_missing(self):
        """Test returns error when some sections are missing."""
        path = FIXTURES_DIR / "task_state_valid" / "STATUS.md"
        errors = validate_required_sections(
            path, ["Current Phase", "Fake Section", "Nonexistent"]
        )
        assert len(errors) == 2
        assert all("Missing required section" in e for e in errors)

    def test_all_missing(self):
        """Test returns errors when no sections are found."""
        path = FIXTURES_DIR / "task_state_valid" / "STATUS.md"
        errors = validate_required_sections(path, ["Alpha", "Beta", "Gamma"])
        assert len(errors) == 3

    def test_empty_sections_list(self):
        """Test returns [] when no sections are required."""
        path = FIXTURES_DIR / "task_state_valid" / "STATUS.md"
        assert validate_required_sections(path, []) == []

    def test_nonexistent_file(self):
        """Test returns error when file doesn't exist."""
        path = FIXTURES_DIR / "nonexistent.md"
        errors = validate_required_sections(path, ["Current Phase"])
        assert len(errors) == 1
        assert "Missing required file" in errors[0]

    def test_empty_file(self):
        """Test returns error when file is empty."""
        path = FIXTURES_DIR / "task_state_empty_plan" / "PLAN.md"
        errors = validate_required_sections(path, ["Phases"])
        assert len(errors) == 1
        assert "File is empty" in errors[0]


class TestValidateArtifact:
    """Tests for validate_artifact combining all checks."""

    def test_all_checks_pass(self):
        """Test artifact passes all checks."""
        path = FIXTURES_DIR / "task_state_valid" / "STATUS.md"
        errors = validate_artifact(path, ["Current Phase", "Current State"])
        assert errors == []

    def test_missing_file(self):
        """Test artifact fails when file missing."""
        path = FIXTURES_DIR / "task_state_missing_status" / "STATUS.md"
        errors = validate_artifact(path, ["Current Phase"])
        assert len(errors) == 1
        assert "Missing required file" in errors[0]

    def test_empty_file(self):
        """Test artifact fails when file empty."""
        path = FIXTURES_DIR / "task_state_empty_plan" / "PLAN.md"
        errors = validate_artifact(path, ["Phases"])
        assert len(errors) == 1
        assert "File is empty" in errors[0]

    def test_missing_sections(self):
        """Test artifact fails when required sections missing."""
        path = FIXTURES_DIR / "task_state_valid" / "STATUS.md"
        errors = validate_artifact(
            path, ["Current Phase", "Section That Does Not Exist"]
        )
        assert len(errors) == 1
        assert "Missing required section" in errors[0]

    def test_no_required_sections(self):
        """Test artifact passes when no sections required."""
        path = FIXTURES_DIR / "task_state_valid" / "STATUS.md"
        assert validate_artifact(path) == []

    def test_plan_file_validation(self):
        """Test PLAN.md validation with its required sections."""
        path = FIXTURES_DIR / "task_state_valid" / "PLAN.md"
        errors = validate_artifact(path, ["Phases", "Validation Gates"])
        assert errors == []


class TestValidateArtifacts:
    """Tests for validate_artifacts batch validation."""

    def test_all_pass(self):
        """Test all artifacts pass validation."""
        state_dir = FIXTURES_DIR / "task_state_valid"
        result = validate_artifacts(
            state_dir, ["STATUS.md", "PLAN.md", "CONTEXT.md"], {}
        )
        assert result["passed"] is True
        assert result["failures"] == []
        assert result["files_checked"] == 3
        assert result["files_passed"] == 3

    def test_all_pass_with_section_config(self):
        """Test all artifacts pass with section requirements."""
        state_dir = FIXTURES_DIR / "task_state_valid"
        config = {
            "section_requirements": {
                "STATUS.md": ["Current Phase", "Current State", "Next Action"],
                "PLAN.md": ["Phases", "Validation Gates"],
            }
        }
        result = validate_artifacts(state_dir, ["STATUS.md", "PLAN.md"], config)
        assert result["passed"] is True
        assert result["failures"] == []
        assert result["files_checked"] == 2
        assert result["files_passed"] == 2

    def test_some_fail(self):
        """Test some artifacts fail validation."""
        state_dir = FIXTURES_DIR / "task_state_missing_status"
        result = validate_artifacts(
            state_dir, ["STATUS.md", "PLAN.md", "CONTEXT.md"], {}
        )
        assert result["passed"] is False
        assert "STATUS.md" in result["failures"][0]
        assert result["files_checked"] == 3
        assert result["files_passed"] == 2

    def test_empty_expected_outputs(self):
        """Test validation passes with no expected outputs."""
        state_dir = FIXTURES_DIR / "task_state_valid"
        result = validate_artifacts(state_dir, [], {})
        assert result["passed"] is True
        assert result["failures"] == []
        assert result["files_checked"] == 0
        assert result["files_passed"] == 0

    def test_with_config_missing_sections(self):
        """Test validation catches missing sections from config."""
        state_dir = FIXTURES_DIR / "task_state_valid"
        config = {
            "section_requirements": {
                "STATUS.md": ["Current Phase", "Section That Does Not Exist"],
            }
        }
        result = validate_artifacts(state_dir, ["STATUS.md"], config)
        assert result["passed"] is False
        assert len(result["failures"]) == 1
        assert "Missing required section" in result["failures"][0]
        assert result["files_checked"] == 1
        assert result["files_passed"] == 0

    def test_nonexistent_state_dir(self):
        """Test validation with non-existent state directory."""
        state_dir = FIXTURES_DIR / "nonexistent_dir"
        result = validate_artifacts(state_dir, ["STATUS.md"], {})
        assert result["passed"] is False
        assert len(result["failures"]) >= 1
        assert "Missing required file" in result["failures"][0]

    def test_checks_checkpoint_json(self):
        """Test validation of checkpoint.json."""
        state_dir = FIXTURES_DIR / "task_state_valid"
        result = validate_artifacts(state_dir, ["checkpoint.json"], {})
        assert result["passed"] is True
        assert result["files_checked"] == 1
        assert result["files_passed"] == 1


class TestValidateSchema:
    """Tests for validate_schema."""

    def test_valid_data(self):
        """Test valid data passes schema validation."""
        from orchestrator.validators import validate_schema

        schema_path = SCHEMAS_DIR / "workflow_config.schema.json"
        data = {
            "workflow_id": "test-valid",
            "version": 1,
            "domain": "coding",
            "mode": "phased-run",
        }
        assert validate_schema(data, schema_path) == []

    def test_invalid_data(self):
        """Test invalid data fails schema validation."""
        from orchestrator.validators import validate_schema

        schema_path = SCHEMAS_DIR / "workflow_config.schema.json"
        data = {"workflow_id": "test-invalid"}  # missing version, domain, mode
        errors = validate_schema(data, schema_path)
        assert len(errors) >= 1
        assert all("Schema validation failed" in e for e in errors)

    def test_missing_schema_file(self):
        """Test schema validation with missing schema file."""
        from orchestrator.validators import validate_schema

        schema_path = FIXTURES_DIR / "nonexistent_schema.json"
        data = {"key": "value"}
        errors = validate_schema(data, schema_path)
        assert len(errors) >= 1
        assert any("Schema validation failed" in e for e in errors)


class TestValidateWorkflowConfig:
    """Tests for validate_workflow_config."""

    def test_valid_config(self):
        """Test valid workflow config passes."""
        from orchestrator.validators import validate_workflow_config

        path = FIXTURES_DIR / "valid_workflow_simple_audit.yaml"
        assert validate_workflow_config(path) == []

    def test_missing_field(self):
        """Test workflow with missing field fails validation."""
        from orchestrator.validators import validate_workflow_config

        path = FIXTURES_DIR / "invalid_workflow_missing_field.yaml"
        errors = validate_workflow_config(path)
        assert len(errors) >= 1
        assert all("Schema validation failed" in e for e in errors)


class TestValidateAgentConfig:
    """Tests for validate_agent_config."""

    def test_valid_config(self):
        """Test valid agent config passes."""
        from orchestrator.validators import validate_agent_config

        path = FIXTURES_DIR / "valid_agent_auditor.yaml"
        assert validate_agent_config(path) == []

    def test_missing_permission(self):
        """Test agent with missing permission fails."""
        from orchestrator.validators import validate_agent_config

        path = FIXTURES_DIR / "invalid_agent_missing_permission.yaml"
        errors = validate_agent_config(path)
        assert len(errors) >= 1
        assert all("Schema validation failed" in e for e in errors)


class TestValidateCheckpointFile:
    """Tests for validate_checkpoint_file."""

    def test_valid(self):
        """Test valid checkpoint passes."""
        from orchestrator.validators import validate_checkpoint_file

        path = FIXTURES_DIR / "task_state_valid" / "checkpoint.json"
        assert validate_checkpoint_file(path) == []

    def test_invalid_json(self):
        """Test malformed checkpoint JSON fails."""
        from orchestrator.validators import validate_checkpoint_file

        path = FIXTURES_DIR / "task_state_invalid_checkpoint" / "checkpoint.json"
        errors = validate_checkpoint_file(path)
        assert len(errors) >= 1
        assert any("Schema validation failed" in e for e in errors)

    def test_missing_required_fields(self):
        """Test checkpoint with missing required fields fails."""
        import json
        import tempfile
        from orchestrator.validators import validate_checkpoint_file

        data = {"workflow_id": "partial"}  # missing version, current_phase, etc.
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            tmp_path = Path(f.name)
        try:
            errors = validate_checkpoint_file(tmp_path)
            assert len(errors) >= 1
        finally:
            tmp_path.unlink()


class TestValidateStateConsistency:
    """Tests for validate_state_consistency."""

    CONFIG = {
        "phase_order": ["phase_1", "phase_2", "phase_3"],
        "states": {
            "phase_1": {"state": "execute"},
            "phase_2": {"state": "audit"},
            "phase_3": {"state": "closeout"},
        },
    }

    def test_consistent_state(self):
        """Test consistent STATUS.md, checkpoint, and config passes."""
        from orchestrator.validators import validate_state_consistency

        status = {"current_phase": "phase_1", "current_state": "execute"}
        checkpoint = {
            "current_phase": "phase_1",
            "current_state": "execute",
            "completed_phases": [],
        }
        assert validate_state_consistency(status, checkpoint, self.CONFIG) == []

    def test_inconsistent_phase(self):
        """Test when STATUS.md phase doesn't match checkpoint."""
        from orchestrator.validators import validate_state_consistency

        status = {"current_phase": "phase_1", "current_state": "execute"}
        checkpoint = {
            "current_phase": "phase_2",  # mismatch
            "current_state": "execute",
            "completed_phases": [],
        }
        errors = validate_state_consistency(status, checkpoint, self.CONFIG)
        assert len(errors) >= 1
        assert "STATUS.md current_phase" in errors[0]
        assert "phase_1" in errors[0]
        assert "phase_2" in errors[0]

    def test_phase_not_in_phase_order(self):
        """Test when checkpoint phase is not in config phase_order."""
        from orchestrator.validators import validate_state_consistency

        status = {"current_phase": "phase_unknown", "current_state": "execute"}
        checkpoint = {
            "current_phase": "phase_unknown",
            "current_state": "execute",
            "completed_phases": [],
        }
        errors = validate_state_consistency(status, checkpoint, self.CONFIG)
        assert len(errors) >= 1
        assert any("not in config phase_order" in e for e in errors)

    def test_completed_phase_not_in_phase_order(self):
        """Test when a completed phase is not in config phase_order."""
        from orchestrator.validators import validate_state_consistency

        status = {"current_phase": "phase_2", "current_state": "audit"}
        checkpoint = {
            "current_phase": "phase_2",
            "current_state": "audit",
            "completed_phases": ["phase_1", "phase_bad"],
        }
        errors = validate_state_consistency(status, checkpoint, self.CONFIG)
        assert len(errors) >= 1
        assert any("completed phase" in e for e in errors)
        assert "phase_bad" in str(errors)

    def test_inconsistent_state(self):
        """Test when STATUS.md state doesn't match checkpoint."""
        from orchestrator.validators import validate_state_consistency

        status = {"current_phase": "phase_1", "current_state": "execute"}
        checkpoint = {
            "current_phase": "phase_1",
            "current_state": "audit",  # mismatch
            "completed_phases": [],
        }
        errors = validate_state_consistency(status, checkpoint, self.CONFIG)
        assert len(errors) >= 1
        assert "STATUS.md current_state" in errors[0]
        assert "execute" in errors[0]
        assert "audit" in errors[0]

    def test_state_not_in_config(self):
        """Test when checkpoint state is not valid in config."""
        from orchestrator.validators import validate_state_consistency

        status = {"current_phase": "phase_1", "current_state": "nonsense"}
        checkpoint = {
            "current_phase": "phase_1",
            "current_state": "nonsense",
            "completed_phases": [],
        }
        errors = validate_state_consistency(status, checkpoint, self.CONFIG)
        assert len(errors) >= 1
        assert any("not a valid state in config" in e for e in errors)
