"""Generic adapter: file-based fallback with no external agent runtime."""

import json
from pathlib import Path

from orchestrator.adapters.base import (
    HarnessAdapter,
    HarnessRegistry,
    HarnessResult,
    StepContract,
)


class GenericAdapter(HarnessAdapter):
    """File-based adapter that works without any external agent runtime.

    Writes the pending prompt to disk and checks for RESULT.json.
    Supports test-mode (fixture injection) and await-human mode.
    """

    @property
    def name(self) -> str:
        """Unique adapter identifier."""
        return "generic"

    def validate_environment(self) -> list[str]:
        """Generic adapter is always available."""
        return []

    def execute(self, contract: StepContract, state_dir: Path) -> HarnessResult:
        """Execute one bounded step using file-based protocol.

        Writes .pending_prompt.md, then checks for RESULT.json or existing
        artifacts. In test mode, loads fixture responses. In poll_human mode,
        checks for .human_response.md (polling, not blocking).
        """
        state_dir = Path(state_dir)
        prompt_path = state_dir / ".pending_prompt.md"
        prompt_path.write_text(self._load_prompt(contract), encoding="utf-8")

        if contract.extra.get("test_mode"):
            return self._run_test_mode(contract, state_dir)
        if contract.extra.get("poll_human"):
            return self._poll_human(contract, state_dir)

        result_file = state_dir / "RESULT.json"
        envelope = None
        if result_file.exists():
            try:
                envelope = json.loads(result_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass

        artifacts = self._collect_existing(contract, state_dir)

        if envelope:
            status = envelope.get("status", "pass")
            reason = envelope.get("reason", "")
            issues = envelope.get("issues", [])
            next_action = envelope.get("next_action", "done")
        else:
            status = (
                "pass" if len(artifacts) == len(contract.expected_outputs) else "fail"
            )
            reason = "generic adapter: no agent runtime, checked existing artifacts"
            issues = (
                [] if artifacts else ["no agent runtime available, no artifacts found"]
            )
            next_action = "done"

        return HarnessResult(
            status=status,
            step_id=contract.step_id,
            reason=reason,
            artifacts={},
            artifacts_written=list(artifacts.keys()),
            validation={
                "files_found": len(artifacts),
                "expected": len(contract.expected_outputs),
            },
            issues=issues,
            next_action=next_action,
        )

    def cancel(self, step_id: str) -> bool:
        """Generic adapter has no running process to cancel."""
        return False

    def get_capabilities(self) -> dict:
        """Declare generic adapter capabilities."""
        return {
            "supports_model_pinning": False,
            "supports_step_caps": False,
            "supports_permission_levels": False,
            "max_concurrent_steps": 1,
            "supports_structured_output": True,
            "supports_cancellation": False,
        }

    def _load_prompt(self, contract: StepContract) -> str:
        """Load prompt text from contract or NEXT_PROMPT.md."""
        if contract.prompt_template:
            return contract.prompt_template
        prompt_path = Path(contract.task_state_dir) / "NEXT_PROMPT.md"
        if prompt_path.exists():
            return prompt_path.read_text(encoding="utf-8")
        return f"# Step: {contract.step_id}\n\nExecute the current phase."

    def _collect_existing(
        self, contract: StepContract, state_dir: Path
    ) -> dict[str, str]:
        """Collect existing artifacts from state_dir."""
        artifacts = {}
        for artifact_name in contract.expected_outputs:
            artifact_path = state_dir / artifact_name
            if artifact_path.exists():
                artifacts[artifact_name] = artifact_path.read_text(encoding="utf-8")
        return artifacts

    def _load_test_fixture(self, contract: StepContract) -> dict | None:
        """Load fixture JSON from the path specified in contract extras."""
        fixture_path = contract.extra.get("fixture")
        if not fixture_path:
            return None
        fixture_file = Path(fixture_path)
        if not fixture_file.exists():
            return None
        try:
            return json.loads(fixture_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None

    def _write_fixture_artifacts(self, fixture: dict, state_dir: Path) -> list[str]:
        """Write fixture-specified artifacts to disk, return written names."""
        artifacts_written = []
        artifacts_to_write = fixture.get("artifacts_content", {})
        for artifact_name in fixture.get("artifacts", []):
            if artifact_name in artifacts_to_write:
                artifact_path = state_dir / artifact_name
                artifact_path.write_text(
                    artifacts_to_write[artifact_name], encoding="utf-8"
                )
                artifacts_written.append(artifact_name)
            elif (state_dir / artifact_name).exists():
                artifacts_written.append(artifact_name)
        return artifacts_written

    def _run_test_mode(self, contract: StepContract, state_dir: Path) -> HarnessResult:
        """Run in test mode using fixture data."""
        fixture = self._load_test_fixture(contract)
        if fixture is not None:
            artifacts_written = self._write_fixture_artifacts(fixture, state_dir)
            return HarnessResult(
                status=fixture.get("status", "pass"),
                step_id=contract.step_id,
                reason=fixture.get("reason", "test mode fixture"),
                artifacts={},
                artifacts_written=artifacts_written,
                validation=fixture.get("validation", {"passed": True}),
                issues=fixture.get("issues", []),
                next_action=fixture.get("next_action", "done"),
            )

        return HarnessResult(
            status="pass",
            step_id=contract.step_id,
            reason="test mode: no fixture provided",
            artifacts={},
            artifacts_written=[],
            validation={"passed": True, "test_mode": True},
            issues=[],
            next_action="done",
        )

    def _poll_human(self, contract: StepContract, state_dir: Path) -> HarnessResult:
        """Poll for human response (non-blocking).

        Checks if .human_response.md exists. If yes, returns the content.
        If no, returns blocked status. This is polling, not blocking.
        The orchestrator should call this repeatedly or implement a wait loop.
        """
        human_path = state_dir / ".human_response.md"
        if human_path.exists():
            content = human_path.read_text(encoding="utf-8")
            return HarnessResult(
                status="pass",
                step_id=contract.step_id,
                reason="human response received",
                artifacts={"human_response": content},
                artifacts_written=[".human_response.md"],
                validation={"passed": True, "human_mode": True},
                issues=[],
                next_action="done",
            )

        return HarnessResult(
            status="blocked",
            step_id=contract.step_id,
            reason="awaiting human response: write .human_response.md",
            artifacts={},
            artifacts_written=[],
            validation={"passed": False, "awaiting_human": True},
            issues=["no .human_response.md found"],
            next_action="fix",
        )


HarnessRegistry.register(GenericAdapter)
