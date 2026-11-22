#!/usr/bin/env python3
"""Verify the pinned T05 CSV-to-SVG generator against sealed golden outputs.

Only the trusted, hash-pinned plotting script is executed. Model-generated code
is never executed. Inputs and golden outputs are checked by Git blob SHA-1 and
byte size before use; generated outputs are compared byte-for-byte.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


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


def verify_figure_regeneration(manifest_path: Path, model_input_root: Path, golden_root: Path, timeout_seconds: int = 60) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    evaluator = _entry(manifest, "E-T05B-DATA-TO-FIGURE")
    repository = evaluator["repository"]
    repository_dir = repository.split("/", 1)[1]
    generator_record = evaluator["generator"]
    generator_path = model_input_root / repository_dir / generator_record["path"]
    generator_identity = verify_identity(generator_path, generator_record["git_blob_sha1"], generator_record["size_bytes"])

    input_records = evaluator["model_visible_inputs"]
    input_paths: list[Path] = []
    input_identities: list[dict[str, Any]] = []
    for record in input_records:
        path = model_input_root / repository_dir / record["path"]
        input_paths.append(path)
        input_identities.append(verify_identity(path, record["git_blob_sha1"], record["size_bytes"]))

    golden_records = evaluator["evaluator_only_reference_outputs"]
    golden_paths: list[Path] = []
    golden_identities: list[dict[str, Any]] = []
    for record in golden_records:
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
            sys.executable,
            str(script_copy),
            "--csv", str(csv_copy),
            "--minima", str(minima_copy),
            "--out-dir", str(output_dir),
        ]
        env = {"PATH": os.environ.get("PATH", ""), "PYTHONIOENCODING": "utf-8", "HOME": str(work)}
        completed = subprocess.run(command, cwd=work, env=env, capture_output=True, text=True, timeout=timeout_seconds, check=False)
        if completed.returncode != 0:
            raise ValueError(f"Pinned plotting script failed ({completed.returncode}): {completed.stderr[-2000:]}")
        generated_paths = [
            output_dir / "fixed_speed_xe131_dsigma_450kev.svg",
            output_dir / "xe131_gcn_jj55_response_ratio_450kev.svg",
        ]
        generated_identities = []
        for generated, golden in zip(generated_paths, golden_paths, strict=True):
            data = generated.read_bytes()
            expected = golden.read_bytes()
            if data != expected:
                raise ValueError(f"Generated SVG differs byte-for-byte from golden reference: {generated.name}")
            generated_identities.append({
                "path": generated.name,
                "size_bytes": len(data),
                "git_blob_sha1": git_blob_sha1(data),
                "sha256": sha256(data),
                "matches_golden": True,
            })
        return {
            "status": "PASS",
            "evaluator_id": evaluator["id"],
            "generator": generator_identity,
            "inputs": input_identities,
            "golden_outputs": golden_identities,
            "generated_outputs": generated_identities,
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
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args()
    try:
        result = verify_figure_regeneration(args.manifest, args.model_input_root, args.golden_root, args.timeout_seconds)
    except (OSError, ValueError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
