#!/usr/bin/env python3
"""Validate and build the frozen EPIC-007 goal-review case inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TASK_ROOT = Path(
    ".project-workflow/tasks/EPIC-007-Strategic-Alignment-And-Goal-Review-Control/"
    "TASK-031-Freeze-Combined-Contract-And-Behaviour-Baseline"
)
AUTHORITY_FILE = TASK_ROOT / "CASE-AUTHORITY.json"
OUTPUT_FILE = TASK_ROOT / "CASE-INVENTORY.json"
FREEZE_MANIFEST = TASK_ROOT / "FREEZE-MANIFEST.json"
RUNTIME_MANIFEST = Path("skills/strategic-advisor/runtime-manifest.json")
EXPECTED_CATEGORIES = {
    "routine-direct-assistance",
    "bounded-reconnaissance",
    "initial-alignment",
    "same-robust-move",
    "evidence-resolvable-fork",
    "owner-value-fork",
    "evidence-triggered-reclarification",
    "selective-invalidation",
    "goal-proxy-ladder",
    "aspiration-handling",
    "discovery-goal",
    "operational-goal-readiness",
    "causal-leading-indicators",
    "material-progress",
    "unjustified-goal-change",
    "justified-goal-change",
    "event-exception-review",
    "weekly-monthly-disposition",
    "owner-reconciliation",
    "process-waste-falsifier",
}
EXPECTED_IDS = {f"SAGR-{index:03d}" for index in range(1, 21)}


class FreezeError(ValueError):
    """Raised when the frozen authority is incomplete or unsafe."""


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise FreezeError(f"Cannot read valid JSON from {path}: {error}") from error


def _nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FreezeError(f"{label} must be non-empty text")
    return value.strip()


def validate_authority(authority: Any) -> list[dict[str, Any]]:
    if not isinstance(authority, dict):
        raise FreezeError("authority must be a JSON object")
    if authority.get("schema_version") != 1:
        raise FreezeError("schema_version must be 1")
    if authority.get("suite_id") != "strategic-advisor-goal-alignment-review-v1":
        raise FreezeError("suite_id is invalid")
    if authority.get("status") != "frozen-pre-treatment":
        raise FreezeError("status must be frozen-pre-treatment")
    if authority.get("provenance") != "synthetic":
        raise FreezeError("provenance must be synthetic")
    if authority.get("proof_layer") != "exact-runtime-synthetic":
        raise FreezeError("proof_layer must be exact-runtime-synthetic")
    _nonempty(authority.get("applicability"), "applicability")
    _nonempty(authority.get("authority_source"), "authority_source")
    required = authority.get("required_categories")
    if not isinstance(required, list) or set(required) != EXPECTED_CATEGORIES:
        raise FreezeError("required_categories differ from the approved envelope")
    if len(required) != len(set(required)):
        raise FreezeError("required_categories contain duplicates")

    cases = authority.get("cases")
    if not isinstance(cases, list):
        raise FreezeError("cases must be an array")
    ids = [case.get("id") if isinstance(case, dict) else None for case in cases]
    if set(ids) != EXPECTED_IDS or len(ids) != len(EXPECTED_IDS):
        raise FreezeError("case IDs differ from the approved SAGR-001..SAGR-020 envelope")
    categories = [
        case.get("category") if isinstance(case, dict) else None for case in cases
    ]
    if set(categories) != EXPECTED_CATEGORIES or len(categories) != len(EXPECTED_CATEGORIES):
        raise FreezeError("each approved category must have exactly one case")

    seen_criteria: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for case in cases:
        if not isinstance(case, dict):
            raise FreezeError("every case must be an object")
        case_id = _nonempty(case.get("id"), "case id")
        category = _nonempty(case.get("category"), f"{case_id} category")
        title = _nonempty(case.get("title"), f"{case_id} title")
        activation = _nonempty(case.get("activation"), f"{case_id} activation")
        if activation not in {"gate", "bypass"}:
            raise FreezeError(f"{case_id} activation must be gate or bypass")
        turns = case.get("turns")
        if not isinstance(turns, list) or not turns:
            raise FreezeError(f"{case_id} turns must be a non-empty array")
        turn_ids: set[str] = set()
        for turn in turns:
            if not isinstance(turn, dict):
                raise FreezeError(f"{case_id} turn must be an object")
            turn_id = _nonempty(turn.get("id"), f"{case_id} turn id")
            _nonempty(turn.get("user"), f"{case_id} {turn_id} user")
            if turn_id in turn_ids:
                raise FreezeError(f"{case_id} duplicate turn id {turn_id}")
            turn_ids.add(turn_id)

        criteria = case.get("criteria")
        if not isinstance(criteria, list) or not criteria:
            raise FreezeError(f"{case_id} criteria must be a non-empty array")
        criterion_ids: list[str] = []
        for criterion in criteria:
            if not isinstance(criterion, dict):
                raise FreezeError(f"{case_id} criterion must be an object")
            criterion_id = _nonempty(criterion.get("id"), f"{case_id} criterion id")
            _nonempty(
                criterion.get("requirement"), f"{case_id} {criterion_id} requirement"
            )
            review_turns = criterion.get("review_turns")
            if not isinstance(review_turns, list) or not review_turns:
                raise FreezeError(f"{case_id} {criterion_id} review_turns are required")
            if any(turn_id not in turn_ids for turn_id in review_turns):
                raise FreezeError(
                    f"{case_id} {criterion_id} references an unknown review turn"
                )
            if criterion_id in seen_criteria:
                raise FreezeError(f"duplicate criterion id {criterion_id}")
            seen_criteria.add(criterion_id)
            criterion_ids.append(criterion_id)

        forbidden = case.get("forbidden_behaviors")
        if not isinstance(forbidden, list) or not forbidden or not all(
            isinstance(item, str) and item.strip() for item in forbidden
        ):
            raise FreezeError(f"{case_id} forbidden_behaviors must be non-empty text")
        normalized.append(
            {
                "id": case_id,
                "category": category,
                "title": title,
                "activation": activation,
                "turn_ids": sorted(turn_ids),
                "criterion_ids": criterion_ids,
                "forbidden_behavior_count": len(forbidden),
            }
        )
    return normalized


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git_blob(root: Path, commit: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise FreezeError(f"cannot read baseline {commit}:{path}: {detail}")
    return result.stdout


def validate_freeze_manifest(root: Path, inventory: dict[str, Any]) -> None:
    manifest = read_json(root / FREEZE_MANIFEST)
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise FreezeError("freeze manifest schema_version must be 1")
    if manifest.get("status") != "frozen-pre-treatment":
        raise FreezeError("freeze manifest status must be frozen-pre-treatment")
    baseline = manifest.get("untreated_repository_baseline")
    if not isinstance(baseline, dict):
        raise FreezeError("untreated_repository_baseline must be an object")
    commit = _nonempty(baseline.get("source_commit"), "baseline source_commit")
    files = manifest.get("baseline_files")
    if not isinstance(files, list) or not files:
        raise FreezeError("baseline_files must be a non-empty array")
    seen: set[str] = set()
    for record in files:
        if not isinstance(record, dict):
            raise FreezeError("baseline file record must be an object")
        path = _nonempty(record.get("path"), "baseline file path")
        expected = _nonempty(record.get("sha256"), f"{path} sha256")
        if path in seen:
            raise FreezeError(f"duplicate baseline file {path}")
        seen.add(path)
        actual = _sha256(_git_blob(root, commit, path))
        if actual != expected:
            raise FreezeError(
                f"baseline hash mismatch for {path}: expected {expected}, got {actual}"
            )
    authority = manifest.get("frozen_case_authority")
    if not isinstance(authority, dict):
        raise FreezeError("frozen_case_authority must be an object")
    for path_key, hash_key in (
        ("path", "sha256"),
        ("derived_inventory_path", "derived_inventory_sha256"),
    ):
        path = _nonempty(authority.get(path_key), f"frozen case {path_key}")
        expected = _nonempty(authority.get(hash_key), f"frozen case {hash_key}")
        actual = _sha256((root / path).read_bytes())
        if actual != expected:
            raise FreezeError(
                f"frozen case hash mismatch for {path}: expected {expected}, got {actual}"
            )
    if authority.get("case_count") != inventory["case_count"]:
        raise FreezeError("freeze manifest case_count differs from derived inventory")
    if authority.get("criterion_count") != inventory["criterion_count"]:
        raise FreezeError("freeze manifest criterion_count differs from derived inventory")
    if authority.get("treatment_output_seen") is not False:
        raise FreezeError("treatment_output_seen must be false at freeze")


def build_document(root: Path) -> dict[str, Any]:
    authority = read_json(root / AUTHORITY_FILE)
    normalized = validate_authority(authority)
    runtime_manifest = read_json(root / RUNTIME_MANIFEST)
    includes = runtime_manifest.get("include") if isinstance(runtime_manifest, dict) else None
    if not isinstance(includes, list):
        raise FreezeError("runtime manifest include list is invalid")
    if any("CASE-AUTHORITY.json" in str(path) for path in includes):
        raise FreezeError("frozen evaluation authority must not enter the runtime package")
    document = {
        "schema_version": 1,
        "suite_id": authority["suite_id"],
        "status": authority["status"],
        "provenance": authority["provenance"],
        "proof_layer": authority["proof_layer"],
        "applicability": authority["applicability"],
        "case_count": len(normalized),
        "criterion_count": sum(len(case["criterion_ids"]) for case in normalized),
        "multi_turn_case_ids": [
            case["id"] for case in normalized if len(case["turn_ids"]) > 1
        ],
        "categories": {
            category: next(case["id"] for case in normalized if case["category"] == category)
            for category in sorted(EXPECTED_CATEGORIES)
        },
        "cases": normalized,
        "runtime_exclusion": True,
    }
    if (root / FREEZE_MANIFEST).exists():
        validate_freeze_manifest(root, document)
    return document


def serialized_document(root: Path) -> str:
    return json.dumps(build_document(root), indent=2, ensure_ascii=False) + "\n"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument("--root", type=Path, default=REPOSITORY_ROOT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    output = root / OUTPUT_FILE
    try:
        expected = serialized_document(root)
    except FreezeError as error:
        print(f"FAIL [GOAL_REVIEW_FREEZE_INVALID]: {error}")
        return 1
    if args.write:
        output.write_text(expected, encoding="utf-8")
        print(f"WROTE {output.relative_to(root)}")
        return 0
    if not output.is_file() or output.read_text(encoding="utf-8") != expected:
        print(f"FAIL [GOAL_REVIEW_FREEZE_STALE]: {output.relative_to(root)}")
        return 1
    document = build_document(root)
    print(
        "PASS [GOAL_REVIEW_FREEZE_CURRENT]: "
        f"{document['case_count']} cases, {document['criterion_count']} criteria"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
