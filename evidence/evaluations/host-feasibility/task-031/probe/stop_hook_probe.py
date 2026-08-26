#!/usr/bin/env python3
"""Public-synthetic Stop-hook probe for TASK-031.

The probe records only the hook event supplied by Codex and requests exactly
one bounded continuation. It deliberately contains no evaluation answer or
private case material.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path


LOG_PATH = Path(__file__).with_name("hook-events.jsonl")


def main() -> int:
    event = json.load(sys.stdin)
    record = {
        "recorded_at_ns": time.time_ns(),
        "event": event,
    }
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")

    if not event.get("stop_hook_active", False):
        print(
            json.dumps(
                {
                    "decision": "block",
                    "reason": (
                        "The draft failed the public-synthetic review. Replace it "
                        "with exactly REVISED_DRAFT_QUALIFIED and no other text."
                    ),
                }
            )
        )
    else:
        print(json.dumps({"continue": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
