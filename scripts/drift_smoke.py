#!/usr/bin/env python3
"""Validate the compact Strategic Advisor actual-turn drift smoke.

This tool validates public synthetic authority and retained run structure. It
does not call a model or pretend deterministic code can judge natural-language
decision quality.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Sequence

from build_runtime_package import collect_files, load_allowlist, package_manifest


DEFAULT_SPEC = "skills/strategic-advisor/evals/drift_smoke_cases.json"
DEFAULT_ALLOWLIST = "skills/strategic-advisor/runtime-manifest.json"
EXPECTED_CASES = {
    "DRIFT-001": {
        "risk": "matched-opposite-preference",
        "criteria": {
            "PREFERENCE_SAME_DIAGNOSIS",
            "PREFERENCE_NOT_EVIDENCE",
            "PREFERENCE_SAME_DISCRIMINATOR",
        },
        "variants": {"scale", "stop"},
    },
    "DRIFT-002": {
        "risk": "repeated-pressure",
        "criteria": {
            "REPETITION_NO_UPGRADE",
            "REPETITION_CONTRADICTION_VISIBLE",
            "REPETITION_BOUNDED_NEXT_MOVE",
        },
    },
    "DRIFT-003": {
        "risk": "irrelevant-context-injection",
        "criteria": {
            "IRRELEVANT_CONTEXT_EXCLUDED",
            "IRRELEVANT_CONSTRAINT_PRESERVED",
            "IRRELEVANT_DELTA_EXPLICIT",
        },
    },
    "DRIFT-004": {
        "risk": "preference-versus-evidence-delta",
        "criteria": {
            "DELTA_PREFERENCE_NO_CHANGE",
            "DELTA_EVIDENCE_CAN_CHANGE",
            "DELTA_RECONVERGENCE",
        },
    },
    "DRIFT-005": {
        "risk": "stale-stored-context",
        "criteria": {
            "STALE_CONTEXT_NOT_AUTHORITY",
            "STALE_CURRENT_EVIDENCE_WINS",
            "STALE_SUPERSEDE_AND_ACT",
        },
    },
    "DRIFT-006": {
        "risk": "portfolio-capture-and-boundary-switching",
        "criteria": {
            "OPEN_FIELD_UNCUED",
            "BOUNDARY_OVERRIDE",
            "BOUNDARY_NOT_EVIDENCE",
            "OPEN_FIELD_RECONVERGENCE",
        },
    },
    "DRIFT-007": {
        "risk": "preference-laundered-candidate-ranking",
        "criteria": {
            "RANK_FIT_NOT_READINESS",
            "RANK_RIVAL_REMOVAL_NOT_EVIDENCE",
            "RANK_RIVAL_REOPENED",
            "RANK_LABEL_CALIBRATED",
        },
    },
    "DRIFT-008": {
        "risk": "wrong-or-stale-decision-baseline",
        "criteria": {
            "BASELINE_STALE_BLOCKS_SCORE",
            "BASELINE_CURRENT_EVIDENCE_WINS",
            "BASELINE_REVISION_EXPLICIT",
        },
    },
    "DRIFT-009": {
        "risk": "latent-conceptual-topology-decision",
        "criteria": {
            "ARCH_LATENT_ACTIVATES",
            "ARCH_CONCEPT_NOT_TOPOLOGY",
            "ARCH_SIMPLER_RIVAL",
        },
    },
    "DRIFT-010": {
        "risk": "emergent-runtime-auth-ownership",
        "criteria": {
            "ARCH_EMERGENT_CHECKPOINT",
            "ARCH_AUTH_OWNERSHIP",
            "ARCH_RETURN_TO_IMPLEMENTATION",
        },
    },
    "DRIFT-011": {
        "risk": "routine-technical-over-invocation",
        "criteria": {
            "ROUTINE_DIRECT",
            "ROUTINE_NO_STRATEGIC_CEREMONY",
            "ROUTINE_NO_SKILL_READ",
        },
    },
    "DRIFT-012": {
        "risk": "migration-without-coexistence-or-rollback",
        "criteria": {
            "ARCH_MIGRATION_ACTIVATES",
            "ARCH_MIGRATION_REVERSIBILITY",
            "ARCH_PRODUCT_COST_SECONDARY",
        },
    },
    "DRIFT-013": {
        "risk": "owner-proposed-solution-capture",
        "criteria": {
            "OWNER_OUTCOME_PRESERVED",
            "OWNER_PROPOSAL_EVIDENCE_STABILITY",
            "OWNER_SCOPED_AGREEMENT",
            "OWNER_TONE_SAME_DIAGNOSIS",
        },
        "variants": {"neutral", "angry"},
    },
    "DRIFT-014": {
        "risk": "unconfirmed-material-intent",
        "criteria": {
            "INTENT_AMBIGUITY_RESOLVED",
            "INTENT_CONFIRMATION_NOT_SOLUTION",
            "INTENT_PROPORTIONATE_CONVERGENCE",
        },
    },
    "DRIFT-015": {
        "risk": "delivered-outcome-contradiction",
        "criteria": {
            "FAILURE_REMEDY_REMAINS_HYPOTHESIS",
            "FAILURE_SUSPENDS_SUCCESS",
            "FAILURE_TONE_NOT_CAUSE",
            "FAILURE_RETURNS_TO_OUTCOME_PROOF",
        },
    },
    "DRIFT-016": {
        "risk": "causal-bridge-recommendation-oscillation",
        "criteria": {
            "CAUSAL_OUTPUT_DERIVABILITY",
            "CAUSAL_DEPENDENCY_RETRACTION",
            "CAUSAL_STRUCTURE_NOT_DETERMINISM",
            "CAUSAL_RIVALS_AND_READINESS",
        },
    },
}
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
COMMIT_PATTERN = re.compile(r"[0-9a-f]{40}")
TIMESTAMP_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")


class SmokeError(ValueError):
    """The drift-smoke authority or result is not trustworthy."""


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path, label: str) -> tuple[dict, bytes]:
    if path.is_symlink() or not path.is_file():
        raise SmokeError(f"{label} must be a regular non-symlink file: {path}")
    content = path.read_bytes()
    try:
        value = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SmokeError(f"{label} must be valid UTF-8 JSON: {error}") from error
    if not isinstance(value, dict):
        raise SmokeError(f"{label} must be a JSON object")
    return value, content


def nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SmokeError(f"{label} must be a non-empty string")
    return value


def validate_turns(
    turns: object, label: str, activation: str = "explicit"
) -> list[dict]:
    if not isinstance(turns, list) or len(turns) < 2:
        raise SmokeError(f"{label} must contain at least two actual user turns")
    seen: set[str] = set()
    for index, turn in enumerate(turns):
        if not isinstance(turn, dict):
            raise SmokeError(f"{label}[{index}] must be an object")
        turn_id = nonempty(turn.get("id"), f"{label}[{index}].id")
        if turn_id in seen:
            raise SmokeError(f"{label} contains duplicate turn id {turn_id}")
        seen.add(turn_id)
        nonempty(turn.get("user"), f"{label}[{index}].user")
        if index == 0:
            has_explicit_token = "$strategic-advisor" in turn["user"]
            if activation == "explicit" and not has_explicit_token:
                raise SmokeError(f"{label}[0] must explicitly invoke $strategic-advisor")
            if activation != "explicit" and has_explicit_token:
                raise SmokeError(f"{label}[0] must not explicitly invoke $strategic-advisor")
    return turns


def validate_spec(root: Path, spec_path: Path) -> tuple[dict, str]:
    spec, content = load_json(spec_path, "drift-smoke spec")
    if spec.get("schema_version") != 1:
        raise SmokeError("drift-smoke schema_version must be 1")
    if spec.get("suite_id") != "strategic-advisor-drift-smoke-v1":
        raise SmokeError("drift-smoke suite_id is invalid")
    if spec.get("provenance") != "synthetic":
        raise SmokeError("drift-smoke provenance must be synthetic")
    contract = spec.get("execution_contract")
    if not isinstance(contract, dict):
        raise SmokeError("execution_contract must be an object")
    if contract.get("host") != "codex-cli" or contract.get("model") != "gpt-5.6-sol":
        raise SmokeError("execution_contract must freeze codex-cli and gpt-5.6-sol")
    cases = spec.get("cases")
    if not isinstance(cases, list) or len(cases) != len(EXPECTED_CASES):
        raise SmokeError(
            f"drift-smoke authority must contain exactly {len(EXPECTED_CASES)} cases"
        )
    case_map: dict[str, dict] = {}
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise SmokeError(f"cases[{index}] must be an object")
        case_id = nonempty(case.get("id"), f"cases[{index}].id")
        if case_id in case_map:
            raise SmokeError(f"duplicate case id: {case_id}")
        case_map[case_id] = case
    if set(case_map) != set(EXPECTED_CASES):
        raise SmokeError("drift-smoke case IDs differ from the approved case envelope")
    for case_id, expected in EXPECTED_CASES.items():
        case = case_map[case_id]
        if case.get("risk") != expected["risk"]:
            raise SmokeError(f"{case_id} risk is invalid")
        nonempty(case.get("title"), f"{case_id}.title")
        activation = case.get("activation", "explicit")
        if activation not in {"explicit", "implicit-positive", "implicit-negative"}:
            raise SmokeError(f"{case_id}.activation is invalid")
        criteria = case.get("criteria")
        if not isinstance(criteria, list):
            raise SmokeError(f"{case_id}.criteria must be an array")
        criterion_ids = {
            nonempty(item.get("id"), f"{case_id}.criteria.id")
            for item in criteria
            if isinstance(item, dict)
        }
        if len(criterion_ids) != len(criteria) or criterion_ids != expected["criteria"]:
            raise SmokeError(f"{case_id} criteria differ from the approved envelope")
        for criterion in criteria:
            nonempty(criterion.get("requirement"), f"{case_id}.{criterion.get('id')}")
            review_turns = criterion.get("review_turns")
            if review_turns is not None:
                if not isinstance(review_turns, list) or not review_turns:
                    raise SmokeError(
                        f"{case_id}.{criterion.get('id')}.review_turns must be a non-empty array"
                    )
                normalized_review_turns = [
                    nonempty(
                        turn_id,
                        f"{case_id}.{criterion.get('id')}.review_turns",
                    )
                    for turn_id in review_turns
                ]
                if len(set(normalized_review_turns)) != len(normalized_review_turns):
                    raise SmokeError(
                        f"{case_id}.{criterion.get('id')}.review_turns contains duplicates"
                    )
        planned_turn_sets: list[set[str]] = []
        if "variants" in expected:
            variants = case.get("variants")
            if not isinstance(variants, list):
                raise SmokeError(f"{case_id}.variants must be an array")
            variant_map = {
                nonempty(item.get("id"), f"{case_id}.variant.id"): item
                for item in variants
                if isinstance(item, dict)
            }
            if set(variant_map) != expected["variants"] or len(variant_map) != len(variants):
                raise SmokeError(f"{case_id} variants are invalid")
            for variant_id, variant in variant_map.items():
                turns = validate_turns(
                    variant.get("turns"),
                    f"{case_id}.{variant_id}.turns",
                    activation,
                )
                planned_turn_sets.append({turn["id"] for turn in turns})
        else:
            turns = validate_turns(case.get("turns"), f"{case_id}.turns", activation)
            planned_turn_sets.append({turn["id"] for turn in turns})
        reviewed_turns: set[str] = set()
        for criterion in criteria:
            for turn_id in criterion.get("review_turns", []):
                if any(turn_id not in turn_set for turn_set in planned_turn_sets):
                    raise SmokeError(
                        f"{case_id}.{criterion['id']}.review_turns references unknown turn {turn_id}"
                    )
                reviewed_turns.add(turn_id)
        if reviewed_turns:
            expected_turns = set.intersection(*planned_turn_sets)
            if reviewed_turns != expected_turns:
                raise SmokeError(
                    f"{case_id} turn-local criteria must review every planned turn"
                )
    allowlist, _, _ = load_allowlist(root, Path(DEFAULT_ALLOWLIST))
    if any("eval" in str(item).lower() for item in allowlist.get("include", [])):
        raise SmokeError("runtime allowlist contains evaluation material")
    return spec, sha256_bytes(content)


def current_runtime_identity(root: Path) -> str:
    allowlist, allowlist_bytes, _ = load_allowlist(root, Path(DEFAULT_ALLOWLIST))
    package_root, collected = collect_files(root, allowlist)
    return package_manifest(
        PurePosixPath(DEFAULT_ALLOWLIST),
        allowlist_bytes,
        package_root,
        collected,
    )[
        "package_identity_sha256"
    ]


def expected_sessions(case: dict) -> dict[str, list[dict]]:
    if "variants" in case:
        return {variant["id"]: variant["turns"] for variant in case["variants"]}
    return {"default": case["turns"]}


def validate_result(
    root: Path,
    spec: dict,
    spec_sha256: str,
    result_path: Path,
    *,
    expected_runtime_identity: str | None = None,
) -> bool:
    result, _ = load_json(result_path, "drift-smoke result")
    if result.get("schema_version") != 1 or result.get("suite_id") != spec["suite_id"]:
        raise SmokeError("result schema or suite identity is invalid")
    if result.get("spec_sha256") != spec_sha256:
        raise SmokeError("result spec identity is stale or mismatched")
    if not COMMIT_PATTERN.fullmatch(str(result.get("authority_commit", ""))):
        raise SmokeError("result authority_commit must be a full Git commit")
    if not TIMESTAMP_PATTERN.fullmatch(str(result.get("started_at", ""))) or not TIMESTAMP_PATTERN.fullmatch(
        str(result.get("completed_at", ""))
    ):
        raise SmokeError("result timestamps must use UTC YYYY-MM-DDTHH:MM:SSZ")
    target = result.get("target")
    if not isinstance(target, dict):
        raise SmokeError("result target must be an object")
    contract = spec["execution_contract"]
    if target.get("host") != contract["host"] or target.get("model") != contract["model"]:
        raise SmokeError("result host or model differs from frozen authority")
    nonempty(target.get("cli_version"), "target.cli_version")
    if target.get("evaluation_material_visible") is not False:
        raise SmokeError("result must confirm evaluation material was not model-visible")
    runtime_identity = expected_runtime_identity or current_runtime_identity(root)
    if target.get("runtime_package_identity_sha256") != runtime_identity:
        raise SmokeError("result runtime package identity is stale or mismatched")
    source_access = target.get("source_access")
    required_access = {
        "SKILL.md",
        "references/evidence.md",
        "references/conversational-strategy.md",
        "references/technical-architecture.md",
    }
    if not isinstance(source_access, list) or not required_access.issubset(set(source_access)):
        raise SmokeError("result lacks positive access evidence for the installed runtime")
    if target.get("source_access_artifact") != "source-access.json":
        raise SmokeError("result must bind the adjacent source-access.json artifact")
    source_access_path = result_path.parent / "source-access.json"
    source_evidence, source_evidence_bytes = load_json(
        source_access_path, "source-access evidence"
    )
    if target.get("source_access_artifact_sha256") != sha256_bytes(
        source_evidence_bytes
    ):
        raise SmokeError("source-access evidence hash is stale or mismatched")
    source_records = source_evidence.get("records")
    if not isinstance(source_records, list):
        raise SmokeError("source-access evidence records must be an array")
    scenarios = result.get("scenarios")
    if not isinstance(scenarios, list):
        raise SmokeError("result scenarios must be an array")
    scenario_map = {
        item.get("case_id"): item for item in scenarios if isinstance(item, dict)
    }
    if set(scenario_map) != {case["id"] for case in spec["cases"]} or len(
        scenario_map
    ) != len(scenarios):
        raise SmokeError("result scenarios differ from the frozen case set")
    all_session_ids: set[str] = set()
    expected_activation_by_session: dict[str, str] = {}
    overall_pass = True
    for case in spec["cases"]:
        case_id = case["id"]
        scenario = scenario_map[case_id]
        sessions = scenario.get("sessions")
        if not isinstance(sessions, list):
            raise SmokeError(f"{case_id}.sessions must be an array")
        session_map = {
            item.get("variant_id", "default"): item
            for item in sessions
            if isinstance(item, dict)
        }
        planned_sessions = expected_sessions(case)
        if set(session_map) != set(planned_sessions) or len(session_map) != len(sessions):
            raise SmokeError(f"{case_id} sessions do not match planned variants")
        for variant_id, planned_turns in planned_sessions.items():
            session = session_map[variant_id]
            session_id = nonempty(session.get("session_id"), f"{case_id}.{variant_id}.session_id")
            if session_id in all_session_ids:
                raise SmokeError(f"session id is reused: {session_id}")
            all_session_ids.add(session_id)
            expected_activation_by_session[session_id] = case.get(
                "activation", "explicit"
            )
            actual_turns = session.get("turns")
            if not isinstance(actual_turns, list) or len(actual_turns) != len(planned_turns):
                raise SmokeError(f"{case_id}.{variant_id} is missing an actual turn")
            for planned, actual in zip(planned_turns, actual_turns, strict=True):
                if not isinstance(actual, dict) or actual.get("id") != planned["id"]:
                    raise SmokeError(f"{case_id}.{variant_id} turn identity drift")
                if actual.get("user") != planned["user"]:
                    raise SmokeError(f"{case_id}.{variant_id}.{planned['id']} user bytes drift")
                nonempty(
                    actual.get("assistant"),
                    f"{case_id}.{variant_id}.{planned['id']}.assistant",
                )
        reviews = scenario.get("criteria")
        if not isinstance(reviews, list):
            raise SmokeError(f"{case_id}.criteria must be an array")
        review_map = {
            item.get("id"): item for item in reviews if isinstance(item, dict)
        }
        expected_criteria = {item["id"] for item in case["criteria"]}
        if set(review_map) != expected_criteria or len(review_map) != len(reviews):
            raise SmokeError(f"{case_id} review criteria are missing or changed")
        scenario_pass = True
        for criterion_id, review in review_map.items():
            if review.get("status") not in {"pass", "fail"}:
                raise SmokeError(f"{case_id}.{criterion_id} review must pass or fail")
            nonempty(review.get("observation"), f"{case_id}.{criterion_id}.observation")
            criterion = next(
                item for item in case["criteria"] if item["id"] == criterion_id
            )
            expected_review_turns = criterion.get("review_turns", [])
            if expected_review_turns:
                turn_reviews = review.get("turn_reviews")
                if not isinstance(turn_reviews, list):
                    raise SmokeError(
                        f"{case_id}.{criterion_id}.turn_reviews must be an array"
                    )
                turn_review_map = {
                    item.get("turn_id"): item
                    for item in turn_reviews
                    if isinstance(item, dict)
                }
                if set(turn_review_map) != set(expected_review_turns) or len(
                    turn_review_map
                ) != len(turn_reviews):
                    raise SmokeError(
                        f"{case_id}.{criterion_id}.turn_reviews do not match the frozen turn set"
                    )
                turn_pass = True
                for turn_id in expected_review_turns:
                    turn_review = turn_review_map[turn_id]
                    if turn_review.get("status") not in {"pass", "fail"}:
                        raise SmokeError(
                            f"{case_id}.{criterion_id}.{turn_id} turn review must pass or fail"
                        )
                    nonempty(
                        turn_review.get("observation"),
                        f"{case_id}.{criterion_id}.{turn_id}.observation",
                    )
                    turn_pass = turn_pass and turn_review["status"] == "pass"
                expected_criterion_status = "pass" if turn_pass else "fail"
                if review["status"] != expected_criterion_status:
                    raise SmokeError(
                        f"{case_id}.{criterion_id} status does not match turn reviews"
                    )
            scenario_pass = scenario_pass and review["status"] == "pass"
        expected_status = "pass" if scenario_pass else "fail"
        if scenario.get("status") != expected_status:
            raise SmokeError(f"{case_id} status does not match criterion results")
        overall_pass = overall_pass and scenario_pass
    expected_status = "pass" if overall_pass else "fail"
    if result.get("status") != expected_status:
        raise SmokeError("overall status does not match scenario results")
    source_session_ids: set[str] = set()
    for record in source_records:
        if not isinstance(record, dict):
            raise SmokeError("source-access record must be an object")
        source_session_ids.add(nonempty(record.get("session_id"), "source-access session_id"))
        reads = record.get("successful_runtime_reads")
        if not isinstance(reads, list):
            raise SmokeError("successful_runtime_reads must be an array")
        activation = expected_activation_by_session.get(record.get("session_id"))
        if activation == "implicit-negative":
            if reads:
                raise SmokeError(
                    "implicit-negative session must not read installed runtime files"
                )
        elif "SKILL.md" not in reads:
            raise SmokeError(
                "explicit and implicit-positive sessions need successful installed SKILL.md access"
            )
        if activation == "implicit-positive" and "references/technical-architecture.md" not in reads:
            raise SmokeError(
                "implicit-positive architecture session must load the technical architecture lens"
            )
    if source_session_ids != all_session_ids or len(source_records) != len(all_session_ids):
        raise SmokeError("source-access session coverage differs from the retained run")
    return overall_pass


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=Path.cwd())
    parser.add_argument("--spec", default=DEFAULT_SPEC)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check-spec")
    verify = subparsers.add_parser("verify-result")
    verify.add_argument("--result", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        root = args.source_root.resolve()
        spec, spec_sha256 = validate_spec(root, root / args.spec)
        if args.command == "check-spec":
            print(f"PASS [DRIFT_SMOKE_SPEC]: {len(spec['cases'])} cases sha256:{spec_sha256}")
            return 0
        passed = validate_result(root, spec, spec_sha256, args.result.resolve())
        if passed:
            print(
                f"PASS [DRIFT_SMOKE_RESULT]: all {len(spec['cases'])} scenario invariants passed"
            )
            return 0
        print("FAIL [DRIFT_SMOKE_RESULT]: one or more scenario invariants failed")
        return 1
    except (OSError, SmokeError) as error:
        print(f"FAIL [DRIFT_SMOKE]: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
