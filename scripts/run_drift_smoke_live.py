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
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from build_runtime_package import build


DEFAULT_SPEC = "skills/strategic-advisor/evals/drift_smoke_cases.json"
DEFAULT_OUTPUT = "evidence/evaluations/drift-smoke/run-008"
DEFAULT_CODEX = "/Applications/ChatGPT.app/Contents/Resources/codex"
PROGRESS_FILE = ".live-progress.json"


class LiveRunError(RuntimeError):
    """A target or adjudication session failed closed."""


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rendered_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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
    package_prefix = str(package_root.resolve()) + "/"
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
        for relative in runtime_paths:
            absolute = package_prefix + relative
            relative_reference = f".agents/skills/strategic-advisor/{relative}"
            reference_loop = (
                relative.startswith("references/")
                and ".agents/skills/strategic-advisor" in command
                and Path(relative).name in command
            )
            if absolute in command or relative_reference in command or reference_loop:
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
        raise LiveRunError(
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
            raise LiveRunError(
                f"invalid JSON event at {raw_path.name}:{line_number}: {error}"
            ) from error
        if not isinstance(event, dict):
            raise LiveRunError(f"non-object JSON event at {raw_path.name}:{line_number}")
        events.append(event)
    if not any(event.get("type") == "turn.completed" for event in events):
        raise LiveRunError(f"missing turn.completed in {raw_path.name}")
    return events, process.stderr


def thread_id_from(events: list[dict[str, Any]]) -> str:
    ids = {
        event.get("thread_id")
        for event in events
        if event.get("type") == "thread.started" and isinstance(event.get("thread_id"), str)
    }
    if len(ids) != 1:
        raise LiveRunError("initial target turn did not produce exactly one thread id")
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
        raise LiveRunError("turn produced no completed agent message")
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
    events, _ = run_json_events(command, prompt, raw_path, timeout)
    resolved_session = session_id or thread_id_from(events)
    answer = (
        answer_path.read_text(encoding="utf-8").strip()
        if answer_path.is_file()
        else last_agent_message(events)
    )
    if not answer:
        raise LiveRunError(f"empty target answer: {answer_path}")
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
        "Return every criterion exactly once. Use pass only when the transcript positively satisfies the "
        "requirement; uncertainty, omission, or mixed compliance is fail. For a criterion with review_turns, "
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
            raise LiveRunError(f"adjudicator returned invalid JSON for {case['id']}: {error}") from error
        if not isinstance(result, dict):
            raise LiveRunError(f"adjudicator returned non-object JSON for {case['id']}")
    criteria = result.get("criteria")
    if not isinstance(criteria, list):
        raise LiveRunError(f"adjudicator returned no criteria for {case['id']}")
    expected = {item["id"]: item for item in case["criteria"]}
    actual = {item.get("id"): item for item in criteria if isinstance(item, dict)}
    if set(actual) != set(expected) or len(actual) != len(criteria):
        raise LiveRunError(f"adjudicator criterion identity mismatch for {case['id']}")
    normalized: list[dict[str, Any]] = []
    for criterion in case["criteria"]:
        review = actual[criterion["id"]]
        expected_turns = criterion.get("review_turns", [])
        turn_reviews = review.get("turn_reviews")
        if not isinstance(turn_reviews, list):
            raise LiveRunError(f"missing turn reviews for {case['id']}.{criterion['id']}")
        actual_turns = {
            item.get("turn_id"): item for item in turn_reviews if isinstance(item, dict)
        }
        if set(actual_turns) != set(expected_turns) or len(actual_turns) != len(turn_reviews):
            raise LiveRunError(f"turn review identity mismatch for {case['id']}.{criterion['id']}")
        item = {
            "id": criterion["id"],
            "status": review["status"],
            "observation": review["observation"],
        }
        if expected_turns:
            item["turn_reviews"] = [actual_turns[turn_id] for turn_id in expected_turns]
            expected_status = (
                "pass"
                if all(actual_turns[turn_id]["status"] == "pass" for turn_id in expected_turns)
                else "fail"
            )
            if item["status"] != expected_status:
                raise LiveRunError(f"criterion/turn status mismatch for {case['id']}.{criterion['id']}")
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
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    source_root = args.source_root.resolve()
    spec_path = source_root / args.spec
    output_dir = (source_root / args.output_dir).resolve()
    if source_root not in output_dir.parents:
        raise LiveRunError("output directory must be inside the source repository")
    if not args.codex_binary.is_file():
        raise LiveRunError(f"Codex binary not found: {args.codex_binary}")
    spec_bytes = spec_path.read_bytes()
    spec = json.loads(spec_bytes.decode("utf-8"))
    model = args.model or spec.get("execution_contract", {}).get("model")
    if not isinstance(model, str) or not model:
        raise LiveRunError("target model must be supplied or frozen in execution_contract")
    progress_path = output_dir / PROGRESS_FILE
    if output_dir.exists() and not args.continue_run:
        raise LiveRunError(f"output already exists; use --continue-run: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    if progress_path.exists():
        progress = read_json(progress_path)
        if progress.get("spec_sha256") != sha256_bytes(spec_bytes):
            raise LiveRunError("progress spec identity is stale")
        target_root = Path(progress["target_root"])
        package_root = target_root / ".agents" / "skills" / "strategic-advisor"
        if not package_root.is_dir():
            raise LiveRunError("checkpoint target runtime no longer exists")
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
        progress = {
            "schema_version": 1,
            "started_at": utc_now(),
            "spec_sha256": sha256_bytes(spec_bytes),
            "target_root": str(target_root),
            "sessions": {},
            "adjudications": {},
        }
        write_json(progress_path, progress)
    manifest = read_json(output_dir / "runtime-package-manifest.json")
    runtime_paths = {item["path"] for item in manifest["files"]}
    source_records: list[dict[str, Any]] = []
    scenarios: list[dict[str, Any]] = []
    for case in spec["cases"]:
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
            for turn in turns[len(checkpoint["turns"]) :]:
                slug = safe_slug(case["id"], variant_id, turn["id"])
                print(f"TARGET {case['id']} {variant_id} {turn['id']}", flush=True)
                session_id, answer, events = target_turn(
                    codex=args.codex_binary,
                    model=model,
                    target_root=target_root,
                    session_id=checkpoint["session_id"],
                    prompt=turn["user"],
                    answer_path=output_dir / "target-answers" / f"{slug}.md",
                    raw_path=output_dir / "target-events" / f"{slug}.jsonl",
                    timeout=args.timeout,
                )
                checkpoint["session_id"] = session_id
                checkpoint["turns"].append(
                    {"id": turn["id"], "user": turn["user"], "assistant": answer}
                )
                reads = set(checkpoint["successful_runtime_reads"])
                reads.update(successful_runtime_reads(events, package_root, runtime_paths))
                checkpoint["successful_runtime_reads"] = sorted(reads)
                write_json(progress_path, progress)
            retained = {
                "session_id": checkpoint["session_id"],
                "turns": checkpoint["turns"],
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
            print(f"ADJUDICATE {case['id']}", flush=True)
            progress["adjudications"][case["id"]] = adjudicate(
                codex=args.codex_binary,
                model=args.adjudicator_model,
                case=case,
                sessions=retained_sessions,
                output_dir=output_dir,
                timeout=args.timeout,
            )
            write_json(progress_path, progress)
        reviews = progress["adjudications"][case["id"]]
        if case.get("activation") == "implicit-negative":
            trace_reads = {
                path
                for _, _turns in sessions_for(case)
                for path in progress["sessions"][f"{case['id']}::{_}"]["successful_runtime_reads"]
            }
            for review in reviews:
                if review["id"] == "ROUTINE_NO_SKILL_READ":
                    review["status"] = "pass" if not trace_reads else "fail"
                    review["observation"] = (
                        "The retained successful-command trace records no installed Strategic Advisor "
                        "runtime reads for this implicit-negative session."
                        if not trace_reads
                        else "The retained successful-command trace records an unexpected installed "
                        "Strategic Advisor runtime read."
                    )
                    review.pop("turn_reviews", None)
            progress["adjudications"][case["id"]] = reviews
            write_json(progress_path, progress)
        scenario_status = "pass" if all(item["status"] == "pass" for item in reviews) else "fail"
        scenarios.append(
            {
                "case_id": case["id"],
                "criteria": reviews,
                "sessions": retained_sessions,
                "status": scenario_status,
            }
        )
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
    cli_version = subprocess.run(
        [str(args.codex_binary), "--version"],
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    all_reads = sorted(
        {path for record in source_records for path in record["successful_runtime_reads"]}
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
        "spec_sha256": sha256_bytes(spec_bytes),
        "started_at": progress["started_at"],
        "status": "pass" if all(item["status"] == "pass" for item in scenarios) else "fail",
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
    write_json(output_dir / "result.json", result)
    print(f"RESULT {result['status']} {output_dir / 'result.json'}", flush=True)
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, LiveRunError, subprocess.SubprocessError) as error:
        print(f"FAIL [LIVE_DRIFT_SMOKE]: {error}", file=sys.stderr)
        sys.exit(1)
