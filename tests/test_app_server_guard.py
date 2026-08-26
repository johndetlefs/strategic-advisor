from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "scripts" / "app_server_guard.py"
FIXTURES = ROOT / "tests" / "fixtures" / "app_server_guard"
FAKE_SERVER = FIXTURES / "fake_app_server.py"
FAKE_REVIEWER = FIXTURES / "fake_reviewer.py"
ORIGINAL = "ORIGINAL_DRAFT_UNCHECKED"
REVISED = "REVISED_DRAFT_QUALIFIED"
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


class AppServerGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary_directory.name)
        self.prompt = self.base / "prompt.txt"
        self.material = self.base / "material.json"
        self.contract = self.base / "contract.txt"
        self.evidence = self.base / "evidence.jsonl"
        self.review_log = self.base / "reviews.jsonl"
        self.wrapper = self.base / "fake-codex"
        self.prompt.write_text(
            "Respond with exactly ORIGINAL_DRAFT_UNCHECKED and no other text.",
            encoding="utf-8",
        )
        self.material.write_text('{"decision":"fixture"}', encoding="utf-8")
        self.contract.write_text("Public synthetic transport fixture.", encoding="utf-8")
        self.wrapper.write_text(
            f"#!/bin/sh\nexec {sys.executable} {FAKE_SERVER} \"$@\"\n",
            encoding="utf-8",
        )
        self.wrapper.chmod(0o700)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_guard(
        self,
        reviewer_mode: str = "pass",
        app_server_mode: str = "success",
    ) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        environment.update(
            {
                "GUARD_REVIEWER_MODE": reviewer_mode,
                "GUARD_APP_SERVER_MODE": app_server_mode,
                "GUARD_REVIEW_LOG": str(self.review_log),
            }
        )
        command = [
            sys.executable,
            str(GUARD),
            "--codex-binary",
            str(self.wrapper),
            "--reviewer-command-json",
            json.dumps([sys.executable, str(FAKE_REVIEWER)]),
            "--prompt-file",
            str(self.prompt),
            "--material-state",
            str(self.material),
            "--gate-contract",
            str(self.contract),
            "--cwd",
            str(ROOT),
            "--review-timeout",
            "0.1",
            "--turn-timeout",
            "2",
            "--evidence",
            str(self.evidence),
        ]
        return subprocess.run(command, text=True, capture_output=True, env=environment, timeout=10)

    def evidence_records(self) -> list[dict]:
        return [json.loads(line) for line in self.evidence.read_text(encoding="utf-8").splitlines()]

    def test_pass_releases_only_reviewed_candidate(self) -> None:
        result = self.run_guard()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, ORIGINAL + "\n")
        records = self.evidence_records()
        self.assertEqual([item["kind"] for item in records].count("answer_delivered"), 1)
        self.assertNotIn(ORIGINAL, self.evidence.read_text(encoding="utf-8"))

    def test_one_revision_releases_only_passing_revision(self) -> None:
        result = self.run_guard("revise_then_pass")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, REVISED + "\n")
        self.assertNotIn(ORIGINAL, result.stdout)
        decisions = [
            item["payload"]["decision"]
            for item in self.evidence_records()
            if item["kind"] == "review_completed"
        ]
        self.assertEqual(decisions, ["revise", "pass"])

    def test_reviewer_receives_only_allowlisted_envelope(self) -> None:
        result = self.run_guard("revise_then_pass")
        self.assertEqual(result.returncode, 0, result.stderr)
        envelopes = [json.loads(line) for line in self.review_log.read_text().splitlines()]
        self.assertEqual(len(envelopes), 2)
        for envelope in envelopes:
            self.assertEqual(set(envelope), ENVELOPE_KEYS)
            self.assertNotIn("evaluation", envelope)
            self.assertNotIn("memory", envelope)
            self.assertNotIn("workflow", envelope)
        self.assertEqual(envelopes[0]["candidate_draft"], ORIGINAL)
        self.assertEqual(envelopes[1]["candidate_draft"], REVISED)

    def test_block_fails_closed_without_draft_disclosure(self) -> None:
        result = self.run_guard("block")
        self.assertEqual(result.returncode, 22)
        self.assertEqual(result.stdout, "")
        self.assertNotIn(ORIGINAL, result.stderr)
        self.assertNotIn(REVISED, result.stderr)

    def test_reviewer_failures_fail_closed(self) -> None:
        for mode, expected_status in (
            ("error", 21),
            ("timeout", 21),
            ("invalid_json", 24),
            ("unknown_field", 24),
        ):
            with self.subTest(mode=mode):
                if self.evidence.exists():
                    self.evidence.unlink()
                result = self.run_guard(mode)
                self.assertEqual(result.returncode, expected_status)
                self.assertEqual(result.stdout, "")
                self.assertNotIn(ORIGINAL, result.stderr)

    def test_second_revision_fails_closed(self) -> None:
        result = self.run_guard("revise_forever")
        self.assertEqual(result.returncode, 23)
        self.assertEqual(result.stdout, "")
        self.assertNotIn(ORIGINAL, result.stderr)
        self.assertNotIn(REVISED, result.stderr)

    def test_app_server_failures_fail_closed(self) -> None:
        for mode in (
            "failed_turn",
            "invalid_json",
            "malformed_item",
            "methodless_event",
            "no_answer",
            "unknown_event",
        ):
            with self.subTest(mode=mode):
                if self.evidence.exists():
                    self.evidence.unlink()
                result = self.run_guard(app_server_mode=mode)
                self.assertEqual(result.returncode, 20)
                self.assertEqual(result.stdout, "")
                self.assertNotIn(ORIGINAL, result.stderr)
                self.assertNotIn(REVISED, result.stderr)

    def test_stale_first_attempt_events_cannot_complete_revision(self) -> None:
        result = self.run_guard("revise_then_pass", "stale_second_turn")
        self.assertEqual(result.returncode, 20)
        self.assertEqual(result.stdout, "")
        self.assertNotIn(ORIGINAL, result.stderr)
        self.assertNotIn(REVISED, result.stderr)


if __name__ == "__main__":
    unittest.main()
