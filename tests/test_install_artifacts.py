from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path, PurePosixPath


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_BUILDER = REPOSITORY_ROOT / "scripts" / "build_runtime_package.py"
INSTALL_BUILDER = REPOSITORY_ROOT / "scripts" / "build_install_artifacts.py"
CANONICAL_LICENSE_BYTES = (REPOSITORY_ROOT / "LICENSE").read_bytes()
CANONICAL_LICENSE_SHA256 = hashlib.sha256(CANONICAL_LICENSE_BYTES).hexdigest()
FIXED_DATETIME = (1980, 1, 1, 0, 0, 0)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class InstallArtifactTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary_directory.name).resolve()
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
        self.evaluation_sentinel = (
            "PRIVATE-EVALUATION-SENTINEL-MUST-NOT-ENTER-INSTALL-ARCHIVES"
        )
        (self.skill_root / "evals" / "cases.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "cases": [
                        {
                            "id": "CASE-001",
                            "prompt": self.evaluation_sentinel
                            + " with enough unique content to become a fingerprint",
                        }
                    ],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        self.allowlist_path = self.skill_root / "runtime-manifest.json"
        self.allowlist_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "package_root": "skills/strategic-advisor",
                    "include": [
                        "references/one.md",
                        "SKILL.md",
                        "agents/openai.yaml",
                    ],
                    "excluded_roots": ["evals", "evaluation-results"],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (self.source_root / "LICENSE").write_bytes(CANONICAL_LICENSE_BYTES)
        self.runtime_builder = load_module(
            f"runtime_builder_for_install_{id(self)}", RUNTIME_BUILDER
        )
        _, runtime_manifest = self.expected_runtime()
        fixture_version = "0.0.0-alpha.1"
        (self.source_root / "distribution.json").write_text(
            json.dumps(
                {
                    "current_public": {
                        "evidence": (
                            f"evidence/releases/v{fixture_version}.json"
                        ),
                        "runtime_package_identity_sha256": runtime_manifest[
                            "package_identity_sha256"
                        ],
                        "source_revision": "1" * 40,
                        "tag": f"v{fixture_version}",
                        "version": fixture_version,
                    },
                    "distribution": {
                        "runtime_package_identity_sha256": runtime_manifest[
                            "package_identity_sha256"
                        ],
                        "version": fixture_version,
                    },
                    "schema_version": 1,
                    "state": "published",
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def outputs(self, label: str) -> tuple[Path, Path, Path, Path]:
        output_root = self.base / label
        return (
            output_root / "strategic-advisor.zip",
            output_root / "strategic-advisor-codex-plugin.zip",
            output_root / "install-artifacts.json",
            output_root / "strategic-advisor-chatgpt.zip",
        )

    def run_builder(
        self,
        label: str,
        *,
        allow_dirty: bool = True,
        allowlist_value: str | None = None,
        license_value: str | None = "LICENSE",
        outputs: tuple[Path, Path, Path, Path] | None = None,
    ) -> tuple[subprocess.CompletedProcess[str], Path, Path, Path, Path]:
        skill_archive, plugin_archive, provenance, chatgpt_kit = (
            outputs or self.outputs(label)
        )
        command = [
            sys.executable,
            str(INSTALL_BUILDER),
            "--source-root",
            str(self.source_root),
        ]
        if allowlist_value is not None:
            command.extend(["--allowlist", allowlist_value])
        if license_value is not None:
            command.extend(["--license", license_value])
        command.extend(
            [
                "--skill-archive",
                str(skill_archive),
                "--plugin-archive",
                str(plugin_archive),
                "--chatgpt-kit",
                str(chatgpt_kit),
                "--provenance-out",
                str(provenance),
            ]
        )
        if allow_dirty:
            command.append("--allow-dirty")
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result, skill_archive, plugin_archive, provenance, chatgpt_kit

    def run_verifier(
        self,
        skill_archive: Path,
        plugin_archive: Path,
        provenance: Path,
        chatgpt_kit: Path | None = None,
        *,
        expected_provenance_sha256: str | None = None,
        expected_runtime_identity: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(INSTALL_BUILDER),
            "verify",
            "--skill-archive",
            str(skill_archive),
            "--plugin-archive",
            str(plugin_archive),
            "--chatgpt-kit",
            str(
                chatgpt_kit
                or provenance.parent / "strategic-advisor-chatgpt.zip"
            ),
            "--provenance",
            str(provenance),
        ]
        if expected_provenance_sha256 is not None:
            command.extend(
                ["--expected-provenance-sha256", expected_provenance_sha256]
            )
        if expected_runtime_identity is not None:
            command.extend(
                ["--expected-runtime-identity", expected_runtime_identity]
            )
        return subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def initialize_git(self) -> str:
        commands = (
            ["git", "init", str(self.source_root)],
            ["git", "-C", str(self.source_root), "config", "user.name", "Fixture"],
            [
                "git",
                "-C",
                str(self.source_root),
                "config",
                "user.email",
                "fixture@example.invalid",
            ],
            ["git", "-C", str(self.source_root), "add", "."],
            [
                "git",
                "-C",
                str(self.source_root),
                "-c",
                "commit.gpgsign=false",
                "commit",
                "-m",
                "fixture",
            ],
        )
        for command in commands:
            completed = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(
                completed.returncode, 0, completed.stdout + completed.stderr
            )
        return subprocess.run(
            ["git", "-C", str(self.source_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def expected_runtime(self) -> tuple[list[tuple[object, bytes]], dict]:
        allowlist_relative = self.runtime_builder.normalized_relative_path(
            self.runtime_builder.DEFAULT_ALLOWLIST, "allowlist path"
        )
        allowlist, allowlist_bytes, _ = self.runtime_builder.load_allowlist(
            self.source_root, allowlist_relative
        )
        package_root, files = self.runtime_builder.collect_files(
            self.source_root, allowlist
        )
        self.runtime_builder.reject_evaluation_content(self.source_root, files)
        manifest = self.runtime_builder.package_manifest(
            allowlist_relative,
            allowlist_bytes,
            package_root,
            files,
        )
        return files, manifest

    def assert_zip_policy(self, archive_path: Path) -> None:
        with zipfile.ZipFile(archive_path) as archive:
            self.assertEqual(archive.comment, b"")
            names = archive.namelist()
            self.assertEqual(names, sorted(names))
            self.assertEqual(len(names), len(set(names)))
            for info in archive.infolist():
                self.assertEqual(info.date_time, FIXED_DATETIME)
                self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
                self.assertEqual(info.create_system, 3)
                self.assertEqual(info.extra, b"")
                self.assertEqual(info.comment, b"")
                expected_mode = 0o755 if info.is_dir() else 0o644
                self.assertEqual((info.external_attr >> 16) & 0o777, expected_mode)
                file_type = (info.external_attr >> 16) & 0o170000
                self.assertEqual(
                    file_type, stat.S_IFDIR if info.is_dir() else stat.S_IFREG
                )

    def rewrite_zip(
        self,
        source: Path,
        destination: Path,
        transform,
    ) -> None:
        entries: list[tuple[str, bytes, zipfile.ZipInfo]] = []
        with zipfile.ZipFile(source) as archive:
            for info in archive.infolist():
                content = archive.read(info)
                transformed = transform(info.filename, content, info.is_dir())
                if transformed is None:
                    continue
                new_name, new_content = transformed
                entries.append((new_name, new_content, info))
        destination.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_STORED) as archive:
            archive.comment = b""
            for name, content, original in sorted(entries, key=lambda item: item[0]):
                info = zipfile.ZipInfo(name, date_time=original.date_time)
                info.compress_type = original.compress_type
                info.create_system = original.create_system
                info.external_attr = original.external_attr
                info.extra = original.extra
                info.comment = original.comment
                archive.writestr(info, content)

    def assert_verify_fails(
        self,
        skill_archive: Path,
        plugin_archive: Path,
        provenance: Path,
        expected_text: str,
        chatgpt_kit: Path | None = None,
    ) -> None:
        result = self.run_verifier(
            skill_archive,
            plugin_archive,
            provenance,
            chatgpt_kit=chatgpt_kit,
        )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("ERROR [INSTALL_ARTIFACTS]", result.stderr)
        self.assertIn(expected_text, result.stderr)

    def test_repeated_builds_are_identical_and_verify_without_source_tree(self) -> None:
        first = self.run_builder("first")
        second = self.run_builder("different-destination")
        self.assertEqual(first[0].returncode, 0, first[0].stdout + first[0].stderr)
        self.assertEqual(second[0].returncode, 0, second[0].stdout + second[0].stderr)
        self.assertEqual(json.loads(first[0].stdout), json.loads(second[0].stdout))
        for first_path, second_path in zip(first[1:], second[1:]):
            self.assertEqual(first_path.read_bytes(), second_path.read_bytes())

        provenance = json.loads(first[3].read_text(encoding="utf-8"))
        hidden_source = self.base / "source-hidden-from-verifier"
        self.source_root.rename(hidden_source)
        verification = self.run_verifier(
            first[1],
            first[2],
            first[3],
            expected_provenance_sha256=sha256_bytes(first[3].read_bytes()),
            expected_runtime_identity=provenance["runtime_package"][
                "package_identity_sha256"
            ],
        )
        self.assertEqual(
            verification.returncode, 0, verification.stdout + verification.stderr
        )
        summary = json.loads(verification.stdout)
        self.assertEqual(
            summary["verification"],
            "structural-and-internal-consistency-passed",
        )
        self.assertEqual(summary["build_mode"], "exploratory")
        self.assertFalse(summary["source_revision_exact"])
        self.assertEqual(summary["source_tree_state"], "not-git")
        self.assertTrue(summary["trusted_provenance_sha256_matched"])
        self.assertTrue(summary["trusted_runtime_identity_matched"])

    def test_exact_structure_license_and_openai_local_marketplace_metadata(self) -> None:
        result, skill_archive, plugin_archive, provenance_path, chatgpt_kit = self.run_builder(
            "structure"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        runtime_files, runtime_manifest = self.expected_runtime()
        expected_standalone = sorted(
            [
                "strategic-advisor/",
                "strategic-advisor/LICENSE",
                "strategic-advisor/SKILL.md",
                "strategic-advisor/agents/",
                "strategic-advisor/agents/openai.yaml",
                "strategic-advisor/references/",
                "strategic-advisor/references/one.md",
            ]
        )
        expected_plugin = sorted(
            [
                ".agents/",
                ".agents/plugins/",
                ".agents/plugins/marketplace.json",
                "plugins/",
                "plugins/strategic-advisor/",
                "plugins/strategic-advisor/.codex-plugin/",
                "plugins/strategic-advisor/.codex-plugin/plugin.json",
                "plugins/strategic-advisor/skills/",
                "plugins/strategic-advisor/skills/strategic-advisor/",
                "plugins/strategic-advisor/skills/strategic-advisor/LICENSE",
                "plugins/strategic-advisor/skills/strategic-advisor/SKILL.md",
                "plugins/strategic-advisor/skills/strategic-advisor/agents/",
                "plugins/strategic-advisor/skills/strategic-advisor/agents/openai.yaml",
                "plugins/strategic-advisor/skills/strategic-advisor/references/",
                "plugins/strategic-advisor/skills/strategic-advisor/references/one.md",
            ]
        )
        with zipfile.ZipFile(skill_archive) as standalone, zipfile.ZipFile(
            plugin_archive
        ) as plugin, zipfile.ZipFile(chatgpt_kit) as chatgpt:
            self.assertEqual(standalone.namelist(), expected_standalone)
            self.assertEqual(plugin.namelist(), expected_plugin)
            for relative, expected_bytes in runtime_files:
                self.assertEqual(
                    standalone.read(f"strategic-advisor/{relative.as_posix()}"),
                    expected_bytes,
                )
                self.assertEqual(
                    plugin.read(
                        "plugins/strategic-advisor/skills/strategic-advisor/"
                        + relative.as_posix()
                    ),
                    expected_bytes,
                )
            self.assertEqual(
                standalone.read("strategic-advisor/LICENSE"), CANONICAL_LICENSE_BYTES
            )
            self.assertEqual(
                plugin.read(
                    "plugins/strategic-advisor/skills/strategic-advisor/LICENSE"
                ),
                CANONICAL_LICENSE_BYTES,
            )
            plugin_manifest = json.loads(
                plugin.read("plugins/strategic-advisor/.codex-plugin/plugin.json")
            )
            self.assertEqual(plugin_manifest["name"], "strategic-advisor")
            self.assertEqual(plugin_manifest["skills"], "./skills/")
            self.assertEqual(plugin_manifest["license"], "Apache-2.0")
            self.assertEqual(plugin_manifest["author"]["name"], "Strategic Advisor contributors")
            self.assertEqual(
                set(plugin_manifest["interface"]),
                {
                    "capabilities",
                    "category",
                    "defaultPrompt",
                    "developerName",
                    "displayName",
                    "longDescription",
                    "shortDescription",
                },
            )
            self.assertNotIn("apps", plugin_manifest)
            self.assertNotIn("mcpServers", plugin_manifest)
            marketplace = json.loads(plugin.read(".agents/plugins/marketplace.json"))
            self.assertEqual(marketplace["name"], "strategic-advisor")
            self.assertEqual(
                marketplace["plugins"][0]["source"],
                {"path": "./plugins/strategic-advisor", "source": "local"},
            )
            self.assertEqual(
                chatgpt.namelist(),
                sorted(
                    [
                        "strategic-advisor-chatgpt/",
                        "strategic-advisor-chatgpt/CONFIG.json",
                        "strategic-advisor-chatgpt/INSTRUCTIONS.md",
                        "strategic-advisor-chatgpt/KNOWLEDGE/",
                        "strategic-advisor-chatgpt/KNOWLEDGE/one.md",
                        "strategic-advisor-chatgpt/LICENSE",
                        "strategic-advisor-chatgpt/MANIFEST.json",
                        "strategic-advisor-chatgpt/README.md",
                    ]
                ),
            )
            instructions = chatgpt.read(
                "strategic-advisor-chatgpt/INSTRUCTIONS.md"
            )
            self.assertTrue(
                instructions.endswith(
                    dict(runtime_files)[PurePosixPath("SKILL.md")]
                )
            )
            self.assertEqual(
                chatgpt.read("strategic-advisor-chatgpt/KNOWLEDGE/one.md"),
                dict(runtime_files)[PurePosixPath("references/one.md")],
            )
            config = json.loads(
                chatgpt.read("strategic-advisor-chatgpt/CONFIG.json")
            )
            self.assertEqual(config["apps"], [])
            self.assertEqual(config["actions"], [])
            self.assertEqual(config["knowledge_upload_order"], ["one.md"])
            starters = config["conversation_starters"]
            self.assertTrue(
                any("outside my portfolio" in starter for starter in starters)
            )
            self.assertTrue(any("clean slate" in starter for starter in starters))
            self.assertTrue(
                any("within my current projects" in starter for starter in starters)
            )

        self.assert_zip_policy(skill_archive)
        self.assert_zip_policy(plugin_archive)
        self.assert_zip_policy(chatgpt_kit)
        provenance = json.loads(provenance_path.read_bytes())
        self.assertEqual(provenance["schema_version"], 3)
        self.assertEqual(provenance["build_mode"], "exploratory")
        self.assertFalse(provenance["source_revision_exact"])
        self.assertEqual(provenance["runtime_package"], runtime_manifest)
        self.assertEqual(provenance["license"]["sha256"], CANONICAL_LICENSE_SHA256)
        self.assertTrue(provenance["license"]["apache_2_0_canonical"])
        self.assertEqual(
            set(provenance["artifacts"]),
            {
                "chatgpt_custom_gpt",
                "standalone_skill",
                "openai_local_marketplace",
            },
        )
        openai_artifact = provenance["artifacts"]["openai_local_marketplace"]
        self.assertEqual(
            openai_artifact["distribution"], "openai-local-marketplace-plugin"
        )
        self.assertEqual(
            openai_artifact["target_surfaces"],
            ["chatgpt-desktop-work", "codex"],
        )
        self.assertEqual(
            openai_artifact["excluded_distribution_claims"],
            [
                "chatgpt-personal-skill-upload",
                "public-plugin-directory-submission",
            ],
        )

    def test_plugin_version_matches_public_early_access_contract(self) -> None:
        contract_text = (REPOSITORY_ROOT / "PRODUCT-CONTRACT.md").read_text(
            encoding="utf-8"
        )
        match = re.search(
            r"<!-- strategic-advisor-contract:start -->\s*```json\s*(.*?)\s*```",
            contract_text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        contract = json.loads(match.group(1))
        authority = json.loads(
            (REPOSITORY_ROOT / "distribution.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            authority["current_public"]["version"],
            contract["early_access_distribution_version"],
        )
        self.assertEqual(
            authority["distribution"]["version"],
            contract["prepared_distribution_version"],
        )

    def test_current_runtime_fits_chatgpt_knowledge_inventory(self) -> None:
        allowlist = json.loads(
            (
                REPOSITORY_ROOT
                / "skills"
                / "strategic-advisor"
                / "runtime-manifest.json"
            ).read_text(encoding="utf-8")
        )
        builder = load_module(
            f"install_builder_inventory_{id(self)}", INSTALL_BUILDER
        )
        runtime_by_path = {
            path: (
                REPOSITORY_ROOT / "skills" / "strategic-advisor" / path
            ).read_bytes()
            for path in allowlist["include"]
        }
        runtime_files = [
            {
                "path": path,
                "sha256": sha256_bytes(runtime_by_path[path]),
                "size_bytes": len(runtime_by_path[path]),
            }
            for path in allowlist["include"]
        ]
        records = builder._chatgpt_knowledge_records(
            runtime_files, runtime_by_path
        )
        self.assertEqual(len(records), 16)
        self.assertLessEqual(len(records), builder.CHATGPT_KNOWLEDGE_LIMIT)
        self.assertEqual(
            len({record["upload_name"] for record in records}), len(records)
        )

        bundle = next(
            record
            for record in records
            if record["upload_name"]
            == builder.CHATGPT_WORKSPACE_TEMPLATE_BUNDLE
        )
        expected_templates = sorted(
            path
            for path in allowlist["include"]
            if path.startswith(builder.CHATGPT_WORKSPACE_TEMPLATE_PREFIX)
        )
        self.assertEqual(bundle["source_paths"], expected_templates)
        bundle_bytes = builder._chatgpt_workspace_template_bundle_bytes(
            bundle["source_paths"], runtime_by_path
        )
        self.assertEqual(bundle["sha256"], sha256_bytes(bundle_bytes))
        self.assertEqual(bundle["size_bytes"], len(bundle_bytes))
        for path in expected_templates:
            self.assertIn(f"## `{path}`\n".encode("utf-8"), bundle_bytes)
            self.assertIn(runtime_by_path[path], bundle_bytes)

    def test_root_license_is_mandatory_exact_and_not_substitutable(self) -> None:
        license_path = self.source_root / "LICENSE"
        license_path.unlink()
        result = self.run_builder("missing-license")
        self.assertNotEqual(result[0].returncode, 0)
        self.assertIn("repository-root LICENSE is missing", result[0].stderr)
        self.assertFalse(result[1].exists())

        license_path.write_bytes(b"Apache License 2.0, approximately.\n")
        result = self.run_builder("fake-license")
        self.assertNotEqual(result[0].returncode, 0)
        self.assertIn("not the complete canonical Apache License 2.0", result[0].stderr)

        license_path.write_bytes(CANONICAL_LICENSE_BYTES)
        result = self.run_builder("wrong-license-argument", license_value="README.md")
        self.assertNotEqual(result[0].returncode, 0)
        self.assertIn("invalid choice", result[0].stderr)

        license_path.unlink()
        os.symlink(REPOSITORY_ROOT / "LICENSE", license_path)
        result = self.run_builder("symlink-license")
        self.assertNotEqual(result[0].returncode, 0)
        self.assertIn("traverses symlink", result[0].stderr)

    def test_builder_rejects_alternate_committed_or_exploratory_allowlist(self) -> None:
        alternate = self.skill_root / "alternate-runtime-manifest.json"
        alternate.write_bytes(self.allowlist_path.read_bytes())
        result = self.run_builder(
            "alternate-allowlist",
            allowlist_value="skills/strategic-advisor/alternate-runtime-manifest.json",
        )
        self.assertNotEqual(result[0].returncode, 0)
        self.assertIn("invalid choice", result[0].stderr)
        for path in result[1:]:
            self.assertFalse(path.exists())
        self.initialize_git()
        release = self.run_builder(
            "committed-alternate-allowlist",
            allow_dirty=False,
            allowlist_value="skills/strategic-advisor/alternate-runtime-manifest.json",
        )
        self.assertNotEqual(release[0].returncode, 0)
        self.assertIn("invalid choice", release[0].stderr)
        for path in release[1:]:
            self.assertFalse(path.exists())

    def test_release_requires_git_root_but_allow_dirty_is_explicitly_inexact(self) -> None:
        release = self.run_builder("non-git-release", allow_dirty=False)
        self.assertNotEqual(release[0].returncode, 0)
        self.assertIn("release build requires a clean Git repository root", release[0].stderr)
        for path in release[1:]:
            self.assertFalse(path.exists())

        self.initialize_git()
        exploratory = self.run_builder("clean-but-exploratory", allow_dirty=True)
        self.assertEqual(
            exploratory[0].returncode,
            0,
            exploratory[0].stdout + exploratory[0].stderr,
        )
        provenance = json.loads(exploratory[3].read_text(encoding="utf-8"))
        self.assertEqual(provenance["source_tree_state"], "clean")
        self.assertFalse(provenance["source_revision_exact"])
        self.assertEqual(provenance["build_mode"], "exploratory")
        self.assertFalse(provenance["git_source_verification"]["performed"])

    def test_clean_release_proves_every_selected_input_against_head(self) -> None:
        revision = self.initialize_git()
        result, skill_archive, plugin_archive, provenance_path, _chatgpt_kit = self.run_builder(
            "clean-release", allow_dirty=False
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        self.assertEqual(provenance["build_mode"], "release")
        self.assertTrue(provenance["source_revision_exact"])
        self.assertEqual(provenance["source_revision"], revision)
        git_proof = provenance["git_source_verification"]
        self.assertTrue(git_proof["performed"])
        self.assertTrue(git_proof["status_rechecked_before_write"])
        self.assertEqual(git_proof["revision"], revision)
        self.assertEqual(
            [entry["path"] for entry in git_proof["input_files"]],
            sorted(
                [
                    "LICENSE",
                    "distribution.json",
                    "skills/strategic-advisor/SKILL.md",
                    "skills/strategic-advisor/agents/openai.yaml",
                    "skills/strategic-advisor/references/one.md",
                    "skills/strategic-advisor/runtime-manifest.json",
                ]
            ),
        )
        verification = self.run_verifier(skill_archive, plugin_archive, provenance_path)
        self.assertEqual(
            verification.returncode, 0, verification.stdout + verification.stderr
        )

    def test_release_rejects_dirty_and_git_hidden_worktree_mutations(self) -> None:
        self.initialize_git()
        skill = self.skill_root / "SKILL.md"
        skill.write_text(skill.read_text() + "\nDirty mutation.\n", encoding="utf-8")
        dirty = self.run_builder("dirty-release", allow_dirty=False)
        self.assertNotEqual(dirty[0].returncode, 0)
        self.assertIn("source Git tree is dirty", dirty[0].stderr)

        subprocess.run(
            ["git", "-C", str(self.source_root), "checkout", "--", str(skill)],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(self.source_root),
                "update-index",
                "--assume-unchanged",
                "skills/strategic-advisor/SKILL.md",
            ],
            check=True,
            capture_output=True,
        )
        skill.write_text(skill.read_text() + "\nHidden mutation.\n", encoding="utf-8")
        hidden = self.run_builder("hidden-release", allow_dirty=False)
        self.assertNotEqual(hidden[0].returncode, 0)
        self.assertIn("canonical runtime bytes do not match", hidden[0].stderr)
        for path in hidden[1:]:
            self.assertFalse(path.exists())

    def test_rejects_symlinked_output_ancestor(self) -> None:
        real_output = self.base / "real-output"
        real_output.mkdir()
        linked_output = self.base / "linked-output"
        linked_output.symlink_to(real_output, target_is_directory=True)
        outputs = (
            linked_output / "skill.zip",
            linked_output / "plugin.zip",
            linked_output / "provenance.json",
            linked_output / "chatgpt.zip",
        )
        result = self.run_builder("unused", outputs=outputs)
        self.assertNotEqual(result[0].returncode, 0)
        self.assertIn("symlinked destination or ancestor", result[0].stderr)
        self.assertEqual(list(real_output.iterdir()), [])

    def test_refuses_overwrite_without_touching_other_outputs(self) -> None:
        skill_archive, plugin_archive, provenance, chatgpt_kit = self.outputs("overwrite")
        skill_archive.parent.mkdir(parents=True)
        sentinel = b"existing-user-file\n"
        skill_archive.write_bytes(sentinel)
        result = self.run_builder(
            "unused", outputs=(skill_archive, plugin_archive, provenance, chatgpt_kit)
        )
        self.assertNotEqual(result[0].returncode, 0)
        self.assertIn("already exists", result[0].stderr)
        self.assertEqual(skill_archive.read_bytes(), sentinel)
        self.assertFalse(plugin_archive.exists())
        self.assertFalse(provenance.exists())
        self.assertFalse(chatgpt_kit.exists())

    def test_archives_and_provenance_exclude_evaluation_material(self) -> None:
        result, skill_archive, plugin_archive, provenance, chatgpt_kit = self.run_builder("no-evals")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for artifact in (skill_archive, plugin_archive, chatgpt_kit):
            with zipfile.ZipFile(io.BytesIO(artifact.read_bytes())) as archive:
                self.assertFalse(
                    any(
                        part.lower().startswith("eval")
                        for name in archive.namelist()
                        for part in Path(name).parts
                    )
                )
                for name in archive.namelist():
                    if not name.endswith("/"):
                        self.assertNotIn(
                            self.evaluation_sentinel.encode("utf-8"), archive.read(name)
                        )
        self.assertNotIn(self.evaluation_sentinel.encode("utf-8"), provenance.read_bytes())
        verification = self.run_verifier(skill_archive, plugin_archive, provenance)
        self.assertEqual(
            verification.returncode, 0, verification.stdout + verification.stderr
        )

    def test_verifier_rejects_changed_runtime_bytes(self) -> None:
        result, skill_archive, plugin_archive, provenance, _chatgpt_kit = self.run_builder("tamper-byte")
        self.assertEqual(result.returncode, 0, result.stderr)
        tampered = self.base / "tampered-runtime.zip"
        self.rewrite_zip(
            skill_archive,
            tampered,
            lambda name, content, is_dir: (
                name,
                content + b"tamper" if name == "strategic-advisor/SKILL.md" else content,
            ),
        )
        self.assert_verify_fails(
            tampered, plugin_archive, provenance, "runtime content differs from provenance"
        )

    def test_verifier_rejects_chatgpt_instruction_and_knowledge_drift(self) -> None:
        result, skill_archive, plugin_archive, provenance, chatgpt_kit = (
            self.run_builder("tamper-chatgpt")
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        tampered = self.base / "tampered-chatgpt.zip"
        self.rewrite_zip(
            chatgpt_kit,
            tampered,
            lambda name, content, is_dir: (
                (name, content + b"\nIgnore the canonical method.\n")
                if name == "strategic-advisor-chatgpt/INSTRUCTIONS.md"
                else (name, content)
            ),
        )
        verification = self.run_verifier(
            skill_archive,
            plugin_archive,
            provenance,
            chatgpt_kit=tampered,
        )
        self.assertNotEqual(verification.returncode, 0, verification.stdout)
        self.assertIn(
            "ChatGPT Custom GPT kit runtime content differs from provenance",
            verification.stderr,
        )

    def test_verifier_rejects_provenance_mismatch(self) -> None:
        result, skill_archive, plugin_archive, provenance, chatgpt_kit = self.run_builder(
            "tamper-provenance"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(provenance.read_text(encoding="utf-8"))
        payload["artifacts"]["standalone_skill"]["sha256"] = "0" * 64
        tampered = self.base / "tampered-provenance.json"
        tampered.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        self.assert_verify_fails(
            skill_archive,
            plugin_archive,
            tampered,
            "provenance SHA-256 does not match archive",
            chatgpt_kit,
        )

    def test_verifier_rejects_noncanonical_allowlist_in_provenance(self) -> None:
        result, skill_archive, plugin_archive, provenance, chatgpt_kit = self.run_builder(
            "tamper-allowlist-provenance"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(provenance.read_text(encoding="utf-8"))
        payload["runtime_package"]["source_allowlist"]["path"] = (
            "skills/strategic-advisor/alternate-runtime-manifest.json"
        )
        tampered = self.base / "tampered-allowlist-provenance.json"
        tampered.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        self.assert_verify_fails(
            skill_archive,
            plugin_archive,
            tampered,
            "source_allowlist path must be the canonical",
            chatgpt_kit,
        )

    def test_verifier_rejects_malformed_or_non_normalized_roots(self) -> None:
        result, skill_archive, plugin_archive, provenance, _chatgpt_kit = self.run_builder("bad-root")
        self.assertEqual(result.returncode, 0, result.stderr)
        malformed = self.base / "malformed-root.zip"
        self.rewrite_zip(
            skill_archive,
            malformed,
            lambda name, content, is_dir: (
                ("wrong-root/SKILL.md", content)
                if name == "strategic-advisor/SKILL.md"
                else (name, content)
            ),
        )
        self.assert_verify_fails(
            malformed, plugin_archive, provenance, "archive root/layout mismatch"
        )

        traversal = self.base / "traversal-root.zip"
        self.rewrite_zip(
            skill_archive,
            traversal,
            lambda name, content, is_dir: (
                ("strategic-advisor/../SKILL.md", content)
                if name == "strategic-advisor/SKILL.md"
                else (name, content)
            ),
        )
        self.assert_verify_fails(
            traversal, plugin_archive, provenance, "contains traversal or is not normalized"
        )

        control = self.base / "control-character-root.zip"
        self.rewrite_zip(
            skill_archive,
            control,
            lambda name, content, is_dir: (
                ("strategic-advisor/\tSKILL.md", content)
                if name == "strategic-advisor/SKILL.md"
                else (name, content)
            ),
        )
        self.assert_verify_fails(
            control, plugin_archive, provenance, "not POSIX-normalized"
        )

    def test_verifier_rejects_missing_and_wrong_license(self) -> None:
        result, skill_archive, plugin_archive, provenance, _chatgpt_kit = self.run_builder("bad-license")
        self.assertEqual(result.returncode, 0, result.stderr)
        missing = self.base / "missing-license.zip"
        self.rewrite_zip(
            skill_archive,
            missing,
            lambda name, content, is_dir: (
                None if name == "strategic-advisor/LICENSE" else (name, content)
            ),
        )
        self.assert_verify_fails(
            missing, plugin_archive, provenance, "missing the required root Apache-2.0 LICENSE"
        )

        wrong = self.base / "wrong-license.zip"
        self.rewrite_zip(
            skill_archive,
            wrong,
            lambda name, content, is_dir: (
                (name, b"not Apache-2.0\n")
                if name == "strategic-advisor/LICENSE"
                else (name, content)
            ),
        )
        self.assert_verify_fails(
            wrong, plugin_archive, provenance, "LICENSE bytes are missing or non-canonical"
        )

    def test_verifier_rejects_changed_openai_plugin_metadata(self) -> None:
        result, skill_archive, plugin_archive, provenance, _chatgpt_kit = self.run_builder(
            "bad-plugin-metadata"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        tampered = self.base / "tampered-plugin.zip"
        self.rewrite_zip(
            plugin_archive,
            tampered,
            lambda name, content, is_dir: (
                (name, content.replace(b"strategic-advisor", b"strategic-impostor", 1))
                if name == "plugins/strategic-advisor/.codex-plugin/plugin.json"
                else (name, content)
            ),
        )
        self.assert_verify_fails(
            skill_archive, tampered, provenance, "plugin-metadata differs from canonical"
        )

    def test_verifier_rejects_non_standard_json_constants(self) -> None:
        result, skill_archive, plugin_archive, provenance, chatgpt_kit = self.run_builder("nan")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = provenance.read_text(encoding="utf-8")
        tampered = self.base / "nan-provenance.json"
        tampered.write_text(
            payload.replace('"schema_version": 3', '"schema_version": NaN', 1),
            encoding="utf-8",
        )
        self.assert_verify_fails(
            skill_archive,
            plugin_archive,
            tampered,
            "non-standard JSON numeric constant: NaN",
            chatgpt_kit,
        )


if __name__ == "__main__":
    unittest.main()
