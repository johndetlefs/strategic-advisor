#!/usr/bin/env python3
"""Build, migrate, or validate the public Strategy Workspace scaffold.

This standard-library tool operates only on the public eight-file contract. It
never discovers, updates, or reads an owner workspace unless the caller names
that exact directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPOSITORY_ROOT / "skills" / "strategic-advisor"
TEMPLATE_ROOT = SKILL_ROOT / "workspace-templates"
ORIGIN_STATUSES = {
    "Observation",
    "Report",
    "Inference",
    "Assumption",
    "Unknown",
    "Preference",
    "Forecast",
}
DECISION_STATUSES = {"Active", "Superseded", "Reversed", "Closed"}
CHANGE_STATUSES = {"Approved", "Applied", "Rejected"}
NONE_VALUE = "None"
ID_PATTERNS = {
    "WORKSPACE.md": re.compile(r"CTX-\d{3,}$"),
    "PROFILE.md": re.compile(r"PRO-\d{3,}$"),
    "OBJECTIVES.md": re.compile(r"OBJ-\d{3,}$"),
    "PORTFOLIO.md": re.compile(r"PORT-\d{3,}$"),
    "CONTEXTS.md": re.compile(r"RCTX-\d{3,}$"),
    "CLAIMS.md": re.compile(r"CLM-\d{3,}$"),
    "DECISIONS.md": re.compile(r"DEC-\d{3,}$"),
    "CHANGELOG.md": re.compile(r"CHG-\d{3,}$"),
}
RETENTION_MODES = {"durable-full", "durable-bounded", "session-only"}
OPTIONAL_DETAIL_ROOTS = {"projects", "contexts"}
LEGACY_FILES = {
    "WORKSPACE.md",
    "PORTFOLIO.md",
    "CLAIMS.md",
    "DECISIONS.md",
    "CHANGELOG.md",
}
LINK_COLUMNS = ("Link ID", "Path", "Purpose", "Owner approval")
FILE_SPECS = {
    "WORKSPACE.md": {
        "headings": (
            "# Strategy Workspace",
            "## Authority",
            "## Workspace scope",
            "## Approved context",
            "## Operating notes",
        ),
        "columns": (
            "Context ID",
            "Statement",
            "Origin status",
            "Provenance",
            "Last checked",
            "Review by",
            "Limitations",
            "Owner approval",
        ),
    },
    "PROFILE.md": {
        "headings": ("# Personal Profile", "## Durable facts", "## Review notes"),
        "columns": (
            "Profile ID",
            "Category",
            "Exact fact",
            "Strategic relevance",
            "Origin status",
            "Provenance",
            "Last checked",
            "Review by",
            "Limitations",
            "Authority basis",
        ),
    },
    "OBJECTIVES.md": {
        "headings": ("# Objectives", "## Objective register", "## Review notes"),
        "columns": (
            "Objective ID",
            "Outcome",
            "Horizon",
            "Priority",
            "Success measure",
            "Constraints",
            "Origin status",
            "Provenance",
            "Last checked",
            "Review by",
            "Authority basis",
        ),
    },
    "PORTFOLIO.md": {
        "headings": ("# Portfolio", "## Portfolio roles", "## Review notes"),
        "columns": (
            "Portfolio ID",
            "Project or role",
            "Intended outcome",
            "Strategic role",
            "Commitment boundary",
            "Origin status",
            "Provenance",
            "Last checked",
            "Review by",
            "Owner approval",
        ),
    },
    "CONTEXTS.md": {
        "headings": ("# Recurring Contexts", "## Context register", "## Review notes"),
        "columns": (
            "Context ID",
            "Type",
            "Name",
            "Exact context",
            "Strategic relevance",
            "Origin status",
            "Provenance",
            "Last checked",
            "Review by",
            "Limitations",
            "Authority basis",
        ),
    },
    "CLAIMS.md": {
        "headings": (
            "# Material Claims",
            "## Claim ledger",
            "## Conflict and freshness attention",
        ),
        "columns": (
            "Claim ID",
            "Proposition",
            "Origin status",
            "Provenance",
            "Last checked",
            "Review by",
            "Support and limitations",
            "Conflict",
            "Falsifier",
            "Owner approval",
        ),
    },
    "DECISIONS.md": {
        "headings": (
            "# Durable Decisions",
            "## Decision register",
            "## Review queue",
        ),
        "columns": (
            "Decision ID",
            "Decision",
            "Status",
            "Basis claim IDs",
            "Decided on",
            "Review by",
            "Reversal trigger",
            "Supersedes",
            "Owner approval",
        ),
    },
    "CHANGELOG.md": {
        "headings": (
            "# Approved Change History",
            "## Write boundary",
            "## Change register",
        ),
        "columns": (
            "Change ID",
            "Target record",
            "Change summary",
            "Status",
            "Proposed on",
            "Approved on",
            "Owner approval",
            "Applied by",
        ),
    },
}
FORBIDDEN_MARKERS = {
    "PRIVATE_" + "CASE_DATA": "explicit private-case sentinel",
    '"expected_properties"': "evaluation expected-properties payload",
    "CASE-ASSERTION-GRADER": "evaluation grader material",
    "freeze-manifest": "evaluation freeze material",
    "SCORER-PROMPT": "evaluation scorer material",
}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
)


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    path: str
    record_id: str
    message: str

    def as_dict(self) -> dict[str, str]:
        value = {"code": self.code, "message": self.message, "path": self.path}
        if self.record_id:
            value["record_id"] = self.record_id
        return value


class WorkspaceError(ValueError):
    """Raised when a build cannot proceed safely."""


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def ensure_real_directory(path: Path, label: str) -> None:
    if path.is_symlink() or not path.is_dir():
        raise WorkspaceError(f"{label} must be an existing non-symlink directory: {path}")


def ensure_no_symlink_ancestor(path: Path) -> None:
    absolute = path.absolute()
    for ancestor in (absolute.parent, *absolute.parent.parents):
        # macOS exposes standard root aliases such as /var -> /private/var and
        # /tmp -> /private/tmp. Reject caller-controlled symlink components,
        # while allowing those single-component operating-system aliases.
        if (
            ancestor.exists()
            and ancestor.is_symlink()
            and len(ancestor.parts) > 2
        ):
            raise WorkspaceError(f"destination ancestor is a symlink: {ancestor}")


def canonical_templates() -> dict[str, bytes]:
    ensure_real_directory(TEMPLATE_ROOT, "template root")
    actual = {entry.name for entry in TEMPLATE_ROOT.iterdir()}
    expected = set(FILE_SPECS)
    if actual != expected:
        raise WorkspaceError(
            "template root differs from the approved file set: "
            f"missing={sorted(expected - actual)}, extra={sorted(actual - expected)}"
        )
    templates: dict[str, bytes] = {}
    for name in sorted(expected):
        path = TEMPLATE_ROOT / name
        if path.is_symlink() or not path.is_file():
            raise WorkspaceError(f"template must be a regular non-symlink file: {name}")
        templates[name] = path.read_bytes()
    return templates


def build_workspace(destination: Path) -> dict[str, object]:
    if os.path.lexists(destination):
        raise WorkspaceError(f"destination already exists; refusing overwrite: {destination}")
    ensure_no_symlink_ancestor(destination)
    parent = destination.absolute().parent
    ensure_real_directory(parent, "destination parent")
    templates = canonical_templates()
    temporary = Path(tempfile.mkdtemp(prefix=".strategy-workspace-", dir=parent))
    try:
        for name, content in templates.items():
            target = temporary / name
            with target.open("xb") as handle:
                handle.write(content)
        os.rename(temporary, destination)
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise
    files = [
        {"path": name, "sha256": sha256_bytes(content), "size_bytes": len(content)}
        for name, content in sorted(templates.items())
    ]
    return {
        "command": "build",
        "file_count": len(files),
        "files": files,
        "status": "built",
    }


def migrated_workspace_text(text: str) -> str:
    updated = text
    if "- Retention mode:" not in updated:
        marker = "## Workspace scope\n"
        if marker not in updated:
            raise WorkspaceError("legacy WORKSPACE.md is missing Workspace scope")
        updated = updated.replace(
            marker,
            marker
            + "\n- Retention mode: durable-bounded\n"
            + "- Durable boundary: Migrated legacy records pending owner review\n",
            1,
        )
    if "## Linked detail" not in updated:
        marker = "## Operating notes"
        if marker not in updated:
            raise WorkspaceError("legacy WORKSPACE.md is missing Operating notes")
        updated = updated.replace(
            marker,
            "## Linked detail\n\n"
            "| Link ID | Path | Purpose | Owner approval |\n"
            "| --- | --- | --- | --- |\n\n"
            + marker,
            1,
        )
    return updated


def migrate_workspace(source: Path, destination: Path) -> dict[str, object]:
    ensure_real_directory(source, "source workspace")
    source_entries = {entry.name for entry in source.iterdir()}
    if source_entries != LEGACY_FILES:
        raise WorkspaceError(
            "legacy source differs from the approved five-file contract: "
            f"missing={sorted(LEGACY_FILES - source_entries)}, "
            f"extra={sorted(source_entries - LEGACY_FILES)}"
        )
    for name in sorted(LEGACY_FILES):
        path = source / name
        if path.is_symlink() or not path.is_file():
            raise WorkspaceError(f"legacy source entry must be a regular file: {name}")
    if os.path.lexists(destination):
        raise WorkspaceError(f"destination already exists; refusing overwrite: {destination}")
    ensure_no_symlink_ancestor(destination)
    parent = destination.absolute().parent
    ensure_real_directory(parent, "destination parent")
    templates = canonical_templates()
    migrated = dict(templates)
    for name in sorted(LEGACY_FILES):
        migrated[name] = (source / name).read_bytes()
    migrated["WORKSPACE.md"] = migrated_workspace_text(
        migrated["WORKSPACE.md"].decode("utf-8")
    ).encode("utf-8")
    temporary = Path(tempfile.mkdtemp(prefix=".strategy-workspace-migrate-", dir=parent))
    try:
        for name, content in sorted(migrated.items()):
            with (temporary / name).open("xb") as handle:
                handle.write(content)
        os.rename(temporary, destination)
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise
    files = [
        {"path": name, "sha256": sha256_bytes(content), "size_bytes": len(content)}
        for name, content in sorted(migrated.items())
    ]
    return {
        "command": "migrate",
        "file_count": len(files),
        "files": files,
        "source": str(source),
        "status": "migrated",
    }


def split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def table_rows(
    name: str, text: str, errors: list[Finding]
) -> list[dict[str, str]]:
    columns = list(FILE_SPECS[name]["columns"])
    lines = text.splitlines()
    header_index = -1
    for index, line in enumerate(lines):
        if split_table_row(line) == columns:
            header_index = index
            break
    if header_index < 0:
        errors.append(
            Finding(
                "WORKSPACE_TABLE_SCHEMA",
                name,
                "",
                "required table header is missing or changed",
            )
        )
        return []
    if header_index + 1 >= len(lines):
        errors.append(
            Finding("WORKSPACE_TABLE_SCHEMA", name, "", "table separator is missing")
        )
        return []
    separators = split_table_row(lines[header_index + 1])
    if len(separators) != len(columns) or any(
        re.fullmatch(r":?-{3,}:?", value) is None for value in separators
    ):
        errors.append(
            Finding("WORKSPACE_TABLE_SCHEMA", name, "", "table separator is invalid")
        )
        return []
    rows: list[dict[str, str]] = []
    for line in lines[header_index + 2 :]:
        if not line.strip() or line.startswith("#"):
            break
        cells = split_table_row(line)
        if not cells:
            errors.append(
                Finding("WORKSPACE_TABLE_ROW", name, "", "non-table content appears in table")
            )
            continue
        if len(cells) != len(columns):
            errors.append(
                Finding(
                    "WORKSPACE_TABLE_ROW",
                    name,
                    cells[0] if cells else "",
                    f"row has {len(cells)} cells; expected {len(columns)}",
                )
            )
            continue
        if not any(cells):
            continue
        rows.append(dict(zip(columns, cells, strict=True)))
    return rows


def linked_detail_rows(text: str, errors: list[Finding]) -> list[dict[str, str]]:
    lines = text.splitlines()
    header_index = next(
        (index for index, line in enumerate(lines) if split_table_row(line) == list(LINK_COLUMNS)),
        -1,
    )
    if header_index < 0:
        errors.append(
            Finding("WORKSPACE_LINK_SCHEMA", "WORKSPACE.md", "", "linked-detail table is missing")
        )
        return []
    if header_index + 1 >= len(lines):
        errors.append(
            Finding("WORKSPACE_LINK_SCHEMA", "WORKSPACE.md", "", "linked-detail separator is missing")
        )
        return []
    separators = split_table_row(lines[header_index + 1])
    if len(separators) != len(LINK_COLUMNS) or any(
        re.fullmatch(r":?-{3,}:?", value) is None for value in separators
    ):
        errors.append(
            Finding("WORKSPACE_LINK_SCHEMA", "WORKSPACE.md", "", "linked-detail separator is invalid")
        )
        return []
    rows: list[dict[str, str]] = []
    for line in lines[header_index + 2 :]:
        if not line.strip() or line.startswith("#"):
            break
        cells = split_table_row(line)
        if len(cells) != len(LINK_COLUMNS):
            errors.append(
                Finding("WORKSPACE_LINK_ROW", "WORKSPACE.md", "", "linked-detail row is invalid")
            )
            continue
        if any(cells):
            rows.append(dict(zip(LINK_COLUMNS, cells, strict=True)))
    return rows


def required_value(
    row: dict[str, str],
    field: str,
    name: str,
    record_id: str,
    errors: list[Finding],
) -> None:
    if not row.get(field, "").strip():
        errors.append(
            Finding(
                "WORKSPACE_REQUIRED_FIELD",
                name,
                record_id,
                f"{field} must not be empty",
            )
        )


def parse_date_field(
    row: dict[str, str],
    field: str,
    name: str,
    record_id: str,
    errors: list[Finding],
) -> date | None:
    value = row.get(field, "").strip()
    if not value:
        required_value(row, field, name, record_id, errors)
        return None
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        errors.append(
            Finding(
                "WORKSPACE_DATE",
                name,
                record_id,
                f"{field} must use YYYY-MM-DD",
            )
        )
        return None
    if parsed.isoformat() != value:
        errors.append(
            Finding(
                "WORKSPACE_DATE",
                name,
                record_id,
                f"{field} must use normalized YYYY-MM-DD",
            )
        )
        return None
    return parsed


def canonical_logic_units() -> set[str]:
    units: set[str] = set()
    manifest = json.loads((SKILL_ROOT / "runtime-manifest.json").read_text(encoding="utf-8"))
    for relative in manifest["include"]:
        if relative.startswith("workspace-templates/") or relative == "references/strategy-workspace.md":
            continue
        path = SKILL_ROOT / relative
        if path.suffix.lower() not in {".md", ".txt"} or not path.is_file():
            continue
        for paragraph in re.split(r"\n\s*\n", path.read_text(encoding="utf-8")):
            normalized = re.sub(r"\s+", " ", paragraph).strip().lower()
            if len(normalized) >= 180 and len(normalized.split()) >= 24:
                units.add(normalized)
    return units


def content_findings(name: str, text: str, errors: list[Finding]) -> None:
    for marker, description in sorted(FORBIDDEN_MARKERS.items()):
        if marker.lower() in text.lower():
            errors.append(
                Finding(
                    "WORKSPACE_FORBIDDEN_CONTENT",
                    name,
                    "",
                    f"workspace contains {description}",
                )
            )
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(
                Finding(
                    "WORKSPACE_SECRET",
                    name,
                    "",
                    "workspace contains a secret-like pattern",
                )
            )
            break
    normalized = re.sub(r"\s+", " ", text).strip().lower()
    if any(unit in normalized for unit in canonical_logic_units()):
        errors.append(
            Finding(
                "WORKSPACE_COPIED_LOGIC",
                name,
                "",
                "workspace contains an exact substantial canonical strategy block",
            )
        )


def validate_rows(
    name: str,
    rows: list[dict[str, str]],
    as_of: date,
    seen_ids: set[str],
    references: list[tuple[str, str, str, str]],
    errors: list[Finding],
    attention: list[Finding],
) -> None:
    id_field = FILE_SPECS[name]["columns"][0]
    for row in rows:
        record_id = row.get(id_field, "").strip()
        if not ID_PATTERNS[name].fullmatch(record_id):
            errors.append(
                Finding(
                    "WORKSPACE_RECORD_ID",
                    name,
                    record_id,
                    f"{id_field} has an invalid format",
                )
            )
        elif record_id in seen_ids:
            errors.append(
                Finding(
                    "WORKSPACE_DUPLICATE_ID",
                    name,
                    record_id,
                    "record ID is duplicated",
                )
            )
        else:
            seen_ids.add(record_id)

        for field in FILE_SPECS[name]["columns"][1:]:
            required_value(row, field, name, record_id, errors)
        approval = row.get("Owner approval", row.get("Authority basis", "")).strip()
        if approval and not approval.startswith("Approved "):
            errors.append(
                Finding(
                    "WORKSPACE_OWNER_APPROVAL",
                    name,
                    record_id,
                    "Owner approval must be an explicit Approved reference",
                )
            )

        if "Origin status" in row and row["Origin status"] not in ORIGIN_STATUSES:
            errors.append(
                Finding(
                    "WORKSPACE_ORIGIN_STATUS",
                    name,
                    record_id,
                    "Origin status must use the canonical epistemic vocabulary",
                )
            )
        if name == "DECISIONS.md" and row["Status"] not in DECISION_STATUSES:
            errors.append(
                Finding(
                    "WORKSPACE_DECISION_STATUS",
                    name,
                    record_id,
                    "decision Status is invalid",
                )
            )
        if name == "CHANGELOG.md" and row["Status"] not in CHANGE_STATUSES:
            errors.append(
                Finding(
                    "WORKSPACE_CHANGE_STATUS",
                    name,
                    record_id,
                    "change Status is invalid",
                )
            )

        for field in ("Last checked", "Review by", "Decided on", "Proposed on", "Approved on"):
            if field not in row:
                continue
            parsed = parse_date_field(row, field, name, record_id, errors)
            if field == "Review by" and parsed is not None and parsed < as_of:
                attention.append(
                    Finding(
                        "WORKSPACE_STALE",
                        name,
                        record_id,
                        f"Review by {parsed.isoformat()} is before as-of {as_of.isoformat()}",
                    )
                )

        if name == "CLAIMS.md":
            if row["Falsifier"].strip() == NONE_VALUE:
                errors.append(
                    Finding(
                        "WORKSPACE_FALSIFIER",
                        name,
                        record_id,
                        "Falsifier must name a disconfirming condition",
                    )
                )
            conflict = row["Conflict"].strip()
            if conflict != NONE_VALUE:
                identifiers = [item.strip() for item in conflict.split(",") if item.strip()]
                if not identifiers or any(
                    re.fullmatch(r"CLM-\d{3,}", item) is None for item in identifiers
                ):
                    errors.append(
                        Finding(
                            "WORKSPACE_CONFLICT_FORMAT",
                            name,
                            record_id,
                            "Conflict must be None or a comma-separated list of CLM IDs",
                        )
                    )
                else:
                    references.extend(
                        (name, record_id, "Conflict", identifier)
                        for identifier in identifiers
                    )
                    attention.append(
                        Finding(
                            "WORKSPACE_CONFLICT",
                            name,
                            record_id,
                            f"declared conflict with {', '.join(identifiers)}",
                        )
                    )
        if name == "DECISIONS.md":
            if row["Reversal trigger"].strip() == NONE_VALUE:
                errors.append(
                    Finding(
                        "WORKSPACE_REVERSAL_TRIGGER",
                        name,
                        record_id,
                        "Reversal trigger must name a review or reversal condition",
                    )
                )
            for field, prefix in (("Basis claim IDs", "CLM"), ("Supersedes", "DEC")):
                value = row[field].strip()
                if field == "Supersedes" and value == NONE_VALUE:
                    continue
                identifiers = [item.strip() for item in value.split(",") if item.strip()]
                if not identifiers or any(
                    re.fullmatch(rf"{prefix}-\d{{3,}}", item) is None for item in identifiers
                ):
                    errors.append(
                        Finding(
                            "WORKSPACE_REFERENCE_FORMAT",
                            name,
                            record_id,
                            f"{field} must contain {prefix} IDs"
                            + (" or None" if field == "Supersedes" else ""),
                        )
                    )
                else:
                    references.extend(
                        (name, record_id, field, identifier)
                        for identifier in identifiers
                    )


def validate_workspace(workspace: Path, as_of: date) -> dict[str, object]:
    errors: list[Finding] = []
    attention: list[Finding] = []
    if workspace.is_symlink() or not workspace.is_dir():
        errors.append(
            Finding(
                "WORKSPACE_ROOT",
                str(workspace),
                "",
                "workspace must be an existing non-symlink directory",
            )
        )
        return validation_result(as_of, errors, attention, 0)
    entries = {entry.name for entry in workspace.iterdir()}
    expected = set(FILE_SPECS)
    for name in sorted(expected - entries):
        errors.append(Finding("WORKSPACE_FILE_MISSING", name, "", "required file is missing"))
    for name in sorted(entries - expected - OPTIONAL_DETAIL_ROOTS):
        errors.append(
            Finding("WORKSPACE_FILE_EXTRA", name, "", "file is outside the approved scaffold")
        )
    workspace_text = ""
    workspace_path = workspace / "WORKSPACE.md"
    if workspace_path.is_file() and not workspace_path.is_symlink():
        try:
            workspace_text = workspace_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            pass
    mode_matches = re.findall(
        r"(?m)^- Retention mode:\s*(\S+)\s*$",
        workspace_text,
    )
    if len(mode_matches) != 1 or mode_matches[0] not in RETENTION_MODES:
        errors.append(
            Finding(
                "WORKSPACE_RETENTION_MODE",
                "WORKSPACE.md",
                "",
                "Retention mode must declare exactly one of durable-full, durable-bounded, or session-only",
            )
        )
    for authority in (
        "Read",
        "Durable write",
        "External action",
        "Disclosure",
        "Cross-workspace",
    ):
        if re.search(rf"(?m)^- {re.escape(authority)}:", workspace_text) is None:
            errors.append(
                Finding(
                    "WORKSPACE_AUTHORITY_SCHEMA",
                    "WORKSPACE.md",
                    "",
                    f"authority declaration is missing: {authority}",
                )
            )
    link_rows = linked_detail_rows(workspace_text, errors) if workspace_text else []
    declared_paths: set[str] = set()
    seen_link_ids: set[str] = set()
    for row in link_rows:
        link_id = row["Link ID"].strip()
        relative = row["Path"].strip()
        approval = row["Owner approval"].strip()
        if re.fullmatch(r"LINK-\d{3,}", link_id) is None or link_id in seen_link_ids:
            errors.append(
                Finding(
                    "WORKSPACE_LINK_ID",
                    "WORKSPACE.md",
                    link_id,
                    "Link ID must be unique and use LINK-NNN",
                )
            )
        seen_link_ids.add(link_id)
        parts = Path(relative).parts
        if (
            not relative
            or Path(relative).is_absolute()
            or ".." in parts
            or len(parts) < 2
            or parts[0] not in OPTIONAL_DETAIL_ROOTS
            or Path(relative).suffix.lower() != ".md"
        ):
            errors.append(
                Finding(
                    "WORKSPACE_LINK_PATH",
                    "WORKSPACE.md",
                    link_id,
                    "linked path must be a relative Markdown file under projects/ or contexts/",
                )
            )
        elif relative in declared_paths:
            errors.append(
                Finding(
                    "WORKSPACE_LINK_PATH",
                    "WORKSPACE.md",
                    link_id,
                    "linked path is duplicated",
                )
            )
        else:
            declared_paths.add(relative)
        if not row["Purpose"].strip():
            errors.append(
                Finding("WORKSPACE_REQUIRED_FIELD", "WORKSPACE.md", link_id, "Purpose must not be empty")
            )
        if not approval.startswith("Approved "):
            errors.append(
                Finding(
                    "WORKSPACE_OWNER_APPROVAL",
                    "WORKSPACE.md",
                    link_id,
                    "Owner approval must be an explicit Approved reference",
                )
            )
    actual_paths: set[str] = set()
    for root_name in sorted(OPTIONAL_DETAIL_ROOTS & entries):
        detail_root = workspace / root_name
        if detail_root.is_symlink() or not detail_root.is_dir():
            errors.append(
                Finding(
                    "WORKSPACE_FILE_TYPE",
                    root_name,
                    "",
                    "optional detail root must be a regular non-symlink directory",
                )
            )
            continue
        for path in sorted(detail_root.rglob("*")):
            relative = path.relative_to(workspace).as_posix()
            if path.is_symlink() or (path.is_file() and path.suffix.lower() != ".md"):
                errors.append(
                    Finding(
                        "WORKSPACE_FILE_TYPE",
                        relative,
                        "",
                        "linked detail must contain only regular non-symlink Markdown files",
                    )
                )
                continue
            if path.is_file():
                actual_paths.add(relative)
                try:
                    content_findings(relative, path.read_text(encoding="utf-8"), errors)
                except UnicodeDecodeError:
                    errors.append(
                        Finding("WORKSPACE_ENCODING", relative, "", "file must be valid UTF-8")
                    )
    for relative in sorted(declared_paths - actual_paths):
        errors.append(
            Finding("WORKSPACE_LINK_MISSING", relative, "", "declared linked detail is missing")
        )
    for relative in sorted(actual_paths - declared_paths):
        errors.append(
            Finding("WORKSPACE_LINK_UNDECLARED", relative, "", "linked detail is not declared")
        )
    seen_ids: set[str] = set()
    references: list[tuple[str, str, str, str]] = []
    validated_files = 0
    for name in sorted(expected & entries):
        path = workspace / name
        if path.is_symlink() or not path.is_file():
            errors.append(
                Finding(
                    "WORKSPACE_FILE_TYPE",
                    name,
                    "",
                    "workspace entry must be a regular non-symlink file",
                )
            )
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(
                Finding("WORKSPACE_ENCODING", name, "", "file must be valid UTF-8")
            )
            continue
        validated_files += 1
        for heading in FILE_SPECS[name]["headings"]:
            if heading not in text.splitlines():
                errors.append(
                    Finding(
                        "WORKSPACE_HEADING",
                        name,
                        "",
                        f"required heading is missing: {heading}",
                    )
                )
        content_findings(name, text, errors)
        rows = table_rows(name, text, errors)
        validate_rows(name, rows, as_of, seen_ids, references, errors, attention)
    for name, record_id, field, target in references:
        if target not in seen_ids:
            errors.append(
                Finding(
                    "WORKSPACE_REFERENCE_MISSING",
                    name,
                    record_id,
                    f"{field} references missing record {target}",
                )
            )
    return validation_result(as_of, errors, attention, validated_files)


def validation_result(
    as_of: date,
    errors: list[Finding],
    attention: list[Finding],
    file_count: int,
) -> dict[str, object]:
    status = "invalid" if errors else ("valid_with_attention" if attention else "valid")
    return {
        "as_of": as_of.isoformat(),
        "attention": [item.as_dict() for item in sorted(set(attention))],
        "command": "validate",
        "errors": [item.as_dict() for item in sorted(set(errors))],
        "file_count": file_count,
        "status": status,
    }


def parse_as_of(value: str) -> date:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("--as-of must use YYYY-MM-DD") from error
    if parsed.isoformat() != value:
        raise argparse.ArgumentTypeError("--as-of must use normalized YYYY-MM-DD")
    return parsed


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build, migrate, or validate the public eight-file Strategy Workspace scaffold."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser("build", help="Build a new blank workspace.")
    build.add_argument("--destination", type=Path, required=True)
    migrate = subparsers.add_parser(
        "migrate", help="Copy a named legacy five-file workspace into the eight-file contract."
    )
    migrate.add_argument("--source", type=Path, required=True)
    migrate.add_argument("--destination", type=Path, required=True)
    validate = subparsers.add_parser("validate", help="Validate a named workspace.")
    validate.add_argument("--workspace", type=Path, required=True)
    validate.add_argument(
        "--as-of",
        type=parse_as_of,
        required=True,
        help="Explicit freshness date in YYYY-MM-DD form.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "build":
            result = build_workspace(args.destination)
            print(canonical_json(result))
            return 0
        if args.command == "migrate":
            result = migrate_workspace(args.source, args.destination)
            print(canonical_json(result))
            return 0
        result = validate_workspace(args.workspace, args.as_of)
        print(canonical_json(result))
        return 1 if result["errors"] else 0
    except (OSError, WorkspaceError, json.JSONDecodeError) as error:
        print(f"ERROR [STRATEGY_WORKSPACE]: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
