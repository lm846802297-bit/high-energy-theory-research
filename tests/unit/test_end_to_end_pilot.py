from copy import deepcopy
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import sys
import tempfile
import unittest

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
PILOT_DIR = ROOT / "tests" / "eval-cases" / "analytic-mass-matrix-pilot"
SCHEMA_DIR = ROOT / "schema" / "v1.4.3.7" / "schemas"
TIMESTAMP = "2026-10-21T00:00:00Z"
PROJECT_ID = "PILOT-MATRIX-001"

def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

PILOT = _load_module("analytic_mass_matrix_pilot", PILOT_DIR / "run_pilot.py")
VALIDATOR = _load_module(
    "skill_project_record_validator",
    ROOT / "skills" / "high-energy-theory-research" / "scripts" / "validate_project_records.py",
)

PRIMARY = {
    "task": "task_id",
    "task_execution_contract": "contract_id",
    "run_plan": "run_plan_id",
    "run": "run_id",
    "run_manifest": "manifest_id",
    "artifact_plan": "artifact_plan_id",
    "artifact": "artifact_id",
    "validation_plan": "validation_plan_id",
    "validation_activity": "validation_activity_id",
    "validation_report": "validation_report_id",
    "claim": "claim_id",
    "source": "source_id",
    "configuration": "configuration_id",
    "code": "code_id",
    "environment": "environment_id",
    "convention_set": "conventions_id",
    "evidence_fragment": "evidence_id",
}

IDS = {
    "task": "TASK-E2E-001",
    "task_execution_contract": "TEC-E2E-001",
    "run_plan": "RUNPLAN-E2E-001",
    "run": "RUN-E2E-001",
    "run_manifest": "MANIFEST-E2E-001",
    "artifact_plan": "ARTPLAN-E2E-001",
    "artifact": "ART-E2E-001",
    "validation_plan": "VALPLAN-E2E-001",
    "validation_activity": "VALACT-E2E-001",
    "validation_report": "VALREP-E2E-001",
    "claim": "CLAIM-E2E-001",
    "source": "SRC-E2E-001",
    "configuration": "CONF-E2E-001",
    "code": "CODE-E2E-001",
    "environment": "ENV-E2E-001",
    "convention_set": "CONV-E2E-001",
    "evidence_fragment": "EVID-E2E-001",
}

def _sha(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def _json_hash(value):
    return _sha(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False))

def _minimal_value(schema, root_schema):
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            raise AssertionError(f"Unsupported external schema reference in pilot: {ref}")
        target = root_schema
        for part in ref[2:].split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
        return _minimal_value(target, root_schema)
    if "const" in schema:
        return deepcopy(schema["const"])
    if "enum" in schema:
        return deepcopy(schema["enum"][0])
    for choice_key in ("oneOf", "anyOf"):
        if choice_key in schema:
            for choice in schema[choice_key]:
                candidate = _minimal_value(choice, root_schema)
                try:
                    if Draft202012Validator(choice).is_valid(candidate):
                        return candidate
                except Exception:
                    pass
            return _minimal_value(schema[choice_key][0], root_schema)

    value_type = schema.get("type")
    if isinstance(value_type, list):
        if "null" in value_type:
            return None
        value_type = value_type[0] if value_type else None
    if value_type is None and ("properties" in schema or "required" in schema):
        value_type = "object"

    if value_type == "object":
        properties = schema.get("properties", {})
        return {
            name: _minimal_value(properties[name], root_schema)
            for name in schema.get("required", [])
            if name in properties
        }
    if value_type == "array":
        minimum = schema.get("minItems", 0)
        item_schema = schema.get("items", {})
        return [_minimal_value(item_schema, root_schema) for _ in range(minimum)]
    if value_type == "string":
        if schema.get("format") == "date-time":
            return TIMESTAMP
        if schema.get("format") == "uri":
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

def _load_schemas():
    return {
        path.name.removesuffix(".schema.json"): json.loads(path.read_text(encoding="utf-8"))
        for path in SCHEMA_DIR.glob("*.schema.json")
    }

