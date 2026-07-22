#!/usr/bin/env python3
"""Build a content-addressed Strategic Advisor runtime package.

Only files explicitly named by the source allowlist are copied. The generated
provenance manifest is written outside the model-visible package and contains
no timestamps or destination-specific values, so identical source bytes yield
identical manifest bytes and aggregate identity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Sequence


DEFAULT_ALLOWLIST = "skills/strategic-advisor/runtime-manifest.json"
FORBIDDEN_RUNTIME_PARTS = {
    "evals",
    "evaluation",
    "evaluation-results",
    "expected",
    "fixtures",
    "results",
    "rubrics",
    "runs",
    "scores",
}
FORBIDDEN_RUNTIME_TOKENS = (
    "adjudicat",
    "eval",
    "expected",
    "fixture",
    "freeze",
    "hard-gate",
    "result",
    "rubric",
    "score",
)
FORBIDDEN_EVALUATION_CONTENT_MARKERS = (
    '"expected_readiness"',
    '"not_applicable_dimensions"',
    '"probe_tags"',
    "case-assertion-grader",
    "hmac-sha256-mask-v1",
)
FINGERPRINT_KEYS = {
    "assertions",
    "expected_decision_properties",
    "expected_diagnosis",
    "forbidden_behaviors",
    "forbidden_decision_properties",
    "prompt",
    "query",
    "required_decision_properties",
}
IDENTITY_ALGORITHM = "sha256-canonical-json-v1"


class PackagingError(ValueError):
    """A package cannot be built without violating the runtime boundary."""


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def rendered_json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def normalized_relative_path(raw: object, label: str) -> PurePosixPath:
    if not isinstance(raw, str) or not raw or "\\" in raw:
        raise PackagingError(f"{label} must be a non-empty POSIX relative path")
    path = PurePosixPath(raw)
    if (
        path.is_absolute()
        or ".." in path.parts
        or "." in path.parts
        or raw != path.as_posix()
    ):
        raise PackagingError(f"{label} contains path traversal or is not normalized: {raw}")
    return path


def relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def reject_symlink_chain(base: Path, relative: PurePosixPath, label: str) -> Path:
    current = base
    if current.is_symlink():
        raise PackagingError(f"{label} traverses symlink source root: {current}")
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise PackagingError(f"{label} traverses symlink: {current}")
    return current


def load_allowlist(
    source_root: Path, allowlist_relative: PurePosixPath
) -> tuple[dict, bytes, Path]:
    allowlist_path = reject_symlink_chain(source_root, allowlist_relative, "allowlist")
    if not allowlist_path.is_file():
        raise PackagingError(f"allowlist is not a regular file: {allowlist_relative}")
    allowlist_bytes = allowlist_path.read_bytes()
    try:
        parsed = json.loads(allowlist_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PackagingError(f"allowlist is not valid UTF-8 JSON: {error}") from error
    if not isinstance(parsed, dict):
        raise PackagingError("allowlist must be a JSON object")
    if parsed.get("schema_version") != 1:
        raise PackagingError("allowlist schema_version must be 1")
    return parsed, allowlist_bytes, allowlist_path


def collect_files(
    source_root: Path, allowlist: dict
) -> tuple[PurePosixPath, list[tuple[PurePosixPath, bytes]]]:
    package_root_relative = normalized_relative_path(
        allowlist.get("package_root"), "package_root"
    )
    if package_root_relative.as_posix() != "skills/strategic-advisor":
        raise PackagingError("package_root must be skills/strategic-advisor")
    package_root = reject_symlink_chain(
        source_root, package_root_relative, "package_root"
    )
    if not package_root.is_dir():
        raise PackagingError(f"package_root is not a directory: {package_root_relative}")

    raw_includes = allowlist.get("include")
    if not isinstance(raw_includes, list) or not raw_includes:
        raise PackagingError("allowlist include must be a non-empty array")

    includes: list[PurePosixPath] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_includes):
        relative = normalized_relative_path(raw, f"include[{index}]")
        if relative.as_posix() in seen:
            raise PackagingError(f"duplicate include path: {relative}")
        seen.add(relative.as_posix())
        forbidden = {part.lower() for part in relative.parts} & FORBIDDEN_RUNTIME_PARTS
        forbidden_name = any(
            token in part.lower()
            for part in relative.parts
            for token in FORBIDDEN_RUNTIME_TOKENS
        )
        if forbidden or forbidden_name:
            raise PackagingError(
                f"evaluation or result material is forbidden in runtime package: {relative}"
            )
        includes.append(relative)

    collected: list[tuple[PurePosixPath, bytes]] = []
    for relative in sorted(includes, key=lambda item: item.as_posix()):
        source = reject_symlink_chain(package_root, relative, f"include {relative}")
        if not source.is_file():
            raise PackagingError(f"allowlisted source is not a regular file: {relative}")
        resolved_source = source.resolve()
        resolved_package_root = package_root.resolve()
        if not relative_to(resolved_source, resolved_package_root):
            raise PackagingError(f"allowlisted source escapes package_root: {relative}")
        collected.append((relative, source.read_bytes()))
    return package_root_relative, collected


def nested_strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for child in value for item in nested_strings(child)]
    if isinstance(value, dict):
        return [item for child in value.values() for item in nested_strings(child)]
    return []


def evaluation_fingerprints(source_root: Path) -> set[str]:
    """Return long, case-specific strings that must not enter the runtime package."""

    eval_root = source_root / "skills" / "strategic-advisor" / "evals"
    if not eval_root.is_dir() or eval_root.is_symlink():
        raise PackagingError("evaluation authority directory is missing or symlinked")
    fingerprints: set[str] = set()
    for path in sorted(eval_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md"}:
            continue
        relative = path.relative_to(source_root)
        if path.is_symlink():
            raise PackagingError(f"evaluation authority is not a regular file: {relative}")
        try:
            authority_text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            raise PackagingError(f"evaluation authority is not UTF-8: {relative}") from error
        stripped_authority = authority_text.strip()
        if len(stripped_authority) >= 60:
            fingerprints.add(stripped_authority)
        if path.suffix.lower() == ".md":
            fingerprints.update(
                paragraph.strip()
                for paragraph in authority_text.split("\n\n")
                if len(paragraph.strip()) >= 120
            )
            continue
        try:
            parsed = json.loads(authority_text)
        except json.JSONDecodeError as error:
            raise PackagingError(f"evaluation authority is invalid JSON: {relative}: {error}") from error

        def collect(value: object) -> None:
            if isinstance(value, dict):
                for key, child in value.items():
                    if key in FINGERPRINT_KEYS:
                        fingerprints.update(
                            item.strip() for item in nested_strings(child) if len(item.strip()) >= 60
                        )
                    collect(child)
            elif isinstance(value, list):
                for child in value:
                    collect(child)

        collect(parsed)
    return fingerprints


def reject_evaluation_content(
    source_root: Path, files: list[tuple[PurePosixPath, bytes]]
) -> None:
    fingerprints = evaluation_fingerprints(source_root)
    for relative, content in files:
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as error:
            raise PackagingError(f"runtime source must be UTF-8 text: {relative}") from error
        lowered = text.lower()
        if any(marker in lowered for marker in FORBIDDEN_EVALUATION_CONTENT_MARKERS):
            raise PackagingError(
                f"evaluation control marker found in runtime source: {relative}"
            )
        if any(fingerprint in text for fingerprint in fingerprints):
            raise PackagingError(
                f"evaluation case or answer fingerprint found in runtime source: {relative}"
            )


def package_manifest(
    allowlist_relative: PurePosixPath,
    allowlist_bytes: bytes,
    package_root_relative: PurePosixPath,
    files: list[tuple[PurePosixPath, bytes]],
) -> dict:
    entries = [
        {
            "path": relative.as_posix(),
            "sha256": sha256_bytes(content),
            "size_bytes": len(content),
        }
        for relative, content in files
    ]
    identity_payload = {
        "files": entries,
        "schema_version": 1,
        "source_allowlist_sha256": sha256_bytes(allowlist_bytes),
    }
    return {
        "file_count": len(entries),
        "files": entries,
        "identity_algorithm": IDENTITY_ALGORITHM,
        "package_identity_sha256": sha256_bytes(canonical_json_bytes(identity_payload)),
        "package_root": package_root_relative.as_posix(),
        "schema_version": 1,
        "source_allowlist": {
            "path": allowlist_relative.as_posix(),
            "sha256": sha256_bytes(allowlist_bytes),
        },
    }


def validate_destinations(
    source_root: Path, package_dir: Path, manifest_out: Path
) -> tuple[Path, Path]:
    package_dir = package_dir.absolute()
    manifest_out = manifest_out.absolute()
    source_root_resolved = source_root.resolve()
    package_dir_resolved = package_dir.resolve(strict=False)
    manifest_out_resolved = manifest_out.resolve(strict=False)

    if relative_to(package_dir_resolved, source_root_resolved):
        raise PackagingError("model-visible package directory must be outside the source repository")
    if not relative_to(manifest_out_resolved, source_root_resolved):
        raise PackagingError("package manifest must be written inside the source repository")
    required_manifest_root = source_root_resolved / "evidence" / "evaluations"
    if not relative_to(manifest_out_resolved, required_manifest_root):
        raise PackagingError(
            "package manifest must be under evidence/evaluations/<iteration>/"
        )
    if manifest_out.name != "runtime-package-manifest.json":
        raise PackagingError("package manifest filename must be runtime-package-manifest.json")
    if relative_to(manifest_out_resolved, package_dir_resolved):
        raise PackagingError("package manifest must remain outside the model-visible package")
    if package_dir.exists() or package_dir.is_symlink():
        raise PackagingError(f"package destination already exists: {package_dir}")
    if manifest_out.exists() or manifest_out.is_symlink():
        raise PackagingError(f"package manifest already exists: {manifest_out}")
    return package_dir, manifest_out


def write_package(
    package_dir: Path,
    manifest_out: Path,
    files: list[tuple[PurePosixPath, bytes]],
    manifest: dict,
) -> tuple[bytes, str]:
    package_dir.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=".strategic-advisor-runtime-", dir=package_dir.parent)
    )
    manifest_bytes = rendered_json_bytes(manifest)
    temporary_manifest = manifest_out.parent / f".{manifest_out.name}.tmp"
    package_committed = False
    try:
        if temporary_manifest.exists() or temporary_manifest.is_symlink():
            raise PackagingError(f"temporary manifest path already exists: {temporary_manifest}")
        for relative, content in files:
            destination = staging / Path(*relative.parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
            os.chmod(destination, 0o644)
        temporary_manifest.write_bytes(manifest_bytes)
        os.chmod(temporary_manifest, 0o644)
        staging.replace(package_dir)
        package_committed = True
        temporary_manifest.replace(manifest_out)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        if package_committed and package_dir.exists() and not package_dir.is_symlink():
            shutil.rmtree(package_dir)
        if temporary_manifest.exists() and not temporary_manifest.is_symlink():
            temporary_manifest.unlink()
        raise
    return manifest_bytes, sha256_bytes(manifest_bytes)


def build(
    source_root: Path,
    allowlist_path: str,
    package_dir: Path,
    manifest_out: Path,
) -> dict:
    source_root = source_root.absolute()
    if source_root.is_symlink() or not source_root.is_dir():
        raise PackagingError(f"source root must be a real directory: {source_root}")
    allowlist_relative = normalized_relative_path(allowlist_path, "allowlist path")
    package_dir, manifest_out = validate_destinations(
        source_root, package_dir, manifest_out
    )
    allowlist, allowlist_bytes, _ = load_allowlist(source_root, allowlist_relative)
    package_root_relative, files = collect_files(source_root, allowlist)
    reject_evaluation_content(source_root, files)
    manifest = package_manifest(
        allowlist_relative,
        allowlist_bytes,
        package_root_relative,
        files,
    )
    _, manifest_sha256 = write_package(
        package_dir, manifest_out, files, manifest
    )
    return {
        "file_count": len(files),
        "package_identity_sha256": manifest["package_identity_sha256"],
        "package_manifest_path": manifest_out.relative_to(source_root).as_posix(),
        "package_manifest_sha256": manifest_sha256,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an allowlisted, content-addressed runtime skill package."
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root containing the source allowlist.",
    )
    parser.add_argument(
        "--allowlist",
        default=DEFAULT_ALLOWLIST,
        help="Normalized repository-relative source allowlist path.",
    )
    parser.add_argument(
        "--package-dir",
        type=Path,
        required=True,
        help="New model-visible package directory outside the source repository.",
    )
    parser.add_argument(
        "--manifest-out",
        type=Path,
        required=True,
        help="New provenance manifest under evidence/evaluations/<iteration>/.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        summary = build(
            source_root=args.source_root,
            allowlist_path=args.allowlist,
            package_dir=args.package_dir,
            manifest_out=args.manifest_out,
        )
    except (OSError, PackagingError) as error:
        print(f"ERROR [RUNTIME_PACKAGE]: {error}", file=sys.stderr)
        return 1
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
