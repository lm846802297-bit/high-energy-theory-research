import sys, json, tempfile, unittest, hashlib, importlib.util
from pathlib import Path
HERE=Path(__file__).resolve()
TOOLS=HERE.parents[2]/"tools"
def load(name):
    spec=importlib.util.spec_from_file_location(name,TOOLS/(name+".py"))
    mod=importlib.util.module_from_spec(spec); sys.modules[name]=mod; spec.loader.exec_module(mod); return mod
cross=load("cross_record_validate")
mig=load("migrate_v1_3_to_v1_4")
dm=load("directory_manifest")

def base_art(**kw):
    x={"record_type":"artifact","artifact_id":"ART-1","project_id":"P-1","artifact_storage_kind":"file",
       "origin_kind":"ingested_external","content_sha256":None,"hash_unavailable_reason":"source does not expose bytes",
       "artifact_integrity_status":"needs_review","directory_manifest":[],"directory_manifest_sha256":None,
       "alternative_identity":None}
    x.update(kw); return x

def contract(**kw):
    x={"record_type":"task_execution_contract","contract_id":"TEC-1","project_id":"P-1","contract_status":"approved",
       "contract_version":1,"contract_sha256":"a"*64,"alternative_identity_methods":[
        {"method_id":"AIM-PUBLISHER-V1","method_version":1,"method_kind":"immutable_versioned_locator","method_status":"approved","description":"resolve immutable publisher version","applicable_source_types":["publisher"],"applicable_artifact_storage_kinds":["file"],"identity_value_specification":"publisher version URL","verification_procedure":"resolve and compare version","required_evidence_kinds":["publisher_record"],"acceptance_criteria":["version id matches"],"limitations":["does not prove local byte equality"]}]}
    x.update(kw); return x

class CrossRecordTests(unittest.TestCase):
    def test_01_file_without_hash_needs_review_allowed(self):
        self.assertEqual(cross.validate_records([base_art()])["errors"],[])
    def test_02_file_without_hash_passed_rejected(self):
        r=cross.validate_records([base_art(artifact_integrity_status="passed")])
        self.assertIn("MISSING_BYTES_HASH_MARKED_PASSED",[e["code"] for e in r["errors"]])
    def test_03_file_without_reason_rejected(self):
        r=cross.validate_records([base_art(hash_unavailable_reason=None)])
        self.assertIn("HASH_UNAVAILABLE_REASON_REQUIRED",[e["code"] for e in r["errors"]])
    def test_04_directory_with_manifest_hash_allowed(self):
        e={"relative_path":"a.txt","entry_type":"file","size_bytes":1,"content_sha256":"b"*64,"symlink_target":None}
        a=base_art(artifact_storage_kind="directory",content_sha256=None,directory_manifest=[e],directory_manifest_sha256="c"*64,
                   hash_unavailable_reason=None,artifact_integrity_status="passed")
        self.assertEqual(cross.validate_records([a])["errors"],[])
    def test_05_directory_missing_hash_rejected(self):
        a=base_art(artifact_storage_kind="directory",directory_manifest=[],directory_manifest_sha256=None,hash_unavailable_reason=None)
        self.assertIn("DIRECTORY_MANIFEST_HASH_REQUIRED",[e["code"] for e in cross.validate_records([a])["errors"]])
    def test_06_alt_identity_requires_contract(self):
        ai={"approved_contract_id":"TEC-MISSING","approved_contract_sha256":"a"*64,"method_id":"AIM-PUBLISHER-V1","method_version":1,
            "identity_value":"https://publisher.example/version/1","evidence_artifact_ids":["E-1"],"verification_status":"verified","verified_at":"2026-01-01T00:00:00Z","verified_by":"reviewer",
            "scope_statement":"version identity only","limitations":["does not prove byte equality"]}
        r=cross.validate_records([base_art(alternative_identity=ai)])
        self.assertIn("ALT_ID_CONTRACT_MISSING",[e["code"] for e in r["errors"]])
    def test_07_alt_identity_valid_but_still_needs_review(self):
        ai={"approved_contract_id":"TEC-1","approved_contract_sha256":"a"*64,"method_id":"AIM-PUBLISHER-V1","method_version":1,
            "identity_value":"https://publisher.example/version/1","evidence_artifact_ids":["ART-EVID-1"],"verification_status":"verified","verified_at":"2026-01-01T00:00:00Z","verified_by":"reviewer",
            "scope_statement":"version identity only","limitations":["does not prove byte equality"]}
        evidence=base_art(artifact_id="ART-EVID-1",content_sha256="b"*64,hash_unavailable_reason=None,artifact_integrity_status="passed")
        r=cross.validate_records([contract(),evidence,base_art(alternative_identity=ai)])
        self.assertEqual(r["errors"],[])
    def test_08_alt_identity_cannot_promote_byte_integrity(self):
        ai={"approved_contract_id":"TEC-1","approved_contract_sha256":"a"*64,"method_id":"AIM-PUBLISHER-V1","method_version":1,
            "identity_value":"https://publisher.example/version/1","evidence_artifact_ids":["ART-EVID-1"],"verification_status":"verified","verified_at":"2026-01-01T00:00:00Z","verified_by":"reviewer",
            "scope_statement":"version identity only","limitations":["does not prove byte equality"]}
        r=cross.validate_records([contract(),base_art(alternative_identity=ai,artifact_integrity_status="passed")])
        self.assertTrue(set(["MISSING_BYTES_HASH_MARKED_PASSED","ALT_ID_CANNOT_PROMOTE_BYTE_INTEGRITY"]) & {e["code"] for e in r["errors"]})
    def test_09_missing_reference_rejected(self):
        r=cross.validate_records([{"record_type":"task","task_id":"T-1","project_id":"P-1","active_contract_id":"TEC-X"}])
        self.assertIn("REF_TARGET_MISSING",[e["code"] for e in r["errors"]])
    def test_10_project_mismatch_rejected(self):
        a={"record_type":"task","task_id":"T-1","project_id":"P-1","active_contract_id":"TEC-1"}
        c=contract(project_id="P-2")
        r=cross.validate_records([a,c])
        self.assertIn("REF_PROJECT_MISMATCH",[e["code"] for e in r["errors"]])
    def test_11_duplicate_ids_rejected(self):
        r=cross.validate_records([{"record_type":"source","source_id":"S-1","project_id":"P-1"},
                                  {"record_type":"source","source_id":"S-1","project_id":"P-1"}])
        self.assertIn("DUPLICATE_ID",[e["code"] for e in r["errors"]])
    def test_12_event_sequence_gap_rejected(self):
        events=[{"record_type":"state_transition_event","event_id":"EV-1","ledger_id":"L-1","sequence_number":1,"previous_event_sha256":None,"event_sha256":"a"*64},
                {"record_type":"state_transition_event","event_id":"EV-3","ledger_id":"L-1","sequence_number":3,"previous_event_sha256":"a"*64,"event_sha256":"c"*64}]
        self.assertIn("EVENT_SEQUENCE_GAP",[e["code"] for e in cross.validate_records(events)["errors"]])
    def test_13_support_cycle_rejected(self):
        c1={"record_type":"claim","claim_id":"C-1","project_id":"P-1"}
        c2={"record_type":"claim","claim_id":"C-2","project_id":"P-1"}
        e1={"record_type":"relation_edge","edge_id":"E-1","project_id":"P-1","from_id":"C-1","from_record_type":"claim","to_id":"C-2","to_record_type":"claim","relation":"supports"}
        e2={"record_type":"relation_edge","edge_id":"E-2","project_id":"P-1","from_id":"C-2","from_record_type":"claim","to_id":"C-1","to_record_type":"claim","relation":"supports"}
        self.assertIn("SUPPORT_CYCLE",[e["code"] for e in cross.validate_records([c1,c2,e1,e2])["errors"]])

