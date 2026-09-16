# project-workflow:generated
"""Subordinate Codex adapter for Project Workflow execution control."""

from __future__ import annotations

import hashlib
import json
import os
import queue
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Any, TypedDict, cast

try:
    from project_workflow.adapter_common import (
        _canonical_json,
        _connect_state,
        _counter,
        _identity,
        _is_workflow_coordination_path,
        _meta_get,
        _meta_set,
        _path_allowed,
        _record_hook_event,
        _set_terminal,
        _state_snapshot,
    )
    from project_workflow.adapter_common import (
        _normalized_relative_path as _common_normalized_relative_path,
    )
except ModuleNotFoundError:  # Standalone managed CLI assets.
    from adapter_common import (  # type: ignore[import-not-found, no-redef]
        _canonical_json,
        _connect_state,
        _counter,
        _identity,
        _is_workflow_coordination_path,
        _meta_get,
        _meta_set,
        _path_allowed,
        _record_hook_event,
        _set_terminal,
        _state_snapshot,
    )
    from adapter_common import (  # type: ignore[import-not-found, no-redef]
        _normalized_relative_path as _common_normalized_relative_path,
    )

CODEX_ADAPTER_SCHEMA_VERSION = 1
CODEX_ADAPTER_KIND = "codex-app-server"
CODEX_TERMINAL_STATES = {"blocked", "failed"}
CODEX_REQUIRED_SETTINGS = {
    "schema_version",
    "adapter_kind",
    "enabled",
    "trust",
    "executable",
    "executable_identity",
    "expected_version",
    "model",
    "prompt",
    "allowed_tools",
    "allowed_command_patterns",
    "test_command_patterns",
    "required_changed_paths",
}


class CodexSettings(TypedDict):
    schema_version: int
    adapter_kind: str
    enabled: bool
    trust: str
    executable: str
    executable_identity: str
    expected_version: str
    model: str
    prompt: str
    allowed_tools: list[str]
    allowed_command_patterns: list[str]
    test_command_patterns: list[str]
    required_changed_paths: list[str]


class CodexAdapterError(RuntimeError):
    """Raised when the Codex adapter cannot preserve its declared boundary."""


def _normalized_relative_path(path: str, root: Path | None = None) -> str:
    try:
        return _common_normalized_relative_path(path, root)
    except ValueError as exc:
        raise CodexAdapterError(str(exc)) from exc


def _required_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CodexAdapterError(f"{label} must be a non-empty string")
    return value.strip()


def _string_list(value: object, label: str, *, empty: bool = False) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise CodexAdapterError(f"{label} must be a string list")
    normalized = [item.strip() for item in value]
    if any(not item for item in normalized) or len(normalized) != len(set(normalized)):
        raise CodexAdapterError(f"{label} contains an empty or duplicate value")
    if not empty and not normalized:
        raise CodexAdapterError(f"{label} must not be empty")
    return normalized


def validate_codex_settings(value: object) -> CodexSettings:
    if not isinstance(value, dict) or set(value) != CODEX_REQUIRED_SETTINGS:
        raise CodexAdapterError("Codex adapter settings have an invalid shape")
    if value.get("schema_version") != CODEX_ADAPTER_SCHEMA_VERSION:
        raise CodexAdapterError("Codex adapter schema_version is invalid")
    if value.get("adapter_kind") != CODEX_ADAPTER_KIND:
        raise CodexAdapterError("Codex adapter kind is invalid")
    if not isinstance(value.get("enabled"), bool):
        raise CodexAdapterError("Codex adapter enabled state must be boolean")
    if value.get("trust") not in {"trusted-local", "untrusted", "unknown"}:
        raise CodexAdapterError("Codex adapter trust state is invalid")
    executable = Path(_required_text(value.get("executable"), "Codex executable"))
    if not executable.is_absolute():
        raise CodexAdapterError("Codex executable must be an absolute path")
    if executable.name != "codex":
        raise CodexAdapterError("Codex executable path must name the codex binary")
    executable_identity = _required_text(
        value.get("executable_identity"), "Codex executable identity"
    )
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", executable_identity):
        raise CodexAdapterError("Codex executable identity must be a SHA-256 identity")
    for field_name in ("expected_version", "model", "prompt"):
        _required_text(value.get(field_name), f"Codex adapter {field_name}")
    allowed_tools = _string_list(value.get("allowed_tools"), "allowed_tools")
    command_patterns = _string_list(
        value.get("allowed_command_patterns"), "allowed_command_patterns", empty=True
    )
    test_patterns = _string_list(
        value.get("test_command_patterns"), "test_command_patterns", empty=True
    )
    required_changed_paths = _string_list(
        value.get("required_changed_paths"), "required_changed_paths", empty=True
    )
    required_changed_paths = [_normalized_relative_path(path) for path in required_changed_paths]
    for pattern in [*command_patterns, *test_patterns]:
        try:
            re.compile(pattern)
        except re.error as exc:
            raise CodexAdapterError(f"invalid Codex command pattern {pattern!r}: {exc}") from exc
    return cast(
        CodexSettings,
        {
            **value,
            "executable": str(executable),
            "executable_identity": executable_identity,
            "allowed_tools": allowed_tools,
            "allowed_command_patterns": command_patterns,
            "test_command_patterns": test_patterns,
            "required_changed_paths": required_changed_paths,
        },
    )


