from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EVAL_ROOT = REPOSITORY_ROOT / "skills" / "strategic-advisor" / "evals"


def read(name: str) -> str:
    return (EVAL_ROOT / name).read_text(encoding="utf-8")


def first_json_block(name: str) -> dict:
    match = re.search(r"```json\n(.*?)\n```", read(name), flags=re.DOTALL)
    if match is None:
        raise AssertionError(f"{name} does not contain a JSON contract")
    parsed = json.loads(match.group(1))
    if not isinstance(parsed, dict):
        raise AssertionError(f"{name} JSON contract is not an object")
    return parsed


class OptionAAuthorityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.protocol = read("PROTOCOL.md")
        self.rubric = read("RUBRIC.md")
        self.scorer = read("SCORER-PROMPT.md")
        self.aggregation = read("AGGREGATION.md")
        self.auditor = read("CONDITION-AUDITOR-PROMPT.md")
        self.freeze = json.loads(read("freeze-manifest.template.json"))

    def test_quality_scorer_schema_has_no_condition_identity_output(self) -> None:
        schema = first_json_block("SCORER-PROMPT.md")
        self.assertEqual(schema["schema_version"], "strategic-advisor-scorer-v2")
        self.assertNotIn("condition_guess", schema)
        self.assertNotIn("likely_skilled", schema)
        self.assertNotIn("condition_guess", self.scorer)
        self.assertNotIn("likely_skilled", self.scorer)
        self.assertIn("Apparent condition is not quality evidence", self.scorer)

    def test_quality_passes_are_inverse_same_family_repeated_evidence(self) -> None:
        masking = self.freeze["masking"]
        scoring = self.freeze["scoring"]
        self.assertEqual(
            masking["quality_pass_label_algorithm"],
            "inverse-ab-quality-pass-v1",
        )
        self.assertEqual(
            scoring["pass_relationship"],
            "same-family-repeated-evidence-not-independent-judges",
        )
        self.assertEqual(scoring["pass_ids"], ["score-1", "score-2"])
        self.assertIn("score-1 presents base A as A", masking["quality_pass_label_rule"])
        self.assertIn("score-2 presents base B as A", masking["quality_pass_label_rule"])
        self.assertIn("score-2.A to base B", masking["quality_normalization_rule"])
        self.assertIn("They are repeated evidence", self.protocol)
        self.assertIn("not independent judges", self.protocol)
        self.assertIn("not independent judges", self.rubric)
        self.assertIn("score-2.A` to base `B`", self.protocol)

    def test_condition_audit_prompt_and_configuration_are_frozen(self) -> None:
        authority_paths = [item["path"] for item in self.freeze["authority_files"]]
        auditor_path = (
            "skills/strategic-advisor/evals/CONDITION-AUDITOR-PROMPT.md"
        )
        self.assertEqual(authority_paths.count(auditor_path), 1)
        self.assertTrue((REPOSITORY_ROOT / auditor_path).is_file())

        audit = self.freeze["condition_audit"]
        self.assertEqual(self.freeze["schema_version"], 3)
        self.assertEqual(audit["mode_ids"], ["structure-only", "full-response"])
        self.assertEqual(audit["passes_per_mode_per_pair"], 1)
        self.assertIn("model", audit)
        self.assertIn("model_version", audit)
        self.assertIn("host", audit)
        self.assertIn("configuration", audit)
        self.assertIn("prompt_sha256", audit)
        self.assertEqual(
            audit["structure_view"]["algorithm_id"], "structure-view-v1"
        )
        self.assertEqual(
            self.freeze["masking"]["audit_mapping_algorithm"],
            "hmac-sha256-condition-audit-map-v1",
        )
        self.assertEqual(
            audit["fresh_context_identity"]["key_fields"],
            ["case_id", "draw_id", "audit_mode", "attempt_id"],
        )

        auditor_schema = first_json_block("CONDITION-AUDITOR-PROMPT.md")
        self.assertEqual(
            auditor_schema["schema_version"],
            "strategic-advisor-condition-auditor-v1",
        )
        self.assertEqual(auditor_schema["audit_mode"], "structure-only")
        self.assertIn("structure-only", self.auditor)
        self.assertIn("full-response", self.auditor)

    def test_structure_only_is_physically_isolated_and_is_the_only_gate(self) -> None:
        audit = self.freeze["condition_audit"]
        self.assertEqual(audit["structure_only_gate"]["minimum_determinate"], 20)
        self.assertEqual(audit["structure_only_gate"]["failure_accuracy_gte"], 0.7)
        self.assertIn("descriptive", audit["full_response_policy"])
        self.assertIn("cannot pass, fail", audit["full_response_policy"])

        self.assertIn("physically exclude lexical response content", self.protocol)
        self.assertIn("structure-view-v1", self.protocol)
        self.assertIn("sole condition-identifiability result used by the release gate", self.protocol)
        self.assertIn("report `full-response` separately without a gating verdict", self.protocol)
        self.assertIn("sole identifiability mode used by the release gate", self.rubric)
        self.assertIn("Full-response identifiability", self.rubric)
        self.assertIn("has no release-gating threshold", self.rubric)
        self.assertIn("systematic_structure_only_condition_leakage", self.aggregation)
        self.assertIn("`gating_verdict: null`", self.aggregation)

    def test_aggregation_normalizes_before_resolution_and_fails_closed(self) -> None:
        self.assertIn("score-2.A` becomes base B", self.aggregation)
        self.assertIn("score-2.B` becomes base A", self.aggregation)
        self.assertIn("before comparing scores", self.aggregation)
        self.assertIn(
            "missing or errored required `structure-only` or `full-response` condition-audit artifact",
            self.aggregation,
        )
        self.assertIn(
            "structure-only audit input containing lexical response content",
            self.aggregation,
        )
        self.assertNotIn("missing scorer pass, condition guess", self.aggregation)
        self.assertIn(
            "quality_scorer_prompt_sha256",
            self.freeze["result_reference_requirements"]["record_in_every_run_and_result"],
        )
        self.assertIn(
            "condition_auditor_prompt_sha256",
            self.freeze["result_reference_requirements"]["record_in_every_run_and_result"],
        )
        self.assertIn(
            "structure_view_authority_sha256",
            self.freeze["result_reference_requirements"]["record_in_every_run_and_result"],
        )

    def test_adjudicator_receives_only_normalized_base_labels(self) -> None:
        adjudicator = read("ADJUDICATOR-PROMPT.md")
        self.assertIn("normalized both quality passes", adjudicator)
        self.assertIn("pass 2 A/B outcomes are inversely remapped", adjudicator)
        self.assertIn(
            "normalized to the same base A/base B presentation", adjudicator
        )
        self.assertNotIn("A/B order is unchanged from scoring", adjudicator)


if __name__ == "__main__":
    unittest.main()
