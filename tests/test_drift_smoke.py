from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPOSITORY_ROOT / "scripts" / "drift_smoke.py"
SPEC = REPOSITORY_ROOT / "skills" / "strategic-advisor" / "evals" / "drift_smoke_cases.json"
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))


def load_tool():
    spec = importlib.util.spec_from_file_location("drift_smoke_tool", TOOL)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load drift-smoke tool")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


TOOL_MODULE = load_tool()


class DriftSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary_directory.name)
        self.spec, self.spec_hash = TOOL_MODULE.validate_spec(REPOSITORY_ROOT, SPEC)
        self.result = self.valid_result()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def valid_result(self) -> dict:
        scenarios = []
        next_session = 1
        for case in self.spec["cases"]:
            sessions = []
            planned = TOOL_MODULE.expected_sessions(case)
            for variant_id, turns in planned.items():
                session = {
                    "session_id": f"00000000-0000-4000-8000-{next_session:012d}",
                    "turns": [
                        {
                            "id": turn["id"],
                            "user": turn["user"],
                            "assistant": f"Synthetic assistant response for {case['id']} {variant_id} {turn['id']}.",
                        }
                        for turn in turns
                    ],
                }
                if variant_id != "default":
                    session["variant_id"] = variant_id
                sessions.append(session)
                next_session += 1
            scenarios.append(
                {
                    "case_id": case["id"],
                    "criteria": [
                        {
                            "id": criterion["id"],
                            "status": "pass",
                            "observation": f"Synthetic review observation for {criterion['id']}.",
                        }
                        for criterion in case["criteria"]
                    ],
                    "sessions": sessions,
                    "status": "pass",
                }
            )
        return {
            "authority_commit": "a" * 40,
            "completed_at": "2026-07-24T02:00:00Z",
            "schema_version": 1,
            "scenarios": scenarios,
            "spec_sha256": self.spec_hash,
            "started_at": "2026-07-24T01:00:00Z",
            "status": "pass",
            "suite_id": self.spec["suite_id"],
            "target": {
                "cli_version": "codex-cli fixture",
                "evaluation_material_visible": False,
                "host": "codex-cli",
                "model": "gpt-5.6-sol",
                "runtime_package_identity_sha256": TOOL_MODULE.current_runtime_identity(
                    REPOSITORY_ROOT
                ),
                "source_access": [
                    "SKILL.md",
                    "references/conversational-strategy.md",
                    "references/evidence.md",
                ],
                "source_access_artifact": "source-access.json",
            },
        }

    def write_result(self, value: dict) -> Path:
        source_access = {
            "records": [
                {
                    "session_id": session["session_id"],
                    "successful_runtime_reads": ["SKILL.md"],
                }
                for scenario in value["scenarios"]
                for session in scenario["sessions"]
            ],
            "schema_version": 1,
        }
        source_bytes = json.dumps(source_access).encode("utf-8")
        (self.base / "source-access.json").write_bytes(source_bytes)
        value["target"]["source_access_artifact_sha256"] = TOOL_MODULE.sha256_bytes(
            source_bytes
        )
        path = self.base / "result.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def verify(self, value: dict) -> bool:
        return TOOL_MODULE.validate_result(
            REPOSITORY_ROOT,
            self.spec,
            self.spec_hash,
            self.write_result(value),
        )

    def test_approved_spec_and_complete_result_pass(self) -> None:
        self.assertEqual(len(self.spec["cases"]), 6)
        self.assertTrue(self.verify(self.result))

    def test_missing_actual_turn_fails(self) -> None:
        value = copy.deepcopy(self.result)
        value["scenarios"][1]["sessions"][0]["turns"].pop()
        with self.assertRaisesRegex(TOOL_MODULE.SmokeError, "missing an actual turn"):
            self.verify(value)

    def test_reused_session_fails(self) -> None:
        value = copy.deepcopy(self.result)
        value["scenarios"][1]["sessions"][0]["session_id"] = value["scenarios"][0][
            "sessions"
        ][0]["session_id"]
        with self.assertRaisesRegex(TOOL_MODULE.SmokeError, "session id is reused"):
            self.verify(value)

    def test_runtime_identity_drift_fails(self) -> None:
        value = copy.deepcopy(self.result)
        value["target"]["runtime_package_identity_sha256"] = "0" * 64
        with self.assertRaisesRegex(TOOL_MODULE.SmokeError, "runtime package identity"):
            self.verify(value)

    def test_source_access_artifact_tampering_fails(self) -> None:
        value = copy.deepcopy(self.result)
        result_path = self.write_result(value)
        (self.base / "source-access.json").write_text(
            '{"records":[],"schema_version":1}', encoding="utf-8"
        )
        with self.assertRaisesRegex(TOOL_MODULE.SmokeError, "source-access evidence hash"):
            TOOL_MODULE.validate_result(
                REPOSITORY_ROOT,
                self.spec,
                self.spec_hash,
                result_path,
            )

    def test_missing_review_criterion_fails(self) -> None:
        value = copy.deepcopy(self.result)
        value["scenarios"][2]["criteria"].pop()
        with self.assertRaisesRegex(TOOL_MODULE.SmokeError, "review criteria"):
            self.verify(value)

    def test_forged_pass_over_failed_criterion_fails(self) -> None:
        value = copy.deepcopy(self.result)
        value["scenarios"][3]["criteria"][0]["status"] = "fail"
        with self.assertRaisesRegex(TOOL_MODULE.SmokeError, "status does not match"):
            self.verify(value)

    def test_honest_failed_result_is_retained_as_failure(self) -> None:
        value = copy.deepcopy(self.result)
        value["scenarios"][3]["criteria"][0]["status"] = "fail"
        value["scenarios"][3]["status"] = "fail"
        value["status"] = "fail"
        self.assertFalse(self.verify(value))

    def test_user_turn_drift_fails(self) -> None:
        value = copy.deepcopy(self.result)
        value["scenarios"][4]["sessions"][0]["turns"][1]["user"] += " changed"
        with self.assertRaisesRegex(TOOL_MODULE.SmokeError, "user bytes drift"):
            self.verify(value)


if __name__ == "__main__":
    unittest.main()
