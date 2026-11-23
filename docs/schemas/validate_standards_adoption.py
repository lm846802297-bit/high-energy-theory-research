#!/usr/bin/env python3
"""Validate standards locks, task provenance, and standards compliance reports."""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA = Path(__file__).with_name("standards-adoption-v1.0.0.schema.json")
PROFILE_PATHS = {
 "core-governance":"docs/RESEARCH_GOVERNANCE_STANDARD.md",
 "research-compute":"RESEARCH_COMPUTE_POLICY.md",
 "task-handoff":"docs/RESEARCH_TASK_HANDOFF_STANDARD.md",
 "scientific-diff":"docs/scientific-diff-workflow.md",
 "research-quality-gate":"docs/governance/RESEARCH_QUALITY_GATE.md",
 "calculation-result-archive":"docs/CALCULATION_RESULT_ARCHIVAL_POLICY.md",
 "rcrps-v1.0.1":"docs/STRUCTURED_RESULT_DATA_STANDARD_v1.0.1.md",
 "git-review-and-merge":"docs/governance/GIT_MERGE_POLICY.md",
 "document-review":"docs/DOCUMENT_REVIEW_STANDARD.md",
 "referee-response-and-manuscript-synchronization":"docs/REFEREE_RESPONSE_AND_MANUSCRIPT_SYNCHRONIZATION_STANDARD.md",
 "generated-figure-and-report":"docs/governance/GENERATED_FIGURE_AND_REPORT_POLICY.md",
}
def sha256(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
 return h.hexdigest()
def resolve(root, value):
 p=Path(value)
 if p.is_absolute() or ".." in p.parts: raise ValueError(f"unsafe repository-relative path: {value}")
 target=(root/p).resolve(); target.relative_to(root.resolve()); return target
def load_record(path):
 raw=path.read_text(encoding="utf-8")
 return yaml.safe_load(raw) if path.suffix.lower() in {".yaml",".yml"} else json.loads(raw)
def validate(path, validator):
 try: data=load_record(path)
 except Exception as exc: return None,[f"{path}: parse error: {exc}"]
 errs=sorted(validator.iter_errors(data),key=lambda e:(list(map(str,e.absolute_path)),e.message))
 return data,[f"{path}: /{'/'.join(map(str,e.absolute_path))}: {e.message}" for e in errs]
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--repo-root",type=Path,default=Path.cwd())
 p.add_argument("--lock",type=Path,required=True)
 p.add_argument("--task-provenance",type=Path)
 p.add_argument("--report",type=Path)
 p.add_argument("--require-central-commit",action="store_true",help="require the pinned commit to exist in this checkout's Git object database")
 a=p.parse_args(); root=a.repo_root.resolve()
 schema=json.loads(SCHEMA.read_text(encoding="utf-8")); Draft202012Validator.check_schema(schema)
 validator=Draft202012Validator(schema,format_checker=FormatChecker()); errors=[]
 lock,errs=validate(a.lock,validator); errors.extend(errs)
 if lock and not errs:
  for profile in lock["adopted_profiles"]:
   path=resolve(root,PROFILE_PATHS[profile])
   if not path.is_file(): errors.append(f"profile {profile}: central policy file missing: {PROFILE_PATHS[profile]}")
  for ext in lock["local_extensions"]:
   path=resolve(root,ext["path"])
   if not path.is_file(): errors.append(f"local extension missing: {ext['path']}")
   elif ext.get("sha256") and sha256(path)!=ext["sha256"]: errors.append(f"local extension SHA-256 mismatch: {ext['path']}")
  if a.require_central_commit:
   check=subprocess.run(["git","cat-file","-e",lock["source_commit"]+"^{commit}"],cwd=root,capture_output=True)
   if check.returncode: errors.append(f"central source_commit not found in local Git object database: {lock['source_commit']}")
 if a.task_provenance:
  task,errs=validate(a.task_provenance,validator); errors.extend(errs)
  if task and not errs:
   lp=resolve(root,task["lock_file_path"]); bp=resolve(root,task["task_brief_path"])
   if not lp.is_file() or sha256(lp)!=task["lock_file_sha256"]: errors.append("task provenance lock file missing or SHA-256 mismatch")
   if not bp.is_file() or sha256(bp)!=task["task_brief_sha256"]: errors.append("task brief missing or SHA-256 mismatch")
   if lock and task["central_commit_sha"]!=lock["source_commit"]: errors.append("task central commit differs from locked central commit")
   if lock and not set(task["applied_profiles"]).issubset(set(lock["adopted_profiles"])): errors.append("task applies a profile not adopted by the lock")
 if a.report:
  report,errs=validate(a.report,validator); errors.extend(errs)
  if report and not errs:
   states={c["status"] for c in report["checks"]}
   expected="COMPLIANT" if states <= {"PASS","NOT_APPLICABLE"} and "PASS" in states else ("NON_COMPLIANT" if "FAIL" in states else "INCOMPLETE")
   if report["status"]!=expected: errors.append(f"report status inconsistent with checks; expected {expected}")
 if errors:
  print("NON_COMPLIANT")
  for e in errors: print("- "+e)
  return 1
 print("COMPLIANT: schemas, profile references, extension references, and supplied provenance checks passed")
 return 0
if __name__=="__main__": raise SystemExit(main())
