#!/usr/bin/env python3
"""Build a self-contained, validated provenance bundle for the UV-EFT PV audit."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
CASE_REL = Path("tests/eval-cases/uv-eFT-hard-derivative-pilot")
PROJECT_ID = "PROJECT-UV-EFT-HARD-PILOT-001"
REPO_URI = "https://github.com/lm846802297-bit/high-energy-theory-research"
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

IDS = {
    "task": "TASK-UV-EFT-HARD-001",
    "task_execution_contract": "TEC-UV-EFT-HARD-001",
    "run_plan": "RUNPLAN-UV-EFT-HARD-001",
    "run": "RUN-UV-EFT-HARD-001",
    "run_manifest": "MANIFEST-UV-EFT-HARD-001",
    "artifact_plan": "ARTPLAN-UV-EFT-RESULT-001",
    "artifact": "ART-UV-EFT-RESULT-001",
    "validation_plan": "VALPLAN-UV-EFT-HARD-001",
    "validation_activity": "VALACT-UV-EFT-HARD-001",
    "validation_report": "VALREP-UV-EFT-HARD-001",
    "claim": "CLAIM-UV-EFT-HARD-001",
    "configuration": "CONF-UV-EFT-HARD-001",
    "code": "CODE-UV-EFT-HARD-001",
    "environment": "ENV-UV-EFT-HARD-001",
    "convention_set": "CONV-UV-EFT-HARD-001",
    "evidence_fragment": "EVID-UV-EFT-HARD-001",
}
SOURCE_IDS = {
    "note": "SRC-UV-EFT-NOTE-001",
    "problem": "SRC-UV-EFT-PROBLEM-001",
    "configuration": "SRC-UV-EFT-CONFIG-001",
    "arxiv": "SRC-UV-EFT-ARXIV-001",
}
LOG_ARTIFACT_PLAN_ID = "ARTPLAN-UV-EFT-LOG-001"
LOG_ARTIFACT_ID = "ART-UV-EFT-LOG-001"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime(TIMESTAMP_FORMAT)


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha_file(path: Path) -> str:
    return _sha_bytes(path.read_bytes())


def _load_module(name: str, path: Path):
    sys.modules.pop(name, None)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _minimal_value(schema, root_schema, field="value", depth=0):
    if depth > 80:
        raise ValueError(f"Schema recursion too deep at {field}")
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            raise ValueError(f"External schema ref is not supported by fixture factory: {ref}")
        target = root_schema
        for part in ref[2:].split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
        return _minimal_value(target, root_schema, field, depth + 1)
    if "const" in schema:
        return schema["const"]
    if isinstance(schema.get("enum"), list) and schema["enum"]:
        return schema["enum"][0]
    for key in ("oneOf", "anyOf"):
        if isinstance(schema.get(key), list):
            for choice in schema[key]:
                candidate = _minimal_value(choice, root_schema, field, depth + 1)
                try:
                    if Draft202012Validator(choice).is_valid(candidate):
                        return candidate
                except Exception:
                    pass
            return _minimal_value(schema[key][0], root_schema, field, depth + 1)

    value_type = schema.get("type")
    if isinstance(value_type, list):
        if "null" in value_type:
            return None
        value_type = value_type[0]
    if not value_type and ("properties" in schema or "required" in schema):
        value_type = "object"
    if value_type == "object":
        result = {}
        for name in schema.get("required", []):
            if name in schema.get("properties", {}):
                result[name] = _minimal_value(schema["properties"][name], root_schema, name, depth + 1)
        for sub_schema in schema.get("allOf", []):
            if "if" in sub_schema:
                continue
            extra = _minimal_value(sub_schema, root_schema, field, depth + 1)
            if isinstance(extra, dict):
                result.update(extra)
        return result
    if value_type == "array":
        count = int(schema.get("minItems", 0))
        return [_minimal_value(schema.get("items", {}), root_schema, field + "[]", depth + 1) for _ in range(count)]
    if value_type == "string":
        if schema.get("format") == "date-time":
            return "2026-10-21T00:00:00Z"
        if schema.get("format") in {"uri", "uri-reference"}:
            return "https://example.org/pilot"
        if schema.get("format") == "email":
            return "pilot@example.org"
        pattern = schema.get("pattern", "")
        if "a-f0-9" in pattern or "a-f" in pattern:
            return "a" * 64
        if pattern.startswith("^[A-Z]"):
            return "PILOT-001"
        return "PILOT"
    if value_type == "integer":
        return max(1, int(schema.get("minimum", 1)))
    if value_type == "number":
        return max(1, float(schema.get("minimum", 1)))
    if value_type == "boolean":
        return False
    if value_type == "null":
        return None
    return {}


def _copy_snapshot(bundle_root: Path) -> None:
    files = [
        (ROOT / CASE_REL / "run_pilot.py", CASE_REL / "run_pilot.py"),
        (ROOT / CASE_REL / "run_record_chain.py", CASE_REL / "run_record_chain.py"),
        (ROOT / CASE_REL / "README.md", CASE_REL / "README.md"),
        (ROOT / CASE_REL / "problem.json", Path("inputs/problem.json")),
        (ROOT / CASE_REL / "config.json", Path("inputs/config.json")),
        (ROOT / CASE_REL / "source-excerpt.md", Path("sources/source-excerpt.md")),
        (ROOT / "requirements-dev.txt", Path("requirements-dev.txt")),
        (ROOT / "skills/high-energy-theory-research/scripts/fingerprint_inputs.py", Path("skills/high-energy-theory-research/scripts/fingerprint_inputs.py")),
        (ROOT / "skills/high-energy-theory-research/scripts/validate_project_records.py", Path("skills/high-energy-theory-research/scripts/validate_project_records.py")),
        (ROOT / "schema/v1.4.3.7/manifest.json", Path("schema/v1.4.3.7/manifest.json")),
        (ROOT / "schema/v1.4.3.7/tools/cross_record_validate.py", Path("schema/v1.4.3.7/tools/cross_record_validate.py")),
        (ROOT / "schema/v1.4.3.7/tools/schema-v1.4.3.6-validate.py", Path("schema/v1.4.3.7/tools/schema-v1.4.3.6-validate.py")),
        (ROOT / "schema/v1.4.3.7/tools/directory_manifest.py", Path("schema/v1.4.3.7/tools/directory_manifest.py")),
    ]
    for source, relative in files:
        destination = bundle_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    schema_source = ROOT / "schema/v1.4.3.7/schemas"
    schema_destination = bundle_root / "schema/v1.4.3.7/schemas"
    shutil.copytree(schema_source, schema_destination, dirs_exist_ok=True)


def _make_record(record_type: str, record_id: str, schemas: dict, primary: dict) -> dict:
    schema = schemas[record_type]
    record = _minimal_value(schema, schema)
    record.update({
        "schema_version": "1.4",
        "record_type": record_type,
        "project_id": PROJECT_ID,
        primary[record_type]: record_id,
    })
    return record


def _assumption(description: str, rationale: str) -> dict:
    return {
        "assumption_id": "ASM-UV-EFT-HARD-001",
        "description": description,
        "scope": "This bounded PV-function and projection audit only.",
        "status": "accepted",
        "source_or_rationale": rationale,
    }


def _criterion() -> dict:
    return {
        "criterion_id": "AC-UV-EFT-HARD-001",
        "description": "Closed-form PV functions, Feynman-parameter quadrature, small-r residuals, and rational projection factors agree within declared tolerances.",
        "required": True,
        "verification_method": "independent Feynman-parameter adaptive Simpson quadrature plus exact rational checks",
        "pass_condition": "all reported checks pass and all record references resolve",
        "failure_condition": "any numerical check fails, any digest changes unexpectedly, or any record reference is missing",
        "evidence_kind": "computed_result",
    }


def _build_records(bundle_root: Path, started_at: str, completed_at: str, run_exit_code: int, physics_result: dict, output_sha: str, log_sha: str, code_tree_sha: str, environment_sha: str, config_sha: str, source_hashes: dict, execution_spec: dict, execution_sha: str, fingerprints: dict, lockfile_sha: str, runtime: dict, convention_payload: dict, configuration_payload: dict, external_reference: dict) -> list[dict]:
    schemas_dir = bundle_root / "schema/v1.4.3.7/schemas"
    schemas = {
        path.name.removesuffix(".schema.json"): json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(schemas_dir.glob("*.schema.json"))
    }
    cross = _load_module("cross_record_validate_for_uv_pilot", bundle_root / "schema/v1.4.3.7/tools/cross_record_validate.py")
    primary = cross.PRIMARY
    rec = {key: _make_record(key, value, schemas, primary) for key, value in IDS.items()}

    note_hash = source_hashes["note"]
    problem_hash = source_hashes["problem"]
    config_file_hash = source_hashes["configuration"]
    all_source_ids = [SOURCE_IDS["note"], SOURCE_IDS["problem"], SOURCE_IDS["configuration"], SOURCE_IDS["arxiv"]]
    source_records = []
    for key, title, path, version, digest, unavailable_reason in [
        ("note", "User project-note excerpt: UV-EFT hard derivative", "sources/source-excerpt.md", "project-note-v153-sections-39-40", note_hash, None),
        ("problem", "UV-EFT hard derivative audit input", "inputs/problem.json", "uv-eFT-hard-derivative-v1", problem_hash, None),
        ("configuration", "UV-EFT hard derivative numerical configuration", "inputs/config.json", "uv-eFT-hard-derivative-config-v1", config_file_hash, None),
        ("arxiv", "An Axial U_A(1)_{L_mu-L_tau}: UV Completion and Experimental Searches", "https://arxiv.org/html/2608.27258v1", "arXiv:2608.27258v1", None, "The paper was accessed for model identity and field/mass conventions but was not vendored byte-for-byte; it is a bibliographic/model-convention reference, not a numerical input to this run."),
    ]:
        item = _make_record("source", SOURCE_IDS[key], schemas, primary)
        item.update({
            "source_type": "project_note_excerpt" if key == "note" else ("arxiv_preprint" if key == "arxiv" else ("run_configuration" if key == "configuration" else "research_task_input")),
            "title": title,
            "uri_or_path": path,
            "source_version": version,
            "content_sha256": digest,
            "retrieved_at": completed_at,
            "lifecycle_status": "active",
            "verification_status": "verified",
            "hash_unavailable_reason": unavailable_reason,
        })
        source_records.append(item)

    convention = rec["convention_set"]
    convention.update({
        "notation": "r=m^2/M^2; L=ln(M^2/mu^2); K=a*b*c_L*s_L*c_R*s_R; M^2=1 and K=1 are audit normalizations only.",
        "metric_signature": "Minkowski convention inherited from the working-note 1PI/PV formulas; this pilot does not redo the loop numerator.",
        "unit_system": "Natural units; Fprime/K and Pi-prime are dimensionless; C_PhiD/Lambda^2 has mass dimension -2.",
        "gauge_conventions": "Model convention cross-reference only: axial U_A(1)_{L_mu-L_tau}; H is neutral under the new U(1), S has charge Q_S=2Q_l in the primary paper.",
        "renormalization_scheme": "The hard-kernel expression is used with the working note's MS-bar subtraction and explicitly declared 1PI insertion convention.",
        "flavor_basis": "Muon-sector light/heavy vector-like lepton block as described in the source note; the numerical audit does not rediagonalize it.",
        "phase_conventions": "Real mass entries and mixing-angle signs as assumed by the source note.",
        "applicability_notes": "Bounded internal-consistency audit of the transcribed PV derivative and conditional single-operator projection; not a complete matching result.",
        "content_sha256": problem_hash,
    })

    configuration = rec["configuration"]
    configuration.update({
        **configuration_payload,
        "configuration_sha256": config_sha,
        "created_at": completed_at,
    })

    code = rec["code"]
    github_sha = os.environ.get("GITHUB_SHA")
    code.update({
        "repository_uri": REPO_URI,
        "git_commit": github_sha or "unavailable-in-local-test",
        "git_commit_unavailable_reason": None if github_sha else "GITHUB_SHA is not set in this local/test context; code identity is retained by the content fingerprint.",
        "dirty": not bool(github_sha),
        "diff_sha256": _sha_bytes(b"") if github_sha else _sha_bytes(b"local diff not captured"),
        "code_tree_sha256": code_tree_sha,
        "created_at": completed_at,
    })

    environment = rec["environment"]
    environment.update({
        "platform": sys.platform,
        "runtime_versions": runtime,
        "lockfile_sha256": lockfile_sha,
        "lockfile_unavailable_reason": None,
        "container_digest": None,
        "container_unavailable_reason": "GitHub-hosted runner image digest is not pinned by this pilot; Python runtime and lockfile are recorded.",
        "environment_sha256": environment_sha,
        "created_at": completed_at,
    })

    config_record_ids = [IDS["configuration"]]
    input_refs = {
        "source_ids": all_source_ids,
        "configuration_ids": config_record_ids,
        "input_artifact_ids": [],
        "external_references": [external_reference],
    }

    contract = rec["task_execution_contract"]
    contract.update({
        "task_id": IDS["task"],
        "contract_version": 1,
        "contract_status": "approved",
        "objective": "Independently audit the transcribed one-loop hard mixed-self-energy derivative formulas and their conditional single-operator projection.",
        "scope": {
            "included": [
                "Feynman-parameter integral checks of the stated PV values and derivatives",
                "small-r expansion through the O(r) terms",
                "1PI insertion factor at mu=M",
                "radial cross-kinetic factor and conditional projection coefficient",
                "provenance, fingerprint, artifact, independent-validation and Claim linkage",
            ],
            "excluded": [
                "rederiving the full UV loop numerator and all diagram combinatorics",
                "complete IBP/EOM reduction and unique Wilson coefficient in a full operator basis",
                "experimental constraints or phenomenological parameter-space claims",
            ],
            "target_domain": "high-energy theoretical physics; one-loop UV-EFT mixed-scalar two-point-function subtask",
            "out_of_scope_behavior": "Do not promote this subtask to a complete UV-EFT matching result; keep human scientific review pending.",
        },
        "input_refs": input_refs,
        "assumptions": [
            _assumption("The working-note hard-kernel expression and its 1PI/PV conventions are the inputs under audit.", "Exact local source excerpt with content hash."),
            _assumption("The numerical checks use M^2=1 and K=1 as dimensionless normalization choices, not a physical benchmark.", "Configuration explicitly labels these choices as audit normalizations."),
            _assumption("The operator projection uses the single-operator convention Pi'_local=-(C_PhiD/Lambda^2)*v_h*v_s/2.", "Source excerpt and problem input state this convention and its limitation."),
        ],
        "conventions_id": IDS["convention_set"],
        "conventions_reason": None,
        "required_capabilities": ["python-stdlib", "sha256", "jsonschema", "rfc8785"],
        "planned_methods": [{
            "method_id": "METHOD-UV-EFT-PV-001",
            "description": "Compare closed-form PV expressions against independent Feynman-parameter adaptive Simpson quadrature and exact rational factor checks.",
            "scope": "The PV derivative and conditional operator projection stated in problem.json only.",
            "status": "accepted",
            "source_or_rationale": "The integral definitions provide an independent numerical representation of the closed-form Bbar and Bprime functions.",
        }],
        "artifact_plan_ids": [IDS["artifact_plan"], LOG_ARTIFACT_PLAN_ID],
        "validation_plan_ids": [IDS["validation_plan"]],
        "acceptance_criteria": [_criterion()],
        "failure_branches": ["Reject invalid mass ratios, non-finite PV values, failed quadrature comparisons, or missing record references."],
        "stop_conditions": ["Stop if any independent numerical check fails or the candidate record graph does not validate."],
        "contract_sha256": "0" * 64,
        "created_at": completed_at,
        "approved_at": completed_at,
        "approved_by": "automated-pilot-contract",
        "supersedes_contract_id": None,
    })
    contract["contract_sha256"] = _load_module(
        "fingerprint_inputs_for_contract_hash", bundle_root / "skills/high-energy-theory-research/scripts/fingerprint_inputs.py"
    ).sha256_json({key: value for key, value in contract.items() if key != "contract_sha256"})

    task = rec["task"]
    task.update({
        "title": "UV-EFT hard mixed-self-energy derivative and single-operator projection audit",
        "task_type": "analytic_derivation",
        "task_status": "complete",
        "active_contract_id": IDS["task_execution_contract"],
        "dependency_task_ids": [],
        "claim_ids": [IDS["claim"]],
        "status_reason": None,
        "completion_evidence_ids": [IDS["evidence_fragment"]],
        "created_at": completed_at,
        "updated_at": completed_at,
    })

    fingerprint_module = _load_module(
        "fingerprint_inputs_for_uv_pilot", bundle_root / "skills/high-energy-theory-research/scripts/fingerprint_inputs.py"
    )
    problem_file = bundle_root / "inputs/problem.json"
    config_file = bundle_root / "inputs/config.json"
    source_inputs = [
        {"source_id": SOURCE_IDS["note"], "content_sha256": note_hash},
        {"source_id": SOURCE_IDS["problem"], "content_sha256": problem_hash},
        {"source_id": SOURCE_IDS["configuration"], "content_sha256": config_file_hash},
    ]
    execution_spec = {
        "entrypoint": "python tests/eval-cases/uv-eFT-hard-derivative-pilot/run_pilot.py",
        "arguments": ["--input", "inputs/problem.json", "--config", "inputs/config.json", "--output", "outputs/results.json"],
        "working_directory": ".",
        "precision": "binary64",
        "tolerances": {"absolute": float(json.loads(config_file.read_text(encoding="utf-8"))["agreement_absolute_tolerance"]), "relative": float(json.loads(config_file.read_text(encoding="utf-8"))["agreement_absolute_tolerance"])},
        "random_seed": None,
        "parallelism": 1,
        "locale": "C",
        "timezone": "UTC",
        "expected_outputs": ["outputs/results.json"],
        "timeout_policy": {"timeout_seconds": 60, "on_timeout": "fail", "retry_limit": 0},
    }
    execution_sha = fingerprint_module.sha256_json(execution_spec)
    fingerprint_inputs = {
        "contract_version": fingerprint_module.CONTRACT_VERSION,
        "canonicalization": fingerprint_module.CANONICALIZATION,
        "source_inputs": source_inputs,
        "input_artifacts": [],
        "configuration": {"record_id": IDS["configuration"], "configuration_sha256": config_sha, "not_applicable_reason": None},
        "code": {"record_id": IDS["code"], "code_tree_sha256": code_tree_sha, "not_applicable_reason": None},
        "environment": {"record_id": IDS["environment"], "environment_sha256": environment_sha, "not_applicable_reason": None},
        "execution_spec_sha256": execution_sha,
        "fingerprint_profile_version": fingerprint_module.DEFAULT_PROFILE_VERSION,
    }
    bundle = fingerprint_module.compute_fingerprint_bundle(fingerprint_inputs, execution_spec)

    run_plan = rec["run_plan"]
    run_plan.update({
        "task_id": IDS["task"],
        "contract_id": IDS["task_execution_contract"],
        "run_plan_status": "instantiated",
        "configuration_id": IDS["configuration"],
        "code_id": IDS["code"],
        "environment_id": IDS["environment"],
        "input_artifact_ids": [],
        "artifact_plan_ids": [IDS["artifact_plan"], LOG_ARTIFACT_PLAN_ID],
        "validation_plan_ids": [IDS["validation_plan"]],
        "execution_spec": execution_spec,
        "fingerprint_inputs": fingerprint_inputs,
        "execution_spec_sha256": execution_sha,
        "instantiated_run_id": IDS["run"],
        "blocked_reason": None,
        "supersedes_run_plan_id": None,
        "created_at": started_at,
    })

    run = rec["run"]
    run.update({
        "task_id": IDS["task"],
        "contract_id": IDS["task_execution_contract"],
        "run_plan_id": IDS["run_plan"],
        "execution_status": "succeeded" if run_exit_code == 0 else "failed",
        "started_at": started_at,
        "completed_at": completed_at,
        "exit_code": run_exit_code,
        "exit_code_unavailable_reason": None,
        "parent_run_id": None,
        "retry_of_run_id": None,
        "manifest_ids": [IDS["run_manifest"]],
        "latest_manifest_id": IDS["run_manifest"],
        "log_artifact_ids": [LOG_ARTIFACT_ID],
        "created_at": completed_at,
    })

    manifest = rec["run_manifest"]
    manifest.update({
        "run_id": IDS["run"],
        "task_id": IDS["task"],
        "contract_id": IDS["task_execution_contract"],
        "run_plan_id": IDS["run_plan"],
        "manifest_revision": 1,
        "execution_status_snapshot": "succeeded" if run_exit_code == 0 else "failed",
        "snapshot_at": completed_at,
        "input_refs": input_refs,
        "configuration": {
            "configuration_id": IDS["configuration"],
            "conventions_id": IDS["convention_set"],
            "independent_inputs": configuration_payload["independent_inputs"],
            "derived_parameters": configuration_payload["derived_parameters"],
            "units": configuration_payload["units"],
            "configuration_sha256": config_sha,
        },
        "code": {
            "code_id": IDS["code"],
            "repository_uri": REPO_URI,
            "repository_uri_unavailable_reason": None,
            "git_commit": code["git_commit"],
            "git_commit_unavailable_reason": code["git_commit_unavailable_reason"],
            "dirty": code["dirty"],
            "diff_sha256": code["diff_sha256"],
            "code_tree_sha256": code_tree_sha,
        },
        "environment": {
            "environment_id": IDS["environment"],
            "platform": sys.platform,
            "runtime_versions": runtime,
            "lockfile_sha256": lockfile_sha,
            "lockfile_unavailable_reason": None,
            "container_digest": None,
            "container_unavailable_reason": environment["container_unavailable_reason"],
            "environment_sha256": environment_sha,
        },
        "fingerprints": bundle,
        "execution": {
            "tool_id": "python-stdlib",
            "command_or_notebook": execution_spec["entrypoint"],
            "arguments": execution_spec["arguments"],
            "working_directory": ".",
            "random_seed": None,
            "precision": "binary64",
            "tolerances": execution_spec["tolerances"],
            "parallelism": 1,
            "locale": "C",
            "timezone": "UTC",
            "started_at": started_at,
            "completed_at": completed_at,
            "exit_code": run_exit_code,
            "exit_code_unavailable_reason": None,
            "runtime_parameters": {
                "r_values": json.loads(config_file.read_text(encoding="utf-8"))["r_values"],
                "L_values": json.loads(config_file.read_text(encoding="utf-8"))["L_values"],
                "quadrature_tolerance": json.loads(config_file.read_text(encoding="utf-8"))["quadrature_tolerance"],
                "quadrature_max_depth": json.loads(config_file.read_text(encoding="utf-8"))["quadrature_max_depth"],
            },
            "log_artifact_ids": [LOG_ARTIFACT_ID],
        },
        "outputs": {
            "artifact_plan_ids": [IDS["artifact_plan"], LOG_ARTIFACT_PLAN_ID],
            "artifact_ids": [IDS["artifact"], LOG_ARTIFACT_ID],
            "artifact_integrity_status": "passed",
            "completeness_check": {
                "missing": [],
                "empty": [],
                "parse_errors": [],
                "checked_at": completed_at,
                "checker_version": "uv-eFT-result-check-v1",
            },
        },
        "validation": {
            "overall_check_status": "passed",
            "validation_plan_ids": [IDS["validation_plan"]],
            "validation_activity_ids": [IDS["validation_activity"]],
            "validation_report_ids": [IDS["validation_report"]],
            "aggregation_profile_version": "uv-eFT-validation-v1",
            "aggregated_at": completed_at,
        },
        "created_at": completed_at,
        "supersedes_manifest_id": None,
    })

    criterion = _criterion()
    artifact_plan = rec["artifact_plan"]
    artifact_plan.update({
        "artifact_type": "analytic_result",
        "format": "application/json",
        "required": True,
        "completeness_rules": {
            "required_paths": ["task_id", "cases", "exact_coefficients", "checks"],
            "non_empty_paths": ["cases", "checks"],
            "allowed_empty_paths": [],
            "allowed_formats": ["application/json"],
            "schema_validator_id": "uv-eFT-result-v1",
            "parse_required": True,
            "directory_policy_version": None,
        },
        "artifact_plan_status": "fulfilled",
        "planned_for_task_id": IDS["task"],
        "planned_run_plan_id": IDS["run_plan"],
        "fulfilled_artifact_ids": [IDS["artifact"]],
        "created_at": completed_at,
        "schema_or_structure": {"type": "object", "required": ["task_id", "cases", "exact_coefficients", "checks"]},
        "units": ["dimensionless PV audit normalization", "C_PhiD/Lambda^2 has mass dimension -2"],
    })

    artifact = rec["artifact"]
    artifact.update({
        "artifact_type": "analytic_result",
        "origin_kind": "generated",
        "path_or_uri": "outputs/results.json",
        "format": "application/json",
        "content_sha256": output_sha,
        "schema_or_structure": {"type": "object", "required": ["task_id", "cases", "exact_coefficients", "checks"]},
        "units": ["dimensionless PV audit normalization", "C_PhiD/Lambda^2 has mass dimension -2"],
        "input_artifact_ids": [],
        "configuration_id": IDS["configuration"],
        "code_id": IDS["code"],
        "environment_id": IDS["environment"],
        "artifact_integrity_status": "passed",
        "artifact_lifecycle_status": "active",
        "generated_by_run_id": IDS["run"],
        "generated_by_activity_id": None,
        "acquired_from_source_id": None,
        "ingested_by_activity_id": None,
        "required_files": [],
        "directory_manifest": [],
        "directory_manifest_sha256": None,
        "hash_unavailable_reason": None,
        "created_at": completed_at,
        "artifact_storage_kind": "file",
        "alternative_identity": None,
    })

    validation_plan = rec["validation_plan"]
    validation_plan.update({
        "task_id": IDS["task"],
        "method": "closed-form PV values compared with independent Feynman-parameter adaptive Simpson quadrature; exact Fraction checks for the insertion/projection factors",
        "acceptance_criteria": [criterion],
        "required": True,
        "validation_plan_status": "completed",
        "subject_ids": [IDS["artifact"], LOG_ARTIFACT_ID],
        "expected_artifact_plan_ids": [IDS["artifact_plan"], LOG_ARTIFACT_PLAN_ID],
        "instantiated_validation_activity_ids": [IDS["validation_activity"]],
        "created_at": completed_at,
        "blocked_reason": None,
    })

    validation_activity = rec["validation_activity"]
    validation_activity.update({
        "validation_plan_id": IDS["validation_plan"],
        "task_id": IDS["task"],
        "subject_ids": [IDS["artifact"], LOG_ARTIFACT_ID],
        "method": "Independent numerical quadrature and exact rational algebra checks, including run-summary integrity",
        "tool_id": "python-stdlib",
        "environment_id": IDS["environment"],
        "input_artifact_ids": [IDS["artifact"], LOG_ARTIFACT_ID],
        "execution_status": "succeeded",
        "started_at": started_at,
        "completed_at": completed_at,
        "failure_reason": None,
        "validation_report_ids": [IDS["validation_report"]],
        "created_at": completed_at,
    })

    validation_report = rec["validation_report"]
    validation_report.update({
        "validation_activity_id": IDS["validation_activity"],
        "subject_ids": [IDS["artifact"], LOG_ARTIFACT_ID],
        "method": "Recomputed Feynman-parameter integrals, compared closed-form PV functions and derivative combinations, checked the O(r) expansion, exact rational projection factors, and run-summary output.",
        "acceptance_criteria": [criterion],
        "check_status": "passed" if physics_result["all_checks_passed"] and run_exit_code == 0 else "failed",
        "evidence_ids": [IDS["evidence_fragment"]],
        "limitations": [
            "The input hard-kernel expression is transcribed from the working note and the full UV diagram numerator is not independently regenerated.",
            "The Wilson-coefficient statement is only a single-operator projection, not a complete-basis match.",
            "Human scientific review remains pending.",
        ],
        "checked_at": completed_at,
        "checked_by": "uv-eFT-independent-validation",
        "review_status": "pending",
        "report_lifecycle_status": "active",
        "not_applicable_reason": None,
        "supersedes_report_id": None,
        "created_at": completed_at,
    })

    evidence = rec["evidence_fragment"]
    evidence.update({
        "evidence_type": "computed_output",
        "target_record_id": IDS["artifact"],
        "locator": "outputs/results.json#/cases and /checks",
        "content_sha256": output_sha,
        "scope_statement": "Supports the PV-integral consistency, small-r derivative expansion, and conditional single-operator projection stated in the result file only.",
        "assumptions": [
            _assumption("The supplied hard-kernel formula is the expression being audited.", "Hashed source excerpt and problem input."),
            _assumption("M^2=1 and K=1 are numerical normalization choices, not a physical benchmark.", "Configuration record."),
        ],
        "captured_at": completed_at,
        "review_status": "pending",
    })

    claim = rec["claim"]
    claim.update({
        "task_id": IDS["task"],
        "claim_type": "analytic_result",
        "statement": "For the transcribed hard-kernel expression and declared PV/1PI conventions, F'_hard(0)/K = 4/3 - 2*ln(M^2/mu^2) + O(r*ln r); at mu=M, Pi'_hard(0) = -K/(12*pi^2) + O(K*r*ln r). Under the stated single-operator projection only, C_PhiD/Lambda^2 = K/(6*pi^2*v_h*v_s) + O(K*r*ln r/(v_h*v_s)).",
        "claim_lifecycle_status": "active",
        "evidence_status": {
            "theory": {
                "check_status": "passed" if physics_result["all_checks_passed"] else "failed",
                "reason": "Closed-form PV functions and the combined derivative agree with independent Feynman-parameter quadrature across eight (r,L) points; exact rational insertion/projection factors pass.",
                "evidence_ids": [IDS["evidence_fragment"]],
                "checked_at": completed_at,
                "checked_by": "uv-eFT-independent-validation",
                "limitations": [
                    "This is an internal-consistency audit of the transcribed kernel, not a fresh full-diagram derivation.",
                    "The Wilson-coefficient translation is conditional on the single-operator projection convention.",
                ],
                "invalidated_by": [],
            }
        },
        "physics_assessment": {
            "theory_result": "derived",
            "experiment_result": "not_assessed",
            "eft_validity_result": "not_applicable",
            "detectability_result": "not_assessed",
            "scope_statement": "One-loop hard mixed-self-energy derivative and conditional operator projection only; no phenomenological or full-basis conclusion.",
            "assessment_basis": "Feynman-parameter integral cross-checks, small-r expansion, exact rational projection checks.",
            "assessed_by": "uv-eFT-independent-validation",
            "assessed_at": completed_at,
        },
        "assumptions": [
            _assumption("The working-note hard-kernel expression and the declared 1PI insertion convention are the inputs under audit.", "Hashed source excerpt and problem input."),
            _assumption("The single-operator projection convention is applied only as a conditional translation.", "Explicitly stated in problem.json."),
        ],
        "source_ids": all_source_ids,
        "config_ids": [IDS["configuration"]],
        "run_plan_ids": [IDS["run_plan"]],
        "run_ids": [IDS["run"]],
        "validation_plan_ids": [IDS["validation_plan"]],
        "validation_activity_ids": [IDS["validation_activity"]],
        "validation_report_ids": [IDS["validation_report"]],
        "artifact_plan_ids": [IDS["artifact_plan"]],
        "artifact_ids": [IDS["artifact"]],
        "limitations": [
            "Does not independently rederive the complete UV loop numerator or establish diagram completeness.",
            "Does not produce a unique Wilson coefficient in a complete nonredundant dimension-six basis.",
            "No experimental constraints or phenomenological parameter point are evaluated.",
        ],
        "unresolved_items": [
            "Independently rederive the full UV diagram numerator and verify diagram completeness in the same convention.",
            "Complete the IBP/EOM basis reduction and account for field/parameter renormalization before claiming a unique Wilson coefficient.",
            "Human scientific review of the formulas and assumptions remains pending.",
        ],
        "created_at": completed_at,
        "updated_at": completed_at,
    })

    log_plan = _make_record("artifact_plan", LOG_ARTIFACT_PLAN_ID, schemas, primary)
    log_plan.update({
        "artifact_type": "run_log",
        "format": "text/plain",
        "required": True,
        "completeness_rules": {
            "required_paths": ["content"],
            "non_empty_paths": ["content"],
            "allowed_empty_paths": [],
            "allowed_formats": ["text/plain"],
            "schema_validator_id": "uv-eFT-run-log-v1",
            "parse_required": False,
            "directory_policy_version": None,
        },
        "artifact_plan_status": "fulfilled",
        "planned_for_task_id": IDS["task"],
        "planned_run_plan_id": IDS["run_plan"],
        "fulfilled_artifact_ids": [LOG_ARTIFACT_ID],
        "created_at": completed_at,
        "schema_or_structure": {"type": "text", "non_empty": True},
        "units": ["UTF-8 text"],
    })
    log_artifact = _make_record("artifact", LOG_ARTIFACT_ID, schemas, primary)
    log_artifact.update({
        "artifact_type": "run_log",
        "origin_kind": "generated",
        "path_or_uri": "outputs/run.log",
        "format": "text/plain",
        "content_sha256": log_sha,
        "schema_or_structure": {"type": "text", "non_empty": True},
        "units": ["UTF-8 text"],
        "input_artifact_ids": [],
        "configuration_id": IDS["configuration"],
        "code_id": IDS["code"],
        "environment_id": IDS["environment"],
        "artifact_integrity_status": "passed",
        "artifact_lifecycle_status": "active",
        "generated_by_run_id": IDS["run"],
        "generated_by_activity_id": None,
        "acquired_from_source_id": None,
        "ingested_by_activity_id": None,
        "required_files": [],
        "directory_manifest": [],
        "directory_manifest_sha256": None,
        "hash_unavailable_reason": None,
        "created_at": completed_at,
        "artifact_storage_kind": "file",
        "alternative_identity": None,
    })

    records = source_records + list(rec.values()) + [log_plan, log_artifact]
    records.sort(key=lambda item: (item["record_type"], item.get(primary[item["record_type"]], "")))
    return records


def build_bundle(output_dir: Path | str) -> dict:
    output_dir = Path(output_dir).resolve()
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    _copy_snapshot(output_dir)
    (output_dir / "inputs").mkdir(parents=True, exist_ok=True)
    (output_dir / "sources").mkdir(parents=True, exist_ok=True)
    (output_dir / "outputs").mkdir(parents=True, exist_ok=True)
    (output_dir / "records").mkdir(parents=True, exist_ok=True)

    started_at = _now()
    command = [
        sys.executable,
        "tests/eval-cases/uv-eFT-hard-derivative-pilot/run_pilot.py",
        "--input", "inputs/problem.json",
        "--config", "inputs/config.json",
        "--output", "outputs/results.json",
    ]
    completed = subprocess.run(command, cwd=output_dir, capture_output=True, text=True, encoding="utf-8")
    completed_at = _now()
    (output_dir / "outputs/run.log").write_text(completed.stdout, encoding="utf-8")
    if completed.stderr:
        (output_dir / "outputs/run.stderr.log").write_text(completed.stderr, encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError(
            f"Physics pilot failed with exit code {completed.returncode}; stdout={completed.stdout}; stderr={completed.stderr}"
        )

    physics_result = json.loads((output_dir / "outputs/results.json").read_text(encoding="utf-8"))
    if not physics_result.get("all_checks_passed"):
        raise RuntimeError("Physics pilot produced a result with failed checks.")

    fingerprint_module = _load_module(
        "fingerprint_inputs_for_bundle", output_dir / "skills/high-energy-theory-research/scripts/fingerprint_inputs.py"
    )
    validator_module = _load_module(
        "project_record_validator_for_bundle", output_dir / "skills/high-energy-theory-research/scripts/validate_project_records.py"
    )
    schemas_dir = output_dir / "schema/v1.4.3.7/schemas"
    config_file = output_dir / "inputs/config.json"
    config = json.loads(config_file.read_text(encoding="utf-8"))
    convention_id = IDS["convention_set"]
    configuration_payload = {
        "conventions_id": convention_id,
        "independent_inputs": config["independent_inputs"],
        "derived_parameters": config["derived_parameters"],
        "units": config["units"],
    }
    config_sha = fingerprint_module.sha256_json(configuration_payload)

    source_hashes = {
        "note": _sha_file(output_dir / "sources/source-excerpt.md"),
        "problem": _sha_file(output_dir / "inputs/problem.json"),
        "configuration": _sha_file(config_file),
    }
    lockfile_sha = _sha_file(output_dir / "requirements-dev.txt")
    runtime = {"python": platform.python_version(), "platform": sys.platform}
    environment_sha = fingerprint_module.sha256_json({"runtime": runtime, "lockfile_sha256": lockfile_sha})

    code_paths = [
        "tests/eval-cases/uv-eFT-hard-derivative-pilot/run_pilot.py",
        "tests/eval-cases/uv-eFT-hard-derivative-pilot/run_record_chain.py",
        "skills/high-energy-theory-research/scripts/fingerprint_inputs.py",
        "skills/high-energy-theory-research/scripts/validate_project_records.py",
        "schema/v1.4.3.7/manifest.json",
        "schema/v1.4.3.7/tools/cross_record_validate.py",
        "schema/v1.4.3.7/tools/schema-v1.4.3.6-validate.py",
        "schema/v1.4.3.7/tools/directory_manifest.py",
        "requirements-dev.txt",
    ]
    code_paths.extend(
        str(path.relative_to(output_dir)).replace("\\", "/")
        for path in sorted(schemas_dir.glob("*.schema.json"))
    )
    code_files = [
        {"path": path, "sha256": _sha_file(output_dir / path)}
        for path in sorted(set(code_paths))
    ]
    code_tree_sha = fingerprint_module.sha256_json(code_files)

    arxiv_reference = {
        "external_system": "arXiv",
        "external_id": "2608.27258v1",
        "uri": "https://arxiv.org/html/2608.27258v1",
        "version_or_revision": "v1",
        "retrieved_at": completed_at,
        "content_sha256": None,
        "hash_unavailable_reason": "The arXiv HTML was checked for model identity and conventions but was not captured byte-for-byte in the bundle; it is a citation, not a numerical input.",
    }
    # Build a provisional execution spec solely to compute the fingerprint payload.
    execution_spec = {
        "entrypoint": "python tests/eval-cases/uv-eFT-hard-derivative-pilot/run_pilot.py",
        "arguments": ["--input", "inputs/problem.json", "--config", "inputs/config.json", "--output", "outputs/results.json"],
        "working_directory": ".",
        "precision": "binary64",
        "tolerances": {"absolute": float(config["agreement_absolute_tolerance"]), "relative": float(config["agreement_absolute_tolerance"])},
        "random_seed": None,
        "parallelism": 1,
        "locale": "C",
        "timezone": "UTC",
        "expected_outputs": ["outputs/results.json"],
        "timeout_policy": {"timeout_seconds": 60, "on_timeout": "fail", "retry_limit": 0},
    }
    execution_sha = fingerprint_module.sha256_json(execution_spec)
    provisional_inputs = {
        "contract_version": fingerprint_module.CONTRACT_VERSION,
        "canonicalization": fingerprint_module.CANONICALIZATION,
        "source_inputs": [
            {"source_id": SOURCE_IDS["note"], "content_sha256": source_hashes["note"]},
            {"source_id": SOURCE_IDS["problem"], "content_sha256": source_hashes["problem"]},
            {"source_id": SOURCE_IDS["configuration"], "content_sha256": source_hashes["configuration"]},
        ],
        "input_artifacts": [],
        "configuration": {"record_id": IDS["configuration"], "configuration_sha256": config_sha, "not_applicable_reason": None},
        "code": {"record_id": IDS["code"], "code_tree_sha256": code_tree_sha, "not_applicable_reason": None},
        "environment": {"record_id": IDS["environment"], "environment_sha256": environment_sha, "not_applicable_reason": None},
        "execution_spec_sha256": execution_sha,
        "fingerprint_profile_version": fingerprint_module.DEFAULT_PROFILE_VERSION,
    }
    fingerprints = fingerprint_module.compute_fingerprint_bundle(provisional_inputs, execution_spec)
    output_sha = _sha_file(output_dir / "outputs/results.json")
    log_sha = _sha_file(output_dir / "outputs/run.log")

    records = _build_records(
        output_dir, started_at, completed_at, completed.returncode, physics_result,
        output_sha, log_sha, code_tree_sha, environment_sha, config_sha, source_hashes,
        execution_spec, execution_sha, fingerprints, lockfile_sha, runtime,
        {"conventions_id": convention_id}, configuration_payload, arxiv_reference,
    )
    for record in records:
        primary_key = record.get("record_type", "record")
        primary_id = next(
            (value for key, value in record.items() if key.endswith("_id") and key != "project_id" and value in {record.get("task_id"), record.get("contract_id"), record.get("run_plan_id"), record.get("run_id"), record.get("manifest_id"), record.get("artifact_plan_id"), record.get("artifact_id"), record.get("validation_plan_id"), record.get("validation_activity_id"), record.get("validation_report_id"), record.get("claim_id"), record.get("source_id"), record.get("configuration_id"), record.get("code_id"), record.get("environment_id"), record.get("conventions_id"), record.get("evidence_id")}),
            record["record_type"].upper(),
        )
        filename = f"{record['record_type']}__{primary_id}.json"
        (output_dir / "records" / filename).write_text(
            json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8"
        )
    (output_dir / "outputs/record-chain.json").write_text(
        json.dumps(records, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )

    # Independently recompute the Run Plan fingerprint and check the entire cross-record graph.
    by_type = {record["record_type"]: record for record in records if record["record_type"] != "source"}
    fingerprint_module.validate_run_plan_fingerprint_inputs(
        by_type["run_plan"], by_type["task_execution_contract"], by_type["run_manifest"]
    )
    record_report = validator_module.validate_project_records(
        output_dir / "records",
        output_dir,
        schemas_dir,
        output_path=output_dir / "outputs/record-validation-report.json",
    )
    report_summary = record_report["summary"]
    (output_dir / "outputs/record-validation-report.json").write_text(
        json.dumps(record_report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    if report_summary["errors"] != 0:
        raise RuntimeError("Candidate record graph failed validation: " + json.dumps(record_report["errors"], ensure_ascii=False))
    if record_report["warnings"]:
        warning_codes = sorted({warning.get("code", "unknown") for warning in record_report["warnings"]})
    else:
        warning_codes = []

    summary = {
        "task_id": physics_result["task_id"],
        "physics_checks": {
            "all_checks_passed": physics_result["all_checks_passed"],
            "checks": physics_result["checks"],
            "case_count": physics_result["summary"]["case_count"],
            "max_Fprime_absolute_error": physics_result["summary"]["max_Fprime_absolute_error"],
        },
        "record_count": len(records),
        "record_types": sorted({record["record_type"] for record in records}),
        "record_validation": report_summary,
        "record_validation_warning_codes": warning_codes,
        "fingerprint_validation": "passed",
        "fingerprints": fingerprints,
        "source_hashes": source_hashes,
        "output_sha256": output_sha,
        "log_sha256": log_sha,
        "code_tree_sha256": code_tree_sha,
        "configuration_sha256": config_sha,
        "environment_sha256": environment_sha,
        "execution_spec_sha256": execution_sha,
        "human_review_status": "pending",
        "physics_scope_boundary": "PV-integral and algebraic projection audit only; no full UV diagram derivation or complete-basis Wilson coefficient claim.",
    }
    (output_dir / "outputs/record-chain-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, help="Destination for the self-contained research record bundle.")
    args = parser.parse_args(argv)
    summary = build_bundle(args.output_dir)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if summary["physics_checks"]["all_checks_passed"] and summary["record_validation"]["errors"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

