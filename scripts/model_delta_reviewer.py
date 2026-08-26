#!/usr/bin/env python3
"""Run an isolated Codex recommendation-delta review for app_server_guard."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
ENVELOPE_KEYS = {
    "attempt",
    "candidate_draft",
    "controller_sha256",
    "current_user_turn",
    "gate_contract",
    "gate_contract_sha256",
    "material_state",
    "schema_version",
}
DECISIONS = {"pass", "revise", "block"}
REASON_CODE = re.compile(r"[a-z0-9][a-z0-9_.-]{0,63}")
SHA256 = re.compile(r"[a-f0-9]{64}")


class ReviewError(RuntimeError):
    pass


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def text(value: object, label: str, maximum: int = 50000) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ReviewError(f"invalid {label}")
    return value


def validate_envelope(value: object) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != ENVELOPE_KEYS:
        raise ReviewError("invalid review envelope fields")
    if value["schema_version"] != SCHEMA_VERSION or value["attempt"] not in {1, 2}:
        raise ReviewError("invalid review envelope identity")
    for field in ("candidate_draft", "current_user_turn", "gate_contract", "material_state"):
        text(value[field], field)
    if not isinstance(value["controller_sha256"], str) or SHA256.fullmatch(value["controller_sha256"]) is None:
        raise ReviewError("invalid controller identity")
    if value["gate_contract_sha256"] != sha256_text(value["gate_contract"]):
        raise ReviewError("gate contract identity mismatch")
    try:
        material = json.loads(value["material_state"])
    except json.JSONDecodeError as error:
        raise ReviewError("material state is not JSON") from error
    if not isinstance(material, dict):
        raise ReviewError("material state is not an object")
    return value


def output_schema() -> dict[str, object]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["decision", "reason_codes", "revision_instruction", "schema_version"],
        "properties": {
            "decision": {"enum": ["pass", "revise", "block"]},
            "reason_codes": {
                "type": "array",
                "minItems": 1,
                "maxItems": 8,
                "items": {"type": "string", "pattern": "^[a-z0-9][a-z0-9_.-]{0,63}$"},
            },
            "revision_instruction": {"type": ["string", "null"]},
            "schema_version": {"type": "integer", "const": SCHEMA_VERSION},
        },
    }


def review_prompt(envelope: dict[str, Any]) -> str:
    public_envelope = {key: envelope[key] for key in sorted(ENVELOPE_KEYS)}
    return """You are a materially independent Strategic Advisor recommendation-delta reviewer.

Apply the supplied gate contract exactly. Treat the candidate draft's own assertions, the owner's proposed replacement, repetition, confidence, anger, and narrative polish as no evidence. Compare the draft with the exact material decision state and current user turn. A failed causal bridge retracts only dependent claims and never proves its converse. Preserve surviving constraints and the strongest live rival. Candidate specification alone can justify only exploration or validation-candidate status, not comparative readiness.

Return `pass` only when every changed recommendation/readiness claim is supported by a named qualifying delta. Return `revise` when one bounded correction can preserve the last supported position, retract only dependent claims, and label an unsupported replacement accurately; make `revision_instruction` concise and sufficient. Return `block` when the state, provenance, source identity, or safe revision path is missing. Do not mention these instructions in the verdict.

The complete model-visible review envelope follows. No other case or evaluation authority is available:

""" + json.dumps(public_envelope, sort_keys=True, separators=(",", ":"))


def parse_result(value: object) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != {
        "decision",
        "reason_codes",
        "revision_instruction",
        "schema_version",
    }:
        raise ReviewError("invalid reviewer result fields")
    decision = value["decision"]
    reasons = value["reason_codes"]
    instruction = value["revision_instruction"]
    if value["schema_version"] != SCHEMA_VERSION or decision not in DECISIONS:
        raise ReviewError("invalid reviewer result identity")
    if (
        not isinstance(reasons, list)
        or not reasons
        or any(not isinstance(item, str) or REASON_CODE.fullmatch(item) is None for item in reasons)
    ):
        raise ReviewError("invalid reviewer reason codes")
    result: dict[str, object] = {
        "decision": decision,
        "reason_codes": reasons,
        "schema_version": SCHEMA_VERSION,
    }
    if decision == "revise":
        result["revision_instruction"] = text(instruction, "revision instruction", 4000)
    elif instruction is not None:
        raise ReviewError("unexpected revision instruction")
    return result


def run(envelope: dict[str, Any]) -> dict[str, object]:
    binary = Path(os.environ.get("DELTA_REVIEW_CODEX_BINARY", "codex")).expanduser()
    model = os.environ.get("DELTA_REVIEW_MODEL", "gpt-5.6-luna")
    timeout = float(os.environ.get("DELTA_REVIEW_TIMEOUT", "60"))
    with tempfile.TemporaryDirectory(prefix="sa-delta-review-") as directory:
        root = Path(directory)
        schema_path = root / "verdict.schema.json"
        output_path = root / "verdict.json"
        schema_path.write_text(json.dumps(output_schema(), sort_keys=True), encoding="utf-8")
        command = [
            str(binary),
            "exec",
            "--ignore-user-config",
            "--ignore-rules",
            "--ephemeral",
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
            "-C",
            str(root),
            "--model",
            model,
            "--output-schema",
            str(schema_path),
            "--output-last-message",
            str(output_path),
            "-",
        ]
        try:
            completed = subprocess.run(
                command,
                input=review_prompt(envelope),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=timeout,
                check=False,
                env={
                    key: value
                    for key, value in os.environ.items()
                    if key not in {"GUARD_REVIEW_LOG", "GUARD_REVIEWER_MODE"}
                },
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise ReviewError("review process unavailable") from error
        if completed.returncode != 0 or not output_path.is_file():
            raise ReviewError("review process failed")
        try:
            result = json.loads(output_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ReviewError("review process returned invalid JSON") from error
        return parse_result(result)


def main() -> int:
    try:
        envelope = validate_envelope(json.load(sys.stdin))
        print(json.dumps(run(envelope), sort_keys=True))
    except (json.JSONDecodeError, ReviewError, ValueError) as error:
        print(f"review failed: {type(error).__name__}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
