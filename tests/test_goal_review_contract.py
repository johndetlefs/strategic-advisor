from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "strategic-advisor"
AUTHORITY = (
    ROOT
    / ".project-workflow/tasks/EPIC-007-Strategic-Alignment-And-Goal-Review-Control"
    / "TASK-031-Freeze-Combined-Contract-And-Behaviour-Baseline/CASE-AUTHORITY.json"
)


def read(relative: str) -> str:
    return (SKILL_ROOT / relative).read_text(encoding="utf-8")


def compact(text: str) -> str:
    return " ".join(text.split())


class GoalReviewContractTests(unittest.TestCase):
    def test_runtime_links_one_goal_review_contract(self) -> None:
        skill = read("SKILL.md")
        manifest = json.loads(read("runtime-manifest.json"))
        self.assertEqual(skill.count("references/goal-review.md"), 1)
        self.assertEqual(manifest["include"].count("references/goal-review.md"), 1)

    def test_event_weekly_and_monthly_purposes_are_distinct(self) -> None:
        contract = read("references/goal-review.md")
        for marker in (
            "**Event review** pre-empts the schedule",
            "**Weekly pulse** is a configurable execution review",
            "**Monthly portfolio review** is a configurable goal-and-allocation review",
            "operating conventions, not universal laws",
        ):
            self.assertIn(marker, contract)

    def test_material_progress_and_enabler_credit_reject_activity(self) -> None:
        contract = read("references/goal-review.md")
        for marker in (
            "**Outcome movement**",
            "**Driver movement**",
            "**Constraint movement**",
            "**Decision movement**",
            "non-advancing effort/output",
            "enabled but not yet advanced",
            "Completion of the enabler never proves",
        ):
            self.assertIn(marker, contract)

    def test_drift_and_amendment_burden_preserve_and_permit_change(self) -> None:
        contract = compact(read("references/goal-review.md"))
        for marker in (
            "execution friction",
            "nor failure of one mechanism proves that the goal should change",
            "Apply the amendment burden of proof",
            "Challenge an unsupported amendment",
            "Prior approval does not make a goal immutable",
        ):
            self.assertIn(marker, contract)

    def test_goal_and_path_dispositions_and_record_fields_are_complete(self) -> None:
        contract = read("references/goal-review.md")
        for disposition in ("Continue", "Correct", "Pivot", "Pause", "Replace", "Stop"):
            self.assertIn(f"**{disposition}**", contract)
        for field in (
            "Review identity",
            "Authority",
            "Goal state",
            "Path state",
            "Evidence",
            "Non-progress",
            "Drift/amendment",
            "Goal decision",
            "Path decision",
            "Follow-through",
            "Reversal and review",
            "Closeout",
        ):
            self.assertIn(f"| {field} |", contract)

    def test_owner_reconciliation_preserves_provenance_and_absence_boundary(self) -> None:
        contract = read("references/goal-review.md")
        self.assertIn("dated owner report", contract)
        self.assertIn("Absence from an execution system is not evidence", contract)
        self.assertIn("preserve both claims", contract)

    def test_process_falsifiers_change_the_process_without_removing_event_gate(self) -> None:
        contract = compact(read("references/goal-review.md"))
        for marker in (
            "repeated reviews cannot change a decision",
            "preparation and discussion cost exceeds",
            "scheduled review delays an event-triggered",
            "Stop a scheduled review",
            "retaining the event exception gate",
        ):
            self.assertIn(marker, contract)

    def test_public_contract_is_consumer_independent_and_private_data_free(self) -> None:
        contract = compact(read("references/goal-review.md"))
        lowered = contract.lower()
        for forbidden in (
            "john",
            "daily checklist",
            "sunday automation",
            "every sunday",
            "must run weekly",
            "accountability partner",
        ):
            self.assertNotIn(forbidden, lowered)
        self.assertIn("owner-authorised private Strategy Workspace", contract)
        self.assertIn("does not become the strategic authority", contract)

    def test_existing_workspace_schema_remains_eight_files(self) -> None:
        contract = read("references/strategy-workspace.md")
        self.assertIn("exactly eight core files", contract)
        self.assertNotIn("REVIEWS.md", contract)
        self.assertIn("goal-review.md", contract)

    def test_every_frozen_task033_category_has_a_canonical_marker(self) -> None:
        cases = json.loads(AUTHORITY.read_text(encoding="utf-8"))["cases"][13:20]
        categories = {case["category"] for case in cases}
        expected = {
            "material-progress",
            "unjustified-goal-change",
            "justified-goal-change",
            "event-exception-review",
            "weekly-monthly-disposition",
            "owner-reconciliation",
            "process-waste-falsifier",
        }
        self.assertEqual(categories, expected)
        contract = read("references/goal-review.md")
        markers = {
            "material-progress": "Apply the material-progress test",
            "unjustified-goal-change": "Test drift before accepting change",
            "justified-goal-change": "Apply the amendment burden of proof",
            "event-exception-review": "**Event review** pre-empts the schedule",
            "weekly-monthly-disposition": "Record two separate dispositions",
            "owner-reconciliation": "Absence from an execution system is not evidence",
            "process-waste-falsifier": "Falsify the review process itself",
        }
        for category, marker in markers.items():
            with self.subTest(category=category):
                self.assertIn(marker, contract)


if __name__ == "__main__":
    unittest.main()
