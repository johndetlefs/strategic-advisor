from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPOSITORY_ROOT / "scripts" / "validate.py"


class ValidatorFixtureTests(unittest.TestCase):
    """Exercise one isolated repository mutation per negative-fixture class."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.fixture_root = Path(self.temporary_directory.name) / "repository"
        shutil.copytree(
            REPOSITORY_ROOT,
            self.fixture_root,
            symlinks=True,
            ignore=shutil.ignore_patterns(
                ".git",
                ".project-workflow",
                "__pycache__",
                "tests",
            ),
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_validator(self, scope: str | None = None) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(VALIDATOR), "--root", str(self.fixture_root)]
        if scope:
            command.extend(["--scope", scope])
        return subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )

    def assert_named_failure(
        self, result: subprocess.CompletedProcess[str], diagnostic: str
    ) -> None:
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f"[{diagnostic}]", result.stdout)

    def test_unmodified_valid_fixture_passes(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUMMARY: PASS", result.stdout)

    def test_private_case_and_secret_fixture_fails_privacy_scope(self) -> None:
        token = "gh" + "p_" + ("A" * 32)
        private_label = "PRIVATE_" + "CASE_DATA"
        (self.fixture_root / "synthetic-private-fixture.txt").write_text(
            f"{private_label}: fictional employee narrative\nSynthetic token: {token}\n",
            encoding="utf-8",
        )
        result = self.run_validator("privacy")
        self.assert_named_failure(result, "PRIVACY_PRIVATE_CASE")
        self.assertIn("[PRIVACY_SECRET_PATTERN]", result.stdout)

    def test_unsupported_domain_claim_fails_claims_scope(self) -> None:
        path = self.fixture_root / "PRODUCT-CONTRACT.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            '"supported_capabilities": []',
            '"supported_capabilities": ["domain.business-venture"]',
            1,
        )
        path.write_text(text, encoding="utf-8")
        result = self.run_validator("claims")
        self.assert_named_failure(result, "CLAIMS_UNSUPPORTED")

    def test_forged_capability_evidence_string_fails_claims_scope(self) -> None:
        path = self.fixture_root / "PRODUCT-CONTRACT.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            '"supported_capabilities": []',
            '"supported_capabilities": ["core.reality-protocol"]',
            1,
        )
        text = text.replace(
            '"id": "core.reality-protocol",\n      "kind": "behaviour",\n      "state": "implemented-not-validated",\n      "evidence": []',
            '"id": "core.reality-protocol",\n      "kind": "behaviour",\n      "state": "validated",\n      "evidence": ["anything"]',
            1,
        )
        path.write_text(text, encoding="utf-8")
        result = self.run_validator("claims")
        self.assert_named_failure(result, "CLAIMS_EVIDENCE_INVALID")
        self.assertIn("[CLAIMS_PROMOTION_DISABLED]", result.stdout)

    def test_premature_capability_promotion_enablement_fails_claims_scope(self) -> None:
        path = self.fixture_root / "PRODUCT-CONTRACT.md"
        text = path.read_text(encoding="utf-8").replace(
            '"capability_promotion_enabled": false',
            '"capability_promotion_enabled": true',
            1,
        )
        path.write_text(text, encoding="utf-8")
        result = self.run_validator("claims")
        self.assert_named_failure(result, "CLAIMS_PROMOTION_DISABLED")

    def test_copied_strategic_logic_fails_skill_scope(self) -> None:
        canonical = (
            self.fixture_root / "skills" / "strategic-advisor" / "SKILL.md"
        ).read_text(encoding="utf-8")
        (self.fixture_root / "copied-host-prompt.md").write_text(
            canonical, encoding="utf-8"
        )
        result = self.run_validator("skill")
        self.assert_named_failure(result, "CANONICAL_DUPLICATE_LOGIC")

    def test_malformed_skill_fails_skill_scope(self) -> None:
        path = self.fixture_root / "skills" / "strategic-advisor" / "SKILL.md"
        path.write_text(
            "---\nname strategic-advisor\ndescription: malformed fixture\n---\n# Invalid\n",
            encoding="utf-8",
        )
        result = self.run_validator("skill")
        self.assert_named_failure(result, "SKILL_FRONTMATTER_INVALID")

    def test_extra_skill_frontmatter_fails_skill_scope(self) -> None:
        path = self.fixture_root / "skills" / "strategic-advisor" / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "name: strategic-advisor\n",
            "name: strategic-advisor\nlicense: Apache-2.0\n",
            1,
        )
        path.write_text(text, encoding="utf-8")
        result = self.run_validator("skill")
        self.assert_named_failure(result, "SKILL_FRONTMATTER_INVALID")

    def test_copied_codex_adapter_fails_skill_scope(self) -> None:
        adapter = self.fixture_root / ".agents" / "skills" / "strategic-advisor"
        adapter.unlink()
        shutil.copytree(
            self.fixture_root / "skills" / "strategic-advisor",
            adapter,
        )
        result = self.run_validator("skill")
        self.assert_named_failure(result, "SKILL_ADAPTER_INVALID")

    def test_broken_internal_link_fails_links_scope(self) -> None:
        path = self.fixture_root / "README.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\n[Broken fixture](missing-artifact.md)\n",
            encoding="utf-8",
        )
        result = self.run_validator("links")
        self.assert_named_failure(result, "LINK_BROKEN")

    def test_invalid_evaluation_metadata_fails_evals_scope(self) -> None:
        path = (
            self.fixture_root
            / "skills"
            / "strategic-advisor"
            / "evals"
            / "invalid-fixture.json"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('{"schema_version": 1, "cases": "invalid"}', encoding="utf-8")
        result = self.run_validator("evals")
        self.assert_named_failure(result, "EVALS_INVALID_METADATA")

    def test_stale_combined_inventory_fails_evals_scope(self) -> None:
        path = (
            self.fixture_root
            / "skills"
            / "strategic-advisor"
            / "evals"
            / "core_cases.json"
        )
        inventory = json.loads(path.read_text(encoding="utf-8"))
        inventory["cases"][0]["prompt"] += " Synthetic mutation."
        path.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
        result = self.run_validator("evals")
        self.assert_named_failure(result, "EVALS_COMBINED_STALE")

    def test_missing_core_probe_fails_evals_scope(self) -> None:
        path = (
            self.fixture_root
            / "skills"
            / "strategic-advisor"
            / "evals"
            / "core_cases.json"
        )
        inventory = json.loads(path.read_text(encoding="utf-8"))
        for case in inventory["cases"]:
            case["probe_tags"] = [
                tag for tag in case["probe_tags"] if tag != "prompt_injection"
            ]
        path.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
        result = self.run_validator("evals")
        self.assert_named_failure(result, "EVALS_COVERAGE")

    def test_noncanonical_lens_claim_status_fails_lenses_scope(self) -> None:
        path = (
            self.fixture_root
            / "skills"
            / "strategic-advisor"
            / "evals"
            / "lens_cases.json"
        )
        inventory = json.loads(path.read_text(encoding="utf-8"))
        inventory["cases"][0]["expected_claim_statuses"][0]["status"] = "reported"
        path.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
        result = self.run_validator("lenses")
        self.assert_named_failure(result, "EVALS_INVALID_METADATA")

    def test_missing_lens_readiness_target_fails_lenses_scope(self) -> None:
        path = (
            self.fixture_root
            / "skills"
            / "strategic-advisor"
            / "evals"
            / "lens_cases.json"
        )
        inventory = json.loads(path.read_text(encoding="utf-8"))
        inventory["cases"][0]["readiness_target"] = ""
        path.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
        result = self.run_validator("lenses")
        self.assert_named_failure(result, "EVALS_READINESS_TARGET_INVALID")

    def test_text_only_observation_expectation_fails_lenses_scope(self) -> None:
        path = (
            self.fixture_root
            / "skills"
            / "strategic-advisor"
            / "evals"
            / "lens_cases.json"
        )
        inventory = json.loads(path.read_text(encoding="utf-8"))
        inventory["cases"][0]["expected_claim_statuses"][0]["status"] = "Observation"
        path.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
        result = self.run_validator("lenses")
        self.assert_named_failure(result, "EVALS_PROVENANCE_INVALID")

    def test_invalid_trigger_inventory_fails_evals_scope(self) -> None:
        path = (
            self.fixture_root
            / "skills"
            / "strategic-advisor"
            / "evals"
            / "eval_queries.json"
        )
        path.write_text('[{"query": "only one", "should_trigger": true}]\n', encoding="utf-8")
        result = self.run_validator("evals")
        self.assert_named_failure(result, "EVALS_TRIGGER_INVALID")

    def test_missing_difficult_trigger_slices_fails_evals_scope(self) -> None:
        path = (
            self.fixture_root
            / "skills"
            / "strategic-advisor"
            / "evals"
            / "eval_queries.json"
        )
        inventory = json.loads(path.read_text(encoding="utf-8"))
        for item in inventory:
            item.pop("slice", None)
        path.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
        result = self.run_validator("evals")
        self.assert_named_failure(result, "EVALS_TRIGGER_INVALID")

    def test_incomplete_freeze_authority_fails_evals_scope(self) -> None:
        path = (
            self.fixture_root
            / "skills"
            / "strategic-advisor"
            / "evals"
            / "freeze-manifest.template.json"
        )
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["authority_files"] = [
            item
            for item in manifest["authority_files"]
            if item["path"] != "skills/strategic-advisor/evals/AGGREGATION.md"
        ]
        path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        result = self.run_validator("evals")
        self.assert_named_failure(result, "EVALS_FREEZE_AUTHORITY_INVALID")

    def test_weak_freeze_controls_fail_evals_scope(self) -> None:
        path = (
            self.fixture_root
            / "skills"
            / "strategic-advisor"
            / "evals"
            / "freeze-manifest.template.json"
        )
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["generation"]["treatment_activation"] = {}
        manifest["sealed_holdout"]["required"] = False
        path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        result = self.run_validator("evals")
        self.assert_named_failure(result, "EVALS_FREEZE_CONTROLS_INVALID")

    def test_wrong_bootstrap_collection_fails_evals_scope(self) -> None:
        path = (
            self.fixture_root
            / "skills"
            / "strategic-advisor"
            / "evals"
            / "AGGREGATION.md"
        )
        text = path.read_text(encoding="utf-8").replace(
            "select `clusters[u mod C]`",
            "select `cases[u mod C]`",
            1,
        )
        path.write_text(text, encoding="utf-8")
        result = self.run_validator("evals")
        self.assert_named_failure(result, "EVALS_AGGREGATION_INVALID")

    def test_scorer_selected_applicability_fails_evals_scope(self) -> None:
        path = (
            self.fixture_root
            / "skills"
            / "strategic-advisor"
            / "evals"
            / "freeze-manifest.template.json"
        )
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["aggregation"]["n_a_policy"] = (
            "The scorer may select not-applicable dimensions after reading the responses."
        )
        path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        result = self.run_validator("evals")
        self.assert_named_failure(result, "EVALS_APPLICABILITY_AUTHORITY_INVALID")

    def test_forged_evaluation_status_fails_evals_scope(self) -> None:
        path = self.fixture_root / "evidence" / "evaluations" / "status.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        status = json.loads(
            (REPOSITORY_ROOT / "evidence/evaluations/status.json").read_text(
                encoding="utf-8"
            )
        )
        status["release_gate"] = "passed"
        path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
        result = self.run_validator("evals")
        self.assert_named_failure(result, "EVALS_STATUS_DRIFT")

    def test_private_context_field_fails_pilot_registry_scope(self) -> None:
        path = self.fixture_root / "pilots" / "registry.json"
        registry = json.loads(path.read_text(encoding="utf-8"))
        registry["status"] = "pilots-enrolled"
        registry["entries"] = [
            {
                "pilot_id": "PILOT-AB12CD34",
                "domain": "project-product",
                "registered_at": "2026-07-22T00:00:00Z",
                "eligibility_status": "eligible",
                "eligibility_reason_code": "synthetic-fixture",
                "consent_status": "granted",
                "consent_reference": "external:fixture",
                "terminal_status": "preregistered",
                "public_record": None,
                "run_manifest": None,
                "case_owner_name": "Private Fixture",
            }
        ]
        path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        result = self.run_validator("pilots")
        self.assert_named_failure(result, "PILOTS_REGISTRY_INVALID")

    def test_evaluation_file_in_runtime_allowlist_fails_evals_scope(self) -> None:
        path = (
            self.fixture_root
            / "skills"
            / "strategic-advisor"
            / "runtime-manifest.json"
        )
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["include"].append("evals/core_cases.json")
        path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        result = self.run_validator("evals")
        self.assert_named_failure(result, "PACKAGING_EVAL_LEAK")


if __name__ == "__main__":
    unittest.main()
