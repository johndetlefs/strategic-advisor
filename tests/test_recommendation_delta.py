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
        "schema_version": 2,
        "turn_kind": turn_kind,
        "stated_request": {"claim": "Adopt shared ownership", "provenance": provenance("reported")},
        "confirmed_outcome": {"claim": "Improve completed handoffs", "provenance": provenance("confirmed")},
        "unacceptable_substitutes": ["More architectural structure without outcome proof"],
        "decision_altitude": "project-outcome",
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
        "objects": [
            {"id": "handoff-outcome", "statement": "Improve completed handoffs", "class": "end", "provenance": provenance("confirmed")},
            {"id": "shared-ownership", "statement": "Adopt shared ownership", "class": "means", "provenance": provenance("proposed")},
        ],
        "goal_purpose": {
            "class": "operational",
            "statement": "Improve completed handoffs this quarter",
            "horizon": "this quarter",
            "learning_outcome": None,
            "falsifier": "Handoff completion does not improve under the tested contract",
            "unlocked_decision": None,
            "provenance": provenance("confirmed"),
        },
        "causal_bridge": {
            "candidate_id": "contract",
            "statement": "An explicit handoff contract reduces ownership ambiguity",
            "status": "conditional",
            "evidence_claim_ids": ["small-rival"],
            "falsifier": "The observed handoff gap persists under the explicit contract",
            "provenance": provenance("inferred"),
        },
        "material_uncertainties": [],
        "owner_settled_state": {"version": 1, "status": "confirmed", "provenance": provenance("owner-confirmed")},
        "reopening_evidence_claim_ids": [],
        "recommendation": {
            "candidate_id": "contract",
            "dependent_claim_ids": ["bridge", "small-rival"],
            "next_move": "Test the handoff contract",
            "qualification": "Test the smaller rival before architecture change",
            "readiness": "Conditional",
        },
        "strongest_rival": {"candidate_id": "contract", "dependent_claim_ids": ["small-rival"], "reason": "It directly targets the observed gap with less exposure"},
    }


def delta(*, kinds: list[str], support: list[str] | None = None, readiness: str = "Ready") -> dict:
    return {
        "schema_version": 2,
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
        result = MODULE.evaluate(base_state(), delta(kinds=["candidate-specification"], readiness="Ready"))
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

    def test_unaffected_recommendation_or_rival_dependency_cannot_disappear(self) -> None:
        value = delta(kinds=["evidence"], support=["replacement-outcome"])
        value["surviving_claim_ids"].remove("small-rival")
        with self.assertRaisesRegex(
            MODULE.ContractError,
            "unaffected recommendation and rival dependencies must be recorded as surviving",
        ):
            MODULE.evaluate(base_state(), value)

    def test_claim_cannot_be_both_falsified_and_surviving(self) -> None:
        value = delta(kinds=["evidence"], support=["replacement-outcome"])
        value["affected_claim_ids"].append("small-rival")
        value["falsified_claim_ids"].append("small-rival")
        with self.assertRaisesRegex(MODULE.ContractError, "both survive and be falsified"):
            MODULE.evaluate(base_state(), value)

    def test_falsified_claim_must_be_affected(self) -> None:
        value = delta(kinds=["evidence"], support=["replacement-outcome"])
        value["falsified_claim_ids"].append("small-rival")
        with self.assertRaisesRegex(MODULE.ContractError, "falsified claims must be affected"):
            MODULE.evaluate(base_state(), value)

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

    def test_unconfirmed_and_reopened_outcome_is_representable(self) -> None:
        value = base_state()
        value["confirmed_outcome"] = None
        value["recommendation"]["readiness"] = "Not validated"
        value["owner_settled_state"] = {
            "version": 2,
            "status": "reopened",
            "provenance": provenance("evidence-triggered"),
        }
        value["reopening_evidence_claim_ids"] = ["small-rival"]
        value["material_uncertainties"] = [
            {
                "id": "outcome-fork",
                "question": "Is the intended result fewer handoffs or more completed handoffs?",
                "action_candidate_ids": ["contract", "orchestrator"],
                "provenance": provenance("inferred"),
            }
        ]
        self.assertEqual(MODULE.validate_state(value), value)

    def test_confirmed_owner_state_requires_confirmed_outcome(self) -> None:
        value = base_state()
        value["confirmed_outcome"] = None
        with self.assertRaisesRegex(MODULE.ContractError, "requires a confirmed outcome"):
            MODULE.validate_state(value)

    def test_unconfirmed_outcome_cannot_launder_execution_readiness(self) -> None:
        value = base_state()
        value["confirmed_outcome"] = None
        value["owner_settled_state"] = {
            "version": 1,
            "status": "unresolved",
            "provenance": provenance("pending-owner-answer"),
        }
        with self.assertRaisesRegex(MODULE.ContractError, "cannot support execution readiness"):
            MODULE.validate_state(value)

    def test_reopened_state_requires_named_reopening_evidence(self) -> None:
        value = base_state()
        value["owner_settled_state"] = {
            "version": 2,
            "status": "reopened",
            "provenance": provenance("evidence-triggered"),
        }
        with self.assertRaisesRegex(MODULE.ContractError, "requires reopening evidence"):
            MODULE.validate_state(value)

    def test_all_object_classes_are_distinct_from_readiness(self) -> None:
        value = base_state()
        value["objects"] = [
            {
                "id": object_class,
                "statement": f"Synthetic {object_class}",
                "class": object_class,
                "provenance": provenance(),
            }
            for object_class in sorted(MODULE.OBJECT_CLASSES)
        ]
        value["recommendation"]["readiness"] = "Infeasible as posed"
        self.assertEqual(MODULE.validate_state(value), value)

    def test_discovery_goal_requires_complete_learning_contract(self) -> None:
        value = base_state()
        value["goal_purpose"] = {
            "class": "discovery",
            "statement": "Learn whether the route changes the outcome",
            "horizon": "two weeks",
            "learning_outcome": "Observe whether the route changes completed handoffs",
            "falsifier": "No relevant change under the bounded test",
            "unlocked_decision": "Whether to stage the route",
            "provenance": provenance("approved"),
        }
        MODULE.validate_state(value)
        value["goal_purpose"]["unlocked_decision"] = None
        with self.assertRaisesRegex(MODULE.ContractError, "discovery goal requires"):
            MODULE.validate_state(value)

    def test_bridge_and_reopening_references_fail_closed(self) -> None:
        for field in ("causal_bridge", "reopening"):
            with self.subTest(field=field):
                value = base_state()
                if field == "causal_bridge":
                    value["causal_bridge"]["evidence_claim_ids"] = ["missing"]
                else:
                    value["reopening_evidence_claim_ids"] = ["missing"]
                with self.assertRaises(MODULE.ContractError):
                    MODULE.validate_state(value)


if __name__ == "__main__":
    unittest.main()
