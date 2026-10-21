#!/usr/bin/env python3
"""Candidate cross-record validator for schema-v1.4.3.7.
Validates declared references and a bounded set of semantic invariants.
Does NOT claim full state-machine, filesystem/JCS, or scientific validation.
"""
import argparse, json, hashlib, sys, re
from pathlib import Path
from collections import defaultdict
from jsonschema import Draft202012Validator, FormatChecker

PRIMARY = {
"task":"task_id","task_execution_contract":"contract_id","run_plan":"run_plan_id","run":"run_id",
"run_manifest":"manifest_id","artifact_plan":"artifact_plan_id","artifact":"artifact_id",
"validation_plan":"validation_plan_id","validation_activity":"validation_activity_id",
"validation_report":"validation_report_id","claim":"claim_id","source":"source_id",
"source_fragment":"source_fragment_id","configuration":"configuration_id","code":"code_id",
"environment":"environment_id","convention_set":"conventions_id","parameter_point":"point_id",
"benchmark_result":"benchmark_result_id","evidence_fragment":"evidence_id","test_case":"test_case_id",
"test_run":"test_run_id","state_transition_event":"event_id","migration_record":"migration_record_id",
"relation_edge":"edge_id"
}
# Explicit non-polymorphic reference contracts. Polymorphic refs are checked separately.
REFS = {
("task","active_contract_id"):"task_execution_contract",("task","dependency_task_ids"):"task",
("task_execution_contract","task_id"):"task",("task_execution_contract","supersedes_contract_id"):"task_execution_contract",
("run_plan","task_id"):"task",("run_plan","contract_id"):"task_execution_contract",("run_plan","instantiated_run_id"):"run",
("run_plan","configuration_id"):"configuration",("run_plan","code_id"):"code",("run_plan","environment_id"):"environment",
("run","task_id"):"task",("run","contract_id"):"task_execution_contract",("run","run_plan_id"):"run_plan",
("run","parent_run_id"):"run",("run","retry_of_run_id"):"run",
("run_manifest","run_id"):"run",("run_manifest","task_id"):"task",("run_manifest","contract_id"):"task_execution_contract",
("run_manifest","run_plan_id"):"run_plan",("run_manifest","supersedes_manifest_id"):"run_manifest",
("artifact_plan","planned_for_task_id"):"task",("artifact_plan","planned_run_plan_id"):"run_plan",
("artifact","configuration_id"):"configuration",("artifact","code_id"):"code",("artifact","environment_id"):"environment",
("artifact","generated_by_run_id"):"run",("artifact","acquired_from_source_id"):"source",
("artifact","input_artifact_ids"):"artifact",
("validation_plan","task_id"):"task",("validation_activity","validation_plan_id"):"validation_plan",
("validation_activity","task_id"):"task",("validation_activity","environment_id"):"environment",
("validation_activity","input_artifact_ids"):"artifact",("validation_activity","validation_report_ids"):"validation_report",
("validation_report","validation_activity_id"):"validation_activity",("validation_report","evidence_ids"):"evidence_any",
("benchmark_result","evidence_ids"):"evidence_any",("parameter_point","artifact_ids"):"artifact",
("source_fragment","source_id"):"source",("configuration","conventions_id"):"convention_set",
("parameter_point","configuration_id"):"configuration",("parameter_point","source_run_id"):"run",
("test_run","test_id"):"test_case"
}
LIST_REF_FIELDS = {
("run","manifest_ids"):"run_manifest",("run","latest_manifest_id"):"run_manifest",("run","log_artifact_ids"):"artifact",
("run_plan","input_artifact_ids"):"artifact",("run_plan","artifact_plan_ids"):"artifact_plan",("run_plan","validation_plan_ids"):"validation_plan",
("task","claim_ids"):"claim",("task","completion_evidence_ids"):"evidence_any",
("artifact_plan","fulfilled_artifact_ids"):"artifact",("validation_plan","expected_artifact_plan_ids"):"artifact_plan",
("validation_plan","instantiated_validation_activity_ids"):"validation_activity",
("validation_activity","input_artifact_ids"):"artifact",("validation_activity","validation_report_ids"):"validation_report",
("validation_report","evidence_ids"):"evidence_any",("claim","source_ids"):"source",
("claim","config_ids"):"configuration",("claim","run_plan_ids"):"run_plan",("claim","run_ids"):"run",
("claim","validation_plan_ids"):"validation_plan",("claim","validation_activity_ids"):"validation_activity",
("claim","validation_report_ids"):"validation_report",("claim","artifact_plan_ids"):"artifact_plan",
("claim","artifact_ids"):"artifact",("parameter_point","artifact_ids"):"artifact",
("parameter_point","validation_report_ids"):"validation_report",("test_run","log_artifact_ids"):"artifact"
}
EVIDENCE_TYPES = {"source","source_fragment","artifact","validation_report","parameter_point","benchmark_result","evidence_fragment"}

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def load_json_records(data_dir):
    records=[]
    data_root=Path(data_dir)
    for p in sorted(data_root.rglob("*.json")):
        rel_parts=p.relative_to(data_root).parts
        if any(part in {"schemas","tests","audit","tools","reports"} for part in rel_parts):
            continue
        try:
            x=json.loads(p.read_text(encoding="utf-8"))
            if isinstance(x,dict) and "record_type" in x:
                records.append((p,x))
        except Exception:
            continue
    return records

