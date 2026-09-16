# project-workflow:generated
"""Subordinate Claude Code adapter for Project Workflow execution control."""

from __future__ import annotations

import hashlib
import json
import os
import queue
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Mapping
from decimal import Decimal, InvalidOperation
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

CLAUDE_ADAPTER_SCHEMA_VERSION = 2
CLAUDE_ADAPTER_KIND = "claude-code-print"
CLAUDE_TERMINAL_STATES = {"blocked", "failed"}
CLAUDE_MINIMUM_VERSION = (2, 1, 217)
CLAUDE_SAFE_NATIVE_TOOLS = {"Read", "Glob", "Grep"}
CLAUDE_MAX_PROTOCOL_EVENTS = 512
CLAUDE_MAX_STDERR_LINES = 200
CLAUDE_REQUIRED_SETTINGS = {
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
    "disallowed_tools",
    "allowed_command_patterns",
    "test_command_patterns",
    "required_changed_paths",
    "required_output_identities",
    "required_validation_commands",
}


class ClaudeSettings(TypedDict):
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
    disallowed_tools: list[str]
    allowed_command_patterns: list[str]
    test_command_patterns: list[str]
    required_changed_paths: list[str]
    required_output_identities: dict[str, str]
    required_validation_commands: list[str]


class ClaudeAdapterError(RuntimeError):
    """Raised when the Claude adapter cannot preserve its declared boundary."""


