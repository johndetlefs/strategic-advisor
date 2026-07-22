#!/usr/bin/env python3
"""Build or verify the canonical Agent Skills evaluation inventory."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EVAL_ROOT = Path("skills/strategic-advisor/evals")
SOURCE_FILES = ("core_cases.json", "lens_cases.json")
OUTPUT_FILE = "evals.json"


class EvalBuildError(ValueError):
    """Raised when a normative source inventory cannot be imported safely."""


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise EvalBuildError(f"Cannot read valid JSON from {path}: {error}") from error


def nonempty_strings(value: Any, field: str, case_id: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise EvalBuildError(f"{case_id}: {field} must be a non-empty string array")
    return value


def routing_assertions(case: dict[str, Any]) -> list[str]:
    assertions: list[str] = []
    routing = case.get("expected_routing")
    if not isinstance(routing, dict):
        return assertions
    primary = routing.get("primary")
    secondary = routing.get("secondary")
    unsupported = routing.get("unsupported_domain")
    if unsupported is True:
        assertions.append(
            "The response activates zero professional lenses and states the unsupported-domain boundary."
        )
    elif isinstance(primary, str) and primary:
        assertions.append(f"The response uses {primary} as its primary lens.")
    if isinstance(secondary, str) and secondary:
        assertions.append(f"The response uses only {secondary} as its secondary lens.")
    elif secondary is None and unsupported is not True:
        assertions.append("The response does not activate an unnecessary secondary lens.")
    return assertions


def claim_status_assertions(case: dict[str, Any], case_id: str) -> list[str]:
    routing = case.get("expected_routing")
    if isinstance(routing, dict) and routing.get("unsupported_domain") is True:
        return []
    raw = case.get("expected_claim_statuses", [])
    if not isinstance(raw, list):
        raise EvalBuildError(f"{case_id}: expected_claim_statuses must be an array")
    assertions: list[str] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise EvalBuildError(
                f"{case_id}: expected_claim_statuses[{index}] must be an object"
            )
        claim = item.get("claim")
        status = item.get("status")
        if not isinstance(claim, str) or not claim or not isinstance(status, str) or not status:
            raise EvalBuildError(
                f"{case_id}: expected_claim_statuses[{index}] needs claim and status"
            )
        assertions.append(f"The response preserves '{claim}' as {status}.")
    return assertions


def import_case(source_name: str, case: Any) -> dict[str, Any]:
    if not isinstance(case, dict):
        raise EvalBuildError(f"{source_name}: every case must be an object")
    case_id = case.get("id")
    prompt = case.get("prompt")
    title = case.get("title")
    if not all(isinstance(value, str) and value.strip() for value in (case_id, prompt, title)):
        raise EvalBuildError(f"{source_name}: every case needs non-empty id, title, and prompt")

    expected_key = (
        "expected_decision_properties"
        if source_name == "core_cases.json"
        else "required_decision_properties"
    )
    forbidden_key = (
        "forbidden_behaviors"
        if source_name == "core_cases.json"
        else "forbidden_decision_properties"
    )
    required = nonempty_strings(case.get(expected_key), expected_key, case_id)
    forbidden = nonempty_strings(case.get(forbidden_key), forbidden_key, case_id)
    assertions = routing_assertions(case)
    readiness = case.get("expected_readiness")
    readiness_target = case.get("readiness_target")
    if isinstance(readiness, str) and readiness:
        if source_name == "lens_cases.json":
            if not isinstance(readiness_target, str) or not readiness_target.strip():
                raise EvalBuildError(
                    f"{case_id}: a supported lens readiness verdict needs a non-empty readiness_target"
                )
            assertions.append(
                f"For '{readiness_target}', the response states exactly one current readiness verdict: {readiness}."
            )
        else:
            assertions.append(
                f"The response states exactly one current readiness verdict: {readiness}."
            )
    elif source_name == "lens_cases.json" and readiness_target is not None:
        raise EvalBuildError(
            f"{case_id}: readiness_target must be null when expected_readiness is null"
        )
    assertions.extend(claim_status_assertions(case, case_id))
    assertions.extend(required)

    metadata: dict[str, Any] = {
        "source_inventory": source_name,
        "source_case_id": case_id,
        "data_classification": "synthetic",
    }
    for field in (
        "covers",
        "case_kind",
        "lens",
        "pair_id",
        "pair_context",
        "matched_facts",
        "preference_label",
        "probe_tags",
        "expected_routing",
        "expected_readiness",
        "readiness_target",
        "not_applicable_dimensions",
    ):
        if field in case:
            metadata[field] = case[field]

    return {
        "id": case_id,
        "prompt": prompt,
        "expected_output": (
            f"A reality-tested response for '{title}' that satisfies the case-specific "
            "assertions without any forbidden behaviour."
        ),
        "files": [],
        "assertions": assertions,
        "forbidden_behaviors": forbidden,
        "metadata": metadata,
    }


def build_document(root: Path) -> dict[str, Any]:
    eval_root = root / EVAL_ROOT
    imported: list[dict[str, Any]] = []
    source_inventory: list[dict[str, Any]] = []
    seen: set[str] = set()
    for source_name in SOURCE_FILES:
        source_path = eval_root / source_name
        source = read_json(source_path)
        if not isinstance(source, dict) or not isinstance(source.get("cases"), list):
            raise EvalBuildError(f"{source_name}: top level must contain a cases array")
        classification = source.get("provenance", source.get("data_classification"))
        if classification != "synthetic":
            raise EvalBuildError(f"{source_name}: top-level classification must be synthetic")
        source_inventory.append(
            {"path": f"evals/{source_name}", "case_count": len(source["cases"])}
        )
        for case in source["cases"]:
            imported_case = import_case(source_name, case)
            case_id = imported_case["id"]
            if case_id in seen:
                raise EvalBuildError(f"Duplicate case id across source inventories: {case_id}")
            seen.add(case_id)
            imported.append(imported_case)
    if len(imported) < 16:
        raise EvalBuildError("Combined inventory must contain at least 16 distinct cases")
    return {
        "schema_version": 1,
        "skill_name": "strategic-advisor",
        "data_classification": "synthetic",
        "source_inventories": source_inventory,
        "evals": imported,
    }


def serialized_document(root: Path) -> str:
    return json.dumps(build_document(root), indent=2, ensure_ascii=False) + "\n"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build or verify skills/strategic-advisor/evals/evals.json."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Fail if evals.json is stale.")
    mode.add_argument("--write", action="store_true", help="Write the canonical evals.json.")
    parser.add_argument("--root", type=Path, default=REPOSITORY_ROOT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    output = root / EVAL_ROOT / OUTPUT_FILE
    try:
        expected = serialized_document(root)
    except EvalBuildError as error:
        print(f"FAIL [EVALS_IMPORT_INVALID]: {error}")
        return 1
    if args.write:
        output.write_text(expected, encoding="utf-8")
        print(f"WROTE {output.relative_to(root)}")
        return 0
    if not output.is_file():
        print(f"FAIL [EVALS_COMBINED_MISSING]: {output.relative_to(root)}")
        return 1
    if output.read_text(encoding="utf-8") != expected:
        print(f"FAIL [EVALS_COMBINED_STALE]: {output.relative_to(root)}")
        return 1
    print(f"PASS [EVALS_COMBINED_CURRENT]: {len(build_document(root)['evals'])} cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
