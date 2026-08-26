#!/usr/bin/env python3
"""Deterministic JSONL app-server fixture for app_server_guard tests."""

from __future__ import annotations

import json
import os
import sys


def emit(value: object) -> None:
    print(json.dumps(value), flush=True)


def main() -> int:
    mode = os.environ.get("GUARD_APP_SERVER_MODE", "success")
    turn_count = 0
    for line in sys.stdin:
        message = json.loads(line)
        method = message.get("method")
        request_id = message.get("id")
        if method == "initialize":
            emit({"id": request_id, "result": {"userAgent": "fake-app-server/1"}})
        elif method == "initialized":
            continue
        elif method == "thread/start":
            emit({"id": request_id, "result": {"thread": {"id": "fixture-thread"}}})
        elif method == "turn/start":
            turn_count += 1
            turn_id = f"turn-{turn_count}"
            item_id = f"item-{turn_count}"
            emit({"id": request_id, "result": {"turn": {"id": turn_id}}})
            if mode == "methodless_event":
                emit({"params": {}})
                continue
            if mode == "unknown_event":
                emit({"method": "future/unchecked", "params": {}})
                continue
            if mode == "invalid_json":
                print("not-json", flush=True)
                continue
            if mode == "failed_turn":
                emit(
                    {
                        "method": "turn/completed",
                        "params": {
                            "threadId": "fixture-thread",
                            "turn": {"id": turn_id, "status": "failed"},
                        },
                    }
                )
                continue
            emit(
                {
                    "method": "turn/started",
                    "params": {
                        "threadId": "fixture-thread",
                        "turn": {"id": turn_id, "status": "inProgress"},
                    },
                }
            )
            if mode == "stale_second_turn" and turn_count == 2:
                stale_item = {
                    "id": "item-1",
                    "type": "agentMessage",
                    "text": "ORIGINAL_DRAFT_UNCHECKED",
                }
                emit(
                    {
                        "method": "item/completed",
                        "params": {
                            "completedAtMs": 1,
                            "item": stale_item,
                            "threadId": "fixture-thread",
                            "turnId": "turn-1",
                        },
                    }
                )
                emit(
                    {
                        "method": "turn/completed",
                        "params": {
                            "threadId": "fixture-thread",
                            "turn": {
                                "id": "turn-1",
                                "status": "completed",
                                "items": [stale_item],
                            },
                        },
                    }
                )
                continue
            candidate = (
                "ORIGINAL_DRAFT_UNCHECKED"
                if turn_count == 1
                else "REVISED_DRAFT_QUALIFIED"
            )
            emit(
                {
                    "method": "item/started",
                    "params": {
                        "item": {"id": item_id, "type": "agentMessage"},
                        "startedAtMs": 1,
                        "threadId": "fixture-thread",
                        "turnId": turn_id,
                    },
                }
            )
            for delta in (candidate[:8], candidate[8:]):
                emit(
                    {
                        "method": "item/agentMessage/delta",
                        "params": {
                            "itemId": item_id,
                            "delta": delta,
                            "threadId": "fixture-thread",
                            "turnId": turn_id,
                        },
                    }
                )
            if mode != "no_answer":
                item = {
                    "id": item_id,
                    "type": "agentMessage",
                    "text": candidate,
                }
                completed_item = item if mode != "malformed_item" else {"type": "agentMessage"}
                emit(
                    {
                        "method": "item/completed",
                        "params": {
                            "completedAtMs": 1,
                            "item": completed_item,
                            "threadId": "fixture-thread",
                            "turnId": turn_id,
                        },
                    }
                )
                items = [item]
            else:
                items = []
            emit(
                {
                    "method": "turn/completed",
                    "params": {
                        "threadId": "fixture-thread",
                        "turn": {
                            "id": turn_id,
                            "status": "completed",
                            "items": items,
                        }
                    },
                }
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