def _initialize_state(path: Path, control: Mapping[str, object]) -> None:
    connection = _connect_state(path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        digest = _identity(control)
        existing = _meta_get(connection, "control_identity")
        if existing and existing != digest:
            raise ClaudeAdapterError("Claude hook state belongs to a different sealed control")
        if not existing:
            _meta_set(connection, "control_identity", digest)
            _meta_set(connection, "status", "running")
            _meta_set(connection, "reason", "")
            _meta_set(connection, "hook_active", "0")
            for key in ("tool-calls", "test-invocations", "worker-launches"):
                _meta_set(connection, key, 0)
            connection.execute(
                "CREATE TABLE IF NOT EXISTS successful_validations (command TEXT PRIMARY KEY)"
            )
        connection.execute("COMMIT")
    except Exception:
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        raise
    finally:
        connection.close()


def _git_head(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise ClaudeAdapterError("Claude adapter requires readable Git source identity")
    return result.stdout.strip()


def _git_changed_paths(root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all", "-z"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise ClaudeAdapterError("Claude adapter cannot read Git worktree status")
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
                raise ClaudeAdapterError("Claude adapter received incomplete Git rename status")
            changed.add(records[index])
            index += 1
    return {path for path in changed if not _is_workflow_coordination_path(path)}


def _maximum(control: Mapping[str, object], name: str) -> int:
    limits = control.get("limits")
    if not isinstance(limits, dict):
        raise ClaudeAdapterError("sealed control has no typed limits")
    detail = limits.get(name)
    if not isinstance(detail, dict) or detail.get("state") != "verified":
        raise ClaudeAdapterError(f"Claude adapter requires verified {name} authority")
    maximum = detail.get("maximum")
    consumed = detail.get("consumed")
    if not isinstance(maximum, int) or not isinstance(consumed, int):
        raise ClaudeAdapterError(f"Claude adapter {name} authority is malformed")
    receipts = control.get("receipts")
    if not isinstance(receipts, list):
        raise ClaudeAdapterError("sealed control has no receipt history")
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
        raise ClaudeAdapterError(f"Claude adapter {name} authority is exhausted")
    return remaining


def _post_tool_check(
    control: Mapping[str, object],
    settings: Mapping[str, object],
    state_path: Path,
    root: Path,
    event: Mapping[str, object],
) -> None:
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
                "Claude tool changed paths outside sealed scope: " + ", ".join(disallowed),
            )
        elif count > _maximum(control, "changed-paths"):
            _set_terminal(connection, "blocked", "Claude changed-path authority is exhausted.")
        tool_input = event.get("tool_input")
        command = tool_input.get("command") if isinstance(tool_input, dict) else None
        required_validations = settings.get("required_validation_commands")
        response = event.get("tool_response")
        response_failed = event.get("hook_event_name") == "PostToolUseFailure" or (
            isinstance(response, dict) and response.get("is_error") is True
        )
        if (
            isinstance(command, str)
            and isinstance(required_validations, list)
            and command in required_validations
            and not response_failed
        ):
            connection.execute(
                "INSERT OR IGNORE INTO successful_validations(command) VALUES (?)",
                (command,),
            )
        connection.execute("COMMIT")
    except Exception:
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        raise
    finally:
        connection.close()


def _required_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ClaudeAdapterError(f"{label} must be a non-empty string")
    return value.strip()


def _string_list(value: object, label: str, *, empty: bool = False) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ClaudeAdapterError(f"{label} must be a string list")
    normalized = [item.strip() for item in value]
    if any(not item for item in normalized) or len(normalized) != len(set(normalized)):
        raise ClaudeAdapterError(f"{label} contains an empty or duplicate value")
    if not empty and not normalized:
        raise ClaudeAdapterError(f"{label} must not be empty")
    return normalized


def _normalized_relative_path(path: str, root: Path | None = None) -> str:
    candidate = Path(path)
    if not path or re.match(r"^[A-Za-z]:", path):
        raise ClaudeAdapterError(f"path is not workspace-relative: {path}")
    if root is None:
        if candidate.is_absolute() or any(part in {"", ".", ".."} for part in candidate.parts):
            raise ClaudeAdapterError(f"path is not workspace-relative: {path}")
        return candidate.as_posix()
    resolved_root = root.resolve()
    resolved_target = (
        candidate.resolve() if candidate.is_absolute() else (resolved_root / candidate).resolve()
    )
    try:
        return resolved_target.relative_to(resolved_root).as_posix()
    except ValueError as exc:
        raise ClaudeAdapterError(f"path is outside the workspace: {path}") from exc


def validate_claude_settings(value: object) -> ClaudeSettings:
    if not isinstance(value, dict) or set(value) != CLAUDE_REQUIRED_SETTINGS:
        raise ClaudeAdapterError("Claude adapter settings have an invalid shape")
    if value.get("schema_version") != CLAUDE_ADAPTER_SCHEMA_VERSION:
        raise ClaudeAdapterError("Claude adapter schema_version is invalid")
    if value.get("adapter_kind") != CLAUDE_ADAPTER_KIND:
        raise ClaudeAdapterError("Claude adapter kind is invalid")
    if not isinstance(value.get("enabled"), bool):
        raise ClaudeAdapterError("Claude adapter enabled state must be boolean")
    if value.get("trust") not in {"trusted-local", "untrusted", "unknown"}:
        raise ClaudeAdapterError("Claude adapter trust state is invalid")
    executable = Path(_required_text(value.get("executable"), "Claude executable"))
    if not executable.is_absolute():
        raise ClaudeAdapterError("Claude executable must be an absolute path")
    if executable.name != "claude":
        raise ClaudeAdapterError("Claude executable path must name the claude binary")
    executable_identity = _required_text(
        value.get("executable_identity"), "Claude executable identity"
    )
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", executable_identity):
        raise ClaudeAdapterError("Claude executable identity must be a SHA-256 identity")
    for field_name in ("expected_version", "model", "prompt"):
        _required_text(value.get(field_name), f"Claude adapter {field_name}")
    allowed_tools = _string_list(value.get("allowed_tools"), "allowed_tools")
    disallowed_tools = _string_list(value.get("disallowed_tools"), "disallowed_tools", empty=True)
    if set(allowed_tools) & set(disallowed_tools):
        raise ClaudeAdapterError("Claude allowed_tools and disallowed_tools overlap")
    command_patterns = _string_list(
        value.get("allowed_command_patterns"), "allowed_command_patterns", empty=True
    )
    test_patterns = _string_list(
        value.get("test_command_patterns"), "test_command_patterns", empty=True
    )
    required_changed_paths = [
        _normalized_relative_path(path)
        for path in _string_list(
            value.get("required_changed_paths"), "required_changed_paths", empty=True
        )
    ]
    raw_output_identities = value.get("required_output_identities")
    if not isinstance(raw_output_identities, dict):
        raise ClaudeAdapterError("required_output_identities must be an object")
    required_output_identities: dict[str, str] = {}
    for raw_path, raw_identity in raw_output_identities.items():
        path = _normalized_relative_path(str(raw_path))
        identity = _required_text(raw_identity, f"required output identity for {path}")
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", identity):
            raise ClaudeAdapterError(f"required output identity for {path} is not SHA-256")
        required_output_identities[path] = identity
    required_validation_commands = _string_list(
        value.get("required_validation_commands"),
        "required_validation_commands",
        empty=True,
    )
    for pattern in [*command_patterns, *test_patterns]:
        try:
            re.compile(pattern)
        except re.error as exc:
            raise ClaudeAdapterError(f"invalid Claude command pattern {pattern!r}: {exc}") from exc
    for command in required_validation_commands:
        _literal_command(command)
        if command not in command_patterns:
            raise ClaudeAdapterError(
                "required_validation_commands must also be exact allowed_command_patterns"
            )
    return cast(
        ClaudeSettings,
        {
            **value,
            "executable": str(executable),
            "executable_identity": executable_identity,
            "allowed_tools": allowed_tools,
            "disallowed_tools": disallowed_tools,
            "allowed_command_patterns": command_patterns,
            "test_command_patterns": test_patterns,
            "required_changed_paths": required_changed_paths,
            "required_output_identities": required_output_identities,
            "required_validation_commands": required_validation_commands,
        },
    )


def _unsupported(reason: str, classification: str) -> dict[str, object]:
    return {
        "state": "unsupported",
        "classification": classification,
        "host": "claude-code",
        "configuration_identity": None,
        "executable_identity": None,
        "reason": reason,
    }


def inspect_claude_capability(value: object) -> dict[str, object]:
    """Inspect sealed local capability without executing configured code."""
    try:
        settings = validate_claude_settings(value)
        if settings["enabled"] is not True:
            return _unsupported("Claude adapter is disabled", "disabled")
        if settings["trust"] != "trusted-local":
            return _unsupported(
                f"Claude adapter trust is {settings['trust']}; trusted-local is required",
                "untrusted",
            )
        executable = Path(str(settings["executable"]))
        if not executable.is_file() or not os.access(executable, os.X_OK):
            return _unsupported("Claude executable is unavailable or not executable", "unavailable")
        observed_identity = "sha256:" + hashlib.sha256(executable.read_bytes()).hexdigest()
        if observed_identity != settings["executable_identity"]:
            return _unsupported(
                "Claude executable identity does not match sealed authority", "untrusted"
            )
        return {
            "state": "inspectable",
            "classification": "inspectable",
            "host": "claude-code",
            "configuration_identity": _identity(settings),
            "executable_identity": observed_identity,
            "reason": "Sealed Claude executable and local trust are inspectable.",
        }
    except (ClaudeAdapterError, OSError) as exc:
        return _unsupported(str(exc), "incompatible")


def probe_claude_capability(value: object) -> dict[str, object]:
    """Probe CLI and authentication contracts without making a model request."""
    try:
        settings = validate_claude_settings(value)
        inspection = inspect_claude_capability(settings)
        if inspection["state"] != "inspectable":
            raise ClaudeAdapterError(str(inspection["reason"]))
        executable = str(settings["executable"])
        version = subprocess.run(
            [executable, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        observed = (version.stdout or version.stderr).strip()
        if version.returncode != 0 or observed != settings["expected_version"]:
            raise ClaudeAdapterError(
                "Claude version is unsupported: "
                f"observed {observed or '<unavailable>'}, expected {settings['expected_version']}"
            )
        match = re.search(r"(?<!\d)(\d+)\.(\d+)\.(\d+)(?!\d)", observed)
        if match is None or tuple(int(part) for part in match.groups()) < CLAUDE_MINIMUM_VERSION:
            minimum = ".".join(str(part) for part in CLAUDE_MINIMUM_VERSION)
            raise ClaudeAdapterError(
                f"Claude version is below the supported execution-control floor {minimum}"
            )
        auth = subprocess.run(
            [executable, "auth", "status"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if auth.returncode != 0:
            raise ClaudeAdapterError("Claude authentication is unavailable")
        return {
            "state": "verified",
            "classification": "verified-at-dispatch",
            "host": "claude-code",
            "version": observed,
            "configuration_identity": _identity(settings),
            "controls": {
                name: "verified"
                for name in (
                    "print-stream",
                    "native-permissions",
                    "hook-preflight",
                    "native-turn-limit",
                    "native-budget-limit",
                    "process-timeout",
                    "typed-receipts",
                )
            },
            "reason": (
                "Exact supported Claude version and authentication are verified; native "
                "permission, plugin and stream behavior still require dispatch preflight/canary."
            ),
        }
    except (ClaudeAdapterError, OSError, subprocess.TimeoutExpired) as exc:
        reason = str(exc)
        classification = "policy-blocked" if "policy" in reason.lower() else "incompatible"
        return {
            **_unsupported(reason, classification),
            "version": None,
            "controls": {},
        }


def _literal_command(pattern: str) -> str:
    """Accept only exact shell commands that Claude native permissions can also seal."""
    if re.search(r"[\\\[\]().{}*+?|^$]", pattern):
        raise ClaudeAdapterError(
            "Claude command authority must use exact literal commands; regex-only authority "
            "cannot fail closed through native permissions"
        )
    return pattern


def _native_permission_rules(settings: ClaudeSettings, control: Mapping[str, object]) -> list[str]:
    allowed_tools = set(settings["allowed_tools"])
    supported = CLAUDE_SAFE_NATIVE_TOOLS | {"Bash", "Edit", "Write"}
    unsupported = sorted(allowed_tools - supported)
    if unsupported:
        raise ClaudeAdapterError(
            "Claude tools have no fail-closed native permission mapping: " + ", ".join(unsupported)
        )
    rules = sorted(allowed_tools & CLAUDE_SAFE_NATIVE_TOOLS)
    if allowed_tools & {"Edit", "Write"}:
        allowed_paths = control.get("allowed_write_paths")
        if not isinstance(allowed_paths, list) or not allowed_paths:
            raise ClaudeAdapterError("Claude write tools require sealed write paths")
        rules.extend(f"Edit(/{path})" for path in allowed_paths)
    if "Bash" in allowed_tools:
        patterns = settings.get("allowed_command_patterns")
        if not isinstance(patterns, list) or not patterns:
            raise ClaudeAdapterError("Claude Bash requires exact sealed command authority")
        rules.extend(f"Bash({_literal_command(str(pattern))})" for pattern in patterns)
    return rules


def _deny(reason: str) -> dict[str, object]:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def _block_loop(reason: str) -> dict[str, object]:
    return {"decision": "block", "reason": reason}


def _sealed_workspace_root(control: Mapping[str, object]) -> Path:
    value = control.get("adapter_workspace_root")
    if not isinstance(value, str) or not Path(value).is_absolute():
        raise ClaudeAdapterError("sealed Claude control has no absolute workspace root")
    try:
        root = Path(value).resolve(strict=True)
    except OSError as exc:
        raise ClaudeAdapterError("sealed Claude workspace root is unavailable") from exc
    if not root.is_dir():
        raise ClaudeAdapterError("sealed Claude workspace root is not a directory")
    return root


def _event_workspace_root(control: Mapping[str, object], event: Mapping[str, object]) -> Path:
    sealed_root = _sealed_workspace_root(control)
    event_cwd = event.get("cwd")
    if not isinstance(event_cwd, str) or not Path(event_cwd).is_absolute():
        raise ClaudeAdapterError("Claude hook event has no absolute workspace cwd")
    try:
        observed_root = Path(event_cwd).resolve(strict=True)
    except OSError as exc:
        raise ClaudeAdapterError("Claude hook workspace cwd is unavailable") from exc
    if observed_root != sealed_root:
        raise ClaudeAdapterError("Claude hook workspace cwd does not match sealed workspace root")
    return sealed_root


def _reserve_pre_tool(
    control: Mapping[str, object],
    settings: ClaudeSettings,
    state_path: Path,
    root: Path,
    event: Mapping[str, object],
) -> str | None:
    connection = _connect_state(state_path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        if _meta_get(connection, "control_identity") != _identity(control):
            reason = "Claude hook state does not match the sealed execution control."
            _set_terminal(connection, "failed", reason)
            connection.execute("COMMIT")
            return reason
        if _meta_get(connection, "status", "running") in CLAUDE_TERMINAL_STATES:
            reason = _meta_get(connection, "reason", "Claude execution is terminal.")
            connection.execute("COMMIT")
            return reason
        tool_name = str(event.get("tool_name", ""))
        aliases = {tool_name}
        if tool_name in {"Agent", "Task"}:
            aliases.update({"Agent", "Task"})
        if tool_name == "Bash":
            aliases.add("exec_command")
        if not aliases.intersection(set(settings["allowed_tools"])):
            reason = f"Tool {tool_name or '<missing>'} is outside sealed Claude authority."
            _set_terminal(connection, "blocked", reason)
            connection.execute("COMMIT")
            return reason
        tool_input = event.get("tool_input")
        if not isinstance(tool_input, dict):
            reason = "Claude tool input is not inspectable JSON."
            _set_terminal(connection, "blocked", reason)
            connection.execute("COMMIT")
            return reason
        calls = _counter(connection, "tool-calls")
        if calls >= _maximum(control, "tool-calls"):
            reason = "Claude tool-call authority is exhausted."
            _set_terminal(connection, "blocked", reason)
            connection.execute("COMMIT")
            return reason
        is_worker = tool_name in {"Agent", "Task"}
        if is_worker and _counter(connection, "worker-launches") >= _maximum(
            control, "worker-launches"
        ):
            reason = "Claude worker-launch authority is exhausted."
            _set_terminal(connection, "blocked", reason)
            connection.execute("COMMIT")
            return reason
        command = ""
        is_test = False
        if tool_name == "Bash":
            command_value = tool_input.get("command", "")
            if not isinstance(command_value, str) or not any(
                re.fullmatch(pattern, command_value, re.DOTALL)
                for pattern in settings["allowed_command_patterns"]
            ):
                reason = "Claude shell command is outside sealed command authority."
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
                    reason = "Claude test-invocation authority is exhausted."
                    _set_terminal(connection, "blocked", reason)
                    connection.execute("COMMIT")
                    return reason
                digest = hashlib.sha256(command.encode()).hexdigest()
                row = connection.execute(
                    "SELECT attempts FROM test_inputs WHERE digest = ?", (digest,)
                ).fetchone()
                attempts = int(row[0]) if row else 0
                if attempts >= _maximum(control, "identical-retries") + 1:
                    reason = "Claude identical test retry authority is exhausted."
                    _set_terminal(connection, "blocked", reason)
                    connection.execute("COMMIT")
                    return reason
        normalized_write_path: str | None = None
        if tool_name in {"Edit", "Write"}:
            raw_path = tool_input.get("file_path")
            if not isinstance(raw_path, str):
                reason = "Claude write target is not inspectable."
                _set_terminal(connection, "blocked", reason)
                connection.execute("COMMIT")
                return reason
            try:
                normalized_write_path = _normalized_relative_path(raw_path, root)
            except ClaudeAdapterError as exc:
                reason = str(exc)
                _set_terminal(connection, "blocked", reason)
                connection.execute("COMMIT")
                return reason
            allowed_paths = control["allowed_write_paths"]
            assert isinstance(allowed_paths, list)
            if not _path_allowed(normalized_write_path, allowed_paths, root):
                reason = "Claude write exceeds sealed scope: " + normalized_write_path
                _set_terminal(connection, "blocked", reason)
                connection.execute("COMMIT")
                return reason
            existing = {str(row[0]) for row in connection.execute("SELECT path FROM changed_paths")}
            if len(existing | {normalized_write_path}) > _maximum(control, "changed-paths"):
                reason = "Claude changed-path authority is exhausted."
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
        if normalized_write_path is not None:
            connection.execute(
                "INSERT OR IGNORE INTO changed_paths(path) VALUES (?)", (normalized_write_path,)
            )
        connection.execute("COMMIT")
        return None
    except Exception:
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        raise
    finally:
        connection.close()


def hook_main(control_path: str | None = None, state_value: str | None = None) -> int:
    control_path = control_path or os.environ.get("PROJECT_WORKFLOW_CLAUDE_CONTROL")
    state_value = state_value or os.environ.get("PROJECT_WORKFLOW_CLAUDE_STATE")
    if not control_path and not state_value:
        print("{}")
        return 0
    if not control_path or not state_value:
        print(json.dumps(_deny("Incomplete Project Workflow Claude hook environment.")))
        return 0
    event_name = ""
    state_path: Path | None = None
    try:
        control = json.loads(Path(control_path).read_text(encoding="utf-8"))
        if not isinstance(control, dict):
            raise ClaudeAdapterError("sealed Claude control must be an object")
        capability = control.get("capability")
        if not isinstance(capability, dict):
            raise ClaudeAdapterError("sealed Claude control has no capability")
        settings = validate_claude_settings(capability.get("settings"))
        state_path = Path(state_value)
        _initialize_state(state_path, control)
        event = json.load(sys.stdin)
        if not isinstance(event, dict):
            raise ClaudeAdapterError("Claude hook input must be an object")
        event_name = str(event.get("hook_event_name", ""))
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
                                "This Claude turn is subordinate to sealed Project Workflow "
                                f"control {control['sealed_identity']}. A denial or termination "
                                "is terminal; do not seek a workaround."
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
        if event_name in {"PostToolUse", "PostToolUseFailure"}:
            root = _event_workspace_root(control, event)
            _post_tool_check(control, settings, state_path, root, event)
            _record_hook_event(state_path, event, decision="observed")
            snapshot = _state_snapshot(state_path)
            reason = str(snapshot["reason"] or "Claude execution is terminal.")
            print(
                json.dumps(_block_loop(reason))
                if snapshot["status"] in CLAUDE_TERMINAL_STATES
                else "{}"
            )
            return 0
        if event_name == "PostToolBatch":
            root = _event_workspace_root(control, event)
            _post_tool_check(control, settings, state_path, root, event)
            _record_hook_event(state_path, event, decision="observed")
            snapshot = _state_snapshot(state_path)
            reason = str(snapshot["reason"] or "Claude execution is terminal.")
            print(
                json.dumps(_block_loop(reason))
                if snapshot["status"] in CLAUDE_TERMINAL_STATES
                else "{}"
            )
            return 0
        if event_name == "Stop":
            _event_workspace_root(control, event)
            _record_hook_event(state_path, event, decision="observed")
            print("{}")
            return 0
        print("{}")
        return 0
    except Exception as exc:
        reason = f"Project Workflow Claude hook failed closed: {exc}"
        if state_path is not None:
            try:
                connection = _connect_state(state_path)
                try:
                    _set_terminal(connection, "failed", reason)
                finally:
                    connection.close()
            except Exception:
                pass
        if event_name == "PreToolUse":
            print(json.dumps(_deny(reason)))
            return 0
        if event_name in {"PostToolUse", "PostToolUseFailure", "PostToolBatch", "Stop"}:
            print(json.dumps(_block_loop(reason)))
            return 0
        print("{}")
        return 2


class _StreamProcess:
    def __init__(self, argv: list[str], *, cwd: Path, env: dict[str, str]) -> None:
        try:
            self.process = subprocess.Popen(
                argv,
                cwd=cwd,
                env=env,
                text=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                start_new_session=True,
            )
        except OSError as exc:
            raise ClaudeAdapterError(f"cannot start Claude print mode: {exc}") from exc
        assert self.process.stdout and self.process.stderr
        self.messages: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=1024)
        self.stderr: list[str] = []
        self.protocol_events: list[dict[str, object]] = []
        self._overflowed = False
        self._stdout_thread = threading.Thread(target=self._read_stdout, daemon=True)
        self._stderr_thread = threading.Thread(target=self._read_stderr, daemon=True)
        self._stdout_thread.start()
        self._stderr_thread.start()

    def _put_message(self, value: dict[str, Any]) -> None:
        try:
            self.messages.put(value, timeout=0.2)
        except queue.Full:
            if not self._overflowed:
                self._overflowed = True
                try:
                    self.messages.get_nowait()
                except queue.Empty:
                    pass
                self.messages.put_nowait({"_overflow": True})

    def _read_stdout(self) -> None:
        assert self.process.stdout
        for line in self.process.stdout:
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                self._put_message({"_invalid": line.rstrip()[:1000]})
                continue
            if isinstance(value, dict):
                if len(self.protocol_events) < CLAUDE_MAX_PROTOCOL_EVENTS:
                    self.protocol_events.append(
                        {
                            "type": str(value.get("type", "")),
                            "subtype": str(value.get("subtype", "")),
                            "keys": sorted(str(key) for key in value),
                        }
                    )
                self._put_message(value)

    def _read_stderr(self) -> None:
        assert self.process.stderr
        for line in self.process.stderr:
            self.stderr.append(line.rstrip()[:2000])
            if len(self.stderr) > CLAUDE_MAX_STDERR_LINES:
                del self.stderr[: len(self.stderr) - CLAUDE_MAX_STDERR_LINES]

    def receive(self, timeout: float) -> dict[str, Any] | None:
        try:
            return self.messages.get(timeout=timeout)
        except queue.Empty:
            return None

    def poll(self) -> int | None:
        return self.process.poll()

    def stop(self) -> None:
        try:
            os.killpg(self.process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        if self.process.poll() is None:
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(self.process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                self.process.wait(timeout=3)
        self._stdout_thread.join(timeout=3)
        self._stderr_thread.join(timeout=3)

    def drain(self) -> list[dict[str, Any]]:
        drained: list[dict[str, Any]] = []
        while True:
            try:
                drained.append(self.messages.get_nowait())
            except queue.Empty:
                return drained


def _microdollars_to_usd(value: int) -> str:
    return format(Decimal(value) / Decimal(1_000_000), "f")


def _result_microdollars(value: object) -> int:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ClaudeAdapterError("Claude result has invalid total_cost_usd") from exc
    if not amount.is_finite() or amount < 0:
        raise ClaudeAdapterError("Claude result has invalid total_cost_usd")
    microdollars = amount * Decimal(1_000_000)
    if microdollars != microdollars.to_integral_value():
        raise ClaudeAdapterError("Claude result cost is more precise than USD microdollars")
    return int(microdollars)


def _plugin_root() -> Path:
    return Path(__file__).resolve().parent / "claude_plugin" / "project-workflow-execution-control"


def _terminate_process_group(process: subprocess.Popen[str]) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    if process.poll() is None:
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=3)


def _run_hook_preflight(
    executable: str,
    plugin_root: Path,
    root: Path,
    environment: dict[str, str],
    state_path: Path,
    timeout: int,
) -> None:
    command = [
        executable,
        "--init-only",
        "--plugin-dir",
        str(plugin_root),
        "--setting-sources",
        "user",
        "--no-chrome",
        "--strict-mcp-config",
        "--mcp-config",
        '{"mcpServers":{}}',
    ]
    try:
        process = subprocess.Popen(
            command,
            cwd=root,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
    except OSError as exc:
        raise ClaudeAdapterError(f"cannot start Claude hook preflight: {exc}") from exc
    try:
        _stdout, stderr = process.communicate(timeout=max(1, min(timeout, 30)))
    except subprocess.TimeoutExpired as exc:
        _terminate_process_group(process)
        raise ClaudeAdapterError("Claude hook preflight timed out") from exc
    finally:
        _terminate_process_group(process)
    snapshot = _state_snapshot(state_path)
    if process.returncode != 0 or not snapshot["hook_active"]:
        detail = " ".join((stderr or "").split())[-500:]
        raise ClaudeAdapterError(
            "Claude package-owned SessionStart hook preflight did not activate"
            + (f": {detail}" if detail else "")
        )


def _run_claude_adapter(
    root: Path, control: Mapping[str, object], state_dir: Path
) -> dict[str, object]:
    capability = control.get("capability")
    if not isinstance(capability, dict):
        raise ClaudeAdapterError("sealed execution control has no capability")
    settings = validate_claude_settings(capability.get("settings"))
    proof_obligations = control.get("proof_obligations", [])
    if not isinstance(proof_obligations, list):
        raise ClaudeAdapterError("sealed execution control has malformed proof obligations")
    if proof_obligations and not (
        settings["required_output_identities"] or settings["required_validation_commands"]
    ):
        raise ClaudeAdapterError(
            "Claude material execution requires sealed output identities or validation commands"
        )
    limits = control.get("limits")
    if not isinstance(limits, dict):
        raise ClaudeAdapterError("sealed execution control has malformed limits")
    budget_limit = limits.get("agent-budget")
    if not isinstance(budget_limit, dict) or budget_limit.get("native_unit") != "usd-micros":
        raise ClaudeAdapterError("Claude adapter requires agent-budget authority in usd-micros")
    turns_limit = limits.get("turns")
    if not isinstance(turns_limit, dict) or turns_limit.get("native_unit") != "turns":
        raise ClaudeAdapterError("Claude adapter requires turns authority in turns")
    probe = probe_claude_capability(settings)
    if probe["state"] != "verified":
        raise ClaudeAdapterError(f"Claude capability is not supported: {probe['reason']}")
    if capability.get("configuration_identity") != probe["configuration_identity"]:
        raise ClaudeAdapterError("Claude capability configuration identity is stale")
    source_revision = str(control["source_revision"])
    if _git_head(root) != source_revision:
        raise ClaudeAdapterError("Claude adapter source revision is not current Git HEAD")
    if _git_changed_paths(root):
        raise ClaudeAdapterError("Claude adapter requires a clean starting worktree")
    os.chmod(state_dir, 0o700)
    sealed_control = {**control, "adapter_workspace_root": str(root.resolve(strict=True))}
    control_path = state_dir / "control.json"
    control_path.write_bytes(_canonical_json(sealed_control) + b"\n")
    os.chmod(control_path, 0o400)
    state_path = state_dir / "state.sqlite3"
    _initialize_state(state_path, sealed_control)
    config_dir = state_dir / "claude-config"
    config_dir.mkdir(mode=0o700)
    plugin_root = _plugin_root()
    required_plugin_files = (
        plugin_root / ".claude-plugin/plugin.json",
        plugin_root / "hooks/hooks.json",
        plugin_root / "scripts/project-workflow-claude-hook",
    )
    if any(not path.is_file() for path in required_plugin_files):
        raise ClaudeAdapterError("packaged Claude plugin assets are unavailable")
    environment = os.environ.copy()
    environment["PROJECT_WORKFLOW_CLAUDE_CONTROL"] = str(control_path)
    environment["PROJECT_WORKFLOW_CLAUDE_STATE"] = str(state_path)
    environment["PROJECT_WORKFLOW_CLAUDE_PYTHON"] = sys.executable
    environment["PROJECT_WORKFLOW_CLAUDE_ADAPTER"] = str(Path(__file__).resolve())
    environment["CLAUDE_CONFIG_DIR"] = str(config_dir)
    elapsed_limit = _maximum(control, "elapsed-seconds")
    budget_microdollars = _maximum(control, "agent-budget")
    maximum_turns = _maximum(control, "turns")
    if elapsed_limit <= 0 or budget_microdollars <= 0 or maximum_turns <= 0:
        raise ClaudeAdapterError("Claude elapsed, budget and turn authority must remain positive")
    allowed_tools = ",".join(str(tool) for tool in settings["allowed_tools"])
    native_permission_rules = ",".join(_native_permission_rules(settings, control))
    disallowed_tools = ",".join(str(tool) for tool in settings["disallowed_tools"])
    _run_hook_preflight(
        str(settings["executable"]),
        plugin_root,
        root,
        environment,
        state_path,
        elapsed_limit,
    )
    connection = _connect_state(state_path)
    try:
        _meta_set(connection, "hook_active", "0")
    finally:
        connection.close()
    command = [
        str(settings["executable"]),
        "--print",
        str(settings["prompt"]),
        "--output-format",
        "stream-json",
        "--verbose",
        "--include-hook-events",
        "--model",
        str(settings["model"]),
        "--max-turns",
        str(maximum_turns),
        "--max-budget-usd",
        _microdollars_to_usd(budget_microdollars),
        "--tools",
        allowed_tools,
        "--allowedTools",
        native_permission_rules,
        "--permission-mode",
        "dontAsk",
        "--plugin-dir",
        str(plugin_root),
        "--setting-sources",
        "user",
        "--no-session-persistence",
        "--no-chrome",
        "--strict-mcp-config",
        "--mcp-config",
        '{"mcpServers":{}}',
    ]
    if disallowed_tools:
        command.extend(("--disallowedTools", disallowed_tools))
    start = time.monotonic()
    process = _StreamProcess(command, cwd=root, env=environment)
    terminal_status = "failed"
    terminal_reason = "Claude print mode ended without a terminal result event."
    session_id = ""
    result_event: dict[str, Any] | None = None
    init_observed = False
    try:
        while True:
            if time.monotonic() - start >= elapsed_limit:
                terminal_status = "interrupted"
                terminal_reason = "Claude elapsed authority is exhausted."
                break
            snapshot = _state_snapshot(state_path)
            if snapshot["status"] in CLAUDE_TERMINAL_STATES:
                terminal_status = "interrupted"
                terminal_reason = str(snapshot["reason"] or "Claude hook entered a terminal state.")
                break
            message = process.receive(0.2)
            if message is not None:
                if "_invalid" in message:
                    raise ClaudeAdapterError("Claude print mode emitted malformed stream JSON")
                if "_overflow" in message:
                    raise ClaudeAdapterError("Claude print mode exceeded bounded stream retention")
                message_type = message.get("type")
                subtype = message.get("subtype")
                if message_type == "system" and subtype == "init":
                    init_observed = True
                    session_id = str(message.get("session_id", ""))
                    plugin_errors = message.get("plugin_errors", [])
                    if isinstance(plugin_errors, list) and plugin_errors:
                        raise ClaudeAdapterError(
                            "Claude plugin activation failed or was blocked by managed policy"
                        )
                if message_type == "result":
                    result_event = message
                    session_id = str(message.get("session_id", session_id))
                    if subtype == "success" and message.get("is_error") is not True:
                        terminal_status = "completed"
                        terminal_reason = "Claude turn completed inside sealed authority."
                    elif subtype in {"error_max_turns", "error_max_budget_usd"}:
                        terminal_status = "interrupted"
                        terminal_reason = (
                            "Claude turn authority is exhausted."
                            if subtype == "error_max_turns"
                            else "Claude budget authority is exhausted."
                        )
                    else:
                        terminal_status = "failed"
                        terminal_reason = f"Claude turn ended with {subtype or 'an error'}."
                    break
            if process.poll() is not None and message is None:
                break
    except Exception as exc:
        terminal_status = "failed"
        terminal_reason = str(exc)
    finally:
        process.stop()
    for message in getattr(process, "drain", lambda: [])():
        if message.get("type") == "result" and result_event is None:
            result_event = message
    snapshot = _state_snapshot(state_path)
    if not init_observed:
        terminal_status = "failed"
        terminal_reason = (
            terminal_reason.rstrip() + " Claude stream initialization was not observed."
        )
    if not snapshot["hook_active"]:
        terminal_status = "failed"
        terminal_reason = (
            terminal_reason.rstrip()
            + " Claude SessionStart hook activation was not observed; managed policy or plugin state may block support."
        )
    if snapshot["status"] in CLAUDE_TERMINAL_STATES and terminal_status == "completed":
        terminal_status = "interrupted"
        terminal_reason = str(snapshot["reason"])
    cost_microdollars = 0
    turns = 0
    usage: object = {}
    if result_event is not None:
        try:
            cost_microdollars = _result_microdollars(result_event.get("total_cost_usd", 0))
        except ClaudeAdapterError as exc:
            terminal_status = "failed"
            terminal_reason = str(exc)
        raw_turns = result_event.get("num_turns", 0)
        if not isinstance(raw_turns, int) or isinstance(raw_turns, bool) or raw_turns < 0:
            terminal_status = "failed"
            terminal_reason = "Claude result has invalid num_turns."
        else:
            turns = raw_turns
        usage = result_event.get("usage", {})
        if terminal_status == "completed" and cost_microdollars > budget_microdollars:
            terminal_status = "interrupted"
            terminal_reason = "Claude result exceeded sealed budget authority."
        if terminal_status == "completed" and turns > maximum_turns:
            terminal_status = "interrupted"
            terminal_reason = "Claude result exceeded sealed turn authority."
    final_head = _git_head(root)
    final_changes = sorted(_git_changed_paths(root))
    allowed_paths = control["allowed_write_paths"]
    assert isinstance(allowed_paths, list)
    disallowed = [path for path in final_changes if not _path_allowed(path, allowed_paths, root)]
    required_changes = set(settings["required_changed_paths"])
    required_changes.update(settings["required_output_identities"])
    unsealed_required = sorted(
        path for path in required_changes if not _path_allowed(path, allowed_paths, root)
    )
    missing_required = sorted(required_changes - set(final_changes))
    required_output_identities = settings["required_output_identities"]
    assert isinstance(required_output_identities, dict)
    output_failures: list[str] = []
    for path, expected_identity in required_output_identities.items():
        target = root / str(path)
        if not target.is_file():
            output_failures.append(f"{path} is missing")
            continue
        observed_identity = "sha256:" + hashlib.sha256(target.read_bytes()).hexdigest()
        if observed_identity != expected_identity:
            output_failures.append(f"{path} has the wrong content identity")
    connection = _connect_state(state_path)
    try:
        successful_validations = {
            str(row[0]) for row in connection.execute("SELECT command FROM successful_validations")
        }
    finally:
        connection.close()
    required_validation_commands = set(settings["required_validation_commands"])
    missing_validations = sorted(required_validation_commands - successful_validations)
    closeout_failed = (
        final_head != source_revision
        or disallowed
        or unsealed_required
        or missing_required
        or output_failures
        or missing_validations
        or len(final_changes) > _maximum(control, "changed-paths")
    )
    if closeout_failed:
        if unsealed_required:
            closeout_reason = "Claude required changes exceed sealed write scope: " + ", ".join(
                unsealed_required
            )
        elif missing_required:
            closeout_reason = "Claude required changes are missing: " + ", ".join(missing_required)
        elif output_failures:
            closeout_reason = "Claude required output proof failed: " + ", ".join(output_failures)
        elif missing_validations:
            closeout_reason = "Claude required validators did not pass: " + ", ".join(
                missing_validations
            )
        else:
            closeout_reason = "Claude closeout found source or write-scope drift."
        if terminal_status == "completed":
            terminal_status = "interrupted"
            terminal_reason = closeout_reason
        else:
            terminal_reason = terminal_reason.rstrip() + " Closeout: " + closeout_reason
    elapsed = max(0, int(time.monotonic() - start))
    native_metrics = {
        "elapsed-seconds": elapsed,
        "agent-budget": cost_microdollars,
        "turns": turns,
        "tool-calls": snapshot["tool_calls"],
        "test-invocations": snapshot["test_invocations"],
        "identical-retries": snapshot["identical_retries"],
        "worker-launches": snapshot["worker_launches"],
        "changed-paths": len(final_changes),
        "write-scope": 1 if disallowed else 0,
    }
    result = {
        "adapter_schema_version": CLAUDE_ADAPTER_SCHEMA_VERSION,
        "adapter_kind": CLAUDE_ADAPTER_KIND,
        "host": "claude-code",
        "version": probe["version"],
        "configuration_identity": probe["configuration_identity"],
        "terminal_status": terminal_status,
        "terminal_reason": terminal_reason,
        "session_id": session_id,
        "hook_active": snapshot["hook_active"],
        "native_metrics": native_metrics,
        "native_usage": usage,
        "final_source_revision": final_head,
        "final_changed_paths": final_changes,
        "hook_events": snapshot.get("hook_events", []),
        "protocol_events": getattr(process, "protocol_events", []),
        "stderr_tail": process.stderr[-20:],
    }
    result["evidence_identity"] = _identity(result)
    return result


def run_claude_adapter(root: Path, control: Mapping[str, object]) -> dict[str, object]:
    """Run one adapter journey and always retire its ephemeral authority state."""
    state_dir = Path(tempfile.mkdtemp(prefix="project-workflow-claude-"))
    try:
        return _run_claude_adapter(root, control, state_dir)
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
    raise SystemExit("Claude adapter is subordinate; use `project execute --id <WORK-ID>`.")


if __name__ == "__main__":
    raise SystemExit(main())
