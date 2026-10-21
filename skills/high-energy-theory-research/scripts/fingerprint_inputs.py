#!/usr/bin/env python3
"""Candidate FingerprintInputs contract using RFC 8785 JSON canonicalization.

This module computes reproducibility fingerprints; it does not validate physics.
The contract remains candidate-only until the governance review is approved.
"""
from __future__ import annotations

import hashlib
import re
from typing import Any

import rfc8785

CONTRACT_VERSION = "fingerprint-inputs-v1"
CANONICALIZATION = "RFC8785"
DEFAULT_PROFILE_VERSION = "fingerprint-profile-v1"
_SHA256_RE = re.compile(r"^[a-f0-9]{64}$")


class FingerprintInputsError(ValueError):
    """Raised when fingerprint inputs are incomplete or internally inconsistent."""


def canonical_json_bytes(value: Any) -> bytes:
    """Return RFC 8785 canonical JSON bytes, rejecting unsupported JSON values."""
    try:
        return rfc8785.dumps(value)
    except Exception as exc:
        raise FingerprintInputsError(f"Cannot canonicalize JSON value: {exc}") from exc


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def _require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FingerprintInputsError(f"{field} must be a non-empty string")
    return value


def _require_sha256(value: Any, field: str) -> str:
    if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
        raise FingerprintInputsError(f"{field} must be a lowercase SHA-256 hex digest")
    return value


def _unique_sorted(items: Any, id_field: str, label: str) -> list[dict]:
    if not isinstance(items, list):
        raise FingerprintInputsError(f"{label} must be a list")
    normalized = []
    seen = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise FingerprintInputsError(f"{label}[{index}] must be an object")
        identifier = _require_text(item.get(id_field), f"{label}[{index}].{id_field}")
        if identifier in seen:
            raise FingerprintInputsError(f"duplicate {id_field} in {label}: {identifier}")
        seen.add(identifier)
        normalized.append(dict(item))
    return sorted(normalized, key=lambda item: item[id_field])


def _validate_component(component: Any, label: str, hash_field: str) -> tuple[str | None, str | None]:
    if not isinstance(component, dict):
        raise FingerprintInputsError(f"{label} must be an object")
    record_id = component.get("record_id")
    digest = component.get(hash_field)
    reason = component.get("not_applicable_reason")
    if record_id is None:
        if digest is not None:
            raise FingerprintInputsError(f"{label}.{hash_field} must be null when record_id is null")
        _require_text(reason, f"{label}.not_applicable_reason")
        return None, None
    _require_text(record_id, f"{label}.record_id")
    _require_sha256(digest, f"{label}.{hash_field}")
    if reason is not None:
        raise FingerprintInputsError(f"{label}.not_applicable_reason must be null when a record is referenced")
    return record_id, digest


def compute_fingerprint_bundle(fingerprint_inputs: dict, execution_spec: dict) -> dict:
    """Compute the exact FingerprintBundle payload defined by the candidate contract.

    Input-set digest covers source byte digests and input-artifact digests.
    Configuration, code, environment and execution digests are separate components
    and are all included in the composite digest.
    """
    if not isinstance(fingerprint_inputs, dict):
        raise FingerprintInputsError("fingerprint_inputs must be an object")
    if fingerprint_inputs.get("contract_version") != CONTRACT_VERSION:
        raise FingerprintInputsError(f"contract_version must be {CONTRACT_VERSION}")
    if fingerprint_inputs.get("canonicalization") != CANONICALIZATION:
        raise FingerprintInputsError(f"canonicalization must be {CANONICALIZATION}")
    profile = _require_text(fingerprint_inputs.get("fingerprint_profile_version"), "fingerprint_profile_version")

    source_inputs = _unique_sorted(fingerprint_inputs.get("source_inputs"), "source_id", "source_inputs")
    for index, item in enumerate(source_inputs):
        _require_sha256(item.get("content_sha256"), f"source_inputs[{index}].content_sha256")

    input_artifacts = _unique_sorted(fingerprint_inputs.get("input_artifacts"), "artifact_id", "input_artifacts")
    for index, item in enumerate(input_artifacts):
        if item.get("digest_kind") not in {"content_sha256", "directory_manifest_sha256"}:
            raise FingerprintInputsError(f"input_artifacts[{index}].digest_kind is invalid")
        _require_sha256(item.get("digest_sha256"), f"input_artifacts[{index}].digest_sha256")

    _, configuration_sha256 = _validate_component(
        fingerprint_inputs.get("configuration"), "configuration", "configuration_sha256"
    )
    _, code_tree_sha256 = _validate_component(
        fingerprint_inputs.get("code"), "code", "code_tree_sha256"
    )
    _, environment_sha256 = _validate_component(
        fingerprint_inputs.get("environment"), "environment", "environment_sha256"
    )

    execution_spec_sha256 = _require_sha256(
        fingerprint_inputs.get("execution_spec_sha256"), "execution_spec_sha256"
    )
    calculated_execution_sha256 = sha256_json(execution_spec)
    if execution_spec_sha256 != calculated_execution_sha256:
        raise FingerprintInputsError("execution_spec_sha256 does not match the canonical execution_spec")

    input_set_payload = {
        "contract_version": CONTRACT_VERSION,
        "canonicalization": CANONICALIZATION,
        "source_inputs": source_inputs,
        "input_artifacts": input_artifacts,
    }
    input_set_sha256 = sha256_json(input_set_payload)
    dependency_artifact_sha256 = sha256_json(input_artifacts)
    bundle = {
        "algorithm": "sha256",
        "input_set_sha256": input_set_sha256,
        "configuration_sha256": configuration_sha256,
        "code_tree_sha256": code_tree_sha256,
        "environment_sha256": environment_sha256,
        "execution_spec_sha256": execution_spec_sha256,
        "dependency_artifact_sha256": dependency_artifact_sha256,
        "fingerprint_profile_version": profile,
    }
    bundle["composite_sha256"] = sha256_json(bundle)
    return bundle


