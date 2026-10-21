from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
VECTOR_PATH = ROOT / "tests" / "fixtures" / "fingerprint-inputs-v1" / "golden-vector.json"
MODULE_PATH = ROOT / "skills" / "high-energy-theory-research" / "scripts" / "fingerprint_inputs.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("fingerprint_inputs_test_module", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


FP = _load_module()


class FingerprintInputsContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vector = json.loads(VECTOR_PATH.read_text(encoding="utf-8"))

    def test_golden_vector_matches_canonical_bytes_and_hashes(self):
        vector = self.vector
        inputs = vector["fingerprint_inputs"]
        execution_spec = vector["execution_spec"]
        normalized_sources = sorted(inputs["source_inputs"], key=lambda item: item["source_id"])
        normalized_artifacts = sorted(inputs["input_artifacts"], key=lambda item: item["artifact_id"])
        input_set_payload = {
            "contract_version": inputs["contract_version"],
            "canonicalization": inputs["canonicalization"],
            "source_inputs": normalized_sources,
            "input_artifacts": normalized_artifacts,
        }
        bundle = FP.compute_fingerprint_bundle(inputs, execution_spec)
        self.assertEqual(FP.canonical_json_bytes(execution_spec).decode("utf-8"), vector["canonical"]["execution_spec"])
        self.assertEqual(FP.canonical_json_bytes(input_set_payload).decode("utf-8"), vector["canonical"]["input_set"])
        self.assertEqual(FP.canonical_json_bytes(normalized_artifacts).decode("utf-8"), vector["canonical"]["dependency_artifacts"])
        self.assertEqual(FP.canonical_json_bytes({key: value for key, value in bundle.items() if key != "composite_sha256"}).decode("utf-8"), vector["canonical"]["composite_payload"])
        for key, expected in vector["expected"].items():
            self.assertEqual(bundle[key], expected, key)

    def test_source_and_artifact_order_does_not_change_fingerprint(self):
        vector = self.vector
        inputs = deepcopy(vector["fingerprint_inputs"])
        original = FP.compute_fingerprint_bundle(inputs, vector["execution_spec"])
        inputs["source_inputs"].reverse()
        inputs["input_artifacts"].reverse()
        reordered = FP.compute_fingerprint_bundle(inputs, vector["execution_spec"])
        self.assertEqual(original, reordered)

    def test_duplicate_source_id_is_rejected_even_with_different_digest(self):
        vector = self.vector
        inputs = deepcopy(vector["fingerprint_inputs"])
        inputs["source_inputs"].append({"source_id": "SRC-001", "content_sha256": "c" * 64})
        with self.assertRaises(FP.FingerprintInputsError):
            FP.compute_fingerprint_bundle(inputs, vector["execution_spec"])

    def test_duplicate_artifact_id_is_rejected_even_with_different_digest(self):
        vector = self.vector
        inputs = deepcopy(vector["fingerprint_inputs"])
        inputs["input_artifacts"].append({"artifact_id": "ART-001", "digest_kind": "content_sha256", "digest_sha256": "a" * 64})
        with self.assertRaises(FP.FingerprintInputsError):
            FP.compute_fingerprint_bundle(inputs, vector["execution_spec"])

    def test_execution_spec_tampering_is_detected(self):
        vector = self.vector
        spec = deepcopy(vector["execution_spec"])
        spec["random_seed"] = 1
        with self.assertRaises(FP.FingerprintInputsError):
            FP.compute_fingerprint_bundle(vector["fingerprint_inputs"], spec)

    def test_non_applicable_component_requires_reason_and_no_digest(self):
        vector = self.vector
        inputs = deepcopy(vector["fingerprint_inputs"])
        inputs["code"] = {"record_id": None, "code_tree_sha256": None, "not_applicable_reason": None}
        with self.assertRaises(FP.FingerprintInputsError):
            FP.compute_fingerprint_bundle(inputs, vector["execution_spec"])

    def test_run_plan_link_mismatch_is_rejected(self):
        vector = self.vector
        inputs = deepcopy(vector["fingerprint_inputs"])
        run_plan = {
            "execution_spec": vector["execution_spec"],
            "execution_spec_sha256": inputs["execution_spec_sha256"],
            "fingerprint_inputs": inputs,
            "configuration_id": "CONF-OTHER",
            "code_id": "CODE-001",
            "environment_id": "ENV-001",
            "input_artifact_ids": ["ART-001", "ART-002"],
        }
        with self.assertRaises(FP.FingerprintInputsError):
            FP.validate_run_plan_fingerprint_inputs(run_plan)


if __name__ == "__main__":
    unittest.main()