class ManifestTests(unittest.TestCase):
    def file_entry(self,path,digest="a"*64,size=1):
        return {"relative_path":path,"entry_type":"file","size_bytes":size,"content_sha256":digest,"symlink_target":None}
    def test_14_order_independent_manifest_hash(self):
        a=[self.file_entry("b.txt"),self.file_entry("a.txt")]
        b=list(reversed(a))
        self.assertEqual(dm.directory_manifest_sha256(a),dm.directory_manifest_sha256(b))
    def test_15_nfc_path_collision_rejected(self):
        a=[self.file_entry("é.txt"),self.file_entry("e\u0301.txt")]
        with self.assertRaises(dm.ManifestError): dm.directory_manifest_sha256(a)
    def test_16_path_traversal_rejected(self):
        with self.assertRaises(dm.ManifestError): dm.directory_manifest_sha256([self.file_entry("../escape")])
    def test_17_symlink_rejected_by_default(self):
        e={"relative_path":"link","entry_type":"symlink","size_bytes":None,"content_sha256":None,"symlink_target":"target"}
        with self.assertRaises(dm.ManifestError): dm.directory_manifest_sha256([e])
    def test_18_canonical_bytes_no_newline(self):
        b=dm.canonical_manifest_bytes([self.file_entry("a.txt")])
        self.assertFalse(b.endswith(b"\n"))
        self.assertEqual(hashlib.sha256(b).hexdigest(),dm.directory_manifest_sha256([self.file_entry("a.txt")]))

