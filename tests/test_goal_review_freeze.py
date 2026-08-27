from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPOSITORY_ROOT / "scripts" / "build_goal_review_freeze.py"
spec = importlib.util.spec_from_file_location("goal_review_freeze", TOOL)
if spec is None or spec.loader is None:
    raise RuntimeError("could not load goal-review freeze tool")
freeze = importlib.util.module_from_spec(spec)
spec.loader.exec_module(freeze)


class GoalReviewFreezeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.authority = freeze.read_json(REPOSITORY_ROOT / freeze.AUTHORITY_FILE)

    def test_current_freeze_is_complete_and_runtime_excluded(self) -> None:
        document = freeze.build_document(REPOSITORY_ROOT)
        self.assertEqual(document["case_count"], 20)
        self.assertGreaterEqual(document["criterion_count"], 25)
        self.assertTrue(document["runtime_exclusion"])
        self.assertEqual(document["proof_layer"], "exact-runtime-synthetic")
        self.assertIn("does not establish", document["applicability"])
        self.assertEqual(set(document["categories"]), freeze.EXPECTED_CATEGORIES)
        self.assertEqual(document["stateful_case_ids"], ["SAGR-007", "SAGR-008"])
        self.assertEqual(document["state_assertion_count"], 3)
        self.assertEqual(set(document["control_pairs"]), freeze.EXPECTED_CONTROL_PAIRS)

    def test_duplicate_case_id_fails(self) -> None:
        authority = copy.deepcopy(self.authority)
        authority["cases"][1]["id"] = authority["cases"][0]["id"]
        with self.assertRaisesRegex(freeze.FreezeError, "case IDs differ"):
            freeze.validate_authority(authority)

    def test_missing_category_fails(self) -> None:
        authority = copy.deepcopy(self.authority)
        authority["required_categories"].pop()
        with self.assertRaisesRegex(freeze.FreezeError, "required_categories differ"):
            freeze.validate_authority(authority)

    def test_unknown_review_turn_fails(self) -> None:
        authority = copy.deepcopy(self.authority)
        authority["cases"][0]["criteria"][0]["review_turns"] = ["T99"]
        with self.assertRaisesRegex(freeze.FreezeError, "unknown review turn"):
            freeze.validate_authority(authority)

    def test_reversed_multi_turn_order_fails(self) -> None:
        authority = copy.deepcopy(self.authority)
        authority["cases"][6]["turns"].reverse()
        with self.assertRaisesRegex(freeze.FreezeError, "turns must be ordered"):
            freeze.validate_authority(authority)

    def test_placeholder_criterion_fails(self) -> None:
        authority = copy.deepcopy(self.authority)
        authority["cases"][0]["criteria"][0]["requirement"] = "x"
        with self.assertRaisesRegex(freeze.FreezeError, "at least 60 characters"):
            freeze.validate_authority(authority)

    def test_missing_state_assertion_fails(self) -> None:
        authority = copy.deepcopy(self.authority)
        authority["cases"][6]["state_assertions"].pop()
        with self.assertRaisesRegex(freeze.FreezeError, "state assertions differ"):
            freeze.validate_authority(authority)

    def test_control_pair_membership_is_fixed(self) -> None:
        authority = copy.deepcopy(self.authority)
        authority["control_pairs"][0]["case_ids"].reverse()
        with self.assertRaisesRegex(freeze.FreezeError, "case_ids differ"):
            freeze.validate_authority(authority)


if __name__ == "__main__":
    unittest.main()
