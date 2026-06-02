import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

CLI = Path(__file__).resolve().parent.parent / "runtime" / "cli.py"
FIXTURES = Path(__file__).parent / "fixtures"


PROJECT_ROOT = CLI.parent.parent


def _run_cli(*args: str) -> subprocess.CompletedProcess:
    """Run the CLI as a subprocess and return the result."""
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
        env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)},
    )


def _temp_fixture(data: dict) -> str:
    """Write data to a temp JSON file and return its path."""
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(data, f)
    return path


import os


# --- Help ---

class TestCliHelp:
    def test_top_level_help(self):
        result = _run_cli("--help")
        assert result.returncode == 0
        assert "contextsmith-validator" in result.stdout.lower() or "ContextSmith" in result.stdout

    def test_subcommand_help_requirements(self):
        result = _run_cli("requirements", "--help")
        assert result.returncode == 0

    def test_subcommand_help_phase_contract(self):
        result = _run_cli("phase-contract", "--help")
        assert result.returncode == 0

    def test_subcommand_help_evidence(self):
        result = _run_cli("evidence", "--help")
        assert result.returncode == 0

    def test_subcommand_help_approval(self):
        result = _run_cli("approval", "--help")
        assert result.returncode == 0

    def test_subcommand_help_closeout(self):
        result = _run_cli("closeout", "--help")
        assert result.returncode == 0

    def test_subcommand_help_domain_pack(self):
        result = _run_cli("domain-pack", "--help")
        assert result.returncode == 0


# --- Passing fixtures exit 0 ---

class TestCliPass:
    def test_requirements_pass(self):
        result = _run_cli("requirements", str(FIXTURES / "requirements_chain_valid.json"))
        assert result.returncode == 0
        assert "PASS" in result.stdout

    def test_phase_contract_pass(self):
        result = _run_cli("phase-contract", str(FIXTURES / "phase_contract_valid.json"))
        assert result.returncode == 0
        assert "PASS" in result.stdout

    def test_evidence_pass(self):
        result = _run_cli("evidence", str(FIXTURES / "evidence_ledger_valid.json"))
        assert result.returncode == 0
        assert "PASS" in result.stdout

    def test_approval_pass(self):
        result = _run_cli("approval", str(FIXTURES / "approval_record_valid.json"))
        assert result.returncode == 0
        assert "PASS" in result.stdout

    def test_closeout_pass(self):
        result = _run_cli("closeout", str(FIXTURES / "phase_closeout_valid.json"))
        assert result.returncode == 0
        assert "PASS" in result.stdout

    def test_domain_pack_pass(self):
        result = _run_cli("domain-pack", str(FIXTURES / "domain_pack_valid.json"))
        assert result.returncode == 0
        assert "PASS" in result.stdout


# --- Failing fixtures exit 1 and list violations ---

class TestCliFail:
    def test_requirements_fail(self):
        result = _run_cli("requirements", str(FIXTURES / "requirements_chain_missing_id.json"))
        assert result.returncode == 1
        assert "FAIL" in result.stdout
        assert "violation" in result.stdout.lower()
        assert "Missing required field: id" in result.stdout

    def test_phase_contract_fail(self):
        result = _run_cli("phase-contract", str(FIXTURES / "phase_contract_missing_domain.json"))
        assert result.returncode == 1
        assert "FAIL" in result.stdout
        assert "Missing required field: domain" in result.stdout

    def test_evidence_fail(self):
        result = _run_cli("evidence", str(FIXTURES / "evidence_ledger_missing_requirement_id.json"))
        assert result.returncode == 1
        assert "FAIL" in result.stdout
        assert "Missing required field: requirement_id" in result.stdout

    def test_approval_fail(self):
        result = _run_cli("approval", str(FIXTURES / "approval_record_missing_requirement_ids.json"))
        assert result.returncode == 1
        assert "FAIL" in result.stdout
        assert "Missing required field: requirement_ids" in result.stdout

    def test_closeout_fail(self):
        result = _run_cli("closeout", str(FIXTURES / "phase_closeout_missing_phase_id.json"))
        assert result.returncode == 1
        assert "FAIL" in result.stdout
        assert "Missing required field: phase_id" in result.stdout

    def test_domain_pack_fail(self):
        result = _run_cli("domain-pack", str(FIXTURES / "domain_pack_missing_approval_gates.json"))
        assert result.returncode == 1
        assert "FAIL" in result.stdout
        assert "Missing required field: approval_gates" in result.stdout

    def test_all_subcommands_fail_with_violation_text(self):
        """Every subcommand outputs specific violation text on failure."""
        fail_cases = [
            ("requirements", "requirements_chain_missing_id.json", "Missing required field: id"),
            ("phase-contract", "phase_contract_missing_domain.json", "Missing required field: domain"),
            ("evidence", "evidence_ledger_missing_requirement_id.json", "Missing required field: requirement_id"),
            ("approval", "approval_record_missing_requirement_ids.json", "Missing required field: requirement_ids"),
            ("closeout", "phase_closeout_missing_phase_id.json", "Missing required field: phase_id"),
            ("domain-pack", "domain_pack_missing_approval_gates.json", "Missing required field: approval_gates"),
        ]
        for cmd, fixture, expected in fail_cases:
            result = _run_cli(cmd, str(FIXTURES / fixture))
            assert result.returncode == 1, f"{cmd}: expected exit 1, got {result.returncode}"
            assert expected in result.stdout, f"{cmd}: expected '{expected}' in output"


# --- File errors exit 2 ---

class TestCliErrors:
    def test_nonexistent_file(self):
        result = _run_cli("requirements", "/nonexistent/artifact.json")
        assert result.returncode == 2
        assert "ERROR" in result.stderr

    def test_invalid_json(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as f:
            f.write("{not valid json}")
        result = _run_cli("requirements", path)
        assert result.returncode == 2
        assert "ERROR" in result.stderr

    def test_no_subcommand(self):
        result = _run_cli(str(FIXTURES / "requirements_chain_valid.json"))
        assert result.returncode != 0

    def test_yaml_file_error(self):
        result = _run_cli("requirements", str(FIXTURES / "requirements_chain_invalid.yml"))
        assert result.returncode == 2
        assert "ERROR" in result.stderr


# --- Programmatic API ---

class TestCliMain:
    def test_main_returns_zero_on_pass(self):
        from runtime.cli import main
        code = main(["requirements", str(FIXTURES / "requirements_chain_valid.json")])
        assert code == 0

    def test_main_returns_one_on_fail(self):
        from runtime.cli import main
        code = main(["requirements", str(FIXTURES / "requirements_chain_missing_id.json")])
        assert code == 1

    def test_main_returns_two_on_missing_file(self):
        from runtime.cli import main
        code = main(["requirements", "/nonexistent/artifact.json"])
        assert code == 2


# --- Warnings display ---

class TestCliWarnings:
    def test_warnings_displayed_on_pass(self):
        """Warnings are displayed even when validation passes."""
        import json, tempfile
        data = {
            "artifact_type": "requirements_chain",
            "id": "req-warn",
            "source": "Pending with no phases",
            "domain": "general",
            "side_effect_tier": "read_only",
            "validation_method": "artifact_check",
            "phase_ids": [],
            "evidence_ids": [],
            "status": "pending",
        }
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as f:
            json.dump(data, f)
        result = _run_cli("requirements", path)
        assert result.returncode == 0
        assert "warning" in result.stdout.lower()
