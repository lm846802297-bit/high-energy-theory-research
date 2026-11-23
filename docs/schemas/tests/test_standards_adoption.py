import json, subprocess, sys, tempfile, unittest
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
ROOT=Path(__file__).resolve().parents[1]
SCHEMA=ROOT/"standards-adoption-v1.0.0.schema.json"
VALIDATOR=ROOT/"validate_standards_adoption.py"
class StandardsAdoptionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.schema=json.loads(SCHEMA.read_text(encoding="utf-8")); Draft202012Validator.check_schema(cls.schema)
  cls.validator=Draft202012Validator(cls.schema,format_checker=FormatChecker())
 def lock(self):
  return {"record_type":"standards_lock","lock_version":1,"central_repository":"lm846802297-bit/high-energy-theory-research","standards_release":None,"source_commit":"a"*40,"adopted_at":"2026-11-23","adoption_pr":"https://github.com/example/project/pull/1","adopted_profiles":["task-handoff","rcrps-v1.0.1"],"local_extensions":[],"deviations":[]}
 def test_valid_lock(self): self.assertTrue(self.validator.is_valid(self.lock()))
 def test_short_commit_rejected(self):
  r=self.lock(); r["source_commit"]="deadbeef"; self.assertFalse(self.validator.is_valid(r))
 def test_unknown_profile_rejected(self):
  r=self.lock(); r["adopted_profiles"]=["invented-profile"]; self.assertFalse(self.validator.is_valid(r))
 def test_duplicate_profiles_rejected(self):
  r=self.lock(); r["adopted_profiles"]=["task-handoff","task-handoff"]; self.assertFalse(self.validator.is_valid(r))
 def test_task_requires_both_fingerprints(self):
  r={"record_type":"task_provenance","provenance_version":"1.0.0","task_id":"20261123-test-task","repository":"example/project","task_brief_path":"research/tasks/brief.md","task_brief_sha256":"b"*64,"central_repository":"lm846802297-bit/high-energy-theory-research","central_commit_sha":"a"*40,"lock_file_path":"research/standards-lock.yaml","lock_file_sha256":"c"*64,"applied_profiles":["task-handoff"],"project_extensions":[],"acceptance_criteria":["schema validation passes"]}
  self.assertTrue(self.validator.is_valid(r)); del r["lock_file_sha256"]; self.assertFalse(self.validator.is_valid(r))
 def test_report_record_shape(self):
  r={"record_type":"standards_validation_report","report_version":"1.0.0","task_id":"20261123-test-task","repository":"example/project","source_commit":"a"*40,"central_commit_sha":"b"*40,"status":"COMPLIANT","checks":[{"check_id":"lock-schema","status":"PASS","evidence":["validation.log"]}]}
  self.assertTrue(self.validator.is_valid(r))
 def test_yaml_date_remains_a_string(self):
  import importlib.util
  spec=importlib.util.spec_from_file_location("standards_validator",VALIDATOR)
  module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/"lock.yaml"
   path.write_text("adopted_at: 2026-11-23\n",encoding="utf-8")
   self.assertEqual(module.load_record(path)["adopted_at"],"2026-11-23")
 def test_cli_rejects_malformed_lock(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp); lock=root/"standards-lock.yaml"; lock.write_text("record_type: standards_lock\n",encoding="utf-8")
   run=subprocess.run([sys.executable,str(VALIDATOR),"--repo-root",str(root),"--lock",str(lock)],capture_output=True,text=True)
   self.assertNotEqual(run.returncode,0); self.assertIn("NON_COMPLIANT",run.stdout)
 def test_cli_rejects_report_status_without_passing_evidence(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp); (root/"docs").mkdir(); (root/"docs/RESEARCH_TASK_HANDOFF_STANDARD.md").write_text("test",encoding="utf-8")
   lock=root/"standards-lock.json"; record=self.lock(); record["adopted_profiles"]=["task-handoff"]; lock.write_text(json.dumps(record),encoding="utf-8")
   report=root/"report.json"; report.write_text(json.dumps({"record_type":"standards_validation_report","report_version":"1.0.0","task_id":"20261123-test-task","repository":"example/project","source_commit":"a"*40,"central_commit_sha":"a"*40,"status":"COMPLIANT","checks":[{"check_id":"profile","status":"BLOCKED","evidence":[]}]}),encoding="utf-8")
   run=subprocess.run([sys.executable,str(VALIDATOR),"--repo-root",str(root),"--lock",str(lock),"--report",str(report)],capture_output=True,text=True)
   self.assertNotEqual(run.returncode,0); self.assertIn("status inconsistent",run.stdout)
if __name__=="__main__": unittest.main()
