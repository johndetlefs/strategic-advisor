#!/usr/bin/env python3
"""Validate and build the frozen EPIC-007 goal-review case inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
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
PARENT_ROOT = TASK_ROOT.parent
PARENT_REQUIREMENTS = PARENT_ROOT / "REQUIREMENTS.md"
INTENT_AUDIT = PARENT_ROOT / "INTENT-AUDIT.json"
DISTRIBUTION = Path("distribution.json")
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
EXPECTED_CONTROL_PAIRS = {
    "QUESTION_GATE": ("SAGR-003", "SAGR-004"),
    "FORK_AUTHORITY": ("SAGR-005", "SAGR-006"),
    "GOAL_CHANGE_BURDEN": ("SAGR-015", "SAGR-016"),
}
EXPECTED_STATE_ASSERTIONS = {
    "SAGR-007": {"REOPEN_OUTCOME_AFTER_EVIDENCE", "RESUME_CONFIRMED_OUTCOME"},
    "SAGR-008": {"INVALIDATE_SCOPE_DEPENDENT_EVIDENCE"},
}


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


def _substantive(value: object, label: str, minimum: int) -> str:
    text = _nonempty(value, label)
    if len(text) < minimum:
        raise FreezeError(f"{label} must contain at least {minimum} characters")
    return text


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

    control_pairs = authority.get("control_pairs")
    if not isinstance(control_pairs, list):
        raise FreezeError("control_pairs must be an array")
    pair_ids = [
        pair.get("id") if isinstance(pair, dict) else None for pair in control_pairs
    ]
    if set(pair_ids) != set(EXPECTED_CONTROL_PAIRS) or len(pair_ids) != len(
        EXPECTED_CONTROL_PAIRS
    ):
        raise FreezeError("control_pairs differ from the approved contrasts")
    pair_membership: dict[str, list[str]] = {case_id: [] for case_id in EXPECTED_IDS}
    for pair in control_pairs:
        if not isinstance(pair, dict):
            raise FreezeError("every control pair must be an object")
        pair_id = _nonempty(pair.get("id"), "control pair id")
        case_ids = pair.get("case_ids")
        if not isinstance(case_ids, list) or tuple(case_ids) != EXPECTED_CONTROL_PAIRS[pair_id]:
            raise FreezeError(f"{pair_id} case_ids differ from the approved contrast")
        _substantive(pair.get("discriminator"), f"{pair_id} discriminator", 80)
        for case_id in case_ids:
            pair_membership[case_id].append(pair_id)

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
        turn_ids: list[str] = []
        for index, turn in enumerate(turns, start=1):
            if not isinstance(turn, dict):
                raise FreezeError(f"{case_id} turn must be an object")
            turn_id = _nonempty(turn.get("id"), f"{case_id} turn id")
            if turn_id != f"T{index}":
                raise FreezeError(f"{case_id} turns must be ordered T1..T{len(turns)}")
            _substantive(turn.get("user"), f"{case_id} {turn_id} user", 40)
            if turn_id in turn_ids:
                raise FreezeError(f"{case_id} duplicate turn id {turn_id}")
            turn_ids.append(turn_id)

        criteria = case.get("criteria")
        if not isinstance(criteria, list) or not criteria:
            raise FreezeError(f"{case_id} criteria must be a non-empty array")
        criterion_ids: list[str] = []
        for criterion in criteria:
            if not isinstance(criterion, dict):
                raise FreezeError(f"{case_id} criterion must be an object")
            criterion_id = _nonempty(criterion.get("id"), f"{case_id} criterion id")
            _substantive(
                criterion.get("requirement"),
                f"{case_id} {criterion_id} requirement",
                60,
            )
            review_turns = criterion.get("review_turns")
            if not isinstance(review_turns, list) or not review_turns:
                raise FreezeError(f"{case_id} {criterion_id} review_turns are required")
            if any(turn_id not in turn_ids for turn_id in review_turns):
                raise FreezeError(
                    f"{case_id} {criterion_id} references an unknown review turn"
                )
            if len(review_turns) != len(set(review_turns)) or review_turns != sorted(
                review_turns, key=turn_ids.index
            ):
                raise FreezeError(
                    f"{case_id} {criterion_id} review_turns must be unique and ordered"
                )
            if criterion_id in seen_criteria:
                raise FreezeError(f"duplicate criterion id {criterion_id}")
            seen_criteria.add(criterion_id)
            criterion_ids.append(criterion_id)

        state_assertions = case.get("state_assertions", [])
        if not isinstance(state_assertions, list):
            raise FreezeError(f"{case_id} state_assertions must be an array")
        state_ids: list[str] = []
        for assertion in state_assertions:
            if not isinstance(assertion, dict):
                raise FreezeError(f"{case_id} state assertion must be an object")
            assertion_id = _nonempty(assertion.get("id"), f"{case_id} state id")
            after_turn = _nonempty(
                assertion.get("after_turn"), f"{case_id} {assertion_id} after_turn"
            )
            if after_turn not in turn_ids:
                raise FreezeError(
                    f"{case_id} {assertion_id} references an unknown state turn"
                )
            for field in ("preserve", "invalidate", "set"):
                values = assertion.get(field)
                if not isinstance(values, list) or not values:
                    raise FreezeError(
                        f"{case_id} {assertion_id} {field} must be a non-empty array"
                    )
                for value in values:
                    _substantive(value, f"{case_id} {assertion_id} {field}", 12)
            _substantive(
                assertion.get("requirement"),
                f"{case_id} {assertion_id} requirement",
                60,
            )
            if assertion_id in state_ids:
                raise FreezeError(f"{case_id} duplicate state assertion {assertion_id}")
            state_ids.append(assertion_id)
        expected_state_ids = EXPECTED_STATE_ASSERTIONS.get(case_id, set())
        if set(state_ids) != expected_state_ids or len(state_ids) != len(expected_state_ids):
            raise FreezeError(f"{case_id} state assertions differ from the approved envelope")

        forbidden = case.get("forbidden_behaviors")
        if not isinstance(forbidden, list) or not forbidden:
            raise FreezeError(f"{case_id} forbidden_behaviors must be non-empty text")
        for index, behavior in enumerate(forbidden, start=1):
            _substantive(behavior, f"{case_id} forbidden behavior {index}", 20)
        normalized.append(
            {
                "id": case_id,
                "category": category,
                "title": title,
                "activation": activation,
                "turn_ids": turn_ids,
                "criterion_ids": criterion_ids,
                "state_assertion_ids": state_ids,
                "control_pair_ids": pair_membership[case_id],
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


def _git_output(root: Path, arguments: list[str], label: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise FreezeError(f"cannot resolve {label}: {result.stderr.strip()}")
    return result.stdout.strip()


def validate_freeze_manifest(root: Path, inventory: dict[str, Any]) -> None:
    manifest = read_json(root / FREEZE_MANIFEST)
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise FreezeError("freeze manifest schema_version must be 1")
    if manifest.get("status") != "frozen-pre-treatment":
        raise FreezeError("freeze manifest status must be frozen-pre-treatment")
    authority_meta = manifest.get("authority")
    if not isinstance(authority_meta, dict):
        raise FreezeError("freeze manifest authority must be an object")
    requirements_match = re.search(
        r"^- Approved artifact identity: (sha256:[0-9a-f]{64})$",
        (root / PARENT_REQUIREMENTS).read_text(encoding="utf-8"),
        flags=re.MULTILINE,
    )
    if not requirements_match:
        raise FreezeError("approved parent requirements identity is unavailable")
    if authority_meta.get("requirements_identity") != requirements_match.group(1):
        raise FreezeError("freeze requirements identity is not the approved parent identity")
    intent_audit = read_json(root / INTENT_AUDIT)
    current_intent_identity = (
        intent_audit.get("artifact_identity") if isinstance(intent_audit, dict) else None
    )
    if authority_meta.get("intent_audit_identity") != current_intent_identity:
        raise FreezeError("freeze intent audit identity is not current")

    baseline = manifest.get("untreated_repository_baseline")
    if not isinstance(baseline, dict):
        raise FreezeError("untreated_repository_baseline must be an object")
    commit = _nonempty(baseline.get("source_commit"), "baseline source_commit")
    expected_tree = _nonempty(baseline.get("source_tree"), "baseline source_tree")
    actual_tree = _git_output(root, ["rev-parse", f"{commit}^{{tree}}"], "baseline tree")
    if actual_tree != expected_tree:
        raise FreezeError(
            f"baseline source_tree mismatch: expected {expected_tree}, got {actual_tree}"
        )
    distribution = read_json(root / DISTRIBUTION)
    current_public = (
        distribution.get("current_public") if isinstance(distribution, dict) else None
    )
    if not isinstance(current_public, dict):
        raise FreezeError("distribution current_public identity is unavailable")
    distribution_bindings = {
        "current_public_version": "version",
        "current_public_tag": "tag",
        "current_public_source_revision": "source_revision",
        "current_public_runtime_package_identity_sha256": (
            "runtime_package_identity_sha256"
        ),
    }
    for baseline_key, distribution_key in distribution_bindings.items():
        if baseline.get(baseline_key) != current_public.get(distribution_key):
            raise FreezeError(f"{baseline_key} differs from distribution.json")
    tag_commit = _git_output(
        root,
        ["rev-list", "-n", "1", str(baseline["current_public_tag"])],
        "public tag commit",
    )
    if tag_commit != baseline["current_public_source_revision"]:
        raise FreezeError("public tag does not resolve to the recorded source revision")
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

    support_artifacts = manifest.get("frozen_support_artifacts")
    if not isinstance(support_artifacts, list) or not support_artifacts:
        raise FreezeError("frozen_support_artifacts must be a non-empty array")
    for record in support_artifacts:
        if not isinstance(record, dict):
            raise FreezeError("frozen support artifact must be an object")
        path = _nonempty(record.get("path"), "support artifact path")
        expected = _nonempty(record.get("sha256"), f"{path} sha256")
        actual = _sha256((root / path).read_bytes())
        if actual != expected:
            raise FreezeError(
                f"frozen support hash mismatch for {path}: expected {expected}, got {actual}"
            )

    execution = manifest.get("execution_identity_contract")
    if not isinstance(execution, dict):
        raise FreezeError("execution_identity_contract must be an object")
    for field in ("model", "host", "host_version", "baseline_result_path"):
        _nonempty(execution.get(field), f"execution identity {field}")
    try:
        baseline_result = json.loads(
            _git_blob(root, commit, str(execution["baseline_result_path"]))
        )
    except json.JSONDecodeError as error:
        raise FreezeError(f"baseline result is not valid JSON: {error}") from error
    baseline_target = (
        baseline_result.get("target") if isinstance(baseline_result, dict) else None
    )
    if not isinstance(baseline_target, dict):
        raise FreezeError("baseline result target identity is unavailable")
    for manifest_key, target_key in (
        ("model", "model"),
        ("host", "host"),
        ("host_version", "cli_version"),
    ):
        if execution.get(manifest_key) != baseline_target.get(target_key):
            raise FreezeError(
                f"execution identity {manifest_key} differs from the alpha.6 baseline"
            )
    baseline_runtime = _nonempty(
        baseline_target.get("runtime_package_identity_sha256"),
        "baseline result runtime identity",
    )
    if execution.get("baseline_runtime_package_identity_sha256") != baseline_runtime:
        raise FreezeError("execution baseline runtime identity differs from run-009")
    if baseline_runtime != baseline["current_public_runtime_package_identity_sha256"]:
        raise FreezeError("run-009 did not exercise the current public runtime identity")
    if execution.get("treatment_runtime_identity_state") != "must-freeze-before-first-output":
        raise FreezeError("treatment runtime identity must fail closed before generation")

    freeze_scope = manifest.get("freeze_scope")
    if not isinstance(freeze_scope, dict):
        raise FreezeError("freeze_scope must be an object")
    scope_commit = _nonempty(freeze_scope.get("authority_commit"), "scope commit")
    allowed_prefixes = freeze_scope.get("allowed_prefixes")
    if not isinstance(allowed_prefixes, list) or not allowed_prefixes:
        raise FreezeError("freeze_scope allowed_prefixes must be a non-empty array")
    changed = _git_output(
        root,
        ["diff", "--name-only", commit, scope_commit],
        "pre-treatment changed paths",
    ).splitlines()
    if any(
        not any(path == prefix or path.startswith(f"{prefix}/") for prefix in allowed_prefixes)
        for path in changed
    ):
        raise FreezeError("freeze authority commit contains treatment or unrelated paths")
    changed_digest = _sha256(("\n".join(changed) + "\n").encode("utf-8"))
    if freeze_scope.get("changed_paths_sha256") != changed_digest:
        raise FreezeError("freeze_scope changed path identity is stale")
    if freeze_scope.get("changed_path_count") != len(changed):
        raise FreezeError("freeze_scope changed path count is stale")


def build_document(root: Path, *, validate_manifest: bool = True) -> dict[str, Any]:
    authority = read_json(root / AUTHORITY_FILE)
    normalized = validate_authority(authority)
    runtime_manifest = read_json(root / RUNTIME_MANIFEST)
    includes = runtime_manifest.get("include") if isinstance(runtime_manifest, dict) else None
    if not isinstance(includes, list):
        raise FreezeError("runtime manifest include list is invalid")
    forbidden_runtime_names = {
        AUTHORITY_FILE.name,
        OUTPUT_FILE.name,
        FREEZE_MANIFEST.name,
        "CLAIM-PROOF-MATRIX.md",
        "PROVENANCE-REVIEW.md",
    }
    if any(
        any(name in str(path) for name in forbidden_runtime_names) for path in includes
    ):
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
        "stateful_case_ids": [
            case["id"] for case in normalized if case["state_assertion_ids"]
        ],
        "state_assertion_count": sum(
            len(case["state_assertion_ids"]) for case in normalized
        ),
        "control_pairs": {
            pair["id"]: pair["case_ids"] for pair in authority["control_pairs"]
        },
        "categories": {
            category: next(case["id"] for case in normalized if case["category"] == category)
            for category in sorted(EXPECTED_CATEGORIES)
        },
        "cases": normalized,
        "runtime_exclusion": True,
    }
    if validate_manifest and (root / FREEZE_MANIFEST).exists():
        validate_freeze_manifest(root, document)
    return document


def serialized_document(root: Path, *, validate_manifest: bool = True) -> str:
    return (
        json.dumps(
            build_document(root, validate_manifest=validate_manifest),
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


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
        expected = serialized_document(root, validate_manifest=not args.write)
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