class MigrationTests(unittest.TestCase):
    def test_19_explicit_alias_mapped(self):
        rec={"schema_version":"1.3","record_type":"claim","claim_id":"C-1","project_id":"P-1","planned_run_ids":["RPL-1"]}
        out,ch,un,w=mig.migrate_record(rec)
        self.assertEqual(out["run_plan_ids"],["RPL-1"]); self.assertNotIn("planned_run_ids",out)
        self.assertEqual(un,[])
    def test_20_missing_validation_target_remains_unresolved(self):
        rec={"schema_version":"1.3","record_type":"claim","claim_id":"C-1","project_id":"P-1","validation_ids":["V-1"]}
        out,ch,un,w=mig.migrate_record(rec)
        self.assertIn("VALIDATION_TARGET_NOT_FOUND",[x["code"] for x in un])
        self.assertNotIn("validation_ids",out)
        self.assertNotIn("validation_activity_ids",out)
        self.assertNotIn("validation_plan_ids",out)
    def test_21_unknown_fields_quarantined_not_silent(self):
        rec={"schema_version":"1.3","record_type":"source","source_id":"S-1","project_id":"P-1","mystery_field":5}
        out,ch,un,w=mig.migrate_record(rec,target_properties={"schema_version":{},"record_type":{},"project_id":{},"source_id":{}})
        self.assertNotIn("mystery_field",out)
        self.assertIn("UNKNOWN_FIELDS_QUARANTINED",[x["code"] for x in w])
    def test_22_migration_is_deterministic(self):
        rec={"schema_version":"1.3","record_type":"claim","claim_id":"C-1","project_id":"P-1","planned_run_ids":["RPL-1"]}
        a=mig.migrate_record(rec)[0]; b=mig.migrate_record(rec)[0]
        self.assertEqual(json.dumps(a,sort_keys=True),json.dumps(b,sort_keys=True))
    def test_23_unknown_record_type_rejected(self):
        out,ch,un,w=mig.migrate_record({"schema_version":"1.3","record_type":"made_up","id":"X"})
        self.assertIsNone(out); self.assertIn("UNKNOWN_RECORD_TYPE",[x["code"] for x in un])
    def test_24_wrong_source_version_unresolved(self):
        out,ch,un,w=mig.migrate_record({"schema_version":"1.2","record_type":"claim","claim_id":"C-1","project_id":"P-1"})
        self.assertIn("UNSUPPORTED_SOURCE_VERSION",[x["code"] for x in un])

    def test_25_method_source_type_mismatch_rejected(self):
        src={"record_type":"source","source_id":"SRC-1","project_id":"P-1","source_type":"arxiv"}
        ai={"approved_contract_id":"TEC-1","approved_contract_sha256":"a"*64,"method_id":"AIM-PUBLISHER-V1","method_version":1,
            "identity_value":"https://publisher.example/version/1","evidence_artifact_ids":["ART-EVID-1"],"verification_status":"verified",
            "verified_at":"2026-01-01T00:00:00Z","verified_by":"reviewer","scope_statement":"version identity only","limitations":["no byte proof"]}
        art=base_art(artifact_id="ART-1",acquired_from_source_id="SRC-1",alternative_identity=ai)
        evid=base_art(artifact_id="ART-EVID-1",content_sha256="b"*64,hash_unavailable_reason=None,artifact_integrity_status="passed")
        r=cross.validate_records([contract(),src,evid,art])
        self.assertIn("ALT_ID_SOURCE_TYPE_NOT_APPLICABLE",[e["code"] for e in r["errors"]])
    def test_26_illegal_integrity_transition_rejected(self):
        e={"record_type":"state_transition_event","event_id":"EV-1","ledger_id":"L-1","sequence_number":1,
           "previous_event_sha256":None,"event_sha256":"a"*64,"field_name":"artifact_integrity_status",
           "from_status":"needs_review","to_status":"in_progress"}
        r=cross.validate_records([e])
        self.assertIn("ILLEGAL_ARTIFACT_INTEGRITY_TRANSITION",[x["code"] for x in r["errors"]])
    def test_27_task_active_contract_must_match_task(self):
        task={"record_type":"task","task_id":"TASK-1","project_id":"P-1","active_contract_id":"TEC-1"}
        c=contract(task_id="TASK-OTHER")
        r=cross.validate_records([task,c])
        self.assertIn("TASK_CONTRACT_TASK_MISMATCH",[e["code"] for e in r["errors"]])

    def test_28_polymorphic_subject_missing_rejected(self):
        rec={"record_type":"validation_report","validation_report_id":"VR-1","project_id":"P-1","subject_ids":["NO-SUCH-ID"]}
        r=cross.validate_records([rec])
        self.assertIn("REF_TARGET_MISSING",[e["code"] for e in r["errors"]])
    def test_29_event_record_reference_checked(self):
        e={"record_type":"state_transition_event","event_id":"EV-1","ledger_id":"L-1","sequence_number":1,
           "previous_event_sha256":None,"event_sha256":"a"*64,"subject_id":"NO-RECORD"}
        r=cross.validate_records([e])
        self.assertIn("REF_TARGET_MISSING",[x["code"] for x in r["errors"]])

if __name__=="__main__": unittest.main(verbosity=2)
