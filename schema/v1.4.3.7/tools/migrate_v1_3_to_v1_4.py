#!/usr/bin/env python3
"""Conservative v1.3 -> v1.4 migration prototype. Dry-run by default.
Does not overwrite source records. Ambiguous transformations are unresolved, never guessed.
"""
import argparse, json, hashlib, csv, sys, re
from pathlib import Path
from datetime import datetime, timezone

RULE_VERSION="v1.4.3.7-migration-rules-3"
KNOWN_TYPES={"task","task_execution_contract","run_plan","run","run_manifest","artifact_plan","artifact","validation_plan","validation_activity","validation_report","claim","source","source_fragment","configuration","code","environment","convention_set","parameter_point","benchmark_result","evidence_fragment","test_case","test_run","state_transition_event","migration_record","relation_edge"}
TARGET_VALIDATION_ACTIVITY_STATUSES={"not_started","running","succeeded","failed","cancelled","blocked","partial"}
# Candidate field mappings are listed in the migration contract; historical semantics remain unverified without the original v1.3 baseline.
FIELD_MAPS={
 "claim":{"planned_run_ids":"run_plan_ids","planned_validation_ids":"validation_plan_ids","expected_artifact_plan_ids":"artifact_plan_ids"},
 "task":{"expected_artifact_plan_ids":"artifact_plan_ids"},
 "task_execution_contract":{"expected_artifact_plan_ids":"artifact_plan_ids"},
 "run_plan":{"expected_artifact_plan_ids":"artifact_plan_ids"},
}
AMBIGUOUS={"validation_ids":"validation_activity_ids_or_validation_plan_ids"}
LEGACY_ALIASES_BY_TYPE={
 "artifact":{"sha256":"content_sha256","uri":"path_or_uri","producer_run_id":"generated_by_run_id","integrity_status":"artifact_integrity_status"},
 "task_execution_contract":{"version":"contract_version","contract_hash":"contract_sha256"},
}

