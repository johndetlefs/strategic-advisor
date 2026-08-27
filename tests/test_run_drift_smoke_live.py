from __future__ import annotations

import argparse
import contextlib
import io
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = REPOSITORY_ROOT / "scripts" / "run_drift_smoke_live.py"
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))


def load_runner():
    spec = importlib.util.spec_from_file_location("run_drift_smoke_live", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load live drift-smoke runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RUNNER = load_runner()


class LiveDriftSmokeControlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.codex = self.root / "codex"
        self.codex.write_text("fixture", encoding="utf-8")
        self.spec_path = self.root / "spec.json"
        self.spec = {
            "schema_version": 1,
            "suite_id": "fixture-suite",
            "execution_contract": {"host": "fixture-host", "model": "fixture-model"},
            "cases": [
                self.case("CASE-001", "risk-a", 1),
                self.case("CASE-002", "risk-b", 2),
                self.case("CASE-003", "risk-b", 1),
            ],
        }
        self.spec_path.write_text(json.dumps(self.spec), encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    @staticmethod
    def case(case_id: str, risk: str, turn_count: int) -> dict:
        return {
            "id": case_id,
            "risk": risk,
            "title": f"Fixture {case_id}",
            "criteria": [{"id": f"{case_id}-AC", "requirement": "Pass fixture."}],
            "turns": [
                {"id": f"T{index}", "user": f"{case_id} prompt {index}"}
                for index in range(1, turn_count + 1)
            ],
        }

    def selection_args(self, **overrides: object) -> argparse.Namespace:
        values = {
            "case": None,
            "affected_case": None,
            "metadata": None,
            "previously_failing": None,
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def common_args(self, output: str) -> list[str]:
        return [
            "--source-root",
            str(self.root),
            "--spec",
            self.spec_path.name,
            "--output-dir",
            output,
            "--codex-binary",
            str(self.codex),
            "--model",
            "fixture-model",
            "--adjudicator-model",
            "fixture-evaluator-1",
            "--timeout",
            "10",
            "--max-elapsed-seconds",
            "100",
        ]

    @staticmethod
    def fake_build(
        _source_root: Path,
        _manifest: str,
        package_root: Path,
        manifest_path: Path,
    ) -> None:
        package_root.mkdir(parents=True, exist_ok=True)
        package_root.joinpath("SKILL.md").write_text("fixture", encoding="utf-8")
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(
                {
                    "package_identity_sha256": "runtime-identity-1",
                    "files": [{"path": "SKILL.md"}],
                }
            ),
            encoding="utf-8",
        )

    @staticmethod
    def fake_subprocess(
        arguments: list[str], **_kwargs: object
    ) -> subprocess.CompletedProcess:
        stdout = "codex fixture 1.0\n" if "--version" in arguments else "a" * 40 + "\n"
        return subprocess.CompletedProcess(arguments, 0, stdout=stdout, stderr="")

    @staticmethod
    def passing_review(case: dict, *_args: object, **_kwargs: object) -> list[dict]:
        return [
            {
                "id": case["criteria"][0]["id"],
                "status": "pass",
                "observation": "Fixture passes.",
            }
        ]

    def runner_patches(self, target: mock.Mock, adjudicator: mock.Mock):
        return mock.patch.multiple(
            RUNNER,
            build=self.fake_build,
            current_runtime_manifest=mock.Mock(
                return_value={"package_identity_sha256": "runtime-identity-1"}
            ),
            target_turn=target,
            adjudicate=adjudicator,
        )

    def test_selection_supports_exact_metadata_affected_and_previous_failure(
        self,
    ) -> None:
        exact = RUNNER.selected_cases(self.spec, self.selection_args(case=["CASE-002"]))
        self.assertEqual([case["id"] for case in exact], ["CASE-002"])
        metadata = RUNNER.selected_cases(
            self.spec, self.selection_args(metadata=["risk=risk-b"])
        )
        self.assertEqual([case["id"] for case in metadata], ["CASE-002", "CASE-003"])
        affected = RUNNER.selected_cases(
            self.spec, self.selection_args(affected_case=["CASE-003"])
        )
        self.assertEqual([case["id"] for case in affected], ["CASE-003"])
        prior = self.root / "prior.json"
        prior.write_text(
            json.dumps(
                {
                    "scenarios": [
                        {"case_id": "CASE-001", "status": "pass"},
                        {"case_id": "CASE-002", "status": "fail"},
                    ]
                }
            ),
            encoding="utf-8",
        )
        previous = RUNNER.selected_cases(
            self.spec, self.selection_args(previously_failing=prior)
        )
        self.assertEqual([case["id"] for case in previous], ["CASE-002"])
        with self.assertRaisesRegex(RUNNER.LiveRunError, "unknown case"):
            RUNNER.selected_cases(self.spec, self.selection_args(case=["CASE-999"]))

        malformed = self.root / "malformed-prior.json"
        malformed.write_text(
            json.dumps({"scenarios": [{"case_id": None, "status": "fail"}]}),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(RUNNER.LiveRunError, "invalid failing case_id"):
            RUNNER.selected_cases(
                self.spec, self.selection_args(previously_failing=malformed)
            )

    def test_certification_product_failure_invokes_no_later_case(self) -> None:
        target = mock.Mock(
            side_effect=lambda **kwargs: (
                "session-" + kwargs["prompt"].split()[0],
                "fixture answer",
                [],
            )
        )

        def review(*, case: dict, **_kwargs: object) -> list[dict]:
            return [
                {
                    "id": case["criteria"][0]["id"],
                    "status": "fail" if case["id"] == "CASE-001" else "pass",
                    "observation": "Fixture review.",
                }
            ]

        adjudicator = mock.Mock(side_effect=review)
        with self.runner_patches(target, adjudicator), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=self.fake_subprocess
        ):
            result = RUNNER.main(self.common_args("run-fail-fast"))
        self.assertEqual(result, 1)
        self.assertEqual(target.call_count, 1)
        self.assertEqual(adjudicator.call_count, 1)
        receipt = json.loads(
            (self.root / "run-fail-fast" / RUNNER.RUNNER_RECEIPT_FILE).read_text()
        )
        self.assertEqual(receipt["outcome"], "product-failure")
        self.assertEqual(receipt["target_calls"], 1)
        scenarios = json.loads((self.root / "run-fail-fast/result.json").read_text())[
            "scenarios"
        ]
        self.assertEqual([scenario["case_id"] for scenario in scenarios], ["CASE-001"])

    def test_provider_retry_is_once_and_retains_typed_telemetry(self) -> None:
        target = mock.Mock(
            side_effect=[
                RUNNER.ProviderFailure("transient provider failure"),
                ("session-1", "fixture answer", []),
            ]
        )
        adjudicator = mock.Mock(
            side_effect=lambda **kwargs: self.passing_review(kwargs["case"])
        )
        args = [
            *self.common_args("run-retry"),
            "--case",
            "CASE-001",
            "--max-target-calls",
            "2",
        ]
        with self.runner_patches(target, adjudicator), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=self.fake_subprocess
        ):
            result = RUNNER.main(args)
        self.assertEqual(result, 0)
        self.assertEqual(target.call_count, 2)
        receipt = json.loads(
            (self.root / "run-retry" / RUNNER.RUNNER_RECEIPT_FILE).read_text()
        )
        self.assertEqual(receipt["target_calls"], 2)
        progress = json.loads(
            (self.root / "run-retry" / RUNNER.PROGRESS_FILE).read_text()
        )
        self.assertEqual(progress["telemetry"]["outcome_counts"]["provider-failure"], 1)
        self.assertEqual(progress["telemetry"]["failures"], 0)

    def test_evaluator_and_harness_failures_keep_distinct_outcomes(self) -> None:
        target = mock.Mock(return_value=("session-1", "fixture answer", []))
        evaluator = mock.Mock(
            side_effect=RUNNER.EvaluatorFailure("invalid rubric output")
        )
        args = [*self.common_args("run-evaluator-failure"), "--case", "CASE-001"]
        with self.runner_patches(target, evaluator), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=self.fake_subprocess
        ):
            self.assertEqual(RUNNER.main(args), 1)
        evaluator_receipt = json.loads(
            (
                self.root / "run-evaluator-failure" / RUNNER.RUNNER_RECEIPT_FILE
            ).read_text()
        )
        self.assertEqual(evaluator_receipt["outcome"], "evaluator-failure")
        self.assertEqual(evaluator_receipt["target_calls"], 1)

        harness_target = mock.Mock(
            side_effect=RUNNER.HarnessFailure("broken local harness")
        )
        unused_evaluator = mock.Mock()
        args = [
            *self.common_args("run-harness-failure"),
            "--case",
            "CASE-001",
            "--max-target-calls",
            "2",
        ]
        with self.runner_patches(harness_target, unused_evaluator), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=self.fake_subprocess
        ):
            self.assertEqual(RUNNER.main(args), 1)
        harness_receipt = json.loads(
            (self.root / "run-harness-failure" / RUNNER.RUNNER_RECEIPT_FILE).read_text()
        )
        self.assertEqual(harness_receipt["outcome"], "harness-failure")
        self.assertEqual(harness_receipt["target_calls"], 2)
        self.assertEqual(unused_evaluator.call_count, 0)

    def test_target_call_limit_stops_before_the_next_call_and_never_passes(
        self,
    ) -> None:
        target = mock.Mock(return_value=("session-1", "fixture answer", []))
        adjudicator = mock.Mock()
        args = [
            *self.common_args("run-limit"),
            "--case",
            "CASE-002",
            "--max-target-calls",
            "1",
            "--infrastructure-retries",
            "0",
        ]
        with self.runner_patches(target, adjudicator), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=self.fake_subprocess
        ):
            result = RUNNER.main(args)
        self.assertEqual(result, 1)
        self.assertEqual(target.call_count, 1)
        self.assertEqual(adjudicator.call_count, 0)
        receipt = json.loads(
            (self.root / "run-limit" / RUNNER.RUNNER_RECEIPT_FILE).read_text()
        )
        self.assertEqual(receipt["outcome"], "limit-reached")
        self.assertFalse(receipt["stage_complete"])

    def test_elapsed_limit_stops_before_the_next_call_and_never_passes(self) -> None:
        target = mock.Mock(return_value=("session-1", "fixture answer", []))
        adjudicator = mock.Mock()
        args = [
            *self.common_args("run-elapsed-limit"),
            "--case",
            "CASE-002",
            "--max-target-calls",
            "10",
            "--max-elapsed-seconds",
            "1",
            "--infrastructure-retries",
            "0",
        ]
        with self.runner_patches(target, adjudicator), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=self.fake_subprocess
        ):
            self.assertEqual(RUNNER.main(args), 1)
        self.assertEqual(target.call_count, 1)
        self.assertEqual(adjudicator.call_count, 0)
        receipt = json.loads(
            (self.root / "run-elapsed-limit" / RUNNER.RUNNER_RECEIPT_FILE).read_text()
        )
        self.assertEqual(receipt["outcome"], "limit-reached")
        progress = json.loads(
            (self.root / "run-elapsed-limit" / RUNNER.PROGRESS_FILE).read_text()
        )
        self.assertIn("max_elapsed_seconds", progress["failure_detail"])

    def test_changed_evaluator_regrades_retained_transcript_with_zero_target_calls(
        self,
    ) -> None:
        target = mock.Mock(return_value=("session-1", "fixture answer", []))
        adjudicator = mock.Mock(
            side_effect=lambda **kwargs: [
                {
                    "id": kwargs["case"]["criteria"][0]["id"],
                    "status": (
                        "fail" if kwargs["model"] == "fixture-evaluator-1" else "pass"
                    ),
                    "observation": "Fixture regrade.",
                }
            ]
        )
        first_args = [*self.common_args("run-regrade"), "--case", "CASE-001"]
        with self.runner_patches(target, adjudicator), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=self.fake_subprocess
        ):
            self.assertEqual(RUNNER.main(first_args), 1)
        self.assertEqual(target.call_count, 1)

        target.reset_mock()
        adjudicator.reset_mock()
        second_args = [
            *self.common_args("run-regrade"),
            "--case",
            "CASE-001",
            "--continue-run",
            "--regrade",
            "--adjudicator-model",
            "fixture-evaluator-2",
        ]
        with self.runner_patches(target, adjudicator), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=self.fake_subprocess
        ):
            self.assertEqual(RUNNER.main(second_args), 0)
        self.assertEqual(target.call_count, 0)
        self.assertEqual(adjudicator.call_count, 1)
        receipt = json.loads(
            (self.root / "run-regrade" / RUNNER.RUNNER_RECEIPT_FILE).read_text()
        )
        self.assertTrue(receipt["regrade"])
        self.assertEqual(receipt["target_calls"], 0)
        self.assertEqual(receipt["evaluator_calls"], 1)
        self.assertEqual(receipt["outcome"], "pass")

    def test_tampered_checkpoint_cannot_be_regraded(self) -> None:
        target = mock.Mock(return_value=("session-1", "fixture answer", []))
        adjudicator = mock.Mock(
            side_effect=lambda **kwargs: self.passing_review(kwargs["case"])
        )
        args = [*self.common_args("run-tamper"), "--case", "CASE-001"]
        with self.runner_patches(target, adjudicator), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=self.fake_subprocess
        ):
            self.assertEqual(RUNNER.main(args), 0)
        progress_path = self.root / "run-tamper" / RUNNER.PROGRESS_FILE
        progress = json.loads(progress_path.read_text())
        progress["sessions"]["CASE-001::default"]["turns"][0]["assistant"] = "tampered"
        progress_path.write_text(json.dumps(progress), encoding="utf-8")
        regrade_args = [
            *self.common_args("run-tamper"),
            "--case",
            "CASE-001",
            "--continue-run",
            "--regrade",
            "--adjudicator-model",
            "fixture-evaluator-2",
        ]
        with self.runner_patches(target, adjudicator), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=self.fake_subprocess
        ), self.assertRaisesRegex(RUNNER.HarnessFailure, "content identity mismatch"):
            RUNNER.main(regrade_args)

    def test_tampered_session_or_runtime_reads_cannot_be_regraded(self) -> None:
        for suffix, mutate in (
            (
                "session",
                lambda checkpoint: checkpoint.update(
                    {"session_id": "tampered-session"}
                ),
            ),
            (
                "reads",
                lambda checkpoint: checkpoint.update(
                    {"successful_runtime_reads": ["tampered/path"]}
                ),
            ),
        ):
            with self.subTest(field=suffix):
                target = mock.Mock(return_value=("session-1", "fixture answer", []))
                adjudicator = mock.Mock(
                    side_effect=lambda **kwargs: self.passing_review(kwargs["case"])
                )
                output_name = f"run-tamper-{suffix}"
                args = [*self.common_args(output_name), "--case", "CASE-001"]
                with self.runner_patches(target, adjudicator), mock.patch.object(
                    RUNNER.subprocess, "run", side_effect=self.fake_subprocess
                ):
                    self.assertEqual(RUNNER.main(args), 0)
                progress_path = self.root / output_name / RUNNER.PROGRESS_FILE
                progress = json.loads(progress_path.read_text())
                mutate(progress["sessions"]["CASE-001::default"])
                progress_path.write_text(json.dumps(progress), encoding="utf-8")
                regrade_args = [
                    *self.common_args(output_name),
                    "--case",
                    "CASE-001",
                    "--continue-run",
                    "--regrade",
                    "--adjudicator-model",
                    "fixture-evaluator-2",
                ]
                with self.runner_patches(target, adjudicator), mock.patch.object(
                    RUNNER.subprocess, "run", side_effect=self.fake_subprocess
                ), self.assertRaisesRegex(
                    RUNNER.HarnessFailure, "session content identity mismatch"
                ):
                    RUNNER.main(regrade_args)

    def test_diagnostic_continues_for_named_decision_but_remains_nonpassing(
        self,
    ) -> None:
        target = mock.Mock(
            side_effect=lambda **kwargs: (
                "session-" + kwargs["prompt"].replace(" ", "-"),
                "fixture answer",
                [],
            )
        )

        def review(*, case: dict, **_kwargs: object) -> list[dict]:
            return [
                {
                    "id": case["criteria"][0]["id"],
                    "status": "fail" if case["id"] == "CASE-001" else "pass",
                    "observation": "Fixture diagnostic.",
                }
            ]

        adjudicator = mock.Mock(side_effect=review)
        args = [
            *self.common_args("run-diagnostic-bounded"),
            "--mode",
            "diagnostic",
            "--diagnostic-decision",
            "determine whether the first failure generalises",
            "--case",
            "CASE-001",
            "--case",
            "CASE-002",
            "--max-failures",
            "2",
            "--max-target-calls",
            "3",
        ]
        with self.runner_patches(target, adjudicator), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=self.fake_subprocess
        ):
            self.assertEqual(RUNNER.main(args), 1)
        self.assertEqual(target.call_count, 3)
        self.assertEqual(adjudicator.call_count, 2)
        receipt = json.loads(
            (
                self.root / "run-diagnostic-bounded" / RUNNER.RUNNER_RECEIPT_FILE
            ).read_text()
        )
        self.assertEqual(receipt["mode"], "diagnostic")
        self.assertEqual(receipt["outcome"], "product-failure")
        self.assertEqual(receipt["selected_scope"], ["CASE-001", "CASE-002"])

    def test_diagnostic_failure_limit_stops_before_the_next_case(self) -> None:
        target = mock.Mock(return_value=("session-1", "fixture answer", []))
        adjudicator = mock.Mock(
            return_value=[
                {
                    "id": "CASE-001-AC",
                    "status": "fail",
                    "observation": "Fixture diagnostic failure.",
                }
            ]
        )
        args = [
            *self.common_args("run-diagnostic-failure-limit"),
            "--mode",
            "diagnostic",
            "--diagnostic-decision",
            "stop after the first retained product failure",
            "--case",
            "CASE-001",
            "--case",
            "CASE-002",
            "--max-failures",
            "1",
            "--max-target-calls",
            "3",
        ]
        with self.runner_patches(target, adjudicator), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=self.fake_subprocess
        ):
            self.assertEqual(RUNNER.main(args), 1)
        self.assertEqual(target.call_count, 1)
        self.assertEqual(adjudicator.call_count, 1)
        receipt = json.loads(
            (
                self.root / "run-diagnostic-failure-limit" / RUNNER.RUNNER_RECEIPT_FILE
            ).read_text()
        )
        self.assertEqual(receipt["outcome"], "limit-reached")
        progress = json.loads(
            (
                self.root / "run-diagnostic-failure-limit" / RUNNER.PROGRESS_FILE
            ).read_text()
        )
        self.assertIn("max_failures", progress["failure_detail"])

    def test_adapter_json_is_parseable_and_uses_typed_outcome_with_zero_exit(
        self,
    ) -> None:
        target = mock.Mock(return_value=("session-1", "fixture answer", []))
        adjudicator = mock.Mock(
            return_value=[
                {
                    "id": "CASE-001-AC",
                    "status": "fail",
                    "observation": "Fixture failure.",
                }
            ]
        )
        args = [
            *self.common_args("run-adapter-json"),
            "--case",
            "CASE-001",
            "--adapter-json",
        ]
        output = io.StringIO()
        errors = io.StringIO()
        with self.runner_patches(target, adjudicator), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=self.fake_subprocess
        ), contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            self.assertEqual(RUNNER.main(args), 0)
        receipt = json.loads(output.getvalue())
        self.assertEqual(receipt["outcome"], "product-failure")
        self.assertEqual(receipt["target_calls"], 1)
        self.assertIn("TARGET CASE-001", errors.getvalue())

    def test_adapter_request_binds_exact_generic_campaign_inputs(self) -> None:
        request = {
            "schema_version": 1,
            "action": "verify",
            "candidate_identity": "candidate-1",
            "source_identity": "sha256:coordinator-source",
            "proof_contract_identity": "sha256:coordinator-proof",
            "mode": "certification",
            "stage": "canary",
            "selected_scope": ["CASE-001"],
            "limits": {
                "max_failures": 1,
                "max_target_calls": 2,
                "max_elapsed_seconds": 100,
            },
            "prior_receipt_identities": [],
            "retained_target_identity": None,
        }
        request["request_identity"] = RUNNER.canonical_identity(request)
        target = mock.Mock(return_value=("session-1", "fixture answer", []))
        adjudicator = mock.Mock(
            side_effect=lambda **kwargs: self.passing_review(kwargs["case"])
        )
        args = [
            *self.common_args("run-bound-adapter"),
            "--case",
            "CASE-001",
            "--adapter-json",
            "--adapter-request-stdin",
        ]
        output = io.StringIO()
        with self.runner_patches(target, adjudicator), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=self.fake_subprocess
        ), mock.patch.object(
            sys, "stdin", io.StringIO(json.dumps(request))
        ), contextlib.redirect_stdout(
            output
        ), contextlib.redirect_stderr(
            io.StringIO()
        ):
            self.assertEqual(RUNNER.main(args), 0)
        receipt = json.loads(output.getvalue())
        for field_name in (
            "request_identity",
            "candidate_identity",
            "source_identity",
            "proof_contract_identity",
            "stage",
        ):
            self.assertEqual(receipt[field_name], request[field_name])
        self.assertIn("verifier_candidate_identity", receipt)
        self.assertNotEqual(
            receipt["verifier_candidate_identity"], receipt["candidate_identity"]
        )

        changed_stage = {**request, "stage": "full"}
        changed_stage["request_identity"] = RUNNER.canonical_identity(
            {
                key: value
                for key, value in changed_stage.items()
                if key != "request_identity"
            }
        )
        continued_args = [*args, "--continue-run"]
        with self.runner_patches(target, adjudicator), mock.patch.object(
            RUNNER.subprocess, "run", side_effect=self.fake_subprocess
        ), mock.patch.object(
            sys, "stdin", io.StringIO(json.dumps(changed_stage))
        ), self.assertRaisesRegex(
            RUNNER.LiveRunError, "adapter_contract_identity"
        ):
            RUNNER.main(continued_args)

    def test_adapter_request_rejects_scope_or_identity_drift(self) -> None:
        request = {
            "schema_version": 1,
            "action": "verify",
            "candidate_identity": "candidate-1",
            "source_identity": "sha256:coordinator-source",
            "proof_contract_identity": "sha256:coordinator-proof",
            "mode": "certification",
            "stage": "canary",
            "selected_scope": ["CASE-002"],
            "limits": {
                "max_failures": 1,
                "max_target_calls": 2,
                "max_elapsed_seconds": 100,
            },
            "prior_receipt_identities": [],
            "retained_target_identity": None,
        }
        request["request_identity"] = RUNNER.canonical_identity(request)
        args = [
            *self.common_args("run-drifted-adapter"),
            "--case",
            "CASE-001",
            "--adapter-json",
            "--adapter-request-stdin",
        ]
        with mock.patch.object(
            sys, "stdin", io.StringIO(json.dumps(request))
        ), self.assertRaisesRegex(RUNNER.LiveRunError, "selected_scope"):
            RUNNER.main(args)

    def test_diagnostic_requires_named_selected_scope_and_explicit_limits(self) -> None:
        args = [*self.common_args("run-diagnostic"), "--mode", "diagnostic"]
        with self.assertRaisesRegex(RUNNER.LiveRunError, "diagnostic-decision"):
            RUNNER.main(args)

    def test_capability_contract_is_standalone_and_generic(self) -> None:
        capabilities = RUNNER.runner_capabilities()
        self.assertEqual(
            set(capabilities["capabilities"]), set(RUNNER.RUNNER_CAPABILITIES)
        )
        self.assertIn("request-binding", capabilities["capabilities"])
        source = RUNNER_PATH.read_text(encoding="utf-8").lower()
        self.assertNotIn("project_workflow", source)
        self.assertNotIn("project-workflow", source)

    def test_current_runtime_identity_is_computed_without_package_writes(self) -> None:
        before = {
            path.relative_to(REPOSITORY_ROOT).as_posix()
            for path in (REPOSITORY_ROOT / "evidence" / "evaluations").rglob("*")
        }
        current = RUNNER.current_runtime_manifest(REPOSITORY_ROOT)
        retained = json.loads(
            (
                REPOSITORY_ROOT
                / "evidence/evaluations/drift-smoke/run-009/runtime-package-manifest.json"
            ).read_text(encoding="utf-8")
        )
        after = {
            path.relative_to(REPOSITORY_ROOT).as_posix()
            for path in (REPOSITORY_ROOT / "evidence" / "evaluations").rglob("*")
        }
        self.assertEqual(
            current["package_identity_sha256"], retained["package_identity_sha256"]
        )
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
