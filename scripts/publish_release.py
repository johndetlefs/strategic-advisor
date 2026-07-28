#!/usr/bin/env python3
"""Generate and independently verify immutable GitHub prerelease material.

GitHub Actions owns the single conditional mutation (`gh release create`).
This module produces release notes and verifies either a newly created release
or an already-existing release without modifying it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Sequence


SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

import build_install_artifacts as install_artifacts  # noqa: E402
import build_runtime_package as runtime_package  # noqa: E402
import release_state  # noqa: E402


ASSET_NAMES = (
    "install-artifacts.json",
    "strategic-advisor-chatgpt.zip",
    "strategic-advisor-plugin.zip",
    "strategic-advisor.zip",
)
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class ReleaseVerificationError(ValueError):
    """A public release differs from the immutable prepared distribution."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path, label: str) -> dict:
    if path.is_symlink() or not path.is_file():
        raise ReleaseVerificationError(f"{label} must be a regular file")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReleaseVerificationError(f"{label} is not valid UTF-8 JSON") from error
    if not isinstance(value, dict):
        raise ReleaseVerificationError(f"{label} must be a JSON object")
    return value


def asset_records(directory: Path) -> list[dict]:
    actual = sorted(path.name for path in directory.iterdir() if path.is_file())
    if actual != list(ASSET_NAMES):
        raise ReleaseVerificationError(
            f"artifact directory must contain exactly {list(ASSET_NAMES)}; "
            f"observed {actual}"
        )
    return [
        {
            "name": name,
            "sha256": sha256_file(directory / name),
            "size_bytes": (directory / name).stat().st_size,
        }
        for name in ASSET_NAMES
    ]


def release_notes(root: Path, build_dir: Path, source_revision: str) -> str:
    authority = release_state.validate(root)
    if authority["state"] != "prepared":
        raise ReleaseVerificationError(
            "release notes require a prepared distribution"
        )
    if not re.fullmatch(r"[0-9a-f]{40}", source_revision):
        raise ReleaseVerificationError("source revision must be a Git SHA-1")
    records = asset_records(build_dir)
    provenance = load_json(
        build_dir / "install-artifacts.json", "install provenance"
    )
    runtime_identity = authority["distribution"][
        "runtime_package_identity_sha256"
    ]
    if (
        provenance.get("source_revision") != source_revision
        or provenance.get("source_revision_exact") is not True
        or provenance.get("runtime_package", {}).get(
            "package_identity_sha256"
        )
        != runtime_identity
    ):
        raise ReleaseVerificationError(
            "clean build provenance does not match prepared release source/runtime"
        )
    digest_lines = "\n".join(
        f"- `{record['name']}`: `sha256:{record['sha256']}`"
        for record in records
    )
    return f"""Strategic Advisor v{authority['distribution']['version']}

Experimental early-access distribution from exact source `{source_revision}`.

- Runtime package identity: `sha256:{runtime_identity}`
- Install provenance: `sha256:{sha256_file(build_dir / 'install-artifacts.json')}`

Assets:

{digest_lines}

These deterministic packages are release candidates for early testing. Their
publication does not prove host installation or activation, supported
capability, cross-host parity, adoption, comparative improvement, or strategic
effectiveness.
"""


def _metadata_assets(metadata: dict) -> list[dict]:
    raw = metadata.get("assets")
    if not isinstance(raw, list):
        raise ReleaseVerificationError("GitHub release metadata lacks assets")
    records: list[dict] = []
    for item in raw:
        if not isinstance(item, dict):
            raise ReleaseVerificationError("GitHub asset metadata is malformed")
        digest = item.get("digest")
        if not isinstance(digest, str) or not digest.startswith("sha256:"):
            raise ReleaseVerificationError(
                f"GitHub asset digest is unavailable for {item.get('name')}"
            )
        sha256 = digest.removeprefix("sha256:")
        if not SHA256_PATTERN.fullmatch(sha256):
            raise ReleaseVerificationError("GitHub asset SHA-256 is invalid")
        records.append(
            {
                "name": item.get("name"),
                "sha256": sha256,
                "size_bytes": item.get("size"),
            }
        )
    return sorted(records, key=lambda item: str(item["name"]))


