#!/usr/bin/env python3
"""Validate a typed Strategic Advisor decision state and recommendation delta.

This helper checks a closed, public contract. It does not infer facts from prose
or claim that structurally valid input is true.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 2
TURN_KINDS = {"material-recommendation", "routine-direct", "open-exploration"}
READINESS = {"Ready", "Conditional", "Not validated", "Infeasible as posed"}
DECISION_ALTITUDES = {"intervention", "project-outcome", "portfolio", "whole-person"}
OBJECT_CLASSES = {"end", "means", "proxy", "metric", "project", "tool", "task"}
GOAL_PURPOSES = {"aspiration", "discovery", "operational"}
OWNER_SETTLED_STATES = {"unresolved", "confirmed", "reopened"}
CAUSAL_BRIDGE_STATES = {"supported", "conditional", "not-validated", "contradicted"}
CLAIM_STATUSES = {
    "evidence",
    "report",
    "preference",
    "assumption",
    "candidate-specification",
}
QUALIFYING_KINDS = {"outcome", "evidence", "framing", "scope", "constraint", "owner-value"}
NONQUALIFYING_KINDS = {"preference", "repetition", "intensity", "rename"}
STATE_KEYS = {
    "causal_bridge",
    "candidates",
    "claims",
    "confirmed_outcome",
    "constraints",
    "decision_altitude",
    "goal_purpose",
    "material_uncertainties",
    "objects",
    "owner_settled_state",
    "recommendation",
    "reopening_evidence_claim_ids",
    "schema_version",
    "stated_request",
    "strongest_rival",
    "turn_kind",
    "unacceptable_substitutes",
}
DELTA_KEYS = {
    "affected_claim_ids",
    "changed_inputs",
    "falsified_claim_ids",
    "proposed_recommendation",
    "replacement_candidate_id",
    "replacement_support_claim_ids",
    "retracted_claim_ids",
    "schema_version",
    "surviving_claim_ids",
}


class ContractError(ValueError):
    pass


@dataclass(frozen=True)
class Evaluation:
    activation: str
    decision: str
    reason_codes: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "activation": self.activation,
            "decision": self.decision,
            "reason_codes": list(self.reason_codes),
            "schema_version": SCHEMA_VERSION,
        }


def _closed_object(value: object, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ContractError(f"{label} fields are invalid")
    return value


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{label} must be non-empty text")
    return value


def _text_list(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ContractError(f"{label} must be a text list")
    if len(value) != len(set(value)):
        raise ContractError(f"{label} contains duplicates")
    return value


def _provenance(value: object, label: str) -> dict[str, str]:
    record = _closed_object(value, {"source", "status"}, label)
    return {"source": _text(record["source"], f"{label}.source"), "status": _text(record["status"], f"{label}.status")}


def _optional_text(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _text(value, label)


def validate_state(value: object) -> dict[str, Any]:
    state = _closed_object(value, STATE_KEYS, "state")
    if state["schema_version"] != SCHEMA_VERSION:
        raise ContractError("state schema version is invalid")
    turn_kind = state["turn_kind"]
    if turn_kind not in TURN_KINDS:
        raise ContractError("turn kind is invalid")

    request = _closed_object(state["stated_request"], {"claim", "provenance"}, "stated request")
    _text(request["claim"], "stated request claim")
    _provenance(request["provenance"], "stated request provenance")

    outcome = state["confirmed_outcome"]
    if outcome is not None:
        outcome = _closed_object(outcome, {"claim", "provenance"}, "confirmed outcome")
        _text(outcome["claim"], "confirmed outcome claim")
        _provenance(outcome["provenance"], "confirmed outcome provenance")
    _text_list(state["unacceptable_substitutes"], "unacceptable substitutes")

    if state["decision_altitude"] not in DECISION_ALTITUDES:
        raise ContractError("decision altitude is invalid")

    owner_state = _closed_object(
        state["owner_settled_state"], {"provenance", "status", "version"}, "owner-settled state"
    )
    if owner_state["status"] not in OWNER_SETTLED_STATES:
        raise ContractError("owner-settled status is invalid")
    if not isinstance(owner_state["version"], int) or isinstance(owner_state["version"], bool) or owner_state["version"] < 1:
        raise ContractError("owner-settled version is invalid")
    _provenance(owner_state["provenance"], "owner-settled provenance")
    if owner_state["status"] == "confirmed" and outcome is None:
        raise ContractError("confirmed owner-settled state requires a confirmed outcome")

    claims = state["claims"]
    if not isinstance(claims, list) or not claims:
        raise ContractError("claims must be a non-empty list")
    claim_map: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(claims):
        claim = _closed_object(raw, {"id", "provenance", "statement", "status"}, f"claim {index}")
        claim_id = _text(claim["id"], f"claim {index} id")
        if claim_id in claim_map:
            raise ContractError("claim ids contain duplicates")
        if claim["status"] not in CLAIM_STATUSES:
            raise ContractError("claim status is invalid")
        _text(claim["statement"], f"claim {claim_id} statement")
        _provenance(claim["provenance"], f"claim {claim_id} provenance")
        claim_map[claim_id] = claim

    constraints = state["constraints"]
    if not isinstance(constraints, list):
        raise ContractError("constraints must be a list")
    for index, raw in enumerate(constraints):
        constraint = _closed_object(raw, {"id", "provenance", "statement"}, f"constraint {index}")
        _text(constraint["id"], f"constraint {index} id")
        _text(constraint["statement"], f"constraint {index} statement")
        _provenance(constraint["provenance"], f"constraint {index} provenance")

    candidates = state["candidates"]
    if not isinstance(candidates, list) or not candidates:
        raise ContractError("candidates must be a non-empty list")
    candidate_ids: set[str] = set()
    for index, raw in enumerate(candidates):
        candidate = _closed_object(raw, {"id", "specification", "support_claim_ids"}, f"candidate {index}")
        candidate_id = _text(candidate["id"], f"candidate {index} id")
        if candidate_id in candidate_ids:
            raise ContractError("candidate ids contain duplicates")
        candidate_ids.add(candidate_id)
        _text(candidate["specification"], f"candidate {candidate_id} specification")
        support_ids = _text_list(candidate["support_claim_ids"], f"candidate {candidate_id} support")
        if any(item not in claim_map for item in support_ids):
            raise ContractError("candidate support references an unknown claim")

    objects = state["objects"]
    if not isinstance(objects, list) or not objects:
        raise ContractError("objects must be a non-empty list")
    object_ids: set[str] = set()
    for index, raw in enumerate(objects):
        item = _closed_object(raw, {"class", "id", "provenance", "statement"}, f"object {index}")
        object_id = _text(item["id"], f"object {index} id")
        if object_id in object_ids:
            raise ContractError("object ids contain duplicates")
        if item["class"] not in OBJECT_CLASSES:
            raise ContractError("object class is invalid")
        _text(item["statement"], f"object {object_id} statement")
        _provenance(item["provenance"], f"object {object_id} provenance")
        object_ids.add(object_id)

    purpose = state["goal_purpose"]
    if purpose is not None:
        purpose = _closed_object(
            purpose,
            {"class", "falsifier", "horizon", "learning_outcome", "provenance", "statement", "unlocked_decision"},
            "goal purpose",
        )
        if purpose["class"] not in GOAL_PURPOSES:
            raise ContractError("goal purpose class is invalid")
        _text(purpose["statement"], "goal purpose statement")
        _provenance(purpose["provenance"], "goal purpose provenance")
        for field in ("falsifier", "horizon", "learning_outcome", "unlocked_decision"):
            _optional_text(purpose[field], f"goal purpose {field}")
        if purpose["class"] == "discovery" and any(
            purpose[field] is None
            for field in ("falsifier", "horizon", "learning_outcome", "unlocked_decision")
        ):
            raise ContractError("discovery goal requires learning outcome, horizon, falsifier, and unlocked decision")

    bridge = state["causal_bridge"]
    if bridge is not None:
        bridge = _closed_object(
            bridge,
            {"candidate_id", "evidence_claim_ids", "falsifier", "provenance", "statement", "status"},
            "causal bridge",
        )
        if bridge["candidate_id"] not in candidate_ids:
            raise ContractError("causal bridge candidate is unknown")
        if bridge["status"] not in CAUSAL_BRIDGE_STATES:
            raise ContractError("causal bridge status is invalid")
        _text(bridge["statement"], "causal bridge statement")
        _text(bridge["falsifier"], "causal bridge falsifier")
        _provenance(bridge["provenance"], "causal bridge provenance")
        bridge_claim_ids = _text_list(bridge["evidence_claim_ids"], "causal bridge evidence")
        if any(item not in claim_map for item in bridge_claim_ids):
            raise ContractError("causal bridge evidence references an unknown claim")

    uncertainties = state["material_uncertainties"]
    if not isinstance(uncertainties, list):
        raise ContractError("material uncertainties must be a list")
    uncertainty_ids: set[str] = set()
    for index, raw in enumerate(uncertainties):
        uncertainty = _closed_object(
            raw, {"action_candidate_ids", "id", "provenance", "question"}, f"material uncertainty {index}"
        )
        uncertainty_id = _text(uncertainty["id"], f"material uncertainty {index} id")
        if uncertainty_id in uncertainty_ids:
            raise ContractError("material uncertainty ids contain duplicates")
        _text(uncertainty["question"], f"material uncertainty {uncertainty_id} question")
        _provenance(uncertainty["provenance"], f"material uncertainty {uncertainty_id} provenance")
        action_ids = _text_list(
            uncertainty["action_candidate_ids"], f"material uncertainty {uncertainty_id} action candidates"
        )
        if any(item not in candidate_ids for item in action_ids):
            raise ContractError("material uncertainty references an unknown candidate")
        uncertainty_ids.add(uncertainty_id)

    reopening_ids = _text_list(state["reopening_evidence_claim_ids"], "reopening evidence")
    if any(item not in claim_map for item in reopening_ids):
        raise ContractError("reopening evidence references an unknown claim")
    if owner_state["status"] == "reopened" and not reopening_ids:
        raise ContractError("reopened owner-settled state requires reopening evidence")

    recommendation = _closed_object(
        state["recommendation"],
        {"candidate_id", "dependent_claim_ids", "next_move", "qualification", "readiness"},
        "recommendation",
    )
    if recommendation["candidate_id"] not in candidate_ids:
        raise ContractError("recommendation candidate is unknown")
    if recommendation["readiness"] not in READINESS:
        raise ContractError("recommendation readiness is invalid")
    if outcome is None and recommendation["readiness"] != "Not validated":
        raise ContractError("an unconfirmed outcome cannot support execution readiness")
    _text(recommendation["qualification"], "recommendation qualification")
    _text(recommendation["next_move"], "recommendation next move")
    dependent_ids = _text_list(recommendation["dependent_claim_ids"], "recommendation dependencies")
    if any(item not in claim_map for item in dependent_ids):
        raise ContractError("recommendation dependency is unknown")

    rival = _closed_object(state["strongest_rival"], {"candidate_id", "dependent_claim_ids", "reason"}, "strongest rival")
    if rival["candidate_id"] not in candidate_ids:
        raise ContractError("strongest rival candidate is unknown")
    _text(rival["reason"], "strongest rival reason")
    rival_ids = _text_list(rival["dependent_claim_ids"], "strongest rival dependencies")
    if any(item not in claim_map for item in rival_ids):
        raise ContractError("strongest rival dependency is unknown")
    return state


def evaluate(state_value: object, delta_value: object | None = None) -> Evaluation:
    state = validate_state(state_value)
    turn_kind = state["turn_kind"]
    if turn_kind != "material-recommendation":
        if delta_value is not None:
            raise ContractError("bypass turns must not construct a recommendation delta")
        return Evaluation("bypass", "pass", (turn_kind,))
    if delta_value is None:
        raise ContractError("material recommendation requires a delta")
    delta = _closed_object(delta_value, DELTA_KEYS, "delta")
    if delta["schema_version"] != SCHEMA_VERSION:
        raise ContractError("delta schema version is invalid")

    claims = {item["id"]: item for item in state["claims"]}
    candidate_ids = {item["id"] for item in state["candidates"]}
    list_fields = (
        "affected_claim_ids",
        "falsified_claim_ids",
        "replacement_support_claim_ids",
        "retracted_claim_ids",
        "surviving_claim_ids",
    )
    values = {field: _text_list(delta[field], field) for field in list_fields}
    if any(item not in claims for field in list_fields for item in values[field]):
        raise ContractError("delta references an unknown claim")
    if set(values["retracted_claim_ids"]) & set(values["surviving_claim_ids"]):
        raise ContractError("a claim cannot both survive and be retracted")
    if not set(values["retracted_claim_ids"]).issubset(set(values["affected_claim_ids"])):
        raise ContractError("retracted claims must be affected")

    changed_inputs = delta["changed_inputs"]
    if not isinstance(changed_inputs, list):
        raise ContractError("changed inputs must be a list")
    change_kinds: set[str] = set()
    for index, raw in enumerate(changed_inputs):
        change = _closed_object(raw, {"id", "kind", "provenance"}, f"changed input {index}")
        _text(change["id"], f"changed input {index} id")
        kind = _text(change["kind"], f"changed input {index} kind")
        if kind not in QUALIFYING_KINDS | NONQUALIFYING_KINDS | {"candidate-specification"}:
            raise ContractError("changed input kind is invalid")
        _provenance(change["provenance"], f"changed input {index} provenance")
        change_kinds.add(kind)

    proposed = _closed_object(delta["proposed_recommendation"], {"candidate_id", "qualification", "readiness"}, "proposed recommendation")
    if proposed["candidate_id"] not in candidate_ids:
        raise ContractError("proposed recommendation candidate is unknown")
    if proposed["readiness"] not in READINESS:
        raise ContractError("proposed recommendation readiness is invalid")
    _text(proposed["qualification"], "proposed recommendation qualification")
    replacement_id = delta["replacement_candidate_id"]
    if replacement_id is not None and replacement_id not in candidate_ids:
        raise ContractError("replacement candidate is unknown")

    current = state["recommendation"]
    recommendation_changed = any(
        proposed[field] != current[field]
        for field in ("candidate_id", "qualification", "readiness")
    )
    if not recommendation_changed:
        return Evaluation("gate", "pass", ("recommendation_unchanged",))

    qualifying = bool(change_kinds & QUALIFYING_KINDS)
    valid_support = [
        claim_id
        for claim_id in values["replacement_support_claim_ids"]
        if claims[claim_id]["status"] == "evidence"
        and claim_id not in values["falsified_claim_ids"]
    ]
    current_dependencies = set(current["dependent_claim_ids"])
    invalid_retractions = set(values["retracted_claim_ids"]) - (
        current_dependencies & set(values["falsified_claim_ids"])
    )
    if invalid_retractions:
        return Evaluation("gate", "revise", ("false_converse_or_over_retraction",))
    if change_kinds == {"candidate-specification"} and proposed["readiness"] != "Not validated":
        return Evaluation("gate", "revise", ("specification_not_outcome_evidence",))
    if not qualifying:
        return Evaluation("gate", "revise", ("no_qualifying_delta",))
    if proposed["candidate_id"] != current["candidate_id"] and not valid_support:
        return Evaluation("gate", "revise", ("replacement_support_missing",))
    return Evaluation("gate", "pass", ("qualifying_delta",))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path)
    parser.add_argument("--delta", type=Path)
    args = parser.parse_args(argv)
    try:
        state = json.loads(args.state.read_text(encoding="utf-8"))
        delta = json.loads(args.delta.read_text(encoding="utf-8")) if args.delta else None
        print(json.dumps(evaluate(state, delta).as_dict(), sort_keys=True))
    except (OSError, json.JSONDecodeError, ContractError) as error:
        print(json.dumps({"decision": "block", "error": str(error), "schema_version": SCHEMA_VERSION}), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
