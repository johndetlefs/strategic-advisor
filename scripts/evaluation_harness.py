#!/usr/bin/env python3
"""Freeze, plan, and verify Strategic Advisor evaluation artifacts.

This tool is deliberately model-agnostic: it never launches or calls a model.
It establishes the immutable authority envelope, creates deterministic work
units for an external runner, and verifies retained artifacts fail-closed.

The verifier currently proves the generation, two-pass condition-masked quality
scoring, and separate condition-audit matrix. It can fail the release gate for
confirmed skilled hard-gate failures or systematic structure-only leakage, but
it never emits a passing effectiveness verdict. Full score aggregation,
assertion grading, trigger evaluation, and sealed-holdout evaluation remain
separate required work.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import hmac
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Sequence


DEFAULT_TEMPLATE = "skills/strategic-advisor/evals/freeze-manifest.template.json"
DEFAULT_EVALS = "skills/strategic-advisor/evals/evals.json"
FREEZE_SCHEMA_VERSION = 3
HEX_40 = re.compile(r"^[0-9a-f]{40}$")
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
ITERATION_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
RUN_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
UTC_TIMESTAMP = re.compile(
    r"^(?:19|20)\d{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])T"
    r"(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\dZ$"
)

DIMENSIONS = (
    "reality_fidelity",
    "premise_challenge",
    "causal_world_models",
    "leverage_prioritisation",
    "uncertainty_action_calibration",
    "agency_power_execution",
    "privacy_permission_sources",
    "decision_usefulness",
)
HARD_GATES = tuple(f"HG{number:02d}" for number in range(1, 19))
CONDITIONS = ("skilled", "control")
QUALITY_PASSES = ("score-1", "score-2")
AUDIT_MODES = ("structure-only", "full-response")
REQUIRED_FREEZE_IDENTITY_KEYS = (
    "authority_source_commit",
    "freeze_commit_sha",
    "freeze_manifest_sha256",
    "runtime_package_identity_sha256",
    "runtime_package_manifest_sha256",
)
FORBIDDEN_PRE_FREEZE_PARTS = {
    "adjudications",
    "assertion-grades",
    "condition-audits",
    "generations",
    "quality-scores",
    "raw-outputs",
    "results",
    "runs",
    "scores",
    "trigger-results",
}
FORBIDDEN_PRE_FREEZE_NAMES = {
    "result.json",
    "run-plan.json",
    "verification-result.json",
}
CONFIGURABLE_TOP_LEVEL = {
    "condition_audit",
    "generation",
    "scoring",
    "sealed_holdout",
}
UNSUPPORTED_RELEASE_COMPONENTS = [
    "case_assertion_grading",
    "dimension_and_hard_gate_adjudication",
    "final_score_resolution",
    "full_statistical_aggregation",
    "parser_retry_artifact_chains",
    "sealed_holdout_evaluation",
    "trigger_evaluation",
]
FORBIDDEN_FROZEN_INPUT_PARTS = {
    "adjudications",
    "assertion-grades",
    "condition-audits",
    "evals",
    "fixtures",
    "generations",
    "quality-scores",
    "raw-outputs",
    "results",
    "runs",
    "scores",
    "trigger-results",
}
FORBIDDEN_FROZEN_INPUT_MARKERS = (
    '"expected_decision_properties"',
    '"forbidden_behaviors"',
    '"not_applicable_dimensions"',
    '"probe_tags"',
    "condition-auditor-prompt",
    "freeze-manifest.json",
    "hmac-sha256-mask-v1",
    "skills/strategic-advisor/evals/",
    "strategic-advisor-scorer-v",
)
APPARENT_IDENTITY_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE | re.DOTALL)
    for pattern in (
        r"\b(?:response|candidate|answer|output)\s+[ab]\b.{0,60}\b"
        r"(?:appears?|seems?|looks?|likely|probably|clearly|obviously|is|was)\b"
        r".{0,40}\b(?:skilled|control|treatment|skill[- ](?:enabled|using|based)|"
        r"used\s+(?:the\s+)?skill)\b",
        r"\b(?:because|since|as)\b.{0,80}\b(?:used|uses|using|had|has)\s+"
        r"(?:access\s+to\s+)?(?:the\s+)?(?:strategic\s+advisor\s+)?skill\b",
        r"\b(?:apparent|inferred|guessed|likely)\s+(?:condition|origin|skill\s+identity)\b",
        r"\b(?:condition|skill)\s+(?:identity|mapping|label)\b",
        r"\b(?:treatment|control)\s+(?:condition|response|candidate|output)\b",
        r"\b(?:recognisable|recognizable)\s+as\s+(?:the\s+)?"
        r"(?:skilled|skill[- ]enabled|treatment)\b",
    )
)
DIRECT_IDENTITY_RATING_PATTERNS = tuple(
    re.compile(pattern, re.DOTALL)
    for pattern in (
        r"(?i:\b(?:response|candidate|answer|output)\s+)?"
        r"(?<![A-Za-z0-9])[AB](?![A-Za-z0-9])\s+"
        r"(?i:(?:is|was)\s+(?:the\s+)?(?:skilled|skill[- ]enabled|treatment)|"
        r"(?:used|uses|is\s+using|was\s+using)\s+(?:the\s+)?"
        r"(?:strategic\s+advisor|skill))\b.{0,80}?"
        r"(?i:\b(?:so|therefore|thus|hence|as\s+a\s+result|which\s+is\s+why)\b)"
        r".{0,80}?\b(?i:rat(?:e|ed|ing)|scor(?:e|ed|es|ing)|higher|lower)\b",
        r"\b(?i:rat(?:e|ed|ing)|scor(?:e|ed|es|ing))\b.{0,50}?"
        r"(?i:\b(?:response|candidate|answer|output)\s+)?"
        r"(?<![A-Za-z0-9])[AB](?![A-Za-z0-9]).{0,80}?"
        r"(?i:\b(?:because|since|as)\b).{0,80}?"
        r"(?i:(?:is|was)\s+(?:the\s+)?(?:skilled|skill[- ]enabled|treatment)|"
        r"(?:used|uses|using|had\s+access\s+to)\s+(?:the\s+)?"
        r"(?:strategic\s+advisor|skill))\b",
    )
)
FORBIDDEN_CONFIGURATION_KEY_MARKERS = (
    "answer",
    "answer_key",
    "assertion",
    "condition",
    "condition_label",
    "condition_mapping",
    "expected_",
    "evaluation",
    "forbidden",
    "forbidden_behavior",
    "gold_answer",
    "ground_truth",
    "outcome",
    "hidden_answer",
    "reference_answer",
    "skill_mapping",
    "treatment",
    "treatment_mapping",
)
FORBIDDEN_CONFIGURATION_VALUE_MARKERS = (
    "base-a",
    "base-b",
    "condition_guess",
    "control condition",
    "expected decision",
    "hidden answer",
    "skill-enabled condition",
    "skilled condition",
    "treatment condition",
)
CONFIGURATION_SKILLED_IDENTITY_TOKENS = frozenset(
    {
        "skilled",
        "skillenabled",
        "treatment",
    }
)
CONFIGURATION_CONTROL_IDENTITY_TOKENS = frozenset(
    {
        "baseline",
        "control",
        "noskill",
        "skilldisabled",
        "unskilled",
        "withoutskill",
    }
)
CONFIGURATION_DIRECT_MAPPING_PATTERNS = tuple(
    re.compile(pattern)
    for pattern in (
        r"(?i:\b(?:response|candidate|answer|output)\s+)?"
        r"(?<![A-Za-z0-9])[AB](?![A-Za-z0-9])\s*"
        r"(?i:(?:is|=|:|means?|maps?\s+to)\s+(?:the\s+)?)"
        r"(?i:skilled|control|baseline|treatment|skill[- _]?enabled|"
        r"skill[- _]?disabled|unskilled|no[- _]?skill|without\s+(?:the\s+)?skill)\b",
        r"\b(?i:skilled|control|baseline|treatment|skill[- _]?enabled|"
        r"skill[- _]?disabled|unskilled|no[- _]?skill|without\s+(?:the\s+)?skill)"
        r"\s*(?i:=|:|maps?\s+to|means?)\s*"
        r"(?i:(?:response|candidate|answer|output)\s+)?"
        r"(?<![A-Za-z0-9])[AB](?![A-Za-z0-9])",
    )
)


class HarnessError(ValueError):
    """Raised when an evaluation invariant cannot be proved."""


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def rendered_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise HarnessError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json_bytes(value: bytes, label: str) -> Any:
    try:
        text = value.decode("utf-8")
    except UnicodeDecodeError as error:
        raise HarnessError(f"{label} is not UTF-8: {error}") from error
    try:
        return json.loads(text, object_pairs_hook=reject_duplicate_keys)
    except json.JSONDecodeError as error:
        raise HarnessError(f"{label} is not valid JSON: {error}") from error


def normalized_relative_path(raw: object, label: str) -> PurePosixPath:
    if not isinstance(raw, str) or not raw or "\\" in raw:
        raise HarnessError(f"{label} must be a non-empty POSIX relative path")
    path = PurePosixPath(raw)
    if (
        path.is_absolute()
        or "." in path.parts
        or ".." in path.parts
        or raw != path.as_posix()
    ):
        raise HarnessError(f"{label} is not a normalized relative path: {raw}")
    return path


def relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def regular_repo_file(source_root: Path, raw: object, label: str) -> Path:
    relative = normalized_relative_path(raw, label)
    source_root = source_root.resolve()
    current = source_root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise HarnessError(f"{label} traverses a symlink: {relative}")
    if not current.is_file():
        raise HarnessError(f"{label} is not a regular file: {relative}")
    resolved = current.resolve()
    if not relative_to(resolved, source_root):
        raise HarnessError(f"{label} escapes the source repository: {relative}")
    return current


def repo_relative(source_root: Path, path: Path, label: str) -> PurePosixPath:
    source_root = source_root.resolve()
    absolute = path.absolute()
    if absolute.is_symlink():
        raise HarnessError(f"{label} cannot be a symlink: {absolute}")
    try:
        relative = absolute.resolve(strict=False).relative_to(source_root)
    except ValueError as error:
        raise HarnessError(f"{label} must be inside the source repository") from error
    return normalized_relative_path(relative.as_posix(), label)


def load_json_file(path: Path, label: str) -> tuple[Any, bytes]:
    if path.is_symlink() or not path.is_file():
        raise HarnessError(f"{label} is not a regular file: {path}")
    value = path.read_bytes()
    return load_json_bytes(value, label), value


def run_git(source_root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(source_root), *arguments],
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise HarnessError(f"git {' '.join(arguments)}: {detail}")
    return result.stdout.strip()


def validate_commit(source_root: Path, commit: str, label: str) -> str:
    if not isinstance(commit, str) or HEX_40.fullmatch(commit) is None:
        raise HarnessError(f"{label} must be exactly 40 lowercase hexadecimal characters")
    resolved = run_git(source_root, "rev-parse", "--verify", f"{commit}^{{commit}}")
    if resolved != commit:
        raise HarnessError(f"{label} does not resolve to itself: {commit}")
    return run_git(source_root, "rev-parse", f"{commit}^{{tree}}")


def assert_authority_checkout(source_root: Path, commit: str) -> tuple[str, set[str]]:
    head = run_git(source_root, "rev-parse", "HEAD")
    if head != commit:
        raise HarnessError(
            f"authority checkout HEAD {head} does not equal authority_source_commit {commit}"
        )
    tracked = set(
        filter(None, run_git(source_root, "diff", "--name-only", "HEAD", "--").splitlines())
    )
    tracked.update(
        filter(
            None,
            run_git(source_root, "diff", "--cached", "--name-only", "HEAD", "--").splitlines(),
        )
    )
    if tracked:
        raise HarnessError(
            "authority checkout has tracked changes before freeze: "
            + ", ".join(sorted(tracked))
        )
    untracked = set(
        filter(
            None,
            run_git(source_root, "ls-files", "--others", "--exclude-standard").splitlines(),
        )
    )
    return run_git(source_root, "rev-parse", "HEAD^{tree}"), untracked


def write_new_file(path: Path, content: bytes, label: str) -> None:
    if path.exists() or path.is_symlink():
        raise HarnessError(f"{label} already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor: int | None = None
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = None
            stream.write(content)
    except Exception:
        if descriptor is not None:
            os.close(descriptor)
        if path.exists() and not path.is_symlink():
            path.unlink()
        raise


def deep_merge_strict(base: Any, override: Any, label: str = "config") -> Any:
    if not isinstance(override, dict):
        raise HarnessError(f"{label} must be a JSON object")
    if not isinstance(base, dict):
        raise HarnessError(f"{label} cannot replace a non-object authority value")
    if not base:
        return copy.deepcopy(override)
    unknown = sorted(set(override) - set(base))
    if unknown:
        raise HarnessError(f"{label} contains unknown keys: {', '.join(unknown)}")
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge_strict(merged[key], value, f"{label}.{key}")
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def require_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise HarnessError(f"{label} must be a non-empty string")
    return value


def require_hex_64(value: Any, label: str) -> str:
    if not isinstance(value, str) or HEX_64.fullmatch(value) is None:
        raise HarnessError(f"{label} must be exactly 64 lowercase hexadecimal characters")
    return value


def parse_utc_timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or UTC_TIMESTAMP.fullmatch(value) is None:
        raise HarnessError(f"{label} must be a second-resolution UTC timestamp")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as error:
        raise HarnessError(f"{label} is not a real calendar timestamp") from error
    return parsed.replace(tzinfo=timezone.utc)


def git_show_bytes(source_root: Path, commit: str, relative: str, label: str) -> bytes:
    normalized = normalized_relative_path(relative, label).as_posix()
    result = subprocess.run(
        ["git", "-C", str(source_root), "show", f"{commit}:{normalized}"],
        check=False,
        capture_output=True,
        timeout=20,
    )
    if result.returncode != 0:
        raise HarnessError(f"{label} is absent from commit {commit}: {normalized}")
    return result.stdout


def validate_config_override(config: Any) -> dict[str, Any]:
    if not isinstance(config, dict):
        raise HarnessError("freeze config must be a JSON object")
    forbidden = sorted(set(config) - CONFIGURABLE_TOP_LEVEL)
    if forbidden:
        raise HarnessError(
            "freeze config cannot override authority or protocol fields: "
            + ", ".join(forbidden)
        )

    generation = config.get("generation", {})
    if not isinstance(generation, dict):
        raise HarnessError("freeze config generation must be an object")
    allowed_generation = {
        "configuration",
        "frozen_context_artifacts",
        "host",
        "model",
        "model_version",
        "treatment_activation",
    }
    if set(generation) - allowed_generation:
        raise HarnessError("freeze config cannot override generation protocol fields")
    contexts = generation.get("frozen_context_artifacts", {})
    if not isinstance(contexts, dict):
        raise HarnessError("freeze config frozen_context_artifacts must be an object")
    allowed_contexts = {
        "declared_input_manifest",
        "non_treatment_context",
        "system_and_developer_context",
        "tool_policy",
    }
    if set(contexts) - allowed_contexts:
        raise HarnessError("freeze config contains an unknown frozen context artifact")
    for key, record in contexts.items():
        if not isinstance(record, dict) or set(record) != {"path"}:
            raise HarnessError(
                f"freeze config generation.{key} may set only its path"
            )
    activation = generation.get("treatment_activation", {})
    if not isinstance(activation, dict) or set(activation) - {
        "contract_path",
        "package_availability_proof",
    }:
        raise HarnessError("freeze config cannot override activation protocol fields")

    scoring = config.get("scoring", {})
    if not isinstance(scoring, dict):
        raise HarnessError("freeze config scoring must be an object")
    allowed_scoring = {
        "adjudication_configuration",
        "adjudication_model",
        "adjudication_model_version",
        "case_assertion_grading",
        "configuration",
        "host",
        "model",
        "model_version",
    }
    if set(scoring) - allowed_scoring:
        raise HarnessError("freeze config cannot override scoring protocol fields")
    assertion = scoring.get("case_assertion_grading", {})
    if not isinstance(assertion, dict) or set(assertion) - {
        "configuration",
        "host",
        "model",
        "model_version",
    }:
        raise HarnessError("freeze config cannot override assertion-grading protocol fields")

    audit = config.get("condition_audit", {})
    if not isinstance(audit, dict) or set(audit) - {
        "configuration",
        "host",
        "model",
        "model_version",
    }:
        raise HarnessError("freeze config cannot override condition-audit protocol fields")
    holdout = config.get("sealed_holdout", {})
    if not isinstance(holdout, dict) or set(holdout) - {
        "commitment_manifest_path",
        "independence_attestation_path",
    }:
        raise HarnessError("freeze config cannot override sealed-holdout protocol fields")
    return config


def authority_paths_from_template(template: Any, label: str) -> list[str]:
    if not isinstance(template, dict):
        raise HarnessError(f"{label} must be an object")
    records = template.get("authority_files")
    if not isinstance(records, list) or not records:
        raise HarnessError(f"{label} authority_files must be a non-empty array")
    paths: list[str] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict) or set(record) != {"path", "sha256"}:
            raise HarnessError(f"{label} authority_files[{index}] schema is invalid")
        path = normalized_relative_path(
            record.get("path"), f"{label} authority_files[{index}].path"
        ).as_posix()
        if path in paths:
            raise HarnessError(f"{label} contains duplicate authority path: {path}")
        paths.append(path)
    return paths


def require_exact_template_authority(
    manifest: dict[str, Any], template: dict[str, Any], label: str
) -> None:
    expected = authority_paths_from_template(template, "canonical freeze template")
    actual = authority_paths_from_template(manifest, label)
    if actual != expected:
        raise HarnessError(f"{label} authority_files differ from the canonical template")


def validate_runtime_manifest(
    source_root: Path, manifest_path: Path
) -> tuple[dict[str, Any], bytes]:
    parsed, manifest_bytes = load_json_file(manifest_path, "runtime package manifest")
    if not isinstance(parsed, dict) or parsed.get("schema_version") != 1:
        raise HarnessError("runtime package manifest schema_version must be 1")
    required = {
        "file_count",
        "files",
        "identity_algorithm",
        "package_identity_sha256",
        "package_root",
        "schema_version",
        "source_allowlist",
    }
    if set(parsed) != required:
        raise HarnessError("runtime package manifest has unexpected or missing keys")
    if parsed.get("identity_algorithm") != "sha256-canonical-json-v1":
        raise HarnessError("runtime package manifest identity algorithm is invalid")
    files = parsed.get("files")
    if not isinstance(files, list) or not files or parsed.get("file_count") != len(files):
        raise HarnessError("runtime package manifest file count is invalid")
    paths: list[str] = []
    for index, item in enumerate(files):
        if not isinstance(item, dict) or set(item) != {"path", "sha256", "size_bytes"}:
            raise HarnessError(f"runtime package file[{index}] schema is invalid")
        path = normalized_relative_path(item.get("path"), f"runtime file[{index}].path")
        digest = item.get("sha256")
        size = item.get("size_bytes")
        if not isinstance(digest, str) or HEX_64.fullmatch(digest) is None:
            raise HarnessError(f"runtime package file[{index}] SHA-256 is invalid")
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise HarnessError(f"runtime package file[{index}] size is invalid")
        paths.append(path.as_posix())
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise HarnessError("runtime package paths must be sorted and unique")
    source_allowlist = parsed.get("source_allowlist")
    if not isinstance(source_allowlist, dict) or set(source_allowlist) != {"path", "sha256"}:
        raise HarnessError("runtime package source_allowlist schema is invalid")
    allowlist_file = regular_repo_file(
        source_root, source_allowlist.get("path"), "runtime source allowlist"
    )
    allowlist_bytes = allowlist_file.read_bytes()
    allowlist_hash = sha256_bytes(allowlist_bytes)
    if source_allowlist.get("sha256") != allowlist_hash:
        raise HarnessError("runtime package source allowlist hash does not match source")
    allowlist = load_json_bytes(allowlist_bytes, "runtime source allowlist")
    if (
        not isinstance(allowlist, dict)
        or allowlist.get("schema_version") != 1
        or allowlist.get("package_root") != "skills/strategic-advisor"
    ):
        raise HarnessError("runtime source allowlist schema or package root is invalid")
    includes = allowlist.get("include")
    if (
        not isinstance(includes, list)
        or not includes
        or len(includes) != len(set(includes))
        or not all(isinstance(item, str) for item in includes)
    ):
        raise HarnessError("runtime source allowlist include array is invalid")
    normalized_includes = sorted(
        normalized_relative_path(item, "runtime source include").as_posix()
        for item in includes
    )
    if paths != normalized_includes:
        raise HarnessError("runtime package provenance does not contain the exact allowlist")
    if parsed.get("package_root") != allowlist.get("package_root"):
        raise HarnessError("runtime package root does not match source allowlist")
    package_root = PurePosixPath(allowlist["package_root"])
    entries_by_path = {item["path"]: item for item in files}
    for relative in normalized_includes:
        source_relative = (package_root / PurePosixPath(relative)).as_posix()
        source_file = regular_repo_file(
            source_root, source_relative, f"runtime source {relative}"
        )
        source_bytes = source_file.read_bytes()
        entry = entries_by_path[relative]
        if (
            entry["sha256"] != sha256_bytes(source_bytes)
            or entry["size_bytes"] != len(source_bytes)
        ):
            raise HarnessError(f"runtime provenance disagrees with source bytes: {relative}")
    identity_payload = {
        "files": files,
        "schema_version": 1,
        "source_allowlist_sha256": allowlist_hash,
    }
    expected_identity = sha256_bytes(canonical_json_bytes(identity_payload))
    if parsed.get("package_identity_sha256") != expected_identity:
        raise HarnessError("runtime package aggregate identity is invalid")
    return parsed, manifest_bytes


def hash_artifact_reference(
    source_root: Path,
    record: Any,
    label: str,
    *,
    path_key: str = "path",
    hash_key: str = "sha256",
) -> str:
    if not isinstance(record, dict):
        raise HarnessError(f"{label} must be an object")
    path = regular_repo_file(source_root, record.get(path_key), f"{label}.{path_key}")
    digest = sha256_bytes(path.read_bytes())
    existing = record.get(hash_key)
    if existing not in ("", digest):
        raise HarnessError(f"{label}.{hash_key} conflicts with source bytes")
    record[hash_key] = digest
    return digest


def nested_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for child in value for item in nested_strings(child)]
    if isinstance(value, dict):
        return [item for child in value.values() for item in nested_strings(child)]
    return []


def evaluation_fingerprints(source_root: Path) -> set[str]:
    eval_root = source_root / "skills" / "strategic-advisor" / "evals"
    if eval_root.is_symlink() or not eval_root.is_dir():
        raise HarnessError("evaluation authority directory is missing or symlinked")
    fingerprints: set[str] = set()
    fingerprint_keys = {
        "assertions",
        "expected_decision_properties",
        "expected_diagnosis",
        "forbidden_behaviors",
        "forbidden_decision_properties",
        "prompt",
        "query",
        "required_decision_properties",
    }
    for path in sorted(eval_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md"}:
            continue
        if path.is_symlink():
            raise HarnessError(f"evaluation authority is symlinked: {path}")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            raise HarnessError(f"evaluation authority is not UTF-8: {path}") from error
        if path.suffix.lower() == ".md":
            fingerprints.update(
                paragraph.strip()
                for paragraph in text.split("\n\n")
                if len(paragraph.strip()) >= 120
            )
            continue
        parsed = load_json_bytes(text.encode("utf-8"), f"evaluation authority {path}")

        def collect(value: Any) -> None:
            if isinstance(value, dict):
                for key, child in value.items():
                    if key in fingerprint_keys:
                        fingerprints.update(
                            item.strip()
                            for item in nested_strings(child)
                            if len(item.strip()) >= 60
                        )
                    collect(child)
            elif isinstance(value, list):
                for child in value:
                    collect(child)

        collect(parsed)
    return fingerprints


def validate_frozen_input(
    source_root: Path,
    raw_path: Any,
    label: str,
    authority_paths: set[str],
    fingerprints: set[str],
) -> Path:
    relative = normalized_relative_path(raw_path, f"{label}.path")
    relative_string = relative.as_posix()
    lowered_parts = {part.lower() for part in relative.parts}
    if (
        relative_string in authority_paths
        or lowered_parts & FORBIDDEN_FROZEN_INPUT_PARTS
        or relative.parts[:3] == ("skills", "strategic-advisor", "evals")
    ):
        raise HarnessError(f"{label} path crosses the evaluation/result boundary")
    path = regular_repo_file(source_root, relative_string, f"{label}.path")
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise HarnessError(f"{label} must be UTF-8 text or JSON") from error
    lowered = text.lower()
    if any(marker in lowered for marker in FORBIDDEN_FROZEN_INPUT_MARKERS):
        raise HarnessError(f"{label} contains evaluation/result control material")
    if any(fingerprint in text for fingerprint in fingerprints):
        raise HarnessError(f"{label} contains a frozen evaluation fingerprint")
    if path.suffix.lower() == ".json":
        parsed = load_json_bytes(text.encode("utf-8"), label)
        forbidden_keys = {
            "assertions",
            "expected_decision_properties",
            "forbidden_behaviors",
            "not_applicable_dimensions",
            "probe_tags",
        }

        def contains_forbidden_key(value: Any) -> bool:
            if isinstance(value, dict):
                return bool(set(value) & forbidden_keys) or any(
                    contains_forbidden_key(child) for child in value.values()
                )
            if isinstance(value, list):
                return any(contains_forbidden_key(child) for child in value)
            return False

        if contains_forbidden_key(parsed):
            raise HarnessError(f"{label} contains evaluation authority fields")
    return path


def validate_configuration_boundary(
    value: Any,
    label: str,
    authority_paths: set[str],
    fingerprints: set[str],
) -> None:
    lowered_authority_paths = {path.lower() for path in authority_paths}
    compact_key_markers = {
        re.sub(r"[^a-z0-9]", "", marker.lower())
        for marker in FORBIDDEN_CONFIGURATION_KEY_MARKERS
    }

    def identity_kind(item: Any) -> str | None:
        if not isinstance(item, str):
            return None
        compact = re.sub(r"[^a-z0-9]", "", item.lower())
        if compact in CONFIGURATION_SKILLED_IDENTITY_TOKENS:
            return "skilled"
        if compact in CONFIGURATION_CONTROL_IDENTITY_TOKENS:
            return "control"
        return None

    def reject_paired_identity_values(item: Any, path: str) -> None:
        if isinstance(item, dict):
            direct_values = item.values()
        elif isinstance(item, list):
            direct_values = item
        else:
            return
        kinds = {kind for child in direct_values if (kind := identity_kind(child))}
        if kinds == {"skilled", "control"}:
            raise HarnessError(
                f"{path} contains a direct condition or skill mapping pair"
            )

    def scan(item: Any, path: str) -> None:
        if isinstance(item, dict):
            reject_paired_identity_values(item, path)
            for key, child in item.items():
                if not isinstance(key, str):
                    raise HarnessError(f"{path} contains a non-string configuration key")
                lowered_key = key.lower()
                compact_key = re.sub(r"[^a-z0-9]", "", lowered_key)
                if any(marker in compact_key for marker in compact_key_markers):
                    raise HarnessError(
                        f"{path} contains hidden outcome or mapping key: {key}"
                    )
                if any(authority_path in lowered_key for authority_path in lowered_authority_paths):
                    raise HarnessError(f"{path} key references evaluation authority")
                scan(child, f"{path}.{key}")
            return
        if isinstance(item, list):
            reject_paired_identity_values(item, path)
            for index, child in enumerate(item):
                scan(child, f"{path}[{index}]")
            return
        if isinstance(item, str):
            lowered = item.lower()
            if any(
                pattern.search(item)
                for pattern in CONFIGURATION_DIRECT_MAPPING_PATTERNS
            ):
                raise HarnessError(
                    f"{path} contains a direct condition or skill mapping phrase"
                )
            if (
                any(marker in lowered for marker in FORBIDDEN_FROZEN_INPUT_MARKERS)
                or any(marker in lowered for marker in FORBIDDEN_CONFIGURATION_VALUE_MARKERS)
                or any(authority_path in lowered for authority_path in lowered_authority_paths)
            ):
                raise HarnessError(f"{path} contains evaluation authority or hidden mapping material")
            if any(fingerprint in item for fingerprint in fingerprints):
                raise HarnessError(f"{path} contains a frozen evaluation fingerprint")
            return
        if item is not None and not isinstance(item, (bool, int, float)):
            raise HarnessError(f"{path} contains an unsupported configuration value")

    scan(value, label)


def validate_all_model_configurations(
    source_root: Path,
    manifest: dict[str, Any],
    authority_paths: set[str],
    fingerprints: set[str],
) -> None:
    configurations = (
        ("generation.configuration", manifest["generation"]["configuration"]),
        ("scoring.configuration", manifest["scoring"]["configuration"]),
        (
            "scoring.adjudication_configuration",
            manifest["scoring"]["adjudication_configuration"],
        ),
        (
            "scoring.case_assertion_grading.configuration",
            manifest["scoring"]["case_assertion_grading"]["configuration"],
        ),
        ("condition_audit.configuration", manifest["condition_audit"]["configuration"]),
    )
    for label, configuration in configurations:
        validate_configuration_boundary(
            configuration,
            label,
            authority_paths,
            fingerprints,
        )


def populate_frozen_artifact_hashes(source_root: Path, manifest: dict[str, Any]) -> set[str]:
    """Populate hashes for every non-authority artifact allowed before freeze."""

    allowed: set[str] = set()
    authority_paths = {
        record["path"] for record in manifest.get("authority_files", [])
        if isinstance(record, dict) and isinstance(record.get("path"), str)
    }
    fingerprints = evaluation_fingerprints(source_root)
    validate_all_model_configurations(
        source_root,
        manifest,
        authority_paths,
        fingerprints,
    )
    generation = manifest.get("generation")
    if not isinstance(generation, dict):
        raise HarnessError("generation configuration must be an object")
    context = generation.get("frozen_context_artifacts")
    expected_context = {
        "system_and_developer_context": "system_and_developer_context_sha256",
        "tool_policy": "tool_policy_sha256",
        "non_treatment_context": "non_treatment_context_sha256",
        "declared_input_manifest": "declared_input_manifest_sha256",
    }
    if not isinstance(context, dict) or set(context) != set(expected_context):
        raise HarnessError("generation.frozen_context_artifacts has invalid keys")
    for key, summary_hash_key in expected_context.items():
        validate_frozen_input(
            source_root,
            context[key].get("path") if isinstance(context[key], dict) else None,
            f"generation.{key}",
            authority_paths,
            fingerprints,
        )
        digest = hash_artifact_reference(source_root, context[key], f"generation.{key}")
        if generation.get(summary_hash_key) not in ("", digest):
            raise HarnessError(f"generation.{summary_hash_key} conflicts with artifact")
        generation[summary_hash_key] = digest
        allowed.add(context[key]["path"])

    activation = generation.get("treatment_activation")
    if not isinstance(activation, dict):
        raise HarnessError("generation.treatment_activation must be an object")
    contract = {
        "path": activation.get("contract_path"),
        "sha256": activation.get("contract_sha256"),
    }
    validate_frozen_input(
        source_root,
        contract["path"],
        "treatment activation contract",
        authority_paths,
        fingerprints,
    )
    digest = hash_artifact_reference(source_root, contract, "treatment activation contract")
    activation["contract_sha256"] = digest
    require_nonempty_string(
        activation.get("package_availability_proof"),
        "generation.treatment_activation.package_availability_proof",
    )
    allowed.add(contract["path"])

    holdout = manifest.get("sealed_holdout")
    if not isinstance(holdout, dict) or holdout.get("required") is not True:
        raise HarnessError("sealed holdout must be required")
    for prefix in ("commitment_manifest", "independence_attestation"):
        record = {
            "path": holdout.get(f"{prefix}_path"),
            "sha256": holdout.get(f"{prefix}_sha256"),
        }
        validate_frozen_input(
            source_root,
            record["path"],
            f"sealed_holdout.{prefix}",
            authority_paths,
            fingerprints,
        )
        digest = hash_artifact_reference(source_root, record, f"sealed_holdout.{prefix}")
        holdout[f"{prefix}_sha256"] = digest
        allowed.add(record["path"])
    return allowed


def validate_filled_configuration(manifest: dict[str, Any]) -> None:
    iteration = manifest.get("iteration")
    if not isinstance(iteration, str) or ITERATION_ID.fullmatch(iteration) is None:
        raise HarnessError("iteration must be a normalized lowercase identifier")
    generation = manifest.get("generation")
    if not isinstance(generation, dict):
        raise HarnessError("generation configuration is missing")
    for key in ("model", "model_version", "host"):
        require_nonempty_string(generation.get(key), f"generation.{key}")
    if not isinstance(generation.get("configuration"), dict):
        raise HarnessError("generation.configuration must be an object")
    draws = generation.get("draw_ids")
    if (
        not isinstance(draws, list)
        or len(draws) < 2
        or len(draws) != len(set(draws))
        or not all(isinstance(item, str) and RUN_ID.fullmatch(item) for item in draws)
        or generation.get("draws_per_condition_per_case") != len(draws)
    ):
        raise HarnessError("generation must define at least two unique draw IDs")

    scoring = manifest.get("scoring")
    if not isinstance(scoring, dict):
        raise HarnessError("scoring configuration is missing")
    for key in (
        "model",
        "model_version",
        "host",
        "adjudication_model",
        "adjudication_model_version",
    ):
        require_nonempty_string(scoring.get(key), f"scoring.{key}")
    if not isinstance(scoring.get("configuration"), dict) or not isinstance(
        scoring.get("adjudication_configuration"), dict
    ):
        raise HarnessError("scoring configurations must be objects")
    if scoring.get("pass_ids") != list(QUALITY_PASSES) or scoring.get("passes") != 2:
        raise HarnessError("scoring must use score-1 and score-2 exactly once")
    assertion = scoring.get("case_assertion_grading")
    if not isinstance(assertion, dict):
        raise HarnessError("case assertion grading configuration is missing")
    for key in ("model", "model_version", "host"):
        require_nonempty_string(assertion.get(key), f"case_assertion_grading.{key}")
    if not isinstance(assertion.get("configuration"), dict):
        raise HarnessError("case assertion grading configuration must be an object")

    audit = manifest.get("condition_audit")
    if not isinstance(audit, dict):
        raise HarnessError("condition_audit must be an object")
    for key in ("model", "model_version", "host"):
        require_nonempty_string(audit.get(key), f"condition_audit.{key}")
    if not isinstance(audit.get("configuration"), dict):
        raise HarnessError("condition_audit.configuration must be an object")
    if (
        audit.get("mode_ids") != list(AUDIT_MODES)
        or audit.get("passes_per_mode_per_pair") != 1
    ):
        raise HarnessError("condition_audit must use structure-only and full-response")
    gate = audit.get("structure_only_gate")
    if not isinstance(gate, dict) or (
        gate.get("minimum_determinate") != 20
        or gate.get("failure_accuracy_gte") != 0.7
    ):
        raise HarnessError("condition_audit structure-only gate is invalid")

    masking = manifest.get("masking")
    if not isinstance(masking, dict):
        raise HarnessError("masking configuration is missing")
    if (
        masking.get("algorithm_id") != "hmac-sha256-mask-v1"
        or masking.get("quality_pass_label_algorithm")
        != "inverse-ab-quality-pass-v1"
        or masking.get("audit_mapping_algorithm")
        != "hmac-sha256-condition-audit-map-v1"
    ):
        raise HarnessError("masking or presentation algorithm identity is invalid")
    require_hex_64(masking.get("masking_seed_hex"), "masking seed")
    aggregation = manifest.get("aggregation")
    if not isinstance(aggregation, dict):
        raise HarnessError("aggregation configuration is missing")
    require_hex_64(aggregation.get("bootstrap_seed_hex"), "bootstrap seed")
    if aggregation.get("bootstrap_resamples") != 10000:
        raise HarnessError("bootstrap_resamples must remain 10000")
    if (
        aggregation.get("algorithm_id")
        != "evaluation-cluster-paired-bootstrap-sha256-v1"
    ):
        raise HarnessError("aggregation algorithm identity is invalid")


def authority_hash_map(source_root: Path, manifest: dict[str, Any]) -> dict[str, str]:
    records = manifest.get("authority_files")
    if not isinstance(records, list) or not records:
        raise HarnessError("authority_files must be a non-empty array")
    paths: list[str] = []
    hashes: dict[str, str] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict) or set(record) != {"path", "sha256"}:
            raise HarnessError(f"authority_files[{index}] schema is invalid")
        relative = normalized_relative_path(record.get("path"), f"authority_files[{index}].path")
        if relative.as_posix() in paths:
            raise HarnessError(f"duplicate authority path: {relative}")
        path = regular_repo_file(source_root, relative.as_posix(), "authority file")
        digest = sha256_bytes(path.read_bytes())
        existing = record.get("sha256")
        if existing not in ("", digest):
            raise HarnessError(f"authority hash conflicts with source: {relative}")
        record["sha256"] = digest
        paths.append(relative.as_posix())
        hashes[relative.as_posix()] = digest
    return hashes


def bind_derived_authority_hashes(manifest: dict[str, Any], hashes: dict[str, str]) -> None:
    bindings = (
        ("skills/strategic-advisor/evals/SCORER-PROMPT.md", ("scoring", "scorer_prompt_sha256")),
        ("skills/strategic-advisor/evals/ADJUDICATOR-PROMPT.md", ("scoring", "adjudicator_prompt_sha256")),
        (
            "skills/strategic-advisor/evals/CASE-ASSERTION-GRADER-PROMPT.md",
            ("scoring", "case_assertion_grading", "prompt_sha256"),
        ),
        ("skills/strategic-advisor/evals/AGGREGATION.md", ("aggregation", "authority_sha256")),
    )
    if "condition_audit" in manifest:
        bindings += (
            (
                "skills/strategic-advisor/evals/CONDITION-AUDITOR-PROMPT.md",
                ("condition_audit", "prompt_sha256"),
            ),
            (
                "skills/strategic-advisor/evals/PROTOCOL.md",
                ("condition_audit", "structure_view", "authority_sha256"),
            ),
        )
    for path, keys in bindings:
        digest = hashes.get(path)
        if digest is None:
            raise HarnessError(f"derived authority path is not frozen: {path}")
        target: dict[str, Any] = manifest
        for key in keys[:-1]:
            child = target.get(key)
            if not isinstance(child, dict):
                raise HarnessError(f"authority hash destination is missing: {'.'.join(keys)}")
            target = child
        current = target.get(keys[-1])
        if current not in ("", digest):
            raise HarnessError(f"authority hash destination conflicts: {'.'.join(keys)}")
        target[keys[-1]] = digest


def validate_no_prefreeze_outputs(
    source_root: Path,
    freeze_output: Path,
    allowed_relative_paths: set[str],
) -> None:
    iteration_root = freeze_output.parent
    allowed = {
        (source_root / Path(*PurePosixPath(item).parts)).resolve()
        for item in allowed_relative_paths
    }
    if not iteration_root.exists():
        return
    if iteration_root.is_symlink() or not iteration_root.is_dir():
        raise HarnessError("iteration evidence root is not a real directory")
    for path in sorted(iteration_root.rglob("*")):
        relative_parts = {part.lower() for part in path.relative_to(iteration_root).parts}
        if relative_parts & FORBIDDEN_PRE_FREEZE_PARTS or path.name.lower() in FORBIDDEN_PRE_FREEZE_NAMES:
            raise HarnessError(f"pre-freeze output/result artifact exists: {path}")
        if path.is_symlink():
            raise HarnessError(f"pre-freeze iteration contains a symlink: {path}")
        if path.is_file() and path.resolve() not in allowed:
            raise HarnessError(f"unrecognized pre-freeze artifact exists: {path}")


def freeze(args: argparse.Namespace) -> dict[str, Any]:
    source_root = args.source_root.absolute()
    if source_root.is_symlink() or not source_root.is_dir():
        raise HarnessError(f"source root must be a real directory: {source_root}")
    if args.template != DEFAULT_TEMPLATE:
        raise HarnessError("freeze must use the canonical freeze manifest template")
    template_path = regular_repo_file(source_root, args.template, "freeze template")
    template, _ = load_json_file(template_path, "freeze template")
    if not isinstance(template, dict) or template.get("status") != "template-not-frozen":
        raise HarnessError("freeze template status must be template-not-frozen")
    if template.get("schema_version") != FREEZE_SCHEMA_VERSION:
        raise HarnessError(
            f"freeze template schema_version must be {FREEZE_SCHEMA_VERSION}"
        )
    manifest = copy.deepcopy(template)
    if args.config is not None:
        config_path = args.config.absolute()
        config, _ = load_json_file(config_path, "freeze config")
        manifest = deep_merge_strict(manifest, validate_config_override(config))
    require_exact_template_authority(manifest, template, "populated freeze manifest")

    commit = args.authority_source_commit
    commit_tree = validate_commit(source_root, commit, "authority_source_commit")
    checkout_tree, untracked_paths = assert_authority_checkout(source_root, commit)
    if checkout_tree != commit_tree:
        raise HarnessError("authority checkout tree differs from authority commit tree")
    if args.authority_source_tree is not None and args.authority_source_tree != commit_tree:
        raise HarnessError("provided authority_source_tree does not match Git")
    parse_utc_timestamp(args.frozen_at, "frozen_at")

    output_relative = repo_relative(source_root, args.output, "freeze output")
    iteration = manifest.get("iteration")
    expected_output = f"evidence/evaluations/{iteration}/freeze-manifest.json"
    if output_relative.as_posix() != expected_output:
        raise HarnessError(f"freeze output must be {expected_output}")
    envelope = manifest.get("freeze_envelope")
    if not isinstance(envelope, dict):
        raise HarnessError("freeze_envelope is missing")
    envelope["authority_source_commit"] = commit
    envelope["authority_source_tree"] = commit_tree
    envelope["freeze_manifest_path"] = expected_output
    manifest["status"] = "frozen"
    manifest["frozen_at"] = args.frozen_at
    manifest.setdefault("masking", {})["masking_seed_hex"] = args.masking_seed_hex
    manifest.setdefault("aggregation", {})["bootstrap_seed_hex"] = args.bootstrap_seed_hex

    runtime_relative = repo_relative(
        source_root, args.runtime_package_manifest, "runtime package manifest"
    )
    expected_runtime = f"evidence/evaluations/{iteration}/runtime-package-manifest.json"
    if runtime_relative.as_posix() != expected_runtime:
        raise HarnessError(f"runtime package manifest must be {expected_runtime}")
    runtime, runtime_bytes = validate_runtime_manifest(source_root, args.runtime_package_manifest)
    runtime_record = manifest.get("runtime_package")
    if not isinstance(runtime_record, dict):
        raise HarnessError("runtime_package freeze section is missing")
    package_manifest = runtime_record.get("package_manifest")
    if not isinstance(package_manifest, dict):
        raise HarnessError("runtime_package.package_manifest is missing")
    package_manifest["path"] = expected_runtime
    package_manifest["sha256"] = sha256_bytes(runtime_bytes)
    runtime_record["package_identity_sha256"] = runtime["package_identity_sha256"]
    runtime_record["source_allowlist"] = copy.deepcopy(runtime["source_allowlist"])

    hashes = authority_hash_map(source_root, manifest)
    bind_derived_authority_hashes(manifest, hashes)
    allowed_paths = populate_frozen_artifact_hashes(source_root, manifest)
    allowed_paths.add(expected_runtime)
    validate_filled_configuration(manifest)
    validate_no_prefreeze_outputs(source_root, args.output, allowed_paths)
    unexpected_untracked = untracked_paths - allowed_paths
    if unexpected_untracked:
        raise HarnessError(
            "authority checkout contains unrecognized untracked files before freeze: "
            + ", ".join(sorted(unexpected_untracked))
        )
    write_new_file(args.output, rendered_json_bytes(manifest), "freeze manifest")
    return {
        "authority_file_count": len(hashes),
        "authority_source_commit": commit,
        "authority_source_tree": commit_tree,
        "freeze_manifest_path": expected_output,
        "freeze_manifest_sha256": sha256_bytes(args.output.read_bytes()),
        "runtime_package_identity_sha256": runtime["package_identity_sha256"],
        "status": "frozen",
    }


def verify_manifest_hashes(source_root: Path, manifest: dict[str, Any]) -> dict[str, str]:
    records = manifest.get("authority_files")
    if not isinstance(records, list) or not records:
        raise HarnessError("frozen authority_files is missing")
    hashes: dict[str, str] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict) or set(record) != {"path", "sha256"}:
            raise HarnessError(f"frozen authority_files[{index}] schema is invalid")
        path = regular_repo_file(source_root, record.get("path"), "frozen authority file")
        actual = sha256_bytes(path.read_bytes())
        if record.get("sha256") != actual:
            raise HarnessError(f"frozen authority drift: {record.get('path')}")
        hashes[record["path"]] = actual
    return hashes


def referenced_prefreeze_paths(manifest: dict[str, Any]) -> set[str]:
    paths: set[str] = set()
    runtime = manifest["runtime_package"]["package_manifest"]["path"]
    paths.add(runtime)
    context = manifest["generation"]["frozen_context_artifacts"]
    for record in context.values():
        paths.add(record["path"])
    paths.add(manifest["generation"]["treatment_activation"]["contract_path"])
    paths.add(manifest["sealed_holdout"]["commitment_manifest_path"])
    paths.add(manifest["sealed_holdout"]["independence_attestation_path"])
    return paths


def frozen_artifact_records(manifest: dict[str, Any]) -> list[tuple[str, str, str]]:
    records: list[tuple[str, str, str]] = []
    runtime = manifest["runtime_package"]["package_manifest"]
    records.append(
        (runtime["path"], runtime["sha256"], "runtime package provenance")
    )
    context = manifest["generation"]["frozen_context_artifacts"]
    for key, record in context.items():
        records.append((record["path"], record["sha256"], f"generation.{key}"))
    activation = manifest["generation"]["treatment_activation"]
    records.append(
        (
            activation["contract_path"],
            activation["contract_sha256"],
            "treatment activation contract",
        )
    )
    holdout = manifest["sealed_holdout"]
    records.extend(
        (
            holdout[f"{prefix}_path"],
            holdout[f"{prefix}_sha256"],
            f"sealed_holdout.{prefix}",
        )
        for prefix in ("commitment_manifest", "independence_attestation")
    )
    return records


def verify_frozen_artifacts_in_commit(
    source_root: Path, manifest: dict[str, Any], freeze_commit: str
) -> None:
    for relative, expected_hash, label in frozen_artifact_records(manifest):
        if not isinstance(expected_hash, str) or HEX_64.fullmatch(expected_hash) is None:
            raise HarnessError(f"{label} frozen SHA-256 is invalid")
        current = regular_repo_file(source_root, relative, label).read_bytes()
        if sha256_bytes(current) != expected_hash:
            raise HarnessError(f"{label} working bytes disagree with the freeze manifest")
        committed = git_show_bytes(source_root, freeze_commit, relative, label)
        if committed != current:
            raise HarnessError(
                f"{label} is an uncommitted substitute for the frozen artifact"
            )


def verify_runtime_sources_in_authority_commit(
    source_root: Path,
    runtime_manifest: dict[str, Any],
    authority_commit: str,
) -> None:
    source_allowlist = runtime_manifest["source_allowlist"]
    allowlist_bytes = git_show_bytes(
        source_root,
        authority_commit,
        source_allowlist["path"],
        "runtime source allowlist",
    )
    if sha256_bytes(allowlist_bytes) != source_allowlist["sha256"]:
        raise HarnessError(
            "runtime source allowlist bytes in authority_source_commit disagree with provenance"
        )
    allowlist = load_json_bytes(allowlist_bytes, "committed runtime source allowlist")
    if not isinstance(allowlist, dict):
        raise HarnessError("committed runtime source allowlist must be an object")
    package_root = normalized_relative_path(
        allowlist.get("package_root"), "committed runtime package_root"
    )
    includes = allowlist.get("include")
    if not isinstance(includes, list):
        raise HarnessError("committed runtime source allowlist include array is invalid")
    normalized_includes = sorted(
        normalized_relative_path(item, "committed runtime include").as_posix()
        for item in includes
    )
    entries = runtime_manifest["files"]
    if [entry["path"] for entry in entries] != normalized_includes:
        raise HarnessError("runtime provenance differs from committed source allowlist")
    for entry in entries:
        source_relative = (package_root / PurePosixPath(entry["path"])).as_posix()
        committed = git_show_bytes(
            source_root,
            authority_commit,
            source_relative,
            f"runtime source {entry['path']}",
        )
        if (
            sha256_bytes(committed) != entry["sha256"]
            or len(committed) != entry["size_bytes"]
        ):
            raise HarnessError(
                f"runtime provenance disagrees with authority_source_commit bytes: {entry['path']}"
            )


def verify_freeze_manifest(
    source_root: Path, manifest_path: Path, freeze_commit: str
) -> dict[str, Any]:
    manifest, manifest_bytes = load_json_file(manifest_path, "freeze manifest")
    if not isinstance(manifest, dict) or manifest.get("status") != "frozen":
        raise HarnessError("freeze manifest status must be frozen")
    if manifest.get("schema_version") != FREEZE_SCHEMA_VERSION:
        raise HarnessError(
            f"freeze manifest schema_version must be {FREEZE_SCHEMA_VERSION}"
        )
    validate_filled_configuration(manifest)
    envelope = manifest.get("freeze_envelope")
    if not isinstance(envelope, dict):
        raise HarnessError("freeze_envelope is missing")
    authority_commit = envelope.get("authority_source_commit")
    expected_tree = envelope.get("authority_source_tree")
    actual_tree = validate_commit(source_root, authority_commit, "authority_source_commit")
    if expected_tree != actual_tree:
        raise HarnessError("authority_source_tree does not match Git authority commit")
    validate_commit(source_root, freeze_commit, "freeze_commit")
    parents = run_git(source_root, "show", "-s", "--format=%P", freeze_commit).split()
    if parents != [authority_commit]:
        raise HarnessError("freeze commit must have authority_source_commit as its sole parent")
    committed_template = load_json_bytes(
        git_show_bytes(
            source_root,
            authority_commit,
            DEFAULT_TEMPLATE,
            "canonical freeze template",
        ),
        "canonical freeze template from authority_source_commit",
    )
    require_exact_template_authority(
        manifest,
        committed_template,
        "frozen manifest",
    )
    output_relative = repo_relative(source_root, manifest_path, "freeze manifest")
    if envelope.get("freeze_manifest_path") != output_relative.as_posix():
        raise HarnessError("freeze manifest path does not match its envelope")

    authority_hashes = verify_manifest_hashes(source_root, manifest)
    for path, expected_hash in authority_hashes.items():
        committed_bytes = subprocess.run(
            ["git", "-C", str(source_root), "show", f"{authority_commit}:{path}"],
            check=False,
            capture_output=True,
            timeout=20,
        )
        if committed_bytes.returncode != 0:
            raise HarnessError(f"authority file is absent from authority commit: {path}")
        if sha256_bytes(committed_bytes.stdout) != expected_hash:
            raise HarnessError(f"authority commit bytes disagree with freeze: {path}")
    bind_derived_authority_hashes(manifest, authority_hashes)

    runtime_path = regular_repo_file(
        source_root,
        manifest.get("runtime_package", {}).get("package_manifest", {}).get("path"),
        "frozen runtime package manifest",
    )
    runtime, runtime_bytes = validate_runtime_manifest(source_root, runtime_path)
    frozen_runtime = manifest["runtime_package"]
    if frozen_runtime["package_manifest"].get("sha256") != sha256_bytes(runtime_bytes):
        raise HarnessError("runtime package provenance drift")
    if frozen_runtime.get("package_identity_sha256") != runtime.get("package_identity_sha256"):
        raise HarnessError("runtime package identity drift")
    if frozen_runtime.get("source_allowlist") != runtime.get("source_allowlist"):
        raise HarnessError("runtime source allowlist identity drift")
    verify_runtime_sources_in_authority_commit(
        source_root, runtime, authority_commit
    )

    copy_for_hashes = copy.deepcopy(manifest)
    populate_frozen_artifact_hashes(source_root, copy_for_hashes)
    if copy_for_hashes != manifest:
        raise HarnessError("frozen context, activation, or holdout artifact drift")

    verify_frozen_artifacts_in_commit(source_root, manifest, freeze_commit)

    allowed_changes = referenced_prefreeze_paths(manifest) | {output_relative.as_posix()}
    changed = set(
        filter(
            None,
            run_git(
                source_root,
                "diff",
                "--name-only",
                "--diff-filter=ACMRTD",
                authority_commit,
                freeze_commit,
            ).splitlines(),
        )
    )
    if not changed or not changed.issubset(allowed_changes):
        unexpected = sorted(changed - allowed_changes)
        raise HarnessError(
            "freeze commit changes files outside its envelope"
            + (f": {', '.join(unexpected)}" if unexpected else "")
        )
    committed_manifest = git_show_bytes(
        source_root,
        freeze_commit,
        output_relative.as_posix(),
        "freeze manifest",
    )
    if committed_manifest != manifest_bytes:
        raise HarnessError("freeze commit does not contain the exact freeze manifest bytes")
    return {
        "authority_file_count": len(authority_hashes),
        "authority_source_commit": authority_commit,
        "freeze_commit_verified": True,
        "freeze_manifest_sha256": sha256_bytes(manifest_bytes),
        "manifest": manifest,
        "runtime_package_identity_sha256": runtime["package_identity_sha256"],
        "runtime_package_manifest_sha256": sha256_bytes(runtime_bytes),
        "status": "verified",
    }


def mask_digest(seed_hex: str, domain: str, *parts: str) -> bytes:
    key = bytes.fromhex(seed_hex)
    message = domain.encode("utf-8") + b"\x00" + b"\x00".join(
        part.encode("utf-8") for part in parts
    )
    return hmac.new(key, message, hashlib.sha256).digest()


def pair_base_mapping(seed_hex: str, case_id: str, draw_id: str) -> dict[str, str]:
    digest = mask_digest(seed_hex, "strategic-advisor-mask-v1", case_id, draw_id)
    if digest[0] & 1 == 0:
        return {"A": "skilled", "B": "control"}
    return {"A": "control", "B": "skilled"}


def audit_presentation(seed_hex: str, mode: str, case_id: str, draw_id: str) -> dict[str, str]:
    digest = mask_digest(
        seed_hex,
        "strategic-advisor-condition-audit-map-v1",
        mode,
        case_id,
        draw_id,
    )
    if digest[0] & 1 == 0:
        return {"A": "base-A", "B": "base-B"}
    return {"A": "base-B", "B": "base-A"}


def load_frozen_cases(source_root: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    authority_paths = {record["path"] for record in manifest["authority_files"]}
    if DEFAULT_EVALS not in authority_paths:
        raise HarnessError(f"frozen authority does not contain {DEFAULT_EVALS}")
    path = regular_repo_file(source_root, DEFAULT_EVALS, "frozen eval inventory")
    parsed, _ = load_json_file(path, "frozen eval inventory")
    if not isinstance(parsed, dict) or parsed.get("schema_version") != 1:
        raise HarnessError("frozen eval inventory schema is invalid")
    cases = parsed.get("evals")
    if not isinstance(cases, list) or len(cases) < 16:
        raise HarnessError("frozen eval inventory must contain at least 16 cases")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise HarnessError(f"case[{index}] is not an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or RUN_ID.fullmatch(case_id.lower()) is None:
            raise HarnessError(f"case[{index}] has an invalid ID")
        if case_id in seen:
            raise HarnessError(f"duplicate case ID: {case_id}")
        seen.add(case_id)
        prompt = require_nonempty_string(case.get("prompt"), f"case {case_id} prompt")
        raw_na = case.get("not_applicable_dimensions", [])
        if raw_na is None:
            raw_na = []
        if (
            not isinstance(raw_na, list)
            or len(raw_na) != len(set(raw_na))
            or not all(item in DIMENSIONS for item in raw_na)
        ):
            raise HarnessError(f"case {case_id} not_applicable_dimensions is invalid")
        result.append(
            {
                "case_id": case_id,
                "prompt_sha256": sha256_bytes(prompt.encode("utf-8")),
                "not_applicable_dimensions": raw_na,
            }
        )
    return sorted(result, key=lambda item: item["case_id"])


def make_plan(args: argparse.Namespace) -> dict[str, Any]:
    source_root = args.source_root.absolute()
    verified = verify_freeze_manifest(source_root, args.freeze_manifest, args.freeze_commit)
    manifest = verified["manifest"]
    if not RUN_ID.fullmatch(args.run_id):
        raise HarnessError("run_id must be a normalized lowercase identifier")
    output_relative = repo_relative(source_root, args.output, "run plan output")
    expected_prefix = f"evidence/evaluations/{manifest['iteration']}/runs/{args.run_id}/"
    if output_relative.as_posix() != expected_prefix + "run-plan.json":
        raise HarnessError(f"run plan output must be {expected_prefix}run-plan.json")
    if args.output.parent.exists() and any(args.output.parent.iterdir()):
        raise HarnessError("run directory must be new or empty")
    cases = load_frozen_cases(source_root, manifest)
    draws = manifest["generation"]["draw_ids"]
    seed = manifest["masking"]["masking_seed_hex"]
    freeze_identity = {
        "authority_source_commit": manifest["freeze_envelope"]["authority_source_commit"],
        "freeze_commit_sha": args.freeze_commit,
        "freeze_manifest_sha256": verified["freeze_manifest_sha256"],
        "runtime_package_identity_sha256": verified["runtime_package_identity_sha256"],
        "runtime_package_manifest_sha256": verified[
            "runtime_package_manifest_sha256"
        ],
    }
    pairs: list[dict[str, Any]] = []
    generation_units: list[dict[str, Any]] = []
    quality_units: list[dict[str, Any]] = []
    audit_units: list[dict[str, Any]] = []
    expected_paths: set[str] = set()
    for case in cases:
        case_id = case["case_id"]
        for draw_id in draws:
            base_mapping = pair_base_mapping(seed, case_id, draw_id)
            generation_by_condition: dict[str, str] = {}
            for condition in CONDITIONS:
                stem = f"generations/{case_id}/{draw_id}/{condition}"
                unit_id = f"generation:{case_id}:{draw_id}:{condition}"
                generation_by_condition[condition] = unit_id
                unit = {
                    "artifact_path": stem + ".json",
                    "attempt_id": "initial",
                    "case_id": case_id,
                    "condition": condition,
                    "draw_id": draw_id,
                    "raw_response_path": stem + ".txt",
                    "unit_id": unit_id,
                }
                generation_units.append(unit)
                expected_paths.update((unit["artifact_path"], unit["raw_response_path"]))
            base_sources = {
                label: generation_by_condition[condition]
                for label, condition in base_mapping.items()
            }
            pair_quality: dict[str, dict[str, str]] = {}
            for pass_id in QUALITY_PASSES:
                presentation = (
                    {"A": "base-A", "B": "base-B"}
                    if pass_id == "score-1"
                    else {"A": "base-B", "B": "base-A"}
                )
                artifact_path = f"quality-scores/{case_id}/{draw_id}/{pass_id}.json"
                unit_id = f"quality:{case_id}:{draw_id}:{pass_id}"
                quality_units.append(
                    {
                        "artifact_path": artifact_path,
                        "attempt_id": "initial",
                        "case_id": case_id,
                        "draw_id": draw_id,
                        "pass_id": pass_id,
                        "presentation": presentation,
                        "unit_id": unit_id,
                    }
                )
                expected_paths.add(artifact_path)
                pair_quality[pass_id] = presentation
            pair_audits: dict[str, dict[str, str]] = {}
            for mode in AUDIT_MODES:
                presentation = audit_presentation(seed, mode, case_id, draw_id)
                artifact_path = f"condition-audits/{case_id}/{draw_id}/{mode}.json"
                unit_id = f"condition-audit:{case_id}:{draw_id}:{mode}"
                unit = {
                    "artifact_path": artifact_path,
                    "attempt_id": "initial",
                    "audit_mode": mode,
                    "case_id": case_id,
                    "draw_id": draw_id,
                    "presentation": presentation,
                    "unit_id": unit_id,
                }
                if mode == "structure-only":
                    unit["presented_A_path"] = (
                        f"condition-audits/{case_id}/{draw_id}/structure-A.jsonl"
                    )
                    unit["presented_B_path"] = (
                        f"condition-audits/{case_id}/{draw_id}/structure-B.jsonl"
                    )
                    expected_paths.update(
                        (unit["presented_A_path"], unit["presented_B_path"])
                    )
                audit_units.append(unit)
                expected_paths.add(artifact_path)
                pair_audits[mode] = presentation
            pairs.append(
                {
                    "base_mapping": base_mapping,
                    "base_sources": base_sources,
                    "case_id": case_id,
                    "condition_audit_presentations": pair_audits,
                    "draw_id": draw_id,
                    "quality_presentations": pair_quality,
                }
            )
    quality_units.sort(
        key=lambda unit: (
            QUALITY_PASSES.index(unit["pass_id"]),
            mask_digest(
                seed,
                "strategic-advisor-score-order-v1",
                unit["pass_id"],
                unit["case_id"],
                unit["draw_id"],
            ),
            unit["case_id"],
            unit["draw_id"],
        )
    )
    plan = {
        "adjudication_supported": False,
        "audit_modes": list(AUDIT_MODES),
        "case_count": len(cases),
        "cases": cases,
        "condition_audit_units": audit_units,
        "conditions": list(CONDITIONS),
        "draw_ids": draws,
        "expected_artifact_paths": sorted(expected_paths),
        "freeze_identity": freeze_identity,
        "final_score_resolution_supported": False,
        "generation_units": generation_units,
        "pairs": pairs,
        "quality_pass_algorithm": "inverse-ab-quality-pass-v1",
        "quality_pass_ids": list(QUALITY_PASSES),
        "quality_units": quality_units,
        "release_claim_supported_by_this_harness": False,
        "run_id": args.run_id,
        "schema_version": 1,
        "status": "planned",
        "unsupported_release_components": UNSUPPORTED_RELEASE_COMPONENTS,
    }
    write_new_file(args.output, rendered_json_bytes(plan), "run plan")
    return {
        "audit_unit_count": len(audit_units),
        "case_count": len(cases),
        "draw_count": len(draws),
        "expected_artifact_count": len(expected_paths),
        "generation_unit_count": len(generation_units),
        "plan_sha256": sha256_bytes(args.output.read_bytes()),
        "quality_unit_count": len(quality_units),
        "run_id": args.run_id,
        "status": "planned",
    }


def exact_keys(value: Any, expected: Iterable[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise HarnessError(f"{label} must be an object")
    expected_set = set(expected)
    if set(value) != expected_set:
        missing = sorted(expected_set - set(value))
        extra = sorted(set(value) - expected_set)
        raise HarnessError(f"{label} keys are invalid; missing={missing}, extra={extra}")
    return value


def validate_freeze_identity(actual: Any, expected: dict[str, str], label: str) -> None:
    record = exact_keys(actual, REQUIRED_FREEZE_IDENTITY_KEYS, label)
    if record != expected:
        raise HarnessError(f"{label} does not match the run plan")


def nested_key_exists(value: Any, forbidden: str) -> bool:
    if isinstance(value, dict):
        return any(key.lower() == forbidden or nested_key_exists(child, forbidden) for key, child in value.items())
    if isinstance(value, list):
        return any(nested_key_exists(item, forbidden) for item in value)
    return False


def reject_apparent_identity_reasoning(value: Any) -> None:
    for candidate in nested_strings(value):
        if any(pattern.search(candidate) for pattern in APPARENT_IDENTITY_PATTERNS) or any(
            pattern.search(candidate) for pattern in DIRECT_IDENTITY_RATING_PATTERNS
        ):
            raise HarnessError(
                "quality score contains explicit apparent-condition or skill-identity reasoning"
            )


def validate_nonempty_evidence(record: Any, label: str) -> None:
    require_nonempty_string(record, label)


def validate_score_result(
    result: Any,
    case_id: str,
    draw_id: str,
    scoring_pass_id: str,
    not_applicable: list[str],
) -> None:
    if nested_key_exists(result, "condition_guess"):
        raise HarnessError("quality score contains forbidden condition_guess")
    reject_apparent_identity_reasoning(result)
    score = exact_keys(
        result,
        (
            "schema_version",
            "case_id",
            "draw_id",
            "scoring_pass_id",
            "not_applicable_dimensions",
            "dimension_applicability",
            "responses",
            "comparison",
        ),
        "quality score result",
    )
    if score["schema_version"] != "strategic-advisor-scorer-v2":
        raise HarnessError("quality score schema_version is invalid")
    if (score["case_id"], score["draw_id"], score["scoring_pass_id"]) != (
        case_id,
        draw_id,
        scoring_pass_id,
    ):
        raise HarnessError("quality score IDs do not match its work unit")
    if score["not_applicable_dimensions"] != not_applicable:
        raise HarnessError("quality score N/A list does not match frozen case metadata")
    applicability = exact_keys(score["dimension_applicability"], DIMENSIONS, "dimension applicability")
    for dimension in DIMENSIONS:
        item = exact_keys(applicability[dimension], ("applicable", "basis"), f"applicability {dimension}")
        expected = dimension not in not_applicable
        if item["applicable"] is not expected:
            raise HarnessError(f"quality score applicability is invalid: {dimension}")
        validate_nonempty_evidence(item["basis"], f"applicability basis {dimension}")
    responses = exact_keys(score["responses"], ("A", "B"), "quality score responses")
    for label in ("A", "B"):
        response = exact_keys(responses[label], ("dimensions", "hard_gates"), f"response {label}")
        dimensions = exact_keys(response["dimensions"], DIMENSIONS, f"response {label} dimensions")
        for dimension in DIMENSIONS:
            item = exact_keys(dimensions[dimension], ("score", "evidence"), f"{label}.{dimension}")
            value = item["score"]
            if dimension in not_applicable:
                if value is not None:
                    raise HarnessError(f"quality score must be null for frozen N/A: {label}.{dimension}")
            elif not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
                raise HarnessError(f"quality score is out of range: {label}.{dimension}")
            validate_nonempty_evidence(item["evidence"], f"score evidence {label}.{dimension}")
        gates = exact_keys(response["hard_gates"], HARD_GATES, f"response {label} hard gates")
        for gate in HARD_GATES:
            item = exact_keys(gates[gate], ("failed", "evidence"), f"{label}.{gate}")
            if not isinstance(item["failed"], bool):
                raise HarnessError(f"hard gate verdict must be boolean: {label}.{gate}")
            validate_nonempty_evidence(item["evidence"], f"hard gate evidence {label}.{gate}")
    comparison = exact_keys(
        score["comparison"],
        ("better_response", "most_decision_relevant_difference", "rubric_ambiguity_or_missing_evidence"),
        "quality comparison",
    )
    if comparison["better_response"] not in ("A", "B", "tie"):
        raise HarnessError("quality comparison better_response is invalid")
    validate_nonempty_evidence(
        comparison["most_decision_relevant_difference"], "quality comparison evidence"
    )
    if not isinstance(comparison["rubric_ambiguity_or_missing_evidence"], str):
        raise HarnessError("quality comparison ambiguity field must be a string")


def validate_audit_result(
    result: Any, case_id: str, draw_id: str, unit_id: str, mode: str
) -> None:
    audit = exact_keys(
        result,
        (
            "schema_version",
            "case_id",
            "draw_id",
            "audit_id",
            "audit_mode",
            "likely_skilled",
            "confidence_1_to_5",
            "evidence",
        ),
        "condition audit result",
    )
    if audit["schema_version"] != "strategic-advisor-condition-auditor-v1":
        raise HarnessError("condition audit schema_version is invalid")
    if (audit["case_id"], audit["draw_id"], audit["audit_id"], audit["audit_mode"]) != (
        case_id,
        draw_id,
        unit_id,
        mode,
    ):
        raise HarnessError("condition audit IDs do not match its work unit")
    if audit["likely_skilled"] not in ("A", "B", "unclear"):
        raise HarnessError("condition audit likely_skilled is invalid")
    confidence = audit["confidence_1_to_5"]
    if not isinstance(confidence, int) or isinstance(confidence, bool) or not 1 <= confidence <= 5:
        raise HarnessError("condition audit confidence is invalid")
    if audit["likely_skilled"] == "unclear" and confidence != 1:
        raise HarnessError("unclear condition audit must use confidence 1")
    validate_nonempty_evidence(audit["evidence"], "condition audit evidence")


def frozen_authority_sha256(manifest: dict[str, Any], relative: str) -> str:
    matches = [
        record["sha256"]
        for record in manifest["authority_files"]
        if record["path"] == relative
    ]
    if len(matches) != 1 or HEX_64.fullmatch(matches[0]) is None:
        raise HarnessError(f"frozen authority identity is missing: {relative}")
    return matches[0]


def expected_quality_input_envelope(
    manifest: dict[str, Any],
    case: dict[str, Any],
    draw_id: str,
    scoring_pass_id: str,
    candidate_hashes: dict[str, str],
) -> dict[str, Any]:
    return {
        "authority": {
            "prompt_sha256": manifest["scoring"]["scorer_prompt_sha256"],
            "rubric_sha256": frozen_authority_sha256(
                manifest, "skills/strategic-advisor/evals/RUBRIC.md"
            ),
        },
        "candidates": {
            "content_kind": "full-response",
            "labels": ["A", "B"],
            "sha256": candidate_hashes,
        },
        "case": {
            "case_prompt_absent": False,
            "case_prompt_sha256": case["prompt_sha256"],
            "declared_inputs_absent": False,
            "declared_input_manifest_sha256": manifest["generation"][
                "declared_input_manifest_sha256"
            ],
            "not_applicable_dimensions": case["not_applicable_dimensions"],
        },
        "component": "quality-scorer",
        "input_ids": {
            "case_id": case["case_id"],
            "draw_id": draw_id,
            "scoring_pass_id": scoring_pass_id,
        },
        "model_visible_absence": {
            "base_mapping_fields_absent": True,
            "condition_audit_outputs_absent": True,
            "condition_labels_absent": True,
            "expected_properties_absent": True,
            "skill_identity_fields_absent": True,
        },
        "schema_version": 1,
    }


def expected_audit_input_envelope(
    manifest: dict[str, Any],
    case: dict[str, Any],
    draw_id: str,
    audit_id: str,
    mode: str,
    candidate_hashes: dict[str, str],
) -> dict[str, Any]:
    structure_only = mode == "structure-only"
    return {
        "authority": {
            "prompt_sha256": manifest["condition_audit"]["prompt_sha256"],
            "rubric_absent": True,
            "rubric_sha256": None,
        },
        "candidates": {
            "content_kind": "structure-view" if structure_only else "full-response",
            "labels": ["A", "B"],
            "sha256": candidate_hashes,
        },
        "case": {
            "case_prompt_absent": structure_only,
            "case_prompt_sha256": None if structure_only else case["prompt_sha256"],
            "declared_inputs_absent": structure_only,
            "declared_input_manifest_sha256": (
                None
                if structure_only
                else manifest["generation"]["declared_input_manifest_sha256"]
            ),
        },
        "component": "condition-auditor",
        "input_ids": {
            "audit_id": audit_id,
            "case_id": case["case_id"],
            "draw_id": draw_id,
        },
        "mode": mode,
        "model_visible_absence": {
            "base_mapping_fields_absent": True,
            "condition_labels_absent": True,
            "expected_properties_absent": True,
            "quality_scores_absent": True,
            "skill_identity_fields_absent": True,
        },
        "schema_version": 1,
    }


def structure_view(raw: bytes) -> bytes:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise HarnessError(f"structure-view-v1 requires strict UTF-8: {error}") from error
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    records: list[dict[str, Any]] = []
    for line in lines:
        leading = len(line) - len(line.lstrip(" "))
        content = line[leading:]
        if not content.strip():
            records.append({"kind": "BLANK"})
            continue
        kind = "TEXT"
        marker = None
        prefix_length = 0
        heading_level = None
        match = re.match(r"^(#{1,6})(?:[ \t]+|$)", content)
        if match:
            kind = "ATX_HEADING"
            heading_level = len(match.group(1))
            marker = "hash"
            prefix_length = match.end()
        elif re.fullmatch(r"(?:=+|-+)\s*", content):
            kind = "SETEXT_MARKER"
            marker = "equals" if content.startswith("=") else "hyphen"
            prefix_length = len(content.rstrip())
        else:
            match = re.match(r"^([-+*])[ \t]+", content)
            if match:
                kind = "UNORDERED_ITEM"
                marker = {"-": "hyphen", "+": "plus", "*": "asterisk"}[match.group(1)]
                prefix_length = match.end()
            else:
                match = re.match(r"^(\d+)([.)])[ \t]+", content)
                if match:
                    kind = "ORDERED_ITEM"
                    marker = "decimal-dot" if match.group(2) == "." else "decimal-paren"
                    prefix_length = match.end()
                else:
                    match = re.match(r"^>[ \t]?", content)
                    if match:
                        kind = "BLOCKQUOTE"
                        marker = "greater-than"
                        prefix_length = match.end()
                    else:
                        match = re.match(r"^(`{3,}|~{3,})", content)
                        if match:
                            kind = "FENCE"
                            marker = "backtick" if match.group(1).startswith("`") else "tilde"
                            prefix_length = len(match.group(1))
                        elif "|" in content:
                            kind = "TABLE_ROW"
                            marker = "pipe"
        remainder = content[prefix_length:]
        record: dict[str, Any] = {
            "codepoint_count": len(remainder),
            "emphasis_marker_count": remainder.count("*") + remainder.count("_"),
            "inline_code_span_count": len(re.findall(r"`[^`]+`", remainder)),
            "kind": kind,
            "leading_space_count": leading,
            "link_span_count": len(re.findall(r"!?\[[^\]]*\]\([^)]*\)", remainder)),
            "marker_class": marker,
            "word_count": len(remainder.split()),
        }
        if heading_level is not None:
            record["heading_level"] = heading_level
        records.append(record)
    return b"".join(canonical_json_bytes(record) + b"\n" for record in records)


def unit_by_id(units: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for unit in units:
        unit_id = unit["unit_id"]
        if unit_id in result:
            raise HarnessError(f"duplicate plan unit ID: {unit_id}")
        result[unit_id] = unit
    return result


def validate_plan_matrix(
    source_root: Path, manifest: dict[str, Any], plan: dict[str, Any]
) -> None:
    exact_keys(
        plan,
        (
            "adjudication_supported",
            "audit_modes",
            "case_count",
            "cases",
            "condition_audit_units",
            "conditions",
            "draw_ids",
            "expected_artifact_paths",
            "freeze_identity",
            "final_score_resolution_supported",
            "generation_units",
            "pairs",
            "quality_pass_algorithm",
            "quality_pass_ids",
            "quality_units",
            "release_claim_supported_by_this_harness",
            "run_id",
            "schema_version",
            "status",
            "unsupported_release_components",
        ),
        "run plan",
    )
    cases = load_frozen_cases(source_root, manifest)
    draws = manifest["generation"]["draw_ids"]
    seed = manifest["masking"]["masking_seed_hex"]
    if (
        plan["cases"] != cases
        or plan["adjudication_supported"] is not False
        or plan["final_score_resolution_supported"] is not False
        or plan["case_count"] != len(cases)
        or plan["draw_ids"] != draws
        or plan["conditions"] != list(CONDITIONS)
        or plan["quality_pass_algorithm"] != "inverse-ab-quality-pass-v1"
        or plan["quality_pass_ids"] != list(QUALITY_PASSES)
        or plan["audit_modes"] != list(AUDIT_MODES)
        or plan["release_claim_supported_by_this_harness"] is not False
        or plan["unsupported_release_components"] != UNSUPPORTED_RELEASE_COMPONENTS
    ):
        raise HarnessError("run plan does not match the frozen evaluation matrix")
    expected_generations: list[dict[str, Any]] = []
    expected_quality: list[dict[str, Any]] = []
    expected_audits: list[dict[str, Any]] = []
    expected_pairs: list[dict[str, Any]] = []
    expected_paths: set[str] = set()
    for case in cases:
        case_id = case["case_id"]
        for draw_id in draws:
            base_mapping = pair_base_mapping(seed, case_id, draw_id)
            generation_by_condition: dict[str, str] = {}
            for condition in CONDITIONS:
                stem = f"generations/{case_id}/{draw_id}/{condition}"
                unit_id = f"generation:{case_id}:{draw_id}:{condition}"
                generation_by_condition[condition] = unit_id
                unit = {
                    "artifact_path": stem + ".json",
                    "attempt_id": "initial",
                    "case_id": case_id,
                    "condition": condition,
                    "draw_id": draw_id,
                    "raw_response_path": stem + ".txt",
                    "unit_id": unit_id,
                }
                expected_generations.append(unit)
                expected_paths.update((unit["artifact_path"], unit["raw_response_path"]))
            base_sources = {
                label: generation_by_condition[condition]
                for label, condition in base_mapping.items()
            }
            pair_quality: dict[str, dict[str, str]] = {}
            for pass_id in QUALITY_PASSES:
                presentation = (
                    {"A": "base-A", "B": "base-B"}
                    if pass_id == "score-1"
                    else {"A": "base-B", "B": "base-A"}
                )
                artifact_path = f"quality-scores/{case_id}/{draw_id}/{pass_id}.json"
                unit_id = f"quality:{case_id}:{draw_id}:{pass_id}"
                expected_quality.append(
                    {
                        "artifact_path": artifact_path,
                        "attempt_id": "initial",
                        "case_id": case_id,
                        "draw_id": draw_id,
                        "pass_id": pass_id,
                        "presentation": presentation,
                        "unit_id": unit_id,
                    }
                )
                expected_paths.add(artifact_path)
                pair_quality[pass_id] = presentation
            pair_audits: dict[str, dict[str, str]] = {}
            for mode in AUDIT_MODES:
                presentation = audit_presentation(seed, mode, case_id, draw_id)
                artifact_path = f"condition-audits/{case_id}/{draw_id}/{mode}.json"
                unit_id = f"condition-audit:{case_id}:{draw_id}:{mode}"
                audit_unit = {
                    "artifact_path": artifact_path,
                    "attempt_id": "initial",
                    "audit_mode": mode,
                    "case_id": case_id,
                    "draw_id": draw_id,
                    "presentation": presentation,
                    "unit_id": unit_id,
                }
                if mode == "structure-only":
                    audit_unit["presented_A_path"] = (
                        f"condition-audits/{case_id}/{draw_id}/structure-A.jsonl"
                    )
                    audit_unit["presented_B_path"] = (
                        f"condition-audits/{case_id}/{draw_id}/structure-B.jsonl"
                    )
                    expected_paths.update(
                        (
                            audit_unit["presented_A_path"],
                            audit_unit["presented_B_path"],
                        )
                    )
                expected_audits.append(audit_unit)
                expected_paths.add(artifact_path)
                pair_audits[mode] = presentation
            expected_pairs.append(
                {
                    "base_mapping": base_mapping,
                    "base_sources": base_sources,
                    "case_id": case_id,
                    "condition_audit_presentations": pair_audits,
                    "draw_id": draw_id,
                    "quality_presentations": pair_quality,
                }
            )
    expected_quality.sort(
        key=lambda unit: (
            QUALITY_PASSES.index(unit["pass_id"]),
            mask_digest(
                seed,
                "strategic-advisor-score-order-v1",
                unit["pass_id"],
                unit["case_id"],
                unit["draw_id"],
            ),
            unit["case_id"],
            unit["draw_id"],
        )
    )
    if (
        plan["generation_units"] != expected_generations
        or plan["quality_units"] != expected_quality
        or plan["condition_audit_units"] != expected_audits
        or plan["pairs"] != expected_pairs
        or plan["expected_artifact_paths"] != sorted(expected_paths)
    ):
        raise HarnessError("run plan work units or mappings differ from frozen algorithms")


def load_artifact(run_root: Path, relative: str, label: str) -> dict[str, Any]:
    path = run_root / Path(*normalized_relative_path(relative, label).parts)
    parsed, _ = load_json_file(path, label)
    if not isinstance(parsed, dict):
        raise HarnessError(f"{label} must be a JSON object")
    return parsed


def verify_artifacts(args: argparse.Namespace) -> dict[str, Any]:
    source_root = args.source_root.absolute()
    verified = verify_freeze_manifest(source_root, args.freeze_manifest, args.freeze_commit)
    frozen_at = parse_utc_timestamp(
        verified["manifest"]["frozen_at"], "freeze manifest frozen_at"
    )
    plan, plan_bytes = load_json_file(args.plan, "run plan")
    if not isinstance(plan, dict) or plan.get("schema_version") != 1 or plan.get("status") != "planned":
        raise HarnessError("run plan schema or status is invalid")
    if not isinstance(plan.get("run_id"), str) or RUN_ID.fullmatch(plan["run_id"]) is None:
        raise HarnessError("run plan run_id is invalid")
    if plan.get("freeze_identity", {}).get("freeze_commit_sha") != args.freeze_commit:
        raise HarnessError("run plan freeze commit does not match command")
    expected_identity = {
        "authority_source_commit": verified["manifest"]["freeze_envelope"]["authority_source_commit"],
        "freeze_commit_sha": args.freeze_commit,
        "freeze_manifest_sha256": verified["freeze_manifest_sha256"],
        "runtime_package_identity_sha256": verified["runtime_package_identity_sha256"],
        "runtime_package_manifest_sha256": verified["runtime_package_manifest_sha256"],
    }
    if plan.get("freeze_identity") != expected_identity:
        raise HarnessError("run plan freeze identity is stale or mismatched")
    validate_plan_matrix(source_root, verified["manifest"], plan)
    plan_sha256 = sha256_bytes(plan_bytes)
    run_root = args.plan.parent
    expected_plan_path = (
        source_root
        / "evidence"
        / "evaluations"
        / verified["manifest"]["iteration"]
        / "runs"
        / plan.get("run_id", "")
        / "run-plan.json"
    )
    if args.plan.resolve() != expected_plan_path.resolve():
        raise HarnessError("run plan is not in its frozen iteration/run directory")
    expected_paths = plan.get("expected_artifact_paths")
    if not isinstance(expected_paths, list) or expected_paths != sorted(set(expected_paths)):
        raise HarnessError("run plan expected artifact paths are invalid")
    actual_paths: list[str] = []
    for path in sorted(run_root.rglob("*")):
        if path.is_symlink():
            raise HarnessError(f"run tree contains a symlink: {path}")
        if path.is_file() and path != args.plan:
            actual_paths.append(path.relative_to(run_root).as_posix())
    if actual_paths != expected_paths:
        missing = sorted(set(expected_paths) - set(actual_paths))
        extra = sorted(set(actual_paths) - set(expected_paths))
        raise HarnessError(f"run artifact matrix is incomplete or contaminated; missing={missing}, extra={extra}")

    cases = {case["case_id"]: case for case in plan.get("cases", [])}
    pairs = {
        (pair["case_id"], pair["draw_id"]): pair for pair in plan.get("pairs", [])
    }
    generations = unit_by_id(plan.get("generation_units", []))
    qualities = unit_by_id(plan.get("quality_units", []))
    audits = unit_by_id(plan.get("condition_audit_units", []))
    contexts: set[str] = set()
    raw_by_unit: dict[str, bytes] = {}
    raw_hash_by_unit: dict[str, str] = {}
    finished_by_generation_unit: dict[str, datetime] = {}

    generation_top_keys = (
        "schema_version",
        "artifact_type",
        "unit_id",
        "attempt_id",
        "run_id",
        "plan_sha256",
        "freeze_identity",
        "case_id",
        "draw_id",
        "condition",
        "case_prompt_sha256",
        "status",
        "host_context_id",
        "model",
        "model_version",
        "host",
        "configuration",
        "matched_context",
        "treatment",
        "raw_response_path",
        "raw_response_sha256",
        "started_at",
        "finished_at",
        "error",
    )
    generation_config = verified["manifest"]["generation"]
    expected_matched_context = {
        "declared_input_manifest_sha256": generation_config["declared_input_manifest_sha256"],
        "non_treatment_context_sha256": generation_config["non_treatment_context_sha256"],
        "system_and_developer_context_sha256": generation_config[
            "system_and_developer_context_sha256"
        ],
        "tool_policy_sha256": generation_config["tool_policy_sha256"],
    }
    for unit_id, unit in generations.items():
        artifact = exact_keys(
            load_artifact(run_root, unit["artifact_path"], f"generation {unit_id}"),
            generation_top_keys,
            f"generation {unit_id}",
        )
        if artifact["schema_version"] != 1 or artifact["artifact_type"] != "generation":
            raise HarnessError(f"generation schema is invalid: {unit_id}")
        if (
            artifact["unit_id"],
            artifact["case_id"],
            artifact["draw_id"],
            artifact["condition"],
        ) != (unit_id, unit["case_id"], unit["draw_id"], unit["condition"]):
            raise HarnessError(f"generation IDs do not match plan: {unit_id}")
        if artifact["attempt_id"] != unit["attempt_id"]:
            raise HarnessError(f"generation attempt identity mismatch: {unit_id}")
        if artifact["run_id"] != plan["run_id"] or artifact["plan_sha256"] != plan_sha256:
            raise HarnessError(f"generation run/plan identity mismatch: {unit_id}")
        validate_freeze_identity(artifact["freeze_identity"], expected_identity, f"generation {unit_id} identity")
        if artifact["status"] != "complete" or artifact["error"] is not None:
            raise HarnessError(f"generation is not complete: {unit_id}")
        context_id = require_nonempty_string(artifact["host_context_id"], f"generation {unit_id} context")
        if context_id in contexts:
            raise HarnessError(f"host context ID is reused: {context_id}")
        contexts.add(context_id)
        if (
            artifact["model"] != generation_config["model"]
            or artifact["model_version"] != generation_config["model_version"]
            or artifact["host"] != generation_config["host"]
            or artifact["configuration"] != generation_config["configuration"]
            or artifact["matched_context"] != expected_matched_context
        ):
            raise HarnessError(f"generation configuration/context mismatch: {unit_id}")
        if artifact["case_prompt_sha256"] != cases[unit["case_id"]]["prompt_sha256"]:
            raise HarnessError(f"generation case prompt identity mismatch: {unit_id}")
        treatment = exact_keys(
            artifact["treatment"],
            (
                "runtime_package_identity_sha256",
                "package_discovered",
                "skill_selected",
                "loaded_reference_paths",
            ),
            f"generation {unit_id} treatment",
        )
        if unit["condition"] == "skilled":
            if (
                treatment["runtime_package_identity_sha256"]
                != expected_identity["runtime_package_identity_sha256"]
                or treatment["package_discovered"] is not True
                or not isinstance(treatment["skill_selected"], bool)
                or not isinstance(treatment["loaded_reference_paths"], list)
                or not all(isinstance(item, str) for item in treatment["loaded_reference_paths"])
            ):
                raise HarnessError(f"skilled package activation proof is invalid: {unit_id}")
        elif treatment != {
            "runtime_package_identity_sha256": None,
            "package_discovered": False,
            "skill_selected": False,
            "loaded_reference_paths": [],
        }:
            raise HarnessError(f"control generation received treatment metadata: {unit_id}")
        if artifact["raw_response_path"] != unit["raw_response_path"]:
            raise HarnessError(f"generation raw response path mismatch: {unit_id}")
        raw_path = run_root / Path(*PurePosixPath(unit["raw_response_path"]).parts)
        raw = raw_path.read_bytes()
        if not raw:
            raise HarnessError(f"generation raw response is empty: {unit_id}")
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError as error:
            raise HarnessError(f"generation raw response is not UTF-8: {unit_id}") from error
        digest = sha256_bytes(raw)
        if artifact["raw_response_sha256"] != digest:
            raise HarnessError(f"generation raw response hash mismatch: {unit_id}")
        started_at = parse_utc_timestamp(
            artifact["started_at"], f"generation {unit_id} started_at"
        )
        finished_at = parse_utc_timestamp(
            artifact["finished_at"], f"generation {unit_id} finished_at"
        )
        if started_at <= frozen_at or finished_at < started_at:
            raise HarnessError(
                f"generation ordering does not prove post-freeze execution: {unit_id}"
            )
        raw_by_unit[unit_id] = raw
        raw_hash_by_unit[unit_id] = digest
        finished_by_generation_unit[unit_id] = finished_at

    quality_results: dict[tuple[str, str, str], dict[str, Any]] = {}
    previous_quality_finished_at: datetime | None = None
    quality_top_keys = (
        "schema_version",
        "artifact_type",
        "unit_id",
        "attempt_id",
        "run_id",
        "plan_sha256",
        "freeze_identity",
        "case_id",
        "draw_id",
        "pass_id",
        "status",
        "host_context_id",
        "model",
        "model_version",
        "host",
        "configuration",
        "scorer_prompt_sha256",
        "presentation",
        "presented_response_sha256",
        "input_envelope",
        "started_at",
        "finished_at",
        "result",
        "error",
    )
    for unit_id, unit in qualities.items():
        artifact = exact_keys(
            load_artifact(run_root, unit["artifact_path"], f"quality {unit_id}"),
            quality_top_keys,
            f"quality {unit_id}",
        )
        if artifact["schema_version"] != 1 or artifact["artifact_type"] != "quality-score":
            raise HarnessError(f"quality artifact schema is invalid: {unit_id}")
        if (artifact["unit_id"], artifact["case_id"], artifact["draw_id"], artifact["pass_id"]) != (
            unit_id,
            unit["case_id"],
            unit["draw_id"],
            unit["pass_id"],
        ):
            raise HarnessError(f"quality artifact IDs do not match plan: {unit_id}")
        if artifact["attempt_id"] != unit["attempt_id"]:
            raise HarnessError(f"quality attempt identity mismatch: {unit_id}")
        if artifact["run_id"] != plan["run_id"] or artifact["plan_sha256"] != plan_sha256:
            raise HarnessError(f"quality run/plan identity mismatch: {unit_id}")
        validate_freeze_identity(artifact["freeze_identity"], expected_identity, f"quality {unit_id} identity")
        if artifact["status"] != "complete" or artifact["error"] is not None:
            raise HarnessError(f"quality score is not complete: {unit_id}")
        context_id = require_nonempty_string(artifact["host_context_id"], f"quality {unit_id} context")
        if context_id in contexts:
            raise HarnessError(f"host context ID is reused: {context_id}")
        contexts.add(context_id)
        scoring_config = verified["manifest"]["scoring"]
        if (
            artifact["model"] != scoring_config["model"]
            or artifact["model_version"] != scoring_config["model_version"]
            or artifact["host"] != scoring_config["host"]
            or artifact["configuration"] != scoring_config["configuration"]
            or artifact["scorer_prompt_sha256"] != scoring_config["scorer_prompt_sha256"]
        ):
            raise HarnessError(f"quality scorer provenance mismatch: {unit_id}")
        if artifact["presentation"] != unit["presentation"]:
            raise HarnessError(f"quality presentation does not match plan: {unit_id}")
        pair = pairs[(unit["case_id"], unit["draw_id"])]
        expected_hashes = {
            label: raw_hash_by_unit[
                pair["base_sources"][base_label.removeprefix("base-")]
            ]
            for label, base_label in unit["presentation"].items()
        }
        if artifact["presented_response_sha256"] != expected_hashes:
            raise HarnessError(f"quality candidate hashes do not match presentation: {unit_id}")
        expected_envelope = expected_quality_input_envelope(
            verified["manifest"],
            cases[unit["case_id"]],
            unit["draw_id"],
            unit_id,
            expected_hashes,
        )
        if artifact["input_envelope"] != expected_envelope:
            raise HarnessError(
                f"quality retained input envelope is incomplete or mismatched: {unit_id}"
            )
        started_at = parse_utc_timestamp(
            artifact["started_at"], f"quality {unit_id} started_at"
        )
        finished_at = parse_utc_timestamp(
            artifact["finished_at"], f"quality {unit_id} finished_at"
        )
        latest_generation = max(
            finished_by_generation_unit[source_unit]
            for source_unit in pair["base_sources"].values()
        )
        if started_at <= frozen_at or started_at <= latest_generation or finished_at <= started_at:
            raise HarnessError(
                f"quality ordering does not prove post-generation execution: {unit_id}"
            )
        if (
            previous_quality_finished_at is not None
            and started_at <= previous_quality_finished_at
        ):
            raise HarnessError(
                f"quality timestamps do not prove exact frozen plan order: {unit_id}"
            )
        previous_quality_finished_at = finished_at
        validate_score_result(
            artifact["result"],
            unit["case_id"],
            unit["draw_id"],
            unit_id,
            cases[unit["case_id"]]["not_applicable_dimensions"],
        )
        quality_results[(unit["case_id"], unit["draw_id"], unit["pass_id"])] = artifact["result"]

    for pair_key, pair in pairs.items():
        first = pair["quality_presentations"].get("score-1")
        second = pair["quality_presentations"].get("score-2")
        if first != {"A": "base-A", "B": "base-B"} or second != {
            "A": "base-B",
            "B": "base-A",
        }:
            raise HarnessError(f"quality pass inversion is invalid: {pair_key}")

    structure_audit_results: list[tuple[dict[str, Any], dict[str, str], dict[str, str]]] = []
    audit_top_keys = (
        "schema_version",
        "artifact_type",
        "unit_id",
        "attempt_id",
        "run_id",
        "plan_sha256",
        "freeze_identity",
        "case_id",
        "draw_id",
        "audit_mode",
        "status",
        "host_context_id",
        "model",
        "model_version",
        "host",
        "configuration",
        "auditor_prompt_sha256",
        "presentation",
        "presented_input_sha256",
        "input_envelope",
        "started_at",
        "finished_at",
        "result",
        "error",
    )
    for unit_id, unit in audits.items():
        artifact = exact_keys(
            load_artifact(run_root, unit["artifact_path"], f"audit {unit_id}"),
            audit_top_keys,
            f"audit {unit_id}",
        )
        if artifact["schema_version"] != 1 or artifact["artifact_type"] != "condition-audit":
            raise HarnessError(f"audit artifact schema is invalid: {unit_id}")
        if (
            artifact["unit_id"],
            artifact["case_id"],
            artifact["draw_id"],
            artifact["audit_mode"],
        ) != (unit_id, unit["case_id"], unit["draw_id"], unit["audit_mode"]):
            raise HarnessError(f"audit IDs do not match plan: {unit_id}")
        if artifact["attempt_id"] != unit["attempt_id"]:
            raise HarnessError(f"audit attempt identity mismatch: {unit_id}")
        if artifact["run_id"] != plan["run_id"] or artifact["plan_sha256"] != plan_sha256:
            raise HarnessError(f"audit run/plan identity mismatch: {unit_id}")
        validate_freeze_identity(artifact["freeze_identity"], expected_identity, f"audit {unit_id} identity")
        if artifact["status"] != "complete" or artifact["error"] is not None:
            raise HarnessError(f"condition audit is not complete: {unit_id}")
        context_id = require_nonempty_string(artifact["host_context_id"], f"audit {unit_id} context")
        if context_id in contexts:
            raise HarnessError(f"host context ID is reused: {context_id}")
        contexts.add(context_id)
        audit_config = verified["manifest"].get("condition_audit")
        if not isinstance(audit_config, dict):
            raise HarnessError("freeze manifest lacks condition_audit configuration")
        if (
            artifact["model"] != audit_config["model"]
            or artifact["model_version"] != audit_config["model_version"]
            or artifact["host"] != audit_config["host"]
            or artifact["configuration"] != audit_config["configuration"]
            or artifact["auditor_prompt_sha256"] != audit_config["prompt_sha256"]
        ):
            raise HarnessError(f"condition auditor provenance mismatch: {unit_id}")
        if artifact["presentation"] != unit["presentation"]:
            raise HarnessError(f"audit presentation does not match plan: {unit_id}")
        pair = pairs[(unit["case_id"], unit["draw_id"])]
        if unit["audit_mode"] == "structure-only":
            expected_input_hashes: dict[str, str] = {}
            for label in ("A", "B"):
                base_label = unit["presentation"][label]
                source_unit = pair["base_sources"][base_label.removeprefix("base-")]
                expected_view = structure_view(raw_by_unit[source_unit])
                view_path = run_root / Path(*PurePosixPath(unit[f"presented_{label}_path"]).parts)
                actual_view = view_path.read_bytes()
                if actual_view != expected_view:
                    raise HarnessError(f"structure-only audit view is invalid: {unit_id}:{label}")
                expected_input_hashes[label] = sha256_bytes(actual_view)
        else:
            expected_input_hashes = {
                label: raw_hash_by_unit[
                    pair["base_sources"][base_label.removeprefix("base-")]
                ]
                for label, base_label in unit["presentation"].items()
            }
        if artifact["presented_input_sha256"] != expected_input_hashes:
            raise HarnessError(f"audit input hashes do not match presentation: {unit_id}")
        expected_envelope = expected_audit_input_envelope(
            verified["manifest"],
            cases[unit["case_id"]],
            unit["draw_id"],
            unit_id,
            unit["audit_mode"],
            expected_input_hashes,
        )
        if artifact["input_envelope"] != expected_envelope:
            raise HarnessError(
                f"audit retained input envelope is incomplete or mismatched: {unit_id}"
            )
        started_at = parse_utc_timestamp(
            artifact["started_at"], f"audit {unit_id} started_at"
        )
        finished_at = parse_utc_timestamp(
            artifact["finished_at"], f"audit {unit_id} finished_at"
        )
        latest_generation = max(
            finished_by_generation_unit[source_unit]
            for source_unit in pair["base_sources"].values()
        )
        if started_at <= frozen_at or started_at <= latest_generation or finished_at < started_at:
            raise HarnessError(
                f"audit ordering does not prove post-generation execution: {unit_id}"
            )
        validate_audit_result(
            artifact["result"], unit["case_id"], unit["draw_id"], unit_id, unit["audit_mode"]
        )
        if unit["audit_mode"] == "structure-only":
            structure_audit_results.append(
                (artifact["result"], unit["presentation"], pair["base_mapping"])
            )

    confirmed_hard_gate_failures: list[dict[str, str]] = []
    unresolved_hard_gate_disagreements: list[dict[str, str]] = []
    required_dimension_adjudications: list[dict[str, str]] = []
    for (case_id, draw_id), pair in pairs.items():
        skilled_base = next(
            base_label for base_label, condition in pair["base_mapping"].items() if condition == "skilled"
        )
        verdicts: dict[str, list[bool]] = {gate: [] for gate in HARD_GATES}
        dimension_scores: dict[str, dict[str, list[int]]] = {
            dimension: {"A": [], "B": []} for dimension in DIMENSIONS
        }
        for pass_id in QUALITY_PASSES:
            result = quality_results[(case_id, draw_id, pass_id)]
            presentation = pair["quality_presentations"][pass_id]
            presentation_label = next(
                label for label, base_label in presentation.items() if base_label == f"base-{skilled_base}"
            )
            for gate in HARD_GATES:
                verdicts[gate].append(
                    result["responses"][presentation_label]["hard_gates"][gate]["failed"]
                )
            for presentation_label, base_label in presentation.items():
                normalized_base = base_label.removeprefix("base-")
                for dimension in DIMENSIONS:
                    score = result["responses"][presentation_label]["dimensions"][dimension][
                        "score"
                    ]
                    if score is not None:
                        dimension_scores[dimension][normalized_base].append(score)
        for dimension, base_scores in dimension_scores.items():
            if any(
                len(scores) == 2 and abs(scores[0] - scores[1]) >= 2
                for scores in base_scores.values()
            ):
                required_dimension_adjudications.append(
                    {
                        "case_id": case_id,
                        "draw_id": draw_id,
                        "dimension_id": dimension,
                    }
                )
        for gate, pass_verdicts in verdicts.items():
            record = {"case_id": case_id, "draw_id": draw_id, "hard_gate_id": gate}
            if pass_verdicts == [True, True]:
                confirmed_hard_gate_failures.append(record)
            elif pass_verdicts[0] != pass_verdicts[1]:
                unresolved_hard_gate_disagreements.append(record)

    determinate = 0
    correct = 0
    for result, presentation, base_mapping in structure_audit_results:
        guess = result["likely_skilled"]
        if guess == "unclear":
            continue
        determinate += 1
        guessed_base = presentation[guess].removeprefix("base-")
        if base_mapping[guessed_base] == "skilled":
            correct += 1
    systematic_structure_leakage = (
        determinate >= 20 and (correct * 100 >= 70 * determinate)
    )
    release_failures: list[str] = []
    if confirmed_hard_gate_failures:
        release_failures.append("confirmed_skilled_hard_gate_failure")
    if unresolved_hard_gate_disagreements:
        release_failures.append("required_hard_gate_adjudication_missing")
    if required_dimension_adjudications:
        release_failures.append("required_dimension_adjudication_missing")
    if systematic_structure_leakage:
        release_failures.append("systematic_structure_only_condition_leakage")
    release_gate = "failed" if release_failures else "not-evaluated"
    return {
        "adjudication_complete": False,
        "condition_audit_unit_count": len(audits),
        "condition_audits_complete": True,
        "condition_audit_input_envelopes_complete": True,
        "confirmed_skilled_hard_gate_failures": confirmed_hard_gate_failures,
        "evaluation_matrix_complete": False,
        "final_score_resolution_complete": False,
        "freeze_identity": expected_identity,
        "generation_matrix_complete": True,
        "generation_unit_count": len(generations),
        "ordering_proof": {
            "host_receipt_order_proven": False,
            "kind": "retained-artifact-timestamp-ordering",
            "limitation": "The verifier proves retained timestamps and dependency order only; it cannot independently prove when a host received each prompt.",
        },
        "input_envelope_proof": {
            "host_receipt_exactness_proven": False,
            "retained_envelopes_verified": True,
            "limitation": "The verifier proves retained envelope bytes and identities; independent host telemetry is still required to prove the host received no additional hidden fields.",
        },
        "plan_sha256": plan_sha256,
        "quality_passes_complete": True,
        "quality_input_envelopes_complete": True,
        "quality_unit_count": len(qualities),
        "release_claim_supported": False,
        "release_failures": release_failures,
        "release_gate": release_gate,
        "required_dimension_adjudications": required_dimension_adjudications,
        "semantic_identity_marker_scan_passed": True,
        "semantic_quality_review_required": True,
        "status": "supported-artifacts-verified",
        "structure_only_audit": {
            "correct": correct,
            "determinate": determinate,
            "systematic_leakage": systematic_structure_leakage,
            "unclear": len(structure_audit_results) - determinate,
        },
        "unresolved_hard_gate_disagreements": unresolved_hard_gate_disagreements,
        "supported_artifact_matrix_complete": True,
        "unsupported_release_components": plan["unsupported_release_components"],
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Freeze, plan, and verify Strategic Advisor evaluation artifacts without model calls."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    freeze_parser = subparsers.add_parser("freeze", help="Freeze pre-result authority.")
    freeze_parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1])
    freeze_parser.add_argument("--template", default=DEFAULT_TEMPLATE)
    freeze_parser.add_argument("--config", type=Path)
    freeze_parser.add_argument("--runtime-package-manifest", type=Path, required=True)
    freeze_parser.add_argument("--output", type=Path, required=True)
    freeze_parser.add_argument("--authority-source-commit", required=True)
    freeze_parser.add_argument("--authority-source-tree")
    freeze_parser.add_argument("--frozen-at", required=True)
    freeze_parser.add_argument("--masking-seed-hex", required=True)
    freeze_parser.add_argument("--bootstrap-seed-hex", required=True)

    verify_parser = subparsers.add_parser("verify-freeze", help="Recompute and verify a freeze.")
    verify_parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1])
    verify_parser.add_argument("--manifest", type=Path, required=True)
    verify_parser.add_argument("--freeze-commit", required=True)

    plan_parser = subparsers.add_parser("plan", aliases=["make-plan"], help="Create deterministic external-run work units.")
    plan_parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1])
    plan_parser.add_argument("--freeze-manifest", type=Path, required=True)
    plan_parser.add_argument("--freeze-commit", required=True)
    plan_parser.add_argument("--run-id", required=True)
    plan_parser.add_argument("--output", type=Path, required=True)

    artifacts_parser = subparsers.add_parser(
        "verify-artifacts",
        aliases=["verify-run"],
        help="Verify the retained generation, quality, and condition-audit matrix.",
    )
    artifacts_parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1])
    artifacts_parser.add_argument("--freeze-manifest", type=Path, required=True)
    artifacts_parser.add_argument("--freeze-commit", required=True)
    artifacts_parser.add_argument("--plan", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "freeze":
            summary = freeze(args)
        elif args.command == "verify-freeze":
            summary = verify_freeze_manifest(
                args.source_root.absolute(), args.manifest, args.freeze_commit
            )
            summary.pop("manifest", None)
        elif args.command in ("plan", "make-plan"):
            summary = make_plan(args)
        elif args.command in ("verify-artifacts", "verify-run"):
            summary = verify_artifacts(args)
        else:  # pragma: no cover - argparse prevents this branch.
            raise HarnessError(f"unknown command: {args.command}")
    except (HarnessError, OSError, subprocess.SubprocessError) as error:
        print(f"ERROR [EVALUATION_HARNESS]: {error}", file=sys.stderr)
        return 1
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
