#!/usr/bin/env python3
"""Conservative v1.3 -> v1.4 migration prototype. Dry-run by default.
Does not overwrite source records. Ambiguous transformations are unresolved, never guessed.
"""
import argparse, json, hashlib, csv, sys
from pathlib import Path
from datetime import datetime, timezone

RULE_VERSION="v1.4.3.7-migration-rules-2"
KNOWN_TYPES={"task","task_execution_contract","run_plan","run","run_manifest","artifact_plan","artifact","validation_plan","validation_activity","validation_report","claim","source","source_fragment","configuration","code","environment","convention_set","parameter_point","benchmark_result","evidence_fragment","test_case","test_run","state_transition_event","migration_record","relation_edge"}
# Only unambiguous, explicitly documented renames.
FIELD_MAPS={
 "claim":{"planned_run_ids":"run_plan_ids","planned_validation_ids":"validation_plan_ids","expected_artifact_plan_ids":"artifact_plan_ids"},
 "task":{"expected_artifact_plan_ids":"artifact_plan_ids"},
 "task_execution_contract":{"expected_artifact_plan_ids":"artifact_plan_ids"},
 "run_plan":{"expected_artifact_plan_ids":"artifact_plan_ids"},
}
AMBIGUOUS={"validation_ids":"validation_activity_ids_or_validation_plan_ids"}
LEGACY_ALIASES={"sha256":"content_sha256","uri":"path_or_uri","producer_run_id":"generated_by_run_id","integrity_status":"artifact_integrity_status","version":"contract_version","contract_hash":"contract_sha256"}

def digest_bytes(b): return hashlib.sha256(b).hexdigest()
def stable_json(obj): return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)
def primary_key(rec):
    rt=rec.get("record_type")
    return rec.get({"task":"task_id","task_execution_contract":"contract_id","run_plan":"run_plan_id","run":"run_id","run_manifest":"manifest_id","artifact_plan":"artifact_plan_id","artifact":"artifact_id","validation_plan":"validation_plan_id","validation_activity":"validation_activity_id","validation_report":"validation_report_id","claim":"claim_id","source":"source_id","source_fragment":"source_fragment_id","configuration":"configuration_id","code":"code_id","environment":"environment_id","convention_set":"conventions_id","parameter_point":"point_id","benchmark_result":"benchmark_result_id","evidence_fragment":"evidence_id","test_case":"test_case_id","test_run":"test_run_id","state_transition_event":"event_id","migration_record":"migration_record_id","relation_edge":"edge_id"}.get(rt,""))
