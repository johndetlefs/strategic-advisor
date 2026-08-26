#!/usr/bin/env python3
"""Retain CLI Stop-hook success, error, and timeout event ordering."""

from __future__ import annotations

import json
import selectors
import subprocess
import time
from pathlib import Path


ROOT = Path("/private/tmp/sa-fix006-causal-bridge")
BINARY = Path("/Users/johndetlefs/.local/bin/codex")
PROBE = ROOT / "evidence/evaluations/host-feasibility/task-031/probe/stop_hook_probe.py"
PROMPT = "Respond with exactly ORIGINAL_DRAFT_UNCHECKED and no other text."


def run_case(name: str, hook_command: str, timeout: int) -> int:
    raw_path = Path(__file__).with_name(f"cli-{name}-events.jsonl")
    if raw_path.exists():
        raw_path.unlink()
    hook_value = (
        "hooks.Stop=[{hooks=[{type=\"command\",command="
        + json.dumps(hook_command)
        + f",timeout={timeout}" + "}]}]"
    )
    command = [
        str(BINARY),
        "-c",
        hook_value,
        "--ask-for-approval",
        "never",
        "exec",
        "--json",
        "--ephemeral",
        "--ignore-user-config",
        "--dangerously-bypass-hook-trust",
        "--sandbox",
        "read-only",
        "--model",
        "gpt-5.6-luna",
        PROMPT,
    ]
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
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
    seq = 1
    with raw_path.open("a", encoding="utf-8") as output:
        output.write(
            json.dumps(
                {
                    "seq": seq,
                    "recorded_at_ns": time.time_ns(),
                    "kind": "process_start",
                    "payload": {
                        "binary": str(BINARY),
                        "case": name,
                        "hook_command": hook_command,
                        "hook_timeout_seconds": timeout,
                        "prompt": PROMPT,
                    },
                },
                sort_keys=True,
            )
            + "\n"
        )
        seq += 1
        while selector.get_map():
            for key, _ in selector.select(timeout=1):
                line = key.fileobj.readline()
                if not line:
                    selector.unregister(key.fileobj)
                    continue
                line = line.rstrip("\n")
                payload: object = line
                if key.data == "stdout":
                    try:
                        payload = json.loads(line)
                    except json.JSONDecodeError:
                        pass
                output.write(
                    json.dumps(
                        {
                            "seq": seq,
                            "recorded_at_ns": time.time_ns(),
                            "kind": key.data,
                            "payload": payload,
                        },
                        sort_keys=True,
                    )
                    + "\n"
                )
                output.flush()
                seq += 1
        return_code = process.wait(timeout=10)
        output.write(
            json.dumps(
                {
                    "seq": seq,
                    "recorded_at_ns": time.time_ns(),
                    "kind": "process_exit",
                    "payload": return_code,
                },
                sort_keys=True,
            )
            + "\n"
        )
    return return_code


def main() -> int:
    cases = [
        ("success", f"/usr/bin/python3 {PROBE}", 30),
        ("error", "/usr/bin/false", 30),
        ("timeout", "/bin/sleep 5", 1),
    ]
    return max(run_case(*case) for case in cases)


if __name__ == "__main__":
    raise SystemExit(main())
