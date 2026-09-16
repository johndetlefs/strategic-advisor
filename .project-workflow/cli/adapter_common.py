# project-workflow:generated
"""Shared dependency-free primitives for Project Workflow host adapters."""

from __future__ import annotations

import fnmatch
import hashlib
import json
import re
import sqlite3
from collections.abc import Iterable, Mapping
from pathlib import Path, PurePosixPath


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def _identity(value: object) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(value)).hexdigest()


def _connect_state(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=4.0, isolation_level=None)
    connection.execute("PRAGMA busy_timeout = 4000")
    connection.execute(
        "CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
    )
    connection.execute(
        "CREATE TABLE IF NOT EXISTS test_inputs "
        "(digest TEXT PRIMARY KEY, attempts INTEGER NOT NULL)"
    )
    connection.execute("CREATE TABLE IF NOT EXISTS changed_paths (path TEXT PRIMARY KEY)")
    connection.execute(
        "CREATE TABLE IF NOT EXISTS hook_events "
        "(sequence INTEGER PRIMARY KEY AUTOINCREMENT, event_name TEXT NOT NULL, "
        "event_cwd TEXT NOT NULL, tool_name TEXT NOT NULL, input_identity TEXT NOT NULL, "
        "decision TEXT NOT NULL, detail TEXT NOT NULL)"
    )
    return connection


def _meta_get(connection: sqlite3.Connection, key: str, default: str = "") -> str:
    row = connection.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return str(row[0]) if row else default


def _meta_set(connection: sqlite3.Connection, key: str, value: object) -> None:
    connection.execute(
        "INSERT INTO meta(key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (key, str(value)),
    )


def _counter(connection: sqlite3.Connection, key: str) -> int:
    return int(_meta_get(connection, key, "0"))


def _record_hook_event(
    state_path: Path,
    event: Mapping[str, object],
    *,
    decision: str,
    detail: str = "",
) -> None:
    tool_input = event.get("tool_input")
    connection = _connect_state(state_path)
    try:
        connection.execute(
            "INSERT INTO hook_events(event_name, event_cwd, tool_name, input_identity, "
            "decision, detail) VALUES (?, ?, ?, ?, ?, ?)",
            (
                str(event.get("hook_event_name", "")),
                str(event.get("cwd", "")),
                str(event.get("tool_name", "")),
                _identity(tool_input) if isinstance(tool_input, dict) else "",
                decision,
                detail,
            ),
        )
    finally:
        connection.close()


def _set_terminal(connection: sqlite3.Connection, status: str, reason: str) -> None:
    if _meta_get(connection, "status", "running") not in {"blocked", "failed"}:
        _meta_set(connection, "status", status)
        _meta_set(connection, "reason", reason)


def _normalized_relative_path(path: str, root: Path | None = None) -> str:
    candidate = path.replace("\\", "/")
    parsed = PurePosixPath(candidate)
    if not candidate or re.match(r"^[A-Za-z]:", candidate):
        raise ValueError(f"path is not workspace-relative: {path}")
    if root is None:
        if parsed.is_absolute() or any(part in {"", ".", ".."} for part in parsed.parts):
            raise ValueError(f"path is not workspace-relative: {path}")
        return str(parsed)
    resolved_root = root.resolve()
    target = Path(candidate)
    resolved_target = (
        target.resolve() if target.is_absolute() else (resolved_root / target).resolve()
    )
    try:
        return resolved_target.relative_to(resolved_root).as_posix()
    except ValueError as exc:
        raise ValueError(f"path is outside the workspace: {path}") from exc


def _path_allowed(path: str, patterns: Iterable[str], root: Path | None = None) -> bool:
    try:
        candidate = _normalized_relative_path(path, root)
    except ValueError:
        return False
    if _is_workflow_coordination_path(candidate):
        return False
    return any(fnmatch.fnmatchcase(candidate, pattern) for pattern in patterns)


def _is_workflow_coordination_path(path: str) -> bool:
    """Return whether Git state belongs to Coordinator control rather than product source."""
    parsed = PurePosixPath(path.replace("\\", "/"))
    return (
        len(parsed.parts) >= 4
        and parsed.parts[:2] == (".project-workflow", "tasks")
        and parsed.name == "COORDINATION.json"
    )


def _state_snapshot(path: Path) -> dict[str, object]:
    connection = _connect_state(path)
    try:
        meta = {
            str(key): str(value) for key, value in connection.execute("SELECT key, value FROM meta")
        }
        changed = [
            str(row[0])
            for row in connection.execute("SELECT path FROM changed_paths ORDER BY path")
        ]
        identical_retries = sum(
            max(0, int(attempts) - 1)
            for _, attempts in connection.execute("SELECT digest, attempts FROM test_inputs")
        )
        hook_events = [
            {
                "sequence": int(sequence),
                "event_name": str(event_name),
                "cwd": str(event_cwd),
                "tool_name": str(tool_name),
                "input_identity": str(input_identity),
                "decision": str(decision),
                "detail": str(detail),
            }
            for (
                sequence,
                event_name,
                event_cwd,
                tool_name,
                input_identity,
                decision,
                detail,
            ) in connection.execute(
                "SELECT sequence, event_name, event_cwd, tool_name, input_identity, decision, "
                "detail FROM hook_events ORDER BY sequence"
            )
        ]
    finally:
        connection.close()
    return {
        "status": meta.get("status", "unknown"),
        "reason": meta.get("reason", ""),
        "hook_active": meta.get("hook_active") == "1",
        "tool_calls": int(meta.get("tool-calls", "0")),
        "test_invocations": int(meta.get("test-invocations", "0")),
        "worker_launches": int(meta.get("worker-launches", "0")),
        "changed_paths": changed,
        "identical_retries": identical_retries,
        "hook_events": hook_events,
    }
