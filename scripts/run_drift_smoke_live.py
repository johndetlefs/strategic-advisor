#!/usr/bin/env python3
"""Run the frozen Strategic Advisor drift smoke against an isolated runtime.

Target sessions see only the allowlisted runtime package and frozen user turns.
Criteria are disclosed later to a separate adjudication session. Progress is
checkpointed after every turn so an interrupted run can be resumed honestly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from build_runtime_package import (
    build,
    collect_files,
    load_allowlist,
    normalized_relative_path,
    package_manifest,
    reject_evaluation_content,
)

DEFAULT_SPEC = "skills/strategic-advisor/evals/drift_smoke_cases.json"
DEFAULT_OUTPUT = "evidence/evaluations/drift-smoke/run-008"
DEFAULT_CODEX = "/Applications/ChatGPT.app/Contents/Resources/codex"
PROGRESS_FILE = ".live-progress.json"
RUNNER_RECEIPT_FILE = "runner-receipt.json"
RUNNER_CAPABILITIES = (
    "request-binding",
    "selection",
    "fail-fast",
    "limits",
    "typed-outcomes",
    "checkpoint-resume",
    "input-bound-receipts",
    "transcript-regrade",
)
OUTCOME_CLASSES = (
    "pass",
    "product-failure",
    "evaluator-failure",
    "provider-failure",
    "harness-failure",
    "limit-reached",
)
ADJUDICATION_POLICY = (
    "Use pass only when the transcript positively satisfies the requirement; "
    "uncertainty, omission, or mixed compliance is fail. For a conditional clause "
    "such as 'any X credit must Y', an explicit refusal to claim X satisfies that "
    "clause; do not require the transcript to assert a premise that the retained "
    "user turns did not supply. Continue to assess every separate obligation in "
    "the criterion."
)


class LiveRunError(RuntimeError):
    """A target or adjudication session failed closed."""


class ProviderFailure(LiveRunError):
    """The external model provider or process did not complete a valid call."""


class HarnessFailure(LiveRunError):
    """The local runner could not preserve or interpret its execution contract."""


class EvaluatorFailure(LiveRunError):
    """The evaluator returned an invalid or unusable adjudication."""


class LimitReached(LiveRunError):
    """A declared campaign limit stopped work with proof still missing."""


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rendered_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_identity(value: object) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return "sha256:" + sha256_bytes(encoded)


def adapter_request_from_stdin(
    args: argparse.Namespace,
    *,
    selected_case_ids: list[str],
    limits: dict[str, int],
) -> dict[str, Any] | None:
    if not args.adapter_request_stdin:
        return None
    if not args.adapter_json:
        raise LiveRunError("--adapter-request-stdin requires --adapter-json")
    try:
        request = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        raise LiveRunError(f"adapter request is invalid JSON: {error}") from error
    if not isinstance(request, dict):
        raise LiveRunError("adapter request must be a JSON object")
    request_identity = request.get("request_identity")
    expected_identity = canonical_identity(
        {key: value for key, value in request.items() if key != "request_identity"}
    )
    if request_identity != expected_identity:
        raise LiveRunError("adapter request_identity is stale or malformed")
    for field_name in (
        "candidate_identity",
        "source_identity",
        "proof_contract_identity",
        "stage",
    ):
        if (
            not isinstance(request.get(field_name), str)
            or not request[field_name].strip()
        ):
            raise LiveRunError(
                f"adapter request {field_name} must be a non-empty string"
            )
    if request.get("schema_version") != 1:
        raise LiveRunError("adapter request schema_version must be 1")
    expected_action = "regrade" if args.regrade else "verify"
    if request.get("action") != expected_action:
        raise LiveRunError(
            "adapter request action does not match the runner invocation"
        )
    if request.get("mode") != args.mode:
        raise LiveRunError("adapter request mode does not match the runner invocation")
    if request.get("selected_scope") != selected_case_ids:
        raise LiveRunError(
            "adapter request selected_scope does not match selected cases"
        )
    if request.get("limits") != limits:
        raise LiveRunError("adapter request limits do not match the runner limits")
    prior = request.get("prior_receipt_identities")
    if not isinstance(prior, list) or any(
        not isinstance(identity, str) or not identity.strip() for identity in prior
    ):
        raise LiveRunError("adapter request prior_receipt_identities is invalid")
    retained_target = request.get("retained_target_identity")
    if args.regrade:
        if not isinstance(retained_target, str) or not retained_target.strip():
            raise LiveRunError(
                "adapter regrade request requires retained_target_identity"
            )
    elif retained_target is not None:
        raise LiveRunError(
            "adapter verify request cannot declare retained_target_identity"
        )
    return request


def positive_int(value: int | None, label: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or value <= 0:
        raise LiveRunError(f"{label} must be a positive integer")
    return value


def scalar_metadata(case: dict[str, Any], key: str) -> set[str]:
    value = case.get(key)
    if isinstance(value, str):
        return {value}
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return set(value)
    return set()


def selected_cases(
    spec: dict[str, Any], args: argparse.Namespace
) -> list[dict[str, Any]]:
    cases = spec.get("cases")
    if not isinstance(cases, list) or not cases:
        raise LiveRunError("spec contains no selectable cases")
    by_id = {case.get("id"): case for case in cases if isinstance(case, dict)}
    if len(by_id) != len(cases) or any(
        not isinstance(case_id, str) for case_id in by_id
    ):
        raise LiveRunError("spec case identities are invalid")
    requested: set[str] = set()
    selectors_used = False
    for label, values in (("case", args.case), ("affected case", args.affected_case)):
        if not values:
            continue
        selectors_used = True
        unknown = sorted(set(values) - set(by_id))
        if unknown:
            raise LiveRunError(f"unknown {label}: {', '.join(unknown)}")
        requested.update(values)
    for raw in args.metadata or []:
        selectors_used = True
        key, separator, expected = raw.partition("=")
        if not separator or not key.strip() or not expected.strip():
            raise LiveRunError("--metadata must use KEY=VALUE")
        matches = {
            case_id
            for case_id, case in by_id.items()
            if expected.strip() in scalar_metadata(case, key.strip())
        }
        if not matches:
            raise LiveRunError(f"metadata selector matched no cases: {raw}")
        requested.update(matches)
    if args.previously_failing:
        selectors_used = True
        prior = read_json(args.previously_failing)
        scenarios = prior.get("scenarios")
        if not isinstance(scenarios, list):
            raise LiveRunError("previous result has no scenarios")
        prior_failures: set[str] = set()
        for scenario in scenarios:
            if not isinstance(scenario, dict) or scenario.get("status") != "fail":
                continue
            case_id = scenario.get("case_id")
            if not isinstance(case_id, str) or not case_id.strip():
                raise LiveRunError("previous result has an invalid failing case_id")
            prior_failures.add(case_id)
        unknown = sorted(prior_failures - set(by_id))
        if unknown:
            raise LiveRunError(
                "previous result references unknown cases: " + ", ".join(unknown)
            )
        if not prior_failures:
            raise LiveRunError("previous result contains no failing cases")
        requested.update(prior_failures)
    if not selectors_used:
        requested = set(by_id)
    if not requested:
        raise LiveRunError("selection is empty")
    return [case for case in cases if case["id"] in requested]


def planned_target_calls(cases: list[dict[str, Any]]) -> int:
    return sum(len(turns) for case in cases for _variant, turns in sessions_for(case))


def runner_capabilities() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "contract": "generic-verifier-adapter",
        "runtime_dependency_required": False,
        "capabilities": list(RUNNER_CAPABILITIES),
        "selection": ["case", "metadata", "previously-failing", "affected-case"],
        "modes": ["certification", "diagnostic"],
        "outcomes": list(OUTCOME_CLASSES),
    }


def campaign_limit_reason(
    progress: dict[str, Any], limits: dict[str, int], *, for_target: bool = True
) -> str | None:
    telemetry = progress["telemetry"]
    baseline = progress.get("limit_baseline", {})
    for key, actual_key in (
        ("max_failures", "failures"),
        ("max_target_calls", "target_calls"),
        ("max_elapsed_seconds", "elapsed_seconds"),
    ):
        if key == "max_target_calls" and not for_target:
            continue
        maximum = limits[key]
        actual = telemetry[actual_key] - baseline.get(actual_key, 0)
        if actual >= maximum:
            return f"{key} reached ({actual}/{maximum})"
    return None


def record_telemetry(
    progress: dict[str, Any],
    *,
    kind: str,
    case_id: str,
    unit_id: str,
    attempt: int,
    elapsed_seconds: float,
    outcome: str,
) -> None:
    if outcome not in OUTCOME_CLASSES:
        raise HarnessFailure(f"unknown outcome class: {outcome}")
    telemetry = progress["telemetry"]
    if kind == "target":
        telemetry["target_calls"] += 1
    elif kind == "evaluator":
        telemetry["evaluator_calls"] += 1
    else:
        raise HarnessFailure(f"unknown telemetry call kind: {kind}")
    rounded_elapsed = max(1, int(math.ceil(elapsed_seconds)))
    telemetry["elapsed_seconds"] += rounded_elapsed
    telemetry["outcome_counts"][outcome] += 1
    if outcome == "product-failure":
        telemetry["failures"] += 1
    telemetry["events"].append(
        {
            "attempt": attempt,
            "case_id": case_id,
            "elapsed_seconds": rounded_elapsed,
            "kind": kind,
            "outcome": outcome,
            "unit_id": unit_id,
        }
    )


def bounded_call(
    operation: Any,
    *,
    progress: dict[str, Any],
    progress_path: Path,
    limits: dict[str, int],
    retries: int,
    kind: str,
    case_id: str,
    unit_id: str,
) -> tuple[Any, int, float]:
    for attempt in range(1, retries + 2):
        reason = campaign_limit_reason(progress, limits, for_target=kind == "target")
        if reason:
            raise LimitReached(reason)
        started = time.monotonic()
        try:
            result = operation()
        except EvaluatorFailure:
            elapsed = time.monotonic() - started
            record_telemetry(
                progress,
                kind=kind,
                case_id=case_id,
                unit_id=unit_id,
                attempt=attempt,
                elapsed_seconds=elapsed,
                outcome="evaluator-failure",
            )
            write_json(progress_path, progress)
            raise
        except (
            ProviderFailure,
            subprocess.TimeoutExpired,
            subprocess.SubprocessError,
        ) as error:
            elapsed = time.monotonic() - started
            record_telemetry(
                progress,
                kind=kind,
                case_id=case_id,
                unit_id=unit_id,
                attempt=attempt,
                elapsed_seconds=elapsed,
                outcome="provider-failure",
            )
            write_json(progress_path, progress)
            if (
                attempt <= retries
                and campaign_limit_reason(progress, limits, for_target=kind == "target")
                is None
            ):
                continue
            raise ProviderFailure(str(error)) from error
        except (LiveRunError, OSError, ValueError, json.JSONDecodeError) as error:
            elapsed = time.monotonic() - started
            record_telemetry(
                progress,
                kind=kind,
                case_id=case_id,
                unit_id=unit_id,
                attempt=attempt,
                elapsed_seconds=elapsed,
                outcome="harness-failure",
            )
            write_json(progress_path, progress)
            if (
                attempt <= retries
                and campaign_limit_reason(progress, limits, for_target=kind == "target")
                is None
            ):
                continue
            raise HarnessFailure(str(error)) from error
        return result, attempt, time.monotonic() - started
    raise HarnessFailure("bounded call exhausted without a disposition")


def current_runtime_manifest(source_root: Path) -> dict[str, Any]:
    allowlist_relative = normalized_relative_path(
        "skills/strategic-advisor/runtime-manifest.json", "allowlist path"
    )
    allowlist, allowlist_bytes, _ = load_allowlist(source_root, allowlist_relative)
    package_root_relative, files = collect_files(source_root, allowlist)
    reject_evaluation_content(source_root, files)
    return package_manifest(
        allowlist_relative,
        allowlist_bytes,
        package_root_relative,
        files,
    )


def remaining_call_timeout(
    progress: dict[str, Any], limits: dict[str, int], configured_timeout: int
) -> int:
    remaining = limits["max_elapsed_seconds"] - progress["telemetry"]["elapsed_seconds"]
    if remaining <= 0:
        raise LimitReached(
            "max_elapsed_seconds reached "
            f"({progress['telemetry']['elapsed_seconds']}/{limits['max_elapsed_seconds']})"
        )
    return min(configured_timeout, remaining)


def validate_session_checkpoints(
    progress: dict[str, Any], cases: list[dict[str, Any]]
) -> None:
    planned = {
        f"{case['id']}::{variant_id}": (case, variant_id, turns)
        for case in cases
        for variant_id, turns in sessions_for(case)
    }
    sessions = progress.get("sessions")
    if not isinstance(sessions, dict) or not set(sessions).issubset(planned):
        raise HarnessFailure(
            "checkpoint sessions fall outside the selected proof contract"
        )
    for key, checkpoint in sessions.items():
        case, variant_id, turns = planned[key]
        if not isinstance(checkpoint, dict):
            raise HarnessFailure(f"checkpoint session is invalid: {key}")
        if (
            checkpoint.get("case_id") != case["id"]
            or checkpoint.get("variant_id") != variant_id
        ):
            raise HarnessFailure(f"checkpoint session identity mismatch: {key}")
        retained = checkpoint.get("turns")
        if not isinstance(retained, list) or len(retained) > len(turns):
            raise HarnessFailure(f"checkpoint turn count is invalid: {key}")
        session_id = checkpoint.get("session_id")
        runtime_reads = checkpoint.get("successful_runtime_reads")
        if retained and (not isinstance(session_id, str) or not session_id.strip()):
            raise HarnessFailure(f"checkpoint session ID is invalid: {key}")
        if (
            not isinstance(runtime_reads, list)
            or any(not isinstance(path, str) or not path for path in runtime_reads)
            or runtime_reads != sorted(set(runtime_reads))
        ):
            raise HarnessFailure(f"checkpoint runtime-read evidence is invalid: {key}")
        for index, record in enumerate(retained):
            if not isinstance(record, dict):
                raise HarnessFailure(f"checkpoint turn is invalid: {key}:{index}")
            expected_turn = turns[index]
            base = {
                "assistant": record.get("assistant"),
                "case_id": case["id"],
                "id": record.get("id"),
                "target_contract_identity": progress["target_contract_identity"],
                "user": record.get("user"),
                "variant_id": variant_id,
            }
            if (
                record.get("id") != expected_turn["id"]
                or record.get("user") != expected_turn["user"]
                or not isinstance(record.get("assistant"), str)
                or not record["assistant"].strip()
                or record.get("receipt_identity") != canonical_identity(base)
            ):
                raise HarnessFailure(
                    f"checkpoint turn content identity mismatch: {key}:{index}"
                )
        if checkpoint.get("session_identity") != session_checkpoint_identity(
            checkpoint, progress["target_contract_identity"]
        ):
            raise HarnessFailure(f"checkpoint session content identity mismatch: {key}")


def session_checkpoint_identity(
    checkpoint: dict[str, Any], target_contract_identity: str
) -> str:
    return canonical_identity(
        {
            "case_id": checkpoint.get("case_id"),
            "session_id": checkpoint.get("session_id"),
            "successful_runtime_reads": checkpoint.get("successful_runtime_reads"),
            "target_contract_identity": target_contract_identity,
            "turn_receipt_identities": [
                record.get("receipt_identity")
                for record in checkpoint.get("turns", [])
                if isinstance(record, dict)
            ],
            "variant_id": checkpoint.get("variant_id"),
        }
    )


def final_runner_receipt(
    *,
    progress: dict[str, Any],
    outcome: str,
    artifact: str,
    target_calls_at_start: int,
    evaluator_calls_at_start: int,
    elapsed_at_start: int,
    regrade: bool,
    adapter_request: dict[str, Any] | None = None,
) -> dict[str, Any]:
    telemetry = progress["telemetry"]
    target_identity = canonical_identity(progress["sessions"])
    base = {
        "schema_version": 1,
        "contract": "generic-verifier-receipt",
        "capabilities": list(RUNNER_CAPABILITIES),
        "candidate_identity": progress["target_contract_identity"],
        "source_identity": progress["source_identity"],
        "proof_contract_identity": progress["proof_contract_identity"],
        "checkpoint_identity": progress["checkpoint_identity"],
        "mode": progress["mode"],
        "selected_scope": progress["selected_case_ids"],
        "diagnostic_decision": progress["diagnostic_decision"],
        "limits": progress["limits"],
        "outcome": outcome,
        "runtime_identity": progress["runtime_identity"],
        "target_identity": target_identity,
        "evaluator_identity": progress["evaluator_identity"],
        "artifact": artifact,
        "target_calls": telemetry["target_calls"] - target_calls_at_start,
        "evaluator_calls": telemetry["evaluator_calls"] - evaluator_calls_at_start,
        "elapsed_seconds": telemetry["elapsed_seconds"] - elapsed_at_start,
        "stage_complete": outcome in {"pass", "product-failure"},
        "regrade": regrade,
        "telemetry_totals": {
            "target_calls": telemetry["target_calls"],
            "evaluator_calls": telemetry["evaluator_calls"],
            "elapsed_seconds": telemetry["elapsed_seconds"],
            "failures": telemetry["failures"],
        },
    }
    if adapter_request is not None:
        base.update(
            {
                "verifier_candidate_identity": base["candidate_identity"],
                "verifier_source_identity": base["source_identity"],
                "verifier_proof_contract_identity": base["proof_contract_identity"],
                "request_identity": adapter_request["request_identity"],
                "candidate_identity": adapter_request["candidate_identity"],
                "source_identity": adapter_request["source_identity"],
                "proof_contract_identity": adapter_request["proof_contract_identity"],
                "stage": adapter_request["stage"],
            }
        )
    return {**base, "receipt_identity": canonical_identity(base)}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise LiveRunError(f"expected JSON object: {path}")
    return value


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(rendered_json(value), encoding="utf-8")
    os.chmod(temporary, 0o644)
    temporary.replace(path)


def sessions_for(case: dict[str, Any]) -> list[tuple[str, list[dict[str, str]]]]:
    if "variants" in case:
        return [(item["id"], item["turns"]) for item in case["variants"]]
    return [("default", case["turns"])]


def safe_slug(*parts: str) -> str:
    return "-".join(part.lower().replace("_", "-") for part in parts)


def collect_strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [text for item in value for text in collect_strings(item)]
    if isinstance(value, dict):
        return [text for item in value.values() for text in collect_strings(item)]
    return []


def successful_runtime_reads(
    events: list[dict[str, Any]], package_root: Path, runtime_paths: set[str]
) -> set[str]:
    """Reduce successful command events to package-relative runtime paths."""
    reads: set[str] = set()
    for event in events:
        if event.get("type") != "item.completed":
            continue
        item = event.get("item")
        if not isinstance(item, dict) or item.get("type") != "command_execution":
            continue
        if item.get("status") not in {None, "completed"}:
            continue
        exit_code = item.get("exit_code")
        if exit_code not in {None, 0}:
            continue
        command = item.get("command")
        if not isinstance(command, str):
            continue
        # Match whole paths, never the suffix inside a global installation.
        paths = re.findall(r"(?<![\w/.-])/[^\s\"';]*strategic-advisor/[^\s\"';]+", command)
        for path in paths:
            relative = path.split("/strategic-advisor/", 1)[1]
            if relative not in runtime_paths:
                continue  # e.g. an explicitly authorised synthetic CSV
            resolved = Path(path).resolve()
            expected = (package_root / relative).resolve()
            if resolved != expected:
                raise HarnessFailure("target read a Strategic Advisor installation outside the frozen runtime")
            reads.add(relative)
        for relative in runtime_paths:
            local = f".agents/skills/strategic-advisor/{relative}"
            if re.search(
                r"(?<![\w/.-])(?:\./)?" + re.escape(local) + r"(?=$|[\s\"';])",
                command,
            ):
                reads.add(relative)
    return reads


def run_json_events(
    command: list[str], prompt: str, raw_path: Path, timeout: int
) -> tuple[list[dict[str, Any]], str]:
    process = subprocess.run(
        command,
        input=prompt,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(process.stdout, encoding="utf-8")
    if process.returncode != 0:
        raise ProviderFailure(
            f"Codex exited {process.returncode} for {raw_path.name}: "
            f"{process.stderr.strip()[-1000:]}"
        )
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(process.stdout.splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise ProviderFailure(
                f"invalid JSON event at {raw_path.name}:{line_number}: {error}"
            ) from error
        if not isinstance(event, dict):
            raise ProviderFailure(
                f"non-object JSON event at {raw_path.name}:{line_number}"
            )
        events.append(event)
    if not any(event.get("type") == "turn.completed" for event in events):
        raise ProviderFailure(f"missing turn.completed in {raw_path.name}")
    return events, process.stderr


def thread_id_from(events: list[dict[str, Any]]) -> str:
    ids = {
        event.get("thread_id")
        for event in events
        if event.get("type") == "thread.started"
        and isinstance(event.get("thread_id"), str)
    }
    if len(ids) != 1:
        raise ProviderFailure(
            "initial target turn did not produce exactly one thread id"
        )
    return ids.pop()


def last_agent_message(events: list[dict[str, Any]]) -> str:
    messages = [
        item.get("text")
        for event in events
        if event.get("type") == "item.completed"
        and isinstance((item := event.get("item")), dict)
        and item.get("type") == "agent_message"
        and isinstance(item.get("text"), str)
        and item.get("text", "").strip()
    ]
    if not messages:
        raise ProviderFailure("turn produced no completed agent message")
    return messages[-1].strip()


def target_turn(
    *,
    codex: Path,
    model: str,
    target_root: Path,
    session_id: str | None,
    prompt: str,
    answer_path: Path,
    raw_path: Path,
    timeout: int,
) -> tuple[str, str, list[dict[str, Any]]]:
    if answer_path.exists():
        answer_path.unlink()
    hidden = [Path.home() / ".agents/skills/strategic-advisor/SKILL.md",
              Path.home() / ".codex/skills/strategic-advisor/SKILL.md"]
    skill_config = "skills.config=[" + ",".join(
        "{path=" + json.dumps(str(path)) + ",enabled=false}" for path in hidden
    ) + "]"
    routing = (
        "Runtime routing only: when Strategic Advisor applies, use only the frozen "
        f"runtime at {target_root / '.agents/skills/strategic-advisor/SKILL.md'}. "
        "Do not read another installed copy. This does not activate the skill for "
        "a request outside its normal scope.\n\n"
    )
    if session_id is None:
        command = [
            str(codex),
            "exec",
            "--ignore-user-config",
            "--ignore-rules",
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
            "-C",
            str(target_root),
            "--model",
            model,
            "--json",
            "--output-last-message",
            str(answer_path),
            "-",
        ]
    else:
        command = [
            str(codex),
            "exec",
            "resume",
            session_id,
            "--ignore-user-config",
            "--ignore-rules",
            "--skip-git-repo-check",
            "--model",
            model,
            "--json",
            "--output-last-message",
            str(answer_path),
            "-",
        ]
    command.extend(["-c", skill_config])
    events, _ = run_json_events(command, routing + prompt, raw_path, timeout)
    resolved_session = session_id or thread_id_from(events)
    answer = (
        answer_path.read_text(encoding="utf-8").strip()
        if answer_path.is_file()
        else last_agent_message(events)
    )
    if not answer:
        raise ProviderFailure(f"empty target answer: {answer_path}")
    return resolved_session, answer, events


def adjudication_schema() -> dict[str, Any]:
    status = {"type": "string", "enum": ["pass", "fail"]}
    turn_review = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "turn_id": {"type": "string", "minLength": 1},
            "status": status,
            "observation": {"type": "string", "minLength": 1},
        },
        "required": ["turn_id", "status", "observation"],
    }
    criterion = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "id": {"type": "string", "minLength": 1},
            "status": status,
            "observation": {"type": "string", "minLength": 1},
            "turn_reviews": {"type": "array", "items": turn_review},
        },
        "required": ["id", "status", "observation", "turn_reviews"],
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "criteria": {"type": "array", "items": criterion},
        },
        "required": ["criteria"],
    }


def adjudicate(
    *,
    codex: Path,
    model: str,
    case: dict[str, Any],
    sessions: list[dict[str, Any]],
    output_dir: Path,
    timeout: int,
) -> list[dict[str, Any]]:
    slug = safe_slug(case["id"])
    schema_path = output_dir / "adjudications" / f"{slug}-schema.json"
    answer_path = output_dir / "adjudications" / f"{slug}.json"
    raw_path = output_dir / "adjudications" / f"{slug}-events.jsonl"
    write_json(schema_path, adjudication_schema())
    payload = {
        "case": {
            "id": case["id"],
            "title": case.get("title"),
            "criteria": case["criteria"],
        },
        "target_sessions": sessions,
    }
    prompt = (
        "You are the independent adjudicator for a frozen synthetic behavioural test. "
        "The target model never saw the criteria below. Evaluate only the retained user/assistant turns. "
        "Target sessions ran in an isolated read-only directory containing only the installed skill; when a "
        "routine implementation prompt supplies no repository method, a concise request for the missing source "
        "is direct assistance and must not fail merely because no edit could be performed. "
        "Return every criterion exactly once. "
        + ADJUDICATION_POLICY
        + " For a criterion with review_turns, "
        "return exactly those turn ids in turn_reviews and set the criterion status to pass only when all "
        "turn reviews pass. For a criterion without review_turns, return an empty turn_reviews array. "
        "Observations must cite concrete transcript behaviour without inventing facts.\n\n"
        + rendered_json(payload)
    )
    if answer_path.exists():
        answer_path.unlink()
    with tempfile.TemporaryDirectory(prefix="sa-drift-adjudicator-") as clean:
        command = [
            str(codex),
            "exec",
            "--ignore-user-config",
            "--ignore-rules",
            "--ephemeral",
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
            "-C",
            clean,
            "--model",
            model,
            "--output-schema",
            str(schema_path),
            "--json",
            "--output-last-message",
            str(answer_path),
            "-",
        ]
        events, _ = run_json_events(command, prompt, raw_path, timeout)
    if answer_path.is_file():
        result = read_json(answer_path)
    else:
        try:
            result = json.loads(last_agent_message(events))
        except json.JSONDecodeError as error:
            raise EvaluatorFailure(
                f"adjudicator returned invalid JSON for {case['id']}: {error}"
            ) from error
        if not isinstance(result, dict):
            raise EvaluatorFailure(
                f"adjudicator returned non-object JSON for {case['id']}"
            )
    criteria = result.get("criteria")
    if not isinstance(criteria, list):
        raise EvaluatorFailure(f"adjudicator returned no criteria for {case['id']}")
    expected = {item["id"]: item for item in case["criteria"]}
    actual = {item.get("id"): item for item in criteria if isinstance(item, dict)}
    if set(actual) != set(expected) or len(actual) != len(criteria):
        raise EvaluatorFailure(
            f"adjudicator criterion identity mismatch for {case['id']}"
        )
    normalized: list[dict[str, Any]] = []
    for criterion in case["criteria"]:
        review = actual[criterion["id"]]
        expected_turns = criterion.get("review_turns", [])
        turn_reviews = review.get("turn_reviews")
        if not isinstance(turn_reviews, list):
            raise EvaluatorFailure(
                f"missing turn reviews for {case['id']}.{criterion['id']}"
            )
        actual_turns = {
            item.get("turn_id"): item for item in turn_reviews if isinstance(item, dict)
        }
        if set(actual_turns) != set(expected_turns) or len(actual_turns) != len(
            turn_reviews
        ):
            raise EvaluatorFailure(
                f"turn review identity mismatch for {case['id']}.{criterion['id']}"
            )
        item = {
            "id": criterion["id"],
            "status": review["status"],
            "observation": review["observation"],
        }
        if expected_turns:
            item["turn_reviews"] = [actual_turns[turn_id] for turn_id in expected_turns]
            expected_status = (
                "pass"
                if all(
                    actual_turns[turn_id]["status"] == "pass"
                    for turn_id in expected_turns
                )
                else "fail"
            )
            if item["status"] != expected_status:
                raise EvaluatorFailure(
                    f"criterion/turn status mismatch for {case['id']}.{criterion['id']}"
                )
        normalized.append(item)
    return normalized


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=Path.cwd())
    parser.add_argument("--spec", default=DEFAULT_SPEC)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT)
    parser.add_argument("--codex-binary", type=Path, default=Path(DEFAULT_CODEX))
    parser.add_argument("--model")
    parser.add_argument("--adjudicator-model", default="gpt-5.6-sol")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--continue-run", action="store_true")
    parser.add_argument(
        "--case", action="append", help="Run one exact case ID; repeatable"
    )
    parser.add_argument(
        "--metadata", action="append", help="Select cases by exact top-level KEY=VALUE"
    )
    parser.add_argument(
        "--previously-failing",
        type=Path,
        help="Select failed cases from a retained prior result",
    )
    parser.add_argument(
        "--affected-case",
        action="append",
        help="Select one declared affected case; repeatable",
    )
    parser.add_argument(
        "--mode", choices=("certification", "diagnostic"), default="certification"
    )
    parser.add_argument("--diagnostic-decision")
    parser.add_argument("--max-failures", type=int)
    parser.add_argument("--max-target-calls", type=int)
    parser.add_argument("--max-elapsed-seconds", type=int)
    parser.add_argument("--infrastructure-retries", type=int, choices=(0, 1), default=1)
    parser.add_argument(
        "--regrade",
        action="store_true",
        help="Re-adjudicate retained transcripts without target calls",
    )
    parser.add_argument(
        "--print-capabilities",
        action="store_true",
        help="Print the standalone generic capability contract and exit",
    )
    parser.add_argument(
        "--receipt",
        type=Path,
        help=f"Write the generic final receipt (default: OUTPUT/{RUNNER_RECEIPT_FILE})",
    )
    parser.add_argument(
        "--adapter-json",
        action="store_true",
        help="Emit only the generic final receipt JSON on stdout; progress goes to stderr",
    )
    parser.add_argument(
        "--adapter-request-stdin",
        action="store_true",
        help="Bind adapter output to one generic invocation request read from stdin",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.print_capabilities:
        print(json.dumps(runner_capabilities(), sort_keys=True, separators=(",", ":")))
        return 0
    source_root = args.source_root.resolve()
    spec_path = source_root / args.spec
    output_dir = (source_root / args.output_dir).resolve()
    if source_root not in output_dir.parents:
        raise LiveRunError("output directory must be inside the source repository")
    positive_int(args.timeout, "--timeout")
    if not args.codex_binary.is_file():
        raise LiveRunError(f"Codex binary not found: {args.codex_binary}")
    spec_bytes = spec_path.read_bytes()
    spec = json.loads(spec_bytes.decode("utf-8"))
    cases = selected_cases(spec, args)
    selected_case_ids = [case["id"] for case in cases]
    all_case_ids = [case["id"] for case in spec["cases"]]
    explicit_selection = any(
        (args.case, args.metadata, args.previously_failing, args.affected_case)
    )
    if args.mode == "diagnostic":
        if (
            not isinstance(args.diagnostic_decision, str)
            or not args.diagnostic_decision.strip()
        ):
            raise LiveRunError("diagnostic mode requires --diagnostic-decision")
        if not explicit_selection:
            raise LiveRunError("diagnostic mode requires an explicit selected scope")
        if any(
            value is None
            for value in (
                args.max_failures,
                args.max_target_calls,
                args.max_elapsed_seconds,
            )
        ):
            raise LiveRunError(
                "diagnostic mode requires explicit max-failures, max-target-calls, and "
                "max-elapsed-seconds"
            )
    elif args.diagnostic_decision:
        raise LiveRunError("--diagnostic-decision is valid only in diagnostic mode")
    if args.mode == "certification" and args.max_failures not in {None, 1}:
        raise LiveRunError("certification is fail-fast and requires max-failures 1")
    planned_calls = planned_target_calls(cases)
    max_failures = positive_int(
        args.max_failures if args.max_failures is not None else 1,
        "--max-failures",
    )
    max_target_calls = positive_int(
        (
            args.max_target_calls
            if args.max_target_calls is not None
            else planned_calls * (args.infrastructure_retries + 1)
        ),
        "--max-target-calls",
    )
    max_elapsed_seconds = positive_int(
        (
            args.max_elapsed_seconds
            if args.max_elapsed_seconds is not None
            else args.timeout
            * (planned_calls + len(cases))
            * (args.infrastructure_retries + 1)
        ),
        "--max-elapsed-seconds",
    )
    assert max_failures is not None
    assert max_target_calls is not None
    assert max_elapsed_seconds is not None
    limits = {
        "max_failures": max_failures,
        "max_target_calls": max_target_calls,
        "max_elapsed_seconds": max_elapsed_seconds,
    }
    adapter_request = adapter_request_from_stdin(
        args,
        selected_case_ids=selected_case_ids,
        limits=limits,
    )
    adapter_contract_identity = (
        canonical_identity(
            {
                field_name: adapter_request[field_name]
                for field_name in (
                    "candidate_identity",
                    "source_identity",
                    "proof_contract_identity",
                    "mode",
                    "stage",
                    "selected_scope",
                    "limits",
                )
            }
        )
        if adapter_request is not None
        else None
    )
    model = args.model or spec.get("execution_contract", {}).get("model")
    if not isinstance(model, str) or not model:
        raise LiveRunError(
            "target model must be supplied or frozen in execution_contract"
        )
    cli_version = subprocess.run(
        [str(args.codex_binary), "--version"],
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    current_manifest = current_runtime_manifest(source_root)
    runtime_identity = current_manifest["package_identity_sha256"]
    source_identity = canonical_identity(
        {
            "runtime_package_identity": runtime_identity,
            "runner_sha256": sha256_bytes(Path(__file__).read_bytes()),
            "spec_sha256": sha256_bytes(spec_bytes),
        }
    )
    proof_contract_identity = canonical_identity(
        {
            "selected_case_ids": selected_case_ids,
            "spec_sha256": sha256_bytes(spec_bytes),
        }
    )
    target_contract_identity = canonical_identity(
        {
            "cli_version": cli_version,
            "host": spec.get("execution_contract", {}).get("host", "codex-cli"),
            "model": model,
            "proof_contract_identity": proof_contract_identity,
            "source_identity": source_identity,
        }
    )
    evaluator_identity = canonical_identity(
        {
            "adjudicator_model": args.adjudicator_model,
            "policy": ADJUDICATION_POLICY,
            "schema": adjudication_schema(),
        }
    )
    checkpoint_identity = canonical_identity(
        {
            "proof_contract_identity": proof_contract_identity,
            "target_contract_identity": target_contract_identity,
        }
    )
    progress_path = output_dir / PROGRESS_FILE
    if output_dir.exists() and not args.continue_run:
        raise LiveRunError(f"output already exists; use --continue-run: {output_dir}")
    if args.regrade and not args.continue_run:
        raise LiveRunError("--regrade requires --continue-run and retained transcripts")
    output_dir.mkdir(parents=True, exist_ok=True)
    if progress_path.exists():
        progress = read_json(progress_path)
        if progress.get("schema_version") != 2:
            raise LiveRunError(
                "legacy checkpoint cannot resume under the bounded runner; start a new output"
            )
        for field_name, expected in (
            ("source_identity", source_identity),
            ("proof_contract_identity", proof_contract_identity),
            ("target_contract_identity", target_contract_identity),
            ("checkpoint_identity", checkpoint_identity),
            ("selected_case_ids", selected_case_ids),
            ("mode", args.mode),
            ("diagnostic_decision", args.diagnostic_decision),
            ("limits", limits),
            ("adapter_contract_identity", adapter_contract_identity),
        ):
            if progress.get(field_name) != expected:
                raise LiveRunError(f"checkpoint {field_name} is stale or mismatched")
        if progress.get("evaluator_identity") != evaluator_identity:
            if not args.regrade:
                raise LiveRunError(
                    "evaluator identity changed; use --regrade to retain target outputs"
                )
            progress["evaluator_identity"] = evaluator_identity
        elif args.regrade:
            raise LiveRunError("--regrade requires a changed evaluator identity")
        if (
            progress.get("outcome") in {"product-failure", "limit-reached"}
            and not args.regrade
        ):
            raise LiveRunError(
                "terminal campaign cannot resume; correct the candidate or start a new bounded "
                "diagnostic output"
            )
        validate_session_checkpoints(progress, cases)
        target_root = Path(progress["target_root"])
        package_root = target_root / ".agents" / "skills" / "strategic-advisor"
        if not package_root.is_dir():
            raise LiveRunError("checkpoint target runtime no longer exists")
        manifest = read_json(output_dir / "runtime-package-manifest.json")
        if manifest.get("package_identity_sha256") != runtime_identity:
            raise LiveRunError("checkpoint runtime package identity is stale")
        if args.regrade:
            if adapter_request is not None and adapter_request[
                "retained_target_identity"
            ] != canonical_identity(progress["sessions"]):
                raise LiveRunError(
                    "adapter retained_target_identity does not match retained transcripts"
                )
            for case_id in selected_case_ids:
                progress["adjudications"].pop(case_id, None)
            progress["limit_baseline"] = {
                key: progress["telemetry"][key]
                for key in ("failures", "target_calls", "elapsed_seconds")
            }
            progress["outcome"] = "pending"
            write_json(progress_path, progress)
    else:
        target_root = Path(tempfile.mkdtemp(prefix="sa-drift-target-"))
        package_root = target_root / ".agents" / "skills" / "strategic-advisor"
        manifest_path = output_dir / "runtime-package-manifest.json"
        build(
            source_root,
            "skills/strategic-advisor/runtime-manifest.json",
            package_root,
            manifest_path,
        )
        manifest = read_json(manifest_path)
        if manifest.get("package_identity_sha256") != runtime_identity:
            raise HarnessFailure(
                "built runtime identity differs from the current source"
            )
        progress = {
            "schema_version": 2,
            "started_at": utc_now(),
            "spec_sha256": sha256_bytes(spec_bytes),
            "source_identity": source_identity,
            "runtime_identity": runtime_identity,
            "proof_contract_identity": proof_contract_identity,
            "target_contract_identity": target_contract_identity,
            "evaluator_identity": evaluator_identity,
            "checkpoint_identity": checkpoint_identity,
            "selected_case_ids": selected_case_ids,
            "mode": args.mode,
            "diagnostic_decision": args.diagnostic_decision,
            "limits": limits,
            "adapter_contract_identity": adapter_contract_identity,
            "target_root": str(target_root),
            "sessions": {},
            "adjudications": {},
            "outcome": "pending",
            "telemetry": {
                "target_calls": 0,
                "evaluator_calls": 0,
                "elapsed_seconds": 0,
                "failures": 0,
                "outcome_counts": {outcome: 0 for outcome in OUTCOME_CLASSES},
                "events": [],
            },
        }
        write_json(progress_path, progress)
    runtime_paths = {item["path"] for item in manifest["files"]}
    start_target_calls = progress["telemetry"]["target_calls"]
    start_evaluator_calls = progress["telemetry"]["evaluator_calls"]
    start_elapsed = progress["telemetry"]["elapsed_seconds"]
    source_records: list[dict[str, Any]] = []
    scenarios: list[dict[str, Any]] = []
    outcome = "pending"
    failure_detail = ""
    try:
        for case in cases:
            retained_sessions: list[dict[str, Any]] = []
            for variant_id, turns in sessions_for(case):
                key = f"{case['id']}::{variant_id}"
                checkpoint = progress["sessions"].setdefault(
                    key,
                    {
                        "case_id": case["id"],
                        "variant_id": variant_id,
                        "session_id": None,
                        "turns": [],
                        "successful_runtime_reads": [],
                    },
                )
                if "session_identity" not in checkpoint:
                    checkpoint["session_identity"] = session_checkpoint_identity(
                        checkpoint, target_contract_identity
                    )
                    write_json(progress_path, progress)
                if args.regrade and len(checkpoint["turns"]) != len(turns):
                    raise HarnessFailure(
                        f"regrade lacks complete retained target turns for {case['id']}::{variant_id}"
                    )
                for turn in turns[len(checkpoint["turns"]) :]:
                    slug = safe_slug(case["id"], variant_id, turn["id"])
                    print(
                        f"TARGET {case['id']} {variant_id} {turn['id']}",
                        file=sys.stderr if args.adapter_json else sys.stdout,
                        flush=True,
                    )
                    operation = lambda: target_turn(
                        codex=args.codex_binary,
                        model=model,
                        target_root=target_root,
                        session_id=checkpoint["session_id"],
                        prompt=turn["user"],
                        answer_path=output_dir / "target-answers" / f"{slug}.md",
                        raw_path=output_dir / "target-events" / f"{slug}.jsonl",
                        timeout=remaining_call_timeout(progress, limits, args.timeout),
                    )
                    (session_id, answer, events), attempt, elapsed = bounded_call(
                        operation,
                        progress=progress,
                        progress_path=progress_path,
                        limits=limits,
                        retries=args.infrastructure_retries,
                        kind="target",
                        case_id=case["id"],
                        unit_id=f"{variant_id}:{turn['id']}",
                    )
                    record_telemetry(
                        progress,
                        kind="target",
                        case_id=case["id"],
                        unit_id=f"{variant_id}:{turn['id']}",
                        attempt=attempt,
                        elapsed_seconds=elapsed,
                        outcome="pass",
                    )
                    checkpoint["session_id"] = session_id
                    turn_record_base = {
                        "assistant": answer,
                        "case_id": case["id"],
                        "id": turn["id"],
                        "target_contract_identity": target_contract_identity,
                        "user": turn["user"],
                        "variant_id": variant_id,
                    }
                    checkpoint["turns"].append(
                        {
                            "id": turn["id"],
                            "user": turn["user"],
                            "assistant": answer,
                            "receipt_identity": canonical_identity(turn_record_base),
                        }
                    )
                    reads = set(checkpoint["successful_runtime_reads"])
                    reads.update(
                        successful_runtime_reads(events, package_root, runtime_paths)
                    )
                    checkpoint["successful_runtime_reads"] = sorted(reads)
                    checkpoint["session_identity"] = session_checkpoint_identity(
                        checkpoint, target_contract_identity
                    )
                    write_json(progress_path, progress)
                retained = {
                    "session_id": checkpoint["session_id"],
                    "turns": [
                        {
                            "id": retained_turn["id"],
                            "user": retained_turn["user"],
                            "assistant": retained_turn["assistant"],
                        }
                        for retained_turn in checkpoint["turns"]
                    ],
                }
                if variant_id != "default":
                    retained["variant_id"] = variant_id
                retained_sessions.append(retained)
                source_record = {
                    "case_id": case["id"],
                    "session_id": checkpoint["session_id"],
                    "successful_runtime_reads": checkpoint["successful_runtime_reads"],
                }
                if variant_id != "default":
                    source_record["variant_id"] = variant_id
                if case.get("activation") == "implicit-negative":
                    source_record["user_config_ignored"] = True
                source_records.append(source_record)
            if case["id"] not in progress["adjudications"]:
                print(
                    f"ADJUDICATE {case['id']}",
                    file=sys.stderr if args.adapter_json else sys.stdout,
                    flush=True,
                )
                operation = lambda: adjudicate(
                    codex=args.codex_binary,
                    model=args.adjudicator_model,
                    case=case,
                    sessions=retained_sessions,
                    output_dir=output_dir,
                    timeout=remaining_call_timeout(progress, limits, args.timeout),
                )
                try:
                    reviews, attempt, elapsed = bounded_call(
                        operation,
                        progress=progress,
                        progress_path=progress_path,
                        limits=limits,
                        retries=args.infrastructure_retries,
                        kind="evaluator",
                        case_id=case["id"],
                        unit_id="adjudication",
                    )
                except HarnessFailure as error:
                    raise EvaluatorFailure(str(error)) from error
                scenario_status = (
                    "pass"
                    if all(item["status"] == "pass" for item in reviews)
                    else "fail"
                )
                record_telemetry(
                    progress,
                    kind="evaluator",
                    case_id=case["id"],
                    unit_id="adjudication",
                    attempt=attempt,
                    elapsed_seconds=elapsed,
                    outcome="pass" if scenario_status == "pass" else "product-failure",
                )
                progress["adjudications"][case["id"]] = reviews
                write_json(progress_path, progress)
            reviews = progress["adjudications"][case["id"]]
            if case.get("activation") == "implicit-negative":
                trace_reads = {
                    path
                    for variant, _turns in sessions_for(case)
                    for path in progress["sessions"][f"{case['id']}::{variant}"][
                        "successful_runtime_reads"
                    ]
                }
                for review in reviews:
                    if review["id"] == "ROUTINE_NO_SKILL_READ":
                        review["status"] = "pass" if not trace_reads else "fail"
                        review["observation"] = (
                            "The retained successful-command trace records no installed Strategic "
                            "Advisor runtime reads for this implicit-negative session."
                            if not trace_reads
                            else "The retained successful-command trace records an unexpected "
                            "installed Strategic Advisor runtime read."
                        )
                        review.pop("turn_reviews", None)
                progress["adjudications"][case["id"]] = reviews
                write_json(progress_path, progress)
            scenario_status = (
                "pass" if all(item["status"] == "pass" for item in reviews) else "fail"
            )
            scenarios.append(
                {
                    "case_id": case["id"],
                    "criteria": reviews,
                    "sessions": retained_sessions,
                    "status": scenario_status,
                }
            )
            if scenario_status == "fail" and args.mode == "certification":
                outcome = "product-failure"
                failure_detail = f"blocking product/assertion failure: {case['id']}"
                break
            if len(scenarios) < len(cases):
                reason = campaign_limit_reason(progress, limits, for_target=True)
                if reason:
                    raise LimitReached(reason)
        if outcome == "pending":
            outcome = (
                "product-failure"
                if any(scenario["status"] == "fail" for scenario in scenarios)
                else "pass"
            )
    except LimitReached as error:
        outcome = "limit-reached"
        failure_detail = str(error)
    except EvaluatorFailure as error:
        outcome = "evaluator-failure"
        failure_detail = str(error)
    except (
        ProviderFailure,
        subprocess.TimeoutExpired,
        subprocess.SubprocessError,
    ) as error:
        outcome = "provider-failure"
        failure_detail = str(error)
    except (
        HarnessFailure,
        LiveRunError,
        OSError,
        ValueError,
        json.JSONDecodeError,
    ) as error:
        outcome = "harness-failure"
        failure_detail = str(error)
    progress["outcome"] = outcome
    progress["failure_detail"] = failure_detail
    write_json(progress_path, progress)
    source_evidence = {
        "observation": (
            "Successful command events were reduced to paths under the isolated allowlisted runtime. "
            "User config and repository rules were ignored for every target session."
        ),
        "records": source_records,
        "schema_version": 1,
    }
    source_path = output_dir / "source-access.json"
    write_json(source_path, source_evidence)
    source_bytes = source_path.read_bytes()
    all_reads = sorted(
        {
            path
            for record in source_records
            for path in record["successful_runtime_reads"]
        }
    )
    result = {
        "authority_commit": subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=source_root,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip(),
        "authority_commit_scope": (
            "Base lineage only because the current correction remains uncommitted; exact spec and "
            "model-visible runtime are independently bound by spec_sha256 and runtime_package_identity_sha256."
        ),
        "completed_at": utc_now(),
        "schema_version": 1,
        "scenarios": scenarios,
        "selection": {
            "mode": args.mode,
            "selected_case_ids": selected_case_ids,
            "full_suite": selected_case_ids == all_case_ids,
            "diagnostic_decision": args.diagnostic_decision,
        },
        "runner": {
            "checkpoint_identity": checkpoint_identity,
            "limits": limits,
            "outcome": outcome,
            "telemetry": progress["telemetry"],
        },
        "spec_sha256": sha256_bytes(spec_bytes),
        "started_at": progress["started_at"],
        "status": "pass" if outcome == "pass" else "fail",
        "suite_id": spec["suite_id"],
        "target": {
            "cli_version": cli_version,
            "evaluation_material_visible": False,
            "host": spec.get("execution_contract", {}).get("host", "codex-cli"),
            "model": model,
            "runtime_package_identity_sha256": manifest["package_identity_sha256"],
            "source_access": all_reads,
            "source_access_artifact": "source-access.json",
            "source_access_artifact_sha256": sha256_bytes(source_bytes),
            "visibility_control": (
                "Target sessions received only the isolated allowlisted runtime package and frozen user turns; "
                "criteria were disclosed later to separate ephemeral adjudicator sessions."
            ),
        },
    }
    result_path = output_dir / "result.json"
    write_json(result_path, result)
    receipt_path = args.receipt or (output_dir / RUNNER_RECEIPT_FILE)
    if not receipt_path.is_absolute():
        receipt_path = (source_root / receipt_path).resolve()
    receipt = final_runner_receipt(
        progress=progress,
        outcome=outcome,
        artifact=str(result_path.relative_to(source_root)),
        target_calls_at_start=start_target_calls,
        evaluator_calls_at_start=start_evaluator_calls,
        elapsed_at_start=start_elapsed,
        regrade=args.regrade,
        adapter_request=adapter_request,
    )
    write_json(receipt_path, receipt)
    if args.adapter_json:
        print(json.dumps(receipt, sort_keys=True, separators=(",", ":")), flush=True)
    else:
        print(
            f"RESULT {result['status']} outcome={outcome} target_calls={receipt['target_calls']} "
            f"evaluator_calls={receipt['evaluator_calls']} {result_path}",
            flush=True,
        )
    if failure_detail:
        print(
            f"STOP {failure_detail}",
            file=sys.stderr if args.adapter_json else sys.stdout,
            flush=True,
        )
    if args.adapter_json:
        return 0
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, LiveRunError, subprocess.SubprocessError) as error:
        print(f"FAIL [LIVE_DRIFT_SMOKE]: {error}", file=sys.stderr)
        sys.exit(1)
