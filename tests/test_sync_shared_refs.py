"""Regression tests for sync_shared_refs.py directory structure preservation.

ISSUE-1: sync_shared_refs.py flattened local:true entries to references/ root,
breaking runtime/ module paths. Fix preserves directory structure for non-skill
local files (e.g., runtime/validator.py -> references/runtime/validator.py).
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "sync_shared_refs.py"


def _run_sync(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Run sync_shared_refs.py with REPO_ROOT overridden via environment."""
    env = {**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parent.parent)}
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else str(Path(__file__).resolve().parent.parent),
        env=env,
    )


class TestDirectoryStructurePreservation:
    """Test that local:true entries preserve directory structure."""

    def test_runtime_files_land_under_references_runtime(self, tmp_path, monkeypatch):
        """runtime/validator.py should sync to references/runtime/validator.py."""
        import yaml

        # Create a minimal skill with a manifest referencing runtime files
        skill_dir = tmp_path / "skills" / "test-skill"
        skill_dir.mkdir(parents=True)

        # Create a fake runtime directory with a file
        runtime_dir = tmp_path / "runtime"
        runtime_dir.mkdir()
        (runtime_dir / "validator.py").write_text("# validator")
        (runtime_dir / "__init__.py").write_text("")

        # Create manifest with local runtime entries
        manifest = {
            "skill": "test-skill",
            "version": "1.0.0",
            "references": [
                {
                    "source": "runtime/validator.py",
                    "version": "local",
                    "required": True,
                    "local": True,
                },
                {
                    "source": "runtime/__init__.py",
                    "version": "local",
                    "required": True,
                    "local": True,
                },
            ],
        }

        (skill_dir / "reference_manifest.yml").write_text(
            yaml.dump(manifest, default_flow_style=False)
        )
        (skill_dir / "SKILL.md").write_text("---\nname: test\n---\nTest skill")

        # Run sync with dry-run, overriding REPO_ROOT
        result = _run_sync(
            "--skill", "test-skill", "--dry-run",
            "--staging-dir", str(tmp_path / ".agent_work" / "staged_skills"),
            "--repo-root", str(tmp_path),
            cwd=tmp_path,
        )

        # Verify runtime files land under references/runtime/
        assert "references/runtime/validator.py" in result.stdout
        assert "references/runtime/__init__.py" in result.stdout

    def test_skill_local_files_remain_flat(self, tmp_path, monkeypatch):
        """skills/<skill>/file.md should sync to references/file.md (flat)."""
        import yaml

        skill_dir = tmp_path / "skills" / "test-skill"
        skill_dir.mkdir(parents=True)

        # Create a local skill file
        (skill_dir / "local-ref.md").write_text("# Local reference")

        # Create manifest with skill-local entry
        manifest = {
            "skill": "test-skill",
            "version": "1.0.0",
            "references": [
                {
                    "source": "skills/test-skill/local-ref.md",
                    "version": "abc123",
                    "required": True,
                    "local": True,
                },
            ],
        }

        (skill_dir / "reference_manifest.yml").write_text(
            yaml.dump(manifest, default_flow_style=False)
        )
        (skill_dir / "SKILL.md").write_text("---\nname: test\n---\nTest skill")

        # Run sync with dry-run
        result = _run_sync(
            "--skill", "test-skill", "--dry-run",
            "--staging-dir", str(tmp_path / ".agent_work" / "staged_skills"),
            "--repo-root", str(tmp_path),
            cwd=tmp_path,
        )

        # Verify skill-local files are flattened to references/file.md
        assert "references/local-ref.md" in result.stdout
        # Should NOT preserve skills/ prefix
        assert "references/skills/" not in result.stdout

    def test_nested_runtime_subdirs_preserved(self, tmp_path, monkeypatch):
        """runtime/domain_packs/file.json should sync to references/runtime/domain_packs/file.json."""
        import yaml

        skill_dir = tmp_path / "skills" / "test-skill"
        skill_dir.mkdir(parents=True)

        # Create nested runtime directory
        domain_packs_dir = tmp_path / "runtime" / "domain_packs"
        domain_packs_dir.mkdir(parents=True)
        (domain_packs_dir / "general_fallback.json").write_text("{}")
        (tmp_path / "runtime" / "__init__.py").write_text("")

        # Create manifest with nested runtime entry
        manifest = {
            "skill": "test-skill",
            "version": "1.0.0",
            "references": [
                {
                    "source": "runtime/domain_packs/general_fallback.json",
                    "version": "local",
                    "required": True,
                    "local": True,
                },
            ],
        }

        (skill_dir / "reference_manifest.yml").write_text(
            yaml.dump(manifest, default_flow_style=False)
        )
        (skill_dir / "SKILL.md").write_text("---\nname: test\n---\nTest skill")

        # Run sync with dry-run
        result = _run_sync(
            "--skill", "test-skill", "--dry-run",
            "--staging-dir", str(tmp_path / ".agent_work" / "staged_skills"),
            "--repo-root", str(tmp_path),
            cwd=tmp_path,
        )

        # Verify nested structure is preserved
        assert "references/runtime/domain_packs/general_fallback.json" in result.stdout
