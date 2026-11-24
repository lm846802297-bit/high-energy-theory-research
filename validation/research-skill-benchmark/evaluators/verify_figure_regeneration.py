#!/usr/bin/env python3
"""Verify pinned T05 plotting inputs, semantic golden agreement, and submitted outputs.

Only the trusted, hash-pinned plotting script is executed. Model-generated code
is never executed. Historical SVG references are compared semantically because
their XML numeric formatting differs from the current pinned generator; plotted
path data must remain exactly identical. When a submitted-output directory is
provided, both submitted SVGs must be byte-identical to the trusted generator's
fresh outputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

COORDINATE_ATTRIBUTES = {"x", "y", "x1", "y1", "x2", "y2", "cx", "cy"}
COORDINATE_TOLERANCE_PX = 0.01
NUMBER_PATTERN = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_identity(path: Path, expected_sha1: str, expected_size: int) -> dict[str, Any]:
    data = path.read_bytes()
    actual_sha1 = git_blob_sha1(data)
    if len(data) != expected_size:
        raise ValueError(f"Size mismatch for {path}: {len(data)} != {expected_size}")
    if actual_sha1 != expected_sha1:
        raise ValueError(f"Git blob SHA-1 mismatch for {path}")
    return {"path": str(path), "size_bytes": len(data), "git_blob_sha1": actual_sha1, "sha256": sha256(data)}


def _entry(manifest: dict[str, Any], evaluator_id: str) -> dict[str, Any]:
    for item in manifest.get("deterministic_evaluators", []):
        if item.get("id") == evaluator_id:
            return item
    raise ValueError(f"Evaluator ID not found in registry: {evaluator_id}")


def _canonical_text(value: str | None) -> str:
    text = (value or "").strip()
    # The archived ratio SVG used a semicolon where the pinned generator uses
    # a comma between the same two metadata clauses. No physics label changes.
    text = re.sub(
        r"(m_V\s*=\s*10\s*GeV)[,;]\s*(v\s*=\s*776\s*km/s)",
        r"\1; \2",
        text,
    )
    return text


def _compare_transform(reference: str, actual: str, state: dict[str, Any], location: str) -> None:
    ref_numbers = NUMBER_PATTERN.findall(reference)
    actual_numbers = NUMBER_PATTERN.findall(actual)
    ref_skeleton = NUMBER_PATTERN.sub("#", reference)
    actual_skeleton = NUMBER_PATTERN.sub("#", actual)
    if ref_skeleton != actual_skeleton or len(ref_numbers) != len(actual_numbers):
        raise ValueError(f"SVG transform mismatch at {location}: {reference!r} != {actual!r}")
    for ref_number, actual_number in zip(ref_numbers, actual_numbers, strict=True):
        delta = abs(float(ref_number) - float(actual_number))
        state["max_coordinate_delta_px"] = max(state["max_coordinate_delta_px"], delta)
        if delta > COORDINATE_TOLERANCE_PX:
            raise ValueError(f"SVG transform numeric mismatch at {location}: delta={delta:.8g}")


def _compare_svg_nodes(reference: ET.Element, actual: ET.Element, state: dict[str, Any], location: str = "/svg") -> None:
    if reference.tag != actual.tag:
        raise ValueError(f"SVG element mismatch at {location}: {reference.tag!r} != {actual.tag!r}")
    if set(reference.attrib) != set(actual.attrib):
        raise ValueError(f"SVG attribute-set mismatch at {location}")

    for name, ref_value in reference.attrib.items():
        actual_value = actual.attrib[name]
        if name in COORDINATE_ATTRIBUTES:
            try:
                delta = abs(float(ref_value) - float(actual_value))
            except ValueError as exc:
                raise ValueError(f"Non-numeric SVG coordinate at {location}/@{name}") from exc
            state["max_coordinate_delta_px"] = max(state["max_coordinate_delta_px"], delta)
            if delta > COORDINATE_TOLERANCE_PX:
                raise ValueError(
                    f"SVG coordinate mismatch at {location}/@{name}: "
                    f"reference={ref_value}, generated={actual_value}, delta={delta:.8g}px"
                )
        elif name == "d":
            state["path_count"] += 1
            if ref_value != actual_value:
                state["path_data_exact"] = False
                raise ValueError(f"SVG plotted path data differ at {location}/@d")
        elif name == "transform":
            _compare_transform(ref_value, actual_value, state, f"{location}/@transform")
        elif ref_value != actual_value:
            raise ValueError(
                f"SVG attribute mismatch at {location}/@{name}: {ref_value!r} != {actual_value!r}"
            )

    reference_text = _canonical_text(reference.text)
    actual_text = _canonical_text(actual.text)
    if reference_text or actual_text:
        state["text_count"] += 1
        if reference_text != actual_text:
            raise ValueError(
                f"SVG text mismatch at {location}: "
                f"{reference_text!r} != {actual_text!r}"
            )

    ref_children = list(reference)
    actual_children = list(actual)
    if len(ref_children) != len(actual_children):
        raise ValueError(f"SVG child-count mismatch at {location}: {len(ref_children)} != {len(actual_children)}")
    state["element_count"] += 1
    for index, (ref_child, actual_child) in enumerate(zip(ref_children, actual_children, strict=True)):
        _compare_svg_nodes(ref_child, actual_child, state, f"{location}/{ref_child.tag}[{index}]")


def compare_svg_semantics(reference_bytes: bytes, actual_bytes: bytes) -> dict[str, Any]:
    """Compare SVG structure, exact plotted path data, labels, and coordinates."""
    try:
        reference = ET.fromstring(reference_bytes)
        actual = ET.fromstring(actual_bytes)
    except ET.ParseError as exc:
        raise ValueError(f"Invalid SVG XML: {exc}") from exc
    state: dict[str, Any] = {
        "path_count": 0,
        "path_data_exact": True,
        "text_count": 0,
        "element_count": 0,
        "max_coordinate_delta_px": 0.0,
    }
    _compare_svg_nodes(reference, actual, state)
    state["semantic_match"] = True
    state["coordinate_tolerance_px"] = COORDINATE_TOLERANCE_PX
    state["byte_identity_match"] = reference_bytes == actual_bytes
    return state


def verify_figure_regeneration(
    manifest_path: Path,
    model_input_root: Path,
    golden_root: Path,
    timeout_seconds: int = 60,
    generated_output_root: Path | None = None,
    submitted_output_root: Path | None = None,
) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    evaluator = _entry(manifest, "E-T05B-DATA-TO-FIGURE")
    repository = evaluator["repository"]
    repository_dir = repository.split("/", 1)[1]
    generator_record = evaluator["generator"]
    generator_path = model_input_root / repository_dir / generator_record["path"]
    generator_identity = verify_identity(generator_path, generator_record["git_blob_sha1"], generator_record["size_bytes"])

    input_paths: list[Path] = []
    input_identities: list[dict[str, Any]] = []
    for record in evaluator["model_visible_inputs"]:
        path = model_input_root / repository_dir / record["path"]
        input_paths.append(path)
        input_identities.append(verify_identity(path, record["git_blob_sha1"], record["size_bytes"]))

    golden_paths: list[Path] = []
    golden_identities: list[dict[str, Any]] = []
    for record in evaluator["evaluator_only_reference_outputs"]:
        path = golden_root / repository_dir / record["path"]
        golden_paths.append(path)
        golden_identities.append(verify_identity(path, record["git_blob_sha1"], record["size_bytes"]))

    with tempfile.TemporaryDirectory(prefix="t05-figure-eval-") as temp:
        work = Path(temp)
        script_copy = work / "plot_user_dsigma_curve.py"
        script_copy.write_bytes(generator_path.read_bytes())
        results_dir = work / "results"
        results_dir.mkdir()
        csv_copy = results_dir / "fixed_speed_xe131_dsigma_450kev.csv"
        minima_copy = results_dir / "local_minima_refinement_1keV.csv"
        shutil.copyfile(input_paths[0], csv_copy)
        shutil.copyfile(input_paths[1], minima_copy)
        output_dir = results_dir / "plots"
        command = [
            sys.executable, str(script_copy),
            "--csv", str(csv_copy),
            "--minima", str(minima_copy),
            "--out-dir", str(output_dir),
        ]
        env = os.environ.copy()
        env.update({"PYTHONIOENCODING": "utf-8", "HOME": str(work), "USERPROFILE": str(work)})
        completed = subprocess.run(
            command, cwd=work, env=env, capture_output=True, text=True,
            timeout=timeout_seconds, check=False,
        )
        if completed.returncode != 0:
            raise ValueError(f"Pinned plotting script failed ({completed.returncode}): {completed.stderr[-2000:]}")

        names = [
            "fixed_speed_xe131_dsigma_450kev.svg",
            "xe131_gcn_jj55_response_ratio_450kev.svg",
        ]
        generated_outputs: list[dict[str, Any]] = []
        semantic_checks: list[dict[str, Any]] = []
        submitted_checks: list[dict[str, Any]] = []
        if generated_output_root is not None:
            generated_output_root.mkdir(parents=True, exist_ok=True)
        for name, golden in zip(names, golden_paths, strict=True):
            generated = output_dir / name
            data = generated.read_bytes()
            expected = golden.read_bytes()
            try:
                semantic = compare_svg_semantics(expected, data)
            except ValueError as exc:
                semantic = {
                    "semantic_match": False,
                    "byte_identity_match": expected == data,
                    "path_data_exact": False,
                    "error": str(exc),
                    "coordinate_tolerance_px": COORDINATE_TOLERANCE_PX,
                }
            if generated_output_root is not None:
                (generated_output_root / name).write_bytes(data)
            generated_outputs.append({
                "path": name,
                "size_bytes": len(data),
                "git_blob_sha1": git_blob_sha1(data),
                "sha256": sha256(data),
            })
            semantic_checks.append({"path": name, **semantic})

            if submitted_output_root is not None:
                submitted = submitted_output_root / name
                if not submitted.is_file():
                    submitted_checks.append({"path": name, "status": "FAIL", "error": "submitted SVG is missing"})
                else:
                    submitted_bytes = submitted.read_bytes()
                    submitted_checks.append({
                        "path": name,
                        "status": "PASS" if submitted_bytes == data else "FAIL",
                        "size_bytes": len(submitted_bytes),
                        "sha256": sha256(submitted_bytes),
                        "matches_trusted_generator": submitted_bytes == data,
                    })

        semantic_pass = all(item["semantic_match"] for item in semantic_checks)
        submission_evaluated = submitted_output_root is not None
        submission_pass = submission_evaluated and all(item["status"] == "PASS" for item in submitted_checks)
        overall_pass = semantic_pass and (submission_pass if submission_evaluated else True)
        return {
            "status": "PASS" if overall_pass else "FAIL",
            "evaluation_mode": "submission" if submission_evaluated else "trusted_baseline_only",
            "semantic_golden_match": semantic_pass,
            "byte_identity_with_historical_golden": all(item["byte_identity_match"] for item in semantic_checks),
            "historical_serialization_differences": [
                item["path"] for item in semantic_checks if not item["byte_identity_match"]
            ],
            "semantic_checks": semantic_checks,
            "submission_evaluated": submission_evaluated,
            "submission_pass": submission_pass if submission_evaluated else None,
            "submitted_outputs": submitted_checks,
            "evaluator_id": evaluator["id"],
            "generator": generator_identity,
            "inputs": input_identities,
            "golden_outputs": golden_identities,
            "generated_outputs": generated_outputs,
            "command": command,
            "exit_status": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "trusted_pinned_source_executed": True,
            "model_generated_code_executed": False,
            "visual_inspection_required": True,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--model-input-root", type=Path, required=True)
    parser.add_argument("--golden-root", type=Path, required=True)
    parser.add_argument("--generated-output-root", type=Path)
    parser.add_argument("--submitted-output-root", type=Path)
    parser.add_argument("--baseline-only", action="store_true", help="validate the pinned generator against the historical semantic reference without model outputs")
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args()
    if args.baseline_only == (args.submitted_output_root is not None):
        parser.error("choose exactly one of --baseline-only or --submitted-output-root")
    try:
        result = verify_figure_regeneration(
            args.manifest, args.model_input_root, args.golden_root,
            args.timeout_seconds, args.generated_output_root, args.submitted_output_root,
        )
    except (OSError, ValueError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0 if result.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
