from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BUILDER = REPOSITORY_ROOT / "scripts" / "build_runtime_package.py"


def load_builder_module():
    spec = importlib.util.spec_from_file_location("runtime_package_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load runtime package builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


class RuntimePackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary_directory.name)
        self.source_root = self.base / "source"
        self.skill_root = self.source_root / "skills" / "strategic-advisor"
        (self.skill_root / "agents").mkdir(parents=True)
        (self.skill_root / "references").mkdir()
        (self.skill_root / "evals").mkdir()
        (self.skill_root / "SKILL.md").write_text(
            "---\nname: strategic-advisor\ndescription: fixture\n---\n# Fixture\n",
            encoding="utf-8",
        )
        (self.skill_root / "agents" / "openai.yaml").write_text(
            "interface:\n  display_name: Fixture\n", encoding="utf-8"
        )
        (self.skill_root / "references" / "one.md").write_text(
            "# One\n\nRuntime reference.\n", encoding="utf-8"
        )
        (self.skill_root / "evals" / "cases.json").write_text(
            '{"schema_version": 1, "cases": []}\n', encoding="utf-8"
        )
        self.allowlist_path = self.skill_root / "runtime-manifest.json"
        self.write_allowlist(
            ["references/one.md", "SKILL.md", "agents/openai.yaml"]
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write_allowlist(self, includes: list[str]) -> None:
        self.allowlist_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "package_root": "skills/strategic-advisor",
                    "include": includes,
                    "excluded_roots": ["evals", "evaluation-results"],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def locations(self, label: str) -> tuple[Path, Path]:
        package_dir = self.base / f"package-{label}"
        manifest_out = (
            self.source_root
            / "evidence"
            / "evaluations"
            / label
            / "runtime-package-manifest.json"
        )
        return package_dir, manifest_out

    def run_builder(
        self, label: str
    ) -> tuple[subprocess.CompletedProcess[str], Path, Path]:
        package_dir, manifest_out = self.locations(label)
        result = subprocess.run(
            [
                sys.executable,
                str(BUILDER),
                "--source-root",
                str(self.source_root),
                "--package-dir",
                str(package_dir),
                "--manifest-out",
                str(manifest_out),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        return result, package_dir, manifest_out

    def assert_rejected(self, result: subprocess.CompletedProcess[str], phrase: str) -> None:
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ERROR [RUNTIME_PACKAGE]", result.stderr)
        self.assertIn(phrase, result.stderr.lower())

    def test_builds_exact_allowlist_with_content_hashes_and_aggregate_identity(self) -> None:
        result, package_dir, manifest_out = self.run_builder("iteration-a")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        packaged_files = sorted(
            path.relative_to(package_dir).as_posix()
            for path in package_dir.rglob("*")
            if path.is_file()
        )
        self.assertEqual(
            packaged_files,
            ["SKILL.md", "agents/openai.yaml", "references/one.md"],
        )
        self.assertFalse((package_dir / "evals").exists())

        manifest_bytes = manifest_out.read_bytes()
        manifest = json.loads(manifest_bytes)
        summary = json.loads(result.stdout)
        self.assertEqual(manifest["file_count"], 3)
        self.assertEqual(
            [item["path"] for item in manifest["files"]], packaged_files
        )
        for item in manifest["files"]:
            content = (package_dir / item["path"]).read_bytes()
            self.assertEqual(item["sha256"], sha256_bytes(content))
            self.assertEqual(item["size_bytes"], len(content))

        identity_payload = {
            "files": manifest["files"],
            "schema_version": 1,
            "source_allowlist_sha256": manifest["source_allowlist"]["sha256"],
        }
        expected_identity = sha256_bytes(canonical_json_bytes(identity_payload))
        self.assertEqual(manifest["package_identity_sha256"], expected_identity)
        self.assertEqual(summary["package_identity_sha256"], expected_identity)
        self.assertEqual(summary["package_manifest_sha256"], sha256_bytes(manifest_bytes))

    def test_identical_sources_produce_identical_manifest_and_package_identity(self) -> None:
        first, first_package, first_manifest = self.run_builder("iteration-a")
        second, second_package, second_manifest = self.run_builder("iteration-b")
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertEqual(first_manifest.read_bytes(), second_manifest.read_bytes())
        self.assertEqual(
            json.loads(first.stdout)["package_identity_sha256"],
            json.loads(second.stdout)["package_identity_sha256"],
        )
        for relative in ("SKILL.md", "agents/openai.yaml", "references/one.md"):
            self.assertEqual(
                (first_package / relative).read_bytes(),
                (second_package / relative).read_bytes(),
            )

    def test_current_repository_allowlist_builds_without_evaluation_files(self) -> None:
        current_source = self.base / "current-source"
        current_skill = current_source / "skills" / "strategic-advisor"
        current_skill.parent.mkdir(parents=True)
        shutil.copytree(
            REPOSITORY_ROOT / "skills" / "strategic-advisor", current_skill
        )
        package_dir = self.base / "current-package"
        manifest_out = (
            current_source
            / "evidence"
            / "evaluations"
            / "current"
            / "runtime-package-manifest.json"
        )
        result = subprocess.run(
            [
                sys.executable,
                str(BUILDER),
                "--source-root",
                str(current_source),
                "--package-dir",
                str(package_dir),
                "--manifest-out",
                str(manifest_out),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        source_allowlist = json.loads(
            (current_skill / "runtime-manifest.json").read_text(encoding="utf-8")
        )
        packaged_files = sorted(
            path.relative_to(package_dir).as_posix()
            for path in package_dir.rglob("*")
            if path.is_file()
        )
        self.assertEqual(packaged_files, sorted(source_allowlist["include"]))
        self.assertFalse(
            any(
                part.lower().startswith("eval")
                for item in packaged_files
                for part in Path(item).parts
            )
        )

    def test_rejects_path_traversal_before_writing_destination(self) -> None:
        self.write_allowlist(["SKILL.md", "../evals/cases.json"])
        result, package_dir, manifest_out = self.run_builder("traversal")
        self.assert_rejected(result, "path traversal")
        self.assertFalse(package_dir.exists())
        self.assertFalse(manifest_out.exists())

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks are unavailable")
    def test_rejects_allowlisted_file_symlink(self) -> None:
        outside = self.base / "outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        link = self.skill_root / "references" / "linked.md"
        link.symlink_to(outside)
        self.write_allowlist(["SKILL.md", "references/linked.md"])
        result, package_dir, manifest_out = self.run_builder("file-symlink")
        self.assert_rejected(result, "symlink")
        self.assertFalse(package_dir.exists())
        self.assertFalse(manifest_out.exists())

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks are unavailable")
    def test_rejects_symlinked_parent_directory(self) -> None:
        outside_directory = self.base / "outside-directory"
        outside_directory.mkdir()
        (outside_directory / "nested.md").write_text("outside\n", encoding="utf-8")
        link = self.skill_root / "linked-references"
        link.symlink_to(outside_directory, target_is_directory=True)
        self.write_allowlist(["SKILL.md", "linked-references/nested.md"])
        result, package_dir, manifest_out = self.run_builder("parent-symlink")
        self.assert_rejected(result, "symlink")
        self.assertFalse(package_dir.exists())
        self.assertFalse(manifest_out.exists())

    def test_rejects_evaluation_material_in_allowlist(self) -> None:
        self.write_allowlist(["SKILL.md", "evals/cases.json"])
        result, package_dir, manifest_out = self.run_builder("eval-leak")
        self.assert_rejected(result, "evaluation or result material")
        self.assertFalse(package_dir.exists())
        self.assertFalse(manifest_out.exists())

    def test_rejects_evaluation_material_in_revealing_filename(self) -> None:
        disguised = self.skill_root / "references" / "evaluation-notes.md"
        disguised.write_text("expected answers\n", encoding="utf-8")
        self.write_allowlist(["SKILL.md", "references/evaluation-notes.md"])
        result, package_dir, manifest_out = self.run_builder("disguised-eval")
        self.assert_rejected(result, "evaluation or result material")
        self.assertFalse(package_dir.exists())
        self.assertFalse(manifest_out.exists())

    def test_rejects_case_prompt_hidden_in_innocuous_reference(self) -> None:
        prompt = (
            "A fictional executive requests a complete rollout even though the only direct "
            "outcome evidence shows that most users cannot complete the core task."
        )
        (self.skill_root / "evals" / "cases.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "cases": [{"id": "CASE-001", "prompt": prompt}],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        disguised = self.skill_root / "references" / "meeting-guide.md"
        disguised.write_text(f"# Meeting guide\n\n{prompt}\n", encoding="utf-8")
        self.write_allowlist(["SKILL.md", "references/meeting-guide.md"])
        result, package_dir, manifest_out = self.run_builder("content-eval-leak")
        self.assert_rejected(result, "evaluation case or answer fingerprint")
        self.assertFalse(package_dir.exists())
        self.assertFalse(manifest_out.exists())

    def test_rejects_rubric_bytes_hidden_in_innocuous_reference(self) -> None:
        aggregation = (
            "# Aggregation authority\n\n"
            "This exact synthetic authority paragraph defines a private scoring contract that "
            "must never be copied into the model-visible runtime treatment package, regardless "
            "of the destination filename chosen by a contributor.\n"
        )
        (self.skill_root / "evals" / "AGGREGATION.md").write_text(
            aggregation, encoding="utf-8"
        )
        disguised = self.skill_root / "references" / "meeting-guide.md"
        disguised.write_text(aggregation, encoding="utf-8")
        self.write_allowlist(["SKILL.md", "references/meeting-guide.md"])
        result, package_dir, manifest_out = self.run_builder("authority-byte-leak")
        self.assert_rejected(result, "evaluation case or answer fingerprint")
        self.assertFalse(package_dir.exists())
        self.assertFalse(manifest_out.exists())

    def test_rejects_manifest_inside_model_visible_package(self) -> None:
        package_dir = self.base / "package-inside"
        manifest_out = package_dir / "runtime-package-manifest.json"
        result = subprocess.run(
            [
                sys.executable,
                str(BUILDER),
                "--source-root",
                str(self.source_root),
                "--package-dir",
                str(package_dir),
                "--manifest-out",
                str(manifest_out),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assert_rejected(result, "inside the source repository")
        self.assertFalse(package_dir.exists())

    def test_refuses_to_overwrite_existing_package(self) -> None:
        package_dir, manifest_out = self.locations("existing")
        package_dir.mkdir()
        result = subprocess.run(
            [
                sys.executable,
                str(BUILDER),
                "--source-root",
                str(self.source_root),
                "--package-dir",
                str(package_dir),
                "--manifest-out",
                str(manifest_out),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assert_rejected(result, "already exists")

    def test_manifest_commit_failure_rolls_back_new_package(self) -> None:
        builder = load_builder_module()
        package_dir, manifest_out = self.locations("rollback")
        files = [(PurePosixPath("SKILL.md"), b"runtime bytes\n")]
        manifest = {
            "schema_version": 1,
            "files": [],
            "package_identity_sha256": "0" * 64,
        }
        original_replace = Path.replace

        def replace_then_fail(path: Path, target: Path) -> Path:
            if Path(target) == manifest_out:
                raise OSError("synthetic manifest commit failure")
            return original_replace(path, target)

        with mock.patch.object(Path, "replace", new=replace_then_fail):
            with self.assertRaisesRegex(OSError, "synthetic manifest commit failure"):
                builder.write_package(
                    package_dir=package_dir,
                    manifest_out=manifest_out,
                    files=files,
                    manifest=manifest,
                )

        self.assertFalse(package_dir.exists())
        self.assertFalse(manifest_out.exists())
        self.assertFalse(
            (manifest_out.parent / f".{manifest_out.name}.tmp").exists()
        )


if __name__ == "__main__":
    unittest.main()
