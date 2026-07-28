#!/usr/bin/env python3
"""Canonical Strategic Advisor distribution state and release preparation.

This module owns the version/runtime binding used by builders, validation, and
GitHub release automation. It deliberately distinguishes a prepared immutable
distribution from the last public distribution that has been clean-downloaded
and verified.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Mapping, Sequence


SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

import build_runtime_package as runtime_package  # noqa: E402


AUTHORITY_PATH = PurePosixPath("distribution.json")
README_PATH = PurePosixPath("README.md")
INSTALL_PATH = PurePosixPath("INSTALL.md")
CONTRACT_PATH = PurePosixPath("PRODUCT-CONTRACT.md")
README_START = "<!-- strategic-advisor-distribution:start -->"
README_END = "<!-- strategic-advisor-distribution:end -->"
INSTALL_START = "<!-- strategic-advisor-download:start -->"
INSTALL_END = "<!-- strategic-advisor-download:end -->"
CONTRACT_START = "<!-- strategic-advisor-contract:start -->"
CONTRACT_END = "<!-- strategic-advisor-contract:end -->"
VERSION_PATTERN = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"-(alpha|beta|rc)\.(0|[1-9][0-9]*)$"
)
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
REVISION_PATTERN = re.compile(r"^[0-9a-f]{40}$")


class ReleaseStateError(ValueError):
    """Committed distribution state violates the release contract."""


def rendered_json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def version_key(version: str) -> tuple[int, int, int, int, int]:
    if not isinstance(version, str):
        raise ReleaseStateError("version must be a string")
    match = VERSION_PATTERN.fullmatch(version)
    if match is None:
        raise ReleaseStateError(
            "version must be a numeric SemVer prerelease such as 0.2.0-alpha.3"
        )
    channel_order = {"alpha": 0, "beta": 1, "rc": 2}
    return (
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        channel_order[match.group(4)],
        int(match.group(5)),
    )


def _require_exact_keys(value: object, keys: set[str], label: str) -> dict:
    if not isinstance(value, dict) or set(value) != keys:
        raise ReleaseStateError(f"{label} must use exactly {sorted(keys)}")
    return value


def validate_authority(value: object) -> dict:
    authority = _require_exact_keys(
        value,
        {"current_public", "distribution", "schema_version", "state"},
        "distribution authority",
    )
    if authority["schema_version"] != 1:
        raise ReleaseStateError("distribution schema_version must be 1")
    if authority["state"] not in {"prepared", "published"}:
        raise ReleaseStateError("distribution state must be prepared or published")
    distribution = _require_exact_keys(
        authority["distribution"],
        {"runtime_package_identity_sha256", "version"},
        "distribution",
    )
    current = _require_exact_keys(
        authority["current_public"],
        {
            "evidence",
            "runtime_package_identity_sha256",
            "source_revision",
            "tag",
            "version",
        },
        "current_public",
    )
    distribution_key = version_key(distribution.get("version"))
    current_key = version_key(current.get("version"))
    if not SHA256_PATTERN.fullmatch(
        str(distribution.get("runtime_package_identity_sha256", ""))
    ):
        raise ReleaseStateError("distribution runtime identity must be SHA-256")
    if not SHA256_PATTERN.fullmatch(
        str(current.get("runtime_package_identity_sha256", ""))
    ):
        raise ReleaseStateError("current_public runtime identity must be SHA-256")
    if not REVISION_PATTERN.fullmatch(str(current.get("source_revision", ""))):
        raise ReleaseStateError("current_public source_revision must be a Git SHA-1")
    if current.get("tag") != f"v{current.get('version')}":
        raise ReleaseStateError("current_public tag must equal v<version>")
    if current.get("evidence") != f"evidence/releases/v{current.get('version')}.json":
        raise ReleaseStateError("current_public evidence path must match its version")
    if authority["state"] == "prepared" and not distribution_key > current_key:
        raise ReleaseStateError(
            "a prepared distribution version must advance current_public"
        )
    if authority["state"] == "published" and distribution_key != current_key:
        raise ReleaseStateError(
            "a published distribution version must equal current_public"
        )
    return authority


def load_authority(root: Path) -> tuple[dict, bytes]:
    path = root / Path(*AUTHORITY_PATH.parts)
    if path.is_symlink() or not path.is_file():
        raise ReleaseStateError(f"{AUTHORITY_PATH} must be a regular file")
    content = path.read_bytes()
    try:
        parsed = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReleaseStateError(f"{AUTHORITY_PATH} is not valid UTF-8 JSON") from error
    authority = validate_authority(parsed)
    if content != rendered_json_bytes(authority):
        raise ReleaseStateError(f"{AUTHORITY_PATH} must use canonical rendered JSON")
    return authority, content


def runtime_identity(root: Path) -> str:
    allowlist_relative = runtime_package.normalized_relative_path(
        runtime_package.DEFAULT_ALLOWLIST, "runtime allowlist"
    )
    allowlist, allowlist_bytes, _ = runtime_package.load_allowlist(
        root, allowlist_relative
    )
    package_root, files = runtime_package.collect_files(root, allowlist)
    runtime_package.reject_evaluation_content(root, files)
    manifest = runtime_package.package_manifest(
        allowlist_relative,
        allowlist_bytes,
        package_root,
        files,
    )
    return manifest["package_identity_sha256"]


def validate_runtime_binding(root: Path, authority: Mapping[str, object]) -> None:
    observed = runtime_identity(root)
    expected = authority["distribution"]["runtime_package_identity_sha256"]
    if observed != expected:
        raise ReleaseStateError(
            "canonical runtime bytes do not match prepared distribution identity: "
            f"expected {expected}, observed {observed}; run "
            "python3 scripts/release_state.py prepare --version <next-version>"
        )


def read_contract(path: Path) -> tuple[str, dict, str]:
    text = path.read_text(encoding="utf-8")
    if CONTRACT_START not in text or CONTRACT_END not in text:
        raise ReleaseStateError("PRODUCT-CONTRACT.md lacks contract markers")
    prefix, remainder = text.split(CONTRACT_START, 1)
    section, suffix = remainder.split(CONTRACT_END, 1)
    match = re.fullmatch(r"\s*```json\s*\n(\{.*\})\n```\s*", section, re.DOTALL)
    if match is None:
        raise ReleaseStateError("PRODUCT-CONTRACT.md contract block is malformed")
    try:
        contract = json.loads(match.group(1))
    except json.JSONDecodeError as error:
        raise ReleaseStateError("PRODUCT-CONTRACT.md contract JSON is invalid") from error
    return prefix, contract, suffix


def render_contract(prefix: str, contract: dict, suffix: str) -> bytes:
    top_level_order = (
        "schema_version",
        "release_status",
        "early_access_distribution_version",
        "prepared_distribution_version",
        "prepared_runtime_package_identity_sha256",
        "capability_promotion_enabled",
        "canonical_product_path",
        "supported_installation_available",
        "runtime_package_manifest",
        "install_artifact_builder",
        "supported_capabilities",
        "capabilities",
    )
    if set(contract) != set(top_level_order):
        raise ReleaseStateError(
            "PRODUCT-CONTRACT.md claim registry fields do not match the "
            "canonical contract"
        )
    ordered = {key: contract[key] for key in top_level_order}
    ordered["capabilities"] = [
        {
            key: capability[key]
            for key in ("id", "kind", "state", "evidence")
        }
        for capability in contract["capabilities"]
    ]
    section = json.dumps(ordered, indent=2).rstrip("\n")
    return (
        prefix
        + CONTRACT_START
        + "\n```json\n"
        + section
        + "\n```\n"
        + CONTRACT_END
        + suffix
    ).encode("utf-8")


def replace_marked_block(
    text: str, start: str, end: str, body: str, label: str
) -> bytes:
    if text.count(start) != 1 or text.count(end) != 1:
        raise ReleaseStateError(f"{label} must contain exactly one release marker block")
    prefix, remainder = text.split(start, 1)
    _, suffix = remainder.split(end, 1)
    return (prefix + start + "\n" + body.rstrip() + "\n" + end + suffix).encode(
        "utf-8"
    )


def readme_block(authority: Mapping[str, object]) -> str:
    current = authority["current_public"]
    distribution = authority["distribution"]
    rows = [
        "| Field | Current state |",
        "| --- | --- |",
        "| Maturity | Pre-release |",
        "| Early-access distribution | "
        f"[`v{current['version']}` GitHub prerelease]"
        f"(https://github.com/johndetlefs/strategic-advisor/releases/tag/v{current['version']}) |",
    ]
    if authority["state"] == "prepared":
        rows.append(
            "| Prepared distribution | "
            f"`v{distribution['version']}` is release intent only until the "
            "protected-main workflow publishes and a fresh public download verifies. |"
        )
    return "\n".join(rows)


def install_block(authority: Mapping[str, object]) -> str:
    current = authority["current_public"]
    distribution = authority["distribution"]
    lines = [
        "Download these four files together from the current",
        f"[`v{current['version']}` prerelease]"
        f"(https://github.com/johndetlefs/strategic-advisor/releases/tag/v{current['version']}):",
    ]
    if authority["state"] == "prepared":
        lines.extend(
            [
                "",
                f"`v{distribution['version']}` is prepared release intent, not the "
                "current public download, until the protected-main workflow and "
                "fresh-download verification pass.",
            ]
        )
    return "\n".join(lines)


def synchronized_documents(root: Path, authority: Mapping[str, object]) -> dict[Path, bytes]:
    contract_path = root / Path(*CONTRACT_PATH.parts)
    prefix, contract, suffix = read_contract(contract_path)
    current = authority["current_public"]
    distribution = authority["distribution"]
    contract["early_access_distribution_version"] = current["version"]
    contract["prepared_distribution_version"] = (
        distribution["version"] if authority["state"] == "prepared" else None
    )
    contract["prepared_runtime_package_identity_sha256"] = (
        distribution["runtime_package_identity_sha256"]
        if authority["state"] == "prepared"
        else None
    )
    return {
        contract_path: render_contract(prefix, contract, suffix),
        root / Path(*README_PATH.parts): replace_marked_block(
            (root / Path(*README_PATH.parts)).read_text(encoding="utf-8"),
            README_START,
            README_END,
            readme_block(authority),
            "README.md",
        ),
        root / Path(*INSTALL_PATH.parts): replace_marked_block(
            (root / Path(*INSTALL_PATH.parts)).read_text(encoding="utf-8"),
            INSTALL_START,
            INSTALL_END,
            install_block(authority),
            "INSTALL.md",
        ),
    }


def validate_documents(root: Path, authority: Mapping[str, object]) -> None:
    _, contract, _ = read_contract(root / Path(*CONTRACT_PATH.parts))
    current = authority["current_public"]
    distribution = authority["distribution"]
    expected_prepared_version = (
        distribution["version"] if authority["state"] == "prepared" else None
    )
    expected_prepared_runtime = (
        distribution["runtime_package_identity_sha256"]
        if authority["state"] == "prepared"
        else None
    )
    if (
        contract.get("early_access_distribution_version") != current["version"]
        or contract.get("prepared_distribution_version")
        != expected_prepared_version
        or contract.get("prepared_runtime_package_identity_sha256")
        != expected_prepared_runtime
    ):
        raise ReleaseStateError(
            "PRODUCT-CONTRACT.md release fields do not match canonical distribution state"
        )
    marked_expectations = (
        (
            root / Path(*README_PATH.parts),
            README_START,
            README_END,
            readme_block(authority),
        ),
        (
            root / Path(*INSTALL_PATH.parts),
            INSTALL_START,
            INSTALL_END,
            install_block(authority),
        ),
    )
    for path, start, end, expected_body in marked_expectations:
        text = path.read_text(encoding="utf-8")
        if text.count(start) != 1 or text.count(end) != 1:
            raise ReleaseStateError(
                f"{path.relative_to(root)} release marker block is missing or duplicated"
            )
        actual_body = text.split(start, 1)[1].split(end, 1)[0].strip()
        if actual_body != expected_body.strip():
            raise ReleaseStateError(
                f"{path.relative_to(root)} release marker block does not match "
                "canonical distribution state"
            )


def _git_output(root: Path, arguments: Sequence[str]) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise ReleaseStateError("Git is unavailable") from error
    if result.returncode != 0:
        raise ReleaseStateError(result.stderr.strip() or "Git command failed")
    return result.stdout.strip()


def ensure_version_unused(root: Path, version: str) -> None:
    tag = f"v{version}"
    if _git_output(root, ["tag", "--list", tag]):
        raise ReleaseStateError(f"version is already used by local tag {tag}")
    if (root / "evidence" / "releases" / f"{tag}.json").exists():
        raise ReleaseStateError(f"version is already used by retained release evidence: {tag}")


def _transactional_write(changes: Mapping[Path, bytes]) -> None:
    originals = {path: path.read_bytes() if path.exists() else None for path in changes}
    temporary: dict[Path, Path] = {}
    replaced: list[Path] = []
    try:
        for path, content in changes.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{path.name}.", suffix=".release-tmp", dir=path.parent
            )
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            temporary[path] = Path(temporary_name)
        for path in sorted(changes, key=lambda candidate: candidate.as_posix()):
            os.replace(temporary[path], path)
            replaced.append(path)
    except Exception:
        for path in reversed(replaced):
            original = originals[path]
            if original is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(original)
        raise
    finally:
        for path in temporary.values():
            path.unlink(missing_ok=True)


def prepare(root: Path, version: str) -> dict:
    authority, _ = load_authority(root)
    if authority["state"] != "published":
        raise ReleaseStateError(
            "current distribution is already prepared; publish and finalize it first"
        )
    if version_key(version) <= version_key(
        authority["current_public"]["version"]
    ):
        raise ReleaseStateError("prepared version must advance current_public")
    ensure_version_unused(root, version)
    updated = json.loads(json.dumps(authority))
    updated["state"] = "prepared"
    updated["distribution"] = {
        "runtime_package_identity_sha256": runtime_identity(root),
        "version": version,
    }
    validate_authority(updated)
    changes = {
        root / Path(*AUTHORITY_PATH.parts): rendered_json_bytes(updated),
        **synchronized_documents(root, updated),
    }
    _transactional_write(changes)
    validate(root)
    return updated


def synchronize(root: Path) -> dict:
    authority, _ = load_authority(root)
    _transactional_write(synchronized_documents(root, authority))
    validate(root)
    return authority


def finalize(root: Path, evidence_path: Path) -> dict:
    authority, _ = load_authority(root)
    if authority["state"] != "prepared":
        raise ReleaseStateError("only a prepared distribution can be finalized")
    if evidence_path.is_symlink() or not evidence_path.is_file():
        raise ReleaseStateError("release evidence input must be a regular file")
    evidence_bytes = evidence_path.read_bytes()
    try:
        evidence = json.loads(evidence_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReleaseStateError("release evidence is not valid UTF-8 JSON") from error
    distribution = authority["distribution"]
    release = evidence.get("release") if isinstance(evidence, dict) else None
    proof = evidence.get("proof_boundary") if isinstance(evidence, dict) else None
    if not (
        isinstance(evidence, dict)
        and evidence.get("schema_version") == 1
        and isinstance(release, dict)
        and release.get("version") == distribution["version"]
        and release.get("tag") == f"v{distribution['version']}"
        and release.get("status") == "prerelease"
        and release.get("runtime_package_identity_sha256")
        == distribution["runtime_package_identity_sha256"]
        and REVISION_PATTERN.fullmatch(str(release.get("source_revision", "")))
        and isinstance(proof, dict)
        and proof.get("package_and_release_alignment_proven") is True
        and proof.get("clean_public_download_proven") is True
    ):
        raise ReleaseStateError(
            "release evidence does not prove the prepared public distribution"
        )
    updated = json.loads(json.dumps(authority))
    updated["state"] = "published"
    updated["current_public"] = {
        "evidence": f"evidence/releases/v{distribution['version']}.json",
        "runtime_package_identity_sha256": distribution[
            "runtime_package_identity_sha256"
        ],
        "source_revision": release["source_revision"],
        "tag": release["tag"],
        "version": distribution["version"],
    }
    validate_authority(updated)
    canonical_evidence = rendered_json_bytes(evidence)
    destination = root / updated["current_public"]["evidence"]
    if destination.exists() or destination.is_symlink():
        raise ReleaseStateError(
            f"release evidence destination already exists: {destination.relative_to(root)}"
        )
    changes = {
        root / Path(*AUTHORITY_PATH.parts): rendered_json_bytes(updated),
        destination: canonical_evidence,
        **synchronized_documents(root, updated),
    }
    _transactional_write(changes)
    validate(root)
    return updated


def validate(root: Path) -> dict:
    authority, _ = load_authority(root)
    validate_runtime_binding(root, authority)
    validate_documents(root, authority)
    return authority


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare and validate immutable Strategic Advisor distributions."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Strategic Advisor repository root.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check")
    subparsers.add_parser("sync")
    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument("--version", required=True)
    finalize_parser = subparsers.add_parser("finalize")
    finalize_parser.add_argument("--evidence", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        root = args.root.resolve()
        if args.command == "prepare":
            result = prepare(root, args.version)
        elif args.command == "finalize":
            result = finalize(root, args.evidence.resolve())
        elif args.command == "sync":
            result = synchronize(root)
        else:
            result = validate(root)
    except (OSError, ReleaseStateError, runtime_package.PackagingError) as error:
        print(f"ERROR [RELEASE_STATE]: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
