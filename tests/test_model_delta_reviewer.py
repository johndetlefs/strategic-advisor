from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEWER = ROOT / "scripts" / "model_delta_reviewer.py"
FAKE_CODEX = ROOT / "tests" / "fixtures" / "app_server_guard" / "fake_codex_reviewer.py"
KEYS = {
    "attempt",
    "candidate_draft",
    "controller_sha256",
    "current_user_turn",
    "gate_contract",
    "gate_contract_sha256",
    "material_state",
    "schema_version",
}


def envelope() -> dict:
    contract = "Public synthetic recommendation delta contract."
    return {
        "attempt": 1,
        "candidate_draft": "Adopt the replacement now.",
        "controller_sha256": "a" * 64,
        "current_user_turn": "The first bridge failed; use my replacement.",
        "gate_contract": contract,
        "gate_contract_sha256": hashlib.sha256(contract.encode()).hexdigest(),
        "material_state": json.dumps({"public_synthetic": True}),
        "schema_version": 1,
    }


class ModelDeltaReviewerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.log = Path(self.directory.name) / "codex-log.json"

    def tearDown(self) -> None:
        self.directory.cleanup()

    def run_reviewer(self, value: dict, mode: str = "pass") -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        environment.update(
            {
                "DELTA_REVIEW_CODEX_BINARY": str(FAKE_CODEX),
                "DELTA_FAKE_CODEX_LOG": str(self.log),
                "DELTA_FAKE_CODEX_MODE": mode,
            }
        )
        return subprocess.run(
            [sys.executable, str(REVIEWER)],
            input=json.dumps(value),
            text=True,
            capture_output=True,
            env=environment,
            timeout=5,
        )

    def test_isolated_command_and_allowlisted_prompt(self) -> None:
        result = self.run_reviewer(envelope())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["decision"], "pass")
        observed = json.loads(self.log.read_text())
        args = observed["args"]
        for flag in ("--ignore-user-config", "--ignore-rules", "--ephemeral", "--skip-git-repo-check"):
            self.assertIn(flag, args)
        self.assertEqual(args[args.index("--sandbox") + 1], "read-only")
        prompt = observed["prompt"]
        for key in KEYS:
            self.assertIn(key, prompt)
        for forbidden in ("evaluation criteria", "expected_answers", ".project-workflow", "memory"):
            self.assertNotIn(forbidden, prompt)

    def test_revision_is_normalized_for_guard(self) -> None:
        result = self.run_reviewer(envelope(), "revise")
        self.assertEqual(result.returncode, 0, result.stderr)
        verdict = json.loads(result.stdout)
        self.assertEqual(set(verdict), {"decision", "reason_codes", "revision_instruction", "schema_version"})
        self.assertEqual(verdict["decision"], "revise")

    def test_extra_or_mismatched_envelope_fails_closed(self) -> None:
        values = []
        extra = envelope()
        extra["evaluation"] = "hidden"
        values.append(extra)
        mismatch = envelope()
        mismatch["gate_contract_sha256"] = "0" * 64
        values.append(mismatch)
        for value in values:
            with self.subTest(keys=set(value)):
                result = self.run_reviewer(value)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")

    def test_process_error_and_invalid_json_fail_closed(self) -> None:
        for mode in ("error", "invalid_json"):
            with self.subTest(mode=mode):
                result = self.run_reviewer(envelope(), mode)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
