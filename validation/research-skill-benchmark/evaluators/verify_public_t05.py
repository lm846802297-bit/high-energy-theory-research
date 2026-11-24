#!/usr/bin/env python3
"""Verify public-source T05 PDF audits and Native AFH Xe-131 figure reproduction."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def t05_task(task_manifest: dict[str, Any]) -> dict[str, Any]:
    for task in task_manifest.get("tasks", []):
        if task.get("id") == "T05":
            return task
    raise ValueError("T05 is absent from the task manifest")


def t05_evaluator(evaluator_manifest: dict[str, Any], evaluator_id: str) -> dict[str, Any]:
    for item in evaluator_manifest.get("deterministic_evaluators", []):
        if item.get("id") == evaluator_id:
            return item
    raise ValueError(f"Evaluator {evaluator_id} is absent from the evaluator manifest")


def verify_inputs(task: dict[str, Any], input_root: Path) -> list[dict[str, Any]]:
    identities: list[dict[str, Any]] = []
    for record in task.get("input_sources", []):
        path = input_root / record["staged_path"]
        data = path.read_bytes()
        actual_sha1 = git_blob_sha1(data)
        actual_sha256 = sha256_bytes(data)
        if len(data) != record["size_bytes"]:
            raise ValueError(
                f"size mismatch for {record['staged_path']}: "
                f"{len(data)} != {record['size_bytes']}"
            )
        if actual_sha1 != record["git_blob_sha1"]:
            raise ValueError(f"Git blob SHA-1 mismatch for {record['staged_path']}")
        if actual_sha256 != record["sha256"]:
            raise ValueError(f"SHA-256 mismatch for {record['staged_path']}")
        identities.append({
            "repository": record["repository"],
            "commit": record["commit"],
            "path": record["path"],
            "staged_path": record["staged_path"],
            "role": record["role"],
            "size_bytes": len(data),
            "git_blob_sha1": actual_sha1,
            "sha256": actual_sha256,
        })
    if not identities:
        raise ValueError("T05 has no model-visible source inputs")
    return identities


def audit_pdfs(
    task: dict[str, Any],
    evaluator_manifest: dict[str, Any],
    input_root: Path,
    pdf_audit_script: Path,
) -> dict[str, Any]:
    evaluator = t05_evaluator(evaluator_manifest, "E-T05A-PDF-TEXT-SCREEN")
    records = [x for x in task["input_sources"] if x["role"] == "pdf_audit_input"]
    if len(records) != 2:
        raise ValueError(f"expected two paired PDF figure panels, found {len(records)}")
    results: list[dict[str, Any]] = []
    for record in records:
        pdf_path = input_root / record["staged_path"]
        completed = subprocess.run(
            [sys.executable, str(pdf_audit_script), str(pdf_path), "--min-pt", "5.0", "--json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
            check=False,
        )
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"PDF text auditor returned invalid JSON for {record['path']}: "
                f"{completed.stderr[-1000:]}"
            ) from exc
        if completed.returncode not in (0, 1) or not payload.get("auditable"):
            raise ValueError(
                f"PDF text audit was not auditable for {record['path']}: "
                f"{completed.stderr[-1000:]}"
            )
        results.append({
            "path": record["path"],
            "sha256": record["sha256"],
            "screening_status": "BELOW_5_PT_TEXT_FOUND" if payload["below_minimum_count"] else "NO_BELOW_5_PT_TEXT_FOUND",
            "minimum_required_pt": payload["minimum_required_pt"],
            "minimum_found_pt": payload["minimum_found_pt"],
            "text_run_count": payload["text_run_count"],
            "below_minimum_count": payload["below_minimum_count"],
            "spacing_issue_count": payload["spacing_issue_count"],
            "warnings": payload["warnings"],
        })
    return {
        "status": "PASS_AUDIT_COMPLETED",
        "evaluator_id": evaluator["id"],
        "pdf_count": len(results),
        "pdf_results": results,
        "interpretation": (
            "The 5 pt threshold is a screening value only. It is not a journal "
            "requirement and does not replace visual inspection at intended size."
        ),
    }


def reproduce_figures(
    task: dict[str, Any],
    evaluator_manifest: dict[str, Any],
    input_root: Path,
    submitted_output_root: Path,
) -> dict[str, Any]:
    evaluator = t05_evaluator(evaluator_manifest, "E-T05B-AFH-RESPONSE-REPRO")
    generator_record = next(
        x for x in task["input_sources"] if x["role"] == "figure_generator"
    )
    csv_record = next(
        x for x in task["input_sources"] if x["role"] == "figure_input_data"
    )
    generator_path = input_root / generator_record["staged_path"]
    csv_path = input_root / csv_record["staged_path"]
    expected_names = evaluator["expected_outputs"]
    with tempfile.TemporaryDirectory(prefix="public-t05-afh-") as temporary:
        output_dir = Path(temporary) / "trusted-output"
        command = [
            sys.executable,
            str(generator_path),
            "--csv",
            str(csv_path),
            "--out-dir",
            str(output_dir),
        ]
        completed = subprocess.run(
            command,
            cwd=input_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
            check=False,
        )
        if completed.returncode != 0:
            raise ValueError(
                f"trusted AFH figure generator failed: {completed.stderr[-2000:]}"
            )
        try:
            generator_report = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise ValueError("trusted AFH generator did not emit valid JSON") from exc
        if generator_report.get("status") != "PASS":
            raise ValueError("trusted AFH generator did not report PASS")
        generated_records: list[dict[str, Any]] = []
        submitted_records: list[dict[str, Any]] = []
        for name in expected_names:
            generated_path = output_dir / name
            submitted_path = submitted_output_root / name
            if not generated_path.is_file():
                raise ValueError(f"trusted generator did not create {name}")
            generated = generated_path.read_bytes()
            if not submitted_path.is_file():
                raise ValueError(f"model-submitted SVG is missing: {name}")
            submitted = submitted_path.read_bytes()
            match = submitted == generated
            generated_records.append({
                "path": name,
                "size_bytes": len(generated),
                "sha256": sha256_bytes(generated),
            })
            submitted_records.append({
                "path": name,
                "size_bytes": len(submitted),
                "sha256": sha256_bytes(submitted),
                "status": "PASS" if match else "FAIL",
                "matches_trusted_generator": match,
            })
            if not match:
                raise ValueError(f"submitted SVG differs from fresh trusted output: {name}")
        return {
            "status": "PASS",
            "evaluator_id": evaluator["id"],
            "evaluation_mode": "submission",
            "submission_evaluated": True,
            "submission_pass": True,
            "generator_command": command,
            "generator_report": generator_report,
            "generated_outputs": generated_records,
            "submitted_outputs": submitted_records,
            "stdout_sha256": sha256_bytes(completed.stdout.encode("utf-8")),
            "stderr_sha256": sha256_bytes(completed.stderr.encode("utf-8")),
        }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--part", choices=("pdf", "figures"), required=True)
    parser.add_argument("--task-manifest", type=Path, required=True)
    parser.add_argument("--evaluator-manifest", type=Path, required=True)
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--pdf-audit-script", type=Path)
    parser.add_argument("--submitted-output-root", type=Path)
    parser.add_argument("--output", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        task = t05_task(load_json(args.task_manifest))
        evaluator_manifest = load_json(args.evaluator_manifest)
        identities = verify_inputs(task, args.input_root)
        if args.part == "pdf":
            if args.pdf_audit_script is None:
                raise ValueError("--pdf-audit-script is required for --part pdf")
            result = audit_pdfs(task, evaluator_manifest, args.input_root, args.pdf_audit_script)
        else:
            if args.submitted_output_root is None:
                raise ValueError("--submitted-output-root is required for --part figures")
            result = reproduce_figures(
                task, evaluator_manifest, args.input_root, args.submitted_output_root
            )
        result["input_identities"] = identities
        result["input_count"] = len(identities)
        encoded = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(encoded, encoding="utf-8")
        print(encoded, end="")
        return 0
    except (OSError, KeyError, StopIteration, ValueError, json.JSONDecodeError) as exc:
        print(f"public T05 verification failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
