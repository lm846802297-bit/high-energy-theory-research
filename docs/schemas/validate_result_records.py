#!/usr/bin/env python3
"""Validate research result JSON records and their local output files."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from decimal import Decimal, InvalidOperation
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    print("ERROR: install the pinned dependency with python -m pip install -r docs/schemas/requirements-result-validation.txt.", file=sys.stderr)
    raise SystemExit(2)


def reject_nonstandard_constant(value: str):
    raise ValueError(f"non-standard JSON numeric constant is forbidden: {value}")


def parse_finite_float(value: str) -> float:
    """Reject JSON floats that overflow or underflow during binary-float parsing."""
    try:
        exact = Decimal(value)
        numeric = float(exact)
    except (InvalidOperation, OverflowError, ValueError) as exc:
        raise ValueError(f"invalid JSON numeric value: {value}") from exc
    if not math.isfinite(numeric):
        raise ValueError(f"JSON numeric value overflows a finite float: {value}")
    if exact != 0 and numeric == 0.0:
        raise ValueError(f"JSON numeric value underflows to zero: {value}")
    return numeric


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(
            stream,
            parse_constant=reject_nonstandard_constant,
            parse_float=parse_finite_float,
        )


def referenced_files(record: dict):
    if record.get("record_type") == "run_manifest":
        return record.get("outputs", [])
    if record.get("record_type") == "result_summary":
        return record.get("data_files", [])
    return []


def resolve_repo_path(root: Path, relative_path: str, errors: list):
    rel = Path(relative_path)
    if rel.is_absolute() or ".." in rel.parts:
        errors.append(f"{relative_path}: path must be repository-relative and cannot escape the repo")
        return None
    target = (root / rel).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        errors.append(f"{relative_path}: resolved path escapes repository root")
        return None
    return target


def verify_inputs(record: dict, repo_root: Path):
    errors, warnings = [], []
    if record.get("record_type") != "run_manifest":
        return errors, warnings
    root = repo_root.resolve()
    for item in record.get("inputs", []):
        if not item.get("path"):
            continue
        target = resolve_repo_path(root, item["path"], errors)
        if target is None:
            continue
        if not target.is_file():
            if item.get("uri"):
                warnings.append(f"{item['path']}: external input not present locally; URI/version retained")
            else:
                errors.append(f"{item['path']}: referenced input file does not exist")
            continue
        if item.get("bytes") is not None and target.stat().st_size != item["bytes"]:
            errors.append(f"{item['path']}: input byte size {target.stat().st_size} != manifest {item['bytes']}")
        if item.get("sha256"):
            digest = hashlib.sha256()
            with target.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            if digest.hexdigest() != item["sha256"]:
                errors.append(f"{item['path']}: input SHA-256 mismatch")
    return errors, warnings


def verify_artifacts(record: dict, repo_root: Path):
    errors, warnings = [], []
    root = repo_root.resolve()
    for item in referenced_files(record):
        target = resolve_repo_path(root, item["path"], errors)
        if target is None:
            continue
        if not target.is_file():
            if item.get("uri"):
                warnings.append(f"{item['path']}: external artifact not present locally; URI/version retained")
            else:
                errors.append(f"{item['path']}: referenced output file does not exist")
            continue

        actual_bytes = target.stat().st_size
        if actual_bytes != item["bytes"]:
            errors.append(f"{item['path']}: byte size {actual_bytes} != manifest {item['bytes']}")

        digest = hashlib.sha256()
        with target.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        if digest.hexdigest() != item["sha256"]:
            errors.append(f"{item['path']}: SHA-256 mismatch")

        if item["format"].lower() == "csv":
            try:
                with target.open("r", encoding="utf-8-sig", newline="") as stream:
                    reader = csv.reader(stream)
                    header = next(reader, None)
                    if header is None:
                        errors.append(f"{item['path']}: CSV is empty and has no header")
                        continue
                    if len(header) != len(set(header)):
                        errors.append(f"{item['path']}: duplicate CSV column names")
                    if item.get("columns") is not None and header != item["columns"]:
                        errors.append(f"{item['path']}: CSV header differs from manifest columns")
                    unit_columns = set(item.get("units", {}))
                    missing_unit_columns = set(header) - unit_columns
                    unknown_unit_columns = unit_columns - set(header)
                    if missing_unit_columns:
                        errors.append(f"{item['path']}: unit map is missing columns {sorted(missing_unit_columns)}")
                    if unknown_unit_columns:
                        errors.append(f"{item['path']}: unit map contains unknown columns {sorted(unknown_unit_columns)}")
                    row_count = 0
                    for row in reader:
                        row_count += 1
                        if len(row) != len(header):
                            errors.append(f"{item['path']}: row {row_count + 1} has {len(row)} fields; expected {len(header)}")
                            continue
                        for col_name, cell in zip(header, row):
                            if not cell.strip():
                                continue
                            try:
                                numeric = float(cell)
                            except ValueError:
                                continue
                            if not math.isfinite(numeric):
                                errors.append(f"{item['path']}: non-finite numeric value in {col_name}, data row {row_count}")
                    if item.get("rows") is not None and row_count != item["rows"]:
                        errors.append(f"{item['path']}: CSV has {row_count} data rows; manifest says {item['rows']}")
            except (OSError, UnicodeError, csv.Error) as exc:
                errors.append(f"{item['path']}: CSV read failed: {exc}")
    return errors, warnings


def verify_source(record: dict, repo_root: Path):
    if record.get("record_type") != "run_manifest" or record.get("schema_version") != "1.0.1":
        return []  # Preserve v1.0.0 validation behavior; source-byte checks are a v1.0.1 gate.
    errors = []
    source = record.get("source", {})
    target = resolve_repo_path(repo_root.resolve(), source.get("script_path", ""), errors)
    if target is None:
        return errors
    if not target.is_file():
        return [f"{source.get('script_path')}: source script does not exist"]
    digest = hashlib.sha256()
    with target.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    if digest.hexdigest() != source.get("script_sha256"):
        errors.append(f"{source.get('script_path')}: source script SHA-256 mismatch")
    return errors


def verify_revision_context(record: dict):
    """Check the semantic relationship between a PR head, base and tested checkout."""
    if record.get("record_type") != "run_manifest" or record.get("schema_version") != "1.0.1":
        return []
    source = record.get("source", {})
    context = source.get("revision_context")
    if not isinstance(context, dict):
        return ["v1.0.1 run_manifest is missing source.revision_context"]
    errors = []
    checked_out = context.get("checked_out_sha")
    if source.get("commit_sha") != checked_out:
        errors.append("source.commit_sha must equal source.revision_context.checked_out_sha")
    event = context.get("event_name")
    mode = context.get("checkout_mode")
    pr_number = context.get("pr_number")
    pr_head = context.get("pr_head_sha")
    base_sha = context.get("base_sha")
    tested_merge = context.get("tested_merge_sha")
    head_ref = context.get("head_ref")
    base_ref = context.get("base_ref")
    if event in {"pull_request", "pull_request_target"}:
        if not isinstance(pr_number, int) or pr_number < 1:
            errors.append("pull-request revision context requires a positive pr_number")
        if not isinstance(pr_head, str) or not isinstance(base_sha, str):
            errors.append("pull-request revision context requires pr_head_sha and base_sha")
        if not isinstance(head_ref, str) or not isinstance(base_ref, str):
            errors.append("pull-request revision context requires head_ref and base_ref")
        if source.get("branch") != head_ref:
            errors.append("source.branch must identify the PR head_ref, not the synthetic merge ref")
        if mode == "pull_request_merge":
            if not isinstance(tested_merge, str) or tested_merge != checked_out:
                errors.append("pull_request_merge requires tested_merge_sha equal to checked_out_sha")
        elif mode == "pull_request_head":
            if checked_out != pr_head:
                errors.append("pull_request_head requires checked_out_sha equal to pr_head_sha")
            if tested_merge is not None:
                errors.append("pull_request_head must not claim a tested_merge_sha")
        elif mode == "unknown":
            if tested_merge is not None and tested_merge != checked_out:
                errors.append("tested_merge_sha, when present, must equal checked_out_sha")
        else:
            errors.append("pull-request checkout_mode must be pull_request_merge, pull_request_head, or unknown")
    else:
        if any(value is not None for value in (pr_number, pr_head, base_sha, tested_merge)):
            errors.append("non-PR revision context must set PR-specific SHA/number fields to null")
        if mode in {"pull_request_merge", "pull_request_head"}:
            errors.append("non-PR revision context cannot use a pull-request checkout_mode")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", nargs="+", type=Path, help="JSON record files to validate")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(), help="repository root for output paths")
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().with_name("research-result-record-v1.0.1.schema.json"),
        help="JSON Schema Draft 2020-12 file",
    )
    args = parser.parse_args()

    try:
        schema = load_json(args.schema)
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        print(f"ERROR: invalid schema {args.schema}: {exc}", file=sys.stderr)
        return 2

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    failed = False
    for record_path in args.records:
        try:
            record = load_json(record_path)
        except Exception as exc:
            print(f"FAIL {record_path}: JSON parse error: {exc}")
            failed = True
            continue

        errors = sorted(
            validator.iter_errors(record),
            key=lambda error: (list(map(str, error.absolute_path)), error.message),
        )
        if errors:
            print(f"FAIL {record_path}: schema validation")
            for error in errors:
                location = ".".join(map(str, error.absolute_path)) or "<root>"
                print(f"  - {location}: {error.message}")
            failed = True
            continue

        input_errors, input_warnings = verify_inputs(record, args.repo_root)
        file_errors, file_warnings = verify_artifacts(record, args.repo_root)
        integrity_errors = input_errors + file_errors + verify_source(record, args.repo_root) + verify_revision_context(record)
        if integrity_errors:
            print(f"FAIL {record_path}: input/output integrity")
            for error in integrity_errors:
                print(f"  - {error}")
            failed = True
        else:
            print(f"PASS {record_path}: schema and local input/output integrity")
        for warning in input_warnings + file_warnings:
            print(f"WARN {record_path}: {warning}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
