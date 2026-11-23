import hashlib, json, subprocess, sys, tempfile, unittest
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from rcrps_v1_0_1_fixtures import minimal_manifest
ROOT=Path(__file__).resolve().parents[1]
SCHEMA=ROOT/"standards-adoption-v1.0.0.schema.json"
VALIDATOR=ROOT/"validate_standards_adoption.py"
class StandardsAdoptionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.schema=json.loads(SCHEMA.read_text(encoding="utf-8")); Draft202012Validator.check_schema(cls.schema)
  cls.validator=Draft202012Validator(cls.schema,format_checker=FormatChecker())
 def lock(self):
  return {"lock_version":1,"central_repository":"lm846802297-bit/high-energy-theory-research","standards_release":None,"source_commit":"a"*40,"adopted_at":"2026-11-23","adoption_pr":"https://github.com/example/project/pull/1","adopted_profiles":["task-handoff","rcrps-v1.0.1"],"local_extensions":[],"deviations":[]}
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
   path=Path(tmp)/"lock.yaml"; path.write_text("adopted_at: 2026-11-23\n",encoding="utf-8")
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
 def test_cli_binds_provenance_to_the_selected_lock(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp); (root/"docs").mkdir(); (root/"research").mkdir()
   (root/"docs/RESEARCH_TASK_HANDOFF_STANDARD.md").write_text("test",encoding="utf-8")
   lock_path="research/standards-lock.json"
   other_path="research/another-standards-lock.json"
   lock={**self.lock(),"adopted_profiles":["task-handoff"]}
   alternate={**lock,"adoption_pr":"https://github.com/example/project/pull/2"}
   self.assertTrue(self.validator.is_valid(lock))
   self.assertTrue(self.validator.is_valid(alternate))
   (root/lock_path).write_text(json.dumps(lock),encoding="utf-8")
   (root/other_path).write_text(json.dumps(alternate),encoding="utf-8")
   (root/"brief.md").write_text("task brief",encoding="utf-8")

   def digest(path):
    return hashlib.sha256((root/path).read_bytes()).hexdigest()

   def check(record_type, claimed, expected):
    provenance={
     "central_repository":lock["central_repository"],"central_commit_sha":lock["source_commit"],
     "lock_file_path":claimed,"lock_file_sha256":digest(claimed),"task_id":"20261123-test-task",
     "task_brief_path":"brief.md","task_brief_sha256":digest("brief.md"),
     "applied_profiles":["task-handoff"],"project_extensions":[],
    }
    if record_type=="task provenance":
     record={**provenance,"record_type":"task_provenance","provenance_version":"1.0.0",
             "repository":"example/project","acceptance_criteria":["validate"]}
     flag="--task-provenance"
    else:
     record=minimal_manifest()
     record["extensions"]={"standards_provenance":provenance}
     flag="--run-manifest"
    (root/"record.json").write_text(json.dumps(record),encoding="utf-8")
    run=subprocess.run([sys.executable,str(VALIDATOR),"--repo-root",str(root),"--lock",lock_path,
                        flag,"record.json"],capture_output=True,text=True)
    self.assertEqual(run.returncode,expected,run.stdout+run.stderr)
    if expected:
     self.assertIn(record_type+" lock file: does not match --lock",run.stdout)
     self.assertNotIn("SHA-256 mismatch",run.stdout)

   for record_type in ("task provenance","run manifest"):
    for claimed,expected in ((lock_path,0),("./research/./standards-lock.json",0),(other_path,1)):
     with self.subTest(record_type=record_type,claimed=claimed):
      check(record_type,claimed,expected)
 def test_cli_pairs_provenance_and_report_by_task_and_repository(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp); (root/"docs").mkdir()
   (root/"docs/RESEARCH_TASK_HANDOFF_STANDARD.md").write_text("test",encoding="utf-8")
   lock={**self.lock(),"adopted_profiles":["task-handoff"]}
   def write(name, data):
    (root/name).write_text(json.dumps(data),encoding="utf-8")
   def digest(name):
    return hashlib.sha256((root/name).read_bytes()).hexdigest()
   write("lock.json",lock)
   (root/"brief.md").write_text("task brief",encoding="utf-8")
   task={
    "record_type":"task_provenance","provenance_version":"1.0.0",
    "task_id":"20261123-test-task","repository":"example/project",
    "central_repository":lock["central_repository"],"central_commit_sha":lock["source_commit"],
    "lock_file_path":"lock.json","lock_file_sha256":digest("lock.json"),
    "task_brief_path":"brief.md","task_brief_sha256":digest("brief.md"),
    "applied_profiles":["task-handoff"],"project_extensions":[],"acceptance_criteria":["validate"],
   }
   report={
    "record_type":"standards_validation_report","report_version":"1.0.0",
    "task_id":task["task_id"],"repository":"Example/Project",
    "source_commit":"b"*40,"central_commit_sha":lock["source_commit"],"status":"COMPLIANT",
    "checks":[{"check_id":"evidence","status":"PASS","evidence":["brief.md"]}],
   }
   write("task.json",task)
   task_args=["--task-provenance","task.json"]
   report_args=["--report","report.json"]
   def invoke(args, expected, message=""):
    run=subprocess.run([sys.executable,str(VALIDATOR),"--repo-root",str(root),
                        "--lock","lock.json",*args],capture_output=True,text=True)
    self.assertEqual(run.returncode,expected,run.stdout+run.stderr)
    if message:
     self.assertIn(message,run.stdout)
   invoke(task_args,0)
   write("report.json",report)
   invoke(task_args+report_args,0)
   for field, value in (("task_id","20261123-other-task"),("repository","example/other-project")):
    with self.subTest(field=field):
     write("report.json",{**report,field:value})
     invoke(report_args,0)
     invoke(task_args+report_args,1,f"report {field} differs from task provenance")
 def make_central_repo(self, central):
  (central/"docs").mkdir(parents=True); (central/"docs/RESEARCH_TASK_HANDOFF_STANDARD.md").write_text("central policy",encoding="utf-8")
  subprocess.run(["git","init","-q"],cwd=central,check=True)
  subprocess.run(["git","config","user.email","test@example.org"],cwd=central,check=True)
  subprocess.run(["git","config","user.name","Test"],cwd=central,check=True)
  subprocess.run(["git","add","."],cwd=central,check=True)
  subprocess.run(["git","commit","-qm","fixture"],cwd=central,check=True)
  return subprocess.run(["git","rev-parse","HEAD"],cwd=central,capture_output=True,text=True,check=True).stdout.strip()
 def test_cli_checks_profile_in_exact_central_checkout(self):
  with tempfile.TemporaryDirectory() as tmp:
   base=Path(tmp); project=base/"project"; central=base/"central"; project.mkdir(); central.mkdir()
   sha=self.make_central_repo(central); record=self.lock(); record["source_commit"]=sha; record["adopted_profiles"]=["task-handoff"]
   lock=project/"standards-lock.json"; lock.write_text(json.dumps(record),encoding="utf-8")
   run=subprocess.run([sys.executable,str(VALIDATOR),"--repo-root",str(project),"--central-root",str(central),"--require-central-commit","--lock",str(lock)],capture_output=True,text=True)
   self.assertEqual(run.returncode,0,run.stdout+run.stderr)
 def test_cli_rejects_central_checkout_at_wrong_commit(self):
  with tempfile.TemporaryDirectory() as tmp:
   base=Path(tmp); project=base/"project"; central=base/"central"; project.mkdir(); central.mkdir()
   self.make_central_repo(central); record=self.lock(); record["adopted_profiles"]=["task-handoff"]
   lock=project/"standards-lock.json"; lock.write_text(json.dumps(record),encoding="utf-8")
   run=subprocess.run([sys.executable,str(VALIDATOR),"--repo-root",str(project),"--central-root",str(central),"--lock",str(lock)],capture_output=True,text=True)
   self.assertNotEqual(run.returncode,0); self.assertIn("central-root HEAD",run.stdout)
if __name__=="__main__": unittest.main()