def migrate_record(rec, target_properties=None, unknown_policy="quarantine", source_index=None):
    out=dict(rec); changes=[]; unresolved=[]; warnings=[]
    rt=out.get("record_type")
    if rt not in KNOWN_TYPES: return None,changes,[{"code":"UNKNOWN_RECORD_TYPE","record_type":rt}],warnings
    sv=str(out.get("schema_version",""))
    if sv not in {"1.3","1.3.0"}:
        unresolved.append({"code":"UNSUPPORTED_SOURCE_VERSION","schema_version":sv,"required":"1.3","record_type":rt})
    if not primary_key(out):
        unresolved.append({"code":"MISSING_PRIMARY_KEY","record_type":rt})
    # Explicit record-type-specific aliases.
    mapping=dict(FIELD_MAPS.get(rt,{}))
    if rt=="artifact":
        mapping.update({k:v for k,v in LEGACY_ALIASES.items() if k in out})
    if rt=="task_execution_contract":
        mapping.update({k:v for k,v in LEGACY_ALIASES.items() if k in out})
    if rt=="run":
        mapping.update({k:v for k,v in LEGACY_ALIASES.items() if k in out})
    for old,new in mapping.items():
        if old not in out: continue
        if new in out and out[new] != out[old]:
            unresolved.append({"code":"FIELD_MAPPING_CONFLICT","old_field":old,"new_field":new,"old_value":out[old],"new_value":out[new]})
            continue
        out[new]=out[old]; changes.append({"from":old,"to":new,"basis":"explicit_rule","rule_version":RULE_VERSION})
        if old!=new: out.pop(old,None)

    # Resolve validation_ids only when the source graph identifies a unique target
    # type and, for activities, evidence that execution actually started.
    if "validation_ids" in out:
        raw_ids=out.pop("validation_ids")
        if not isinstance(raw_ids,list):
            unresolved.append({"code":"VALIDATION_IDS_INVALID_SHAPE","field":"validation_ids","source_value":raw_ids})
        elif not raw_ids:
            # An empty legacy list carries no type information and no references;
            # represent "no references" explicitly in both typed target fields.
            for field in ("validation_activity_ids","validation_plan_ids"):
                if field not in out:
                    out[field]=[]
                elif not isinstance(out[field],list):
                    unresolved.append({"code":"FIELD_MAPPING_CONFLICT","old_field":"validation_ids","new_field":field,"existing_value":out[field],"mapped_values":[]})
            changes.append({"from":"validation_ids","to":"validation_activity_ids+validation_plan_ids","source_value":[],"basis":"empty_legacy_reference_list","rule_version":RULE_VERSION})
        else:
            if any(not isinstance(value,str) or not value.strip() for value in raw_ids):
                unresolved.append({"code":"VALIDATION_IDS_INVALID_VALUE","field":"validation_ids","source_value":raw_ids})
            if len(raw_ids)!=len(set(value for value in raw_ids if isinstance(value,str))):
                unresolved.append({"code":"DUPLICATE_VALIDATION_IDS","field":"validation_ids","source_value":raw_ids})
            mapped_activities=[]; mapped_plans=[]
            for target_id in raw_ids:
                if not isinstance(target_id,str) or not target_id.strip():
                    continue
                matches=(source_index or {}).get((out.get("project_id"),target_id),[])
                if len(matches)==0:
                    unresolved.append({"code":"VALIDATION_TARGET_NOT_FOUND","field":"validation_ids","target_id":target_id,"basis":"no matching source record in the same project"})
                    continue
                if len(matches)>1:
                    unresolved.append({"code":"VALIDATION_TARGET_ID_AMBIGUOUS","field":"validation_ids","target_id":target_id,"matching_record_types":sorted(str(item.get("record_type")) for item in matches),"basis":"primary ID is not unique in the source project"})
                    continue
                target=matches[0]
                target_type=target.get("record_type")
                if target_type=="validation_plan":
                    mapped_plans.append(target_id)
                    changes.append({"from":"validation_ids","to":"validation_plan_ids","target_id":target_id,"basis":"source_record_type","rule_version":RULE_VERSION})
                elif target_type=="validation_activity":
                    status=target.get("execution_status")
                    started_at=target.get("started_at")
                    has_start=isinstance(started_at,str) and bool(started_at.strip())
                    if status in {"in_progress","succeeded","failed"} and has_start:
                        mapped_activities.append(target_id)
                        changes.append({"from":"validation_ids","to":"validation_activity_ids","target_id":target_id,"basis":"source_record_type_and_launch_evidence","rule_version":RULE_VERSION})
                    elif status in {"planned","not_run"} and not has_start:
                        unresolved.append({"code":"VALIDATION_ACTIVITY_NOT_STARTED","field":"validation_ids","target_id":target_id,"execution_status":status,"started_at":started_at,"choices":["retain as unresolved","review whether a validation_plan can be constructed from source evidence"]})
                    else:
                        unresolved.append({"code":"VALIDATION_ACTIVITY_LAUNCH_EVIDENCE_INSUFFICIENT","field":"validation_ids","target_id":target_id,"execution_status":status,"started_at":started_at,"required":"execution_status in in_progress/succeeded/failed and non-empty started_at"})
                else:
                    unresolved.append({"code":"VALIDATION_TARGET_TYPE_UNSUPPORTED","field":"validation_ids","target_id":target_id,"target_record_type":target_type,"choices":["validation_activity_ids","validation_plan_ids"]})
            for field,values in (("validation_activity_ids",mapped_activities),("validation_plan_ids",mapped_plans)):
                if not values:
                    continue
                existing=out.get(field,[])
                if not isinstance(existing,list):
                    unresolved.append({"code":"FIELD_MAPPING_CONFLICT","old_field":"validation_ids","new_field":field,"existing_value":existing,"mapped_values":values})
                    continue
                # Stable merge preserves pre-existing references and does not silently duplicate IDs.
                merged=list(existing)
                for value in values:
                    if value not in merged:
                        merged.append(value)
                out[field]=merged

    out["schema_version"]="1.4"
    changes.append({"from":"schema_version","to":"schema_version","old_value":sv or None,"new_value":"1.4","basis":"explicit_rule","rule_version":RULE_VERSION})
    # Ensure alternative identity fields are explicit but do not invent contract approval or method mappings.
    if rt=="artifact":
        if "artifact_storage_kind" not in out:
            unresolved.append({"code":"ARTIFACT_STORAGE_KIND_UNRESOLVED","field":"artifact_storage_kind","reason":"must be inferred from authoritative source evidence; extension/path guessing forbidden"})
        if "alternative_identity" not in out:
            out["alternative_identity"]=None
            changes.append({"from":"<absent>","to":"alternative_identity","new_value":None,"basis":"explicit migration rule, candidate pending approval","rule_version":RULE_VERSION})
            warnings.append({"code":"ALTERNATIVE_IDENTITY_EXPLICIT_NULL","reason":"candidate rule; approval required"})
        if out.get("origin_kind")=="ingested_external" and out.get("artifact_storage_kind")=="file" and out.get("content_sha256") is None:
            if not (isinstance(out.get("hash_unavailable_reason"),str) and out["hash_unavailable_reason"].strip()):
                unresolved.append({"code":"HASH_UNAVAILABLE_REASON_MISSING"})
            if out.get("artifact_integrity_status")=="passed":
                out["artifact_integrity_status"]="needs_review"
                changes.append({"from":"artifact_integrity_status","to":"artifact_integrity_status","old_value":"passed","new_value":"needs_review","basis":"candidate strict semantics; pending approval","rule_version":RULE_VERSION})
                warnings.append({"code":"INTEGRITY_DOWNGRADED_PENDING_REVIEW"})
    # Strict unknown-field strategy: quarantine extras in report, never silently preserve them in schema record.
    if target_properties is not None:
        unknown=sorted(set(out)-set(target_properties))
        if unknown:
            if unknown_policy=="reject":
                unresolved.append({"code":"UNKNOWN_FIELDS","fields":unknown})
            elif unknown_policy=="quarantine":
                warnings.append({"code":"UNKNOWN_FIELDS_QUARANTINED","fields":unknown,"values":{k:out[k] for k in unknown}})
                for k in unknown: out.pop(k,None)
            elif unknown_policy=="preserve":
                unresolved.append({"code":"UNKNOWN_FIELDS_PRESERVE_NOT_SCHEMA_SAFE","fields":unknown})
    return out,changes,unresolved,warnings
