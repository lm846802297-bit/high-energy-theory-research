#!/usr/bin/env python3
"""Deterministic evaluator for Particle Physics Research Skill Benchmark v1.0.

This program validates run records, verifies pinned source bytes, checks paired
A/B controls, recomputes rubric scores, and creates a blinded-comparison report.
It never executes model-provided code and never modifies input artifacts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_SCHEMA = ROOT / "protocol" / "run-record.schema.json"
DEFAULT_REPORT_SCHEMA = ROOT / "protocol" / "comparison-report.schema.json"
DEFAULT_RUBRIC = ROOT / "protocol" / "scoring-rubric.yaml"
DEFAULT_TASK_MANIFEST = ROOT / "tasks" / "development" / "manifest.json"
DEFAULT_EVALUATOR_MANIFEST = ROOT / "evaluators" / "manifest.json"
DEFAULT_ENVIRONMENT_LOCK = ROOT / "protocol" / "environment-lock.json"
DEFAULT_ANALYSIS_PLAN = ROOT / "protocol" / "experimental-design.md"
DIMENSIONS = (
    "scientific_correctness",
    "independent_validation",
    "reproducibility",
    "evidence_quality",
    "efficiency",
)
GATES = (
    "critical_physics_error",
    "fabricated_evidence",
    "destructive_change",
    "false_pass",
    "convention_or_unit_failure",
)


class EvaluationError(Exception):
    """Raised for invalid benchmark evidence or protocol violations."""


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvaluationError(f"Cannot read JSON {path}: {exc}") from exc


def read_rubric(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise EvaluationError(f"Cannot read scoring rubric {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise EvaluationError("Scoring rubric must be a YAML mapping")
    entries = data.get("weighted_dimensions")
    if not isinstance(entries, list) or not entries:
        raise EvaluationError("Rubric weighted_dimensions must be a non-empty list")
    weights: dict[str, float] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            raise EvaluationError("Invalid weighted dimension entry")
        key = entry["id"]
        value = entry.get("weight_percent")
        if key in weights or not isinstance(value, (int, float)) or value <= 0:
            raise EvaluationError(f"Invalid or duplicate rubric weight for {key}")
        weights[key] = float(value) / 100.0
    if set(weights) != set(DIMENSIONS):
        raise EvaluationError(f"Rubric dimensions must be exactly {list(DIMENSIONS)}")
    if not math.isclose(sum(weights.values()), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise EvaluationError("Rubric weights must sum to 100 percent")
    return {"raw": data, "weights": weights}


def validate_schema(instance: Any, schema_path: Path) -> None:
    schema = read_json(schema_path)
    try:
        Draft202012Validator.check_schema(schema)
        errors = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance),
            key=lambda e: list(map(str, e.path)),
        )
    except Exception as exc:
        raise EvaluationError(f"Schema validation setup failed for {schema_path}: {exc}") from exc
    if errors:
        details = [f"/{'/'.join(map(str, err.path))}: {err.message}" for err in errors]
        raise EvaluationError("Schema validation failed: " + "; ".join(details))


def score_dimensions(scores: dict[str, Any], weights: dict[str, float]) -> float:
    if not isinstance(scores, dict):
        raise EvaluationError("dimension_scores must be an object")
    missing = [name for name in DIMENSIONS if name not in scores]
    if missing:
        raise EvaluationError(f"Missing dimension scores: {missing}")
    values: dict[str, float] = {}
    for name in DIMENSIONS:
        value = scores[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise EvaluationError(f"Score {name} must be a number from 0 to 4")
        if not 0 <= float(value) <= 4:
            raise EvaluationError(f"Score {name} outside 0..4")
        values[name] = float(value)
    return 25.0 * sum(weights[name] * values[name] for name in DIMENSIONS)


def validate_run(
    record: dict[str, Any],
    schema_path: Path = DEFAULT_RUN_SCHEMA,
    rubric_path: Path = DEFAULT_RUBRIC,
    require_scored: bool = True,
    artifact_root: Path | None = None,
) -> float | None:
    validate_schema(record, schema_path)
    rubric = read_rubric(rubric_path)
    evaluation = record["evaluation"]
    if not require_scored:
        return None
    for name in DIMENSIONS:
        if evaluation["dimension_scores"].get(name) is None:
            raise EvaluationError(f"Run {record['run_id']} has no final score for {name}")
    if evaluation.get("autonomy_score") is None:
        raise EvaluationError(f"Run {record['run_id']} has no autonomy score")
    computed = score_dimensions(evaluation["dimension_scores"], rubric["weights"])
    stored = evaluation.get("weighted_score")
    if stored is None or not math.isclose(float(stored), computed, rel_tol=0.0, abs_tol=1e-8):
        raise EvaluationError(
            f"Run {record['run_id']} weighted_score mismatch: stored={stored}, recomputed={computed:.12g}"
        )
    adjudication = evaluation.get("adjudication")
    if adjudication is not None:
        if adjudication.get("final_dimension_scores") != evaluation["dimension_scores"]:
            raise EvaluationError(f"Run {record['run_id']} final scores disagree with adjudication")
        if adjudication.get("final_autonomy_score") != evaluation["autonomy_score"]:
            raise EvaluationError(f"Run {record['run_id']} autonomy score disagrees with adjudication")
    reviewers = evaluation.get("reviewer_assessments", [])
    if len(reviewers) != 2:
        raise EvaluationError(f"Run {record['run_id']} must contain exactly two blinded reviewer assessments")
    for reviewer in reviewers:
        if reviewer.get("arm_label_hidden") is not True:
            raise EvaluationError(f"Run {record['run_id']} reviewer was not blinded to arm")
    disagreements = []
    for name in DIMENSIONS:
        left = reviewers[0]["dimension_scores"].get(name)
        right = reviewers[1]["dimension_scores"].get(name)
        if left != right:
            disagreements.append((name, left, right))
    autonomy_left = reviewers[0].get("autonomy_score")
    autonomy_right = reviewers[1].get("autonomy_score")
    autonomy_disagreement = autonomy_left != autonomy_right
    hard_disagreement = reviewers[0].get("hard_gates") != reviewers[1].get("hard_gates")
    if adjudication is not None:
        if adjudication.get("final_hard_gates") != evaluation["hard_gates"]:
            raise EvaluationError(f"Run {record['run_id']} final hard gates disagree with adjudication")
    elif not hard_disagreement and evaluation["hard_gates"] != reviewers[0]["hard_gates"]:
        raise EvaluationError(f"Run {record['run_id']} final hard gates differ from unanimous reviewer gates")
    needs_adjudication = hard_disagreement or any(abs(float(a) - float(b)) >= 2 for _, a, b in disagreements)
    if autonomy_disagreement and autonomy_left is not None and autonomy_right is not None:
        needs_adjudication = needs_adjudication or abs(float(autonomy_left) - float(autonomy_right)) >= 2
    if needs_adjudication and adjudication is None:
        raise EvaluationError(f"Run {record['run_id']} requires third-party adjudication")
    any_reviewer_disagreement = bool(disagreements) or autonomy_disagreement
    if any_reviewer_disagreement and adjudication is None and not evaluation.get("reviewer_consensus_note"):
        raise EvaluationError(f"Run {record['run_id']} requires a documented reviewer consensus note")
    if adjudication is None:
        for name, left, right in disagreements:
            if evaluation["dimension_scores"][name] not in (left, right):
                raise EvaluationError(f"Run {record['run_id']} consensus score for {name} is not one of the reviewers' scores")
        if autonomy_disagreement and evaluation["autonomy_score"] not in (autonomy_left, autonomy_right):
            raise EvaluationError(f"Run {record['run_id']} consensus autonomy score is not one of the reviewers' scores")
        if not any_reviewer_disagreement:
            if evaluation["dimension_scores"] != reviewers[0]["dimension_scores"] or evaluation["autonomy_score"] != reviewers[0]["autonomy_score"]:
                raise EvaluationError(f"Run {record['run_id']} final scores differ from unanimous reviewer scores")
    artifact_paths = {item["path"] for item in record["artifacts"]}
    required_artifacts = {
        record["execution"]["tool_log_artifact"],
        record["execution"]["transcript_artifact"],
        record["skill"]["availability_evidence_artifact"],
    }
    missing_artifacts = sorted(required_artifacts - artifact_paths)
    if missing_artifacts:
        raise EvaluationError(f"Run {record['run_id']} is missing required artifact records: {missing_artifacts}")
    if artifact_root is not None:
        verify_run_artifacts(record, artifact_root)
    skill = record["skill"]
    expected_skill_commit = record["protocol"].get("skill_source_commit")
    if record["arm"] == "with-skill" and skill.get("source_commit") != expected_skill_commit:
        raise EvaluationError(f"Run {record['run_id']} Skill commit differs from the protocol lock")
    if record["arm"] == "no-skill" and expected_skill_commit is None:
        raise EvaluationError("Protocol must pin the Skill source commit even for the no-skill comparison arm")
    budget = record["budget"]
    execution = record["execution"]
    if execution["actual_wall_time_seconds"] > budget["wall_time_seconds"]:
        raise EvaluationError(f"Run {record['run_id']} exceeded its wall-time budget")
    if execution["actual_tool_calls"] > budget["tool_call_limit"]:
        raise EvaluationError(f"Run {record['run_id']} exceeded its tool-call budget")
    if budget.get("token_limit") is not None and execution.get("token_count") is not None:
        if execution["token_count"] > budget["token_limit"]:
            raise EvaluationError(f"Run {record['run_id']} exceeded its token budget")
    return computed


def _control_projection(record: dict[str, Any]) -> dict[str, Any]:
    execution = record["execution"]
    return {
        "protocol": record["protocol"],
        "model": record["model"],
        "runtime": record["runtime"],
        "project_context": record["project_context"],
        "task_input": record["task_input"],
        "tools": record["tools"],
        "budget": record["budget"],
        "randomization_seed": execution["randomization_seed"],
        "pair_order": execution["pair_order"],
    }


def validate_pair(
    first: dict[str, Any],
    second: dict[str, Any],
    schema_path: Path = DEFAULT_RUN_SCHEMA,
    rubric_path: Path = DEFAULT_RUBRIC,
    artifact_root: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_run(first, schema_path, rubric_path, artifact_root=artifact_root)
    validate_run(second, schema_path, rubric_path, artifact_root=artifact_root)
    if {first["arm"], second["arm"]} != {"no-skill", "with-skill"}:
        raise EvaluationError("A valid pair must contain exactly one no-skill and one with-skill record")
    a = first if first["arm"] == "no-skill" else second
    b = first if first["arm"] == "with-skill" else second
    for field in ("pair_id", "task_id", "repeat"):
        if a[field] != b[field]:
            raise EvaluationError(f"Paired runs disagree on {field}: {a[field]} != {b[field]}")
    if a["run_id"] == b["run_id"]:
        raise EvaluationError("A/B runs must have distinct run_id values")
    if a["execution"]["transcript_artifact"] == b["execution"]["transcript_artifact"]:
        raise EvaluationError("A/B runs must have separate transcript artifacts")
    shared_artifacts = {item["path"] for item in a["artifacts"]} & {item["path"] for item in b["artifacts"]}
    if shared_artifacts:
        raise EvaluationError(f"A/B runs must have separate artifact paths: {sorted(shared_artifacts)}")
    control_a = _control_projection(a)
    control_b = _control_projection(b)
    if control_a != control_b:
        differing = [key for key in control_a if control_a[key] != control_b[key]]
        raise EvaluationError(f"A/B controls differ outside the Skill treatment: {differing}")
    if a["project_context"]["shared_skill_routing_removed"] is not True:
        raise EvaluationError("Common project snapshot must remove shared-Skill routing before both arms")
    if a["skill"]["available"] is not False or a["skill"]["references_loaded"]:
        raise EvaluationError("No-Skill arm has evidence of Skill availability or loaded references")
    if b["skill"]["available"] is not True or not b["skill"]["references_loaded"]:
        raise EvaluationError("With-Skill arm lacks evidence of Skill availability/reference loading")
    return a, b


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_source_record(record: dict[str, Any], local_path: Path) -> dict[str, Any]:
    try:
        data = local_path.read_bytes()
    except OSError as exc:
        raise EvaluationError(f"Cannot read staged source {local_path}: {exc}") from exc
    actual = {
        "path": str(local_path),
        "size_bytes": len(data),
        "git_blob_sha1": git_blob_sha1(data),
        "sha256": sha256(data),
    }
    if actual["size_bytes"] != record["size_bytes"]:
        raise EvaluationError(f"Source size mismatch for {record['path']}: {actual['size_bytes']} != {record['size_bytes']}")
    if actual["git_blob_sha1"] != record["git_blob_sha1"]:
        raise EvaluationError(f"Git blob SHA-1 mismatch for {record['path']}")
    expected_sha = record.get("sha256")
    if expected_sha and actual["sha256"] != expected_sha:
        raise EvaluationError(f"SHA-256 mismatch for {record['path']}")
    return actual


def verify_run_artifacts(record: dict[str, Any], artifact_root: Path) -> list[dict[str, Any]]:
    root = artifact_root.resolve()
    verified: list[dict[str, Any]] = []
    for artifact in record["artifacts"]:
        relative = Path(artifact["path"])
        if relative.is_absolute():
            raise EvaluationError(f"Artifact path must be relative: {artifact['path']}")
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            raise EvaluationError(f"Artifact path escapes artifact root: {artifact['path']}")
        if not path.is_file():
            raise EvaluationError(f"Missing run artifact: {artifact['path']}")
        actual_sha = sha256(path.read_bytes())
        if actual_sha != artifact["sha256"]:
            raise EvaluationError(f"Artifact SHA-256 mismatch: {artifact['path']}")
        verified.append({"path": artifact["path"], "sha256": actual_sha, "status": "PASS"})
    return verified


def validate_task_source_bundle(
    record: dict[str, Any],
    task: dict[str, Any],
    input_root: Path | None = None,
) -> list[dict[str, Any]]:
    expected_sources = task.get("input_sources", [])
    actual_sources = record["task_input"]["source_files"]

    def identity(item: dict[str, Any]) -> tuple[str, str, str, str, int]:
        return (
            item["repository"],
            item["commit"],
            item["path"],
            item["git_blob_sha1"],
            item["size_bytes"],
        )

    expected = sorted(expected_sources, key=lambda item: (item["repository"], item["path"]))
    actual = sorted(actual_sources, key=lambda item: (item["repository"], item["path"]))
    if len(expected) != len(actual):
        raise EvaluationError(
            f"Run {record['run_id']} source-file count does not match task manifest: "
            f"{len(actual)} != {len(expected)}"
        )
    for exp, got in zip(expected, actual, strict=True):
        if identity(exp) != identity(got):
            raise EvaluationError(
                f"Run {record['run_id']} source identity differs from task manifest for {exp['path']}"
            )
        if exp.get("sha256") and exp["sha256"] != got["sha256"]:
            raise EvaluationError(f"Run {record['run_id']} SHA-256 differs from task manifest for {exp['path']}")

    expected_commits = {item["commit"] for item in expected}
    if len(expected_commits) == 1 and record["task_input"].get("source_commit") not in expected_commits:
        raise EvaluationError(f"Run {record['run_id']} source_commit differs from task manifest")

    verified = []
    if input_root is not None:
        root = input_root.resolve()
        for exp, got in zip(expected, actual, strict=True):
            repository_slug = exp["repository"].split("/", 1)[1]
            staged_path = exp.get("staged_path", f"{repository_slug}/{exp['path']}")
            path = (root / staged_path).resolve()
            if not path.is_relative_to(root):
                raise EvaluationError(f"Staged source path escapes input root: {staged_path}")
            verified.append(verify_source_record(got, path))
    return verified



def _index_evaluator_registry(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = manifest.get("deterministic_evaluators")
    if not isinstance(entries, list):
        raise EvaluationError("Evaluator registry must contain a deterministic_evaluators list")
    indexed: dict[str, dict[str, Any]] = {}
    allowed_types = {"deterministic", "manual", "internal"}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str) or not entry["id"]:
            raise EvaluationError("Evaluator registry contains an invalid evaluator entry")
        evaluator_id = entry["id"]
        if evaluator_id in indexed:
            raise EvaluationError(f"Evaluator registry contains duplicate ID {evaluator_id}")
        evaluator_type = entry.get("evaluator_type")
        if evaluator_type not in allowed_types:
            raise EvaluationError(f"Evaluator {evaluator_id} has an invalid evaluator_type")
        task_ids = entry.get("task_ids")
        if not isinstance(task_ids, list) or not task_ids or len(task_ids) != len(set(task_ids)):
            raise EvaluationError(f"Evaluator {evaluator_id} must declare unique task_ids")
        if evaluator_type == "deterministic":
            payload_schema = entry.get("result_payload_schema")
            if not isinstance(payload_schema, dict):
                raise EvaluationError(f"Deterministic evaluator {evaluator_id} lacks result_payload_schema")
            try:
                Draft202012Validator.check_schema(payload_schema)
            except Exception as exc:
                raise EvaluationError(f"Evaluator {evaluator_id} has an invalid result_payload_schema: {exc}") from exc
        indexed[evaluator_id] = entry
    return indexed


def _validate_evaluator_payload(
    evaluator_spec: dict[str, Any],
    payload: dict[str, Any],
    run_id: str,
) -> None:
    if not isinstance(payload, dict):
        raise EvaluationError(f"Evaluator result for {evaluator_spec['id']} in run {run_id} is not a JSON object")
    payload_schema = evaluator_spec["result_payload_schema"]
    errors = sorted(
        Draft202012Validator(payload_schema, format_checker=FormatChecker()).iter_errors(payload),
        key=lambda error: list(map(str, error.path)),
    )
    if errors:
        details = [f"/{'/'.join(map(str, error.path))}: {error.message}" for error in errors]
        raise EvaluationError(
            f"Evaluator payload for {evaluator_spec['id']} in run {run_id} failed its registry contract: "
            + "; ".join(details)
        )


def validate_required_evaluators(
    record: dict[str, Any],
    task: dict[str, Any],
    artifact_root: Path | None = None,
    evaluator_manifest: dict[str, Any] | None = None,
) -> list[str]:
    if record.get("task_id") != task.get("id"):
        raise EvaluationError(f"Run {record['run_id']} task_id does not match the task manifest entry")
    if "required_evaluators" not in task or not isinstance(task["required_evaluators"], list):
        raise EvaluationError(f"Task {task.get('id', '<unknown>')} must declare required_evaluators")
    required = task["required_evaluators"]
    if any(not isinstance(item, str) or not item for item in required):
        raise EvaluationError(f"Task {task['id']} contains an invalid required_evaluators entry")
    if len(required) != len(set(required)):
        raise EvaluationError(f"Task {task['id']} contains duplicate required_evaluators")

    if evaluator_manifest is None:
        evaluator_manifest = read_json(DEFAULT_EVALUATOR_MANIFEST)
    evaluator_specs = _index_evaluator_registry(evaluator_manifest)
    for evaluator_id in required:
        spec = evaluator_specs.get(evaluator_id)
        if spec is None:
            raise EvaluationError(f"Task {task['id']} requires unregistered evaluator {evaluator_id}")
        if spec["evaluator_type"] != "deterministic":
            raise EvaluationError(f"Task {task['id']} requires non-deterministic evaluator {evaluator_id}")
        if task["id"] not in spec["task_ids"]:
            raise EvaluationError(f"Evaluator {evaluator_id} is not registered for task {task['id']}")

    checks = record["evaluation"].get("deterministic_checks", [])
    by_id: dict[str, dict[str, Any]] = {}
    for check in checks:
        evaluator_id = check["id"]
        if evaluator_id in by_id:
            raise EvaluationError(f"Run {record['run_id']} contains duplicate evaluator result {evaluator_id}")
        by_id[evaluator_id] = check

    missing = sorted(set(required) - set(by_id))
    if missing:
        raise EvaluationError(f"Run {record['run_id']} is missing required evaluator results: {missing}")

    artifact_by_path = {item["path"]: item for item in record["artifacts"]}
    validated: list[str] = []
    for evaluator_id in required:
        spec = evaluator_specs[evaluator_id]
        check = by_id[evaluator_id]
        if check["status"] != "pass":
            raise EvaluationError(
                f"Run {record['run_id']} required evaluator {evaluator_id} has status {check['status']!r}, not 'pass'"
            )
        if check["input_sha256"] != record["task_input"]["input_manifest_sha256"]:
            raise EvaluationError(
                f"Run {record['run_id']} evaluator {evaluator_id} input hash is not bound to the task input manifest"
            )
        result_path = check["result_artifact"]
        artifact = artifact_by_path.get(result_path)
        if artifact is None:
            raise EvaluationError(
                f"Run {record['run_id']} evaluator {evaluator_id} result is not registered as a run artifact"
            )
        if check["output_sha256"] != artifact["sha256"]:
            raise EvaluationError(
                f"Run {record['run_id']} evaluator {evaluator_id} output hash differs from its artifact record"
            )
        if artifact_root is not None:
            root = artifact_root.resolve()
            relative = Path(result_path)
            if relative.is_absolute():
                raise EvaluationError(f"Evaluator result path must be relative: {result_path}")
            path = (root / relative).resolve()
            if not path.is_relative_to(root):
                raise EvaluationError(f"Evaluator result path escapes artifact root: {result_path}")
            if not path.is_file():
                raise EvaluationError(f"Missing evaluator result artifact: {result_path}")
            _validate_evaluator_payload(spec, read_json(path), record["run_id"])
        validated.append(evaluator_id)
    return validated


def _quantile(sorted_values: list[float], probability: float):
    if not sorted_values:
        raise EvaluationError("Cannot calculate quantile of empty values")
    position = (len(sorted_values) - 1) * probability
    low = int(math.floor(position))
    high = int(math.ceil(position))
    if low == high:
        return sorted_values[low]
    fraction = position - low
    return sorted_values[low] * (1.0 - fraction) + sorted_values[high] * fraction


def reviewer_agreement(records: list[dict[str, Any]]) -> dict[str, Any]:
    left_scores: list[int] = []
    right_scores: list[int] = []
    for record in records:
        reviewers = record["evaluation"]["reviewer_assessments"]
        for name in DIMENSIONS:
            left_scores.append(int(reviewers[0]["dimension_scores"][name]))
            right_scores.append(int(reviewers[1]["dimension_scores"][name]))
        if reviewers[0].get("autonomy_score") is not None and reviewers[1].get("autonomy_score") is not None:
            left_scores.append(int(reviewers[0]["autonomy_score"]))
            right_scores.append(int(reviewers[1]["autonomy_score"]))
    if not left_scores:
        return {"ratings_compared": 0, "exact_agreement_rate": None, "quadratic_weighted_cohen_kappa": None}
    exact = sum(a == b for a, b in zip(left_scores, right_scores)) / len(left_scores)
    categories = range(5)
    observed = [[0 for _ in categories] for _ in categories]
    left_hist = [0 for _ in categories]
    right_hist = [0 for _ in categories]
    for a, b in zip(left_scores, right_scores):
        observed[a][b] += 1
        left_hist[a] += 1
        right_hist[b] += 1
    n = len(left_scores)
    observed_disagreement = 0.0
    expected_disagreement = 0.0
    for i in categories:
        for j in categories:
            weight = ((i - j) / 4.0) ** 2
            observed_disagreement += weight * observed[i][j] / n
            expected_disagreement += weight * (left_hist[i] / n) * (right_hist[j] / n)
    kappa = None if expected_disagreement == 0 else 1.0 - observed_disagreement / expected_disagreement
    if expected_disagreement == 0 and observed_disagreement == 0:
        kappa = 1.0
    return {
        "ratings_compared": n,
        "exact_agreement_rate": exact,
        "quadratic_weighted_cohen_kappa": kappa,
    }


def cluster_bootstrap_interval(
    family_means: dict[str, float], seed: int, resamples: int = 10000
) -> dict[str, Any]:
    if len(family_means) < 2:
        raise EvaluationError("Cluster bootstrap requires at least two independent task families")
    names = sorted(family_means)
    rng = random.Random(seed)
    draws: list[float] = []
    for _ in range(resamples):
        sample = [family_means[rng.choice(names)] for _ in names]
        draws.append(statistics.fmean(sample))
    draws.sort()
    return {
        "lower": _quantile(draws, 0.025),
        "upper": _quantile(draws, 0.975),
        "method": "cluster_bootstrap_by_task_family",
        "resamples": resamples,
        "seed": seed,
    }


def _load_run_files(records_dir: Path) -> list[dict[str, Any]]:
    paths = sorted(records_dir.rglob("*.json"))
    if not paths:
        raise EvaluationError(f"No JSON run records found under {records_dir}")
    records = []
    for path in paths:
        record = read_json(path)
        if not isinstance(record, dict) or "run_id" not in record:
            raise EvaluationError(f"Not a run record: {path}")
        records.append(record)
    return records


def compare_records(
    records: list[dict[str, Any]],
    task_manifest: dict[str, Any],
    round_name: str,
    seed: int,
    schema_path: Path = DEFAULT_RUN_SCHEMA,
    rubric_path: Path = DEFAULT_RUBRIC,
    artifact_root: Path | None = None,
    input_root: Path | None = None,
    evaluator_manifest: dict[str, Any] | None = None,
    protocol_bindings: dict[str, str] | None = None,
) -> dict[str, Any]:
    if evaluator_manifest is None:
        evaluator_manifest = read_json(DEFAULT_EVALUATOR_MANIFEST)
    _index_evaluator_registry(evaluator_manifest)
    if protocol_bindings is not None:
        for record in records:
            for field, expected_hash in protocol_bindings.items():
                if record["protocol"].get(field) != expected_hash:
                    raise EvaluationError(
                        f"Run {record['run_id']} protocol binding mismatch for {field}: "
                        f"recorded={record['protocol'].get(field)}, expected={expected_hash}"
                    )
    task_info = {item["id"]: item for item in task_manifest.get("tasks", [])}
    if not task_info:
        raise EvaluationError("Task manifest contains no tasks")
    by_pair: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_runs: set[str] = set()
    for record in records:
        if record["run_id"] in seen_runs:
            raise EvaluationError(f"Duplicate run_id {record['run_id']}")
        seen_runs.add(record["run_id"])
        if record["task_id"] not in task_info:
            raise EvaluationError(f"Run references unknown task_id {record['task_id']}")
        by_pair[record["pair_id"]].append(record)
    pair_rows: list[dict[str, Any]] = []
    task_pairs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    gate_counts = {"no-skill": 0, "with-skill": 0}
    b_only_gate_failures = 0
    b_only_failure_pair_ids: set[str] = set()
    b_failure_pair_ids: set[str] = set()
    unresolved_deviation_pair_ids: set[str] = set()
    dimension_deltas: dict[str, list[float]] = {name: [] for name in DIMENSIONS}
    wall_times = {"no-skill": [], "with-skill": []}
    tool_calls = {"no-skill": [], "with-skill": []}
    for pair_id, members in sorted(by_pair.items()):
        if len(members) != 2:
            raise EvaluationError(f"Pair {pair_id} has {len(members)} records; expected exactly 2")
        a, b = validate_pair(members[0], members[1], schema_path, rubric_path, artifact_root)
        task = task_info[a["task_id"]]
        validate_task_source_bundle(a, task, input_root)
        validate_task_source_bundle(b, task, input_root)
        validate_required_evaluators(a, task, artifact_root, evaluator_manifest)
        validate_required_evaluators(b, task, artifact_root, evaluator_manifest)
        family = task.get("task_family", a["task_id"])
        qa = float(a["evaluation"]["weighted_score"])
        qb = float(b["evaluation"]["weighted_score"])
        delta = qb - qa
        autonomy_a = float(a["evaluation"]["autonomy_score"])
        autonomy_b = float(b["evaluation"]["autonomy_score"])
        gates_a = [name for name in GATES if a["evaluation"]["hard_gates"].get(name) == "fail"]
        gates_b = [name for name in GATES if b["evaluation"]["hard_gates"].get(name) == "fail"]
        gate_counts["no-skill"] += len(gates_a)
        gate_counts["with-skill"] += len(gates_b)
        b_only = sorted(set(gates_b) - set(gates_a))
        b_only_gate_failures += len(b_only)
        if b_only:
            b_only_failure_pair_ids.add(pair_id)
        if gates_b:
            b_failure_pair_ids.add(pair_id)
        expected_reference = task.get("skill_reference")
        if expected_reference and expected_reference not in b["skill"]["references_loaded"]:
            raise EvaluationError(f"B run {b['run_id']} did not load the task-specific Skill reference {expected_reference}")
        for name in DIMENSIONS:
            dimension_deltas[name].append(
                float(b["evaluation"]["dimension_scores"][name]) - float(a["evaluation"]["dimension_scores"][name])
            )
        for arm, record in (("no-skill", a), ("with-skill", b)):
            wall_times[arm].append(float(record["execution"]["actual_wall_time_seconds"]))
            tool_calls[arm].append(int(record["execution"]["actual_tool_calls"]))
        pair_deviations = list(a["deviations"]) + list(b["deviations"])
        unresolved = [item for item in pair_deviations if not str(item).lower().startswith(("resolved:", "none"))]
        if unresolved:
            unresolved_deviation_pair_ids.add(pair_id)
        row = {
            "pair_id": pair_id,
            "task_id": a["task_id"],
            "task_family": family,
            "repeat": a["repeat"],
            "no_skill_run_id": a["run_id"],
            "with_skill_run_id": b["run_id"],
            "scores": {
                "q_no_skill": qa,
                "q_with_skill": qb,
                "delta_q": delta,
                "autonomy_no_skill": autonomy_a,
                "autonomy_with_skill": autonomy_b,
                "delta_autonomy": autonomy_b - autonomy_a,
            },
            "hard_gate_failures": [f"A:{name}" for name in gates_a] + [f"B:{name}" for name in gates_b],
            "b_only_hard_gate_failures": b_only,
            "deviations": pair_deviations,
        }
        pair_rows.append(row)
        task_pairs[a["task_id"]].append(row)

    task_means = {
        task_id: statistics.fmean(row["scores"]["delta_q"] for row in rows)
        for task_id, rows in task_pairs.items()
    }
    task_autonomy_means = {
        task_id: statistics.fmean(row["scores"]["delta_autonomy"] for row in rows)
        for task_id, rows in task_pairs.items()
    }
    family_to_tasks: dict[str, list[str]] = defaultdict(list)
    for task_id in task_means:
        family = task_info[task_id].get("task_family", task_id)
        family_to_tasks[family].append(task_id)
    family_means = {
        family: statistics.fmean(task_means[task_id] for task_id in task_ids)
        for family, task_ids in family_to_tasks.items()
    }
    family_autonomy_means = {
        family: statistics.fmean(task_autonomy_means[task_id] for task_id in task_ids)
        for family, task_ids in family_to_tasks.items()
    }
    macro_family = statistics.fmean(family_means.values()) if family_means else None
    mean_autonomy = statistics.fmean(row["scores"]["delta_autonomy"] for row in pair_rows) if pair_rows else None
    task_macro = statistics.fmean(task_means.values()) if task_means else None
    interval = None
    reasons: list[str] = []
    decision = "inconclusive"
    if round_name == "round_1_pilot":
        reasons.append("Round 1 is exploratory only and cannot establish a confirmatory decision.")
    elif round_name == "round_2_full":
        dimensions = {item.get("dimension") for item in task_info.values()}
        families_by_dimension: dict[str, set[str]] = defaultdict(set)
        for task_id, item in task_info.items():
            families_by_dimension[item.get("dimension", "unknown")].add(item.get("task_family", task_id))
        design_ok = len(dimensions) >= 6 and all(len(families_by_dimension[d]) >= 2 for d in dimensions)
        design_ok = design_ok and all(len(task_pairs.get(task_id, [])) >= 3 for task_id in task_info)
        design_ok = design_ok and len(family_means) >= 12 and len(pair_rows) >= 36
        if not design_ok:
            reasons.append("Holdout design is below the preregistered minimum: two independent task families per dimension, three paired repetitions per task, at least 12 families and 36 pairs.")
        else:
            interval = cluster_bootstrap_interval(family_means, seed=seed, resamples=10000)
            if interval["upper"] < 0:
                decision = "negative"
                reasons.append("The 95% task-family cluster-bootstrap interval is entirely below zero.")
            elif len(b_failure_pair_ids) >= 2:
                decision = "negative"
                reasons.append("B-arm hard-gate failures occurred in at least two distinct paired runs, establishing a repeated material regression.")
            elif b_failure_pair_ids:
                decision = "mixed"
                reasons.append("At least one B-arm hard-gate failure prevents a Positive decision.")
            elif unresolved_deviation_pair_ids:
                decision = "inconclusive"
                reasons.append("Unresolved run deviations remain in one or more pairs.")
            elif macro_family is not None and mean_autonomy is not None and macro_family >= 5 and interval["lower"] > 0 and mean_autonomy >= -0.5:
                dimension_regression = any(statistics.fmean(values) <= -0.5 for values in dimension_deltas.values() if values)
                family_regression = any(value <= -5 for value in family_means.values())
                if dimension_regression or family_regression:
                    decision = "mixed"
                    reasons.append("Overall improvement coexists with a material dimension or task-family regression.")
                else:
                    decision = "positive"
                    reasons.append("Practical-effect, uncertainty, autonomy, hard-gate, and pair-integrity criteria are all satisfied.")
            elif interval["upper"] < 0:
                decision = "negative"
                reasons.append("The estimated effect is negative with the 95% interval below zero.")
            else:
                decision = "inconclusive"
                reasons.append("The practical-effect, confidence-interval, or autonomy threshold was not met.")
    else:
        reasons.append("Round 3 project-level results require a separate project-stratified analysis plan.")

    all_deltas = [row["scores"]["delta_q"] for row in pair_rows]
    report = {
        "protocol_version": "1.0",
        "protocol_commit": None,
        "analysis_plan_sha256": None,
        "environment_lock_sha256": None,
        "round": round_name,
        "task_pairs": pair_rows,
        "summary": {
            "paired_run_count": len(pair_rows),
            "independent_task_count": len(task_means),
            "independent_task_family_count": len(family_means),
            "mean_paired_delta_q": statistics.fmean(all_deltas) if all_deltas else None,
            "task_macro_mean_delta_q": task_macro,
            "macro_mean_delta_q": macro_family,
            "median_paired_delta_q": statistics.median(all_deltas) if all_deltas else None,
            "minimum_paired_delta_q": min(all_deltas) if all_deltas else None,
            "maximum_paired_delta_q": max(all_deltas) if all_deltas else None,
            "task_family_mean_delta_q": family_means,
            "confidence_interval_95": interval,
            "mean_autonomy_delta": mean_autonomy,
            "task_family_mean_autonomy_delta": family_autonomy_means,
            "dimension_deltas": {name: statistics.fmean(values) if values else None for name, values in dimension_deltas.items()},
            "hard_gate_summary": {"failures_by_arm": gate_counts, "b_only_failure_count": b_only_gate_failures, "b_only_failure_pair_count": len(b_only_failure_pair_ids), "b_failure_pair_count": len(b_failure_pair_ids)},
            "reviewer_agreement": reviewer_agreement(records),
            "unresolved_deviation_pair_count": len(unresolved_deviation_pair_ids),
            "resource_summary": {
                "mean_wall_time_seconds": {arm: statistics.fmean(values) if values else None for arm, values in wall_times.items()},
                "mean_tool_calls": {arm: statistics.fmean(values) if values else None for arm, values in tool_calls.items()},
            },
        },
        "decision": decision,
        "decision_reasons": reasons,
    }
    return report


def command_validate_run(args: argparse.Namespace) -> dict[str, Any]:
    record = read_json(args.run_record)
    score = validate_run(record, args.schema, args.rubric, require_scored=not args.allow_unscored, artifact_root=args.artifact_root)
    return {"status": "PASS", "run_id": record["run_id"], "arm": record["arm"], "recomputed_weighted_score": score}


def command_validate_pair(args: argparse.Namespace) -> dict[str, Any]:
    first, second = read_json(args.first), read_json(args.second)
    a, b = validate_pair(first, second, args.schema, args.rubric, args.artifact_root)
    return {"status": "PASS", "pair_id": a["pair_id"], "task_id": a["task_id"], "no_skill_run_id": a["run_id"], "with_skill_run_id": b["run_id"]}


def command_verify_sources(args: argparse.Namespace) -> dict[str, Any]:
    manifest = read_json(args.manifest)
    results = []
    for task in manifest.get("tasks", []):
        for source in task.get("input_sources", []):
            staged_path = source.get("staged_path", source["path"])
            local_path = (args.input_root / staged_path).resolve()
            root_path = args.input_root.resolve()
            if not local_path.is_relative_to(root_path):
                raise EvaluationError(f"Staged source path escapes input root: {staged_path}")
            result = verify_source_record(source, local_path)
            result.update({"task_id": task["id"], "repository": source["repository"]})
            results.append(result)
    if not results:
        raise EvaluationError("No source inputs were found in the task manifest")
    return {"status": "PASS", "verified_source_count": len(results), "sources": results}


def command_compare(args: argparse.Namespace) -> dict[str, Any]:
    records = _load_run_files(args.records_dir)
    manifest = read_json(args.task_manifest)
    evaluator_manifest = read_json(args.evaluator_manifest)
    analysis_plan_sha256 = sha256(args.analysis_plan.read_bytes())
    environment_lock_sha256 = sha256(args.environment_lock.read_bytes())
    if args.analysis_plan_sha256 is not None and args.analysis_plan_sha256 != analysis_plan_sha256:
        raise EvaluationError("Provided analysis_plan_sha256 does not match the exact analysis-plan file bytes")
    if args.environment_lock_sha256 is not None and args.environment_lock_sha256 != environment_lock_sha256:
        raise EvaluationError("Provided environment_lock_sha256 does not match the exact environment-lock file bytes")
    protocol_bindings = {
        "commit": args.protocol_commit,
        "task_manifest_sha256": sha256(args.task_manifest.read_bytes()),
        "scoring_rubric_sha256": sha256(args.rubric.read_bytes()),
        "environment_lock_sha256": environment_lock_sha256,
        "evaluator_manifest_sha256": sha256(args.evaluator_manifest.read_bytes()),
        "analysis_plan_sha256": analysis_plan_sha256,
    }
    report = compare_records(
        records,
        manifest,
        args.round,
        args.seed,
        args.schema,
        args.rubric,
        args.artifact_root,
        args.input_root,
        evaluator_manifest,
        protocol_bindings,
    )
    report["protocol_commit"] = args.protocol_commit
    report["analysis_plan_sha256"] = analysis_plan_sha256
    report["environment_lock_sha256"] = environment_lock_sha256
    validate_schema(report, args.report_schema)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("validate-run", help="validate one run record and recompute its score")
    run.add_argument("run_record", type=Path)
    run.add_argument("--schema", type=Path, default=DEFAULT_RUN_SCHEMA)
    run.add_argument("--rubric", type=Path, default=DEFAULT_RUBRIC)
    run.add_argument("--artifact-root", type=Path, required=True)
    run.add_argument("--allow-unscored", action="store_true")
    run.set_defaults(func=command_validate_run)

    pair = sub.add_parser("validate-pair", help="validate A/B treatment and common controls")
    pair.add_argument("first", type=Path)
    pair.add_argument("second", type=Path)
    pair.add_argument("--schema", type=Path, default=DEFAULT_RUN_SCHEMA)
    pair.add_argument("--rubric", type=Path, default=DEFAULT_RUBRIC)
    pair.add_argument("--artifact-root", type=Path, required=True)
    pair.set_defaults(func=command_validate_pair)

    source = sub.add_parser("verify-sources", help="verify staged task inputs against Git identities")
    source.add_argument("--manifest", type=Path, default=DEFAULT_TASK_MANIFEST)
    source.add_argument("--input-root", type=Path, required=True)
    source.set_defaults(func=command_verify_sources)

    compare = sub.add_parser("compare", help="build a paired A/B comparison report")
    compare.add_argument("--records-dir", type=Path, required=True)
    compare.add_argument("--task-manifest", type=Path, default=DEFAULT_TASK_MANIFEST)
    compare.add_argument("--evaluator-manifest", type=Path, default=DEFAULT_EVALUATOR_MANIFEST)
    compare.add_argument("--analysis-plan", type=Path, default=DEFAULT_ANALYSIS_PLAN)
    compare.add_argument("--environment-lock", type=Path, default=DEFAULT_ENVIRONMENT_LOCK)
    compare.add_argument("--round", choices=["round_1_pilot", "round_2_full", "round_3_real_projects"], required=True)
    compare.add_argument("--seed", type=int, required=True)
    compare.add_argument("--protocol-commit", required=True)
    compare.add_argument("--analysis-plan-sha256")
    compare.add_argument("--environment-lock-sha256")
    compare.add_argument("--schema", type=Path, default=DEFAULT_RUN_SCHEMA)
    compare.add_argument("--rubric", type=Path, default=DEFAULT_RUBRIC)
    compare.add_argument("--artifact-root", type=Path, required=True)
    compare.add_argument("--input-root", type=Path, required=True)
    compare.add_argument("--report-schema", type=Path, default=DEFAULT_REPORT_SCHEMA)
    compare.add_argument("--output", type=Path)
    compare.set_defaults(func=command_compare)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = args.func(args)
    except EvaluationError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
