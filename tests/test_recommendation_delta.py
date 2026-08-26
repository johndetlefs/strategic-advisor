from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "recommendation_delta", ROOT / "scripts" / "recommendation_delta.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def provenance(status: str = "reported") -> dict[str, str]:
    return {"source": "public-synthetic fixture", "status": status}


def base_state(turn_kind: str = "material-recommendation") -> dict:
    return {
        "schema_version": 1,
        "turn_kind": turn_kind,
        "confirmed_outcome": {"claim": "Improve completed handoffs", "provenance": provenance("confirmed")},
        "unacceptable_substitutes": ["More architectural structure without outcome proof"],
        "claims": [
            {"id": "bridge", "statement": "Shared ownership causes the handoff failures", "status": "assumption", "provenance": provenance()},
            {"id": "small-rival", "statement": "A smaller explicit handoff contract could resolve the observed gap", "status": "evidence", "provenance": provenance("observed")},
            {"id": "replacement-spec", "statement": "A single orchestrator could centralise routing", "status": "candidate-specification", "provenance": provenance("proposed")},
            {"id": "replacement-outcome", "statement": "A bounded pilot improved handoff completion", "status": "evidence", "provenance": provenance("observed")},
        ],
        "constraints": [{"id": "reversible", "statement": "The next move must be reversible", "provenance": provenance("confirmed")}],
        "candidates": [
            {"id": "contract", "specification": "Explicit handoff contract", "support_claim_ids": ["small-rival"]},
            {"id": "orchestrator", "specification": "Single orchestrator", "support_claim_ids": []},
        ],
        "recommendation": {
            "candidate_id": "contract",
            "dependent_claim_ids": ["bridge", "small-rival"],
            "next_move": "Test the handoff contract",
            "qualification": "Test the smaller rival before architecture change",
            "readiness": "conditional",
        },
        "strongest_rival": {"candidate_id": "contract", "dependent_claim_ids": ["small-rival"], "reason": "It directly targets the observed gap with less exposure"},
    }


def delta(*, kinds: list[str], support: list[str] | None = None, readiness: str = "ready") -> dict:
    return {
        "schema_version": 1,
        "changed_inputs": [{"id": f"change-{index}", "kind": kind, "provenance": provenance()} for index, kind in enumerate(kinds)],
        "falsified_claim_ids": ["bridge"],
        "affected_claim_ids": ["bridge"],
        "retracted_claim_ids": ["bridge"],
        "surviving_claim_ids": ["small-rival"],
        "replacement_candidate_id": "orchestrator",
        "replacement_support_claim_ids": support or [],
        "proposed_recommendation": {"candidate_id": "orchestrator", "qualification": "Adopt the orchestrator", "readiness": readiness},
    }


class RecommendationDeltaTests(unittest.TestCase):
    def test_closed_state_rejects_unknown_and_missing_fields(self) -> None:
        for mutate in (lambda value: value.update({"unknown": True}), lambda value: value.pop("strongest_rival")):
            value = base_state()
            mutate(value)
            with self.assertRaises(MODULE.ContractError):
                MODULE.validate_state(value)

    def test_proposal_and_failed_bridge_do_not_support_replacement(self) -> None:
        result = MODULE.evaluate(base_state(), delta(kinds=["candidate-specification"], readiness="ready"))
        self.assertEqual(result.decision, "revise")
        self.assertIn(result.reason_codes[0], {"no_qualifying_delta", "specification_not_outcome_evidence", "replacement_support_missing"})

    def test_false_converse_cannot_retract_surviving_rival(self) -> None:
        value = delta(kinds=["evidence"], support=["replacement-outcome"])
        value["affected_claim_ids"].append("small-rival")
        value["retracted_claim_ids"].append("small-rival")
        value["surviving_claim_ids"].remove("small-rival")
        result = MODULE.evaluate(base_state(), value)
        self.assertEqual(result.decision, "revise")
        self.assertEqual(result.reason_codes, ("false_converse_or_over_retraction",))

    def test_preference_and_repetition_do_not_change_recommendation(self) -> None:
        result = MODULE.evaluate(base_state(), delta(kinds=["preference", "repetition"]))
        self.assertEqual(result.decision, "revise")
        self.assertEqual(result.reason_codes, ("no_qualifying_delta",))

    def test_legitimate_evidence_can_change_recommendation(self) -> None:
        result = MODULE.evaluate(base_state(), delta(kinds=["evidence"], support=["replacement-outcome"]))
        self.assertEqual(result.decision, "pass")
        self.assertEqual(result.reason_codes, ("qualifying_delta",))

    def test_routine_and_open_exploration_bypass_without_delta(self) -> None:
        for kind in ("routine-direct", "open-exploration"):
            with self.subTest(kind=kind):
                result = MODULE.evaluate(base_state(kind))
                self.assertEqual(result.activation, "bypass")
                self.assertEqual(result.decision, "pass")

    def test_bypass_rejects_hidden_delta(self) -> None:
        with self.assertRaisesRegex(MODULE.ContractError, "must not construct"):
            MODULE.evaluate(base_state("routine-direct"), delta(kinds=["evidence"]))

    def test_unknown_claim_reference_fails_closed(self) -> None:
        value = delta(kinds=["evidence"], support=["missing"])
        with self.assertRaises(MODULE.ContractError):
            MODULE.evaluate(base_state(), value)


if __name__ == "__main__":
    unittest.main()