def _make_records(result_path, result_hash):
    schemas = _load_schemas()
    records = {}
    for record_type, record_id in IDS.items():
        schema = schemas[record_type]
        record = _minimal_value(schema, schema)
        record["schema_version"] = "1.4"
        record["record_type"] = record_type
        record["project_id"] = PROJECT_ID
        record[PRIMARY[record_type]] = record_id
        records[record_type] = record

    problem_path = PILOT_DIR / "problem.json"
    problem_hash = _sha(problem_path.read_bytes())
    script_path = PILOT_DIR / "run_pilot.py"
    expected_path = PILOT_DIR / "expected-results.json"
    code_files = []
    for path in sorted((problem_path, expected_path, script_path)):
        code_files.append({
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": _sha(path.read_bytes()),
        })
    code_tree_hash = _json_hash(code_files)
    lockfile_hash = _sha((ROOT / "requirements-dev.txt").read_bytes())
    runtime = {"python": platform.python_version(), "platform": sys.platform}
    environment_hash = _json_hash({"runtime": runtime, "lockfile_sha256": lockfile_hash})
    config_payload = {
        "conventions_id": IDS["convention_set"],
        "independent_inputs": ["M2=[[5,2],[2,8]]"],
        "derived_parameters": ["eigenvalues", "masses"],
        "units": ["TeV^2", "TeV"],
    }

    task = records["task"]
    task.update({
        "title": "Analytic diagonalization of a 2x2 real symmetric mass-squared matrix",
        "task_type": "analytic_derivation",
        "task_status": "complete",
        "active_contract_id": IDS["task_execution_contract"],
        "dependency_task_ids": [],
        "claim_ids": [IDS["claim"]],
        "status_reason": None,
        "completion_evidence_ids": [IDS["evidence_fragment"]],
        "created_at": TIMESTAMP,
        "updated_at": TIMESTAMP,
    })

    contract = records["task_execution_contract"]
    contract.update({
        "task_id": IDS["task"],
        "contract_version": 1,
        "contract_status": "approved",
        "objective": "Derive and independently check the eigenvalues of the supplied toy matrix.",
        "scope": {
            "included": ["closed-form eigenvalues", "trace/determinant checks", "eigenvector checks"],
            "excluded": ["complete particle-physics model", "experimental constraints"],
            "target_domain": "synthetic algebraic test",
            "out_of_scope_behavior": "Do not infer phenomenological validity.",
        },
        "input_refs": {
            "source_ids": [IDS["source"]],
            "configuration_ids": [IDS["configuration"]],
            "input_artifact_ids": [],
            "external_references": [],
        },
        "assumptions": [{"assumption_id": "ASM-E2E-001", "description": "The matrix is real symmetric and entries are in TeV^2.", "scope": "This single toy matrix.", "status": "accepted", "source_or_rationale": "Explicit input declaration in problem.json."}],
        "conventions_id": IDS["convention_set"],
        "conventions_reason": None,
        "required_capabilities": ["python-stdlib"],
        "planned_methods": [{"method_id": "METHOD-E2E-001", "description": "Analytic eigenvalue formula with independent checks.", "scope": "The supplied 2x2 matrix only.", "status": "accepted", "source_or_rationale": "The closed-form characteristic equation is exact for a real symmetric 2x2 matrix."}],
        "artifact_plan_ids": [IDS["artifact_plan"]],
        "validation_plan_ids": [IDS["validation_plan"]],
        "acceptance_criteria": [{
            "criterion_id": "AC-E2E-001",
            "description": "Eigenvalues, masses, and independent invariants agree with the exact solution.",
            "required": True,
            "verification_method": "unit test",
            "pass_condition": "all numerical and algebraic checks pass",
            "failure_condition": "any invariant or residual check fails",
            "evidence_kind": "computed_result",
        }],
        "failure_branches": ["Reject malformed or non-symmetric matrices."],
        "stop_conditions": ["Stop if any independent check fails."],
        "approved_at": TIMESTAMP,
        "approved_by": "automated-test-fixture",
        "supersedes_contract_id": None,
    })
    contract["contract_sha256"] = _json_hash({
        key: value for key, value in contract.items() if key != "contract_sha256"
    })

    source = records["source"]
    source.update({
        "source_type": "local_problem_specification",
        "title": "Analytic mass-matrix pilot input",
        "uri_or_path": str(problem_path.relative_to(ROOT)).replace("\\", "/"),
        "source_version": "pilot-v1",
        "content_sha256": problem_hash,
        "retrieved_at": TIMESTAMP,
        "lifecycle_status": "active",
        "verification_status": "verified",
        "hash_unavailable_reason": None,
    })

    convention = records["convention_set"]
    convention.update({
        "notation": "M2 is the matrix of squared masses in the stated basis.",
        "metric_signature": "not applicable to this finite-dimensional algebra exercise",
        "unit_system": "matrix entries in TeV^2; masses in TeV",
        "gauge_conventions": "not applicable",
        "renormalization_scheme": "not applicable",
        "flavor_basis": "basis (1,2) as given in problem.json",
        "phase_conventions": "real normalized eigenvectors; overall signs are arbitrary",
        "applicability_notes": "synthetic algebraic pilot only",
        "content_sha256": problem_hash,
    })

    configuration = records["configuration"]
    configuration.update({
        **config_payload,
        "configuration_sha256": _json_hash(config_payload),
        "created_at": TIMESTAMP,
    })

    code = records["code"]
    github_sha = os.environ.get("GITHUB_SHA")
    code.update({
        "repository_uri": "https://github.com/lm846802297-bit/high-energy-theory-research",
        "git_commit": github_sha or "unavailable-in-local-test",
        "git_commit_unavailable_reason": None if github_sha else "GITHUB_SHA is not set in this local/test context.",
        "dirty": not bool(github_sha),
        "diff_sha256": _sha(b"") if github_sha else _sha(b"local diff not captured"),
        "code_tree_sha256": code_tree_hash,
        "created_at": TIMESTAMP,
    })

    environment = records["environment"]
    environment.update({
        "platform": sys.platform,
        "runtime_versions": runtime,
        "lockfile_sha256": lockfile_hash,
        "lockfile_unavailable_reason": None,
        "container_digest": None,
        "container_unavailable_reason": "The hosted runner image digest is not pinned by this pilot.",
        "environment_sha256": environment_hash,
        "created_at": TIMESTAMP,
    })

    execution_spec = {
        "entrypoint": "python tests/eval-cases/analytic-mass-matrix-pilot/run_pilot.py",
        "arguments": ["--input", str(problem_path.relative_to(ROOT)), "--output", str(result_path.relative_to(ROOT))],
        "working_directory": ".",
        "precision": "binary64",
        "tolerances": {"absolute": 1e-12, "relative": 1e-12},
        "random_seed": None,
        "parallelism": 1,
        "locale": "C",
        "timezone": "UTC",
        "expected_outputs": ["results.json"],
        "timeout_policy": {"timeout_seconds": 30, "on_timeout": "fail", "retry_limit": 0},
    }
    run_plan = records["run_plan"]
    run_plan.update({
        "task_id": IDS["task"],
        "contract_id": IDS["task_execution_contract"],
        "run_plan_status": "instantiated",
        "configuration_id": IDS["configuration"],
        "code_id": IDS["code"],
        "environment_id": IDS["environment"],
        "input_artifact_ids": [],
        "artifact_plan_ids": [IDS["artifact_plan"]],
        "validation_plan_ids": [IDS["validation_plan"]],
        # Current candidate schema permits only empty objects here; see gap test.
        "execution_spec": execution_spec,
        "fingerprint_inputs": {},
        "execution_spec_sha256": _json_hash(execution_spec),
        "instantiated_run_id": IDS["run"],
        "blocked_reason": None,
        "supersedes_run_plan_id": None,
        "created_at": TIMESTAMP,
    })

    run = records["run"]
    run.update({
        "task_id": IDS["task"],
        "contract_id": IDS["task_execution_contract"],
        "run_plan_id": IDS["run_plan"],
        "execution_status": "succeeded",
        "started_at": TIMESTAMP,
        "completed_at": TIMESTAMP,
        "exit_code": 0,
        "exit_code_unavailable_reason": None,
        "parent_run_id": None,
        "retry_of_run_id": None,
        "manifest_ids": [IDS["run_manifest"]],
        "latest_manifest_id": IDS["run_manifest"],
        "log_artifact_ids": [],
        "created_at": TIMESTAMP,
    })

    manifest = records["run_manifest"]
    manifest.update({
        "run_id": IDS["run"],
        "task_id": IDS["task"],
        "contract_id": IDS["task_execution_contract"],
        "run_plan_id": IDS["run_plan"],
        "manifest_revision": 1,
        "execution_status_snapshot": "succeeded",
        "snapshot_at": TIMESTAMP,
        "input_refs": {
            "source_ids": [IDS["source"]],
            "configuration_ids": [IDS["configuration"]],
            "input_artifact_ids": [],
            "external_references": [],
        },
        # The candidate schemas currently reject non-empty values in these
        # closed objects; the negative tests below make that limitation explicit.
        "configuration": {
            "configuration_id": IDS["configuration"],
            "conventions_id": IDS["convention_set"],
            "independent_inputs": config_payload["independent_inputs"],
            "derived_parameters": config_payload["derived_parameters"],
            "units": config_payload["units"],
            "configuration_sha256": configuration["configuration_sha256"],
        },
        "code": {
            "code_id": IDS["code"],
            "repository_uri": code["repository_uri"],
            "repository_uri_unavailable_reason": None,
            "git_commit": code["git_commit"],
            "git_commit_unavailable_reason": code["git_commit_unavailable_reason"],
            "dirty": code["dirty"],
            "diff_sha256": code["diff_sha256"],
            "code_tree_sha256": code["code_tree_sha256"],
        },
        "environment": {
            "environment_id": IDS["environment"],
            "platform": environment["platform"],
            "runtime_versions": environment["runtime_versions"],
            "lockfile_sha256": environment["lockfile_sha256"],
            "lockfile_unavailable_reason": environment["lockfile_unavailable_reason"],
            "container_digest": environment["container_digest"],
            "container_unavailable_reason": environment["container_unavailable_reason"],
            "environment_sha256": environment["environment_sha256"],
        },
        "fingerprints": {
            "algorithm": "sha256",
            "input_set_sha256": _json_hash({"source_sha256": problem_hash, "configuration_sha256": configuration["configuration_sha256"], "input_artifact_ids": []}),
            "configuration_sha256": configuration["configuration_sha256"],
            "code_tree_sha256": code_tree_hash,
            "environment_sha256": environment_hash,
            "execution_spec_sha256": _json_hash(execution_spec),
            "dependency_artifact_sha256": _json_hash([]),
            "composite_sha256": _json_hash({
                "algorithm": "sha256",
                "input_set_sha256": _json_hash({"source_sha256": problem_hash, "configuration_sha256": configuration["configuration_sha256"], "input_artifact_ids": []}),
                "configuration_sha256": configuration["configuration_sha256"],
                "code_tree_sha256": code_tree_hash,
                "environment_sha256": environment_hash,
                "execution_spec_sha256": _json_hash(execution_spec),
                "dependency_artifact_sha256": _json_hash([]),
                "fingerprint_profile_version": "pilot-fingerprint-v1",
            }),
            "fingerprint_profile_version": "pilot-fingerprint-v1",
        },
        "execution": {
            "tool_id": "python-stdlib",
            "command_or_notebook": "python tests/eval-cases/analytic-mass-matrix-pilot/run_pilot.py",
            "arguments": ["--input", str(problem_path.relative_to(ROOT)), "--output", str(result_path.relative_to(ROOT))],
            "working_directory": ".",
            "random_seed": None,
            "precision": "binary64",
            "tolerances": {"absolute": 1e-12, "relative": 1e-12},
            "parallelism": 1,
            "locale": "C",
            "timezone": "UTC",
            "started_at": TIMESTAMP,
            "completed_at": TIMESTAMP,
            "exit_code": 0,
            "exit_code_unavailable_reason": None,
            "runtime_parameters": runtime,
            "log_artifact_ids": [],
        },
        "outputs": {
            "artifact_plan_ids": [IDS["artifact_plan"]],
            "artifact_ids": [IDS["artifact"]],
            "artifact_integrity_status": "passed",
            "completeness_check": {
                "missing": [],
                "empty": [],
                "parse_errors": [],
                "checked_at": TIMESTAMP,
                "checker_version": "pilot-result-check-v1",
            },
        },
        "validation": {
            "overall_check_status": "passed",
            "validation_plan_ids": [IDS["validation_plan"]],
            "validation_activity_ids": [IDS["validation_activity"]],
            "validation_report_ids": [IDS["validation_report"]],
            "aggregation_profile_version": "pilot-validation-v1",
            "aggregated_at": TIMESTAMP,
        },
        "created_at": TIMESTAMP,
        "supersedes_manifest_id": None,
    })

    artifact_plan = records["artifact_plan"]
    artifact_plan.update({
        "artifact_type": "analytic_result",
        "format": "application/json",
        "required": True,
        "completeness_rules": {
            "required_paths": ["eigenvalues", "masses", "checks"],
            "non_empty_paths": ["eigenvalues", "masses"],
            "allowed_empty_paths": [],
            "allowed_formats": ["application/json"],
            "schema_validator_id": "pilot-result-v1",
            "parse_required": True,
            "directory_policy_version": None,
        },
        "artifact_plan_status": "fulfilled",
        "planned_for_task_id": IDS["task"],
        "planned_run_plan_id": IDS["run_plan"],
        "fulfilled_artifact_ids": [IDS["artifact"]],
        "created_at": TIMESTAMP,
        "schema_or_structure": {},
        "units": ["TeV^2", "TeV"],
    })

    artifact = records["artifact"]
    artifact.update({
        "artifact_type": "analytic_result",
        "origin_kind": "generated",
        "path_or_uri": str(result_path.relative_to(ROOT)).replace("\\", "/"),
        "format": "application/json",
        "content_sha256": result_hash,
        "schema_or_structure": {"type": "object", "required": ["eigenvalues", "masses", "checks"]},
        "units": ["TeV^2", "TeV"],
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
        "created_at": TIMESTAMP,
        "artifact_storage_kind": "file",
        "alternative_identity": None,
    })

    criteria = [{
        "criterion_id": "AC-E2E-001",
        "description": "The exact eigenvalues, trace, determinant, eigenvectors, and positivity checks pass.",
        "required": True,
        "verification_method": "Python standard-library test",
        "pass_condition": "all checks are true and eigenpair residuals are below tolerance",
        "failure_condition": "any check fails",
        "evidence_kind": "computed_result",
    }]
    validation_plan = records["validation_plan"]
    validation_plan.update({
        "task_id": IDS["task"],
        "method": "analytic formula plus independent invariants and eigenvector residuals",
        "acceptance_criteria": criteria,
        "required": True,
        "validation_plan_status": "completed",
        "subject_ids": [IDS["artifact"]],
        "expected_artifact_plan_ids": [IDS["artifact_plan"]],
        "instantiated_validation_activity_ids": [IDS["validation_activity"]],
        "created_at": TIMESTAMP,
        "blocked_reason": None,
    })

    validation_activity = records["validation_activity"]
    validation_activity.update({
        "validation_plan_id": IDS["validation_plan"],
        "task_id": IDS["task"],
        "subject_ids": [IDS["artifact"]],
        "method": "automated independent checks",
        "tool_id": "python-stdlib",
        "environment_id": IDS["environment"],
        "input_artifact_ids": [IDS["artifact"]],
        "execution_status": "succeeded",
        "started_at": TIMESTAMP,
        "completed_at": TIMESTAMP,
        "failure_reason": None,
        "validation_report_ids": [IDS["validation_report"]],
        "created_at": TIMESTAMP,
    })

    validation_report = records["validation_report"]
    validation_report.update({
        "validation_activity_id": IDS["validation_activity"],
        "subject_ids": [IDS["artifact"]],
        "method": "trace/determinant, normalized eigenvectors, orthogonality, residuals, positivity",
        "acceptance_criteria": criteria,
        "check_status": "passed",
        "evidence_ids": [IDS["evidence_fragment"]],
        "limitations": [
            "synthetic matrix only",
            "human review remains pending",
            "candidate manifest and claim evidence schemas are not expressive enough for full provenance",
        ],
        "checked_at": TIMESTAMP,
        "checked_by": "automated-pilot-test",
        "review_status": "pending",
        "report_lifecycle_status": "active",
        "not_applicable_reason": None,
        "supersedes_report_id": None,
        "created_at": TIMESTAMP,
    })

    evidence = records["evidence_fragment"]
    evidence.update({
        "evidence_type": "computed_output",
        "target_record_id": IDS["artifact"],
        "locator": "results.json#/eigenvalues and results.json#/checks",
        "content_sha256": result_hash,
        "scope_statement": "Supports the eigenvalues and checks for the single matrix in problem.json only.",
        "assumptions": [{"assumption_id": "ASM-E2E-001", "description": "The input matrix is real symmetric.", "scope": "The computed eigenvalues and checks for this input only.", "status": "accepted", "source_or_rationale": "Explicit input declaration in problem.json."}],
        "captured_at": TIMESTAMP,
        "review_status": "pending",
    })

    claim = records["claim"]
    claim.update({
        "task_id": IDS["task"],
        "claim_type": "analytic_result",
        "statement": "For the supplied toy matrix, the eigenvalues are 4 and 9 TeV^2 and the corresponding masses are 2 and 3 TeV.",
        "claim_lifecycle_status": "active",
        # Empty because the candidate schema disallows dimension keys today.
        "evidence_status": {
            "theory": {
                "check_status": "passed",
                "reason": "Closed-form eigenvalues agree with independent invariants and eigenvector checks.",
                "evidence_ids": [IDS["evidence_fragment"]],
                "checked_at": TIMESTAMP,
                "checked_by": "automated-pilot-test",
                "limitations": ["toy matrix only"],
                "invalidated_by": [],
            }
        },
        "physics_assessment": {
            "theory_result": "derived",
            "experiment_result": "not_assessed",
            "eft_validity_result": "not_applicable",
            "detectability_result": "not_assessed",
            "scope_statement": "toy matrix only; not a phenomenological model",
            "assessment_basis": "closed-form solution and independent algebraic checks",
            "assessed_by": "automated-pilot-test",
            "assessed_at": TIMESTAMP,
        },
        "assumptions": [{"assumption_id": "ASM-E2E-001", "description": "The matrix is real symmetric and expressed in TeV^2.", "scope": "This single toy matrix.", "status": "accepted", "source_or_rationale": "Explicit input declaration in problem.json."}],
        "source_ids": [IDS["source"]],
        "config_ids": [IDS["configuration"]],
        "run_plan_ids": [IDS["run_plan"]],
        "run_ids": [IDS["run"]],
        "validation_plan_ids": [IDS["validation_plan"]],
        "validation_activity_ids": [IDS["validation_activity"]],
        "validation_report_ids": [IDS["validation_report"]],
        "artifact_plan_ids": [IDS["artifact_plan"]],
        "artifact_ids": [IDS["artifact"]],
        "limitations": ["No model-building or experimental inference is included."],
        "unresolved_items": [
            "Full evidence-dimension statuses cannot be stored in the current candidate schema.",
            "The Run Manifest snapshot objects cannot store their intended non-empty payloads."
        ],
        "created_at": TIMESTAMP,
        "updated_at": TIMESTAMP,
    })

    return records, schemas


