#!/usr/bin/env python3
"""Capture exact app-server and hook event ordering for TASK-031."""

from __future__ import annotations

import json
import os
import selectors
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path("/private/tmp/sa-fix006-causal-bridge")
BINARY = Path("/Applications/ChatGPT.app/Contents/Resources/codex")
RAW_PATH = Path(__file__).with_name("app-server-events.jsonl")
PROMPT = "Respond with exactly ORIGINAL_DRAFT_UNCHECKED and no other text."


def write_record(kind: str, payload: object) -> None:
    record = {
        "seq": write_record.seq,
        "recorded_at_ns": time.time_ns(),
        "kind": kind,
        "payload": payload,
    }
    write_record.seq += 1
    with RAW_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


write_record.seq = 1


def send(process: subprocess.Popen[str], message: dict[str, object]) -> None:
    write_record("client_send", message)
    assert process.stdin is not None
    process.stdin.write(json.dumps(message) + "\n")
    process.stdin.flush()


def main() -> int:
    if RAW_PATH.exists():
        RAW_PATH.unlink()
    command = [
        str(BINARY),
        "-c",
        (
            'hooks.Stop=[{hooks=[{type="command",command="/usr/bin/python3 '
            '/private/tmp/sa-fix006-causal-bridge/evidence/evaluations/'
            'host-feasibility/task-031/probe/stop_hook_probe.py",timeout=30}]}]'
        ),
        "--dangerously-bypass-hook-trust",
        "app-server",
        "--stdio",
    ]
    environment = dict(os.environ)
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        env=environment,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    assert process.stdout is not None
    assert process.stderr is not None

    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, "stdout")
    selector.register(process.stderr, selectors.EVENT_READ, "stderr")

    send(
        process,
        {
            "method": "initialize",
            "id": 0,
            "params": {
                "clientInfo": {
                    "name": "sa_task_031_probe",
                    "title": "SA TASK-031 Probe",
                    "version": "0.1.0",
                }
            },
        },
    )

    thread_started = False
    deadline = time.monotonic() + 120
    try:
        while time.monotonic() < deadline:
            ready = selector.select(timeout=1)
            if not ready:
                if process.poll() is not None:
                    break
                continue
            for key, _ in ready:
                line = key.fileobj.readline()
                if not line:
                    continue
                line = line.rstrip("\n")
                if key.data == "stderr":
                    write_record("server_stderr", line)
                    continue
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    write_record("server_stdout_non_json", line)
                    continue
                write_record("server_message", message)

                if message.get("id") == 0 and "result" in message:
                    send(process, {"method": "initialized", "params": {}})
                    send(
                        process,
                        {
                            "method": "hooks/list",
                            "id": 10,
                            "params": {"cwds": [str(ROOT)]},
                        },
                    )
                elif message.get("id") == 10 and "result" in message:
                    send(
                        process,
                        {
                            "method": "thread/start",
                            "id": 1,
                            "params": {
                                "model": "gpt-5.6-luna",
                                "cwd": str(ROOT),
                                "ephemeral": True,
                            },
                        },
                    )
                elif message.get("id") == 1 and message.get("result", {}).get("thread", {}).get("id"):
                    thread_id = message["result"]["thread"]["id"]
                    send(
                        process,
                        {
                            "method": "turn/start",
                            "id": 2,
                            "params": {
                                "threadId": thread_id,
                                "input": [{"type": "text", "text": PROMPT}],
                            },
                        },
                    )
                    thread_started = True
                elif (
                    thread_started
                    and message.get("method") == "turn/completed"
                ):
                    return 0
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        write_record("process_exit", process.returncode)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
