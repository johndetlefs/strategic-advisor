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
        authority["schema_version"] = 2
        authority["superseded"] = []
        authority["state"] = "published"
        authority["distribution"] = {
            "runtime_package_identity_sha256": self.module.runtime_identity(
                self.root
            ),
            "version": "0.2.0-alpha.4",
        }
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
        self.initial_revision = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=20,
        ).stdout.strip()

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

    def git_commit(self, message: str) -> str:
        add = subprocess.run(
            ["git", "-C", str(self.root), "add", "."],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(add.returncode, 0, add.stdout + add.stderr)
        command = [
            "git",
            "-C",
            str(self.root),
            "-c",
            "commit.gpgsign=false",
            "commit",
        ]
        command.extend(["-m", message])
        commit = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(commit.returncode, 0, commit.stdout + commit.stderr)
        return subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=20,
        ).stdout.strip()

    def prepare_committed_candidate(self) -> str:
        self.module.prepare(self.root, "0.2.0-alpha.5")
        return self.git_commit("prepare alpha.5")

    def test_prepare_advances_and_synchronizes_release_state(self) -> None:
        authority = self.module.prepare(self.root, "0.2.0-alpha.5")
        self.assertEqual(authority["state"], "prepared")
        self.assertEqual(authority["distribution"]["version"], "0.2.0-alpha.5")
        self.assertEqual(
            authority["distribution"]["runtime_package_identity_sha256"],
            self.module.runtime_identity(self.root),
        )
        self.assertEqual(self.module.validate(self.root), authority)
        self.assertIn(
            "`v0.2.0-alpha.5` is release intent only",
            (self.root / "README.md").read_text(encoding="utf-8"),
        )

    def test_invalid_nonadvancing_and_reused_versions_do_not_write(self) -> None:
        before = self.tracked_hashes()
        for version in ("not-semver", "0.2.0-alpha.4", "0.1.9-rc.9"):
            with self.subTest(version=version):
                with self.assertRaises(self.module.ReleaseStateError):
                    self.module.prepare(self.root, version)
                self.assertEqual(self.tracked_hashes(), before)

        reused = self.root / "evidence" / "releases" / "v0.2.0-alpha.5.json"
        reused.write_text("{}\n", encoding="utf-8")
        with self.assertRaisesRegex(
            self.module.ReleaseStateError, "already used"
        ):
            self.module.prepare(self.root, "0.2.0-alpha.5")
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
                self.module.prepare(self.root, "0.2.0-alpha.5")
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

    def test_supersede_records_exact_candidate_and_prepares_replacement(self) -> None:
        prepared_revision = self.prepare_committed_candidate()
        prepared, _ = self.module.load_authority(self.root)
        prepared_identity = prepared["distribution"][
            "runtime_package_identity_sha256"
        ]
        skill = self.root / "skills" / "strategic-advisor" / "SKILL.md"
        skill.write_text(
            skill.read_text(encoding="utf-8") + "\nCorrected runtime.\n",
            encoding="utf-8",
        )

        authority = self.module.supersede(
            self.root,
            next_version="0.2.0-alpha.6",
            prepared_source_revision=prepared_revision,
            reason="Corrected before publication.",
            superseded_at="2026-08-24T01:02:03Z",
        )

        self.assertEqual(authority["schema_version"], 2)
        self.assertEqual(authority["state"], "prepared")
        self.assertEqual(authority["distribution"]["version"], "0.2.0-alpha.6")
        self.assertEqual(
            authority["distribution"]["runtime_package_identity_sha256"],
            self.module.runtime_identity(self.root),
        )
        self.assertEqual(
            authority["superseded"],
            [
                {
                    "reason": "Corrected before publication.",
                    "replacement_version": "0.2.0-alpha.6",
                    "runtime_package_identity_sha256": prepared_identity,
                    "source_revision": prepared_revision,
                    "superseded_at": "2026-08-24T01:02:03Z",
                    "version": "0.2.0-alpha.5",
                }
            ],
        )
        self.assertEqual(self.module.validate(self.root), authority)
        self.assertIn(
            "`v0.2.0-alpha.6` is release intent only",
            (self.root / "README.md").read_text(encoding="utf-8"),
        )
        evidence = self.root / "alpha.6-evidence.json"
        evidence.write_bytes(
            self.module.rendered_json_bytes(
                {
                    "schema_version": 1,
                    "release": {
                        "runtime_package_identity_sha256": authority[
                            "distribution"
                        ]["runtime_package_identity_sha256"],
                        "source_revision": "3" * 40,
                        "status": "prerelease",
                        "tag": "v0.2.0-alpha.6",
                        "version": "0.2.0-alpha.6",
                    },
                    "proof_boundary": {
                        "clean_public_download_proven": True,
                        "package_and_release_alignment_proven": True,
                    },
                }
            )
        )
        finalized = self.module.finalize(self.root, evidence)
        self.assertEqual(finalized["state"], "published")
        self.assertEqual(finalized["superseded"], authority["superseded"])
        with self.assertRaisesRegex(
            self.module.ReleaseStateError, "superseded prepared candidate"
        ):
            self.module.ensure_version_unused(
                self.root, "0.2.0-alpha.5", authority
            )

    def test_supersede_rejects_unproven_published_or_invalid_transition(self) -> None:
        with self.assertRaisesRegex(
            self.module.ReleaseStateError, "only a prepared distribution"
        ):
            self.module.supersede(
                self.root,
                next_version="0.2.0-alpha.5",
                prepared_source_revision=self.initial_revision,
                reason="Not applicable.",
                superseded_at="2026-08-24T01:02:03Z",
            )

        prepared_revision = self.prepare_committed_candidate()
        before = self.tracked_hashes()
        invalid_cases = (
            {
                "next_version": "0.2.0-alpha.5",
                "prepared_source_revision": prepared_revision,
                "reason": "No advance.",
                "superseded_at": "2026-08-24T01:02:03Z",
            },
            {
                "next_version": "0.2.0-alpha.6",
                "prepared_source_revision": self.initial_revision,
                "reason": "Wrong source.",
                "superseded_at": "2026-08-24T01:02:03Z",
            },
            {
                "next_version": "0.2.0-alpha.6",
                "prepared_source_revision": prepared_revision,
                "reason": "   ",
                "superseded_at": "2026-08-24T01:02:03Z",
            },
            {
                "next_version": "0.2.0-alpha.6",
                "prepared_source_revision": prepared_revision,
                "reason": "Invalid timestamp.",
                "superseded_at": "yesterday",
            },
            {
                "next_version": "0.2.0-alpha.6",
                "prepared_source_revision": prepared_revision,
                "reason": "Invalid calendar timestamp.",
                "superseded_at": "2026-02-31T01:02:03Z",
            },
        )
        for arguments in invalid_cases:
            with self.subTest(arguments=arguments):
                with self.assertRaises(self.module.ReleaseStateError):
                    self.module.supersede(self.root, **arguments)
                self.assertEqual(self.tracked_hashes(), before)

    def test_supersede_rejects_tagged_prepared_candidate(self) -> None:
        prepared_revision = self.prepare_committed_candidate()
        subprocess.run(
            ["git", "-C", str(self.root), "tag", "v0.2.0-alpha.5"],
            check=True,
            capture_output=True,
            text=True,
            timeout=20,
        )
        before = self.tracked_hashes()
        with self.assertRaisesRegex(
            self.module.ReleaseStateError, "already has local tag"
        ):
            self.module.supersede(
                self.root,
                next_version="0.2.0-alpha.6",
                prepared_source_revision=prepared_revision,
                reason="Must not supersede a tagged candidate.",
                superseded_at="2026-08-24T01:02:03Z",
            )
        self.assertEqual(self.tracked_hashes(), before)

    def test_superseded_history_must_match_committed_prepared_intent(self) -> None:
        prepared_revision = self.prepare_committed_candidate()
        authority = self.module.supersede(
            self.root,
            next_version="0.2.0-alpha.6",
            prepared_source_revision=prepared_revision,
            reason="Corrected before publication.",
            superseded_at="2026-08-24T01:02:03Z",
        )
        authority["superseded"][0]["source_revision"] = self.initial_revision
        (self.root / "distribution.json").write_bytes(
            self.module.rendered_json_bytes(authority)
        )
        with self.assertRaisesRegex(
            self.module.ReleaseStateError,
            "superseded history source does not contain its exact prepared intent",
        ):
            self.module.validate(
                self.root, verify_superseded_provenance=True
            )

    def test_supersede_transaction_rolls_back_if_replace_fails(self) -> None:
        prepared_revision = self.prepare_committed_candidate()
        before = self.tracked_hashes()
        real_replace = self.module.os.replace
        calls = 0

        def fail_second(source, destination):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("synthetic supersede replace failure")
            return real_replace(source, destination)

        with mock.patch.object(self.module.os, "replace", side_effect=fail_second):
            with self.assertRaisesRegex(
                OSError, "synthetic supersede replace failure"
            ):
                self.module.supersede(
                    self.root,
                    next_version="0.2.0-alpha.6",
                    prepared_source_revision=prepared_revision,
                    reason="Corrected before publication.",
                    superseded_at="2026-08-24T01:02:03Z",
                )
        self.assertEqual(self.tracked_hashes(), before)


if __name__ == "__main__":
    unittest.main()
