"""OpenCode adapter: subprocess-based agent execution via OpenCode CLI."""

import json
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from orchestrator.adapters.base import (
    HarnessAdapter,
    HarnessExecutionError,
    HarnessRegistry,
    HarnessResult,
    HarnessTimeoutError,
    StepContract,
)

PERMISSION_MAP = {
    "read-only": "contextsmith-auditor",
    "edit": "contextsmith-builder",
    "external-action": "contextsmith-migrator",
}


class OpenCodeAdapter(HarnessAdapter):
    """Adapter that launches agents via the OpenCode CLI subprocess."""

    def __init__(self):
        self._processes: dict[str, subprocess.Popen] = {}

    @property
    def name(self) -> str:
        """Unique adapter identifier."""
        return "opencode"

    def validate_environment(self) -> list[str]:
        """Check that the opencode command is available on PATH."""
        if shutil.which("opencode") is None:
            return ["opencode command not found on PATH"]
        return []

    def execute(self, contract: StepContract, state_dir: Path) -> HarnessResult:
        """Execute one bounded step via OpenCode subprocess.

        Builds the opencode command, launches the subprocess with timeout,
        reads RESULT.json, and collects artifacts.
        """
        state_dir = Path(state_dir)
        cmd = self._build_command(contract)

        try:
            proc = subprocess.Popen(
                cmd,
                cwd=str(state_dir),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=self._build_env(contract),
            )
            self._processes[contract.step_id] = proc

            try:
                stdout, stderr = proc.communicate(timeout=contract.timeout_s)
            except subprocess.TimeoutExpired:
                proc.kill()
                stdout, stderr = proc.communicate()
                raise HarnessTimeoutError(contract.step_id, contract.timeout_s)

            # Create a CompletedProcess-like object for _read_result
            completed = subprocess.CompletedProcess(
                args=cmd,
                returncode=proc.returncode,
                stdout=stdout,
                stderr=stderr,
            )

        except OSError as e:
            raise HarnessExecutionError(
                contract.step_id, f"subprocess launch failed: {e}"
            )
        finally:
            self._processes.pop(contract.step_id, None)

        return self._read_result(completed, contract, state_dir)

    def cancel(self, step_id: str) -> bool:
        """Cancel a running OpenCode subprocess."""
        proc = self._processes.pop(step_id, None)
        if proc is None:
            return False
        try:
            proc.terminate()
            return True
        except OSError:
            return False

    def get_capabilities(self) -> dict:
        """Declare OpenCode adapter capabilities."""
        return {
            "supports_model_pinning": True,
            "supports_step_caps": True,
            "supports_permission_levels": True,
            "max_concurrent_steps": 1,
            "supports_structured_output": True,
            "supports_cancellation": True,
        }

    def _build_command(self, contract: StepContract) -> list[str]:
        """Build the opencode CLI command from the step contract."""
        cmd = ["opencode", "run"]

        if contract.agent_profile:
            cmd.extend(["--agent", contract.agent_profile])
        elif contract.permissions in PERMISSION_MAP:
            cmd.extend(["--agent", PERMISSION_MAP[contract.permissions]])

        if contract.model_pin:
            cmd.extend(["--model", contract.model_pin])

        if contract.prompt_template:
            cmd.extend(["--prompt", contract.prompt_template])
        else:
            prompt_path = Path(contract.task_state_dir) / "NEXT_PROMPT.md"
            if not prompt_path.exists() and contract.task_state_dir:
                prompt_path = Path(contract.task_state_dir) / "NEXT_PROMPT.md"
            if prompt_path.exists():
                cmd.extend(["--file", str(prompt_path)])

        cmd.extend(["--format", "json"])

        return cmd

    def _build_env(self, contract: StepContract) -> Optional[dict]:
        """Build environment variables for the subprocess."""
        return None

    def _read_result(
        self,
        proc: subprocess.CompletedProcess,
        contract: StepContract,
        state_dir: Path,
    ) -> HarnessResult:
        """Read RESULT.json and collect artifacts from state_dir."""
        artifacts = {}
        artifacts_written = []

        for artifact_name in contract.expected_outputs:
            artifact_path = state_dir / artifact_name
            if artifact_path.exists():
                artifacts[artifact_name] = artifact_path.read_text(encoding="utf-8")
                artifacts_written.append(artifact_name)

        result_file = state_dir / "RESULT.json"
        envelope = None
        if result_file.exists():
            try:
                envelope = json.loads(result_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError, OSError:
                pass

        if envelope:
            status = envelope.get("status", "pass")
        elif proc.returncode != 0:
            status = "fail"
        elif len(artifacts_written) == len(contract.expected_outputs):
            status = "pass"
        elif len(artifacts_written) > 0:
            status = "fail"
        else:
            status = "fail"

        reason = ""
        issues = []
        next_action = "done"
        if envelope:
            reason = envelope.get("reason", "")
            issues = envelope.get("issues", [])
            next_action = envelope.get("next_action", "done")
        else:
            n_found = len(artifacts_written)
            n_expected = len(contract.expected_outputs)
            reason = f"{n_found}/{n_expected} artifacts produced"

        return HarnessResult(
            status=status,
            step_id=contract.step_id,
            reason=reason,
            artifacts=artifacts,
            artifacts_written=artifacts_written,
            validation={
                "files_found": len(artifacts_written),
                "expected": len(contract.expected_outputs),
            },
            issues=issues,
            next_action=next_action,
        )


HarnessRegistry.register(OpenCodeAdapter)
