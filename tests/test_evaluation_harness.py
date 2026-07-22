from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = REPOSITORY_ROOT / "scripts" / "evaluation_harness.py"


def load_harness():
    spec = importlib.util.spec_from_file_location("evaluation_harness", HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load evaluation harness")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HARNESS = load_harness()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(HARNESS.rendered_json_bytes(value))


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout.strip()


class EvaluationHarnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary_directory.name)
        self.source = self.base / "source"
        self.source.mkdir()
        self.copy_authority_surface()
        self.write_frozen_inputs()
        git(self.source, "init", "-b", "main")
        git(self.source, "config", "user.email", "evaluation@example.invalid")
        git(self.source, "config", "user.name", "Evaluation Fixture")
        git(self.source, "add", ".")
        git(self.source, "commit", "-m", "authority")
        self.authority_commit = git(self.source, "rev-parse", "HEAD")
        self.authority_tree = git(self.source, "rev-parse", "HEAD^{tree}")
        self.runtime_manifest = self.write_runtime_manifest()
        self.config = self.write_config()
        self.freeze_manifest = (
            self.source
            / "evidence"
            / "evaluations"
            / "iteration-001"
            / "freeze-manifest.json"
        )
        self.plan_path = (
            self.source
            / "evidence"
            / "evaluations"
            / "iteration-001"
            / "runs"
            / "run-001"
            / "run-plan.json"
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def copy_authority_surface(self) -> None:
        template_source = (
            REPOSITORY_ROOT
            / "skills"
            / "strategic-advisor"
            / "evals"
            / "freeze-manifest.template.json"
        )
        template = json.loads(template_source.read_text(encoding="utf-8"))
        paths = [record["path"] for record in template["authority_files"]]
        paths.append("skills/strategic-advisor/evals/freeze-manifest.template.json")
        allowlist = json.loads(
            (
                REPOSITORY_ROOT
                / "skills"
                / "strategic-advisor"
                / "runtime-manifest.json"
            ).read_text(encoding="utf-8")
        )
        paths.extend(
            f"skills/strategic-advisor/{relative}"
            for relative in allowlist["include"]
        )
        for relative in sorted(set(paths)):
            source = REPOSITORY_ROOT / relative
            destination = self.source / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

    def write_frozen_inputs(self) -> None:
        values = {
            "evidence/freeze-inputs/system-and-developer-context.txt": "system context\n",
            "evidence/freeze-inputs/tool-policy.json": '{"tools":[]}\n',
            "evidence/freeze-inputs/non-treatment-context.txt": "shared context\n",
            "evidence/freeze-inputs/declared-inputs.json": '{"inputs":[]}\n',
            "evidence/freeze-inputs/activation-contract.json": '{"activation":"automatic"}\n',
            "evidence/freeze-inputs/holdout-commitment.json": '{"commitments":6}\n',
            "evidence/freeze-inputs/holdout-independence.md": "Independent author attestation.\n",
        }
        for relative, content in values.items():
            path = self.source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def write_runtime_manifest(self) -> Path:
        allowlist_path = (
            self.source / "skills" / "strategic-advisor" / "runtime-manifest.json"
        )
        allowlist_bytes = allowlist_path.read_bytes()
        allowlist = json.loads(allowlist_bytes.decode("utf-8"))
        files = []
        for relative in sorted(allowlist["include"]):
            content = (
                self.source / "skills" / "strategic-advisor" / relative
            ).read_bytes()
            files.append(
                {
                    "path": relative,
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "size_bytes": len(content),
                }
            )
        identity_payload = {
            "files": files,
            "schema_version": 1,
            "source_allowlist_sha256": hashlib.sha256(allowlist_bytes).hexdigest(),
        }
        manifest = {
            "file_count": len(files),
            "files": files,
            "identity_algorithm": "sha256-canonical-json-v1",
            "package_identity_sha256": hashlib.sha256(
                HARNESS.canonical_json_bytes(identity_payload)
            ).hexdigest(),
            "package_root": "skills/strategic-advisor",
            "schema_version": 1,
            "source_allowlist": {
                "path": "skills/strategic-advisor/runtime-manifest.json",
                "sha256": hashlib.sha256(allowlist_bytes).hexdigest(),
            },
        }
        path = (
            self.source
            / "evidence"
            / "evaluations"
            / "iteration-001"
            / "runtime-package-manifest.json"
        )
        write_json(path, manifest)
        return path

    def write_config(self) -> Path:
        config = {
            "generation": {
                "model": "fixture-generation-model",
                "model_version": "fixture-generation-v1",
                "host": "fixture-host",
                "configuration": {"temperature": 0.2},
                "frozen_context_artifacts": {
                    "system_and_developer_context": {
                        "path": "evidence/freeze-inputs/system-and-developer-context.txt"
                    },
                    "tool_policy": {"path": "evidence/freeze-inputs/tool-policy.json"},
                    "non_treatment_context": {
                        "path": "evidence/freeze-inputs/non-treatment-context.txt"
                    },
                    "declared_input_manifest": {
                        "path": "evidence/freeze-inputs/declared-inputs.json"
                    },
                },
                "treatment_activation": {
                    "contract_path": "evidence/freeze-inputs/activation-contract.json",
                    "package_availability_proof": "Fixture host exposes package discovery metadata.",
                },
            },
            "scoring": {
                "model": "fixture-scorer-model",
                "model_version": "fixture-scorer-v1",
                "host": "fixture-host",
                "configuration": {"temperature": 0},
                "adjudication_model": "fixture-adjudicator-model",
                "adjudication_model_version": "fixture-adjudicator-v1",
                "adjudication_configuration": {"temperature": 0},
                "case_assertion_grading": {
                    "model": "fixture-assertion-model",
                    "model_version": "fixture-assertion-v1",
                    "host": "fixture-host",
                    "configuration": {"temperature": 0},
                },
            },
            "condition_audit": {
                "model": "fixture-auditor-model",
                "model_version": "fixture-auditor-v1",
                "host": "fixture-host",
                "configuration": {"temperature": 0},
            },
            "sealed_holdout": {
                "commitment_manifest_path": "evidence/freeze-inputs/holdout-commitment.json",
                "independence_attestation_path": "evidence/freeze-inputs/holdout-independence.md",
            },
        }
        path = self.base / "freeze-config.json"
        write_json(path, config)
        return path

    def freeze_args(self) -> argparse.Namespace:
        return argparse.Namespace(
            source_root=self.source,
            template="skills/strategic-advisor/evals/freeze-manifest.template.json",
            config=self.config,
            runtime_package_manifest=self.runtime_manifest,
            output=self.freeze_manifest,
            authority_source_commit=self.authority_commit,
            authority_source_tree=self.authority_tree,
            frozen_at="2026-07-22T01:02:03Z",
            masking_seed_hex="1" * 64,
            bootstrap_seed_hex="2" * 64,
        )

    def create_freeze_commit(self) -> None:
        HARNESS.freeze(self.freeze_args())
        git(self.source, "add", "evidence/evaluations/iteration-001")
        git(self.source, "commit", "-m", "freeze")
        self.freeze_commit = git(self.source, "rev-parse", "HEAD")
        HARNESS.verify_freeze_manifest(
            self.source, self.freeze_manifest, self.freeze_commit
        )

    def create_plan(self) -> dict:
        HARNESS.make_plan(
            argparse.Namespace(
                source_root=self.source,
                freeze_manifest=self.freeze_manifest,
                freeze_commit=self.freeze_commit,
                run_id="run-001",
                output=self.plan_path,
            )
        )
        return json.loads(self.plan_path.read_text(encoding="utf-8"))

    def score_result(
        self,
        unit: dict,
        not_applicable: list[str],
        *,
        failed_all_gates: bool = False,
    ) -> dict:
        applicability = {
            dimension: {
                "applicable": dimension not in not_applicable,
                "basis": "Frozen-list membership establishes applicability.",
            }
            for dimension in HARNESS.DIMENSIONS
        }
        responses = {}
        for label in ("A", "B"):
            responses[label] = {
                "dimensions": {
                    dimension: {
                        "score": None if dimension in not_applicable else 3,
                        "evidence": "Fixture response-specific evidence.",
                    }
                    for dimension in HARNESS.DIMENSIONS
                },
                "hard_gates": {
                    gate: {
                        "failed": failed_all_gates,
                        "evidence": "Fixture gate-specific evidence.",
                    }
                    for gate in HARNESS.HARD_GATES
                },
            }
        return {
            "schema_version": "strategic-advisor-scorer-v2",
            "case_id": unit["case_id"],
            "draw_id": unit["draw_id"],
            "scoring_pass_id": unit["unit_id"],
            "not_applicable_dimensions": not_applicable,
            "dimension_applicability": applicability,
            "responses": responses,
            "comparison": {
                "better_response": "tie",
                "most_decision_relevant_difference": "The fixture scores are equal.",
                "rubric_ambiguity_or_missing_evidence": "",
            },
        }

    def create_complete_artifacts(self, plan: dict, *, failed_all_gates: bool = False) -> None:
        run_root = self.plan_path.parent
        freeze = json.loads(self.freeze_manifest.read_text(encoding="utf-8"))
        identity = plan["freeze_identity"]
        plan_sha256 = hashlib.sha256(self.plan_path.read_bytes()).hexdigest()
        raw_by_unit: dict[str, bytes] = {}
        raw_hash_by_unit: dict[str, str] = {}
        pairs = {
            (pair["case_id"], pair["draw_id"]): pair for pair in plan["pairs"]
        }
        cases = {case["case_id"]: case for case in plan["cases"]}
        matched_context = {
            "declared_input_manifest_sha256": freeze["generation"][
                "declared_input_manifest_sha256"
            ],
            "non_treatment_context_sha256": freeze["generation"][
                "non_treatment_context_sha256"
            ],
            "system_and_developer_context_sha256": freeze["generation"][
                "system_and_developer_context_sha256"
            ],
            "tool_policy_sha256": freeze["generation"]["tool_policy_sha256"],
        }
        for unit in plan["generation_units"]:
            raw = f"# Fixture response\n\n{unit['unit_id']}\n".encode("utf-8")
            raw_path = run_root / unit["raw_response_path"]
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            raw_path.write_bytes(raw)
            digest = hashlib.sha256(raw).hexdigest()
            treatment = (
                {
                    "runtime_package_identity_sha256": identity[
                        "runtime_package_identity_sha256"
                    ],
                    "package_discovered": True,
                    "skill_selected": True,
                    "loaded_reference_paths": ["SKILL.md"],
                }
                if unit["condition"] == "skilled"
                else {
                    "runtime_package_identity_sha256": None,
                    "package_discovered": False,
                    "skill_selected": False,
                    "loaded_reference_paths": [],
                }
            )
            artifact = {
                "schema_version": 1,
                "artifact_type": "generation",
                "unit_id": unit["unit_id"],
                "attempt_id": unit["attempt_id"],
                "run_id": plan["run_id"],
                "plan_sha256": plan_sha256,
                "freeze_identity": identity,
                "case_id": unit["case_id"],
                "draw_id": unit["draw_id"],
                "condition": unit["condition"],
                "case_prompt_sha256": cases[unit["case_id"]]["prompt_sha256"],
                "status": "complete",
                "host_context_id": "context:" + unit["unit_id"],
                "model": freeze["generation"]["model"],
                "model_version": freeze["generation"]["model_version"],
                "host": freeze["generation"]["host"],
                "configuration": freeze["generation"]["configuration"],
                "matched_context": matched_context,
                "treatment": treatment,
                "raw_response_path": unit["raw_response_path"],
                "raw_response_sha256": digest,
                "started_at": "2026-07-22T02:00:00Z",
                "finished_at": "2026-07-22T02:00:01Z",
                "error": None,
            }
            write_json(run_root / unit["artifact_path"], artifact)
            raw_by_unit[unit["unit_id"]] = raw
            raw_hash_by_unit[unit["unit_id"]] = digest

        quality_epoch = datetime(2026, 7, 22, 2, 1, 0, tzinfo=timezone.utc)
        for quality_index, unit in enumerate(plan["quality_units"]):
            pair = pairs[(unit["case_id"], unit["draw_id"])]
            presented_hashes = {
                label: raw_hash_by_unit[
                    pair["base_sources"][base_label.removeprefix("base-")]
                ]
                for label, base_label in unit["presentation"].items()
            }
            artifact = {
                "schema_version": 1,
                "artifact_type": "quality-score",
                "unit_id": unit["unit_id"],
                "attempt_id": unit["attempt_id"],
                "run_id": plan["run_id"],
                "plan_sha256": plan_sha256,
                "freeze_identity": identity,
                "case_id": unit["case_id"],
                "draw_id": unit["draw_id"],
                "pass_id": unit["pass_id"],
                "status": "complete",
                "host_context_id": "context:" + unit["unit_id"],
                "model": freeze["scoring"]["model"],
                "model_version": freeze["scoring"]["model_version"],
                "host": freeze["scoring"]["host"],
                "configuration": freeze["scoring"]["configuration"],
                "scorer_prompt_sha256": freeze["scoring"]["scorer_prompt_sha256"],
                "presentation": unit["presentation"],
                "presented_response_sha256": presented_hashes,
                "input_envelope": HARNESS.expected_quality_input_envelope(
                    freeze,
                    cases[unit["case_id"]],
                    unit["draw_id"],
                    unit["unit_id"],
                    presented_hashes,
                ),
                "started_at": (
                    quality_epoch + timedelta(seconds=quality_index * 2)
                ).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "finished_at": (
                    quality_epoch + timedelta(seconds=quality_index * 2 + 1)
                ).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "result": self.score_result(
                    unit,
                    cases[unit["case_id"]]["not_applicable_dimensions"],
                    failed_all_gates=failed_all_gates,
                ),
                "error": None,
            }
            write_json(run_root / unit["artifact_path"], artifact)

        for unit in plan["condition_audit_units"]:
            pair = pairs[(unit["case_id"], unit["draw_id"])]
            if unit["audit_mode"] == "structure-only":
                hashes = {}
                for label in ("A", "B"):
                    source_unit = pair["base_sources"][
                        unit["presentation"][label].removeprefix("base-")
                    ]
                    view = HARNESS.structure_view(raw_by_unit[source_unit])
                    path = run_root / unit[f"presented_{label}_path"]
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(view)
                    hashes[label] = hashlib.sha256(view).hexdigest()
            else:
                hashes = {
                    label: raw_hash_by_unit[
                        pair["base_sources"][base_label.removeprefix("base-")]
                    ]
                    for label, base_label in unit["presentation"].items()
                }
            result = {
                "schema_version": "strategic-advisor-condition-auditor-v1",
                "case_id": unit["case_id"],
                "draw_id": unit["draw_id"],
                "audit_id": unit["unit_id"],
                "audit_mode": unit["audit_mode"],
                "likely_skilled": "unclear",
                "confidence_1_to_5": 1,
                "evidence": "Fixture inputs do not discriminate.",
            }
            artifact = {
                "schema_version": 1,
                "artifact_type": "condition-audit",
                "unit_id": unit["unit_id"],
                "attempt_id": unit["attempt_id"],
                "run_id": plan["run_id"],
                "plan_sha256": plan_sha256,
                "freeze_identity": identity,
                "case_id": unit["case_id"],
                "draw_id": unit["draw_id"],
                "audit_mode": unit["audit_mode"],
                "status": "complete",
                "host_context_id": "context:" + unit["unit_id"],
                "model": freeze["condition_audit"]["model"],
                "model_version": freeze["condition_audit"]["model_version"],
                "host": freeze["condition_audit"]["host"],
                "configuration": freeze["condition_audit"]["configuration"],
                "auditor_prompt_sha256": freeze["condition_audit"]["prompt_sha256"],
                "presentation": unit["presentation"],
                "presented_input_sha256": hashes,
                "input_envelope": HARNESS.expected_audit_input_envelope(
                    freeze,
                    cases[unit["case_id"]],
                    unit["draw_id"],
                    unit["unit_id"],
                    unit["audit_mode"],
                    hashes,
                ),
                "started_at": "2026-07-22T03:00:00Z",
                "finished_at": "2026-07-22T03:00:01Z",
                "result": result,
                "error": None,
            }
            write_json(run_root / unit["artifact_path"], artifact)

    def verify_artifacts(self) -> dict:
        return HARNESS.verify_artifacts(
            argparse.Namespace(
                source_root=self.source,
                freeze_manifest=self.freeze_manifest,
                freeze_commit=self.freeze_commit,
                plan=self.plan_path,
            )
        )

    def test_freeze_rejects_any_preexisting_result_artifact(self) -> None:
        result_path = (
            self.runtime_manifest.parent / "results" / "premature-result.json"
        )
        write_json(result_path, {"release_gate": "passed"})
        with self.assertRaisesRegex(HARNESS.HarnessError, "pre-freeze output/result"):
            HARNESS.freeze(self.freeze_args())
        self.assertFalse(self.freeze_manifest.exists())

    def test_freeze_config_cannot_replace_authority_files(self) -> None:
        config = json.loads(self.config.read_text(encoding="utf-8"))
        config["authority_files"] = [
            {"path": "skills/strategic-advisor/evals/evals.json", "sha256": ""}
        ]
        write_json(self.config, config)
        with self.assertRaisesRegex(
            HARNESS.HarnessError, "cannot override authority or protocol"
        ):
            HARNESS.freeze(self.freeze_args())
        self.assertFalse(self.freeze_manifest.exists())

    def test_freeze_rejects_hidden_answer_key_in_model_configuration(self) -> None:
        evals = json.loads(
            (
                self.source / "skills/strategic-advisor/evals/evals.json"
            ).read_text(encoding="utf-8")
        )
        config = json.loads(self.config.read_text(encoding="utf-8"))
        config["generation"]["configuration"]["nested"] = {
            "hidden_answer_key": evals["evals"][0]["assertions"][0]
        }
        write_json(self.config, config)
        with self.assertRaisesRegex(HARNESS.HarnessError, "hidden outcome or mapping"):
            HARNESS.freeze(self.freeze_args())

    def test_freeze_rejects_direct_condition_mappings_across_model_configs(self) -> None:
        cases = (
            (
                "generation phrase",
                ("generation", "configuration"),
                {"routing_note": "A is skilled"},
            ),
            (
                "scorer label pair",
                ("scoring", "configuration"),
                {"labels": ["skilled", "control"]},
            ),
            (
                "adjudicator group pair",
                ("scoring", "adjudication_configuration"),
                {"group": ["skill-enabled", "baseline"]},
            ),
            (
                "assertion grader object pair",
                ("scoring", "case_assertion_grading", "configuration"),
                {"assignments": {"A": "skilled", "B": "control"}},
            ),
            (
                "auditor reverse phrase",
                ("condition_audit", "configuration"),
                {"routing_note": "skill-enabled: A"},
            ),
        )
        for label, path, payload in cases:
            with self.subTest(label=label):
                self.write_config()
                config = json.loads(self.config.read_text(encoding="utf-8"))
                target = config
                for segment in path[:-1]:
                    target = target[segment]
                target[path[-1]] = payload
                write_json(self.config, config)
                with self.assertRaisesRegex(
                    HARNESS.HarnessError, "direct condition or skill mapping"
                ):
                    HARNESS.freeze(self.freeze_args())

    def test_configuration_mapping_scan_allows_neutral_configuration(self) -> None:
        neutral_configurations = (
            {
                "labels": ["concise", "detailed"],
                "reference_mode": "baseline",
                "routing_note": "A is available",
            },
            {
                "group": ["primary", "fallback"],
                "operator_level": "skilled",
                "temperature": 0,
            },
        )
        for index, configuration in enumerate(neutral_configurations):
            with self.subTest(index=index):
                HARNESS.validate_configuration_boundary(
                    configuration,
                    "neutral.configuration",
                    set(),
                    set(),
                )

    def test_verify_freeze_rejects_uncommitted_frozen_input_substitute(self) -> None:
        substitute_relative = "evidence/freeze-inputs/uncommitted-tool-policy.json"
        substitute = self.source / substitute_relative
        substitute.write_text('{"tools":[]}\n', encoding="utf-8")
        config = json.loads(self.config.read_text(encoding="utf-8"))
        config["generation"]["frozen_context_artifacts"]["tool_policy"] = {
            "path": substitute_relative
        }
        write_json(self.config, config)
        HARNESS.freeze(self.freeze_args())
        git(self.source, "add", "evidence/evaluations/iteration-001")
        git(self.source, "commit", "-m", "freeze without referenced tool policy")
        freeze_commit = git(self.source, "rev-parse", "HEAD")
        with self.assertRaisesRegex(HARNESS.HarnessError, "absent from commit"):
            HARNESS.verify_freeze_manifest(
                self.source, self.freeze_manifest, freeze_commit
            )

    def test_runtime_provenance_must_match_authority_commit_bytes(self) -> None:
        runtime = json.loads(self.runtime_manifest.read_text(encoding="utf-8"))
        runtime["files"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(
            HARNESS.HarnessError, "authority_source_commit bytes"
        ):
            HARNESS.verify_runtime_sources_in_authority_commit(
                self.source, runtime, self.authority_commit
            )

    def test_freeze_rejects_context_path_into_evaluation_authority(self) -> None:
        config = json.loads(self.config.read_text(encoding="utf-8"))
        config["generation"]["frozen_context_artifacts"]["tool_policy"] = {
            "path": "skills/strategic-advisor/evals/evals.json"
        }
        write_json(self.config, config)
        with self.assertRaisesRegex(HARNESS.HarnessError, "evaluation/result boundary"):
            HARNESS.freeze(self.freeze_args())

    def test_freeze_rejects_evaluation_fingerprint_in_context_content(self) -> None:
        evals = json.loads(
            (
                self.source / "skills/strategic-advisor/evals/evals.json"
            ).read_text(encoding="utf-8")
        )
        leaked_relative = "evidence/freeze-inputs/leaked-case.txt"
        (self.source / leaked_relative).write_text(
            evals["evals"][0]["prompt"] + "\n", encoding="utf-8"
        )
        config = json.loads(self.config.read_text(encoding="utf-8"))
        config["generation"]["frozen_context_artifacts"][
            "non_treatment_context"
        ] = {"path": leaked_relative}
        write_json(self.config, config)
        with self.assertRaisesRegex(HARNESS.HarnessError, "evaluation fingerprint"):
            HARNESS.freeze(self.freeze_args())

    def test_verify_freeze_rejects_authority_drift(self) -> None:
        self.create_freeze_commit()
        rubric = self.source / "skills/strategic-advisor/evals/RUBRIC.md"
        rubric.write_text(rubric.read_text(encoding="utf-8") + "\nDrift.\n", encoding="utf-8")
        with self.assertRaisesRegex(HARNESS.HarnessError, "authority drift"):
            HARNESS.verify_freeze_manifest(
                self.source, self.freeze_manifest, self.freeze_commit
            )

    def test_plan_is_deterministic_and_inverts_second_quality_pass(self) -> None:
        self.create_freeze_commit()
        first = self.create_plan()
        first_bytes = self.plan_path.read_bytes()
        for pair in first["pairs"]:
            self.assertEqual(
                pair["quality_presentations"]["score-1"],
                {"A": "base-A", "B": "base-B"},
            )
            self.assertEqual(
                pair["quality_presentations"]["score-2"],
                {"A": "base-B", "B": "base-A"},
            )
        self.assertGreaterEqual(first["case_count"], 16)
        self.assertGreaterEqual(len(first["draw_ids"]), 2)
        shutil.rmtree(self.plan_path.parent)
        second = self.create_plan()
        self.assertEqual(first, second)
        self.assertEqual(first_bytes, self.plan_path.read_bytes())

    def test_verify_artifacts_rejects_incomplete_matrix(self) -> None:
        self.create_freeze_commit()
        plan = self.create_plan()
        self.create_complete_artifacts(plan)
        missing = self.plan_path.parent / plan["quality_units"][0]["artifact_path"]
        missing.unlink()
        with self.assertRaisesRegex(HARNESS.HarnessError, "incomplete or contaminated"):
            self.verify_artifacts()

    def test_plan_validation_rejects_non_inverted_second_pass(self) -> None:
        self.create_freeze_commit()
        plan = self.create_plan()
        plan["pairs"][0]["quality_presentations"]["score-2"] = {
            "A": "base-A",
            "B": "base-B",
        }
        freeze = json.loads(self.freeze_manifest.read_text(encoding="utf-8"))
        with self.assertRaisesRegex(HARNESS.HarnessError, "work units or mappings"):
            HARNESS.validate_plan_matrix(self.source, freeze, plan)

    def test_verify_artifacts_rejects_condition_guess_in_quality_score(self) -> None:
        self.create_freeze_commit()
        plan = self.create_plan()
        self.create_complete_artifacts(plan)
        unit = plan["quality_units"][0]
        path = self.plan_path.parent / unit["artifact_path"]
        artifact = json.loads(path.read_text(encoding="utf-8"))
        artifact["result"]["condition_guess"] = "A"
        write_json(path, artifact)
        with self.assertRaisesRegex(HARNESS.HarnessError, "forbidden condition_guess"):
            self.verify_artifacts()

    def test_verify_artifacts_rejects_explicit_skill_identity_scoring_reason(self) -> None:
        self.create_freeze_commit()
        plan = self.create_plan()
        self.create_complete_artifacts(plan)
        unit = plan["quality_units"][0]
        path = self.plan_path.parent / unit["artifact_path"]
        artifact = json.loads(path.read_text(encoding="utf-8"))
        artifact["result"]["responses"]["A"]["dimensions"]["reality_fidelity"][
            "evidence"
        ] = "Response A appears to be skill-enabled, so I scored it higher."
        write_json(path, artifact)
        with self.assertRaisesRegex(
            HARNESS.HarnessError, "apparent-condition or skill-identity"
        ):
            self.verify_artifacts()

    def test_verify_artifacts_rejects_direct_identity_causal_rating(self) -> None:
        self.create_freeze_commit()
        plan = self.create_plan()
        self.create_complete_artifacts(plan)
        unit = plan["quality_units"][0]
        path = self.plan_path.parent / unit["artifact_path"]
        statements = (
            "A is skilled, so I rated it higher.",
            "B used Strategic Advisor and therefore scores 5.",
        )
        for statement in statements:
            with self.subTest(statement=statement):
                artifact = json.loads(path.read_text(encoding="utf-8"))
                artifact["result"]["responses"]["A"]["dimensions"][
                    "reality_fidelity"
                ]["evidence"] = statement
                write_json(path, artifact)
                with self.assertRaisesRegex(
                    HARNESS.HarnessError,
                    "apparent-condition or skill-identity",
                ):
                    self.verify_artifacts()

    def test_identity_reason_scan_allows_rating_without_identity_inference(self) -> None:
        HARNESS.reject_apparent_identity_reasoning(
            {"evidence": "Response A is clearer, so I rated it higher."}
        )

    def test_verify_artifacts_rejects_output_ordering_before_dependencies(self) -> None:
        self.create_freeze_commit()
        plan = self.create_plan()
        self.create_complete_artifacts(plan)
        unit = plan["quality_units"][0]
        path = self.plan_path.parent / unit["artifact_path"]
        artifact = json.loads(path.read_text(encoding="utf-8"))
        artifact["started_at"] = "2026-07-22T02:00:01Z"
        artifact["finished_at"] = "2026-07-22T02:00:02Z"
        write_json(path, artifact)
        with self.assertRaisesRegex(HARNESS.HarnessError, "post-generation execution"):
            self.verify_artifacts()

    def test_verify_artifacts_rejects_quality_timestamp_tie_in_plan_order(self) -> None:
        self.create_freeze_commit()
        plan = self.create_plan()
        self.create_complete_artifacts(plan)
        first_path = self.plan_path.parent / plan["quality_units"][0]["artifact_path"]
        second_path = self.plan_path.parent / plan["quality_units"][1]["artifact_path"]
        first = json.loads(first_path.read_text(encoding="utf-8"))
        second = json.loads(second_path.read_text(encoding="utf-8"))
        second["started_at"] = first["finished_at"]
        second["finished_at"] = "2026-07-22T02:01:02Z"
        write_json(second_path, second)
        with self.assertRaisesRegex(HARNESS.HarnessError, "exact frozen plan order"):
            self.verify_artifacts()

    def test_verify_artifacts_rejects_quality_input_envelope_mapping_field(self) -> None:
        self.create_freeze_commit()
        plan = self.create_plan()
        self.create_complete_artifacts(plan)
        unit = plan["quality_units"][0]
        path = self.plan_path.parent / unit["artifact_path"]
        artifact = json.loads(path.read_text(encoding="utf-8"))
        artifact["input_envelope"]["model_visible_absence"][
            "condition_labels_absent"
        ] = False
        write_json(path, artifact)
        with self.assertRaisesRegex(HARNESS.HarnessError, "quality retained input envelope"):
            self.verify_artifacts()

    def test_verify_artifacts_rejects_structure_audit_input_envelope_drift(self) -> None:
        self.create_freeze_commit()
        plan = self.create_plan()
        self.create_complete_artifacts(plan)
        unit = next(
            item
            for item in plan["condition_audit_units"]
            if item["audit_mode"] == "structure-only"
        )
        path = self.plan_path.parent / unit["artifact_path"]
        artifact = json.loads(path.read_text(encoding="utf-8"))
        artifact["input_envelope"]["case"]["case_prompt_absent"] = False
        write_json(path, artifact)
        with self.assertRaisesRegex(HARNESS.HarnessError, "audit retained input envelope"):
            self.verify_artifacts()

    def test_verify_artifacts_rejects_full_audit_candidate_envelope_drift(self) -> None:
        self.create_freeze_commit()
        plan = self.create_plan()
        self.create_complete_artifacts(plan)
        unit = next(
            item
            for item in plan["condition_audit_units"]
            if item["audit_mode"] == "full-response"
        )
        path = self.plan_path.parent / unit["artifact_path"]
        artifact = json.loads(path.read_text(encoding="utf-8"))
        artifact["input_envelope"]["candidates"]["sha256"]["A"] = "0" * 64
        write_json(path, artifact)
        with self.assertRaisesRegex(HARNESS.HarnessError, "audit retained input envelope"):
            self.verify_artifacts()

    def test_complete_matrix_is_verified_but_never_claimed_as_release_pass(self) -> None:
        self.create_freeze_commit()
        plan = self.create_plan()
        self.create_complete_artifacts(plan)
        result = self.verify_artifacts()
        self.assertTrue(result["supported_artifact_matrix_complete"])
        self.assertFalse(result["evaluation_matrix_complete"])
        self.assertFalse(result["adjudication_complete"])
        self.assertFalse(result["final_score_resolution_complete"])
        self.assertTrue(result["quality_input_envelopes_complete"])
        self.assertTrue(result["condition_audit_input_envelopes_complete"])
        self.assertFalse(result["input_envelope_proof"]["host_receipt_exactness_proven"])
        self.assertEqual(result["release_gate"], "not-evaluated")
        self.assertFalse(result["release_claim_supported"])
        self.assertIn(
            "dimension_and_hard_gate_adjudication",
            result["unsupported_release_components"],
        )
        self.assertIn("final_score_resolution", result["unsupported_release_components"])
        self.assertIn("full_statistical_aggregation", result["unsupported_release_components"])

    def test_confirmed_skilled_hard_gate_failure_fails_release_gate(self) -> None:
        self.create_freeze_commit()
        plan = self.create_plan()
        self.create_complete_artifacts(plan, failed_all_gates=True)
        result = self.verify_artifacts()
        self.assertEqual(result["release_gate"], "failed")
        self.assertIn("confirmed_skilled_hard_gate_failure", result["release_failures"])
        self.assertTrue(result["confirmed_skilled_hard_gate_failures"])


if __name__ == "__main__":
    unittest.main()