def validate_records(records, schema_map=None, validate_schema=False):
    """records: list of dicts or (path, dict). Return machine-readable errors/warnings."""
    errors=[]; warnings=[]; indexed={}; by_type=defaultdict(list); seen={}
    norm=[]
    for i,item in enumerate(records):
        if isinstance(item,tuple): path,rec=item
        else: path,rec=Path(f"<memory:{i}>"),item
        norm.append((path,rec))
        rt=rec.get("record_type")
        if rt not in PRIMARY:
            errors.append({"code":"UNKNOWN_RECORD_TYPE","path":str(path),"record_type":rt}); continue
        keyfield=PRIMARY[rt]; key=rec.get(keyfield)
        if not isinstance(key,str) or not key:
            errors.append({"code":"MISSING_PRIMARY_KEY","path":str(path),"record_type":rt,"field":keyfield}); continue
        idx=(rt,key)
        if idx in indexed:
            errors.append({"code":"DUPLICATE_ID","path":str(path),"record_type":rt,"id":key,"first_path":str(indexed[idx][0])})
        else: indexed[idx]=(path,rec)
        by_type[rt].append((path,rec))
        if validate_schema and schema_map and rt in schema_map:
            es=list(Draft202012Validator(schema_map[rt],format_checker=FormatChecker()).iter_errors(rec))
            for e in es[:10]: errors.append({"code":"SCHEMA_INVALID","path":str(path),"record_type":rt,"json_path":"/"+"/".join(map(str,e.absolute_path)),"message":e.message})
    def check_ref(path, rec, field, target_type, value):
        if value is None: return
        if not isinstance(value,str):
            errors.append({"code":"REF_BAD_TYPE","path":str(path),"field":field,"value":value}); return
        target=indexed.get((target_type,value))
        if target is None:
            errors.append({"code":"REF_TARGET_MISSING","path":str(path),"field":field,"target_type":target_type,"target_id":value}); return
        target_rec=target[1]
        if rec.get("project_id") is not None and target_rec.get("project_id") is not None and rec.get("project_id")!=target_rec.get("project_id"):
            errors.append({"code":"REF_PROJECT_MISMATCH","path":str(path),"field":field,"target_id":value,"source_project":rec.get("project_id"),"target_project":target_rec.get("project_id")})
    def check_poly(path, rec, field, value):
        if not isinstance(value,str):
            errors.append({"code":"REF_BAD_TYPE","path":str(path),"field":field,"value":value}); return
        found=[(typ,item) for (typ,rid),item in indexed.items() if rid==value]
        if not found:
            errors.append({"code":"REF_TARGET_MISSING","path":str(path),"field":field,"target_type":"polymorphic","target_id":value}); return
        if len(found)>1:
            errors.append({"code":"REF_TARGET_AMBIGUOUS","path":str(path),"field":field,"target_id":value,"matches":[x[0] for x in found]}); return
        target=found[0][1][1]
        if rec.get("project_id") is not None and target.get("project_id") not in (None,rec.get("project_id")):
            errors.append({"code":"REF_PROJECT_MISMATCH","path":str(path),"field":field,"target_id":value})
    for path,rec in norm:
        rt=rec.get("record_type")
        for (owner,field),target_type in REFS.items():
            if rt==owner and field in rec:
                check_ref(path,rec,field,target_type,rec[field])
        for (owner,field),target_type in LIST_REF_FIELDS.items():
            if rt==owner and field in rec and isinstance(rec[field],list):
                for value in rec[field]:
                    if target_type=="evidence_any":
                        found=[(typ,indexed.get((typ,value))) for typ in EVIDENCE_TYPES if indexed.get((typ,value))]
                        if not found: errors.append({"code":"REF_TARGET_MISSING","path":str(path),"field":field,"target_type":"evidence_any","target_id":value})
                        elif any(x[1][1].get("project_id") not in (None,rec.get("project_id")) for x in found):
                            errors.append({"code":"REF_PROJECT_MISMATCH","path":str(path),"field":field,"target_id":value})
                    else: check_ref(path,rec,field,target_type,value)
        # Polymorphic subject/target references: target type is not encoded in the field.
        if rt in {"validation_plan","validation_activity","validation_report","benchmark_result"} and isinstance(rec.get("subject_ids"),list):
            for value in rec["subject_ids"]: check_poly(path,rec,"subject_ids",value)
        if rt=="evidence_fragment" and rec.get("target_record_id") is not None:
            check_poly(path,rec,"target_record_id",rec["target_record_id"])
        if rt=="state_transition_event" and rec.get("subject_id") is not None:
            check_poly(path,rec,"subject_id",rec["subject_id"])
        if rt=="state_transition_event" and rec.get("record_id") is not None:
            # Current candidate schema lacks a separate subject_record_type field.
            # Check unique ID resolution only; exact target type cannot be proven.
            check_poly(path,rec,"record_id",rec["record_id"])
            warnings.append({"code":"EVENT_SUBJECT_TYPE_NOT_EXPLICIT","path":str(path),"record_id":rec.get("record_id"),"reason":"candidate schema has no separate target record type field"})
        if rt=="run_manifest":
            nested_refs={
                "input_refs":{"source_ids":"source","configuration_ids":"configuration","input_artifact_ids":"artifact"},
                "outputs":{"artifact_plan_ids":"artifact_plan","artifact_ids":"artifact"},
                "validation":{"validation_plan_ids":"validation_plan","validation_activity_ids":"validation_activity","validation_report_ids":"validation_report"}
            }
            for parent,submap in nested_refs.items():
                obj=rec.get(parent)
                if isinstance(obj,dict):
                    for field,target_type in submap.items():
                        vals=obj.get(field,[])
                        if isinstance(vals,list):
                            for value in vals: check_ref(path,rec,f"{parent}.{field}",target_type,value)
        # Explicit polymorphic relation edge.
        if rt=="relation_edge":
            for idfield,typefield in (("from_id","from_record_type"),("to_id","to_record_type")):
                tid=rec.get(typefield); rid=rec.get(idfield)
                if tid not in PRIMARY:
                    errors.append({"code":"REF_TARGET_TYPE_UNKNOWN","path":str(path),"field":typefield,"value":tid})
                else: check_ref(path,rec,idfield,tid,rid)
            if rec.get("relation") in {"supports","contradicts"} and rec.get("from_id")==rec.get("to_id"):
                errors.append({"code":"SUPPORT_SELF_LOOP","path":str(path),"edge_id":rec.get("edge_id")})
        # Artifact file/directory and alternative identity semantics.
        if rt=="artifact":
            kind=rec.get("artifact_storage_kind"); origin=rec.get("origin_kind")
            content=rec.get("content_sha256"); dirmh=rec.get("directory_manifest_sha256")
            if kind=="file":
                if content is not None and not (isinstance(content,str) and re.fullmatch(r"[a-f0-9]{64}",content)):
                    errors.append({"code":"CONTENT_SHA256_INVALID","path":str(path)})
                if rec.get("directory_manifest") not in (None,[]) and rec.get("directory_manifest") is not None:
                    errors.append({"code":"FILE_HAS_DIRECTORY_MANIFEST","path":str(path)})
                if content is None and origin=="ingested_external" and not (isinstance(rec.get("hash_unavailable_reason"),str) and rec["hash_unavailable_reason"].strip()):
                    errors.append({"code":"HASH_UNAVAILABLE_REASON_REQUIRED","path":str(path)})
                if content is None and rec.get("artifact_integrity_status")=="passed":
                    errors.append({"code":"MISSING_BYTES_HASH_MARKED_PASSED","path":str(path)})
                if content is None and rec.get("artifact_integrity_status")!="needs_review":
                    errors.append({"code":"MISSING_BYTES_HASH_NOT_NEEDS_REVIEW","path":str(path),"status":rec.get("artifact_integrity_status")})
            elif kind=="directory":
                if content is not None: errors.append({"code":"DIRECTORY_CONTENT_SHA256_MUST_NULL","path":str(path)})
                if not (isinstance(dirmh,str) and re.fullmatch(r"[a-f0-9]{64}",dirmh)):
                    errors.append({"code":"DIRECTORY_MANIFEST_HASH_REQUIRED","path":str(path)})
                if not isinstance(rec.get("directory_manifest"),list):
                    errors.append({"code":"DIRECTORY_MANIFEST_REQUIRED","path":str(path)})
            elif kind is not None:
                errors.append({"code":"ARTIFACT_STORAGE_KIND_INVALID","path":str(path),"value":kind})
            ai=rec.get("alternative_identity")
            if ai is not None:
                contract_id=ai.get("approved_contract_id")
                contract=indexed.get(("task_execution_contract",contract_id))
                if contract is None:
                    errors.append({"code":"ALT_ID_CONTRACT_MISSING","path":str(path),"contract_id":contract_id})
                else:
                    c=contract[1]
                    if c.get("contract_status")!="approved": errors.append({"code":"ALT_ID_CONTRACT_NOT_APPROVED","path":str(path),"contract_id":contract_id})
                    if ai.get("approved_contract_sha256")!=c.get("contract_sha256"): errors.append({"code":"ALT_ID_CONTRACT_HASH_MISMATCH","path":str(path)})
                    methods=c.get("alternative_identity_methods",[])
                    matches=[m for m in methods if m.get("method_id")==ai.get("method_id") and m.get("method_version")==ai.get("method_version")]
                    if len(matches)!=1: errors.append({"code":"ALT_ID_METHOD_NOT_UNIQUE","path":str(path),"method_id":ai.get("method_id")})
                    elif matches[0].get("method_status")!="approved": errors.append({"code":"ALT_ID_METHOD_NOT_APPROVED","path":str(path),"method_id":ai.get("method_id")})
                    else:
                        if rec.get("artifact_storage_kind") not in matches[0].get("applicable_artifact_storage_kinds",[]):
                            errors.append({"code":"ALT_ID_STORAGE_KIND_NOT_APPLICABLE","path":str(path),"storage_kind":rec.get("artifact_storage_kind")})
                        if rec.get("acquired_from_source_id"):
                            src=indexed.get(("source",rec.get("acquired_from_source_id")))
                            if src and src[1].get("source_type") not in matches[0].get("applicable_source_types",[]):
                                errors.append({"code":"ALT_ID_SOURCE_TYPE_NOT_APPLICABLE","path":str(path),"source_type":src[1].get("source_type"),"method_id":ai.get("method_id")})
                if ai.get("verification_status")=="verified":
                    for field in ("evidence_artifact_ids","verified_at","verified_by","scope_statement","limitations"):
                        if field not in ai or ai[field] in (None,"",[]):
                            errors.append({"code":"ALT_ID_VERIFIED_MISSING_EVIDENCE_FIELD","path":str(path),"field":field})
                    for evid in ai.get("evidence_artifact_ids",[]):
                        ev=indexed.get(("artifact",evid))
                        if ev is None:
                            errors.append({"code":"ALT_ID_EVIDENCE_ARTIFACT_MISSING","path":str(path),"artifact_id":evid})
                        elif rec.get("project_id") is not None and ev[1].get("project_id") not in (None,rec.get("project_id")):
                            errors.append({"code":"ALT_ID_EVIDENCE_PROJECT_MISMATCH","path":str(path),"artifact_id":evid})
            if kind=="file" and content is None and ai is not None and rec.get("artifact_integrity_status")=="passed":
                errors.append({"code":"ALT_ID_CANNOT_PROMOTE_BYTE_INTEGRITY","path":str(path)})
        # Contract approval/ownership invariants.
        if rt=="task" and rec.get("active_contract_id"):
            target=indexed.get(("task_execution_contract",rec.get("active_contract_id")))
            if target:
                tr=target[1]
                if tr.get("task_id")!=rec.get("task_id"):
                    errors.append({"code":"TASK_CONTRACT_TASK_MISMATCH","path":str(path),"task_id":rec.get("task_id"),"contract_task_id":tr.get("task_id")})
                if tr.get("contract_status")!="approved":
                    errors.append({"code":"ACTIVE_CONTRACT_NOT_APPROVED","path":str(path),"contract_id":tr.get("contract_id")})
        if rt=="task_execution_contract":
            methods=rec.get("alternative_identity_methods",[])
            ids=[m.get("method_id") for m in methods if isinstance(m,dict)]
            if len(ids)!=len(set(ids)):
                errors.append({"code":"DUPLICATE_ALT_ID_METHOD_ID","path":str(path)})
            if rec.get("contract_status")=="approved":
                if not isinstance(rec.get("contract_sha256"),str) or not re.fullmatch(r"[a-f0-9]{64}",rec["contract_sha256"]):
                    errors.append({"code":"APPROVED_CONTRACT_HASH_INVALID","path":str(path)})
        # State-transition event chain: structural sequence/link checks only; event hash recomputation remains undefined.
    ledgers=defaultdict(list)
    for path,rec in norm:
        if rec.get("record_type")=="state_transition_event":
            ledgers[rec.get("ledger_id")].append((path,rec))
    for ledger,items in ledgers.items():
        items.sort(key=lambda x:x[1].get("sequence_number",0))
        seq=[x[1].get("sequence_number") for x in items]
        if any(not isinstance(n,int) for n in seq) or seq!=list(range(1,len(seq)+1)):
            errors.append({"code":"EVENT_SEQUENCE_GAP","ledger_id":ledger,"sequence":seq})
        for i,(path,rec) in enumerate(items):
            expected_prev=None if i==0 else items[i-1][1].get("event_sha256")
            actual=rec.get("previous_event_sha256")
            if actual!=expected_prev:
                errors.append({"code":"EVENT_PREVIOUS_HASH_MISMATCH","path":str(path),"ledger_id":ledger,"sequence_number":rec.get("sequence_number"),"expected":expected_prev,"actual":actual})
            if rec.get("field_name")=="artifact_integrity_status":
                transitions={"not_checked":{"in_progress","passed","failed","blocked","needs_review","not_applicable"},
                             "in_progress":{"passed","failed","blocked","needs_review"},
                             "blocked":{"in_progress","needs_review"},
                             "needs_review":{"passed","failed","blocked"}}
                if rec.get("to_status") not in transitions.get(rec.get("from_status"),set()):
                    errors.append({"code":"ILLEGAL_ARTIFACT_INTEGRITY_TRANSITION","path":str(path),"from":rec.get("from_status"),"to":rec.get("to_status")})
            if i>0 and rec.get("record_id")!=items[i-1][1].get("record_id") and rec.get("record_type")==items[i-1][1].get("record_type"):
                # Allowed: a ledger may span multiple records; keep this informational.
                warnings.append({"code":"LEDGER_SPANS_RECORDS","ledger_id":ledger,"sequence_number":rec.get("sequence_number")})
    # Detect cycles in supports/contradicts graph (all relation types retained; only supports graph drives cycle check).
    graph=defaultdict(list)
    for path,rec in norm:
        if rec.get("record_type")=="relation_edge" and rec.get("relation")=="supports":
            graph[(rec.get("from_record_type"),rec.get("from_id"))].append((rec.get("to_record_type"),rec.get("to_id")))
    visiting=set(); visited=set()
    def dfs(node, stack):
        if node in visiting:
            errors.append({"code":"SUPPORT_CYCLE","cycle":[str(x) for x in stack+[node]]}); return
        if node in visited: return
        visiting.add(node)
        for nxt in graph.get(node,[]): dfs(nxt,stack+[node])
        visiting.remove(node); visited.add(node)
    for node in list(graph): dfs(node,[])
    return {"errors":errors,"warnings":warnings,"summary":{"records":len(norm),"errors":len(errors),"warnings":len(warnings),"cross_record_scope":"explicit reference map + alternative identity + event chain continuity + supports-cycle checks","not_implemented":["JCS directory manifest hash recomputation","filesystem traversal/symlink and path-collision checks","event_sha256 payload recomputation because canonical event payload is not yet specified","all state-machine transitions for every namespace","full polymorphic reference coverage for every field","physics/scientific acceptance"]}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("data_dir"); ap.add_argument("--schemas-dir"); ap.add_argument("--output",default="cross-record-report.json")
    args=ap.parse_args()
    records=load_json_records(args.data_dir)
    schemas={}
    if args.schemas_dir:
        for p in Path(args.schemas_dir).glob("*.schema.json"):
            try: schemas[p.name.replace(".schema.json","")]=json.loads(p.read_text(encoding="utf-8"))
            except Exception: pass
    result=validate_records(records,schemas,bool(schemas))
    result["input_files"]=[{"path":str(p),"sha256":sha256_file(p)} for p,r in records]
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["summary"],ensure_ascii=False,indent=2))
    return 1 if result["errors"] else 0
if __name__=="__main__": sys.exit(main())
