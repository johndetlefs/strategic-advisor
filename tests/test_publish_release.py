from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PUBLISH_RELEASE = REPOSITORY_ROOT / "scripts" / "publish_release.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PublishReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary_directory.name).resolve()
        self.root = self.base / "repository"
        shutil.copytree(
            REPOSITORY_ROOT,
            self.root,
            symlinks=True,
            ignore=shutil.ignore_patterns(
                ".git",
                ".project-workflow",
                "__pycache__",
                "tests",
            ),
        )
        self.module = load_module(
            f"publish_release_fixture_{id(self)}", PUBLISH_RELEASE
        )
        authority, _ = self.module.release_state.load_authority(self.root)
        authority["state"] = "prepared"
        authority["distribution"]["version"] = "0.2.0-alpha.4"
        changes = {
            self.root / "distribution.json": (
                self.module.release_state.rendered_json_bytes(authority)
            ),
            **self.module.release_state.synchronized_documents(
                self.root, authority
            ),
        }
        for path, content in changes.items():
            path.write_bytes(content)
        for command in (
            ["git", "init", str(self.root)],
            ["git", "-C", str(self.root), "config", "user.name", "Fixture"],
            [
                "git",
                "-C",
                str(self.root),
                "config",
                "user.email",
                "fixture@example.invalid",
            ],
            ["git", "-C", str(self.root), "add", "."],
            [
                "git",
                "-C",
                str(self.root),
                "-c",
                "commit.gpgsign=false",
                "commit",
                "-m",
                "fixture",
            ],
        ):
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=20,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.revision = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.build = self.base / "build"
        self.download = self.base / "download"
        self.build.mkdir()
        result = subprocess.run(
            [
                sys.executable,
                str(self.root / "scripts" / "build_install_artifacts.py"),
                "build",
                "--source-root",
                str(self.root),
                "--skill-archive",
                str(self.build / "strategic-advisor.zip"),
                "--plugin-archive",
                str(self.build / "strategic-advisor-plugin.zip"),
                "--chatgpt-kit",
                str(self.build / "strategic-advisor-chatgpt.zip"),
                "--provenance-out",
                str(self.build / "install-artifacts.json"),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        shutil.copytree(self.build, self.download)
        authority, _ = self.module.release_state.load_authority(self.root)
        self.version = authority["distribution"]["version"]
        self.metadata = {
            "assets": [
                {
                    "digest": f"sha256:{sha256(self.build / name)}",
                    "name": name,
                    "size": (self.build / name).stat().st_size,
                }
                for name in self.module.ASSET_NAMES
            ],
            "isPrerelease": True,
            "publishedAt": "2026-07-28T00:00:00Z",
            "tagName": f"v{self.version}",
            "targetCommitish": self.revision,
            "url": (
                "https://github.com/johndetlefs/strategic-advisor/releases/tag/"
                f"v{self.version}"
            ),
        }
        self.metadata_path = self.base / "metadata.json"
        self.metadata_path.write_text(
            json.dumps(self.metadata) + "\n", encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def directory_hashes(self, directory: Path) -> dict[str, str]:
        return {
            path.name: sha256(path)
            for path in sorted(directory.iterdir())
            if path.is_file()
        }

    def test_exact_public_release_verifies_without_mutating_assets(self) -> None:
        before_build = self.directory_hashes(self.build)
        before_download = self.directory_hashes(self.download)
        first = self.module.verify_public(
            self.root,
            self.metadata_path,
            self.download,
            self.build,
            self.revision,
            self.base / "evidence-a.json",
        )
        second = self.module.verify_public(
            self.root,
            self.metadata_path,
            self.download,
            self.build,
            self.revision,
            self.base / "evidence-b.json",
        )
        self.assertEqual(first, second)
        self.assertEqual(self.directory_hashes(self.build), before_build)
        self.assertEqual(self.directory_hashes(self.download), before_download)
        self.assertTrue(
            first["proof_boundary"]["package_and_release_alignment_proven"]
        )
        finalized = self.module.release_state.finalize(
            self.root, self.base / "evidence-a.json"
        )
        self.assertEqual(finalized["state"], "published")
        self.assertEqual(
            finalized["current_public"]["version"], self.version
        )
        self.assertTrue(
            (
                self.root
                / "evidence"
                / "releases"
                / f"v{self.version}.json"
            ).is_file()
        )
        self.assertIn(
            f"`v{self.version}` GitHub prerelease",
            (self.root / "README.md").read_text(encoding="utf-8"),
        )

    def test_existing_release_mismatch_fails_without_mutation(self) -> None:
        before_build = self.directory_hashes(self.build)
        before_download = self.directory_hashes(self.download)
        mismatched = json.loads(json.dumps(self.metadata))
        mismatched["assets"][0]["digest"] = f"sha256:{'0' * 64}"
        mismatch_path = self.base / "mismatch.json"
        mismatch_path.write_text(
            json.dumps(mismatched) + "\n", encoding="utf-8"
        )
        evidence = self.base / "mismatch-evidence.json"
        with self.assertRaisesRegex(
            self.module.ReleaseVerificationError,
            "metadata, fresh downloads, and local clean build differ",
        ):
            self.module.verify_public(
                self.root,
                mismatch_path,
                self.download,
                self.build,
                self.revision,
                evidence,
            )
        self.assertFalse(evidence.exists())
        self.assertEqual(self.directory_hashes(self.build), before_build)
        self.assertEqual(self.directory_hashes(self.download), before_download)

    def test_release_workflow_is_pinned_and_publish_once(self) -> None:
        workflow = (
            REPOSITORY_ROOT / ".github" / "workflows" / "release.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: write\n", workflow)
        self.assertNotIn("pull-requests: write", workflow)
        self.assertIn(
            "actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683",
            workflow,
        )
        self.assertIn(
            "actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065",
            workflow,
        )
        self.assertIn(
            "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02",
            workflow,
        )
        self.assertEqual(workflow.count("gh release create"), 1)
        self.assertIn(
            "steps.existing.outputs.exists == 'false'",
            workflow,
        )
        self.assertNotIn("gh release upload", workflow)
        self.assertNotIn("--clobber", workflow)
        self.assertIn("cancel-in-progress: false", workflow)


if __name__ == "__main__":
    unittest.main()