def migrate(input_dir, schemas_dir=None, output_dir=None, unknown_policy="quarantine", write_staging=False):
    inp=Path(input_dir); records=[]; all_changes=[]; all_unresolved=[]; all_warnings=[]; idmap=[]
    schema_props={}
    if schemas_dir:
        for p in Path(schemas_dir).glob("*.schema.json"):
            try: schema_props[p.name.replace(".schema.json","")]=json.loads(p.read_text(encoding="utf-8")).get("properties",{})
            except Exception: pass

    # Load a read-only source snapshot first so legacy references can be resolved
    # by project-scoped primary key and concrete record type.
    source_entries=[]; source_index={}
    for p in sorted(inp.rglob("*.json")):
        try:
            raw_bytes=p.read_bytes()
            rec=json.loads(raw_bytes.decode("utf-8"))
        except Exception as e:
            all_unresolved.append({"path":str(p),"code":"INVALID_JSON","message":str(e)}); continue
        if not isinstance(rec,dict) or "record_type" not in rec: continue
        src_sha=digest_bytes(raw_bytes)
        source_entries.append((p,rec,src_sha))
        pk=primary_key(rec)
        project_id=rec.get("project_id")
        if isinstance(project_id,str) and project_id.strip() and isinstance(pk,str) and pk.strip():
            source_index.setdefault((project_id,pk),[]).append(rec)

    for p,rec,src_sha in source_entries:
        rt=rec.get("record_type")
        out,changes,unresolved,warnings=migrate_record(rec,schema_props.get(rt),unknown_policy,source_index)
        all_changes += [{"path":str(p),"record_type":rt,"source_sha256":src_sha,**x} for x in changes]
        all_unresolved += [{"path":str(p),"record_type":rt,**x} for x in unresolved]
        all_warnings += [{"path":str(p),"record_type":rt,**x} for x in warnings]
        records.append({"source_path":str(p),"source_sha256":src_sha,"source_record_key":{"project_id":rec.get("project_id"),"record_type":rt,"primary_key":primary_key(rec)},"target_record":out,"target_sha256":digest_bytes(stable_json(out).encode("utf-8")) if out is not None else None})
        idmap.append({"source_path":str(p),"source_record_type":rt,"source_id":primary_key(rec),"target_record_type":rt,"target_id":primary_key(out or {}),"mapping_basis":"explicit_rule" if not unresolved else "unresolved","unresolved_count":len(unresolved),"source_sha256":src_sha,"target_sha256":digest_bytes(stable_json(out).encode("utf-8")) if out else None})
    report={"migration_rule_version":RULE_VERSION,"source_schema_version":"1.3","target_schema_version":"1.4","mode":"write_staging" if write_staging else "dry_run","source_count":len(records),"changes":all_changes,"unresolved":all_unresolved,"warnings":all_warnings,"id_mapping":idmap,"commit_allowed":False,"limitations":["Source references are resolved only within the same project and only when primary IDs are unique.","A validation activity maps as an actual activity only when execution_status is in_progress/succeeded/failed and started_at is non-empty.","A validation activity with not_run/planned status is not silently converted into a validation plan; the source must support a separate plan record.","This prototype does not implement transactional commit or pointer-based rollback.","It does not recalculate TEC contract hashes unless canonical source payload is available.","No migration is considered committed; human approval and full target validation are required."]}
    if write_staging:
        if output_dir is None: raise ValueError("--output required with --write-staging")
        outroot=Path(output_dir)
        outroot.mkdir(parents=True,exist_ok=True)
        for i,rec in enumerate(records):
            if rec["target_record"] is None: continue
            p=outroot/f"{i:05d}-{rec['source_record_key']['record_type']}.json"
            p.write_text(json.dumps(rec["target_record"],ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        (outroot/"migration-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        with (outroot/"id-mapping.csv").open("w",encoding="utf-8-sig",newline="") as f:
            fields=list(idmap[0].keys()) if idmap else ["source_path"]
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(idmap)
    return report
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input_dir")
    ap.add_argument("--schemas-dir")
    ap.add_argument("--output")
    ap.add_argument("--unknown-fields",choices=["quarantine","reject","preserve"],default="quarantine")
    ap.add_argument("--write-staging",action="store_true",help="write candidate staging outputs; never commits/overwrites")
    args=ap.parse_args()
    r=migrate(args.input_dir,args.schemas_dir,args.output,args.unknown_fields,args.write_staging)
    print(json.dumps({"source_count":r["source_count"],"changes":len(r["changes"]),"unresolved":len(r["unresolved"]),"warnings":len(r["warnings"]),"commit_allowed":False},ensure_ascii=False,indent=2))
    return 0
if __name__=="__main__": sys.exit(main())
