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
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RELEASE_STATE = REPOSITORY_ROOT / "scripts" / "release_state.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class ReleaseStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name) / "repository"
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
            f"release_state_fixture_{id(self)}", RELEASE_STATE
        )
        authority, _ = self.module.load_authority(self.root)
        authority["state"] = "published"
        authority["current_public"] = {
            "evidence": (
                "evidence/releases/"
                f"v{authority['distribution']['version']}.json"
            ),
            "runtime_package_identity_sha256": authority["distribution"][
                "runtime_package_identity_sha256"
            ],
            "source_revision": "2" * 40,
            "tag": f"v{authority['distribution']['version']}",
            "version": authority["distribution"]["version"],
        }
        changes = {
            self.root / "distribution.json": self.module.rendered_json_bytes(
                authority
            ),
            **self.module.synchronized_documents(self.root, authority),
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

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def tracked_hashes(self) -> dict[str, str]:
        paths = (
            "distribution.json",
            "README.md",
            "INSTALL.md",
            "PRODUCT-CONTRACT.md",
        )
        return {
            path: hashlib.sha256((self.root / path).read_bytes()).hexdigest()
            for path in paths
        }

    def test_prepare_advances_and_synchronizes_release_state(self) -> None:
        authority = self.module.prepare(self.root, "0.2.0-alpha.4")
        self.assertEqual(authority["state"], "prepared")
        self.assertEqual(authority["distribution"]["version"], "0.2.0-alpha.4")
        self.assertEqual(
            authority["distribution"]["runtime_package_identity_sha256"],
            self.module.runtime_identity(self.root),
        )
        self.assertEqual(self.module.validate(self.root), authority)
        self.assertIn(
            "`v0.2.0-alpha.4` is release intent only",
            (self.root / "README.md").read_text(encoding="utf-8"),
        )

    def test_invalid_nonadvancing_and_reused_versions_do_not_write(self) -> None:
        before = self.tracked_hashes()
        for version in ("not-semver", "0.2.0-alpha.3", "0.1.9-rc.9"):
            with self.subTest(version=version):
                with self.assertRaises(self.module.ReleaseStateError):
                    self.module.prepare(self.root, version)
                self.assertEqual(self.tracked_hashes(), before)

        reused = self.root / "evidence" / "releases" / "v0.2.0-alpha.4.json"
        reused.write_text("{}\n", encoding="utf-8")
        with self.assertRaisesRegex(
            self.module.ReleaseStateError, "already used"
        ):
            self.module.prepare(self.root, "0.2.0-alpha.4")
        self.assertEqual(self.tracked_hashes(), before)

    def test_transaction_rolls_back_if_replace_fails(self) -> None:
        before = self.tracked_hashes()
        real_replace = self.module.os.replace
        calls = 0

        def fail_second(source, destination):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("synthetic replace failure")
            return real_replace(source, destination)

        with mock.patch.object(self.module.os, "replace", side_effect=fail_second):
            with self.assertRaisesRegex(OSError, "synthetic replace failure"):
                self.module.prepare(self.root, "0.2.0-alpha.4")
        self.assertEqual(self.tracked_hashes(), before)

    def test_runtime_drift_fails_but_documentation_drift_does_not(self) -> None:
        self.module.validate(self.root)
        contributing = self.root / "CONTRIBUTING.md"
        contributing.write_text(
            contributing.read_text(encoding="utf-8") + "\nDocumentation note.\n",
            encoding="utf-8",
        )
        self.module.validate(self.root)
        skill = self.root / "skills" / "strategic-advisor" / "SKILL.md"
        skill.write_text(
            skill.read_text(encoding="utf-8") + "\nRuntime drift.\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            self.module.ReleaseStateError, "runtime bytes do not match"
        ):
            self.module.validate(self.root)


if __name__ == "__main__":
    unittest.main()
