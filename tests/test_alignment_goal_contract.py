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


class AlignmentGoalContractTests(unittest.TestCase):
    def test_runtime_links_one_goal_qualification_contract(self) -> None:
        skill = read("SKILL.md")
        manifest = json.loads(read("runtime-manifest.json"))
        self.assertEqual(skill.count("references/goal-qualification.md"), 1)
        self.assertEqual(manifest["include"].count("references/goal-qualification.md"), 1)

    def test_alignment_requires_action_changing_ambiguity(self) -> None:
        contract = read("references/conversational-strategy.md")
        for text in (
            "bounded reconnaissance",
            "materially different actions",
            "same robust move",
            "research first",
            "owner-only outcomes",
        ):
            self.assertIn(text, contract)

    def test_reclarification_preserves_valid_state_selectively(self) -> None:
        contract = read("references/conversational-strategy.md")
        for text in (
            "both conditions hold",
            "owner-settled",
            "Preserve the state version",
            "Invalidate and redo",
            "only dependent research",
            "do not repeat the resolved question",
        ):
            self.assertIn(text, contract)

    def test_goal_object_purpose_and_readiness_are_separate(self) -> None:
        contract = read("references/goal-qualification.md")
        for object_class in ("End", "Means", "Proxy", "Metric", "Project", "Tool", "Task"):
            self.assertIn(f"**{object_class}**", contract)
        for purpose in ("Aspiration", "Discovery goal", "Operational goal"):
            self.assertIn(f"**{purpose}**", contract)
        for readiness in ("Not validated", "Conditional", "Infeasible as posed"):
            self.assertIn(readiness, contract)
        self.assertIn("Goal purpose never replaces the four readiness states", contract)

    def test_discovery_and_indicator_contracts_are_complete(self) -> None:
        contract = read("references/goal-qualification.md")
        for text in (
            "learning outcome, horizon, falsifier, and decision",
            "predictor, causal driver, constraint measure, or activity",
            "Evenly dividing a final target",
            "arithmetic, not a causal plan",
        ):
            self.assertIn(text, contract)

    def test_recurring_review_logic_is_not_implemented_here(self) -> None:
        contract = read("references/goal-qualification.md").lower()
        self.assertNotIn("weekly pulse", contract)
        self.assertNotIn("monthly portfolio", contract)
        self.assertNotIn("sunday automation", contract)

    def test_every_frozen_task032_category_has_a_canonical_contract_marker(self) -> None:
        categories = [case["category"] for case in json.loads(AUTHORITY.read_text())["cases"][:13]]
        markers = {
            "routine-direct-assistance": ("references/conversational-strategy.md", "Direct assistance should look like direct assistance"),
            "bounded-reconnaissance": ("references/conversational-strategy.md", "Do enough bounded reconnaissance"),
            "initial-alignment": ("references/conversational-strategy.md", "### Initial alignment gate"),
            "same-robust-move": ("references/conversational-strategy.md", "same robust move"),
            "evidence-resolvable-fork": ("references/conversational-strategy.md", "research first"),
            "owner-value-fork": ("references/conversational-strategy.md", "owner-only outcomes"),
            "evidence-triggered-reclarification": ("references/conversational-strategy.md", "### Evidence-triggered re-clarification"),
            "selective-invalidation": ("references/conversational-strategy.md", "Invalidate and redo"),
            "goal-proxy-ladder": ("references/goal-qualification.md", "## Move up before moving down"),
            "aspiration-handling": ("references/goal-qualification.md", "**Aspiration**"),
            "discovery-goal": ("references/goal-qualification.md", "**Discovery goal**"),
            "operational-goal-readiness": ("references/goal-qualification.md", "**Operational goal**"),
            "causal-leading-indicators": ("references/goal-qualification.md", "## Prevent indicator and milestone laundering"),
        }
        self.assertEqual(set(categories), set(markers))
        for category, (path, marker) in markers.items():
            with self.subTest(category=category):
                self.assertIn(marker, read(path))


if __name__ == "__main__":
    unittest.main()
