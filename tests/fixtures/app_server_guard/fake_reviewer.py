#!/usr/bin/env python3
"""Separate deterministic reviewer fixture for app_server_guard tests."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path


def main() -> int:
    envelope = json.load(sys.stdin)
    log_path = os.environ.get("GUARD_REVIEW_LOG")
    if log_path:
        with Path(log_path).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(envelope, sort_keys=True) + "\n")
    mode = os.environ.get("GUARD_REVIEWER_MODE", "pass")
    if mode == "error":
        return 2
    if mode == "timeout":
        time.sleep(2)
    if mode == "invalid_json":
        print("not-json")
        return 0
    if mode == "block":
        result = {"schema_version": 1, "decision": "block", "reason_codes": ["fixture_block"]}
    elif mode == "unknown_field":
        result = {
            "schema_version": 1,
            "decision": "pass",
            "reason_codes": ["fixture_pass"],
            "unexpected": True,
        }
    elif mode == "revise_forever" or (
        mode == "revise_then_pass" and envelope["attempt"] == 1
    ):
        result = {
            "schema_version": 1,
            "decision": "revise",
            "reason_codes": ["fixture_revision"],
            "revision_instruction": "Replace the answer with exactly REVISED_DRAFT_QUALIFIED.",
        }
    else:
        result = {"schema_version": 1, "decision": "pass", "reason_codes": ["fixture_pass"]}
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