def verify_public(
    root: Path,
    metadata_path: Path,
    download_dir: Path,
    local_build_dir: Path,
    source_revision: str,
    evidence_out: Path,
) -> dict:
    authority = release_state.validate(root)
    if authority["state"] != "prepared":
        raise ReleaseVerificationError(
            "public verification requires a prepared distribution"
        )
    distribution = authority["distribution"]
    tag = f"v{distribution['version']}"
    metadata = load_json(metadata_path, "GitHub release metadata")
    if (
        metadata.get("tagName") != tag
        or metadata.get("isPrerelease") is not True
        or metadata.get("targetCommitish") != source_revision
        or metadata.get("url")
        != f"https://github.com/johndetlefs/strategic-advisor/releases/tag/{tag}"
        or not isinstance(metadata.get("publishedAt"), str)
    ):
        raise ReleaseVerificationError(
            "GitHub release tag, prerelease state, source, URL, or publication "
            "timestamp does not match prepared intent"
        )
    local_records = asset_records(local_build_dir)
    downloaded_records = asset_records(download_dir)
    github_records = _metadata_assets(metadata)
    if local_records != downloaded_records or local_records != github_records:
        raise ReleaseVerificationError(
            "GitHub metadata, fresh downloads, and local clean build differ"
        )
    provenance_path = download_dir / "install-artifacts.json"
    provenance = load_json(provenance_path, "downloaded install provenance")
    if (
        provenance.get("source_revision") != source_revision
        or provenance.get("source_revision_exact") is not True
        or provenance.get("source_tree_state") != "clean"
        or provenance.get("distribution_version") != distribution["version"]
        or provenance.get("runtime_package", {}).get(
            "package_identity_sha256"
        )
        != distribution["runtime_package_identity_sha256"]
    ):
        raise ReleaseVerificationError(
            "downloaded provenance does not match clean source, version, or runtime"
        )
    verification = install_artifacts.verify(
        skill_archive=download_dir / "strategic-advisor.zip",
        plugin_archive=download_dir / "strategic-advisor-plugin.zip",
        chatgpt_kit=download_dir / "strategic-advisor-chatgpt.zip",
        provenance_path=provenance_path,
        expected_provenance_sha256=sha256_file(provenance_path),
        expected_runtime_identity=distribution[
            "runtime_package_identity_sha256"
        ],
    )
    evidence = {
        "schema_version": 1,
        "release": {
            "assets": local_records,
            "published_at": metadata["publishedAt"],
            "runtime_package_identity_sha256": distribution[
                "runtime_package_identity_sha256"
            ],
            "source_revision": source_revision,
            "status": "prerelease",
            "tag": tag,
            "url": metadata["url"],
            "version": distribution["version"],
        },
        "reproduction": {
            "clean_download_consumer_verification": "pass",
            "public_asset_digests_match_local_build": True,
            "trusted_provenance_matched": verification[
                "trusted_provenance_sha256_matched"
            ],
            "trusted_runtime_identity_matched": verification[
                "trusted_runtime_identity_matched"
            ],
        },
        "proof_boundary": {
            "package_and_release_alignment_proven": True,
            "clean_public_download_proven": True,
            "codex_account_activation_proven_here": False,
            "chatgpt_account_activation_proven_here": False,
            "claude_account_activation_proven_here": False,
            "cross_host_parity_proven": False,
            "strategic_effectiveness_proven": False,
            "supported_capability_claimed": False,
        },
    }
    if evidence_out.exists() or evidence_out.is_symlink():
        raise ReleaseVerificationError(
            f"evidence output already exists: {evidence_out}"
        )
    evidence_out.parent.mkdir(parents=True, exist_ok=True)
    with evidence_out.open("xb") as handle:
        handle.write(runtime_package.rendered_json_bytes(evidence))
    return evidence


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create release notes and verify immutable GitHub releases."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    notes = subparsers.add_parser("notes")
    notes.add_argument("--build-dir", type=Path, required=True)
    notes.add_argument("--source-revision", required=True)
    verify = subparsers.add_parser("verify-public")
    verify.add_argument("--metadata", type=Path, required=True)
    verify.add_argument("--download-dir", type=Path, required=True)
    verify.add_argument("--local-build-dir", type=Path, required=True)
    verify.add_argument("--source-revision", required=True)
    verify.add_argument("--evidence-out", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        root = args.root.resolve()
        if args.command == "notes":
            print(
                release_notes(
                    root,
                    args.build_dir.resolve(),
                    args.source_revision,
                ),
                end="",
            )
            return 0
        evidence = verify_public(
            root,
            args.metadata.resolve(),
            args.download_dir.resolve(),
            args.local_build_dir.resolve(),
            args.source_revision,
            args.evidence_out.resolve(),
        )
    except (
        OSError,
        ReleaseVerificationError,
        install_artifacts.InstallArtifactError,
        release_state.ReleaseStateError,
    ) as error:
        print(f"ERROR [RELEASE_PUBLISH]: {error}", file=sys.stderr)
        return 1
    print(json.dumps(evidence, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