class EndToEndResearchSkillPilotTests(unittest.TestCase):
    def test_analytic_result_and_independent_checks(self):
        problem = json.loads((PILOT_DIR / "problem.json").read_text(encoding="utf-8"))
        expected = json.loads((PILOT_DIR / "expected-results.json").read_text(encoding="utf-8"))
        result = PILOT.solve(problem)
        self.assertEqual(result["eigenvalues"], [float(x) for x in expected["expected_eigenvalues"]])
        self.assertEqual(result["masses"], [float(x) for x in expected["expected_masses"]])
        self.assertEqual(result["invariants"]["trace"], expected["expected_trace"])
        self.assertEqual(result["invariants"]["determinant"], expected["expected_determinant"])
        self.assertTrue(result["checks"]["positive_definite_by_sylvester"])
        self.assertTrue(result["all_checks_passed"], result["checks"])

    def test_synthetic_research_record_chain_passes_bounded_validator(self):
        problem_path = PILOT_DIR / "problem.json"
        generated_path = PILOT_DIR / ".generated-results.json"
        result = PILOT.run(problem_path, generated_path)
        self.addCleanup(lambda: generated_path.unlink(missing_ok=True))
        self.assertTrue(result["all_checks_passed"])

        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        records_dir = Path(temp.name) / "records"
        records_dir.mkdir()
        report_path = Path(temp.name) / "validation-report.json"
        records, _schemas = _make_records(generated_path, _sha(generated_path.read_bytes()))
        for index, (record_type, record) in enumerate(records.items()):
            (records_dir / f"{index:02d}-{record_type}.json").write_text(
                json.dumps(record, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        report = VALIDATOR.validate_project_records(
            records_dir,
            ROOT,
            SCHEMA_DIR,
            output_path=report_path,
        )
        self.assertEqual(report["summary"]["errors"], 0, json.dumps(report["errors"], ensure_ascii=False, indent=2))
        self.assertGreaterEqual(report["summary"]["records"], 17)
        self.assertTrue(generated_path.is_file())

    def test_structured_payloads_are_supported_except_undefined_fingerprint_inputs(self):
        schemas = _load_schemas()
        records, _ = _make_records(PILOT_DIR / "expected-results.json", _sha((PILOT_DIR / "expected-results.json").read_bytes()))

        accepted = [
            ("run_plan", "execution_spec", {
                "entrypoint": "python run_pilot.py", "arguments": [], "working_directory": ".",
                "precision": "binary64", "tolerances": {"absolute": 1e-12}, "random_seed": None,
                "parallelism": 1, "locale": "C", "timezone": "UTC", "expected_outputs": ["results.json"],
                "timeout_policy": {"timeout_seconds": 30, "on_timeout": "fail", "retry_limit": 0},
            }),
            ("run_manifest", "outputs", {
                "artifact_plan_ids": [IDS["artifact_plan"]], "artifact_ids": [IDS["artifact"]],
                "artifact_integrity_status": "passed",
                "completeness_check": {"missing": [], "empty": [], "parse_errors": [], "checked_at": TIMESTAMP, "checker_version": "test-v1"},
            }),
            ("run_manifest", "code", {"code_id": IDS["code"], "repository_uri": "https://example.org/repo"}),
            ("claim", "evidence_status", {"theory": {
                "check_status": "passed", "reason": "independent check passed", "evidence_ids": [IDS["evidence_fragment"]],
                "checked_at": TIMESTAMP, "checked_by": "test", "limitations": [], "invalidated_by": [],
            }}),
            ("artifact_plan", "completeness_rules", {
                "required_paths": ["eigenvalues"], "non_empty_paths": ["eigenvalues"], "allowed_empty_paths": [],
                "allowed_formats": ["application/json"], "schema_validator_id": "test-v1",
                "parse_required": True, "directory_policy_version": None,
            }),
            ("artifact_plan", "schema_or_structure", {"type": "object", "required": ["eigenvalues"]}),
            ("artifact", "schema_or_structure", {"type": "object", "required": ["eigenvalues"]}),
        ]
        for record_type, field, value in accepted:
            with self.subTest(record_type=record_type, field=field):
                candidate = deepcopy(records[record_type])
                candidate[field] = value
                errors = list(Draft202012Validator(schemas[record_type]).iter_errors(candidate))
                self.assertFalse(errors, f"{record_type}.{field} should accept its declared structured payload: {errors}")

        candidate = deepcopy(records["run_plan"])
        candidate["fingerprint_inputs"] = {"code_tree_sha256": "a" * 64}
        errors = list(Draft202012Validator(schemas["run_plan"]).iter_errors(candidate))
        self.assertTrue(errors, "fingerprint_inputs must remain blocked until its field contract is defined")

        readme = (PILOT_DIR / "README.md").read_text(encoding="utf-8")
        self.assertIn("full reproducibility acceptance remains blocked", readme)
        self.assertIn("run_plan.fingerprint_inputs", readme)
        self.assertIn("not define its fields", readme)


if __name__ == "__main__":
    unittest.main()
