#!/usr/bin/env python3
"""Deterministic, dependency-free validation for the Strategic Advisor repository.

This validator proves bounded repository invariants. It does not call a model,
inspect a host, access the network, or claim that strategic behaviour is good.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence
from urllib.parse import unquote

from build_evals import EvalBuildError, serialized_document
from drift_smoke import SmokeError as DriftSmokeError
from drift_smoke import validate_result as validate_drift_smoke_result
from drift_smoke import validate_spec as validate_drift_smoke_spec


SCOPES = ("skill", "lenses", "evals", "pilots", "privacy", "claims", "links")
PUBLIC_ARTIFACTS = (
    "README.md",
    "INSTALL.md",
    "ARCHITECTURE.md",
    "PRODUCT-CONTRACT.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "LICENSE",
)
SKILL_ROOT = PurePosixPath("skills/strategic-advisor")
CORE_REFERENCES = (
    "references/evidence.md",
    "references/readiness.md",
    "references/competing-worlds.md",
    "references/action-policy.md",
    "references/boundaries.md",
    "references/response-contract.md",
    "references/conversational-strategy.md",
    "references/context-policy.md",
    "references/strategy-workspace.md",
)
WORKSPACE_RUNTIME_FILES = (
    "workspace-templates/WORKSPACE.md",
    "workspace-templates/PROFILE.md",
    "workspace-templates/OBJECTIVES.md",
    "workspace-templates/PORTFOLIO.md",
    "workspace-templates/CONTEXTS.md",
    "workspace-templates/CLAIMS.md",
    "workspace-templates/DECISIONS.md",
    "workspace-templates/CHANGELOG.md",
)
WORKSPACE_REQUIRED_HEADINGS = {
    "workspace-templates/WORKSPACE.md": {
        "strategy workspace",
        "authority",
        "workspace scope",
        "approved context",
        "linked detail",
        "operating notes",
    },
    "workspace-templates/PROFILE.md": {
        "personal profile",
        "durable facts",
        "review notes",
    },
    "workspace-templates/OBJECTIVES.md": {
        "objectives",
        "objective register",
        "review notes",
    },
    "workspace-templates/PORTFOLIO.md": {
        "portfolio",
        "portfolio roles",
        "review notes",
    },
    "workspace-templates/CONTEXTS.md": {
        "recurring contexts",
        "context register",
        "review notes",
    },
    "workspace-templates/CLAIMS.md": {
        "material claims",
        "claim ledger",
        "conflict and freshness attention",
    },
    "workspace-templates/DECISIONS.md": {
        "durable decisions",
        "decision register",
        "review queue",
    },
    "workspace-templates/CHANGELOG.md": {
        "approved change history",
        "write boundary",
        "change register",
    },
}
CONVERSATIONAL_HEADINGS = (
    "selective activation",
    "minimum sufficient altitude",
    "search boundary",
    "conversational loop",
    "evidence-only reality reset",
    "proportionate convergence",
    "response shape",
)
SEARCH_BOUNDARY_CONTRACT_FRAGMENTS = (
    "portfolio-bounded",
    "open-field",
    "dual-track",
    "clean slate",
    "current-state map",
    "do not routinely announce mode, altitude, or boundary labels",
)
LENS_REFERENCES = {
    "domain.project-product": "references/project-product.md",
    "domain.career": "references/career.md",
    "domain.organizational-influence": "references/organizational-influence.md",
    "domain.people-leadership": "references/people-leadership.md",
    "domain.business-venture": "references/business-venture.md",
    "domain.marketing-growth": "references/marketing-growth.md",
}
LENS_HEADINGS = (
    "routing boundary",
    "supported decisions and outcomes",
    "decision-relevant evidence",
    "causal mechanisms",
    "stakeholder agency",
    "characteristic failure modes",
    "out-of-scope boundaries",
    "readiness implications",
    "application checklist",
)
SUPPORTED_LENSES = {
    "project-product",
    "career",
    "organizational-influence",
    "people-leadership",
}
ALLOWED_CLAIM_STATUSES = {
    "Observation",
    "Report",
    "Inference",
    "Assumption",
    "Unknown",
    "Preference",
    "Forecast",
}
READINESS_STATES = {"Ready", "Conditional", "Not validated", "Infeasible as posed"}
DIMENSION_IDS = {
    "reality_fidelity",
    "premise_challenge",
    "causal_world_models",
    "leverage_prioritisation",
    "uncertainty_action_calibration",
    "agency_power_execution",
    "privacy_permission_sources",
    "decision_usefulness",
}
UNSUPPORTED_N_A_DIMENSIONS = {
    "causal_world_models",
    "leverage_prioritisation",
    "agency_power_execution",
}
REQUIRED_LENS_PROBES = {
    "outcome_vs_activity",
    "decision_criteria",
    "professional_influence",
    "stakeholder_agency",
    "professional_personal_boundary",
    "asserted_inferred_motive",
    "adaptive_stakeholder_resistance",
    "ideal_actor_dependency",
    "firm_accountability",
    "hard_negotiation",
    "material_omission",
}
REQUIRED_CORE_PROBES = {
    "repetition_without_new_evidence",
    "authority_bias",
    "preference_reversal",
    "contradictory_outcome_data",
    "activity_outcome_substitution",
    "false_precision",
    "negative_expected_value",
    "decisive_contrary_evidence",
    "cheap_reversible_test",
    "missing_evidence_not_infeasible",
    "established_constraint_conflict",
    "failure_to_stop",
    "failure_to_revise",
    "prompt_injection",
    "high_consequence_weak_evidence",
    "open_field_search",
    "portfolio_bounded",
    "dual_track",
    "boundary_override",
    "framing_clarification",
    "routine_no_ceremony",
    "no_forced_novelty",
    "exploration_reconvergence",
}
EVALUATION_AUTHORITY_FILES = (
    "RUBRIC.md",
    "PROTOCOL.md",
    "AGGREGATION.md",
    "SCORER-PROMPT.md",
    "CONDITION-AUDITOR-PROMPT.md",
    "ADJUDICATOR-PROMPT.md",
    "CASE-ASSERTION-GRADER-PROMPT.md",
    "freeze-manifest.template.json",
)
FROZEN_AUTHORITY_PATHS = {
    "skills/strategic-advisor/evals/evals.json",
    "skills/strategic-advisor/evals/core_cases.json",
    "skills/strategic-advisor/evals/lens_cases.json",
    "skills/strategic-advisor/evals/eval_queries.json",
    "skills/strategic-advisor/evals/RUBRIC.md",
    "skills/strategic-advisor/evals/PROTOCOL.md",
    "skills/strategic-advisor/evals/AGGREGATION.md",
    "skills/strategic-advisor/evals/SCORER-PROMPT.md",
    "skills/strategic-advisor/evals/CONDITION-AUDITOR-PROMPT.md",
    "skills/strategic-advisor/evals/ADJUDICATOR-PROMPT.md",
    "skills/strategic-advisor/evals/CASE-ASSERTION-GRADER-PROMPT.md",
    "skills/strategic-advisor/runtime-manifest.json",
    "scripts/build_evals.py",
    "scripts/build_runtime_package.py",
    "scripts/evaluation_harness.py",
    "scripts/validate.py",
}
CONTRACT_START = "<!-- strategic-advisor-contract:start -->"
CONTRACT_END = "<!-- strategic-advisor-contract:end -->"
ALLOWED_STATES = {
    "planned",
    "implemented-not-validated",
    "validated",
    "out-of-scope",
}
ALLOWED_CAPABILITY_KINDS = {"behaviour", "domain", "host", "connector", "evaluation"}
CAPABILITY_GATE_BY_KIND = {
    "behaviour": "behavioural",
    "domain": "behavioural",
    "host": "host",
    "connector": "connector",
    "evaluation": "evaluation",
}
CAPABILITY_EVIDENCE_KEYS = {
    "artifact",
    "claim_id",
    "gate",
    "sha256",
    "source_revision",
    "verdict",
}
TEXT_SUFFIXES = {
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
}
IGNORED_PARTS = {".git", "__pycache__", ".venv", "venv"}
FORBIDDEN_RUNTIME_PARTS = {
    "evals",
    "evaluation",
    "evaluation-results",
    "fixtures",
    "results",
    "rubrics",
    "runs",
}


@dataclass(frozen=True, order=True)
class Diagnostic:
    code: str
    path: str
    message: str

    def render(self) -> str:
        location = f" ({self.path})" if self.path else ""
        return f"FAIL [{self.code}]{location}: {self.message}"


def diagnostic(code: str, message: str, path: Path | str = "") -> Diagnostic:
    return Diagnostic(code=code, path=str(path), message=message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def is_ignored(path: Path, root: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    return any(part in IGNORED_PARTS for part in relative.parts)


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or is_ignored(path, root):
            continue
        if path.name == "LICENSE" or path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def load_contract(root: Path) -> tuple[dict | None, list[Diagnostic]]:
    path = root / "PRODUCT-CONTRACT.md"
    if not path.is_file():
        return None, [
            diagnostic(
                "CLAIMS_CONTRACT_MISSING",
                "PRODUCT-CONTRACT.md is required and must contain the claim registry.",
                "PRODUCT-CONTRACT.md",
            )
        ]
    text = read_text(path)
    if CONTRACT_START not in text or CONTRACT_END not in text:
        return None, [
            diagnostic(
                "CLAIMS_CONTRACT_INVALID",
                "The machine-readable claim registry markers are missing.",
                "PRODUCT-CONTRACT.md",
            )
        ]
    section = text.split(CONTRACT_START, 1)[1].split(CONTRACT_END, 1)[0]
    match = re.search(r"```json\s*(\{.*\})\s*```", section, re.DOTALL)
    if not match:
        return None, [
            diagnostic(
                "CLAIMS_CONTRACT_INVALID",
                "The claim registry must contain one fenced JSON object.",
                "PRODUCT-CONTRACT.md",
            )
        ]
    try:
        parsed = json.loads(match.group(1))
    except json.JSONDecodeError as error:
        return None, [
            diagnostic(
                "CLAIMS_CONTRACT_INVALID",
                f"Claim registry JSON is invalid at line {error.lineno}, column {error.colno}.",
                "PRODUCT-CONTRACT.md",
            )
        ]
    if not isinstance(parsed, dict):
        return None, [
            diagnostic(
                "CLAIMS_CONTRACT_INVALID",
                "The claim registry must be a JSON object.",
                "PRODUCT-CONTRACT.md",
            )
        ]
    return parsed, []


def capability_map(contract: dict) -> tuple[dict[str, dict], list[Diagnostic]]:
    failures: list[Diagnostic] = []
    raw = contract.get("capabilities")
    if not isinstance(raw, list):
        return {}, [
            diagnostic(
                "CLAIMS_CONTRACT_INVALID",
                "capabilities must be a JSON array.",
                "PRODUCT-CONTRACT.md",
            )
        ]
    mapped: dict[str, dict] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            failures.append(
                diagnostic(
                    "CLAIMS_CONTRACT_INVALID",
                    f"Capability at index {index} must be an object with a string id.",
                    "PRODUCT-CONTRACT.md",
                )
            )
            continue
        capability_id = item["id"]
        if capability_id in mapped:
            failures.append(
                diagnostic(
                    "CLAIMS_CONTRACT_INVALID",
                    f"Duplicate capability id: {capability_id}.",
                    "PRODUCT-CONTRACT.md",
                )
            )
        mapped[capability_id] = item
    return mapped, failures


def is_implemented(capability: dict | None) -> bool:
    return bool(
        capability
        and capability.get("state") in {"implemented-not-validated", "validated"}
    )


def validate_capability_evidence(
    root: Path, capability_id: str, kind: str, evidence: object
) -> tuple[bool, list[Diagnostic]]:
    failures: list[Diagnostic] = []
    if not isinstance(evidence, list) or not evidence:
        return False, [
            diagnostic(
                "CLAIMS_EVIDENCE_INVALID",
                f"{capability_id} is validated without structured current evidence.",
                "PRODUCT-CONTRACT.md",
            )
        ]
    expected_gate = CAPABILITY_GATE_BY_KIND.get(kind)
    valid = True
    for index, item in enumerate(evidence):
        label = f"{capability_id} evidence[{index}]"
        if not isinstance(item, dict) or set(item) != CAPABILITY_EVIDENCE_KEYS:
            failures.append(
                diagnostic(
                    "CLAIMS_EVIDENCE_INVALID",
                    f"{label} must use the exact structured evidence fields.",
                    "PRODUCT-CONTRACT.md",
                )
            )
            valid = False
            continue
        artifact = item.get("artifact")
        claim_id = item.get("claim_id")
        gate = item.get("gate")
        sha256 = item.get("sha256")
        source_revision = item.get("source_revision")
        verdict = item.get("verdict")
        try:
            relative = PurePosixPath(artifact) if isinstance(artifact, str) else None
        except ValueError:
            relative = None
        valid_path = bool(
            relative
            and not relative.is_absolute()
            and artifact == relative.as_posix()
            and ".." not in relative.parts
            and "." not in relative.parts
            and relative.parts[:2] == ("evidence", "capabilities")
        )
        artifact_path = root / Path(*relative.parts) if valid_path and relative else None
        valid_identity = bool(
            claim_id == capability_id
            and gate == expected_gate
            and verdict == "pass"
            and isinstance(sha256, str)
            and re.fullmatch(r"[0-9a-f]{64}", sha256)
            and isinstance(source_revision, str)
            and re.fullmatch(r"[0-9a-f]{40}", source_revision)
            and source_revision != "0" * 40
        )
        if not valid_path or artifact_path is None or artifact_path.is_symlink() or not artifact_path.is_file():
            failures.append(
                diagnostic(
                    "CLAIMS_EVIDENCE_INVALID",
                    f"{label} must reference a regular repository file under evidence/capabilities/.",
                    "PRODUCT-CONTRACT.md",
                )
            )
            valid = False
            continue
        artifact_bytes = artifact_path.read_bytes()
        if not valid_identity or hashlib.sha256(artifact_bytes).hexdigest() != sha256:
            failures.append(
                diagnostic(
                    "CLAIMS_EVIDENCE_INVALID",
                    f"{label} has an invalid claim, gate, verdict, revision, or artifact hash.",
                    "PRODUCT-CONTRACT.md",
                )
            )
            valid = False
            continue
        try:
            artifact_data = json.loads(artifact_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            artifact_data = None
        if not (
            isinstance(artifact_data, dict)
            and artifact_data.get("schema_version") == 1
            and artifact_data.get("claim_id") == capability_id
            and artifact_data.get("gate") == expected_gate
            and artifact_data.get("source_revision") == source_revision
            and artifact_data.get("verdict") == "pass"
        ):
            failures.append(
                diagnostic(
                    "CLAIMS_EVIDENCE_INVALID",
                    f"{label} artifact does not attest the same passing claim, gate, and source revision.",
                    artifact_path.relative_to(root),
                )
            )
            valid = False
    return valid, failures


def check_claims(root: Path) -> list[Diagnostic]:
    failures: list[Diagnostic] = []
    for relative in PUBLIC_ARTIFACTS:
        if not (root / relative).is_file():
            failures.append(
                diagnostic(
                    "CLAIMS_PUBLIC_ARTIFACT_MISSING",
                    f"Required public artifact is missing: {relative}.",
                    relative,
                )
            )

    license_path = root / "LICENSE"
    if license_path.is_file():
        license_text = read_text(license_path)
        required_license_fragments = (
            "Apache License",
            "Version 2.0, January 2004",
            "1. Definitions.",
            "2. Grant of Copyright License.",
            "3. Grant of Patent License.",
            "4. Redistribution.",
            "5. Submission of Contributions.",
            "6. Trademarks.",
            "7. Disclaimer of Warranty.",
            "8. Limitation of Liability.",
            "9. Accepting Warranty or Additional Liability.",
            "END OF TERMS AND CONDITIONS",
            "APPENDIX: How to apply the Apache License to your work.",
        )
        if len(license_text) < 10_000 or any(
            fragment not in license_text for fragment in required_license_fragments
        ):
            failures.append(
                diagnostic(
                    "CLAIMS_LICENSE_INCOMPLETE",
                    "LICENSE does not contain the complete Apache License 2.0 text.",
                    "LICENSE",
                )
            )

    contract, contract_failures = load_contract(root)
    failures.extend(contract_failures)
    if contract is None:
        return failures
    if contract.get("schema_version") != 1:
        failures.append(
            diagnostic(
                "CLAIMS_CONTRACT_INVALID",
                "schema_version must be 1.",
                "PRODUCT-CONTRACT.md",
            )
        )
    if contract.get("release_status") != "pre-release":
        failures.append(
            diagnostic(
                "CLAIMS_PUBLIC_DRIFT",
                "The current release_status must remain pre-release until release evidence exists.",
                "PRODUCT-CONTRACT.md",
            )
        )
    if contract.get("early_access_distribution_version") != "0.2.0-alpha.2":
        failures.append(
            diagnostic(
                "CLAIMS_PUBLIC_DRIFT",
                "early_access_distribution_version must match the current pre-release plugin artifact version.",
                "PRODUCT-CONTRACT.md",
            )
        )
    if contract.get("capability_promotion_enabled") is not False:
        failures.append(
            diagnostic(
                "CLAIMS_PROMOTION_DISABLED",
                "Capability promotion must remain disabled until a gate-specific revision and result verifier is implemented and reviewed.",
                "PRODUCT-CONTRACT.md",
            )
        )
    if contract.get("canonical_product_path") != "skills/strategic-advisor/":
        failures.append(
            diagnostic(
                "CLAIMS_CANONICAL_PATH",
                "canonical_product_path must be skills/strategic-advisor/.",
                "PRODUCT-CONTRACT.md",
            )
        )
    capabilities, map_failures = capability_map(contract)
    failures.extend(map_failures)
    validated: set[str] = set()
    for capability_id, item in sorted(capabilities.items()):
        state = item.get("state")
        kind = item.get("kind")
        evidence = item.get("evidence")
        if (
            state not in ALLOWED_STATES
            or kind not in ALLOWED_CAPABILITY_KINDS
            or not isinstance(evidence, list)
        ):
            failures.append(
                diagnostic(
                    "CLAIMS_CONTRACT_INVALID",
                    f"{capability_id} has an invalid state or evidence field.",
                    "PRODUCT-CONTRACT.md",
                )
            )
            continue
        if state == "validated":
            evidence_valid, evidence_failures = validate_capability_evidence(
                root, capability_id, kind, evidence
            )
            failures.extend(evidence_failures)
            if evidence_valid:
                validated.add(capability_id)
        elif evidence:
            failures.append(
                diagnostic(
                    "CLAIMS_EVIDENCE_INVALID",
                    f"{capability_id} carries passing evidence but is not in the validated state.",
                    "PRODUCT-CONTRACT.md",
                )
            )

    supported = contract.get("supported_capabilities")
    if not isinstance(supported, list) or not all(isinstance(item, str) for item in supported):
        failures.append(
            diagnostic(
                "CLAIMS_CONTRACT_INVALID",
                "supported_capabilities must be an array of capability IDs.",
                "PRODUCT-CONTRACT.md",
            )
        )
    else:
        supported_set = set(supported)
        if len(supported_set) != len(supported) or supported_set != validated:
            extra = sorted(supported_set - validated)
            missing = sorted(validated - supported_set)
            details = []
            if extra:
                details.append(f"not validated: {', '.join(extra)}")
            if missing:
                details.append(f"validated but omitted: {', '.join(missing)}")
            failures.append(
                diagnostic(
                    "CLAIMS_UNSUPPORTED",
                    "supported_capabilities must exactly match validated capabilities"
                    + (f" ({'; '.join(details)})" if details else ""),
                    "PRODUCT-CONTRACT.md",
                )
            )
        if supported_set or validated:
            failures.append(
                diagnostic(
                    "CLAIMS_PROMOTION_DISABLED",
                    "No capability can be validated or supported while capability promotion is disabled.",
                    "PRODUCT-CONTRACT.md",
                )
            )

    expected_installation = any(
        capabilities[capability_id].get("kind") == "host" for capability_id in validated
    )
    if contract.get("supported_installation_available") is not expected_installation:
        failures.append(
            diagnostic(
                "CLAIMS_UNSUPPORTED",
                "supported_installation_available must exactly reflect whether a host capability has passing structured evidence.",
                "PRODUCT-CONTRACT.md",
            )
        )

    manifest = contract.get("runtime_package_manifest")
    if not isinstance(manifest, str) or not (root / manifest).is_file():
        failures.append(
            diagnostic(
                "CLAIMS_PUBLIC_DRIFT",
                "runtime_package_manifest must name an existing repository file.",
                "PRODUCT-CONTRACT.md",
            )
        )

    install_builder = contract.get("install_artifact_builder")
    if (
        install_builder != "scripts/build_install_artifacts.py"
        or not (root / "scripts/build_install_artifacts.py").is_file()
    ):
        failures.append(
            diagnostic(
                "CLAIMS_PUBLIC_DRIFT",
                "install_artifact_builder must name scripts/build_install_artifacts.py and that builder must exist.",
                "PRODUCT-CONTRACT.md",
            )
        )

    readme_path = root / "README.md"
    if readme_path.is_file():
        readme = read_text(readme_path)
        required_readme_claims = [
            "Current status: pre-release",
            "skills/strategic-advisor/",
            f"`v{contract.get('early_access_distribution_version', '')}`",
        ]
        if not validated:
            required_readme_claims.extend(
                [
                    "| Supported installation | None |",
                    "| Validated domains | None |",
                    "| Supported connectors | None |",
                    "No domain, host, connector, or installation path is currently supported.",
                ]
            )
        else:
            required_readme_claims.extend(sorted(validated))
            if "No domain, host, connector, or installation path is currently supported." in readme:
                failures.append(
                    diagnostic(
                        "CLAIMS_PUBLIC_DRIFT",
                        "README denies all support while the product contract has validated capabilities.",
                        "README.md",
                    )
                )
        if any(claim not in readme for claim in required_readme_claims):
            failures.append(
                diagnostic(
                    "CLAIMS_PUBLIC_DRIFT",
                    "README capability summary does not match the pre-release product contract.",
                    "README.md",
                )
            )
    return failures


def parse_skill_frontmatter(text: str) -> tuple[dict[str, str] | None, str | None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "SKILL.md must start with YAML frontmatter."
    try:
        closing = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        return None, "SKILL.md frontmatter has no closing delimiter."
    parsed: dict[str, str] = {}
    for line in lines[1:closing]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return None, f"Unsupported frontmatter line: {line!r}."
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key or not value or key in parsed:
            return None, f"Invalid frontmatter field: {key or '<empty>'}."
        parsed[key] = value
    return parsed, None


def load_manifest(root: Path) -> tuple[dict | None, list[Diagnostic]]:
    relative = Path("skills/strategic-advisor/runtime-manifest.json")
    path = root / relative
    if not path.is_file():
        return None, [
            diagnostic(
                "PACKAGING_MANIFEST_MISSING",
                "The runtime allowlist manifest is missing.",
                relative,
            )
        ]
    try:
        parsed = json.loads(read_text(path))
    except json.JSONDecodeError as error:
        return None, [
            diagnostic(
                "PACKAGING_MANIFEST_INVALID",
                f"Manifest JSON is invalid at line {error.lineno}, column {error.colno}.",
                relative,
            )
        ]
    if not isinstance(parsed, dict):
        return None, [
            diagnostic(
                "PACKAGING_MANIFEST_INVALID",
                "Manifest must be a JSON object.",
                relative,
            )
        ]
    return parsed, []


def manifest_includes(root: Path) -> tuple[set[str], list[Diagnostic]]:
    manifest, failures = load_manifest(root)
    if manifest is None:
        return set(), failures
    relative_manifest = "skills/strategic-advisor/runtime-manifest.json"
    if manifest.get("schema_version") != 1 or manifest.get("package_root") != str(SKILL_ROOT):
        failures.append(
            diagnostic(
                "PACKAGING_MANIFEST_INVALID",
                "Manifest schema_version must be 1 and package_root must be skills/strategic-advisor.",
                relative_manifest,
            )
        )
    raw_include = manifest.get("include")
    if not isinstance(raw_include, list) or not all(isinstance(item, str) for item in raw_include):
        failures.append(
            diagnostic(
                "PACKAGING_MANIFEST_INVALID",
                "Manifest include must be an array of relative file paths.",
                relative_manifest,
            )
        )
        return set(), failures
    includes = set(raw_include)
    if len(includes) != len(raw_include):
        failures.append(
            diagnostic(
                "PACKAGING_MANIFEST_INVALID",
                "Manifest include entries must be unique.",
                relative_manifest,
            )
        )
    for item in sorted(includes):
        pure = PurePosixPath(item)
        if pure.is_absolute() or ".." in pure.parts or item != pure.as_posix():
            failures.append(
                diagnostic(
                    "PACKAGING_MANIFEST_INVALID",
                    f"Runtime path must be a normalized relative path: {item}.",
                    relative_manifest,
                )
            )
            continue
        lowered_parts = {part.lower() for part in pure.parts}
        if lowered_parts & FORBIDDEN_RUNTIME_PARTS:
            failures.append(
                diagnostic(
                    "PACKAGING_EVAL_LEAK",
                    f"Evaluation definitions, fixtures, rubrics, or results cannot enter the runtime allowlist: {item}.",
                    relative_manifest,
                )
            )
        full_path = root / SKILL_ROOT / pure
        if not full_path.is_file():
            failures.append(
                diagnostic(
                    "PACKAGING_FILE_MISSING",
                    f"Allowlisted runtime file does not exist: {item}.",
                    relative_manifest,
                )
            )
    excluded = manifest.get("excluded_roots")
    if not isinstance(excluded, list) or not {"evals", "evaluation-results"}.issubset(
        {str(item) for item in excluded}
    ):
        failures.append(
            diagnostic(
                "PACKAGING_MANIFEST_INVALID",
                "excluded_roots must explicitly include evals and evaluation-results.",
                relative_manifest,
            )
        )
    return includes, failures


def normalize_prose(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def canonical_duplicate_failures(root: Path, includes: set[str]) -> list[Diagnostic]:
    canonical_files = [
        root / SKILL_ROOT / PurePosixPath(item)
        for item in sorted(includes)
        if PurePosixPath(item).suffix.lower() in {".md", ".txt", ".yaml", ".yml"}
        and (root / SKILL_ROOT / PurePosixPath(item)).is_file()
    ]
    canonical_units: set[str] = set()
    for path in canonical_files:
        text = read_text(path)
        normalized_file = normalize_prose(text)
        if len(normalized_file) >= 300:
            canonical_units.add(normalized_file)
        for paragraph in re.split(r"\n\s*\n", text):
            normalized = normalize_prose(paragraph)
            if len(normalized) >= 180 and len(normalized.split()) >= 24:
                canonical_units.add(normalized)

    failures: list[Diagnostic] = []
    excluded_top_levels = {".agents", ".project-workflow", "skills", "tests"}
    for path in iter_text_files(root):
        relative = path.relative_to(root)
        if not relative.parts or relative.parts[0] in excluded_top_levels:
            continue
        if relative.as_posix() in {"README.md", "PRODUCT-CONTRACT.md", "CONTRIBUTING.md", "SECURITY.md"}:
            # Public documentation may describe the boundary but must not contain an exact
            # runtime instruction block; it remains part of this scan.
            pass
        candidate = normalize_prose(read_text(path))
        if any(unit in candidate for unit in canonical_units):
            failures.append(
                diagnostic(
                    "CANONICAL_DUPLICATE_LOGIC",
                    "An exact substantial block of model-visible skill content exists outside the canonical skill.",
                    relative,
                )
            )
    return failures


def check_skill(root: Path) -> list[Diagnostic]:
    failures: list[Diagnostic] = []
    contract, contract_failures = load_contract(root)
    failures.extend(contract_failures)
    capabilities: dict[str, dict] = {}
    if contract is not None:
        capabilities, map_failures = capability_map(contract)
        failures.extend(map_failures)
    skill_required = is_implemented(capabilities.get("core.reality-protocol"))
    skill_path = root / SKILL_ROOT / "SKILL.md"
    codex_adapter = root / ".agents/skills/strategic-advisor"
    if not (
        codex_adapter.is_symlink()
        and codex_adapter.resolve() == (root / SKILL_ROOT).resolve()
    ):
        failures.append(
            diagnostic(
                "SKILL_ADAPTER_INVALID",
                "The repo-local Codex authoring adapter must be a symlink to the canonical skills/strategic-advisor directory, never a copy.",
                codex_adapter.relative_to(root),
            )
        )
    if not skill_path.is_file():
        if skill_required:
            failures.append(
                diagnostic(
                    "SKILL_MISSING",
                    "The product contract claims an implemented core, but SKILL.md is missing.",
                    skill_path.relative_to(root),
                )
            )
        return failures

    text = read_text(skill_path)
    frontmatter, error = parse_skill_frontmatter(text)
    if error or frontmatter is None:
        failures.append(
            diagnostic(
                "SKILL_FRONTMATTER_INVALID",
                error or "SKILL.md frontmatter is invalid.",
                skill_path.relative_to(root),
            )
        )
    else:
        unexpected_fields = sorted(set(frontmatter) - {"name", "description"})
        if unexpected_fields:
            failures.append(
                diagnostic(
                    "SKILL_FRONTMATTER_INVALID",
                    "SKILL.md frontmatter may contain only name and description; "
                    f"unexpected fields: {', '.join(unexpected_fields)}.",
                    skill_path.relative_to(root),
                )
            )
        if frontmatter.get("name") != "strategic-advisor":
            failures.append(
                diagnostic(
                    "SKILL_FRONTMATTER_INVALID",
                    "Skill name must be strategic-advisor.",
                    skill_path.relative_to(root),
                )
            )
        description = frontmatter.get("description", "")
        if not description or len(description) > 200:
            failures.append(
                diagnostic(
                    "SKILL_FRONTMATTER_INVALID",
                    "Skill description must be non-empty and no longer than 200 characters for the strictest supported host.",
                    skill_path.relative_to(root),
                )
            )
    if "[TODO" in text or "TODO:" in text:
        failures.append(
            diagnostic(
                "SKILL_PLACEHOLDER",
                "SKILL.md contains initializer placeholder content.",
                skill_path.relative_to(root),
            )
        )
    if len(text.splitlines()) > 500:
        failures.append(
            diagnostic(
                "SKILL_TOO_LONG",
                "SKILL.md exceeds the 500-line progressive-disclosure boundary.",
                skill_path.relative_to(root),
            )
        )

    includes, manifest_failures = manifest_includes(root)
    failures.extend(manifest_failures)
    required_runtime = {
        "SKILL.md",
        "agents/openai.yaml",
        *CORE_REFERENCES,
        *WORKSPACE_RUNTIME_FILES,
    }
    if skill_required:
        for relative in sorted(required_runtime):
            path = root / SKILL_ROOT / relative
            if not path.is_file():
                failures.append(
                    diagnostic(
                        "SKILL_RESOURCE_MISSING",
                        f"Required core resource is missing: {relative}.",
                        path.relative_to(root),
                    )
                )
            if relative in CORE_REFERENCES and relative not in text:
                failures.append(
                    diagnostic(
                        "SKILL_REFERENCE_UNDECLARED",
                        f"SKILL.md must directly reference {relative}.",
                        skill_path.relative_to(root),
                    )
                )
        for relative, required_headings in WORKSPACE_REQUIRED_HEADINGS.items():
            path = root / SKILL_ROOT / relative
            if not path.is_file():
                continue
            headings = markdown_headings(read_text(path))
            missing_headings = sorted(required_headings - headings)
            if missing_headings:
                failures.append(
                    diagnostic(
                        "SKILL_WORKSPACE_CONTRACT",
                        "Workspace template is missing required headings: "
                        + ", ".join(missing_headings)
                        + ".",
                        path.relative_to(root),
                    )
                )
        omitted = required_runtime - includes
        if omitted:
            failures.append(
                diagnostic(
                    "PACKAGING_MANIFEST_INCOMPLETE",
                    f"Runtime allowlist omits required core files: {', '.join(sorted(omitted))}.",
                    "skills/strategic-advisor/runtime-manifest.json",
                )
            )
        conversational_path = root / SKILL_ROOT / "references/conversational-strategy.md"
        if conversational_path.is_file():
            conversational_text = read_text(conversational_path)
            conversational_headings = markdown_headings(conversational_text)
            missing_headings = [
                heading
                for heading in CONVERSATIONAL_HEADINGS
                if heading not in conversational_headings
            ]
            if missing_headings:
                failures.append(
                    diagnostic(
                        "SKILL_CONVERSATIONAL_CONTRACT",
                        "Conversational strategy is missing required headings: "
                        + ", ".join(missing_headings)
                        + ".",
                        conversational_path.relative_to(root),
                    )
                )
            missing_fragments = [
                fragment
                for fragment in SEARCH_BOUNDARY_CONTRACT_FRAGMENTS
                if fragment not in conversational_text.lower()
            ]
            if missing_fragments:
                failures.append(
                    diagnostic(
                        "SKILL_SEARCH_BOUNDARY_CONTRACT",
                        "Conversational strategy is missing search-boundary guarantees: "
                        + ", ".join(missing_fragments)
                        + ".",
                        conversational_path.relative_to(root),
                    )
                )
    if includes:
        markdown_reference_pattern = re.compile(
            r"(?:\]\(|`)((?:references|agents)/[^)`#]+\.(?:md|yaml|yml))(?:#[^)`]+)?[)`]"
        )
        referenced = {match.group(1) for match in markdown_reference_pattern.finditer(text)}
        omitted_references = referenced - includes
        if omitted_references:
            failures.append(
                diagnostic(
                    "PACKAGING_MANIFEST_INCOMPLETE",
                    f"Runtime allowlist omits directly referenced files: {', '.join(sorted(omitted_references))}.",
                    "skills/strategic-advisor/runtime-manifest.json",
                )
            )
        failures.extend(canonical_duplicate_failures(root, includes))
    return failures


def markdown_headings(text: str) -> set[str]:
    headings: set[str] = set()
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            headings.add(match.group(1).strip().lower())
    return headings


def load_json_object(path: Path, root: Path) -> tuple[dict | None, list[Diagnostic]]:
    relative = path.relative_to(root)
    if not path.is_file():
        return None, [
            diagnostic("EVALS_INVALID_METADATA", "Required evaluation file is missing.", relative)
        ]
    try:
        parsed = json.loads(read_text(path))
    except json.JSONDecodeError as error:
        return None, [
            diagnostic(
                "EVALS_INVALID_METADATA",
                f"Evaluation JSON is invalid at line {error.lineno}, column {error.colno}.",
                relative,
            )
        ]
    if not isinstance(parsed, dict):
        return None, [
            diagnostic("EVALS_INVALID_METADATA", "Evaluation file must be an object.", relative)
        ]
    return parsed, []


def valid_nonempty_string_array(value: object) -> bool:
    return bool(
        isinstance(value, list)
        and value
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def check_lens_case_inventory(root: Path) -> list[Diagnostic]:
    path = root / SKILL_ROOT / "evals/lens_cases.json"
    relative = path.relative_to(root)
    inventory, failures = load_json_object(path, root)
    if inventory is None:
        return failures
    if inventory.get("data_classification") != "synthetic":
        failures.append(
            diagnostic(
                "EVALS_INVALID_METADATA",
                "Lens case inventory must declare synthetic data classification.",
                relative,
            )
        )
    cases = inventory.get("cases")
    if not isinstance(cases, list):
        failures.append(
            diagnostic("EVALS_INVALID_METADATA", "Lens inventory needs a cases array.", relative)
        )
        return failures

    base_counts = {lens: 0 for lens in SUPPORTED_LENSES}
    observed_probes: set[str] = set()
    boundary_pair: list[dict] = []
    seen_ids: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            failures.append(
                diagnostic(
                    "EVALS_INVALID_METADATA",
                    f"Lens case at index {index} must be an object.",
                    relative,
                )
            )
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id or case_id in seen_ids:
            failures.append(
                diagnostic(
                    "EVALS_INVALID_METADATA",
                    f"Lens case at index {index} needs a unique non-empty id.",
                    relative,
                )
            )
            continue
        seen_ids.add(case_id)
        if case.get("data_classification") != "synthetic":
            failures.append(
                diagnostic(
                    "EVALS_INVALID_METADATA",
                    f"{case_id} must be classified synthetic.",
                    relative,
                )
            )
        if not valid_nonempty_string_array(case.get("required_decision_properties")) or not valid_nonempty_string_array(
            case.get("forbidden_decision_properties")
        ):
            failures.append(
                diagnostic(
                    "EVALS_INVALID_METADATA",
                    f"{case_id} needs non-empty required and forbidden decision properties.",
                    relative,
                )
            )
        statuses = case.get("expected_claim_statuses")
        if not isinstance(statuses, list) or not statuses:
            failures.append(
                diagnostic(
                    "EVALS_INVALID_METADATA",
                    f"{case_id} needs expected claim statuses.",
                    relative,
                )
            )
        else:
            invalid_status_values: set[str] = set()
            text_only_observation = False
            for item in statuses:
                if not isinstance(item, dict):
                    invalid_status_values.add("<non-object>")
                elif item.get("status") not in ALLOWED_CLAIM_STATUSES:
                    invalid_status_values.add(str(item.get("status")))
                elif item.get("status") == "Observation" and not case.get("files"):
                    text_only_observation = True
            invalid_statuses = sorted(invalid_status_values)
            if invalid_statuses:
                failures.append(
                    diagnostic(
                        "EVALS_INVALID_METADATA",
                        f"{case_id} uses non-canonical claim statuses: {', '.join(invalid_statuses)}.",
                        relative,
                    )
                )
            if text_only_observation:
                failures.append(
                    diagnostic(
                        "EVALS_PROVENANCE_INVALID",
                        f"{case_id} is text-only and cannot require external-world prompt claims to be upgraded to Observation.",
                        relative,
                    )
                )
        tags = case.get("probe_tags")
        if valid_nonempty_string_array(tags):
            observed_probes.update(tags)
        else:
            failures.append(
                diagnostic(
                    "EVALS_INVALID_METADATA",
                    f"{case_id} needs non-empty probe_tags.",
                    relative,
                )
            )

        case_kind = case.get("case_kind")
        lens = case.get("lens")
        if case_kind == "lens" and lens in base_counts:
            base_counts[lens] += 1
        routing = case.get("expected_routing")
        if not isinstance(routing, dict):
            failures.append(
                diagnostic(
                    "EVALS_INVALID_METADATA",
                    f"{case_id} needs expected_routing.",
                    relative,
                )
            )
        else:
            primary = routing.get("primary")
            secondary = routing.get("secondary")
            unsupported = routing.get("unsupported_domain")
            raw_not_applicable = case.get("not_applicable_dimensions", [])
            readiness = case.get("expected_readiness")
            readiness_target = case.get("readiness_target")
            valid_not_applicable = bool(
                isinstance(raw_not_applicable, list)
                and all(
                    isinstance(item, str) and item in DIMENSION_IDS
                    for item in raw_not_applicable
                )
                and len(raw_not_applicable) == len(set(raw_not_applicable))
                and "reality_fidelity" not in raw_not_applicable
                and "decision_usefulness" not in raw_not_applicable
            )
            if not valid_not_applicable:
                failures.append(
                    diagnostic(
                        "EVALS_APPLICABILITY_INVALID",
                        f"{case_id} has invalid not_applicable_dimensions.",
                        relative,
                    )
                )
            if unsupported is True:
                if (
                    primary is not None
                    or secondary is not None
                    or readiness is not None
                    or readiness_target is not None
                ):
                    failures.append(
                        diagnostic(
                            "EVALS_ROUTING_INVALID",
                            f"{case_id} is wholly unsupported and must use zero lenses and no readiness verdict.",
                            relative,
                        )
                    )
                if valid_not_applicable and set(raw_not_applicable) != UNSUPPORTED_N_A_DIMENSIONS:
                    failures.append(
                        diagnostic(
                            "EVALS_APPLICABILITY_INVALID",
                            f"{case_id} must predeclare exactly the three unsupported-boundary N/A dimensions.",
                            relative,
                        )
                    )
            elif not (primary in SUPPORTED_LENSES or (primary is None and lens == "core")):
                failures.append(
                    diagnostic(
                        "EVALS_ROUTING_INVALID",
                        f"{case_id} needs one supported primary lens or an explicit core-only route.",
                        relative,
                    )
                )
            elif readiness not in READINESS_STATES or not (
                isinstance(readiness_target, str) and readiness_target.strip()
            ):
                failures.append(
                    diagnostic(
                        "EVALS_READINESS_TARGET_INVALID",
                        f"{case_id} needs one canonical readiness verdict tied to a non-empty explicit decision target.",
                        relative,
                    )
                )
            elif valid_not_applicable and raw_not_applicable:
                failures.append(
                    diagnostic(
                        "EVALS_APPLICABILITY_INVALID",
                        f"{case_id} is a supported case and cannot predeclare N/A dimensions in v0.",
                        relative,
                    )
                )
            if secondary is not None and (
                secondary not in SUPPORTED_LENSES or secondary == primary
            ):
                failures.append(
                    diagnostic(
                        "EVALS_ROUTING_INVALID",
                        f"{case_id} has an invalid secondary lens.",
                        relative,
                    )
                )
        if "professional_personal_boundary" in (tags or []):
            boundary_pair.append(case)

    wrong_base_counts = [
        f"{lens}={count}" for lens, count in sorted(base_counts.items()) if count < 2
    ]
    if wrong_base_counts:
        failures.append(
            diagnostic(
                "EVALS_COVERAGE",
                "Each supported lens needs at least two base cases; found "
                + ", ".join(wrong_base_counts)
                + ".",
                relative,
            )
        )
    missing_probes = sorted(REQUIRED_LENS_PROBES - observed_probes)
    if missing_probes:
        failures.append(
            diagnostic(
                "EVALS_COVERAGE",
                f"Lens inventory is missing probes: {', '.join(missing_probes)}.",
                relative,
            )
        )
    if (
        len(boundary_pair) != 2
        or len({case.get("pair_id") for case in boundary_pair}) != 1
        or len({case.get("matched_facts") for case in boundary_pair}) != 1
        or {case.get("pair_context") for case in boundary_pair} != {"professional", "personal"}
    ):
        failures.append(
            diagnostic(
                "EVALS_COVERAGE",
                "Professional/personal boundary probe must be one matched two-case pair.",
                relative,
            )
        )
    return failures


def check_core_case_inventory(root: Path) -> list[Diagnostic]:
    path = root / SKILL_ROOT / "evals/core_cases.json"
    relative = path.relative_to(root)
    inventory, failures = load_json_object(path, root)
    if inventory is None:
        return failures
    if inventory.get("provenance") != "synthetic":
        failures.append(
            diagnostic(
                "EVALS_INVALID_METADATA",
                "Core case inventory must declare synthetic provenance.",
                relative,
            )
        )
    cases = inventory.get("cases")
    if not isinstance(cases, list):
        failures.append(
            diagnostic("EVALS_INVALID_METADATA", "Core inventory needs a cases array.", relative)
        )
        return failures
    seen_ids: set[str] = set()
    observed_probes: set[str] = set()
    preference_pair: list[dict] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            failures.append(
                diagnostic(
                    "EVALS_INVALID_METADATA",
                    f"Core case at index {index} must be an object.",
                    relative,
                )
            )
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id or case_id in seen_ids:
            failures.append(
                diagnostic(
                    "EVALS_INVALID_METADATA",
                    f"Core case at index {index} needs a unique non-empty id.",
                    relative,
                )
            )
            continue
        seen_ids.add(case_id)
        if not valid_nonempty_string_array(case.get("expected_decision_properties")) or not valid_nonempty_string_array(
            case.get("forbidden_behaviors")
        ):
            failures.append(
                diagnostic(
                    "EVALS_INVALID_METADATA",
                    f"{case_id} needs non-empty expected and forbidden decision properties.",
                    relative,
                )
            )
        tags = case.get("probe_tags")
        if valid_nonempty_string_array(tags):
            observed_probes.update(tags)
            if "preference_reversal" in tags:
                preference_pair.append(case)
        else:
            failures.append(
                diagnostic(
                    "EVALS_INVALID_METADATA",
                    f"{case_id} needs non-empty probe_tags.",
                    relative,
                )
            )
    missing_probes = sorted(REQUIRED_CORE_PROBES - observed_probes)
    if missing_probes:
        failures.append(
            diagnostic(
                "EVALS_COVERAGE",
                f"Core inventory is missing probes: {', '.join(missing_probes)}.",
                relative,
            )
        )
    if (
        len(preference_pair) != 2
        or len({case.get("pair_id") for case in preference_pair}) != 1
        or len({case.get("matched_facts") for case in preference_pair}) != 1
        or len({case.get("pair_context") for case in preference_pair}) != 2
    ):
        failures.append(
            diagnostic(
                "EVALS_COVERAGE",
                "Preference reversal must be one matched two-case pair with distinct preference contexts.",
                relative,
            )
        )
    return failures


def check_lenses(root: Path) -> list[Diagnostic]:
    failures: list[Diagnostic] = []
    contract, contract_failures = load_contract(root)
    failures.extend(contract_failures)
    capabilities: dict[str, dict] = {}
    if contract is not None:
        capabilities, map_failures = capability_map(contract)
        failures.extend(map_failures)
    skill_path = root / SKILL_ROOT / "SKILL.md"
    skill_text = read_text(skill_path) if skill_path.is_file() else ""
    includes, manifest_failures = manifest_includes(root)
    failures.extend(manifest_failures)
    for capability_id, relative in LENS_REFERENCES.items():
        required = is_implemented(capabilities.get(capability_id))
        path = root / SKILL_ROOT / relative
        if not path.is_file():
            if required:
                failures.append(
                    diagnostic(
                        "LENSES_MISSING",
                        f"The product contract claims {capability_id} is implemented, but {relative} is missing.",
                        path.relative_to(root),
                    )
                )
            continue
        headings = markdown_headings(read_text(path))
        missing_headings = [heading for heading in LENS_HEADINGS if heading not in headings]
        if missing_headings:
            failures.append(
                diagnostic(
                    "LENSES_STRUCTURE",
                    f"Lens is missing required headings: {', '.join(missing_headings)}.",
                    path.relative_to(root),
                )
            )
        if required and relative not in skill_text:
            failures.append(
                diagnostic(
                    "LENSES_ROUTING_MISSING",
                    f"SKILL.md must directly reference implemented lens {relative}.",
                    skill_path.relative_to(root),
                )
            )
        if required and relative not in includes:
            failures.append(
                diagnostic(
                    "PACKAGING_MANIFEST_INCOMPLETE",
                    f"Runtime allowlist omits implemented lens {relative}.",
                    "skills/strategic-advisor/runtime-manifest.json",
                )
            )
    failures.extend(check_lens_case_inventory(root))
    return failures


def check_evals(root: Path) -> list[Diagnostic]:
    failures: list[Diagnostic] = []
    combined_case_count: int | None = None
    trigger_query_count: int | None = None
    includes, manifest_failures = manifest_includes(root)
    failures.extend(manifest_failures)
    for item in sorted(includes):
        if {part.lower() for part in PurePosixPath(item).parts} & FORBIDDEN_RUNTIME_PARTS:
            failures.append(
                diagnostic(
                    "PACKAGING_EVAL_LEAK",
                    f"Runtime allowlist contains evaluation material: {item}.",
                    "skills/strategic-advisor/runtime-manifest.json",
                )
            )

    skill_root = root / SKILL_ROOT
    if skill_root.is_dir():
        for path in sorted(skill_root.rglob("*")):
            if path.is_file() and any(
                part.lower() in {"evaluation-results", "results", "runs", "outputs"}
                for part in path.relative_to(skill_root).parts[:-1]
            ):
                failures.append(
                    diagnostic(
                        "EVALS_RESULT_IN_SKILL",
                        "Prior model outputs and run results must not be stored in the canonical skill package.",
                        path.relative_to(root),
                    )
                )

    eval_root = skill_root / "evals"
    if not eval_root.is_dir():
        return failures
    seen_case_ids: set[str] = set()
    for path in sorted(eval_root.rglob("*.json")):
        try:
            parsed = json.loads(read_text(path))
        except json.JSONDecodeError as error:
            failures.append(
                diagnostic(
                    "EVALS_INVALID_METADATA",
                    f"Evaluation JSON is invalid at line {error.lineno}, column {error.colno}.",
                    path.relative_to(root),
                )
            )
            continue
        if not isinstance(parsed, (dict, list)):
            failures.append(
                diagnostic(
                    "EVALS_INVALID_METADATA",
                    "Evaluation JSON must be an object or array.",
                    path.relative_to(root),
                )
            )
            continue
        if isinstance(parsed, list):
            if any(not isinstance(item, dict) for item in parsed):
                failures.append(
                    diagnostic(
                        "EVALS_INVALID_METADATA",
                        "Top-level evaluation arrays may contain only objects.",
                        path.relative_to(root),
                    )
                )
            continue
        if "schema_version" in parsed and not (
            isinstance(parsed["schema_version"], (int, str))
            and str(parsed["schema_version"]).strip()
        ):
            failures.append(
                diagnostic(
                    "EVALS_INVALID_METADATA",
                    "schema_version must be a non-empty integer or string when present.",
                    path.relative_to(root),
                )
            )
        if "cases" in parsed:
            cases = parsed["cases"]
            classification = parsed.get("data_classification", parsed.get("provenance"))
            if not isinstance(cases, list) or classification != "synthetic":
                failures.append(
                    diagnostic(
                        "EVALS_INVALID_METADATA",
                        "Case inventories require a cases array and top-level synthetic classification or provenance.",
                        path.relative_to(root),
                    )
                )
                continue
            for index, case in enumerate(cases):
                if (
                    not isinstance(case, dict)
                    or not isinstance(case.get("id"), str)
                    or not case["id"]
                    or (
                        "data_classification" in case
                        and case.get("data_classification") != "synthetic"
                    )
                ):
                    failures.append(
                        diagnostic(
                            "EVALS_INVALID_METADATA",
                            f"Case at index {index} requires a non-empty id and, when present, synthetic data classification.",
                            path.relative_to(root),
                        )
                    )
                    continue
                if case["id"] in seen_case_ids:
                    failures.append(
                        diagnostic(
                            "EVALS_INVALID_METADATA",
                            f"Duplicate evaluation case id: {case['id']}.",
                            path.relative_to(root),
                        )
                    )
                seen_case_ids.add(case["id"])

    failures.extend(check_core_case_inventory(root))
    failures.extend(check_lens_case_inventory(root))
    drift_spec_path = eval_root / "drift_smoke_cases.json"
    try:
        validate_drift_smoke_spec(root, drift_spec_path)
    except (OSError, DriftSmokeError) as error:
        failures.append(
            diagnostic(
                "DRIFT_SMOKE_INVALID",
                str(error),
                drift_spec_path.relative_to(root),
            )
        )

    combined_path = eval_root / "evals.json"
    try:
        expected_combined = serialized_document(root)
    except EvalBuildError as error:
        failures.append(
            diagnostic(
                "EVALS_IMPORT_INVALID",
                str(error),
                combined_path.relative_to(root),
            )
        )
    else:
        combined_case_count = len(json.loads(expected_combined)["evals"])
        if not combined_path.is_file():
            failures.append(
                diagnostic(
                    "EVALS_COMBINED_MISSING",
                    "The deterministic combined Agent Skills inventory is missing.",
                    combined_path.relative_to(root),
                )
            )
        elif read_text(combined_path) != expected_combined:
            failures.append(
                diagnostic(
                    "EVALS_COMBINED_STALE",
                    "evals.json does not exactly match the normative core and lens inventories.",
                    combined_path.relative_to(root),
                )
            )

    trigger_path = eval_root / "eval_queries.json"
    if not trigger_path.is_file():
        failures.append(
            diagnostic(
                "EVALS_TRIGGER_INVALID",
                "Trigger evaluation inventory is missing.",
                trigger_path.relative_to(root),
            )
        )
    else:
        try:
            queries = json.loads(read_text(trigger_path))
        except json.JSONDecodeError as error:
            failures.append(
                diagnostic(
                    "EVALS_TRIGGER_INVALID",
                    f"Trigger JSON is invalid at line {error.lineno}, column {error.colno}.",
                    trigger_path.relative_to(root),
                )
            )
        else:
            valid_queries = bool(
                isinstance(queries, list)
                and len(queries) >= 20
                and all(
                    isinstance(item, dict)
                    and isinstance(item.get("id"), str)
                    and re.fullmatch(r"TRIGGER-[0-9]{3}", item["id"])
                    and isinstance(item.get("query"), str)
                    and item["query"].strip()
                    and type(item.get("should_trigger")) is bool
                    for item in queries
                )
            )
            if valid_queries:
                trigger_query_count = len(queries)
                query_ids = [item["id"] for item in queries]
                query_texts = [item["query"] for item in queries]
                positive = sum(item["should_trigger"] is True for item in queries)
                negative = sum(item["should_trigger"] is False for item in queries)
                allowed_slices = {
                    "direct-positive": True,
                    "implicit-mixed-positive": True,
                    "direct-negative": False,
                    "supported-operational-negative": False,
                }
                slice_counts = {name: 0 for name in allowed_slices}
                slice_valid = True
                for item in queries:
                    slice_name = item.get("slice")
                    if slice_name is None:
                        slice_name = (
                            "direct-positive"
                            if item["should_trigger"] is True
                            else "direct-negative"
                        )
                    if (
                        slice_name not in allowed_slices
                        or allowed_slices[slice_name] is not item["should_trigger"]
                    ):
                        slice_valid = False
                        continue
                    slice_counts[slice_name] += 1
                valid_queries = (
                    len(set(query_ids)) == len(query_ids)
                    and query_ids == sorted(query_ids)
                    and len(set(query_texts)) == len(query_texts)
                    and positive >= 8
                    and negative >= 8
                    and slice_valid
                    and slice_counts["implicit-mixed-positive"] >= 4
                    and slice_counts["supported-operational-negative"] >= 4
                )
            if not valid_queries:
                failures.append(
                    diagnostic(
                        "EVALS_TRIGGER_INVALID",
                        "Trigger inventory needs at least 20 ordered unique TRIGGER-NNN IDs and query texts, boolean labels, at least 8 per class, and four correctly labelled examples in each difficult slice.",
                        trigger_path.relative_to(root),
                    )
                )

    for name in EVALUATION_AUTHORITY_FILES:
        path = eval_root / name
        if not path.is_file() or not read_text(path).strip():
            failures.append(
                diagnostic(
                    "EVALS_AUTHORITY_MISSING",
                    f"Required evaluation authority is missing or empty: {name}.",
                    path.relative_to(root),
                )
            )

    freeze_path = eval_root / "freeze-manifest.template.json"
    freeze_template, freeze_failures = load_json_object(freeze_path, root)
    failures.extend(freeze_failures)
    if freeze_template is not None:
        authority_files = freeze_template.get("authority_files")
        authority_paths: list[str] = []
        if isinstance(authority_files, list):
            authority_paths = [
                item.get("path")
                for item in authority_files
                if isinstance(item, dict) and isinstance(item.get("path"), str)
            ]
        if (
            freeze_template.get("status") != "template-not-frozen"
            or len(authority_paths) != len(authority_files or [])
            or len(authority_paths) != len(set(authority_paths))
            or set(authority_paths) != FROZEN_AUTHORITY_PATHS
        ):
            failures.append(
                diagnostic(
                    "EVALS_FREEZE_AUTHORITY_INVALID",
                    "Freeze template must remain explicitly unfrozen and name the exact complete authority path set once each.",
                    freeze_path.relative_to(root),
                )
            )

        aggregation = freeze_template.get("aggregation")
        n_a_policy = aggregation.get("n_a_policy") if isinstance(aggregation, dict) else None
        if not (
            isinstance(n_a_policy, str)
            and "frozen executable case metadata" in n_a_policy
            and "cannot infer, add, remove, or adjudicate N/A" in n_a_policy
        ):
            failures.append(
                diagnostic(
                    "EVALS_APPLICABILITY_AUTHORITY_INVALID",
                    "Freeze template must make frozen case metadata the sole N/A authority and deny scorer discretion.",
                    freeze_path.relative_to(root),
                )
            )

        generation = freeze_template.get("generation")
        activation = (
            generation.get("treatment_activation") if isinstance(generation, dict) else None
        )
        context_artifacts = (
            generation.get("frozen_context_artifacts")
            if isinstance(generation, dict)
            else None
        )
        sealed_holdout = freeze_template.get("sealed_holdout")
        freeze_controls_valid = bool(
            isinstance(aggregation, dict)
            and aggregation.get("algorithm_id")
            == "evaluation-cluster-paired-bootstrap-sha256-v1"
            and "pair_id" in str(aggregation.get("cluster_unit"))
            and isinstance(activation, dict)
            and activation.get("user_prompt_policy")
            == "User prompt bytes are identical across conditions and contain no treatment-only invocation token."
            and activation.get("trace_fields")
            == ["package_discovered", "skill_selected", "loaded_reference_paths"]
            and isinstance(context_artifacts, dict)
            and set(context_artifacts)
            == {
                "system_and_developer_context",
                "tool_policy",
                "non_treatment_context",
                "declared_input_manifest",
            }
            and isinstance(sealed_holdout, dict)
            and sealed_holdout.get("required") is True
            and sealed_holdout.get("minimum_cases", 0) >= 6
            and sealed_holdout.get("minimum_causal_families", 0) >= 3
        )
        if not freeze_controls_valid:
            failures.append(
                diagnostic(
                    "EVALS_FREEZE_CONTROLS_INVALID",
                    "Freeze template must preserve exact context artifacts, treatment activation proof, pair-aware aggregation, and the sealed holdout gate.",
                    freeze_path.relative_to(root),
                )
            )

        masking = freeze_template.get("masking")
        scoring = freeze_template.get("scoring")
        condition_audit = freeze_template.get("condition_audit")
        structure_view = (
            condition_audit.get("structure_view")
            if isinstance(condition_audit, dict)
            else None
        )
        structure_gate = (
            condition_audit.get("structure_only_gate")
            if isinstance(condition_audit, dict)
            else None
        )
        option_a_template_valid = bool(
            freeze_template.get("schema_version") == 3
            and isinstance(masking, dict)
            and masking.get("quality_pass_label_algorithm")
            == "inverse-ab-quality-pass-v1"
            and masking.get("quality_pass_label_rule")
            == "score-1 presents base A as A and base B as B; score-2 presents base B as A and base A as B."
            and "Normalize score-2.A to base B and score-2.B to base A"
            in str(masking.get("quality_normalization_rule"))
            and masking.get("audit_mapping_algorithm")
            == "hmac-sha256-condition-audit-map-v1"
            and isinstance(scoring, dict)
            and scoring.get("pass_ids") == ["score-1", "score-2"]
            and scoring.get("passes") == 2
            and scoring.get("pass_relationship")
            == "same-family-repeated-evidence-not-independent-judges"
            and "never receive, guess, or return apparent condition"
            in str(scoring.get("condition_identity_policy"))
            and isinstance(condition_audit, dict)
            and condition_audit.get("mode_ids")
            == ["structure-only", "full-response"]
            and condition_audit.get("passes_per_mode_per_pair") == 1
            and isinstance(structure_view, dict)
            and structure_view.get("algorithm_id") == "structure-view-v1"
            and structure_view.get("authority_path")
            == "skills/strategic-advisor/evals/PROTOCOL.md"
            and isinstance(structure_gate, dict)
            and structure_gate.get("minimum_determinate") == 20
            and structure_gate.get("failure_accuracy_gte") == 0.7
            and "cannot pass, fail, rescue, reweight, adjust, or interpret"
            in str(condition_audit.get("full_response_policy"))
        )

        scorer_path = eval_root / "SCORER-PROMPT.md"
        scorer_text = read_text(scorer_path) if scorer_path.is_file() else ""
        auditor_path = eval_root / "CONDITION-AUDITOR-PROMPT.md"
        auditor_text = read_text(auditor_path) if auditor_path.is_file() else ""
        protocol_path = eval_root / "PROTOCOL.md"
        protocol_text = read_text(protocol_path) if protocol_path.is_file() else ""
        option_a_authority_valid = bool(
            "strategic-advisor-scorer-v2" in scorer_text
            and "condition_guess" not in scorer_text
            and '"likely_skilled"' not in scorer_text
            and "strategic-advisor-condition-auditor-v1" in auditor_text
            and "`structure-only`" in auditor_text
            and "`full-response`" in auditor_text
            and "structure-view-v1" in protocol_text
            and "same judge family, not independent judges" in protocol_text
        )
        if not option_a_template_valid or not option_a_authority_valid:
            failures.append(
                diagnostic(
                    "EVALS_OPTION_A_INVALID",
                    "Option A requires condition-free quality scoring, exact inverse A/B quality passes from one judge family, and a separate structure-only gating/full-response descriptive condition audit.",
                    freeze_path.relative_to(root),
                )
            )
        aggregation_path = eval_root / "AGGREGATION.md"
        aggregation_text = read_text(aggregation_path) if aggregation_path.is_file() else ""
        if (
            "select `clusters[u mod C]`" not in aggregation_text
            or "select `cases[u mod C]`" in aggregation_text
        ):
            failures.append(
                diagnostic(
                    "EVALS_AGGREGATION_INVALID",
                    "The evaluation-cluster rejection sampler must select from the declared clusters collection.",
                    aggregation_path.relative_to(root),
                )
            )

        drift_result_path = (
            root
            / "evidence"
            / "evaluations"
            / "drift-smoke"
            / "run-004"
            / "result.json"
        )
        drift_result, drift_result_failures = load_json_object(drift_result_path, root)
        failures.extend(drift_result_failures)
        drift_result_valid = False
        if drift_result is not None:
            try:
                drift_spec, drift_spec_sha256 = validate_drift_smoke_spec(
                    root, eval_root / "drift_smoke_cases.json"
                )
                drift_result_valid = validate_drift_smoke_result(
                    root,
                    drift_spec,
                    drift_spec_sha256,
                    drift_result_path,
                )
            except (OSError, DriftSmokeError) as error:
                failures.append(
                    diagnostic(
                        "DRIFT_SMOKE_RESULT_INVALID",
                        str(error),
                        drift_result_path.relative_to(root),
                    )
                )
        if not drift_result_valid:
            failures.append(
                diagnostic(
                    "DRIFT_SMOKE_RESULT_INVALID",
                    "The current bounded drift smoke is missing, structurally invalid, or contains a failed criterion.",
                    drift_result_path.relative_to(root),
                )
            )
        drift_target = (
            drift_result.get("target", {}) if isinstance(drift_result, dict) else {}
        )
        expected_status = {
            "schema_version": 1,
            "behavioral_comparison": "not-run",
            "frozen_iteration_manifest": "not-created",
            "skilled_vs_unskilled_improvement": "not-established",
            "release_gate": "pending",
            "real_pilot_evidence": "none-enrolled",
            "executable_case_count": combined_case_count,
            "trigger_query_count": trigger_query_count,
            "bounded_drift_smoke": "pass",
            "bounded_drift_smoke_run": "run-004",
            "bounded_drift_smoke_authority_commit": (
                drift_result.get("authority_commit", "")
                if isinstance(drift_result, dict)
                else ""
            ),
            "bounded_drift_smoke_model": drift_target.get("model", ""),
            "bounded_drift_smoke_runtime_package_identity_sha256": drift_target.get(
                "runtime_package_identity_sha256", ""
            ),
        }
        status_path = root / "evidence/evaluations/status.json"
        status, status_failures = load_json_object(status_path, root)
        failures.extend(status_failures)
        if status is not None and status != expected_status:
            failures.append(
                diagnostic(
                    "EVALS_STATUS_DRIFT",
                    "Machine evaluation status must exactly match the current pre-result inventories and absence of release evidence.",
                    status_path.relative_to(root),
                )
            )
        status_markdown = root / "evidence/evaluations/STATUS.md"
        required_status_lines = (
            "Behavioural comparison: **Not run**",
            "Frozen iteration manifest: **Not created**",
            "Skilled-versus-unskilled improvement claim: **Not established**",
            "Hard-gate release status: **Pending**",
            "Real-pilot evidence: **None enrolled**",
            f"Executable synthetic inventory: **{combined_case_count} cases**",
            f"Trigger inventory: **{trigger_query_count} queries**",
            "Bounded current-source drift smoke: **Pass**",
            "Drift-smoke execution: **Codex CLI / gpt-5.6-sol / run-004**",
        )
        if not status_markdown.is_file() or any(
            line not in read_text(status_markdown) for line in required_status_lines
        ):
            failures.append(
                diagnostic(
                    "EVALS_STATUS_DRIFT",
                    "Human-readable evaluation status does not match the machine pre-result status.",
                    status_markdown.relative_to(root),
                )
            )
        evaluation_evidence_root = root / "evidence/evaluations"
        allowed_evidence = {
            "drift-smoke/run-001/result.json",
            "drift-smoke/run-001/runtime-package-manifest.json",
            "drift-smoke/run-001/source-access.json",
            "drift-smoke/run-002/result.json",
            "drift-smoke/run-002/runtime-package-manifest.json",
            "drift-smoke/run-002/source-access.json",
            "drift-smoke/run-003/result.json",
            "drift-smoke/run-003/runtime-package-manifest.json",
            "drift-smoke/run-003/source-access.json",
            "drift-smoke/run-004/result.json",
            "drift-smoke/run-004/runtime-package-manifest.json",
            "drift-smoke/run-004/source-access.json",
        }
        actual_evidence = {
            path.relative_to(evaluation_evidence_root).as_posix()
            for path in sorted(evaluation_evidence_root.rglob("*"))
            if path.is_file() and path.name not in {"STATUS.md", "status.json"}
        }
        unexpected_evidence = sorted(actual_evidence - allowed_evidence)
        missing_evidence = sorted(allowed_evidence - actual_evidence)
        if missing_evidence:
            failures.append(
                diagnostic(
                    "EVALS_STATUS_DRIFT",
                    "Bounded drift-smoke status is missing retained evidence: "
                    + ", ".join(missing_evidence),
                    evaluation_evidence_root.relative_to(root),
                )
            )
        if unexpected_evidence:
            failures.append(
                diagnostic(
                    "EVALS_STATUS_DRIFT",
                    "Evaluation status says no run or freeze exists but additional evaluation evidence files are present: "
                    + ", ".join(unexpected_evidence),
                    evaluation_evidence_root.relative_to(root),
                )
            )
    return failures


def check_privacy(root: Path) -> list[Diagnostic]:
    patterns = (
        (
            "PRIVACY_PRIVATE_CASE",
            re.compile(re.escape("PRIVATE_" + "CASE_DATA"), re.IGNORECASE),
            "Explicit private-case sentinel found.",
        ),
        (
            "PRIVACY_SECRET_PATTERN",
            re.compile(r"AKIA[0-9A-Z]{16}"),
            "AWS access-key-shaped value found.",
        ),
        (
            "PRIVACY_SECRET_PATTERN",
            re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
            "GitHub-token-shaped value found.",
        ),
        (
            "PRIVACY_SECRET_PATTERN",
            re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
            "Slack-token-shaped value found.",
        ),
        (
            "PRIVACY_SECRET_PATTERN",
            re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
            "Private-key header found.",
        ),
    )
    failures: list[Diagnostic] = []
    for path in iter_text_files(root):
        relative = path.relative_to(root)
        text = read_text(path)
        for code, pattern, message in patterns:
            if pattern.search(text):
                failures.append(diagnostic(code, message, relative))
    return failures


def check_pilots(root: Path) -> list[Diagnostic]:
    failures: list[Diagnostic] = []
    required_files = (
        "pilots/PROTOCOL.md",
        "pilots/registry.json",
        "pilots/registry.schema.json",
        "pilots/run-manifest.schema.json",
        "pilots/decision-record.template.md",
    )
    for relative in required_files:
        path = root / relative
        if not path.is_file() or not read_text(path).strip():
            failures.append(
                diagnostic(
                    "PILOTS_ARTIFACT_MISSING",
                    f"Required pilot artifact is missing or empty: {relative}.",
                    relative,
                )
            )
    registry_path = root / "pilots/registry.json"
    if not registry_path.is_file():
        return failures
    try:
        registry = json.loads(read_text(registry_path))
    except json.JSONDecodeError as error:
        failures.append(
            diagnostic(
                "PILOTS_REGISTRY_INVALID",
                f"Registry JSON is invalid at line {error.lineno}, column {error.colno}.",
                registry_path.relative_to(root),
            )
        )
        return failures
    if not isinstance(registry, dict) or set(registry) != {
        "schema_version",
        "status",
        "entries",
    }:
        failures.append(
            diagnostic(
                "PILOTS_REGISTRY_INVALID",
                "Registry must contain exactly schema_version, status, and entries.",
                registry_path.relative_to(root),
            )
        )
        return failures
    entries = registry.get("entries")
    status = registry.get("status")
    if (
        registry.get("schema_version") != 1
        or status not in {"no-pilots-enrolled", "pilots-enrolled", "pilots-complete"}
        or not isinstance(entries, list)
    ):
        failures.append(
            diagnostic(
                "PILOTS_REGISTRY_INVALID",
                "Registry version, status, or entries type is invalid.",
                registry_path.relative_to(root),
            )
        )
        return failures
    if status == "no-pilots-enrolled" and entries:
        failures.append(
            diagnostic(
                "PILOTS_REGISTRY_INVALID",
                "no-pilots-enrolled requires an empty registry.",
                registry_path.relative_to(root),
            )
        )

    required_entry_fields = {
        "pilot_id",
        "domain",
        "registered_at",
        "eligibility_status",
        "eligibility_reason_code",
        "consent_status",
        "consent_reference",
        "terminal_status",
        "public_record",
        "run_manifest",
    }
    seen_ids: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or set(entry) != required_entry_fields:
            failures.append(
                diagnostic(
                    "PILOTS_REGISTRY_INVALID",
                    f"Registry entry {index} has missing or unexpected fields.",
                    registry_path.relative_to(root),
                )
            )
            continue
        pilot_id = entry.get("pilot_id")
        if (
            not isinstance(pilot_id, str)
            or re.fullmatch(r"PILOT-[A-Z0-9]{8}", pilot_id) is None
            or pilot_id in seen_ids
        ):
            failures.append(
                diagnostic(
                    "PILOTS_REGISTRY_INVALID",
                    f"Registry entry {index} has an invalid or duplicate pilot_id.",
                    registry_path.relative_to(root),
                )
            )
            continue
        seen_ids.add(pilot_id)
        if entry.get("domain") not in {"project-product", "career-organizational"}:
            failures.append(
                diagnostic(
                    "PILOTS_REGISTRY_INVALID",
                    f"{pilot_id} has an unsupported pilot domain.",
                    registry_path.relative_to(root),
                )
            )
        consent_reference = entry.get("consent_reference")
        if consent_reference is not None and (
            not isinstance(consent_reference, str)
            or re.fullmatch(r"external:[A-Za-z0-9._:-]+", consent_reference) is None
        ):
            failures.append(
                diagnostic(
                    "PILOTS_REGISTRY_INVALID",
                    f"{pilot_id} has an invalid external consent reference.",
                    registry_path.relative_to(root),
                )
            )
        if entry.get("terminal_status") not in {
            "preregistered",
            "excluded",
            "withdrawn",
            "failed",
            "inconclusive",
            "completed",
        }:
            failures.append(
                diagnostic(
                    "PILOTS_REGISTRY_INVALID",
                    f"{pilot_id} has an invalid terminal status.",
                    registry_path.relative_to(root),
                )
            )
        if entry.get("terminal_status") == "completed":
            for field in ("public_record", "run_manifest"):
                value = entry.get(field)
                if not isinstance(value, str) or not (root / value).is_file():
                    failures.append(
                        diagnostic(
                            "PILOTS_RECORD_MISSING",
                            f"Completed {pilot_id} needs an existing {field}.",
                            registry_path.relative_to(root),
                        )
                    )

    for relative in ("pilots/registry.schema.json", "pilots/run-manifest.schema.json"):
        path = root / relative
        if not path.is_file():
            continue
        try:
            schema = json.loads(read_text(path))
        except json.JSONDecodeError as error:
            failures.append(
                diagnostic(
                    "PILOTS_SCHEMA_INVALID",
                    f"Schema JSON is invalid at line {error.lineno}, column {error.colno}.",
                    relative,
                )
            )
            continue
        if (
            not isinstance(schema, dict)
            or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
            or schema.get("type") != "object"
            or schema.get("additionalProperties") is not False
            or not isinstance(schema.get("required"), list)
        ):
            failures.append(
                diagnostic(
                    "PILOTS_SCHEMA_INVALID",
                    "Pilot schema must be a closed Draft 2020-12 object with required fields.",
                    relative,
                )
            )

    template_path = root / "pilots/decision-record.template.md"
    if template_path.is_file():
        required_headings = {
            "registration and approval",
            "sanitised decision",
            "reality ledger",
            "readiness",
            "competing explanations",
            "decision",
            "immediate moves",
            "controls and review",
            "case-owner judgment",
            "privacy review",
        }
        missing = sorted(required_headings - markdown_headings(read_text(template_path)))
        if missing:
            failures.append(
                diagnostic(
                    "PILOTS_TEMPLATE_INVALID",
                    f"Pilot decision template is missing headings: {', '.join(missing)}.",
                    template_path.relative_to(root),
                )
            )
    return failures


def slugify_heading(heading: str) -> str:
    heading = re.sub(r"<[^>]+>", "", heading).strip().lower()
    heading = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE)
    return re.sub(r"[ -]+", "-", heading).strip("-")


def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in read_text(path).splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        base = slugify_heading(match.group(1))
        count = counts.get(base, 0)
        counts[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def check_links(root: Path) -> list[Diagnostic]:
    failures: list[Diagnostic] = []
    candidates: list[Path] = []
    for relative in ("README.md", "PRODUCT-CONTRACT.md", "CONTRIBUTING.md", "SECURITY.md"):
        path = root / relative
        if path.is_file():
            candidates.append(path)
    skill_root = root / SKILL_ROOT
    if skill_root.is_dir():
        candidates.extend(sorted(skill_root.rglob("*.md")))
    link_pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
    for source in sorted(set(candidates)):
        for raw_target in link_pattern.findall(read_text(source)):
            target = raw_target.strip().strip("<>")
            if not target or re.match(r"^(?:https?|mailto):", target, re.IGNORECASE):
                continue
            target = unquote(target)
            path_part, separator, anchor = target.partition("#")
            destination = source if not path_part else (source.parent / path_part).resolve()
            try:
                relative_destination = destination.relative_to(root.resolve())
            except ValueError:
                failures.append(
                    diagnostic(
                        "LINK_BROKEN",
                        f"Internal link escapes the repository: {raw_target}.",
                        source.relative_to(root),
                    )
                )
                continue
            if not destination.exists():
                failures.append(
                    diagnostic(
                        "LINK_BROKEN",
                        f"Internal link target does not exist: {raw_target}.",
                        source.relative_to(root),
                    )
                )
                continue
            if separator and anchor and destination.is_file() and destination.suffix.lower() == ".md":
                if anchor not in markdown_anchors(destination):
                    failures.append(
                        diagnostic(
                            "LINK_BROKEN",
                            f"Internal link anchor does not exist: {raw_target}.",
                            source.relative_to(root),
                        )
                    )
            _ = relative_destination
    return failures


CHECKS = {
    "skill": check_skill,
    "lenses": check_lenses,
    "evals": check_evals,
    "pilots": check_pilots,
    "privacy": check_privacy,
    "claims": check_claims,
    "links": check_links,
}


def validate(root: Path, scopes: Sequence[str]) -> list[Diagnostic]:
    failures: set[Diagnostic] = set()
    for scope in scopes:
        failures.update(CHECKS[scope](root))
    return sorted(failures)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run deterministic Strategic Advisor repository checks."
    )
    parser.add_argument(
        "--scope",
        choices=SCOPES,
        help="Run one check scope; omit to run all scopes.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (primarily for isolated fixture validation).",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    scopes = (args.scope,) if args.scope else SCOPES
    failures = validate(root, scopes)
    for failure in failures:
        print(failure.render())
    if failures:
        print(f"SUMMARY: FAIL ({len(failures)} diagnostic(s))")
        return 1
    for scope in scopes:
        print(f"PASS [SCOPE_{scope.upper()}]")
    print(f"SUMMARY: PASS ({len(scopes)} scope(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
