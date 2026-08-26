#!/usr/bin/env python3
"""Fail-closed custom Codex app-server client prototype.

This is a transport proof, not the Strategic Advisor recommendation reviewer.
It buffers assistant output, calls a separate reviewer process, permits one
reviewed revision, and writes an assistant answer to stdout only after a pass.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


SCHEMA_VERSION = 1
MAX_REVISIONS = 1
ENVELOPE_KEYS = {
    "attempt",
    "candidate_draft",
    "controller_sha256",
    "current_user_turn",
    "gate_contract",
    "gate_contract_sha256",
    "material_state",
    "schema_version",
}
COMMON_VERDICT_KEYS = {"decision", "reason_codes", "schema_version"}
REVISION_VERDICT_KEYS = COMMON_VERDICT_KEYS | {"revision_instruction"}
DECISIONS = {"pass", "revise", "block"}
REASON_CODE = re.compile(r"[a-z0-9][a-z0-9_.-]{0,63}")
PASSIVE_EVENT_METHODS = {
    "account/rateLimits/updated",
    "item/started",
    "mcpServer/startupStatus/updated",
    "remoteControl/status/changed",
    "thread/started",
    "thread/status/changed",
    "thread/tokenUsage/updated",
    "tokenUsage/updated",
    "turn/started",
    "warning",
}
TURN_EVENT_METHODS = {
    "item/started",
    "item/agentMessage/delta",
    "item/completed",
    "turn/started",
    "turn/completed",
}


class GuardError(RuntimeError):
    """A fail-closed condition safe to report without draft content."""

    def __init__(self, code: str, exit_status: int, message: str):
        super().__init__(message)
        self.code = code
        self.exit_status = exit_status
        self.message = message


@dataclass(frozen=True)
class Verdict:
    decision: str
    reason_codes: tuple[str, ...]
    revision_instruction: str | None = None


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_text(value: object, label: str, *, maximum: int = 20000) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise GuardError("invalid_reviewer_result", 24, f"reviewer returned invalid {label}")
    return value


def parse_verdict(payload: object) -> Verdict:
    if not isinstance(payload, dict):
        raise GuardError("invalid_reviewer_result", 24, "reviewer result is not an object")
    decision = payload.get("decision")
    allowed = REVISION_VERDICT_KEYS if decision == "revise" else COMMON_VERDICT_KEYS
    if set(payload) != allowed:
        raise GuardError("invalid_reviewer_result", 24, "reviewer result fields are invalid")
    if payload.get("schema_version") != SCHEMA_VERSION or decision not in DECISIONS:
        raise GuardError("invalid_reviewer_result", 24, "reviewer result identity is invalid")
    reason_codes = payload.get("reason_codes")
    if (
        not isinstance(reason_codes, list)
        or not reason_codes
        or any(
            not isinstance(item, str) or REASON_CODE.fullmatch(item) is None
            for item in reason_codes
        )
    ):
        raise GuardError("invalid_reviewer_result", 24, "reviewer reason codes are invalid")
    instruction = None
    if decision == "revise":
        instruction = require_text(
            payload.get("revision_instruction"),
            "revision instruction",
            maximum=4000,
        )
    return Verdict(decision, tuple(reason_codes), instruction)


def reviewer_identity(command: Sequence[str]) -> dict[str, object]:
    files: dict[str, str] = {}
    for index, item in enumerate(command):
        candidate = Path(item).expanduser()
        if candidate.is_file():
            files[str(index)] = f"sha256:{sha256_file(candidate.resolve())}"
    return {
        "command_sha256": sha256_bytes(canonical_json(list(command))),
        "file_identities": files,
    }


def run_reviewer(
    command: Sequence[str], envelope: dict[str, object], timeout_seconds: float
) -> Verdict:
    if set(envelope) != ENVELOPE_KEYS:
        raise GuardError("invalid_review_envelope", 25, "internal review envelope is invalid")
    try:
        completed = subprocess.run(
            list(command),
            input=json.dumps(envelope),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise GuardError("reviewer_timeout", 21, "reviewer timed out") from error
    except OSError as error:
        raise GuardError("reviewer_unavailable", 21, "reviewer could not start") from error
    if completed.returncode != 0:
        raise GuardError("reviewer_error", 21, "reviewer exited unsuccessfully")
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise GuardError("invalid_reviewer_result", 24, "reviewer returned invalid JSON") from error
    return parse_verdict(payload)


class EvidenceRecorder:
    """Records hashes and lifecycle metadata, never prompt or draft text."""

    def __init__(self, path: Path | None, metadata: dict[str, object]):
        self.path = path
        self.records: list[dict[str, object]] = [
            {"seq": 1, "kind": "guard_start", "payload": metadata}
        ]

    def add(self, kind: str, payload: dict[str, object]) -> None:
        self.records.append(
            {"seq": len(self.records) + 1, "kind": kind, "payload": payload}
        )

    def write(self, *, delivered: bool, exit_status: int, failure_code: str | None) -> None:
        self.add(
            "guard_exit",
            {
                "delivered": delivered,
                "exit_status": exit_status,
                "failure_code": failure_code,
            },
        )
        if self.path is None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        encoded = "".join(json.dumps(item, sort_keys=True) + "\n" for item in self.records)
        self.path.write_text(encoded, encoding="utf-8")


class AppServerClient:
    def __init__(
        self,
        binary: Path,
        cwd: Path,
        model: str,
        timeout_seconds: float,
        recorder: EvidenceRecorder,
    ):
        self.binary = binary
        self.cwd = cwd
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.recorder = recorder
        self.process: subprocess.Popen[str] | None = None
        self.messages: queue.Queue[tuple[str, str | None]] = queue.Queue()
        self.readers: list[threading.Thread] = []
        self.request_id = 0
        self.thread_id: str | None = None

    def __enter__(self) -> "AppServerClient":
        try:
            self.process = subprocess.Popen(
                [str(self.binary), "app-server", "--stdio"],
                cwd=self.cwd,
                env=dict(os.environ),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
        except OSError as error:
            raise GuardError("app_server_unavailable", 20, "app-server could not start") from error
        assert self.process.stdout is not None
        assert self.process.stderr is not None
        for stream, label in (
            (self.process.stdout, "stdout"),
            (self.process.stderr, "stderr"),
        ):
            reader = threading.Thread(
                target=self._pump,
                args=(stream, label),
                daemon=True,
            )
            reader.start()
            self.readers.append(reader)
        self.recorder.add("app_server_started", {"pid_recorded": True})
        try:
            self._initialize()
        except BaseException:
            self._stop()
            raise
        return self

    def __exit__(self, *_: object) -> None:
        self._stop()

    def _stop(self) -> None:
        if self.process is None:
            return
        if self.process.poll() is None:
            self.process.terminate()
        try:
            self.process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=3)
        self.recorder.add("app_server_stopped", {"returncode": self.process.returncode})
        self.process = None

    def _pump(self, stream: Any, label: str) -> None:
        try:
            for line in stream:
                self.messages.put((label, line))
        finally:
            self.messages.put((label, None))

    def _send(self, method: str, params: dict[str, object], *, notification: bool = False) -> int:
        if self.process is None or self.process.stdin is None:
            raise GuardError("app_server_state", 20, "app-server is not available")
        message: dict[str, object] = {"method": method, "params": params}
        request_id = -1
        if not notification:
            self.request_id += 1
            request_id = self.request_id
            message["id"] = request_id
        try:
            self.process.stdin.write(json.dumps(message) + "\n")
            self.process.stdin.flush()
        except (BrokenPipeError, OSError) as error:
            raise GuardError("app_server_write", 20, "app-server input failed") from error
        self.recorder.add("client_send", {"method": method, "request_id": request_id})
        return request_id

    def _read_message(self, deadline: float) -> dict[str, object]:
        if self.process is None:
            raise GuardError("app_server_state", 20, "app-server is not available")
        while time.monotonic() < deadline:
            try:
                label, line = self.messages.get(
                    timeout=min(0.25, max(0.0, deadline - time.monotonic()))
                )
            except queue.Empty:
                if self.process.poll() is not None:
                    raise GuardError("app_server_exit", 20, "app-server exited before completion")
                continue
            if line is None:
                if self.process.poll() is not None:
                    raise GuardError("app_server_exit", 20, "app-server exited before completion")
                continue
            if label == "stderr":
                self.recorder.add(
                    "app_server_stderr",
                    {"length": len(line), "sha256": sha256_text(line)},
                )
                continue
            try:
                message = json.loads(line)
            except json.JSONDecodeError as error:
                raise GuardError("app_server_protocol", 20, "app-server emitted invalid JSON") from error
            if not isinstance(message, dict):
                raise GuardError("app_server_protocol", 20, "app-server message is invalid")
            return message
        raise GuardError("app_server_timeout", 20, "app-server turn timed out")

    def _wait_response(
        self,
        request_id: int,
        pending_turn_events: list[dict[str, object]] | None = None,
    ) -> dict[str, object]:
        deadline = time.monotonic() + self.timeout_seconds
        while True:
            message = self._read_message(deadline)
            if "id" in message and message.get("method"):
                raise GuardError("app_server_request", 20, "unexpected app-server request")
            if message.get("id") != request_id:
                if (
                    pending_turn_events is not None
                    and message.get("method") in TURN_EVENT_METHODS
                ):
                    pending_turn_events.append(message)
                    continue
                self._record_notification(message)
                continue
            if "error" in message:
                raise GuardError("app_server_error", 20, "app-server request failed")
            result = message.get("result")
            if not isinstance(result, dict):
                raise GuardError("app_server_protocol", 20, "app-server response is invalid")
            return result

    def _record_notification(self, message: dict[str, object]) -> None:
        method = message.get("method")
        if not isinstance(method, str):
            raise GuardError("app_server_protocol", 20, "app-server message has no method")
        if method not in PASSIVE_EVENT_METHODS | {
            "item/agentMessage/delta",
            "item/completed",
            "turn/completed",
        }:
            raise GuardError("app_server_protocol", 20, "unrecognised app-server event")
        params = message.get("params")
        if not isinstance(params, dict):
            raise GuardError("app_server_protocol", 20, "app-server event params are invalid")
        record: dict[str, object] = {"method": method}
        if method == "item/agentMessage/delta":
            delta = params.get("delta")
            if not isinstance(delta, str):
                raise GuardError("app_server_protocol", 20, "agent-message delta is invalid")
            record.update({"content_length": len(delta), "content_sha256": sha256_text(delta)})
        self.recorder.add("server_event", record)

    def _initialize(self) -> None:
        initialize_id = self._send(
            "initialize",
            {
                "clientInfo": {
                    "name": "strategic_advisor_guard_prototype",
                    "title": "Strategic Advisor Guard Prototype",
                    "version": "0.1.0",
                }
            },
        )
        self._wait_response(initialize_id)
        self._send("initialized", {}, notification=True)
        thread_id = self._send(
            "thread/start",
            {
                "model": self.model,
                "cwd": str(self.cwd),
                "ephemeral": True,
                "approvalPolicy": "never",
                "sandbox": "read-only",
            },
        )
        result = self._wait_response(thread_id)
        thread = result.get("thread")
        if not isinstance(thread, dict) or not isinstance(thread.get("id"), str):
            raise GuardError("app_server_protocol", 20, "thread identity is missing")
        self.thread_id = thread["id"]
        self.recorder.add("thread_started", {"thread_id_sha256": sha256_text(self.thread_id)})

    def turn(self, prompt: str, attempt: int) -> str:
        if self.thread_id is None:
            raise GuardError("app_server_state", 20, "thread is not initialized")
        request_id = self._send(
            "turn/start",
            {
                "threadId": self.thread_id,
                "input": [{"type": "text", "text": prompt}],
            },
        )
        pending_turn_events: list[dict[str, object]] = []
        result = self._wait_response(request_id, pending_turn_events)
        response_turn = result.get("turn")
        if not isinstance(response_turn, dict):
            raise GuardError("app_server_protocol", 20, "turn identity is missing")
        expected_turn_id = response_turn.get("id")
        if not isinstance(expected_turn_id, str) or not expected_turn_id:
            raise GuardError("app_server_protocol", 20, "turn identity is missing")
        deadline = time.monotonic() + self.timeout_seconds
        completed_text: str | None = None
        agent_item_id: str | None = None
        observed_turn_started = False
        completed = False
        while not completed:
            message = (
                pending_turn_events.pop(0)
                if pending_turn_events
                else self._read_message(deadline)
            )
            if "id" in message and message.get("method"):
                raise GuardError("app_server_request", 20, "unexpected app-server request")
            method = message.get("method")
            params = message.get("params")
            if not isinstance(params, dict):
                raise GuardError("app_server_protocol", 20, "app-server event params are invalid")
            if method in TURN_EVENT_METHODS:
                if params.get("threadId") != self.thread_id:
                    raise GuardError("app_server_protocol", 20, "turn event thread identity is invalid")
                if method.startswith("item/") and params.get("turnId") != expected_turn_id:
                    raise GuardError("app_server_protocol", 20, "item event turn identity is invalid")
            if method == "turn/started":
                self._record_notification(message)
                turn = params.get("turn")
                if (
                    observed_turn_started
                    or not isinstance(turn, dict)
                    or turn.get("id") != expected_turn_id
                ):
                    raise GuardError("app_server_protocol", 20, "started turn identity is invalid")
                observed_turn_started = True
            elif method == "item/started":
                self._record_notification(message)
                item = params.get("item")
                if not isinstance(item, dict):
                    raise GuardError("app_server_protocol", 20, "started item is invalid")
                item_id = item.get("id")
                item_type = item.get("type")
                if not isinstance(item_id, str) or not item_id or not isinstance(item_type, str) or not item_type:
                    raise GuardError("app_server_protocol", 20, "started item identity is invalid")
                if item_type == "agentMessage":
                    if agent_item_id is not None:
                        raise GuardError("app_server_protocol", 20, "multiple agent messages are invalid")
                    agent_item_id = item_id
            elif method == "item/agentMessage/delta":
                self._record_notification(message)
                item_id = params.get("itemId")
                if agent_item_id is None or item_id != agent_item_id:
                    raise GuardError("app_server_protocol", 20, "agent-message item identity is invalid")
            elif method == "item/completed":
                self._record_notification(message)
                item = params.get("item")
                if not isinstance(item, dict):
                    raise GuardError("app_server_protocol", 20, "completed item is invalid")
                item_id = item.get("id")
                item_type = item.get("type")
                if not isinstance(item_id, str) or not item_id or not isinstance(item_type, str) or not item_type:
                    raise GuardError("app_server_protocol", 20, "completed item identity is invalid")
                if item_type == "agentMessage":
                    if item_id != agent_item_id or completed_text is not None:
                        raise GuardError("app_server_protocol", 20, "completed agent message identity is invalid")
                    text = item.get("text")
                    if not isinstance(text, str) or not text:
                        raise GuardError("app_server_protocol", 20, "completed agent message is invalid")
                    completed_text = text
            elif method == "turn/completed":
                self._record_notification(message)
                turn = params.get("turn")
                if (
                    not isinstance(turn, dict)
                    or turn.get("id") != expected_turn_id
                    or turn.get("status") != "completed"
                ):
                    raise GuardError("app_server_turn", 20, "app-server turn did not complete")
                if not observed_turn_started or completed_text is None or agent_item_id is None:
                    raise GuardError("app_server_no_answer", 20, "app-server returned no bound assistant answer")
                items = turn.get("items")
                if not isinstance(items, list):
                    raise GuardError("app_server_protocol", 20, "completed turn items are invalid")
                matching_items = [
                    item
                    for item in items
                    if isinstance(item, dict)
                    and item.get("id") == agent_item_id
                    and item.get("type") == "agentMessage"
                    and item.get("text") == completed_text
                ]
                if len(matching_items) != 1:
                    raise GuardError("app_server_protocol", 20, "completed turn answer identity is invalid")
                completed = True
            elif method in PASSIVE_EVENT_METHODS:
                self._record_notification(message)
            elif "id" in message:
                raise GuardError("app_server_protocol", 20, "unexpected app-server response")
            elif method:
                raise GuardError("app_server_protocol", 20, "unrecognised app-server event")
        if not completed_text:
            raise GuardError("app_server_no_answer", 20, "app-server returned no assistant answer")
        self.recorder.add(
            "candidate_buffered",
            {
                "attempt": attempt,
                "content_length": len(completed_text),
                "content_sha256": sha256_text(completed_text),
            },
        )
        return completed_text


def parse_command(value: str) -> list[str]:
    try:
        command = json.loads(value)
    except json.JSONDecodeError as error:
        raise argparse.ArgumentTypeError("reviewer command must be a JSON string array") from error
    if not isinstance(command, list) or not command or any(not isinstance(item, str) for item in command):
        raise argparse.ArgumentTypeError("reviewer command must be a non-empty JSON string array")
    return command


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--codex-binary", required=True, type=Path)
    value.add_argument("--reviewer-command-json", required=True, type=parse_command)
    value.add_argument("--prompt-file", required=True, type=Path)
    value.add_argument("--material-state", required=True, type=Path)
    value.add_argument("--gate-contract", required=True, type=Path)
    value.add_argument("--cwd", required=True, type=Path)
    value.add_argument("--model", default="gpt-5.6-luna")
    value.add_argument("--review-timeout", type=float, default=30.0)
    value.add_argument("--turn-timeout", type=float, default=120.0)
    value.add_argument("--evidence", type=Path)
    return value


def read_input(path: Path, label: str) -> str:
    try:
        value = path.read_text(encoding="utf-8")
    except OSError as error:
        raise GuardError("input_unavailable", 25, f"{label} is unavailable") from error
    if not value.strip():
        raise GuardError("input_invalid", 25, f"{label} is empty")
    return value


def run(arguments: argparse.Namespace) -> tuple[int, str | None, EvidenceRecorder]:
    binary = arguments.codex_binary.resolve()
    cwd = arguments.cwd.resolve()
    if not binary.is_file() or not cwd.is_dir():
        raise GuardError("host_unavailable", 25, "selected host path is unavailable")
    prompt = read_input(arguments.prompt_file, "prompt")
    material_state = read_input(arguments.material_state, "material state")
    gate_contract = read_input(arguments.gate_contract, "gate contract")
    controller_sha = sha256_file(Path(__file__).resolve())
    metadata = {
        "app_server_binary_sha256": sha256_file(binary),
        "controller_sha256": controller_sha,
        "cwd_sha256": sha256_text(str(cwd)),
        "gate_contract_sha256": sha256_text(gate_contract),
        "material_state_sha256": sha256_text(material_state),
        "model": arguments.model,
        "prompt_sha256": sha256_text(prompt),
        "reviewer_identity": reviewer_identity(arguments.reviewer_command_json),
        "schema_version": SCHEMA_VERSION,
        "thread_approval_policy": "never",
        "thread_sandbox": "read-only",
    }
    recorder = EvidenceRecorder(arguments.evidence, metadata)
    arguments._recorder = recorder
    with AppServerClient(binary, cwd, arguments.model, arguments.turn_timeout, recorder) as client:
        candidate = client.turn(prompt, attempt=1)
        for attempt in (1, 2):
            envelope = {
                "attempt": attempt,
                "candidate_draft": candidate,
                "controller_sha256": controller_sha,
                "current_user_turn": prompt,
                "gate_contract": gate_contract,
                "gate_contract_sha256": sha256_text(gate_contract),
                "material_state": material_state,
                "schema_version": SCHEMA_VERSION,
            }
            verdict = run_reviewer(
                arguments.reviewer_command_json,
                envelope,
                arguments.review_timeout,
            )
            recorder.add(
                "review_completed",
                {
                    "attempt": attempt,
                    "candidate_sha256": sha256_text(candidate),
                    "decision": verdict.decision,
                    "reason_codes": list(verdict.reason_codes),
                    "review_envelope_sha256": sha256_bytes(canonical_json(envelope)),
                },
            )
            if verdict.decision == "pass":
                recorder.add(
                    "answer_delivered",
                    {
                        "attempt": attempt,
                        "content_length": len(candidate),
                        "content_sha256": sha256_text(candidate),
                    },
                )
                return 0, candidate, recorder
            if verdict.decision == "block":
                raise GuardError("review_blocked", 22, "reviewer blocked delivery")
            if attempt > MAX_REVISIONS:
                raise GuardError("revision_limit", 23, "reviewer requested another revision")
            assert verdict.revision_instruction is not None
            revision_prompt = (
                "Revise your previous answer using the independent review instruction below. "
                "Return only the revised answer and do not discuss the review process. "
                "Do not repeat a claim the reviewer rejected. Preserve the last supported "
                "recommendation, surviving constraints, and strongest rival unless the material "
                "state contains a qualifying delta that supports changing them. An unsupported "
                "replacement must remain a validation candidate.\n\n"
                f"Review instruction: {verdict.revision_instruction}\n\n"
                f"Material decision state:\n{material_state}\n\n"
                f"Canonical gate contract:\n{gate_contract}"
            )
            candidate = client.turn(revision_prompt, attempt=2)
    raise GuardError("guard_state", 25, "guard did not reach a delivery decision")


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    recorder: EvidenceRecorder | None = None
    try:
        status, answer, recorder = run(arguments)
    except GuardError as error:
        recorder = getattr(arguments, "_recorder", None)
        if recorder is None:
            metadata = {"schema_version": SCHEMA_VERSION, "startup_failed": True}
            recorder = EvidenceRecorder(getattr(arguments, "evidence", None), metadata)
        recorder.write(delivered=False, exit_status=error.exit_status, failure_code=error.code)
        print(f"guard failed closed: {error.code}", file=sys.stderr)
        return error.exit_status
    assert answer is not None
    recorder.write(delivered=True, exit_status=status, failure_code=None)
    sys.stdout.write(answer)
    if not answer.endswith("\n"):
        sys.stdout.write("\n")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
