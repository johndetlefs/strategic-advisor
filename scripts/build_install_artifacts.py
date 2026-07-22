#!/usr/bin/env python3
"""Build and independently verify deterministic Strategic Advisor archives.

The runtime-package builder remains the authority for selecting model-visible
Strategic Advisor files. This module adds the repository-root Apache-2.0
license, places those exact bytes into deterministic distribution envelopes,
and records external provenance. The plugin archive is an OpenAI local
marketplace bundle for Codex and ChatGPT desktop Work mode only; it is neither
a Personal Skill upload nor a public Plugin Directory submission package.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import stat
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Sequence


SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

import build_runtime_package as runtime_package  # noqa: E402


SKILL_NAME = "strategic-advisor"
PLUGIN_VERSION = "0.1.0-alpha.1"
PLUGIN_DESCRIPTION = (
    "Reality-tested strategic analysis for consequential professional decisions."
)
PLUGIN_AUTHOR = "Strategic Advisor contributors"
LICENSE_PATH = PurePosixPath("LICENSE")
APACHE_2_0_LICENSE_SHA256 = (
    "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4"
)
APACHE_2_0_LICENSE_SIZE_BYTES = 11357
FIXED_ZIP_DATETIME = (1980, 1, 1, 0, 0, 0)
FIXED_TIMESTAMP_TEXT = "1980-01-01T00:00:00"
FILE_MODE = 0o644
DIRECTORY_MODE = 0o755
ARCHIVE_ORDER = "ascending-posix-path-v1"
PROVENANCE_SCHEMA_VERSION = 2
STANDALONE_ARTIFACT_KEY = "standalone_skill"
OPENAI_MARKETPLACE_ARTIFACT_KEY = "openai_local_marketplace"
OPENAI_MARKETPLACE_TARGET_SURFACES = ["chatgpt-desktop-work", "codex"]
EXCLUDED_PLUGIN_DISTRIBUTION_CLAIMS = [
    "chatgpt-personal-skill-upload",
    "public-plugin-directory-submission",
]
MAX_ARCHIVE_ENTRIES = 512
MAX_ARCHIVE_UNCOMPRESSED_BYTES = 16 * 1024 * 1024
MAX_ARCHIVE_BYTES = 32 * 1024 * 1024
MAX_PROVENANCE_BYTES = 4 * 1024 * 1024


class InstallArtifactError(ValueError):
    """An install artifact violates its build or verification contract."""


@dataclass(frozen=True)
class ArchiveEntry:
    """One deterministic ZIP entry."""

    path: str
    content: bytes | None
    role: str

    @property
    def is_directory(self) -> bool:
        return self.content is None


@dataclass(frozen=True)
class SourcePackage:
    """Freshly collected canonical source inputs for one invocation."""

    allowlist_relative: PurePosixPath
    allowlist_bytes: bytes
    package_root_relative: PurePosixPath
    runtime_files: tuple[tuple[PurePosixPath, bytes], ...]
    runtime_manifest: dict
    license_bytes: bytes
    license_details: dict


@dataclass(frozen=True)
class ExpectedArchiveFile:
    """One independently expected verifier entry."""

    role: str
    sha256: str
    size_bytes: int
    content: bytes | None = None


def _directory_entry(path: str) -> ArchiveEntry:
    if not path.endswith("/"):
        raise InstallArtifactError(f"directory archive path must end in '/': {path}")
    return ArchiveEntry(path=path, content=None, role="directory")


def _file_entry(path: str, content: bytes, role: str) -> ArchiveEntry:
    if path.endswith("/"):
        raise InstallArtifactError(f"file archive path must not end in '/': {path}")
    return ArchiveEntry(path=path, content=content, role=role)


def _parent_directories(path: str) -> set[str]:
    pure_path = PurePosixPath(path)
    return {
        "/".join(pure_path.parts[:index]) + "/"
        for index in range(1, len(pure_path.parts))
    }


def _entries_with_directories(files: list[ArchiveEntry]) -> list[ArchiveEntry]:
    by_path: dict[str, ArchiveEntry] = {}
    for entry in files:
        if entry.is_directory:
            raise InstallArtifactError("archive file input unexpectedly contains a directory")
        if entry.path in by_path:
            raise InstallArtifactError(f"duplicate archive path: {entry.path}")
        by_path[entry.path] = entry
        for directory in _parent_directories(entry.path):
            existing = by_path.get(directory)
            if existing is not None and not existing.is_directory:
                raise InstallArtifactError(
                    f"archive path is both a file and directory: {directory}"
                )
            by_path[directory] = _directory_entry(directory)
    return [by_path[path] for path in sorted(by_path)]


def _zip_info(entry: ArchiveEntry) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(entry.path, date_time=FIXED_ZIP_DATETIME)
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.extra = b""
    info.comment = b""
    if entry.is_directory:
        info.external_attr = ((stat.S_IFDIR | DIRECTORY_MODE) << 16) | 0x10
    else:
        info.external_attr = (stat.S_IFREG | FILE_MODE) << 16
    return info


def build_zip(entries: list[ArchiveEntry]) -> bytes:
    """Render entries as a deterministic, uncompressed ZIP archive."""

    ordered = _entries_with_directories(entries)
    buffer = io.BytesIO()
    with zipfile.ZipFile(
        buffer,
        mode="w",
        compression=zipfile.ZIP_STORED,
        allowZip64=True,
        strict_timestamps=True,
    ) as archive:
        archive.comment = b""
        for entry in ordered:
            archive.writestr(_zip_info(entry), entry.content or b"")
    return buffer.getvalue()


def _normalized_archive_path(raw: str, is_directory: bool) -> PurePosixPath:
    if (
        not raw
        or "\\" in raw
        or any(ord(character) < 32 or ord(character) == 127 for character in raw)
    ):
        raise InstallArtifactError(f"archive path is empty or not POSIX-normalized: {raw!r}")
    if is_directory:
        if not raw.endswith("/"):
            raise InstallArtifactError(f"archive directory lacks trailing slash: {raw}")
        candidate = raw[:-1]
    else:
        if raw.endswith("/"):
            raise InstallArtifactError(f"archive file has trailing slash: {raw}")
        candidate = raw
    path = PurePosixPath(candidate)
    expected = path.as_posix() + ("/" if is_directory else "")
    if (
        not candidate
        or path.is_absolute()
        or "." in path.parts
        or ".." in path.parts
        or raw != expected
    ):
        raise InstallArtifactError(
            f"archive path contains traversal or is not normalized: {raw}"
        )
    return path


def _inventory_item(
    info: zipfile.ZipInfo,
    index: int,
    role: str,
    content: bytes | None,
) -> dict:
    is_directory = info.is_dir()
    expected_mode = DIRECTORY_MODE if is_directory else FILE_MODE
    item = {
        "compression": "ZIP_STORED",
        "kind": "directory" if is_directory else "file",
        "mode": f"{expected_mode:04o}",
        "order": index,
        "path": info.filename,
        "role": "directory" if is_directory else role,
        "timestamp": FIXED_TIMESTAMP_TEXT,
    }
    if content is not None:
        item["sha256"] = runtime_package.sha256_bytes(content)
        item["size_bytes"] = len(content)
    return item


def _validate_zip_metadata(info: zipfile.ZipInfo) -> None:
    is_directory = info.is_dir()
    _normalized_archive_path(info.filename, is_directory)
    expected_mode = DIRECTORY_MODE if is_directory else FILE_MODE
    expected_type = stat.S_IFDIR if is_directory else stat.S_IFREG
    actual_mode = (info.external_attr >> 16) & 0o777
    actual_type = (info.external_attr >> 16) & 0o170000
    if info.date_time != FIXED_ZIP_DATETIME:
        raise InstallArtifactError(
            f"archive timestamp drift for {info.filename}: {info.date_time}"
        )
    if info.compress_type != zipfile.ZIP_STORED:
        raise InstallArtifactError(f"archive compression drift for {info.filename}")
    if info.create_system != 3:
        raise InstallArtifactError(f"archive creator system drift for {info.filename}")
    if info.extra or info.comment:
        raise InstallArtifactError(f"archive entry metadata must be empty: {info.filename}")
    if info.flag_bits & 0x1:
        raise InstallArtifactError(f"encrypted archive entry is forbidden: {info.filename}")
    if actual_mode != expected_mode or actual_type != expected_type:
        raise InstallArtifactError(
            f"archive permission or file-type drift for {info.filename}"
        )
    if is_directory and info.file_size != 0:
        raise InstallArtifactError(f"archive directory is not empty: {info.filename}")


def archive_inventory(archive_bytes: bytes, roles: dict[str, str]) -> list[dict]:
    """Describe actual built entries and reject deterministic-metadata drift."""

    inventory: list[dict] = []
    with zipfile.ZipFile(io.BytesIO(archive_bytes), mode="r") as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if names != sorted(names) or len(names) != len(set(names)):
            raise InstallArtifactError("archive entry order is not unique lexicographic order")
        if archive.comment:
            raise InstallArtifactError("archive comment must be empty")
        for index, info in enumerate(infos):
            _validate_zip_metadata(info)
            content = None if info.is_dir() else archive.read(info)
            if not info.is_dir() and info.filename not in roles:
                raise InstallArtifactError(f"archive entry has no role: {info.filename}")
            inventory.append(
                _inventory_item(
                    info,
                    index,
                    "directory" if info.is_dir() else roles[info.filename],
                    content,
                )
            )
    return inventory


def plugin_manifest_bytes() -> bytes:
    """Return a parser-valid, skills-only OpenAI plugin manifest."""

    return runtime_package.rendered_json_bytes(
        {
            "author": {"name": PLUGIN_AUTHOR},
            "description": PLUGIN_DESCRIPTION,
            "interface": {
                "capabilities": [],
                "category": "Productivity",
                "defaultPrompt": [
                    "Use Strategic Advisor to reality-test this decision."
                ],
                "developerName": PLUGIN_AUTHOR,
                "displayName": "Strategic Advisor",
                "longDescription": (
                    "Reality-tested strategic analysis with explicit evidence, "
                    "uncertainty, rival explanations, and decision tests."
                ),
                "shortDescription": "Reality-test consequential decisions.",
            },
            "license": "Apache-2.0",
            "name": SKILL_NAME,
            "skills": "./skills/",
            "version": PLUGIN_VERSION,
        }
    )


def marketplace_manifest_bytes() -> bytes:
    """Return the deterministic repo-local OpenAI marketplace catalog."""

    return runtime_package.rendered_json_bytes(
        {
            "interface": {"displayName": "Strategic Advisor"},
            "name": SKILL_NAME,
            "plugins": [
                {
                    "category": "Productivity",
                    "name": SKILL_NAME,
                    "policy": {
                        "authentication": "ON_INSTALL",
                        "installation": "AVAILABLE",
                    },
                    "source": {
                        "path": "./plugins/strategic-advisor",
                        "source": "local",
                    },
                }
            ],
        }
    )


def _source_provenance(source_root: Path) -> dict:
    """Observe Git state without upgrading an unavailable or dirty state."""

    try:
        top_level = subprocess.run(
            ["git", "-C", str(source_root), "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            timeout=10,
        )
        if top_level.returncode != 0:
            return {"revision": None, "tree_state": "not-git"}
        top_level_path = Path(os.fsdecode(top_level.stdout.strip())).resolve()
        if top_level_path != source_root.resolve():
            return {"revision": None, "tree_state": "not-git-root"}
        revision_result = subprocess.run(
            ["git", "-C", str(source_root), "rev-parse", "--verify", "HEAD^{commit}"],
            check=False,
            capture_output=True,
            timeout=10,
        )
        status_result = subprocess.run(
            [
                "git",
                "-C",
                str(source_root),
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ],
            check=False,
            capture_output=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return {"revision": None, "tree_state": "git-unavailable"}

    revision = revision_result.stdout.strip().decode("ascii", errors="ignore").lower()
    if (
        revision_result.returncode != 0
        or len(revision) not in {40, 64}
        or any(character not in "0123456789abcdef" for character in revision)
    ):
        return {"revision": None, "tree_state": "unborn-or-invalid-head"}
    if status_result.returncode != 0:
        return {"revision": revision, "tree_state": "status-unavailable"}
    return {
        "revision": revision,
        "tree_state": "dirty" if status_result.stdout else "clean",
    }


def _require_release_source(snapshot: dict, allow_dirty: bool) -> None:
    if allow_dirty:
        return
    if snapshot["tree_state"] == "dirty":
        raise InstallArtifactError(
            "source Git tree is dirty; commit the exact source or pass --allow-dirty "
            "for a non-release exploratory artifact"
        )
    if snapshot["tree_state"] != "clean" or snapshot["revision"] is None:
        raise InstallArtifactError(
            "release build requires a clean Git repository root with an available "
            f"HEAD and status; observed {snapshot['tree_state']!r}. Pass --allow-dirty "
            "only for an inexact exploratory artifact"
        )


def _git_show(source_root: Path, revision: str, relative: PurePosixPath) -> bytes:
    try:
        result = subprocess.run(
            ["git", "-C", str(source_root), "show", f"{revision}:{relative.as_posix()}"],
            check=False,
            capture_output=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise InstallArtifactError(
            f"git show is unavailable for source input {relative}"
        ) from error
    if result.returncode != 0:
        raise InstallArtifactError(
            f"git show could not read source input at {revision}:{relative}"
        )
    return result.stdout


def _license_details(
    license_bytes: bytes,
    runtime_files: tuple[tuple[PurePosixPath, bytes], ...],
) -> dict:
    return {
        "apache_2_0_canonical": True,
        "included": True,
        "plugin_archive_path": (
            "plugins/strategic-advisor/skills/strategic-advisor/LICENSE"
        ),
        "provenance": "repository-root-apache-2.0",
        "runtime_allowlisted": LICENSE_PATH in dict(runtime_files),
        "sha256": runtime_package.sha256_bytes(license_bytes),
        "size_bytes": len(license_bytes),
        "source_repository_path": LICENSE_PATH.as_posix(),
        "standalone_archive_path": "strategic-advisor/LICENSE",
    }


def _load_license(
    source_root: Path,
    runtime_files: tuple[tuple[PurePosixPath, bytes], ...],
) -> tuple[bytes, dict]:
    """Load only the complete canonical repository-root Apache-2.0 license."""

    license_source = runtime_package.reject_symlink_chain(
        source_root, LICENSE_PATH, "root Apache-2.0 LICENSE"
    )
    if not license_source.is_file():
        raise InstallArtifactError("repository-root LICENSE is missing or not a regular file")
    license_bytes = license_source.read_bytes()
    license_sha256 = runtime_package.sha256_bytes(license_bytes)
    if (
        len(license_bytes) != APACHE_2_0_LICENSE_SIZE_BYTES
        or license_sha256 != APACHE_2_0_LICENSE_SHA256
    ):
        raise InstallArtifactError(
            "repository-root LICENSE is not the complete canonical Apache License 2.0 "
            f"text (expected sha256 {APACHE_2_0_LICENSE_SHA256})"
        )
    runtime_license = dict(runtime_files).get(LICENSE_PATH)
    if runtime_license is not None and runtime_license != license_bytes:
        raise InstallArtifactError(
            "runtime-allowlisted LICENSE differs from the repository-root Apache-2.0 LICENSE"
        )
    return license_bytes, _license_details(license_bytes, runtime_files)


def _collect_source_package(source_root: Path, allowlist_path: str) -> SourcePackage:
    if allowlist_path != runtime_package.DEFAULT_ALLOWLIST:
        raise InstallArtifactError(
            "install artifacts require the canonical runtime allowlist at "
            f"{runtime_package.DEFAULT_ALLOWLIST}"
        )
    allowlist_relative = runtime_package.normalized_relative_path(
        allowlist_path, "allowlist path"
    )
    allowlist, allowlist_bytes, _ = runtime_package.load_allowlist(
        source_root, allowlist_relative
    )
    package_root_relative, collected = runtime_package.collect_files(
        source_root, allowlist
    )
    runtime_files = tuple(collected)
    runtime_package.reject_evaluation_content(source_root, list(runtime_files))
    runtime_manifest = runtime_package.package_manifest(
        allowlist_relative,
        allowlist_bytes,
        package_root_relative,
        list(runtime_files),
    )
    license_bytes, license_details = _load_license(source_root, runtime_files)
    return SourcePackage(
        allowlist_relative=allowlist_relative,
        allowlist_bytes=allowlist_bytes,
        package_root_relative=package_root_relative,
        runtime_files=runtime_files,
        runtime_manifest=runtime_manifest,
        license_bytes=license_bytes,
        license_details=license_details,
    )


def _source_input_map(source: SourcePackage) -> dict[PurePosixPath, bytes]:
    inputs = {source.allowlist_relative: source.allowlist_bytes}
    for relative, content in source.runtime_files:
        path = PurePosixPath(source.package_root_relative, relative)
        existing = inputs.get(path)
        if existing is not None and existing != content:
            raise InstallArtifactError(f"conflicting source input bytes for {path}")
        inputs[path] = content
    inputs[LICENSE_PATH] = source.license_bytes
    return inputs


def _verify_git_inputs(
    source_root: Path,
    revision: str,
    source: SourcePackage,
) -> list[dict]:
    """Prove every selected input byte equals ``git show <revision>:<path>``."""

    verified: list[dict] = []
    for relative, content in sorted(
        _source_input_map(source).items(), key=lambda item: item[0].as_posix()
    ):
        head_content = _git_show(source_root, revision, relative)
        if head_content != content:
            raise InstallArtifactError(
                f"source input differs from git show {revision}:{relative}"
            )
        verified.append(
            {
                "path": relative.as_posix(),
                "sha256": runtime_package.sha256_bytes(content),
                "size_bytes": len(content),
            }
        )
    return verified


def _standalone_files(source: SourcePackage) -> tuple[list[ArchiveEntry], dict[str, str]]:
    files: list[ArchiveEntry] = []
    roles: dict[str, str] = {}
    for relative, content in source.runtime_files:
        path = f"{SKILL_NAME}/{relative.as_posix()}"
        role = "runtime-license" if relative == LICENSE_PATH else "runtime"
        files.append(_file_entry(path, content, role))
        roles[path] = role
    if LICENSE_PATH not in dict(source.runtime_files):
        path = f"{SKILL_NAME}/LICENSE"
        files.append(_file_entry(path, source.license_bytes, "license"))
        roles[path] = "license"
    return files, roles


def _plugin_files(source: SourcePackage) -> tuple[list[ArchiveEntry], dict[str, str]]:
    marketplace_path = ".agents/plugins/marketplace.json"
    plugin_manifest_path = "plugins/strategic-advisor/.codex-plugin/plugin.json"
    files = [
        _file_entry(
            marketplace_path, marketplace_manifest_bytes(), "marketplace-metadata"
        ),
        _file_entry(plugin_manifest_path, plugin_manifest_bytes(), "plugin-metadata"),
    ]
    roles = {
        marketplace_path: "marketplace-metadata",
        plugin_manifest_path: "plugin-metadata",
    }
    plugin_skill_prefix = "plugins/strategic-advisor/skills/strategic-advisor"
    for relative, content in source.runtime_files:
        path = f"{plugin_skill_prefix}/{relative.as_posix()}"
        role = "runtime-license" if relative == LICENSE_PATH else "runtime"
        files.append(_file_entry(path, content, role))
        roles[path] = role
    if LICENSE_PATH not in dict(source.runtime_files):
        path = f"{plugin_skill_prefix}/LICENSE"
        files.append(_file_entry(path, source.license_bytes, "license"))
        roles[path] = "license"
    return files, roles


def _reject_symlinked_output_ancestors(path: Path) -> None:
    current = path.absolute()
    while True:
        if current.is_symlink():
            raise InstallArtifactError(
                f"output path traverses symlinked destination or ancestor: {current}"
            )
        parent = current.parent
        if parent == current:
            return
        current = parent


def _validate_output_paths(paths: list[Path]) -> list[Path]:
    absolute = [Path(os.path.abspath(os.fspath(path))) for path in paths]
    for path in absolute:
        _reject_symlinked_output_ancestors(path)
        if path.exists() or path.is_symlink():
            raise InstallArtifactError(f"output destination already exists: {path}")
        if path.name in {"", ".", ".."}:
            raise InstallArtifactError(f"output destination is not a file path: {path}")
    resolved = [path.resolve(strict=False) for path in absolute]
    if len(set(resolved)) != len(resolved):
        raise InstallArtifactError("output paths must be distinct")
    for index, left in enumerate(resolved):
        for right in resolved[index + 1 :]:
            if left in right.parents or right in left.parents:
                raise InstallArtifactError("output file paths must not contain one another")
    return absolute


def _write_outputs(outputs: list[tuple[Path, bytes]]) -> None:
    validated_paths = _validate_output_paths([path for path, _ in outputs])
    normalized_outputs = [
        (path, outputs[index][1]) for index, path in enumerate(validated_paths)
    ]
    created: list[Path] = []
    try:
        for path, content in normalized_outputs:
            path.parent.mkdir(parents=True, exist_ok=True)
            _reject_symlinked_output_ancestors(path)
            with path.open("xb") as handle:
                handle.write(content)
            os.chmod(path, FILE_MODE)
            created.append(path)
    except Exception:
        for path in reversed(created):
            if path.exists() and not path.is_symlink():
                path.unlink()
        raise


def _archive_policy() -> dict:
    return {
        "compression": "ZIP_STORED",
        "directory_mode": f"{DIRECTORY_MODE:04o}",
        "entry_order": ARCHIVE_ORDER,
        "file_mode": f"{FILE_MODE:04o}",
        "timestamp": FIXED_TIMESTAMP_TEXT,
        "timestamp_basis": "fixed ZIP DOS minimum tuple",
    }


def build(
    source_root: Path,
    allowlist_path: str,
    skill_archive_out: Path,
    plugin_archive_out: Path,
    provenance_out: Path,
    license_path: str = "LICENSE",
    allow_dirty: bool = False,
) -> dict:
    """Build deterministic archives and their external provenance document."""

    if license_path != LICENSE_PATH.as_posix():
        raise InstallArtifactError(
            "license path is fixed at the normalized repository-root LICENSE"
        )
    if allowlist_path != runtime_package.DEFAULT_ALLOWLIST:
        raise InstallArtifactError(
            "install artifacts require the canonical runtime allowlist at "
            f"{runtime_package.DEFAULT_ALLOWLIST}"
        )
    source_root = source_root.absolute()
    if source_root.is_symlink() or not source_root.is_dir():
        raise InstallArtifactError(f"source root must be a real directory: {source_root}")
    initial_snapshot = _source_provenance(source_root)
    _require_release_source(initial_snapshot, allow_dirty)
    skill_archive_out, plugin_archive_out, provenance_out = _validate_output_paths(
        [skill_archive_out, plugin_archive_out, provenance_out]
    )

    source = _collect_source_package(source_root, allowlist_path)
    verified_git_inputs: list[dict] = []
    if not allow_dirty:
        verified_git_inputs = _verify_git_inputs(
            source_root, initial_snapshot["revision"], source
        )

    standalone_files, standalone_roles = _standalone_files(source)
    plugin_files, plugin_roles = _plugin_files(source)
    skill_archive_bytes = build_zip(standalone_files)
    plugin_archive_bytes = build_zip(plugin_files)
    skill_inventory = archive_inventory(skill_archive_bytes, standalone_roles)
    plugin_inventory = archive_inventory(plugin_archive_bytes, plugin_roles)

    if not allow_dirty:
        final_snapshot = _source_provenance(source_root)
        if final_snapshot != initial_snapshot or final_snapshot["tree_state"] != "clean":
            raise InstallArtifactError(
                "Git source changed after inputs were read or while artifacts were built; "
                "no release outputs were written"
            )
        final_source = _collect_source_package(source_root, allowlist_path)
        if _source_input_map(final_source) != _source_input_map(source):
            raise InstallArtifactError(
                "release source bytes changed after collection; no outputs were written"
            )
        if (
            _verify_git_inputs(source_root, final_snapshot["revision"], final_source)
            != verified_git_inputs
        ):
            raise InstallArtifactError(
                "release Git input proof changed before write; no outputs were written"
            )

    provenance = {
        "archive_policy": _archive_policy(),
        "artifacts": {
            OPENAI_MARKETPLACE_ARTIFACT_KEY: {
                "distribution": "openai-local-marketplace-plugin",
                "excluded_distribution_claims": EXCLUDED_PLUGIN_DISTRIBUTION_CLAIMS,
                "format": "zip",
                "inventory": plugin_inventory,
                "sha256": runtime_package.sha256_bytes(plugin_archive_bytes),
                "size_bytes": len(plugin_archive_bytes),
                "target_surfaces": OPENAI_MARKETPLACE_TARGET_SURFACES,
            },
            STANDALONE_ARTIFACT_KEY: {
                "distribution": "agent-skills-archive",
                "format": "zip",
                "inventory": skill_inventory,
                "sha256": runtime_package.sha256_bytes(skill_archive_bytes),
                "size_bytes": len(skill_archive_bytes),
            },
        },
        "build_mode": "exploratory" if allow_dirty else "release",
        "git_source_verification": {
            "input_files": verified_git_inputs,
            "performed": not allow_dirty,
            "revision": None if allow_dirty else initial_snapshot["revision"],
            "status_rechecked_before_write": not allow_dirty,
        },
        "identity_algorithm": "sha256-install-artifacts-v2",
        "license": source.license_details,
        "runtime_package": source.runtime_manifest,
        "schema_version": PROVENANCE_SCHEMA_VERSION,
        "source_revision": initial_snapshot["revision"],
        "source_revision_exact": not allow_dirty,
        "source_tree_state": initial_snapshot["tree_state"],
    }
    provenance_bytes = runtime_package.rendered_json_bytes(provenance)
    _write_outputs(
        [
            (skill_archive_out, skill_archive_bytes),
            (plugin_archive_out, plugin_archive_bytes),
            (provenance_out, provenance_bytes),
        ]
    )
    return {
        "openai_local_marketplace_sha256": provenance["artifacts"][
            OPENAI_MARKETPLACE_ARTIFACT_KEY
        ]["sha256"],
        "provenance_sha256": runtime_package.sha256_bytes(provenance_bytes),
        "runtime_package_identity_sha256": source.runtime_manifest[
            "package_identity_sha256"
        ],
        "standalone_skill_sha256": provenance["artifacts"][
            STANDALONE_ARTIFACT_KEY
        ]["sha256"],
    }


def _strict_json_bytes(content: bytes, label: str) -> object:
    def object_pairs(pairs: list[tuple[str, object]]) -> dict:
        value: dict = {}
        for key, child in pairs:
            if key in value:
                raise InstallArtifactError(f"{label} contains duplicate JSON key: {key}")
            value[key] = child
        return value

    def reject_constant(value: str) -> object:
        raise InstallArtifactError(
            f"{label} contains non-standard JSON numeric constant: {value}"
        )

    try:
        return json.loads(
            content.decode("utf-8"),
            object_pairs_hook=object_pairs,
            parse_constant=reject_constant,
        )
    except UnicodeDecodeError as error:
        raise InstallArtifactError(f"{label} is not UTF-8") from error
    except json.JSONDecodeError as error:
        raise InstallArtifactError(f"{label} is not valid JSON: {error}") from error


def _read_regular_file(
    path: Path,
    label: str,
    maximum_size_bytes: int | None = None,
) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise InstallArtifactError(f"{label} is missing, symlinked, or not a regular file")
    if maximum_size_bytes is not None and path.stat().st_size > maximum_size_bytes:
        raise InstallArtifactError(f"{label} exceeds the verifier size limit")
    return path.read_bytes()


def _require_keys(value: object, keys: set[str], label: str) -> dict:
    if not isinstance(value, dict):
        raise InstallArtifactError(f"{label} must be a JSON object")
    actual = set(value)
    if actual != keys:
        raise InstallArtifactError(
            f"{label} fields mismatch; missing={sorted(keys - actual)}, "
            f"extra={sorted(actual - keys)}"
        )
    return value


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _validate_runtime_manifest_identity(manifest_value: object) -> dict:
    manifest = _require_keys(
        manifest_value,
        {
            "file_count",
            "files",
            "identity_algorithm",
            "package_identity_sha256",
            "package_root",
            "schema_version",
            "source_allowlist",
        },
        "runtime_package",
    )
    if manifest["schema_version"] != 1:
        raise InstallArtifactError("runtime_package schema_version must be 1")
    if manifest["identity_algorithm"] != runtime_package.IDENTITY_ALGORITHM:
        raise InstallArtifactError("runtime_package identity algorithm mismatch")
    package_root = runtime_package.normalized_relative_path(
        manifest["package_root"], "runtime_package package_root"
    )
    if package_root.as_posix() != "skills/strategic-advisor":
        raise InstallArtifactError("runtime_package package_root is not canonical")
    allowlist = _require_keys(
        manifest["source_allowlist"], {"path", "sha256"}, "source_allowlist"
    )
    runtime_package.normalized_relative_path(allowlist["path"], "source_allowlist path")
    if allowlist["path"] != runtime_package.DEFAULT_ALLOWLIST:
        raise InstallArtifactError(
            "runtime_package source_allowlist path must be the canonical "
            f"{runtime_package.DEFAULT_ALLOWLIST}"
        )
    if not _is_sha256(allowlist["sha256"]):
        raise InstallArtifactError("source_allowlist sha256 is invalid")
    files = manifest["files"]
    if not isinstance(files, list) or not files:
        raise InstallArtifactError("runtime_package files must be a non-empty array")
    normalized_files: list[dict] = []
    seen: set[str] = set()
    for index, raw_entry in enumerate(files):
        entry = _require_keys(
            raw_entry, {"path", "sha256", "size_bytes"}, f"runtime file[{index}]"
        )
        relative = runtime_package.normalized_relative_path(
            entry["path"], f"runtime file[{index}] path"
        )
        path = relative.as_posix()
        if path in seen:
            raise InstallArtifactError(f"duplicate runtime_package file path: {path}")
        seen.add(path)
        if not _is_sha256(entry["sha256"]):
            raise InstallArtifactError(f"runtime file sha256 is invalid: {path}")
        if (
            not isinstance(entry["size_bytes"], int)
            or isinstance(entry["size_bytes"], bool)
            or entry["size_bytes"] < 0
        ):
            raise InstallArtifactError(f"runtime file size is invalid: {path}")
        normalized_files.append(entry)
    if [entry["path"] for entry in normalized_files] != sorted(seen):
        raise InstallArtifactError("runtime_package files are not in canonical path order")
    if manifest["file_count"] != len(normalized_files):
        raise InstallArtifactError("runtime_package file_count mismatch")
    identity_payload = {
        "files": normalized_files,
        "schema_version": 1,
        "source_allowlist_sha256": allowlist["sha256"],
    }
    expected_identity = runtime_package.sha256_bytes(
        runtime_package.canonical_json_bytes(identity_payload)
    )
    if manifest["package_identity_sha256"] != expected_identity:
        raise InstallArtifactError("runtime_package identity does not recompute")
    return manifest


def _expected_archive_names(
    expected_files: dict[str, ExpectedArchiveFile],
) -> list[str]:
    names = set(expected_files)
    for path in expected_files:
        names.update(_parent_directories(path))
    return sorted(names)


def _verify_archive(
    path: Path,
    label: str,
    expected_files: dict[str, ExpectedArchiveFile],
) -> tuple[bytes, list[dict], dict[str, bytes]]:
    """Read an existing ZIP and independently validate bytes, layout, and metadata."""

    archive_bytes = _read_regular_file(path, label, MAX_ARCHIVE_BYTES)
    expected_names = _expected_archive_names(expected_files)
    inventory: list[dict] = []
    actual_files: dict[str, bytes] = {}
    try:
        with zipfile.ZipFile(io.BytesIO(archive_bytes), mode="r") as archive:
            if archive.comment:
                raise InstallArtifactError(f"{label} archive comment must be empty")
            infos = archive.infolist()
            if len(infos) > MAX_ARCHIVE_ENTRIES:
                raise InstallArtifactError(f"{label} exceeds the archive entry limit")
            if sum(info.file_size for info in infos) > MAX_ARCHIVE_UNCOMPRESSED_BYTES:
                raise InstallArtifactError(
                    f"{label} exceeds the uncompressed archive size limit"
                )
            names = [info.filename for info in infos]
            if names != sorted(names) or len(names) != len(set(names)):
                raise InstallArtifactError(
                    f"{label} entry order is not unique lexicographic order"
                )
            for info in infos:
                _validate_zip_metadata(info)
            if names != expected_names:
                missing = sorted(set(expected_names) - set(names))
                extra = sorted(set(names) - set(expected_names))
                expected_license_paths = {
                    name for name in expected_names if name.endswith("/LICENSE")
                }
                if expected_license_paths & set(missing):
                    raise InstallArtifactError(
                        f"{label} is missing the required root Apache-2.0 LICENSE entry"
                    )
                raise InstallArtifactError(
                    f"{label} archive root/layout mismatch; missing={missing}, extra={extra}"
                )
            for index, info in enumerate(infos):
                if info.is_dir():
                    inventory.append(
                        _inventory_item(info, index, "directory", None)
                    )
                    continue
                content = archive.read(info)
                expected = expected_files[info.filename]
                content_sha256 = runtime_package.sha256_bytes(content)
                if (
                    len(content) != expected.size_bytes
                    or content_sha256 != expected.sha256
                    or (
                        expected.content is not None
                        and content != expected.content
                    )
                ):
                    if info.filename.endswith("/LICENSE"):
                        raise InstallArtifactError(
                            f"{label} Apache-2.0 LICENSE bytes are missing or non-canonical"
                        )
                    if expected.role in {"plugin-metadata", "marketplace-metadata"}:
                        raise InstallArtifactError(
                            f"{label} OpenAI {expected.role} differs from canonical metadata"
                        )
                    raise InstallArtifactError(
                        f"{label} runtime content differs from provenance: "
                        f"{info.filename}"
                    )
                actual_files[info.filename] = content
                inventory.append(
                    _inventory_item(info, index, expected.role, content)
                )
    except zipfile.BadZipFile as error:
        raise InstallArtifactError(f"{label} is not a valid ZIP archive: {error}") from error
    return archive_bytes, inventory, actual_files


def _verify_artifact_record(
    record_value: object,
    label: str,
    archive_bytes: bytes,
    inventory: list[dict],
    *,
    openai_marketplace: bool,
) -> None:
    keys = {"distribution", "format", "inventory", "sha256", "size_bytes"}
    if openai_marketplace:
        keys.update({"excluded_distribution_claims", "target_surfaces"})
    record = _require_keys(record_value, keys, f"{label} artifact provenance")
    expected_distribution = (
        "openai-local-marketplace-plugin"
        if openai_marketplace
        else "agent-skills-archive"
    )
    if record["distribution"] != expected_distribution or record["format"] != "zip":
        raise InstallArtifactError(f"{label} distribution metadata mismatch")
    if openai_marketplace and (
        record["target_surfaces"] != OPENAI_MARKETPLACE_TARGET_SURFACES
        or record["excluded_distribution_claims"]
        != EXCLUDED_PLUGIN_DISTRIBUTION_CLAIMS
    ):
        raise InstallArtifactError("OpenAI local marketplace surface boundary mismatch")
    if record["inventory"] != inventory:
        raise InstallArtifactError(f"{label} provenance inventory does not match archive")
    if record["sha256"] != runtime_package.sha256_bytes(archive_bytes):
        raise InstallArtifactError(f"{label} provenance SHA-256 does not match archive")
    if record["size_bytes"] != len(archive_bytes):
        raise InstallArtifactError(f"{label} provenance size does not match archive")


def _validate_plugin_metadata(content: bytes, marketplace: bool) -> None:
    label = "OpenAI marketplace metadata" if marketplace else "OpenAI plugin metadata"
    parsed = _strict_json_bytes(content, label)
    if not isinstance(parsed, dict):
        raise InstallArtifactError(f"{label} must be a JSON object")
    expected = marketplace_manifest_bytes() if marketplace else plugin_manifest_bytes()
    if content != expected:
        raise InstallArtifactError(f"{label} is not canonical")


def _runtime_expectations(
    runtime_manifest: dict,
    prefix: str,
) -> dict[str, ExpectedArchiveFile]:
    expected: dict[str, ExpectedArchiveFile] = {}
    for entry in runtime_manifest["files"]:
        relative = runtime_package.normalized_relative_path(
            entry["path"], "runtime archive path"
        )
        if relative == LICENSE_PATH and (
            entry["sha256"] != APACHE_2_0_LICENSE_SHA256
            or entry["size_bytes"] != APACHE_2_0_LICENSE_SIZE_BYTES
        ):
            raise InstallArtifactError(
                "runtime-allowlisted LICENSE is not canonical Apache-2.0"
            )
        path = f"{prefix}/{relative.as_posix()}"
        expected[path] = ExpectedArchiveFile(
            role="runtime-license" if relative == LICENSE_PATH else "runtime",
            sha256=entry["sha256"],
            size_bytes=entry["size_bytes"],
        )
    if not any(entry["path"] == LICENSE_PATH.as_posix() for entry in runtime_manifest["files"]):
        expected[f"{prefix}/LICENSE"] = ExpectedArchiveFile(
            role="license",
            sha256=APACHE_2_0_LICENSE_SHA256,
            size_bytes=APACHE_2_0_LICENSE_SIZE_BYTES,
        )
    return expected


def _standalone_expectations(runtime_manifest: dict) -> dict[str, ExpectedArchiveFile]:
    return _runtime_expectations(runtime_manifest, SKILL_NAME)


def _plugin_expectations(runtime_manifest: dict) -> dict[str, ExpectedArchiveFile]:
    prefix = "plugins/strategic-advisor/skills/strategic-advisor"
    expected = _runtime_expectations(runtime_manifest, prefix)
    plugin_content = plugin_manifest_bytes()
    marketplace_content = marketplace_manifest_bytes()
    expected["plugins/strategic-advisor/.codex-plugin/plugin.json"] = (
        ExpectedArchiveFile(
            role="plugin-metadata",
            sha256=runtime_package.sha256_bytes(plugin_content),
            size_bytes=len(plugin_content),
            content=plugin_content,
        )
    )
    expected[".agents/plugins/marketplace.json"] = ExpectedArchiveFile(
        role="marketplace-metadata",
        sha256=runtime_package.sha256_bytes(marketplace_content),
        size_bytes=len(marketplace_content),
        content=marketplace_content,
    )
    return expected


def _expected_license_details(runtime_manifest: dict) -> dict:
    return {
        "apache_2_0_canonical": True,
        "included": True,
        "plugin_archive_path": (
            "plugins/strategic-advisor/skills/strategic-advisor/LICENSE"
        ),
        "provenance": "repository-root-apache-2.0",
        "runtime_allowlisted": any(
            entry["path"] == LICENSE_PATH.as_posix()
            for entry in runtime_manifest["files"]
        ),
        "sha256": APACHE_2_0_LICENSE_SHA256,
        "size_bytes": APACHE_2_0_LICENSE_SIZE_BYTES,
        "source_repository_path": LICENSE_PATH.as_posix(),
        "standalone_archive_path": "strategic-advisor/LICENSE",
    }


def _reject_consumer_visible_evaluation_content(
    runtime_manifest: dict,
    archive_files: dict[str, bytes],
    prefix: str,
) -> None:
    """Apply source-independent path and fixed-marker leakage checks."""

    for entry in runtime_manifest["files"]:
        relative = runtime_package.normalized_relative_path(
            entry["path"], "runtime verification path"
        )
        lowered_parts = [part.lower() for part in relative.parts]
        if set(lowered_parts) & runtime_package.FORBIDDEN_RUNTIME_PARTS or any(
            token in part
            for part in lowered_parts
            for token in runtime_package.FORBIDDEN_RUNTIME_TOKENS
        ):
            raise InstallArtifactError(
                f"evaluation or result path is forbidden in runtime archive: {relative}"
            )
        content = archive_files[f"{prefix}/{relative.as_posix()}"]
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as error:
            raise InstallArtifactError(
                f"runtime archive source is not UTF-8: {relative}"
            ) from error
        lowered = text.lower()
        if any(
            marker in lowered
            for marker in runtime_package.FORBIDDEN_EVALUATION_CONTENT_MARKERS
        ):
            raise InstallArtifactError(
                f"evaluation control marker found in runtime archive: {relative}"
            )


def _valid_revision(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) in {40, 64}
        and all(character in "0123456789abcdef" for character in value)
    )


def _expected_git_input_records(runtime_manifest: dict) -> dict[str, tuple[str, int | None]]:
    allowlist = runtime_manifest["source_allowlist"]
    expected: dict[str, tuple[str, int | None]] = {
        allowlist["path"]: (allowlist["sha256"], None),
        LICENSE_PATH.as_posix(): (
            APACHE_2_0_LICENSE_SHA256,
            APACHE_2_0_LICENSE_SIZE_BYTES,
        ),
    }
    package_root = PurePosixPath(runtime_manifest["package_root"])
    for entry in runtime_manifest["files"]:
        path = PurePosixPath(package_root, entry["path"]).as_posix()
        value = (entry["sha256"], entry["size_bytes"])
        existing = expected.get(path)
        if existing is not None and existing != value:
            raise InstallArtifactError(
                f"Git input provenance has conflicting source path: {path}"
            )
        expected[path] = value
    return expected


def _validate_git_provenance(provenance: dict, runtime_manifest: dict) -> None:
    git_verification = _require_keys(
        provenance["git_source_verification"],
        {"input_files", "performed", "revision", "status_rechecked_before_write"},
        "git_source_verification",
    )
    build_mode = provenance["build_mode"]
    tree_states = {
        "clean",
        "dirty",
        "git-unavailable",
        "not-git",
        "not-git-root",
        "status-unavailable",
        "unborn-or-invalid-head",
    }
    if provenance["source_tree_state"] not in tree_states:
        raise InstallArtifactError("source_tree_state is invalid")
    revision = provenance["source_revision"]
    if revision is not None and not _valid_revision(revision):
        raise InstallArtifactError("source_revision is invalid")

    if build_mode == "exploratory":
        if provenance["source_revision_exact"] is not False:
            raise InstallArtifactError("exploratory provenance must remain inexact")
        if git_verification != {
            "input_files": [],
            "performed": False,
            "revision": None,
            "status_rechecked_before_write": False,
        }:
            raise InstallArtifactError("exploratory Git provenance must remain inexact")
        return

    if build_mode != "release":
        raise InstallArtifactError("install provenance build_mode is invalid")
    if (
        provenance["source_tree_state"] != "clean"
        or provenance["source_revision_exact"] is not True
        or not _valid_revision(revision)
        or git_verification["performed"] is not True
        or git_verification["revision"] != revision
        or git_verification["status_rechecked_before_write"] is not True
    ):
        raise InstallArtifactError("release Git provenance is not exact and self-consistent")

    raw_records = git_verification["input_files"]
    if not isinstance(raw_records, list) or not raw_records:
        raise InstallArtifactError("release Git provenance input_files must be non-empty")
    actual: dict[str, tuple[str, int]] = {}
    ordered_paths: list[str] = []
    for index, raw_record in enumerate(raw_records):
        record = _require_keys(
            raw_record, {"path", "sha256", "size_bytes"}, f"Git input[{index}]"
        )
        relative = runtime_package.normalized_relative_path(
            record["path"], f"Git input[{index}] path"
        )
        path = relative.as_posix()
        if path in actual:
            raise InstallArtifactError(f"duplicate Git input path: {path}")
        if not _is_sha256(record["sha256"]):
            raise InstallArtifactError(f"Git input sha256 is invalid: {path}")
        if (
            not isinstance(record["size_bytes"], int)
            or isinstance(record["size_bytes"], bool)
            or record["size_bytes"] < 0
        ):
            raise InstallArtifactError(f"Git input size is invalid: {path}")
        ordered_paths.append(path)
        actual[path] = (record["sha256"], record["size_bytes"])
    if ordered_paths != sorted(ordered_paths):
        raise InstallArtifactError("Git input provenance is not in canonical path order")
    expected = _expected_git_input_records(runtime_manifest)
    if set(actual) != set(expected):
        raise InstallArtifactError("Git input provenance path set mismatch")
    for path, (expected_sha256, expected_size) in expected.items():
        actual_sha256, actual_size = actual[path]
        if actual_sha256 != expected_sha256 or (
            expected_size is not None and actual_size != expected_size
        ):
            raise InstallArtifactError(f"Git input provenance mismatch: {path}")


def verify(
    skill_archive: Path,
    plugin_archive: Path,
    provenance_path: Path,
    expected_provenance_sha256: str | None = None,
    expected_runtime_identity: str | None = None,
) -> dict:
    """Verify consumer artifacts without access to the source repository."""

    provenance_bytes = _read_regular_file(
        provenance_path, "install provenance", MAX_PROVENANCE_BYTES
    )
    provenance_sha256 = runtime_package.sha256_bytes(provenance_bytes)
    if expected_provenance_sha256 is not None:
        if not _is_sha256(expected_provenance_sha256):
            raise InstallArtifactError("expected provenance SHA-256 is invalid")
        if provenance_sha256 != expected_provenance_sha256:
            raise InstallArtifactError("trusted expected provenance SHA-256 mismatch")
    provenance_value = _strict_json_bytes(provenance_bytes, "install provenance")
    provenance = _require_keys(
        provenance_value,
        {
            "archive_policy",
            "artifacts",
            "build_mode",
            "git_source_verification",
            "identity_algorithm",
            "license",
            "runtime_package",
            "schema_version",
            "source_revision",
            "source_revision_exact",
            "source_tree_state",
        },
        "install provenance",
    )
    if provenance_bytes != runtime_package.rendered_json_bytes(provenance):
        raise InstallArtifactError("install provenance is not canonical rendered JSON")
    if provenance["schema_version"] != PROVENANCE_SCHEMA_VERSION:
        raise InstallArtifactError("install provenance schema_version mismatch")
    if provenance["identity_algorithm"] != "sha256-install-artifacts-v2":
        raise InstallArtifactError("install provenance identity algorithm mismatch")
    if provenance["archive_policy"] != _archive_policy():
        raise InstallArtifactError("install provenance archive policy mismatch")
    runtime_manifest = _validate_runtime_manifest_identity(
        provenance["runtime_package"]
    )
    if expected_runtime_identity is not None:
        if not _is_sha256(expected_runtime_identity):
            raise InstallArtifactError("expected runtime identity is invalid")
        if runtime_manifest["package_identity_sha256"] != expected_runtime_identity:
            raise InstallArtifactError("trusted expected runtime identity mismatch")
    if provenance["license"] != _expected_license_details(runtime_manifest):
        raise InstallArtifactError(
            "license provenance does not identify the canonical root Apache-2.0 LICENSE"
        )
    _validate_git_provenance(provenance, runtime_manifest)

    skill_archive_bytes, skill_inventory, skill_files = _verify_archive(
        skill_archive,
        "standalone skill",
        _standalone_expectations(runtime_manifest),
    )
    plugin_archive_bytes, plugin_inventory, plugin_files = _verify_archive(
        plugin_archive,
        "OpenAI local marketplace",
        _plugin_expectations(runtime_manifest),
    )

    plugin_manifest_path = "plugins/strategic-advisor/.codex-plugin/plugin.json"
    marketplace_path = ".agents/plugins/marketplace.json"
    _validate_plugin_metadata(plugin_files[plugin_manifest_path], marketplace=False)
    _validate_plugin_metadata(plugin_files[marketplace_path], marketplace=True)

    plugin_prefix = "plugins/strategic-advisor/skills/strategic-advisor"
    _reject_consumer_visible_evaluation_content(
        runtime_manifest, skill_files, SKILL_NAME
    )
    _reject_consumer_visible_evaluation_content(
        runtime_manifest, plugin_files, plugin_prefix
    )
    standalone_skill_files = {
        path.removeprefix(f"{SKILL_NAME}/"): content
        for path, content in skill_files.items()
    }
    plugin_skill_files = {
        path.removeprefix(f"{plugin_prefix}/"): content
        for path, content in plugin_files.items()
        if path.startswith(f"{plugin_prefix}/")
    }
    if standalone_skill_files != plugin_skill_files:
        raise InstallArtifactError(
            "OpenAI marketplace plugin skill bytes differ from standalone skill bytes"
        )

    artifacts = _require_keys(
        provenance["artifacts"],
        {OPENAI_MARKETPLACE_ARTIFACT_KEY, STANDALONE_ARTIFACT_KEY},
        "install provenance artifacts",
    )
    _verify_artifact_record(
        artifacts[STANDALONE_ARTIFACT_KEY],
        "standalone skill",
        skill_archive_bytes,
        skill_inventory,
        openai_marketplace=False,
    )
    _verify_artifact_record(
        artifacts[OPENAI_MARKETPLACE_ARTIFACT_KEY],
        "OpenAI local marketplace",
        plugin_archive_bytes,
        plugin_inventory,
        openai_marketplace=True,
    )

    return {
        "openai_local_marketplace_sha256": runtime_package.sha256_bytes(
            plugin_archive_bytes
        ),
        "provenance_sha256": provenance_sha256,
        "runtime_package_identity_sha256": runtime_manifest[
            "package_identity_sha256"
        ],
        "build_mode": provenance["build_mode"],
        "source_revision": provenance["source_revision"],
        "source_revision_exact": provenance["source_revision_exact"],
        "source_tree_state": provenance["source_tree_state"],
        "standalone_skill_sha256": runtime_package.sha256_bytes(
            skill_archive_bytes
        ),
        "trusted_provenance_sha256_matched": expected_provenance_sha256 is not None,
        "trusted_runtime_identity_matched": expected_runtime_identity is not None,
        "verification": "structural-and-internal-consistency-passed",
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a deterministic standalone skill ZIP and OpenAI local "
            "marketplace/plugin ZIP from the Strategic Advisor runtime allowlist."
        )
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Git repository root containing the runtime source allowlist.",
    )
    parser.add_argument(
        "--allowlist",
        default=runtime_package.DEFAULT_ALLOWLIST,
        choices=[runtime_package.DEFAULT_ALLOWLIST],
        help="Canonical repository-relative runtime allowlist path; overrides are forbidden.",
    )
    parser.add_argument(
        "--license",
        dest="license_path",
        choices=[LICENSE_PATH.as_posix()],
        default=LICENSE_PATH.as_posix(),
        help=(
            "Compatibility option fixed to the mandatory repository-root LICENSE; "
            "arbitrary license paths are forbidden."
        ),
    )
    parser.add_argument(
        "--skill-archive",
        type=Path,
        required=True,
        help="New output path for the standalone Agent Skills ZIP.",
    )
    parser.add_argument(
        "--plugin-archive",
        "--codex-plugin-archive",
        dest="plugin_archive",
        type=Path,
        required=True,
        help="New output path for the OpenAI local marketplace/plugin ZIP.",
    )
    parser.add_argument(
        "--provenance-out",
        type=Path,
        required=True,
        help="New output path for external install-artifact JSON provenance.",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help=(
            "Permit non-Git, unavailable-status, or dirty source for local exploration. "
            "The resulting provenance is always inexact and is not a release proof."
        ),
    )
    return parser


def _verify_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Independently verify existing Strategic Advisor install ZIPs and provenance."
        )
    )
    parser.add_argument("--skill-archive", type=Path, required=True)
    parser.add_argument(
        "--plugin-archive",
        "--codex-plugin-archive",
        dest="plugin_archive",
        type=Path,
        required=True,
    )
    parser.add_argument("--provenance", type=Path, required=True)
    parser.add_argument(
        "--expected-provenance-sha256",
        help=(
            "Optional trusted external SHA-256 for the provenance document. "
            "Without it, verification proves internal consistency, not publisher identity."
        ),
    )
    parser.add_argument(
        "--expected-runtime-identity",
        help="Optional trusted external runtime package identity SHA-256.",
    )
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    raw = list(sys.argv[1:] if argv is None else argv)
    if raw and raw[0] == "verify":
        args = _verify_parser().parse_args(raw[1:])
        args.command = "verify"
        return args
    if raw and raw[0] == "build":
        raw = raw[1:]
    args = _build_parser().parse_args(raw)
    args.command = "build"
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "verify":
            summary = verify(
                skill_archive=args.skill_archive,
                plugin_archive=args.plugin_archive,
                provenance_path=args.provenance,
                expected_provenance_sha256=args.expected_provenance_sha256,
                expected_runtime_identity=args.expected_runtime_identity,
            )
        else:
            summary = build(
                source_root=args.source_root,
                allowlist_path=args.allowlist,
                skill_archive_out=args.skill_archive,
                plugin_archive_out=args.plugin_archive,
                provenance_out=args.provenance_out,
                license_path=args.license_path,
                allow_dirty=args.allow_dirty,
            )
    except (
        OSError,
        InstallArtifactError,
        runtime_package.PackagingError,
        zipfile.BadZipFile,
    ) as error:
        print(f"ERROR [INSTALL_ARTIFACTS]: {error}", file=sys.stderr)
        return 1
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