def inspect_codex_capability(value: object) -> dict[str, object]:
    """Inspect sealed local capability without executing configured code."""
    try:
        settings = validate_codex_settings(value)
        if settings["enabled"] is not True:
            raise CodexAdapterError("Codex adapter is disabled")
        if settings["trust"] != "trusted-local":
            raise CodexAdapterError(
                f"Codex adapter trust is {settings['trust']}; trusted-local is required"
            )
        executable = Path(str(settings["executable"]))
        if not executable.is_file() or not os.access(executable, os.X_OK):
            raise CodexAdapterError("Codex executable is unavailable or not executable")
        observed_identity = "sha256:" + hashlib.sha256(executable.read_bytes()).hexdigest()
        if observed_identity != settings["executable_identity"]:
            raise CodexAdapterError("Codex executable identity does not match sealed authority")
        return {
            "state": "inspectable",
            "host": "codex",
            "configuration_identity": _identity(settings),
            "executable_identity": observed_identity,
            "reason": "Sealed Codex executable and local trust are inspectable.",
        }
    except (CodexAdapterError, OSError) as exc:
        return {
            "state": "unsupported",
            "host": "codex",
            "configuration_identity": None,
            "executable_identity": None,
            "reason": str(exc),
        }


def probe_codex_capability(value: object) -> dict[str, object]:
    try:
        settings = validate_codex_settings(value)
        inspection = inspect_codex_capability(settings)
        if inspection["state"] != "inspectable":
            raise CodexAdapterError(str(inspection["reason"]))
        executable = Path(str(settings["executable"]))
        version = subprocess.run(
            [str(executable), "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        observed = version.stdout.strip()
        if version.returncode != 0 or observed != settings["expected_version"]:
            raise CodexAdapterError(
                "Codex version is unsupported: "
                f"observed {observed or '<unavailable>'}, expected {settings['expected_version']}"
            )
        app_server = subprocess.run(
            [str(executable), "app-server", "--help"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        execute = subprocess.run(
            [str(executable), "exec", "--help"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        required_app_server = ("--listen", "stdio://")
        required_exec = ("--output-schema", "--json")
        if app_server.returncode != 0 or any(
            token not in app_server.stdout for token in required_app_server
        ):
            raise CodexAdapterError("Codex App Server stdio contract is unavailable")
        if execute.returncode != 0 or any(token not in execute.stdout for token in required_exec):
            raise CodexAdapterError("Codex non-interactive typed-output contract is unavailable")
        return {
            "state": "verified",
            "host": "codex",
            "version": observed,
            "configuration_identity": _identity(settings),
            "controls": {
                name: "verified"
                for name in (
                    "app-server-events",
                    "synchronous-hooks",
                    "turn-interrupt",
                    "token-usage",
                    "typed-receipts",
                )
            },
            "reason": "Current Codex executable exposes the required supervised local contract.",
        }
    except (CodexAdapterError, OSError, subprocess.TimeoutExpired) as exc:
        return {
            "state": "unsupported",
            "host": "codex",
            "version": None,
            "configuration_identity": None,
            "controls": {},
            "reason": str(exc),
        }


def _initialize_state(path: Path, control: Mapping[str, object]) -> None:
    connection = _connect_state(path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        digest = _identity(control)
        existing = _meta_get(connection, "control_identity")
        if existing and existing != digest:
            raise CodexAdapterError("Codex hook state belongs to a different sealed control")
        if not existing:
            _meta_set(connection, "control_identity", digest)
            _meta_set(connection, "status", "running")
            _meta_set(connection, "reason", "")
            _meta_set(connection, "hook_active", "0")
            for key in ("tool-calls", "test-invocations", "worker-launches"):
                _meta_set(connection, key, 0)
        connection.execute("COMMIT")
    except Exception:
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        raise
    finally:
        connection.close()


def _deny(reason: str) -> dict[str, object]:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def _patch_paths(command: str) -> set[str]:
    matches = re.findall(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", command, re.MULTILINE)
    matches.extend(re.findall(r"^\*\*\* Move to: (.+)$", command, re.MULTILINE))
    return {path.strip() for path in matches if path.strip()}


def _git_changed_paths(root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all", "-z"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise CodexAdapterError("Codex adapter cannot read Git worktree status")
    records = result.stdout.decode(errors="replace").split("\0")
    changed: set[str] = set()
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record:
            continue
        changed.add(record[3:])
        if "R" in record[:2] or "C" in record[:2]:
            if index >= len(records) or not records[index]:
                raise CodexAdapterError("Codex adapter received incomplete Git rename status")
            changed.add(records[index])
            index += 1
    return {path for path in changed if not _is_workflow_coordination_path(path)}


def _limits(control: Mapping[str, object]) -> dict[str, dict[str, object]]:
    limits = control.get("limits")
    if not isinstance(limits, dict):
        raise CodexAdapterError("sealed control has no typed limits")
    return limits  # type: ignore[return-value]


def _maximum(control: Mapping[str, object], name: str) -> int:
    detail = _limits(control).get(name)
    if not isinstance(detail, dict) or detail.get("state") != "verified":
        raise CodexAdapterError(f"Codex adapter requires verified {name} authority")
    maximum = detail.get("maximum")
    consumed = detail.get("consumed")
    if not isinstance(maximum, int) or not isinstance(consumed, int):
        raise CodexAdapterError(f"Codex adapter {name} authority is malformed")
    receipts = control.get("receipts")
    if not isinstance(receipts, list):
        raise CodexAdapterError("sealed control has no receipt history")
    observed = 0
    for receipt in receipts:
        if not isinstance(receipt, dict):
            continue
        metrics = receipt.get("native_metrics")
        if not isinstance(metrics, dict):
            continue
        value = metrics.get(name)
        if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
            observed += value
    remaining = maximum - consumed - observed
    if remaining < 0:
        raise CodexAdapterError(f"Codex adapter {name} authority is exhausted")
    return remaining


def _reserve_pre_tool(
    control: Mapping[str, object],
    settings: CodexSettings,
    state_path: Path,
    root: Path,
    event: Mapping[str, object],
) -> str | None:
    connection = _connect_state(state_path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        if _meta_get(connection, "control_identity") != _identity(control):
            reason = "Codex hook state does not match the sealed execution control."
            _set_terminal(connection, "failed", reason)
            connection.execute("COMMIT")
            return reason
        if _meta_get(connection, "status", "running") in CODEX_TERMINAL_STATES:
            reason = _meta_get(connection, "reason", "Codex execution is terminal.")
            connection.execute("COMMIT")
            return reason
        tool_name = str(event.get("tool_name", ""))
        aliases = {tool_name}
        if tool_name == "Agent":
            aliases.add("spawn_agent")
        elif tool_name == "spawn_agent":
            aliases.add("Agent")
        elif tool_name == "Bash":
            aliases.add("exec_command")
        elif tool_name == "exec_command":
            aliases.add("Bash")
        allowed_tools = set(settings["allowed_tools"])
        if not aliases.intersection(allowed_tools):
            reason = f"Tool {tool_name or '<missing>'} is outside sealed Codex authority."
            _set_terminal(connection, "blocked", reason)
            connection.execute("COMMIT")
            return reason
        calls = _counter(connection, "tool-calls")
        if calls >= _maximum(control, "tool-calls"):
            reason = "Codex tool-call authority is exhausted."
            _set_terminal(connection, "blocked", reason)
            connection.execute("COMMIT")
            return reason
        tool_input = event.get("tool_input")
        if not isinstance(tool_input, dict):
            reason = "Codex tool input is not inspectable JSON."
            _set_terminal(connection, "blocked", reason)
            connection.execute("COMMIT")
            return reason
        is_worker = tool_name in {"Agent", "spawn_agent"}
        if is_worker and _counter(connection, "worker-launches") >= _maximum(
            control, "worker-launches"
        ):
            reason = "Codex worker-launch authority is exhausted."
            _set_terminal(connection, "blocked", reason)
            connection.execute("COMMIT")
            return reason
        command = ""
        is_test = False
        if tool_name in {"Bash", "exec_command"}:
            command_value = tool_input.get("command", tool_input.get("cmd", ""))
            if not isinstance(command_value, str) or not any(
                re.fullmatch(pattern, command_value, re.DOTALL)
                for pattern in settings["allowed_command_patterns"]
            ):
                reason = "Codex shell command is outside sealed command authority."
                _set_terminal(connection, "blocked", reason)
                connection.execute("COMMIT")
                return reason
            command = command_value
            is_test = any(
                re.fullmatch(pattern, command, re.DOTALL)
                for pattern in settings["test_command_patterns"]
            )
            if is_test:
                if _counter(connection, "test-invocations") >= _maximum(
                    control, "test-invocations"
                ):
                    reason = "Codex test-invocation authority is exhausted."
                    _set_terminal(connection, "blocked", reason)
                    connection.execute("COMMIT")
                    return reason
                digest = hashlib.sha256(command.encode()).hexdigest()
                row = connection.execute(
                    "SELECT attempts FROM test_inputs WHERE digest = ?", (digest,)
                ).fetchone()
                attempts = int(row[0]) if row else 0
                if attempts >= _maximum(control, "identical-retries") + 1:
                    reason = "Codex identical test retry authority is exhausted."
                    _set_terminal(connection, "blocked", reason)
                    connection.execute("COMMIT")
                    return reason
        patch_paths: set[str] = set()
        normalized_patch_paths: set[str] = set()
        if tool_name == "apply_patch":
            patch_value = tool_input.get(
                "command", tool_input.get("patch", tool_input.get("input", ""))
            )
            if not isinstance(patch_value, str) or not (patch_paths := _patch_paths(patch_value)):
                reason = "Codex patch targets are not inspectable."
                _set_terminal(connection, "blocked", reason)
                connection.execute("COMMIT")
                return reason
            command = patch_value
            allowed_paths = control["allowed_write_paths"]
            assert isinstance(allowed_paths, list)
            normalized_patch_paths = {_normalized_relative_path(path, root) for path in patch_paths}
            disallowed = sorted(
                path
                for path in normalized_patch_paths
                if not _path_allowed(path, allowed_paths, root)
            )
            if disallowed:
                reason = "Codex patch exceeds sealed write scope: " + ", ".join(disallowed)
                _set_terminal(connection, "blocked", reason)
                connection.execute("COMMIT")
                return reason
            existing = {str(row[0]) for row in connection.execute("SELECT path FROM changed_paths")}
            if len(existing | normalized_patch_paths) > _maximum(control, "changed-paths"):
                reason = "Codex changed-path authority is exhausted."
                _set_terminal(connection, "blocked", reason)
                connection.execute("COMMIT")
                return reason
        _meta_set(connection, "tool-calls", calls + 1)
        if is_worker:
            _meta_set(connection, "worker-launches", _counter(connection, "worker-launches") + 1)
        if is_test:
            _meta_set(
                connection,
                "test-invocations",
                _counter(connection, "test-invocations") + 1,
            )
            digest = hashlib.sha256(command.encode()).hexdigest()
            connection.execute(
                "INSERT INTO test_inputs(digest, attempts) VALUES (?, 1) "
                "ON CONFLICT(digest) DO UPDATE SET attempts = attempts + 1",
                (digest,),
            )
        for path in normalized_patch_paths:
            connection.execute("INSERT OR IGNORE INTO changed_paths(path) VALUES (?)", (path,))
        connection.execute("COMMIT")
        return None
    except Exception:
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        raise
    finally:
        connection.close()


def _post_tool_check(control: Mapping[str, object], state_path: Path, root: Path) -> None:
    changed = _git_changed_paths(root)
    allowed_paths = control["allowed_write_paths"]
    assert isinstance(allowed_paths, list)
    connection = _connect_state(state_path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        for path in changed:
            connection.execute("INSERT OR IGNORE INTO changed_paths(path) VALUES (?)", (path,))
        count = int(connection.execute("SELECT COUNT(*) FROM changed_paths").fetchone()[0])
        disallowed = sorted(
            path for path in changed if not _path_allowed(path, allowed_paths, root)
        )
        if disallowed:
            _set_terminal(
                connection,
                "blocked",
                "Codex tool changed paths outside sealed scope: " + ", ".join(disallowed),
            )
        elif count > _maximum(control, "changed-paths"):
            _set_terminal(connection, "blocked", "Codex changed-path authority is exhausted.")
        connection.execute("COMMIT")
    except Exception:
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        raise
    finally:
        connection.close()


def _sealed_workspace_root(control: Mapping[str, object]) -> Path:
    value = control.get("adapter_workspace_root")
    if not isinstance(value, str) or not Path(value).is_absolute():
        raise CodexAdapterError("sealed Codex control has no absolute workspace root")
    try:
        root = Path(value).resolve(strict=True)
    except OSError as exc:
        raise CodexAdapterError("sealed Codex workspace root is unavailable") from exc
    if not root.is_dir():
        raise CodexAdapterError("sealed Codex workspace root is not a directory")
    return root


def _event_workspace_root(control: Mapping[str, object], event: Mapping[str, object]) -> Path:
    sealed_root = _sealed_workspace_root(control)
    event_cwd = event.get("cwd")
    if not isinstance(event_cwd, str) or not Path(event_cwd).is_absolute():
        raise CodexAdapterError("Codex hook event has no absolute workspace cwd")
    try:
        observed_root = Path(event_cwd).resolve(strict=True)
    except OSError as exc:
        raise CodexAdapterError("Codex hook workspace cwd is unavailable") from exc
    if observed_root != sealed_root:
        raise CodexAdapterError("Codex hook workspace cwd does not match sealed workspace root")
    return sealed_root


def hook_main(control_path: str | None = None, state_value: str | None = None) -> int:
    control_path = control_path or os.environ.get("PROJECT_WORKFLOW_CODEX_CONTROL")
    state_value = state_value or os.environ.get("PROJECT_WORKFLOW_CODEX_STATE")
    if not control_path and not state_value:
        print("{}")
        return 0
    if not control_path or not state_value:
        print(json.dumps(_deny("Incomplete Project Workflow Codex hook environment.")))
        return 0
    try:
        control = json.loads(Path(control_path).read_text(encoding="utf-8"))
        if not isinstance(control, dict):
            raise CodexAdapterError("sealed Codex control must be an object")
        capability = control.get("capability")
        if not isinstance(capability, dict):
            raise CodexAdapterError("sealed Codex control has no capability")
        settings = validate_codex_settings(capability.get("settings"))
        state_path = Path(state_value)
        _initialize_state(state_path, control)
        event = json.load(sys.stdin)
        if not isinstance(event, dict):
            raise CodexAdapterError("Codex hook input must be an object")
        event_name = event.get("hook_event_name")
        if event_name == "SessionStart":
            _event_workspace_root(control, event)
            connection = _connect_state(state_path)
            try:
                _meta_set(connection, "hook_active", "1")
            finally:
                connection.close()
            _record_hook_event(state_path, event, decision="active")
            print(
                json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "SessionStart",
                            "additionalContext": (
                                "This Codex turn is subordinate to sealed Project Workflow "
                                f"control {control['sealed_identity']}. A denial or interrupt is "
                                "terminal; do not seek a workaround."
                            ),
                        }
                    }
                )
            )
            return 0
        if event_name == "PreToolUse":
            root = _event_workspace_root(control, event)
            reason = _reserve_pre_tool(control, settings, state_path, root, event)
            _record_hook_event(
                state_path,
                event,
                decision="denied" if reason else "allowed",
                detail=reason or "",
            )
            print(json.dumps(_deny(reason)) if reason else "{}")
            return 0
        if event_name == "PostToolUse":
            root = _event_workspace_root(control, event)
            _post_tool_check(control, state_path, root)
            _record_hook_event(state_path, event, decision="observed")
            print("{}")
            return 0
        print("{}")
        return 0
    except Exception as exc:
        print(json.dumps(_deny(f"Project Workflow Codex hook failed closed: {exc}")))
        return 0


class _JsonRpcProcess:
    def __init__(self, argv: list[str], *, cwd: Path, env: dict[str, str]) -> None:
        try:
            self.process = subprocess.Popen(
                argv,
                cwd=cwd,
                env=env,
                text=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
            )
        except OSError as exc:
            raise CodexAdapterError(f"cannot start Codex App Server: {exc}") from exc
        assert self.process.stdin and self.process.stdout and self.process.stderr
        self.messages: queue.Queue[dict[str, Any]] = queue.Queue()
        self.stderr: list[str] = []
        self.protocol_events: list[dict[str, object]] = []
        threading.Thread(target=self._read_stdout, daemon=True).start()
        threading.Thread(target=self._read_stderr, daemon=True).start()

    def _read_stdout(self) -> None:
        assert self.process.stdout
        for line in self.process.stdout:
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                self.messages.put({"_invalid": line.rstrip()})
                continue
            if isinstance(value, dict):
                self.protocol_events.append(
                    {
                        "direction": "server",
                        "method": str(value.get("method", "")),
                        "id": value.get("id"),
                        "keys": sorted(str(key) for key in value),
                    }
                )
                self.messages.put(value)

    def _read_stderr(self) -> None:
        assert self.process.stderr
        for line in self.process.stderr:
            self.stderr.append(line.rstrip())

    def send(self, method: str, params: dict[str, object], request_id: int | None = None) -> None:
        assert self.process.stdin
        payload: dict[str, object] = {"method": method, "params": params}
        if request_id is not None:
            payload["id"] = request_id
        self.protocol_events.append(
            {
                "direction": "client",
                "method": method,
                "id": request_id,
                "parameter_keys": sorted(params),
            }
        )
        try:
            self.process.stdin.write(json.dumps(payload, separators=(",", ":")) + "\n")
            self.process.stdin.flush()
        except (BrokenPipeError, OSError) as exc:
            raise CodexAdapterError("Codex App Server closed its input") from exc

    def receive(self, timeout: float) -> dict[str, Any] | None:
        try:
            return self.messages.get(timeout=timeout)
        except queue.Empty:
            return None

    def request(
        self, method: str, params: dict[str, object], request_id: int, timeout: float
    ) -> dict[str, Any]:
        self.send(method, params, request_id)
        deadline = time.monotonic() + timeout
        deferred: list[dict[str, Any]] = []
        try:
            while time.monotonic() < deadline:
                message = self.receive(max(0.01, deadline - time.monotonic()))
                if message is None:
                    continue
                if message.get("id") == request_id:
                    if "error" in message:
                        raise CodexAdapterError(f"{method} failed: {message['error']}")
                    result = message.get("result")
                    if not isinstance(result, dict):
                        raise CodexAdapterError(f"{method} returned an invalid result")
                    return result
                deferred.append(message)
        finally:
            for message in deferred:
                self.messages.put(message)
        raise CodexAdapterError(f"timed out waiting for {method}")

    def stop(self) -> None:
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=3)


def _hook_config(command: str) -> dict[str, object]:
    handler = {"type": "command", "command": command, "timeout": 5}
    return {
        "description": "Ephemeral Project Workflow sealed execution hooks.",
        "hooks": {
            "SessionStart": [{"hooks": [handler]}],
            "PreToolUse": [{"matcher": "*", "hooks": [handler]}],
            "PostToolUse": [{"matcher": "*", "hooks": [handler]}],
        },
    }


def _git_head(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise CodexAdapterError("Codex adapter requires readable Git source identity")
    return result.stdout.strip()


def _verify_runtime_hooks(
    rpc: _JsonRpcProcess, root: Path, hook_command: str, timeout: float
) -> None:
    result = rpc.request("hooks/list", {"cwds": [str(root)]}, 3, timeout)
    data = result.get("data")
    if not isinstance(data, list) or len(data) != 1 or not isinstance(data[0], dict):
        raise CodexAdapterError("Codex runtime hook inventory is unavailable")
    entry = data[0]
    hooks = entry.get("hooks")
    if not isinstance(hooks, list):
        raise CodexAdapterError("Codex runtime hook inventory is malformed")
    required = {"sessionStart", "preToolUse", "postToolUse"}
    observed = {
        str(hook.get("eventName"))
        for hook in hooks
        if isinstance(hook, dict)
        and hook.get("enabled") is True
        and hook.get("command") == hook_command
    }
    if not required.issubset(observed):
        missing = ", ".join(sorted(required - observed))
        raise CodexAdapterError(f"Codex runtime hook inventory is missing: {missing}")


def _run_codex_adapter(
    root: Path, control: Mapping[str, object], state_dir: Path
) -> dict[str, object]:
    capability = control.get("capability")
    if not isinstance(capability, dict):
        raise CodexAdapterError("sealed execution control has no capability")
    settings = validate_codex_settings(capability.get("settings"))
    budget_limit = _limits(control).get("agent-budget")
    if not isinstance(budget_limit, dict) or budget_limit.get("native_unit") != "tokens":
        raise CodexAdapterError("Codex adapter requires agent-budget authority in tokens")
    probe = probe_codex_capability(settings)
    if probe["state"] != "verified":
        raise CodexAdapterError(f"Codex capability is not supported: {probe['reason']}")
    if capability.get("configuration_identity") != probe["configuration_identity"]:
        raise CodexAdapterError("Codex capability configuration identity is stale")
    source_revision = str(control["source_revision"])
    if _git_head(root) != source_revision:
        raise CodexAdapterError("Codex adapter source revision is not current Git HEAD")
    initial_changes = _git_changed_paths(root)
    if initial_changes:
        raise CodexAdapterError("Codex adapter requires a clean starting worktree")
    os.chmod(state_dir, 0o700)
    sealed_control = {
        **control,
        "adapter_workspace_root": str(root.resolve(strict=True)),
    }
    control_path = state_dir / "control.json"
    control_path.write_bytes(_canonical_json(sealed_control) + b"\n")
    os.chmod(control_path, 0o400)
    state_path = state_dir / "state.sqlite3"
    _initialize_state(state_path, sealed_control)
    codex_home = state_dir / "codex-home"
    codex_home.mkdir(mode=0o700)
    source_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).expanduser()
    source_auth = source_home / "auth.json"
    if source_auth.is_file():
        (codex_home / "auth.json").symlink_to(source_auth)
    elif not os.environ.get("OPENAI_API_KEY"):
        raise CodexAdapterError("Codex adapter has neither auth.json nor OPENAI_API_KEY")
    hook_command = " ".join(
        shlex.quote(part)
        for part in (
            sys.executable,
            str(Path(__file__).resolve()),
            "hook",
            "--control",
            str(control_path),
            "--state",
            str(state_path),
        )
    )
    environment = os.environ.copy()
    environment["PROJECT_WORKFLOW_CODEX_CONTROL"] = str(control_path)
    environment["PROJECT_WORKFLOW_CODEX_STATE"] = str(state_path)
    environment["CODEX_HOME"] = str(codex_home)
    permission_profile = "project-workflow-sealed"
    config_path = codex_home / "config.toml"
    config_path.write_text(
        f'default_permissions = "{permission_profile}"\n\n'
        f"[permissions.{permission_profile}]\n"
        'extends = ":workspace"\n\n'
        f"[permissions.{permission_profile}.network]\n"
        "enabled = false\n",
        encoding="utf-8",
    )
    os.chmod(config_path, 0o400)
    hooks_path = codex_home / "hooks.json"
    hooks_path.write_bytes(_canonical_json(_hook_config(hook_command)) + b"\n")
    os.chmod(hooks_path, 0o400)
    command = [
        str(settings["executable"]),
        "--enable",
        "hooks",
        "app-server",
        "--listen",
        "stdio://",
    ]
    elapsed_limit = _maximum(control, "elapsed-seconds")
    token_limit = _maximum(control, "agent-budget")
    if elapsed_limit == 0 or token_limit == 0:
        raise CodexAdapterError("Codex elapsed and token authority must remain positive")
    start = time.monotonic()
    deadline = start + elapsed_limit

    def timeout(maximum: float = 20.0) -> float:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise CodexAdapterError("Codex elapsed authority is exhausted")
        return min(maximum, remaining)

    rpc = _JsonRpcProcess(command, cwd=root, env=environment)
    thread_id = ""
    turn_id = ""
    tokens = 0
    terminal_status = "failed"
    terminal_reason = "Codex App Server ended without a terminal turn event."
    interrupt_sent = False
    grace_deadline: float | None = None
    try:
        rpc.request(
            "initialize",
            {
                "clientInfo": {
                    "name": "project_workflow_codex_adapter",
                    "title": "Project Workflow Codex Adapter",
                    "version": "1.0.0",
                },
                "capabilities": {"experimentalApi": True},
            },
            1,
            timeout(),
        )
        rpc.send("initialized", {})
        thread_result = rpc.request(
            "thread/start",
            {
                "cwd": str(root),
                "runtimeWorkspaceRoots": [str(root)],
                "model": settings["model"],
                "permissions": permission_profile,
                "approvalPolicy": "never",
                "ephemeral": True,
                "config": {"bypass_hook_trust": True},
                "developerInstructions": (
                    "Execute only the sealed Project Workflow task. A denial or interrupt is "
                    "terminal; do not seek a workaround, widen proof, or create another candidate."
                ),
                "serviceName": "project_workflow_codex_adapter",
            },
            2,
            timeout(),
        )
        thread = thread_result.get("thread")
        if not isinstance(thread, dict) or not thread.get("id"):
            raise CodexAdapterError("thread/start returned no thread id")
        thread_id = str(thread["id"])
        _verify_runtime_hooks(rpc, root, hook_command, timeout())
        auth_link = codex_home / "auth.json"
        if auth_link.is_symlink():
            auth_link.unlink()
        turn_result = rpc.request(
            "turn/start",
            {
                "threadId": thread_id,
                "input": [{"type": "text", "text": settings["prompt"]}],
                "cwd": str(root),
                "runtimeWorkspaceRoots": [str(root)],
                "permissions": permission_profile,
                "approvalPolicy": "never",
            },
            4,
            timeout(),
        )
        turn = turn_result.get("turn")
        if not isinstance(turn, dict) or not turn.get("id"):
            raise CodexAdapterError("turn/start returned no turn id")
        turn_id = str(turn["id"])
        request_id = 10
        while True:
            elapsed = time.monotonic() - start
            snapshot = _state_snapshot(state_path)
            reason = ""
            if not snapshot["hook_active"] and elapsed > 15:
                reason = "Codex SessionStart hook did not activate."
            elif snapshot["status"] in CODEX_TERMINAL_STATES:
                reason = str(snapshot["reason"] or "Codex hook entered a terminal state.")
            elif elapsed >= elapsed_limit:
                reason = "Codex elapsed authority is exhausted."
            elif tokens >= token_limit:
                reason = "Codex token authority is exhausted."
            if reason and not interrupt_sent:
                terminal_reason = reason
                rpc.send(
                    "turn/interrupt",
                    {"threadId": thread_id, "turnId": turn_id},
                    request_id,
                )
                request_id += 1
                interrupt_sent = True
                grace_deadline = time.monotonic() + 8
            message = rpc.receive(0.25)
            if message:
                if "_invalid" in message:
                    raise CodexAdapterError("Codex App Server emitted malformed JSON")
                method = message.get("method")
                params = message.get("params")
                if method == "thread/tokenUsage/updated" and isinstance(params, dict):
                    usage = params.get("tokenUsage")
                    total = usage.get("total") if isinstance(usage, dict) else None
                    if isinstance(total, dict) and isinstance(total.get("totalTokens"), int):
                        tokens = int(total["totalTokens"])
                elif method == "turn/completed" and isinstance(params, dict):
                    completed = params.get("turn")
                    if isinstance(completed, dict) and str(completed.get("id")) == turn_id:
                        observed = str(completed.get("status", "failed"))
                        if interrupt_sent:
                            terminal_status = "interrupted"
                        elif observed == "completed":
                            terminal_status = "completed"
                            terminal_reason = "Codex turn completed inside sealed authority."
                        else:
                            terminal_status = "failed"
                            terminal_reason = f"Codex turn ended with {observed}."
                        break
            if rpc.process.poll() is not None:
                terminal_reason = "Codex App Server exited before turn completion."
                break
            if grace_deadline is not None and time.monotonic() >= grace_deadline:
                terminal_reason += " Codex did not acknowledge interrupt before the deadline."
                break
    except Exception as exc:
        terminal_status = "failed"
        terminal_reason = str(exc)
    finally:
        rpc.stop()
    snapshot = _state_snapshot(state_path)
    if not snapshot["hook_active"]:
        terminal_status = "failed"
        hook_reason = "Codex hook activation was not observed; no support claim is valid."
        if terminal_reason == "Codex App Server ended without a terminal turn event.":
            terminal_reason = hook_reason
        else:
            terminal_reason = terminal_reason.rstrip() + " " + hook_reason
    if snapshot["status"] in CODEX_TERMINAL_STATES and terminal_status == "completed":
        terminal_status = "interrupted"
        terminal_reason = str(snapshot["reason"])
    final_head = _git_head(root)
    final_changes = sorted(_git_changed_paths(root))
    allowed_paths = control["allowed_write_paths"]
    assert isinstance(allowed_paths, list)
    disallowed = [path for path in final_changes if not _path_allowed(path, allowed_paths, root)]
    required_changes = set(settings["required_changed_paths"])
    unsealed_required = sorted(
        path for path in required_changes if not _path_allowed(path, allowed_paths, root)
    )
    missing_required = sorted(required_changes - set(final_changes))
    closeout_failed = (
        final_head != source_revision
        or disallowed
        or unsealed_required
        or missing_required
        or (len(final_changes) > _maximum(control, "changed-paths"))
    )
    if closeout_failed:
        if unsealed_required:
            closeout_reason = "Codex required changes exceed sealed write scope: " + ", ".join(
                unsealed_required
            )
        elif missing_required:
            closeout_reason = "Codex required changes are missing: " + ", ".join(missing_required)
        else:
            closeout_reason = "Codex closeout found source or write-scope drift."
        if terminal_status == "completed":
            terminal_status = "interrupted"
            terminal_reason = closeout_reason
        else:
            terminal_reason = terminal_reason.rstrip() + " Closeout: " + closeout_reason
    elapsed = max(0, int(time.monotonic() - start))
    native_metrics = {
        "elapsed-seconds": elapsed,
        "agent-budget": tokens,
        "turns": 1,
        "tool-calls": snapshot["tool_calls"],
        "test-invocations": snapshot["test_invocations"],
        "identical-retries": snapshot["identical_retries"],
        "worker-launches": snapshot["worker_launches"],
        "changed-paths": len(final_changes),
        "write-scope": 1 if disallowed else 0,
    }
    result = {
        "adapter_schema_version": CODEX_ADAPTER_SCHEMA_VERSION,
        "adapter_kind": CODEX_ADAPTER_KIND,
        "host": "codex",
        "version": probe["version"],
        "configuration_identity": probe["configuration_identity"],
        "terminal_status": terminal_status,
        "terminal_reason": terminal_reason,
        "thread_id": thread_id,
        "turn_id": turn_id,
        "hook_active": snapshot["hook_active"],
        "native_metrics": native_metrics,
        "final_source_revision": final_head,
        "final_changed_paths": final_changes,
        "hook_events": snapshot.get("hook_events", []),
        "protocol_events": getattr(rpc, "protocol_events", []),
        "stderr_tail": rpc.stderr[-20:],
    }
    result["evidence_identity"] = _identity(result)
    return result


def run_codex_adapter(root: Path, control: Mapping[str, object]) -> dict[str, object]:
    """Run one adapter journey and always retire its ephemeral authority state."""
    state_dir = Path(tempfile.mkdtemp(prefix="project-workflow-codex-"))
    try:
        return _run_codex_adapter(root, control, state_dir)
    finally:
        shutil.rmtree(state_dir, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments == ["hook"]:
        return hook_main()
    if (
        len(arguments) == 5
        and arguments[0] == "hook"
        and arguments[1] == "--control"
        and arguments[3] == "--state"
    ):
        return hook_main(arguments[2], arguments[4])
    raise SystemExit("Codex adapter is subordinate; use `project execute --id <WORK-ID>`. ")


if __name__ == "__main__":
    raise SystemExit(main())