def digest_bytes(b): return hashlib.sha256(b).hexdigest()
def is_timezone_aware_datetime(value):
    if not isinstance(value,str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})",value.strip()): return False
    try: parsed=datetime.fromisoformat(value.strip().replace("Z","+00:00"))
    except (TypeError,ValueError): return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None
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
    pk=primary_key(out)
    if not isinstance(pk,str) or not pk.strip():
        unresolved.append({"code":"MISSING_PRIMARY_KEY","record_type":rt,"value":pk})
    project_id=out.get("project_id")
    if not isinstance(project_id,str) or not project_id.strip():
        unresolved.append({"code":"MISSING_OR_INVALID_PROJECT_ID","record_type":rt,"value":project_id})
    if rt=="validation_activity":
        status=out.get("execution_status")
        allowed_statuses=TARGET_VALIDATION_ACTIVITY_STATUSES
        if target_properties is not None:
            status_schema=target_properties.get("execution_status",{})
            if isinstance(status_schema,dict) and isinstance(status_schema.get("enum"),list):
                allowed_statuses=set(status_schema["enum"])
        if not isinstance(status,str) or status not in allowed_statuses:
            unresolved.append({"code":"TARGET_ENUM_VALUE_UNMAPPED","field":"execution_status","source_value":status,"allowed_target_values":sorted(allowed_statuses)})
    # Explicit record-type-specific aliases.
    mapping=dict(FIELD_MAPS.get(rt,{}))
    mapping.update({k:v for k,v in LEGACY_ALIASES_BY_TYPE.get(rt,{}).items() if k in out})
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
        validation_unresolved_start=len(unresolved)
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
                    has_start=is_timezone_aware_datetime(started_at)
                    if status in {"in_progress","succeeded","failed"} and has_start:
                        if status not in TARGET_VALIDATION_ACTIVITY_STATUSES:
                            unresolved.append({"code":"VALIDATION_ACTIVITY_STATUS_UNMAPPED","field":"execution_status","target_id":target_id,"source_value":status,"required":"an explicit migration rule to a v1.4 target enum value"})
                        else:
                            mapped_activities.append(target_id)
                            changes.append({"from":"validation_ids","to":"validation_activity_ids","target_id":target_id,"basis":"source_record_type_and_launch_evidence","rule_version":RULE_VERSION})
                    elif status in {"planned","not_run"} and not has_start:
                        unresolved.append({"code":"VALIDATION_ACTIVITY_NOT_STARTED","field":"validation_ids","target_id":target_id,"execution_status":status,"started_at":started_at,"choices":["retain as unresolved","review whether a validation_plan can be constructed from source evidence"]})
                    else:
                        unresolved.append({"code":"VALIDATION_ACTIVITY_LAUNCH_EVIDENCE_INSUFFICIENT","field":"validation_ids","target_id":target_id,"execution_status":status,"started_at":started_at,"required":"a supported source execution_status plus a timezone-aware ISO date-time started_at; source statuses outside the v1.4 target enum require an explicit mapping rule"})
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
            # The target Claim schema separates plans from activities. If every
            # legacy reference was resolved, make the other typed list explicitly empty.
            if len(unresolved)==validation_unresolved_start:
                for field in ("validation_activity_ids","validation_plan_ids"):
                    if field not in out:
                        out[field]=[]

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
    if rt=="claim":
        for field in ("validation_activity_ids","validation_plan_ids"):
            if field not in out: continue
            values=out[field]
            if not isinstance(values,list):
                unresolved.append({"code":"TYPED_VALIDATION_REFERENCES_INVALID_SHAPE","field":field,"value":values})
                continue
            invalid_values=[value for value in values if not isinstance(value,str) or not value.strip()]
            if invalid_values:
                unresolved.append({"code":"TYPED_VALIDATION_REFERENCE_INVALID_VALUE","field":field,"values":invalid_values})
            string_values=[value for value in values if isinstance(value,str)]
            duplicates=sorted({value for value in string_values if string_values.count(value)>1})
            if duplicates:
                unresolved.append({"code":"DUPLICATE_TYPED_VALIDATION_REFERENCES","field":field,"values":duplicates})
    if target_properties is not None:
        for field,field_schema in target_properties.items():
            if rt=="validation_activity" and field=="execution_status": continue
            enum_values=field_schema.get("enum") if isinstance(field_schema,dict) else None
            if field in out and isinstance(enum_values,list) and out[field] not in enum_values:
                unresolved.append({"code":"TARGET_ENUM_VALUE_UNMAPPED","field":field,"source_value":out[field],"allowed_target_values":enum_values})
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
    inp=Path(input_dir)
    if not inp.exists() or not inp.is_dir(): raise ValueError(f"input_dir must be an existing directory: {inp}")
    if write_staging:
        if output_dir is None: raise ValueError("--output required with --write-staging")
        outroot=Path(output_dir)
        input_resolved=inp.resolve(); output_resolved=outroot.resolve()
        if output_resolved==input_resolved or input_resolved in output_resolved.parents:
            raise ValueError("staging output must be outside the input tree to prevent recursive re-ingestion")
        if outroot.exists():
            if not outroot.is_dir(): raise ValueError("staging output path exists and is not a directory")
            if any(outroot.iterdir()): raise ValueError("refusing to write staging output into a non-empty directory; use a new empty path")
    records=[]; all_changes=[]; all_unresolved=[]; all_warnings=[]; idmap=[]
    schema_props={}
    schema_root=Path(schemas_dir) if schemas_dir else Path(__file__).resolve().parents[1]/"schemas"
    if not schema_root.is_dir(): raise ValueError(f"candidate schemas directory not found: {schema_root}")
    schema_files=sorted(schema_root.glob("*.schema.json"))
    if not schema_files: raise ValueError(f"no *.schema.json files found in {schema_root}")
    for p in schema_files:
        try: schema=json.loads(p.read_text(encoding="utf-8"))
        except Exception as e: raise ValueError(f"invalid candidate schema JSON {p}: {e}") from e
        record_type=p.name.replace(".schema.json","")
        props=schema.get("properties")
        if not isinstance(props,dict): raise ValueError(f"schema has no properties object: {p}")
        if props.get("record_type",{}).get("const")!=record_type: raise ValueError(f"schema record_type does not match filename: {p}")
        if props.get("schema_version",{}).get("const")!="1.4": raise ValueError(f"schema version const is not 1.4: {p}")
        schema_props[record_type]=props
    if set(schema_props)!=KNOWN_TYPES:
        raise ValueError(f"candidate schema set mismatch; missing={sorted(KNOWN_TYPES-set(schema_props))}, extra={sorted(set(schema_props)-KNOWN_TYPES)}")

    # Load a read-only source snapshot first so legacy references can be resolved
    # by project-scoped primary key and concrete record type.
    source_files=sorted(inp.rglob("*.json"))
    if not source_files:
        all_unresolved.append({"path":str(inp),"code":"EMPTY_SOURCE_SNAPSHOT","message":"no JSON source files were found"})
    source_entries=[]; source_index={}; typed_source_index={}
    for p in source_files:
        try: raw_bytes=p.read_bytes()
        except Exception as e:
            all_unresolved.append({"path":str(p),"code":"SOURCE_READ_FAILED","message":str(e)}); continue
        src_sha=digest_bytes(raw_bytes)
        try: rec=json.loads(raw_bytes.decode("utf-8"))
        except Exception as e:
            all_unresolved.append({"path":str(p),"code":"INVALID_JSON","source_sha256":src_sha,"message":str(e)}); continue
        if not isinstance(rec,dict):
            all_unresolved.append({"path":str(p),"code":"SOURCE_RECORD_NOT_OBJECT","source_sha256":src_sha,"actual_type":type(rec).__name__}); continue
        if not isinstance(rec.get("record_type"),str) or not rec.get("record_type","").strip():
            all_unresolved.append({"path":str(p),"code":"SOURCE_RECORD_TYPE_MISSING","source_sha256":src_sha}); continue
        source_entries.append((p,rec,src_sha))
        pk=primary_key(rec); project_id=rec.get("project_id"); rt=rec.get("record_type")
        if isinstance(project_id,str) and project_id.strip() and isinstance(pk,str) and pk.strip():
            source_index.setdefault((project_id,pk),[]).append(rec)
            typed_source_index.setdefault((project_id,rt,pk),[]).append({"path":str(p),"source_sha256":src_sha})
    duplicate_source_keys={key:entries for key,entries in typed_source_index.items() if len(entries)>1}

    for p,rec,src_sha in source_entries:
        rt=rec.get("record_type")
        out,changes,unresolved,warnings=migrate_record(rec,schema_props.get(rt),unknown_policy,source_index)
        identity=(rec.get("project_id"),rt,primary_key(rec))
        if identity in duplicate_source_keys:
            unresolved.append({"code":"DUPLICATE_SOURCE_PRIMARY_KEY","project_id":identity[0],"record_type":identity[1],"primary_key":identity[2],"source_paths":[entry["path"] for entry in duplicate_source_keys[identity]]})
        all_changes += [{"path":str(p),"record_type":rt,"source_sha256":src_sha,**x} for x in changes]
        all_unresolved += [{"path":str(p),"record_type":rt,**x} for x in unresolved]
        all_warnings += [{"path":str(p),"record_type":rt,**x} for x in warnings]
        records.append({"source_path":str(p),"source_sha256":src_sha,"source_record_key":{"project_id":rec.get("project_id"),"record_type":rt,"primary_key":primary_key(rec)},"target_record":out,"target_sha256":digest_bytes(stable_json(out).encode("utf-8")) if out is not None else None})
        mapping_basis="unresolved" if unresolved else ("source_reference_resolution" if any(change.get("from")=="validation_ids" for change in changes) else "explicit_rule")
        idmap.append({"source_path":str(p),"source_record_type":rt,"source_id":primary_key(rec),"target_record_type":rt,"target_id":primary_key(out or {}),"mapping_basis":mapping_basis,"unresolved_count":len(unresolved),"source_sha256":src_sha,"target_sha256":digest_bytes(stable_json(out).encode("utf-8")) if out else None})
    report={"migration_rule_version":RULE_VERSION,"source_schema_version":"1.3","target_schema_version":"1.4","mode":"write_staging" if write_staging else "dry_run","source_count":len(source_files),"migratable_record_count":sum(record["target_record"] is not None for record in records),"loaded_record_count":len(source_entries),"source_files_skipped_count":len(source_files)-len(source_entries),"changes":all_changes,"unresolved":all_unresolved,"warnings":all_warnings,"id_mapping":idmap,"commit_allowed":False,"target_schema_validation":"not_performed_by_migration_prototype","limitations":["Candidate schema files are loaded fail-closed for top-level property filtering and enum checks, but full JSON Schema validation of target records is not performed by this prototype.","Source references are resolved only within the same project and only when primary IDs are unique.","A validation activity reference is typed only when the source activity is uniquely identified, its status is supported by an explicit target mapping, and started_at is a timezone-aware ISO date-time.","Source execution statuses outside the v1.4 target enum remain unresolved until an explicit mapping rule is approved.","Non-object JSON files, missing record_type values, malformed JSON, duplicate typed primary keys, and empty source snapshots block migration.","This prototype does not implement transactional commit or pointer-based rollback.","It does not recalculate TEC contract hashes unless canonical source payload is available.","No migration is considered committed; human approval and full target validation are required."]}
    if write_staging:
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