def validate_run_plan_fingerprint_inputs(run_plan: dict, contract: dict | None = None, manifest: dict | None = None) -> dict:
    """Validate the candidate fingerprint contract against linked records and return its bundle."""
    if not isinstance(run_plan, dict):
        raise FingerprintInputsError("run_plan must be an object")
    fingerprint_inputs = run_plan.get("fingerprint_inputs")
    execution_spec = run_plan.get("execution_spec")
    bundle = compute_fingerprint_bundle(fingerprint_inputs, execution_spec)

    if run_plan.get("execution_spec_sha256") != bundle["execution_spec_sha256"]:
        raise FingerprintInputsError("run_plan.execution_spec_sha256 does not match FingerprintInputs")
    for top_field, component_field in (
        ("configuration_id", "configuration"),
        ("code_id", "code"),
        ("environment_id", "environment"),
    ):
        if run_plan.get(top_field) != fingerprint_inputs[component_field].get("record_id"):
            raise FingerprintInputsError(f"run_plan.{top_field} does not match fingerprint_inputs.{component_field}.record_id")

    run_plan_artifacts = run_plan.get("input_artifact_ids", [])
    fingerprint_artifacts = [item["artifact_id"] for item in fingerprint_inputs["input_artifacts"]]
    if len(run_plan_artifacts) != len(set(run_plan_artifacts)) or sorted(run_plan_artifacts) != sorted(fingerprint_artifacts):
        raise FingerprintInputsError("run_plan.input_artifact_ids does not match fingerprint_inputs.input_artifacts")

    source_ids = {item["source_id"] for item in fingerprint_inputs["source_inputs"]}
    if contract is not None:
        refs = contract.get("input_refs", {})
        if not source_ids.issubset(set(refs.get("source_ids", []))):
            raise FingerprintInputsError("fingerprint source inputs are not declared in contract.input_refs.source_ids")
        if sorted(run_plan_artifacts) != sorted(refs.get("input_artifact_ids", [])):
            raise FingerprintInputsError("run_plan input artifacts do not match contract.input_refs.input_artifact_ids")
        record_id = fingerprint_inputs["configuration"]["record_id"]
        declared = refs.get("configuration_ids", [])
        if record_id is not None and record_id not in declared:
            raise FingerprintInputsError("fingerprint configuration is not declared in contract.input_refs.configuration_ids")

    if manifest is not None:
        refs = manifest.get("input_refs", {})
        if not source_ids.issubset(set(refs.get("source_ids", []))):
            raise FingerprintInputsError("fingerprint source inputs are not declared in manifest.input_refs.source_ids")
        if sorted(run_plan_artifacts) != sorted(refs.get("input_artifact_ids", [])):
            raise FingerprintInputsError("run_plan input artifacts do not match manifest.input_refs.input_artifact_ids")
        expected_snapshots = {
            "configuration": ("configuration_id", "configuration_sha256"),
            "code": ("code_id", "code_tree_sha256"),
            "environment": ("environment_id", "environment_sha256"),
        }
        for component, (id_field, hash_field) in expected_snapshots.items():
            expected_id = fingerprint_inputs[component]["record_id"]
            expected_hash = fingerprint_inputs[component][hash_field]
            snapshot = manifest.get(component, {})
            if expected_id is not None and snapshot.get(id_field) != expected_id:
                raise FingerprintInputsError(f"manifest.{component}.{id_field} does not match FingerprintInputs")
            if snapshot.get(hash_field) != expected_hash:
                raise FingerprintInputsError(f"manifest.{component}.{hash_field} does not match FingerprintInputs")
        if manifest.get("fingerprints") != bundle:
            raise FingerprintInputsError("manifest.fingerprints does not match the recomputed FingerprintBundle")
    return bundle
