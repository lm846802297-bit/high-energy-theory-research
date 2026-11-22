#!/usr/bin/env python3
"""Verify T06 reproducibility-package hashes and independently recompute result.

The evaluator does not execute model-generated source code. It verifies the
source/input/output identities, validates the run manifest, and independently
recomputes the weighted mean from the pinned CSV bytes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

EXPECTED_CSV = b"x,weight\n0,1\n1,2\n2,1\n"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def weighted_mean_from_csv(data: bytes) -> float:
    import io
    text = data.decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(text, newline="")))
    if not rows or set(rows[0]) != {"x", "weight"}:
        raise ValueError("CSV must contain exactly x,weight columns and at least one row")
    numerator = 0.0
    denominator = 0.0
    for row in rows:
        x = float(row["x"])
        weight = float(row["weight"])
        numerator += x * weight
        denominator += weight
    if denominator == 0:
        raise ValueError("Sum of weights must be nonzero")
    return numerator / denominator


def verify(source_path: Path, input_path: Path, output_path: Path, manifest_path: Path, tolerance: float = 1e-12) -> dict[str, Any]:
    source = source_path.read_bytes()
    input_bytes = input_path.read_bytes()
    output_bytes = output_path.read_bytes()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if input_bytes != EXPECTED_CSV:
        raise ValueError("Input CSV bytes differ from the exact T06 fixture, including final newline")
    output = json.loads(output_bytes.decode("utf-8"))
    expected = weighted_mean_from_csv(input_bytes)
    reported = output.get("weighted_mean")
    if isinstance(reported, bool) or not isinstance(reported, (int, float)):
        raise ValueError("Output JSON must contain numeric weighted_mean")
    if not math.isclose(float(reported), expected, rel_tol=0.0, abs_tol=tolerance):
        raise ValueError(f"Reported weighted mean {reported} differs from independent result {expected}")
    expected_hashes = {
        "source_sha256": sha256(source),
        "input_sha256": sha256(input_bytes),
        "output_sha256": sha256(output_bytes),
    }
    for key, value in expected_hashes.items():
        if manifest.get(key) != value:
            raise ValueError(f"Manifest {key} mismatch")
    if manifest.get("command") is None or "python" not in str(manifest["command"]).lower():
        raise ValueError("Manifest must record the Python command used")
    environment = manifest.get("environment")
    if not isinstance(environment, dict) or not environment.get("python_version") or not environment.get("os") or not environment.get("architecture"):
        raise ValueError("Manifest must record Python version, OS, and architecture")
    return {
        "status": "PASS",
        "weighted_mean_reported": float(reported),
        "weighted_mean_independent": expected,
        "absolute_difference": abs(float(reported) - expected),
        "tolerance": tolerance,
        "hashes": expected_hashes,
        "manifest_sha256_outer_record_only": sha256(manifest_path.read_bytes()),
        "source_executed_by_evaluator": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    args = parser.parse_args()
    try:
        result = verify(args.source, args.input, args.output, args.manifest, args.tolerance)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
