#!/usr/bin/env python3
"""Retain only public-synthetic TASK-031 event fields."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent


def dump(path: Path, records: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def sanitize_app_server() -> None:
    records: list[dict[str, object]] = []
    source = ROOT / "app-server-events.jsonl"
    for line in source.read_text(encoding="utf-8").splitlines():
        raw = json.loads(line)
        payload = raw["payload"]
        if raw["kind"] == "client_send":
            method = payload.get("method")
            if method in {"initialize", "initialized", "hooks/list", "thread/start", "turn/start"}:
                sanitized = {"method": method, "id": payload.get("id")}
                if method == "turn/start":
                    sanitized["prompt"] = payload["params"]["input"][0]["text"]
                records.append({"seq": raw["seq"], "kind": "client_send", "payload": sanitized})
            continue
        if raw["kind"] != "server_message" or not isinstance(payload, dict):
            continue
        if payload.get("id") == 0 and "result" in payload:
            records.append(
                {
                    "seq": raw["seq"],
                    "kind": "server_identity",
                    "payload": {"userAgent": payload["result"].get("userAgent")},
                }
            )
            continue
        if payload.get("id") == 10 and "result" in payload:
            hooks = []
            for group in payload["result"].get("data", []):
                for hook in group.get("hooks", []):
                    hooks.append(
                        {
                            key: hook.get(key)
                            for key in (
                                "currentHash",
                                "enabled",
                                "eventName",
                                "executionMode",
                                "handlerType",
                                "source",
                                "trustStatus",
                            )
                        }
                    )
            records.append(
                {"seq": raw["seq"], "kind": "hooks_list", "payload": hooks}
            )
            continue
        method = payload.get("method")
        params = payload.get("params", {})
        if method == "item/started" and params.get("item", {}).get("type") == "agentMessage":
            records.append(
                {
                    "seq": raw["seq"],
                    "kind": method,
                    "payload": {
                        "itemId": params["item"].get("id"),
                        "phase": params["item"].get("phase"),
                        "text": params["item"].get("text"),
                    },
                }
            )
        elif method == "item/agentMessage/delta":
            records.append(
                {
                    "seq": raw["seq"],
                    "kind": method,
                    "payload": {
                        "itemId": params.get("itemId"),
                        "delta": params.get("delta"),
                    },
                }
            )
        elif method == "item/completed" and params.get("item", {}).get("type") == "agentMessage":
            records.append(
                {
                    "seq": raw["seq"],
                    "kind": method,
                    "payload": {
                        "itemId": params["item"].get("id"),
                        "phase": params["item"].get("phase"),
                        "text": params["item"].get("text"),
                    },
                }
            )
        elif method in {"hook/started", "hook/completed", "turn/completed"}:
            records.append({"seq": raw["seq"], "kind": method, "payload": params})
    dump(ROOT / "app-server-relevant-events.jsonl", records)


def sanitize_cli() -> None:
    for source in sorted(ROOT.glob("cli-*-events.jsonl")):
        records: list[dict[str, object]] = []
        for line in source.read_text(encoding="utf-8").splitlines():
            raw = json.loads(line)
            payload = raw["payload"]
            if raw["kind"] == "process_start":
                records.append(
                    {
                        "seq": raw["seq"],
                        "recorded_at_ns": raw["recorded_at_ns"],
                        "kind": "process_start",
                        "payload": {
                            "case": payload["case"],
                            "hook_timeout_seconds": payload["hook_timeout_seconds"],
                            "prompt": payload["prompt"],
                        },
                    }
                )
            elif raw["kind"] == "stdout" and isinstance(payload, dict):
                event_type = payload.get("type")
                item = payload.get("item", {})
                if event_type == "turn.completed" or item.get("type") == "agent_message":
                    records.append(raw)
            elif raw["kind"] == "process_exit":
                records.append(raw)
        target = ROOT / source.name.replace("-events.jsonl", "-relevant-events.jsonl")
        dump(target, records)


def sanitize_hook_log() -> None:
    records = []
    source = ROOT / "hook-events.jsonl"
    for line in source.read_text(encoding="utf-8").splitlines():
        raw = json.loads(line)
        event = raw["event"]
        records.append(
            {
                "recorded_at_ns": raw["recorded_at_ns"],
                "event": {
                    key: event.get(key)
                    for key in (
                        "hook_event_name",
                        "last_assistant_message",
                        "model",
                        "session_id",
                        "stop_hook_active",
                        "turn_id",
                    )
                },
            }
        )
    dump(ROOT / "hook-relevant-events.jsonl", records)


if __name__ == "__main__":
    sanitize_app_server()
    sanitize_cli()
    sanitize_hook_log()
