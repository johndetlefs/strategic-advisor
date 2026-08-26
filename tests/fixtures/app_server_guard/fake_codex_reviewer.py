#!/usr/bin/env python3
"""Fake `codex exec` used to inspect model_delta_reviewer isolation."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def main() -> int:
    args = sys.argv[1:]
    prompt = sys.stdin.read()
    log = os.environ.get("DELTA_FAKE_CODEX_LOG")
    if log:
        Path(log).write_text(json.dumps({"args": args, "prompt": prompt}), encoding="utf-8")
    if os.environ.get("DELTA_FAKE_CODEX_MODE") == "error":
        return 2
    output_flag = args.index("--output-last-message")
    output = Path(args[output_flag + 1])
    mode = os.environ.get("DELTA_FAKE_CODEX_MODE", "pass")
    if mode == "invalid_json":
        output.write_text("not-json", encoding="utf-8")
        return 0
    if mode == "revise":
        result = {
            "decision": "revise",
            "reason_codes": ["unsupported_replacement"],
            "revision_instruction": "Preserve the prior qualified recommendation and label the replacement as a validation candidate.",
            "schema_version": 1,
        }
    else:
        result = {
            "decision": "pass",
            "reason_codes": ["supported_delta"],
            "revision_instruction": None,
            "schema_version": 1,
        }
    output.write_text(json.dumps(result), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
