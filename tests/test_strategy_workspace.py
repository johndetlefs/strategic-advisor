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
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPOSITORY_ROOT / "scripts" / "strategy_workspace.py"
TEMPLATES = (
    REPOSITORY_ROOT / "skills" / "strategic-advisor" / "workspace-templates"
)
FILES = {
    "WORKSPACE.md",
    "PORTFOLIO.md",
    "CLAIMS.md",
    "DECISIONS.md",
    "CHANGELOG.md",
}


def load_tool_module():
    spec = importlib.util.spec_from_file_location("strategy_workspace_tool", TOOL)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load strategy workspace tool")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class StrategyWorkspaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_tool(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), *arguments],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )

    def build(self, name: str = "workspace") -> tuple[Path, dict]:
        destination = self.base / name
        result = self.run_tool("build", "--destination", str(destination))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return destination, json.loads(result.stdout)

    def validate(
        self, workspace: Path, as_of: str = "2026-07-24"
    ) -> tuple[subprocess.CompletedProcess[str], dict]:
        result = self.run_tool(
            "validate",
            "--workspace",
            str(workspace),
            "--as-of",
            as_of,
        )
        return result, json.loads(result.stdout)

    def insert_row(self, workspace: Path, name: str, row: str) -> None:
        path = workspace / name
        lines = path.read_text(encoding="utf-8").splitlines()
        separator = next(
            index for index, line in enumerate(lines) if line.startswith("| ---")
        )
        lines.insert(separator + 1, row)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def add_valid_rows(self, workspace: Path) -> None:
        self.insert_row(
            workspace,
            "WORKSPACE.md",
            "| CTX-001 | Synthetic scope | Report | Synthetic source | 2026-07-01 | 2026-12-31 | Synthetic limitation | Approved 2026-07-02 |",
        )
        self.insert_row(
            workspace,
            "PORTFOLIO.md",
            "| PORT-001 | Synthetic project | Test outcome | Option | One bounded test | Preference | Owner statement | 2026-07-01 | 2026-12-31 | Approved 2026-07-02 |",
        )
        self.insert_row(
            workspace,
            "CLAIMS.md",
            "| CLM-001 | Synthetic proposition | Assumption | Synthetic fixture | 2026-07-01 | 2026-12-31 | Not externally tested | None | Synthetic disconfirming observation | Approved 2026-07-02 |",
        )
        self.insert_row(
            workspace,
            "DECISIONS.md",
            "| DEC-001 | Run a synthetic test | Active | CLM-001 | 2026-07-02 | 2026-12-31 | Synthetic stop condition | None | Approved 2026-07-02 |",
        )
        self.insert_row(
            workspace,
            "CHANGELOG.md",
            "| CHG-001 | CLM-001 | Add synthetic record | Applied | 2026-07-02 | 2026-07-02 | Approved 2026-07-02 | Test fixture |",
        )

    def assert_error(self, payload: dict, code: str) -> None:
        self.assertEqual(payload["status"], "invalid")
        self.assertIn(code, {item["code"] for item in payload["errors"]})

    def test_two_builds_are_exact_and_byte_identical(self) -> None:
        first, first_payload = self.build("first")
        second, second_payload = self.build("second")
        self.assertEqual(set(path.name for path in first.iterdir()), FILES)
        self.assertEqual(first_payload["files"], second_payload["files"])
        for name in FILES:
            self.assertEqual((first / name).read_bytes(), (second / name).read_bytes())
            self.assertEqual((first / name).read_bytes(), (TEMPLATES / name).read_bytes())
        aggregate = hashlib.sha256(
            b"".join((first / name).read_bytes() for name in sorted(FILES))
        ).hexdigest()
        self.assertEqual(
            aggregate,
            hashlib.sha256(
                b"".join((second / name).read_bytes() for name in sorted(FILES))
            ).hexdigest(),
        )

    def test_build_refuses_existing_destination_without_overwrite(self) -> None:
        workspace, _ = self.build()
        marker = workspace / "owner-file.txt"
        marker.write_text("preserve\n", encoding="utf-8")
        result = self.run_tool("build", "--destination", str(workspace))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(marker.read_text(encoding="utf-8"), "preserve\n")

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks are unavailable")
    def test_build_refuses_symlinked_destination_parent(self) -> None:
        real_parent = self.base / "real"
        real_parent.mkdir()
        linked_parent = self.base / "linked"
        linked_parent.symlink_to(real_parent, target_is_directory=True)
        result = self.run_tool(
            "build", "--destination", str(linked_parent / "workspace")
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((real_parent / "workspace").exists())
        self.assertIn("symlink", result.stderr.lower())

    def test_build_rejects_unapproved_template_layout(self) -> None:
        tool = load_tool_module()
        source = self.base / "templates"
        shutil.copytree(TEMPLATES, source)
        (source / "EXTRA.md").write_text("# Extra\n", encoding="utf-8")
        original = tool.TEMPLATE_ROOT
        tool.TEMPLATE_ROOT = source
        try:
            with self.assertRaisesRegex(tool.WorkspaceError, "approved file set"):
                tool.canonical_templates()
        finally:
            tool.TEMPLATE_ROOT = original

    def test_blank_and_synthetic_workspaces_validate(self) -> None:
        blank, _ = self.build("blank")
        blank_result, blank_payload = self.validate(blank)
        self.assertEqual(blank_result.returncode, 0, blank_result.stderr)
        self.assertEqual(blank_payload["status"], "valid")
        synthetic, _ = self.build("synthetic")
        self.add_valid_rows(synthetic)
        result, payload = self.validate(synthetic)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(payload["status"], "valid")

    def test_missing_and_extra_files_fail(self) -> None:
        workspace, _ = self.build()
        (workspace / "CLAIMS.md").unlink()
        (workspace / "EXTRA.md").write_text("# Extra\n", encoding="utf-8")
        result, payload = self.validate(workspace)
        self.assertNotEqual(result.returncode, 0)
        codes = {item["code"] for item in payload["errors"]}
        self.assertIn("WORKSPACE_FILE_MISSING", codes)
        self.assertIn("WORKSPACE_FILE_EXTRA", codes)

    def test_heading_and_table_schema_drift_fail(self) -> None:
        workspace, _ = self.build()
        path = workspace / "CLAIMS.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("## Claim ledger", "## Notes", 1)
        text = text.replace("| Claim ID |", "| Record |", 1)
        path.write_text(text, encoding="utf-8")
        result, payload = self.validate(workspace)
        self.assertNotEqual(result.returncode, 0)
        codes = {item["code"] for item in payload["errors"]}
        self.assertIn("WORKSPACE_HEADING", codes)
        self.assertIn("WORKSPACE_TABLE_SCHEMA", codes)

    def test_record_id_status_and_duplicate_failures_are_named(self) -> None:
        workspace, _ = self.build()
        row = "| BAD | Synthetic proposition | Belief | Fixture | 2026-07-01 | 2026-12-31 | Limitation | None | Falsifier | Approved ref |"
        self.insert_row(workspace, "CLAIMS.md", row)
        self.insert_row(workspace, "CLAIMS.md", row)
        result, payload = self.validate(workspace)
        self.assertNotEqual(result.returncode, 0)
        codes = {item["code"] for item in payload["errors"]}
        self.assertIn("WORKSPACE_RECORD_ID", codes)
        self.assertIn("WORKSPACE_ORIGIN_STATUS", codes)

        second, _ = self.build("duplicate")
        valid = "| CLM-001 | Synthetic proposition | Report | Fixture | 2026-07-01 | 2026-12-31 | Limitation | None | Falsifier | Approved ref |"
        self.insert_row(second, "CLAIMS.md", valid)
        self.insert_row(second, "CLAIMS.md", valid)
        _, duplicate_payload = self.validate(second)
        self.assert_error(duplicate_payload, "WORKSPACE_DUPLICATE_ID")

    def test_missing_provenance_freshness_and_approval_fail(self) -> None:
        workspace, _ = self.build()
        self.insert_row(
            workspace,
            "WORKSPACE.md",
            "| CTX-001 | Synthetic scope | Report |  |  |  | Limitation |  |",
        )
        result, payload = self.validate(workspace)
        self.assertNotEqual(result.returncode, 0)
        required_messages = {
            item["message"]
            for item in payload["errors"]
            if item["code"] == "WORKSPACE_REQUIRED_FIELD"
        }
        self.assertIn("Provenance must not be empty", required_messages)
        self.assertIn("Last checked must not be empty", required_messages)
        self.assertIn("Review by must not be empty", required_messages)
        self.assertIn("Owner approval must not be empty", required_messages)

    def test_invalid_approval_falsifier_and_missing_reference_fail(self) -> None:
        workspace, _ = self.build()
        self.insert_row(
            workspace,
            "CLAIMS.md",
            "| CLM-001 | Synthetic proposition | Report | Fixture | 2026-07-01 | 2026-12-31 | Limitation | CLM-999 | None | Not approved |",
        )
        result, payload = self.validate(workspace)
        self.assertNotEqual(result.returncode, 0)
        codes = {item["code"] for item in payload["errors"]}
        self.assertIn("WORKSPACE_OWNER_APPROVAL", codes)
        self.assertIn("WORKSPACE_FALSIFIER", codes)
        self.assertIn("WORKSPACE_REFERENCE_MISSING", codes)

    def test_stale_and_conflicting_claims_are_attention_not_errors(self) -> None:
        workspace, _ = self.build()
        self.insert_row(
            workspace,
            "CLAIMS.md",
            "| CLM-001 | First synthetic proposition | Report | Fixture A | 2026-01-01 | 2026-02-01 | Limitation | CLM-002 | Falsifier A | Approved ref |",
        )
        self.insert_row(
            workspace,
            "CLAIMS.md",
            "| CLM-002 | Rival synthetic proposition | Inference | Fixture B | 2026-07-01 | 2026-12-31 | Limitation | CLM-001 | Falsifier B | Approved ref |",
        )
        result, payload = self.validate(workspace)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(payload["status"], "valid_with_attention")
        pairs = {(item["code"], item["record_id"]) for item in payload["attention"]}
        self.assertIn(("WORKSPACE_STALE", "CLM-001"), pairs)
        self.assertIn(("WORKSPACE_CONFLICT", "CLM-001"), pairs)
        self.assertIn(("WORKSPACE_CONFLICT", "CLM-002"), pairs)
        self.assertEqual(payload["errors"], [])

    def test_private_evaluation_secret_and_copied_logic_fail(self) -> None:
        mutations = {
            "private": ("PRIVATE_" + "CASE_DATA", "WORKSPACE_FORBIDDEN_CONTENT"),
            "evaluation": ('"expected_properties"', "WORKSPACE_FORBIDDEN_CONTENT"),
            "secret": ("ghp_" + ("A" * 32), "WORKSPACE_SECRET"),
        }
        for label, (marker, code) in mutations.items():
            with self.subTest(label=label):
                workspace, _ = self.build(label)
                path = workspace / "WORKSPACE.md"
                path.write_text(
                    path.read_text(encoding="utf-8") + f"\n{marker}\n",
                    encoding="utf-8",
                )
                result, payload = self.validate(workspace)
                self.assertNotEqual(result.returncode, 0)
                self.assert_error(payload, code)

        copied, _ = self.build("copied")
        skill = (
            REPOSITORY_ROOT / "skills" / "strategic-advisor" / "SKILL.md"
        ).read_text(encoding="utf-8")
        paragraph = next(
            item
            for item in skill.split("\n\n")
            if len(item) >= 180 and len(item.split()) >= 24
        )
        path = copied / "WORKSPACE.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\n" + paragraph + "\n",
            encoding="utf-8",
        )
        result, payload = self.validate(copied)
        self.assertNotEqual(result.returncode, 0)
        self.assert_error(payload, "WORKSPACE_COPIED_LOGIC")


if __name__ == "__main__":
    unittest.main()
