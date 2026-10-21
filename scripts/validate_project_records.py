#!/usr/bin/env python3
"""Validate project records against the current candidate schema bundle.

This is a bounded software validator, not a scientific correctness oracle.
It checks JSON/YAML parsing, candidate JSON Schemas, mapped cross-record
references, per-project primary-ID uniqueness, status/reason consistency,
and local source/artifact paths that can be checked on the current host.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml
from yaml.constructor import ConstructorError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_TOOLS = ROOT / "schema" / "v1.4.3.7" / "tools"
if str(SCHEMA_TOOLS) not in sys.path:
    sys.path.insert(0, str(SCHEMA_TOOLS))

from cross_record_validate import PRIMARY, validate_records  # noqa: E402

SUPPORTED_SUFFIXES = {".json", ".yaml", ".yml"}
IGNORED_PARTS = {".git", ".venv", "__pycache__", "node_modules"}
CHECK_STATUS_VALUES = {
    "not_run", "in_progress", "passed", "failed", "inconclusive",
    "blocked", "needs_review", "stale", "not_applicable",
}
STATUS_ENUMS = {
    ("claim", "claim_lifecycle_status"): {"draft", "active", "superseded", "withdrawn"},
    ("source", "lifecycle_status"): {"current", "stale", "superseded", "withdrawn"},
    ("relation_edge", "lifecycle_status"): {"active", "superseded", "archived", "withdrawn"},
}
LOCAL_REFERENCE_FIELDS = {
    ("source", "uri_or_path"),
    ("artifact", "path_or_uri"),
}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise ConstructorError(
                "while constructing a mapping", node.start_mark,
                "unhashable mapping key", key_node.start_mark,
            ) from exc
        if duplicate:
            raise ConstructorError(
                "while constructing a mapping", node.start_mark,
                f"duplicate key {key!r}", key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def _json_object_without_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _display_path(path: Path, project_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(project_root.resolve()))
    except (ValueError, OSError):
        return str(path)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_document(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text, object_pairs_hook=_json_object_without_duplicate_keys)
    return yaml.load(text, Loader=UniqueKeyLoader)


def _load_records(records_dir: Path, project_root: Path, output_path: Path | None):
    records = []
    errors = []
    input_files = []
    if not records_dir.is_dir():
        return records, [{"code": "RECORDS_DIR_NOT_FOUND", "path": str(records_dir)}], input_files

    for path in sorted(records_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        relative_parts = path.relative_to(records_dir).parts
        if any(part in IGNORED_PARTS for part in relative_parts):
            continue
        if output_path is not None and path.resolve() == output_path.resolve():
            continue

        input_files.append({
            "path": _display_path(path, project_root),
            "sha256": _sha256_file(path),
        })
        try:
            record = _load_document(path)
        except Exception as exc:
            errors.append({
                "code": "RECORD_PARSE_ERROR",
                "path": _display_path(path, project_root),
                "message": str(exc),
            })
            continue

        if not isinstance(record, dict):
            errors.append({
                "code": "RECORD_NOT_OBJECT",
                "path": _display_path(path, project_root),
                "message": "Each record file must contain one mapping/object.",
            })
            continue
        if not isinstance(record.get("record_type"), str) or not record["record_type"].strip():
            errors.append({
                "code": "RECORD_TYPE_REQUIRED",
                "path": _display_path(path, project_root),
                "message": "Every record must declare a non-empty record_type.",
            })
            continue
        records.append((path, record))

    if not records:
        errors.append({
            "code": "NO_RECORDS_FOUND",
            "path": _display_path(records_dir, project_root),
            "message": "No parseable JSON/YAML project records were found.",
        })
    return records, errors, input_files


def _load_schemas(schemas_dir: Path):
    schemas = {}
    errors = []
    if not schemas_dir.is_dir():
        return schemas, [{
            "code": "SCHEMAS_DIR_NOT_FOUND",
            "path": str(schemas_dir),
        }]
    for path in sorted(schemas_dir.glob("*.schema.json")):
        name = path.name.removesuffix(".schema.json")
        try:
            schemas[name] = json.loads(
                path.read_text(encoding="utf-8"),
                object_pairs_hook=_json_object_without_duplicate_keys,
            )
        except Exception as exc:
            errors.append({
                "code": "SCHEMA_PARSE_ERROR",
                "path": str(path),
                "message": str(exc),
            })
    if not schemas:
        errors.append({
            "code": "NO_SCHEMAS_FOUND",
            "path": str(schemas_dir),
        })
    return schemas, errors


def _schema_declares_enum(schemas, record_type, field):
    prop = schemas.get(record_type, {}).get("properties", {}).get(field, {})
    return "enum" in prop or "const" in prop


def _reason_is_present(record: dict, field: str) -> bool:
    candidates = {"reason", "status_reason", "not_applicable_reason"}
    if field.endswith("_status"):
        candidates.add(field[:-len("_status")] + "_reason")
    return any(
        isinstance(record.get(name), str) and record[name].strip()
        for name in candidates
    )


def _check_global_ids(records, project_root: Path):
    """Enforce the design rule that IDs share one namespace within a project."""
    errors = []
    seen = {}
    for path, record in records:
        record_type = record.get("record_type")
        id_field = PRIMARY.get(record_type)
        record_id = record.get(id_field) if id_field else None
        if not isinstance(record_id, str) or not record_id:
            continue
        project_id = record.get("project_id")
        key = (project_id, record_id)
        previous = seen.get(key)
        if previous is not None and previous[0] != record_type:
            errors.append({
                "code": "DUPLICATE_ID_ACROSS_TYPES",
                "path": _display_path(path, project_root),
                "record_type": record_type,
                "id": record_id,
                "first_record_type": previous[0],
                "first_path": _display_path(previous[1], project_root),
                "project_id": project_id,
            })
        else:
            seen.setdefault(key, (record_type, path))
    return errors


def _check_statuses_and_reasons(records, schemas, project_root: Path):
    errors = []
    for path, record in records:
        record_type = record.get("record_type")
        for (owner, field), allowed in STATUS_ENUMS.items():
            if owner != record_type or field not in record or record[field] is None:
                continue
            if record[field] not in allowed and not _schema_declares_enum(schemas, owner, field):
                errors.append({
                    "code": "INVALID_STATUS",
                    "path": _display_path(path, project_root),
                    "field": field,
                    "value": record[field],
                    "allowed": sorted(allowed),
                })

        seen_objects = set()

        def walk(value, json_path="$"):
            if not isinstance(value, (dict, list)):
                return
            identity = id(value)
            if identity in seen_objects:
                return
            seen_objects.add(identity)

            if isinstance(value, dict):
                if "check_status" in value:
                    status = value["check_status"]
                    if status not in CHECK_STATUS_VALUES:
                        errors.append({
                            "code": "INVALID_CHECK_STATUS",
                            "path": _display_path(path, project_root),
                            "json_path": json_path + "/check_status",
                            "value": status,
                            "allowed": sorted(CHECK_STATUS_VALUES),
                        })
                    if status == "not_applicable" and not _reason_is_present(value, "check_status"):
                        errors.append({
                            "code": "NOT_APPLICABLE_REASON_REQUIRED",
                            "path": _display_path(path, project_root),
                            "json_path": json_path,
                            "field": "check_status",
                        })

                for key, child in value.items():
                    if key.endswith("_status") and child == "not_applicable":
                        if not _reason_is_present(value, key):
                            errors.append({
                                "code": "NOT_APPLICABLE_REASON_REQUIRED",
                                "path": _display_path(path, project_root),
                                "json_path": json_path + "/" + str(key),
                                "field": key,
                            })
                    walk(child, json_path + "/" + str(key))
            else:
                for index, child in enumerate(value):
                    walk(child, json_path + "/" + str(index))

        walk(record)
    return errors


def _is_windows_absolute(value: str) -> bool:
    return bool(re.match(r"^[A-Za-z]:[\\/]", value) or value.startswith("\\\\"))


def _check_local_references(records, project_root: Path):
    errors = []
    warnings = []
    root = project_root.resolve()

    if not project_root.is_dir():
        return [{"code": "PROJECT_ROOT_NOT_FOUND", "path": str(project_root)}], warnings

    for path, record in records:
        record_type = record.get("record_type")
        for owner, field in LOCAL_REFERENCE_FIELDS:
            if owner != record_type:
                continue
            value = record.get(field)
            if not isinstance(value, str) or not value.strip():
                continue
            value = value.strip()

            if _is_windows_absolute(value):
                warnings.append({
                    "code": "WINDOWS_PATH_NOT_CHECKED",
                    "path": _display_path(path, root),
                    "field": field,
                    "value": value,
                    "reason": "A remote Linux CI runner cannot verify a Windows-local path.",
                })
                continue

            parsed = urlparse(value)
            if parsed.scheme and parsed.scheme.lower() != "file":
                continue
            if parsed.scheme.lower() == "file":
                local_value = unquote(parsed.path)
                if re.match(r"^/[A-Za-z]:/", local_value):
                    warnings.append({
                        "code": "WINDOWS_FILE_URI_NOT_CHECKED",
                        "path": _display_path(path, root),
                        "field": field,
                        "value": value,
                    })
                    continue
                candidate = Path(local_value)
            else:
                candidate = Path(value)

            resolved = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                errors.append({
                    "code": "LOCAL_PATH_OUTSIDE_PROJECT_ROOT",
                    "path": _display_path(path, root),
                    "field": field,
                    "value": value,
                    "project_root": str(root),
                })
                continue

            if not resolved.exists():
                errors.append({
                    "code": "LOCAL_PATH_MISSING",
                    "path": _display_path(path, root),
                    "field": field,
                    "value": value,
                })
                continue

            if record_type == "source" and not resolved.is_file():
                errors.append({
                    "code": "SOURCE_PATH_NOT_FILE",
                    "path": _display_path(path, root),
                    "field": field,
                    "value": value,
                })
            if record_type == "artifact":
                kind = record.get("artifact_storage_kind")
                if kind == "file" and not resolved.is_file():
                    errors.append({
                        "code": "ARTIFACT_FILE_PATH_NOT_FILE",
                        "path": _display_path(path, root),
                        "field": field,
                        "value": value,
                    })
                if kind == "directory" and not resolved.is_dir():
                    errors.append({
                        "code": "ARTIFACT_DIRECTORY_PATH_NOT_DIRECTORY",
                        "path": _display_path(path, root),
                        "field": field,
                        "value": value,
                    })
    return errors, warnings


def validate_project_records(
    records_dir: Path | str,
    project_root: Path | str,
    schemas_dir: Path | str,
    output_path: Path | str | None = None,
):
    """Return a deterministic validation report without modifying input records."""
    records_dir = Path(records_dir).resolve()
    project_root = Path(project_root).resolve()
    schemas_dir = Path(schemas_dir).resolve()
    output = Path(output_path).resolve() if output_path is not None else None

    records, load_errors, input_files = _load_records(records_dir, project_root, output)
    schemas, schema_errors = _load_schemas(schemas_dir)

    cross = validate_records(records, schemas, validate_schema=bool(schemas))
    id_errors = _check_global_ids(records, project_root)
    extra_errors = _check_statuses_and_reasons(records, schemas, project_root)
    path_errors, path_warnings = _check_local_references(records, project_root)

    errors = load_errors + schema_errors + cross["errors"] + id_errors + extra_errors + path_errors
    warnings = cross["warnings"] + path_warnings

    for item in errors + warnings:
        if isinstance(item.get("path"), str):
            candidate = Path(item["path"])
            if candidate.is_absolute():
                item["path"] = _display_path(candidate, project_root)

    errors.sort(key=lambda item: (
        str(item.get("path", "")), str(item.get("code", "")),
        str(item.get("field", "")), str(item.get("target_id", "")),
    ))
    warnings.sort(key=lambda item: (
        str(item.get("path", "")), str(item.get("code", "")),
    ))
    input_files.sort(key=lambda item: item["path"])

    return {
        "validator": "high-energy-theory-research project-record validator",
        "schema_bundle": "v1.4.3.7-candidate",
        "summary": {
            "records": len(records),
            "input_files": len(input_files),
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "scope": [
            "JSON and YAML record parsing; duplicate mapping keys are rejected",
            "candidate JSON Schema validation",
            "explicit cross-record references and bounded candidate semantic checks",
            "primary-ID uniqueness across record types within each project",
            "known status enums and not_applicable reason requirements",
            "local source/artifact path existence and project-root containment",
        ],
        "not_implemented": [
            "complete state-machine transition coverage for every namespace",
            "canonical directory-manifest digest recomputation and full filesystem inventory",
            "state-transition event payload-hash recomputation",
            "scientific correctness, independent physics validation, or experimental acceptance",
        ],
        "input_files": input_files,
        "errors": errors,
        "warnings": warnings,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate JSON/YAML project records against the current candidate schema bundle."
    )
    parser.add_argument("records_dir", help="Directory containing only project record JSON/YAML files")
    parser.add_argument("--project-root", default=".", help="Root against which local record paths are resolved")
    parser.add_argument(
        "--schemas-dir",
        default=str(ROOT / "schema" / "v1.4.3.7" / "schemas"),
        help="Candidate JSON Schema directory",
    )
    parser.add_argument("--output", default="project-record-validation-report.json")
    args = parser.parse_args(argv)

    output_path = Path(args.output).resolve()
    report = validate_project_records(
        args.records_dir, args.project_root, args.schemas_dir, output_path=output_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"Report: {output_path}")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
