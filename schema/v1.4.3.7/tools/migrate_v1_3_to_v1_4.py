#!/usr/bin/env python3
"""Conservative v1.3 -> v1.4 migration prototype. Dry-run by default.
Does not overwrite source records. Ambiguous transformations are unresolved, never guessed.
"""
import argparse, json, hashlib, csv, sys, re, math
import rfc8785
from jsonschema import Draft202012Validator, FormatChecker
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import quote
try:
    import yaml
    from yaml.events import AliasEvent
except ImportError:
    yaml=None
    AliasEvent=None

RULE_VERSION="v1.4.3.7-migration-rules-6"
TARGET_SCHEMA_VALIDATION_POLICY="draft2020-12+format-checker-per-record; invalid-targets-withheld"
TARGET_DIGEST_ALGORITHM="RFC8785-JCS-SHA256"
KNOWN_TYPES={"task","task_execution_contract","run_plan","run","run_manifest","artifact_plan","artifact","validation_plan","validation_activity","validation_report","claim","source","source_fragment","configuration","code","environment","convention_set","parameter_point","benchmark_result","evidence_fragment","test_case","test_run","state_transition_event","migration_record","relation_edge"}
TARGET_VALIDATION_ACTIVITY_STATUSES={"not_started","running","succeeded","failed","cancelled","blocked","partial"}
ID_MAPPING_FIELDS=["source_record_uri","source_record_type","source_primary_key","source_sha256","target_record_type","target_primary_key","target_sha256","candidate_target_record_type","candidate_target_primary_key","candidate_target_sha256","mapping_basis","mapping_rule_id","applied_field_mapping_ids","review_status","collision_check","rewritten_reference_count","unresolved_count","mapped_at_utc","operator"]
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
def reject_duplicate_json_keys(pairs):
    result={}
    for key,value in pairs:
        if key in result: raise ValueError(f"duplicate JSON object key: {key!r}")
        result[key]=value
    return result
def reject_nonfinite_json_constant(value):
    raise ValueError(f"non-finite JSON numeric constant is not allowed: {value}")
def ensure_json_compatible(value,seen=None):
    if seen is None: seen=set()
    if isinstance(value,dict):
        identity=id(value)
        if identity in seen: raise ValueError("cyclic YAML object graph is unsupported")
        seen.add(identity)
        for key,item in value.items():
            if not isinstance(key,str): raise ValueError(f"YAML mapping key must be a string, got {type(key).__name__}")
            ensure_json_compatible(item,seen)
        seen.remove(identity)
    elif isinstance(value,list):
        identity=id(value)
        if identity in seen: raise ValueError("cyclic YAML object graph is unsupported")
        seen.add(identity)
        for item in value: ensure_json_compatible(item,seen)
        seen.remove(identity)
    elif value is None or isinstance(value,(str,bool,int)):
        return
    elif isinstance(value,float):
        if not math.isfinite(value): raise ValueError("non-finite YAML number is not allowed")
    else:
        raise ValueError(f"non-JSON YAML value is unsupported: {type(value).__name__}")
def load_yaml_record(text):
    if yaml is None: raise RuntimeError("PyYAML is unavailable")
    class UniqueKeySafeLoader(yaml.SafeLoader):
        def compose_node(self,parent,index):
            if self.check_event(AliasEvent): raise ValueError("YAML aliases are unsupported in migration inputs")
            return super().compose_node(parent,index)
    UniqueKeySafeLoader.yaml_implicit_resolvers={
        key:[(tag,pattern) for tag,pattern in values if tag!="tag:yaml.org,2002:timestamp"]
        for key,values in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }
    def construct_mapping(loader,node,deep=False):
        mapping={}
        for key_node,value_node in node.value:
            key=loader.construct_object(key_node,deep=deep)
            try: duplicate=key in mapping
            except TypeError as e: raise ValueError("unhashable YAML mapping key") from e
            if duplicate: raise ValueError(f"duplicate YAML mapping key: {key!r}")
            mapping[key]=loader.construct_object(value_node,deep=deep)
        return mapping
    UniqueKeySafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,construct_mapping)
    return yaml.load(text,Loader=UniqueKeySafeLoader)
def stable_json(obj):
    """Return RFC 8785 canonical JSON text for deterministic target-record digests."""
    return rfc8785.dumps(obj).decode("utf-8")

def json_pointer(path):
    parts=[str(part).replace("~","~0").replace("/","~1") for part in path]
    return "/" + "/".join(parts) if parts else ""

def target_schema_error_rows(validator, instance, max_errors=100):
    """Flatten schema combinator errors and return deterministic JSON Pointer diagnostics."""
    rows=[]
    for error in validator.iter_errors(instance):
        pending=[error]
        while pending:
            current=pending.pop()
            if current.context:
                pending.extend(reversed(current.context))
                continue
            rows.append({
                "instance_path":json_pointer(current.absolute_path),
                "schema_path":json_pointer(current.absolute_schema_path),
                "message":current.message,
            })
    rows.sort(key=lambda row:(row["instance_path"],row["schema_path"],row["message"]))
    total=len(rows)
    result=rows[:max_errors]
    if total>max_errors:
        result.append({"instance_path":"","schema_path":"","message":f"{total-max_errors} additional schema errors omitted","truncated":True})
    return result
def load_mapping_contract():
    path=Path(__file__).resolve().parents[1]/"migrations"/"v1.3-to-v1.4-mapping.json"
    try:
        raw=path.read_bytes()
        contract=json.loads(raw.decode("utf-8"))
    except Exception as e:
        raise ValueError(f"migration mapping contract cannot be loaded: {e}") from e
    if contract.get("migration_rules_version")!=RULE_VERSION:
        raise ValueError(f"migration rule version mismatch: code={RULE_VERSION}, contract={contract.get('migration_rules_version')}")
    declared={(item.get("record_type"),item.get("source_field"),item.get("target_field")) for item in contract.get("field_mappings",[])}
    implemented={(record_type,source_field,target_field) for record_type,field_map in FIELD_MAPS.items() for source_field,target_field in field_map.items()} | {(record_type,source_field,target_field) for record_type,field_map in LEGACY_ALIASES_BY_TYPE.items() for source_field,target_field in field_map.items()}
    if declared!=implemented: raise ValueError("field_mappings in migration contract do not match the implementation")
    declared_ids={(item.get("record_type"),item.get("source_field"),item.get("rule_id")) for item in contract.get("field_mappings",[])}
    implemented_ids={(record_type,source_field,f"MAP-{record_type.upper()}-{source_field.upper()}") for record_type,field_map in FIELD_MAPS.items() for source_field in field_map} | {(record_type,source_field,f"MAP-{record_type.upper()}-{source_field.upper()}") for record_type,field_map in LEGACY_ALIASES_BY_TYPE.items() for source_field in field_map}
    if declared_ids!=implemented_ids: raise ValueError("field mapping rule IDs in contract do not match the implementation")
    if contract.get("id_mapping_fields")!=ID_MAPPING_FIELDS: raise ValueError("id_mapping_fields in migration contract do not match the emitted mapping rows")
    rules_by_id={rule.get("rule_id"):rule.get("rule") for rule in contract.get("rules",[]) if isinstance(rule,dict)}
    if not any(rule.get("rule_id")=="MIG-002" for rule in contract.get("rules",[])): raise ValueError("migration contract is missing MIG-002")
    required_rules={
        "MIG-012":"Validate every provisional target against its complete Draft 2020-12 JSON Schema with a format checker; any target schema error blocks target emission to staging.",
        "MIG-013":"Compute target_record_sha256 as SHA-256 over RFC 8785 JCS canonical UTF-8 bytes; source_sha256 remains the digest of the original source bytes.",
        "MIG-014":"Withhold a migrated record when a validation_ids reference resolves to a source Validation Plan or Validation Activity that does not produce a valid target record; report VALIDATION_TARGET_WITHHELD.",
        "MIG-015":"Withhold a migrated Task Execution Contract when alternative_identity_methods is absent or contract_sha256 cannot be revalidated under an owner-approved DD-ART-010 payload; do not silently default the registry to an empty array.",
    }
    for rule_id,expected_text in required_rules.items():
        if rules_by_id.get(rule_id)!=expected_text:
            raise ValueError(f"migration contract rule {rule_id} is missing or does not match the implementation")
    if contract.get("target_schema_validation")!=TARGET_SCHEMA_VALIDATION_POLICY: raise ValueError("target_schema_validation policy in migration contract does not match the implementation")
    if contract.get("target_digest_algorithm")!=TARGET_DIGEST_ALGORITHM: raise ValueError("target_digest_algorithm in migration contract does not match the implementation")
    return contract,digest_bytes(raw)
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
        reference_count=len(out[old]) if old.endswith("_ids") and isinstance(out[old],list) else 0
        rule_id=f"MAP-{rt.upper()}-{old.upper()}"
        out[new]=out[old]; changes.append({"from":old,"to":new,"basis":"explicit_rule","rule_version":RULE_VERSION,"rule_id":rule_id,"reference_count":reference_count})
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
            changes.append({"from":"validation_ids","to":"validation_activity_ids+validation_plan_ids","source_value":[],"basis":"empty_legacy_reference_list","rule_version":RULE_VERSION,"rule_id":"MIG-VAL-IDS-EMPTY-001","reference_count":0})
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
                    changes.append({"from":"validation_ids","to":"validation_plan_ids","target_id":target_id,"basis":"source_record_type","rule_version":RULE_VERSION,"rule_id":"MIG-VAL-IDS-RESOLUTION-001","reference_count":1})
                elif target_type=="validation_activity":
                    status=target.get("execution_status")
                    started_at=target.get("started_at")
                    has_start=is_timezone_aware_datetime(started_at)
                    if status in {"in_progress","succeeded","failed"} and has_start:
                        if status not in TARGET_VALIDATION_ACTIVITY_STATUSES:
                            unresolved.append({"code":"VALIDATION_ACTIVITY_STATUS_UNMAPPED","field":"execution_status","target_id":target_id,"source_value":status,"required":"an explicit migration rule to a v1.4 target enum value"})
                        else:
                            mapped_activities.append(target_id)
                            changes.append({"from":"validation_ids","to":"validation_activity_ids","target_id":target_id,"basis":"source_record_type_and_launch_evidence","rule_version":RULE_VERSION,"rule_id":"MIG-VAL-IDS-RESOLUTION-001","reference_count":1})
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
    changes.append({"from":"schema_version","to":"schema_version","old_value":sv or None,"new_value":"1.4","basis":"explicit_rule","rule_version":RULE_VERSION,"rule_id":"MIG-SCHEMA-VERSION-001"})
    # Ensure alternative identity fields are explicit but do not invent contract approval or method mappings.
    if rt=="artifact":
        if "artifact_storage_kind" not in out:
            unresolved.append({"code":"ARTIFACT_STORAGE_KIND_UNRESOLVED","field":"artifact_storage_kind","reason":"must be inferred from authoritative source evidence; extension/path guessing forbidden"})
        if "alternative_identity" not in out:
            out["alternative_identity"]=None
            changes.append({"from":"<absent>","to":"alternative_identity","new_value":None,"basis":"explicit migration rule, candidate pending approval","rule_version":RULE_VERSION,"rule_id":"MIG-ART-ALT-ID-NULL-001"})
            warnings.append({"code":"ALTERNATIVE_IDENTITY_EXPLICIT_NULL","reason":"candidate rule; approval required"})
            unresolved.append({"code":"ARTIFACT_ALTERNATIVE_IDENTITY_RULE_PENDING_APPROVAL","field":"alternative_identity","message":"the candidate null-insertion rule must not be applied to a target record before the relevant normative decision is approved"})
        if out.get("origin_kind")=="ingested_external" and out.get("artifact_storage_kind")=="file" and out.get("content_sha256") is None:
            if not (isinstance(out.get("hash_unavailable_reason"),str) and out["hash_unavailable_reason"].strip()):
                unresolved.append({"code":"HASH_UNAVAILABLE_REASON_MISSING"})
            if out.get("artifact_integrity_status")=="passed":
                out["artifact_integrity_status"]="needs_review"
                changes.append({"from":"artifact_integrity_status","to":"artifact_integrity_status","old_value":"passed","new_value":"needs_review","basis":"candidate strict semantics; pending approval","rule_version":RULE_VERSION,"rule_id":"MIG-ART-HASHLESS-REVIEW-001"})
                warnings.append({"code":"INTEGRITY_DOWNGRADED_PENDING_REVIEW"})
                unresolved.append({"code":"ARTIFACT_INTEGRITY_DOWNGRADE_RULE_PENDING_APPROVAL","field":"artifact_integrity_status","message":"the candidate downgrade rule is pending normative approval and blocks target staging"})
    if rt=="task_execution_contract":
        if "alternative_identity_methods" not in out:
            unresolved.append({
                "code":"TEC_ALTERNATIVE_IDENTITY_METHODS_MISSING_PENDING_DD_ART_010",
                "rule_id":"MIG-015",
                "field":"alternative_identity_methods",
                "decision":"DD-ART-010",
                "message":"do not silently default a missing method registry to []; the normative payload rule is pending owner approval",
            })
        if "contract_sha256" in out:
            unresolved.append({
                "code":"TEC_CONTRACT_HASH_REVALIDATION_PENDING_DD_ART_010",
                "rule_id":"MIG-015",
                "field":"contract_sha256",
                "decision":"DD-ART-010",
                "message":"the source contract hash is preserved as source evidence but cannot be asserted as a validated target hash until the owner approves the payload rule and the target digest is recomputed",
            })
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
                unresolved.append({"code":"UNKNOWN_FIELDS_QUARANTINED_REQUIRES_REVIEW","fields":unknown,"message":"quarantined source fields block generation of a target record until reviewed"})
                for k in unknown: out.pop(k,None)
            elif unknown_policy=="preserve":
                unresolved.append({"code":"UNKNOWN_FIELDS_PRESERVE_NOT_SCHEMA_SAFE","fields":unknown})
    return out,changes,unresolved,warnings
def migrate(input_dir, schemas_dir=None, output_dir=None, unknown_policy="quarantine", write_staging=False, operator=None):
    inp=Path(input_dir)
    if not inp.exists() or not inp.is_dir(): raise ValueError(f"input_dir must be an existing directory: {inp}")
    if write_staging:
        if output_dir is None: raise ValueError("--output required with --write-staging")
        outroot=Path(output_dir)
        input_resolved=inp.resolve(); output_resolved=outroot.resolve()
        if output_resolved==input_resolved or input_resolved in output_resolved.parents:
            raise ValueError("staging output must be outside the input tree to prevent recursive re-ingestion")
        if outroot.is_symlink(): raise ValueError("staging output path must not be a symlink")
        if outroot.exists():
            if not outroot.is_dir(): raise ValueError("staging output path exists and is not a directory")
            if any(outroot.iterdir()): raise ValueError("refusing to write staging output into a non-empty directory; use a new empty path")
    mapping_contract,mapping_contract_sha256=load_mapping_contract()
    records=[]; all_changes=[]; all_unresolved=[]; all_warnings=[]; idmap=[]
    schema_props={}; schema_objects={}; schema_validators={}
    schema_root=Path(schemas_dir) if schemas_dir else Path(__file__).resolve().parents[1]/"schemas"
    if not schema_root.is_dir(): raise ValueError(f"candidate schemas directory not found: {schema_root}")
    bundle_root=schema_root.parent
    if schema_root.resolve()!=(bundle_root/"schemas").resolve(): raise ValueError("schemas_dir must be the schemas directory adjacent to its bundle manifest")
    manifest_path=bundle_root/"manifest.json"
    if not manifest_path.is_file(): raise ValueError(f"candidate schema manifest not found: {manifest_path}")
    try:
        manifest_bytes=manifest_path.read_bytes()
        manifest=json.loads(manifest_bytes.decode("utf-8"))
    except Exception as e:
        raise ValueError(f"candidate schema manifest cannot be loaded: {e}") from e
    if manifest.get("schema_version")!="1.4.3.7-candidate" or manifest.get("bundle_status")!="candidate" or manifest.get("release_status")!="not_released":
        raise ValueError("migration requires the unreleased Schema v1.4.3.7 candidate manifest")
    manifest_schemas=manifest.get("schema_files",{})
    if set(manifest_schemas)!=KNOWN_TYPES:
        raise ValueError("manifest schema_files do not match the expected candidate record types")
    schema_files=sorted(schema_root.glob("*.schema.json"))
    if not schema_files: raise ValueError(f"no *.schema.json files found in {schema_root}")
    for p in schema_files:
        record_type=p.name.replace(".schema.json","")
        entry=manifest_schemas.get(record_type)
        if not isinstance(entry,dict) or not isinstance(entry.get("path"),str) or not isinstance(entry.get("sha256"),str):
            raise ValueError(f"manifest schema entry is malformed for {record_type}")
        if (bundle_root/entry["path"]).resolve()!=p.resolve():
            raise ValueError(f"manifest schema path does not match file location: {p}")
        schema_bytes=p.read_bytes()
        if digest_bytes(schema_bytes)!=entry["sha256"]:
            raise ValueError(f"candidate schema SHA-256 does not match manifest: {p}")
        try: schema=json.loads(schema_bytes.decode("utf-8"))
        except Exception as e: raise ValueError(f"invalid candidate schema JSON {p}: {e}") from e
        if not isinstance(schema,dict):
            raise ValueError(f"candidate schema root must be an object: {p}")
        if schema.get("$schema")!=manifest.get("json_schema_dialect"):
            raise ValueError(f"candidate schema dialect does not match manifest: {p}")
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as e:
            raise ValueError(f"candidate schema is invalid under Draft 2020-12: {p}: {e}") from e
        schema_objects[record_type]=schema
        schema_validators[record_type]=Draft202012Validator(schema,format_checker=FormatChecker())
        props=schema.get("properties")
        if not isinstance(props,dict): raise ValueError(f"schema has no properties object: {p}")
        record_type_schema=props.get("record_type")
        version_schema=props.get("schema_version")
        if not isinstance(record_type_schema,dict) or record_type_schema.get("const")!=record_type:
            raise ValueError(f"schema record_type does not match filename: {p}")
        if not isinstance(version_schema,dict) or version_schema.get("const")!="1.4":
            raise ValueError(f"schema version const is not 1.4: {p}")
        schema_props[record_type]=props
    if set(schema_props)!=KNOWN_TYPES or len(schema_files)!=len(KNOWN_TYPES):
        raise ValueError(f"candidate schema set mismatch; missing={sorted(KNOWN_TYPES-set(schema_props))}, extra={sorted(set(schema_props)-KNOWN_TYPES)}")

    # Load a read-only source snapshot first so legacy references can be resolved
    # by project-scoped primary key and concrete record type.
    def source_relpath(p): return p.relative_to(inp).as_posix()
    generated_at_utc=datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")
    operator_name=operator.strip() if isinstance(operator,str) and operator.strip() else "not_recorded"
    source_symlinks=sorted(p for p in inp.rglob("*") if p.is_symlink())
    for link in source_symlinks:
        all_unresolved.append({"path":source_relpath(link),"code":"SOURCE_SYMLINK_REJECTED","message":"source snapshot must not contain symlinks"})
    source_files=sorted(p for p in inp.rglob("*") if p.suffix.lower() in {".json",".yaml",".yml"} and (p.is_file() or p.is_symlink()))
    if not source_files:
        all_unresolved.append({"path":str(inp),"code":"EMPTY_SOURCE_SNAPSHOT","message":"no JSON/YAML source files were found"})
    source_entries=[]; source_index={}; typed_source_index={}
    for p in source_files:
        if p.is_symlink(): continue
        try: raw_bytes=p.read_bytes()
        except Exception as e:
            all_unresolved.append({"path":source_relpath(p),"code":"SOURCE_READ_FAILED","message":str(e)}); continue
        src_sha=digest_bytes(raw_bytes)
        try:
            source_text=raw_bytes.decode("utf-8")
            if p.suffix.lower()==".json":
                rec=json.loads(source_text,object_pairs_hook=reject_duplicate_json_keys,parse_constant=reject_nonfinite_json_constant)
            elif p.suffix.lower() in {".yaml",".yml"}:
                if yaml is None:
                    all_unresolved.append({"path":source_relpath(p),"code":"YAML_PARSER_UNAVAILABLE","source_sha256":src_sha}); continue
                rec=load_yaml_record(source_text)
                ensure_json_compatible(rec)
                json.dumps(rec,ensure_ascii=False,allow_nan=False)
            else:
                all_unresolved.append({"path":source_relpath(p),"code":"UNSUPPORTED_SOURCE_FORMAT","source_sha256":src_sha}); continue
        except Exception as e:
            code="INVALID_JSON" if p.suffix.lower()==".json" else "INVALID_YAML"
            all_unresolved.append({"path":source_relpath(p),"code":code,"source_sha256":src_sha,"message":str(e)}); continue
        if not isinstance(rec,dict):
            all_unresolved.append({"path":source_relpath(p),"code":"SOURCE_RECORD_NOT_OBJECT","source_sha256":src_sha,"actual_type":type(rec).__name__}); continue
        if not isinstance(rec.get("record_type"),str) or not rec.get("record_type","").strip():
            all_unresolved.append({"path":source_relpath(p),"code":"SOURCE_RECORD_TYPE_MISSING","source_sha256":src_sha}); continue
        source_entries.append((p,rec,src_sha))
        pk=primary_key(rec); project_id=rec.get("project_id"); rt=rec.get("record_type")
        if isinstance(project_id,str) and project_id.strip() and isinstance(pk,str) and pk.strip():
            source_index.setdefault((project_id,pk),[]).append(rec)
            typed_source_index.setdefault((project_id,rt,pk),[]).append({"path":source_relpath(p),"source_sha256":src_sha})
    duplicate_source_keys={key:entries for key,entries in typed_source_index.items() if len(entries)>1}

    for p,rec,src_sha in source_entries:
        rt=rec.get("record_type")
        out,changes,unresolved,warnings=migrate_record(rec,schema_props.get(rt),unknown_policy,source_index)
        identity=(rec.get("project_id"),rt,primary_key(rec))
        if identity in duplicate_source_keys:
            unresolved.append({"code":"DUPLICATE_SOURCE_PRIMARY_KEY","project_id":identity[0],"record_type":identity[1],"primary_key":identity[2],"source_paths":[entry["path"] for entry in duplicate_source_keys[identity]]})
        if out is not None and rt in schema_validators:
            for schema_error in target_schema_error_rows(schema_validators[rt],out):
                unresolved.append({"code":"TARGET_SCHEMA_VALIDATION_FAILED","record_type":rt,**schema_error})
        relpath=source_relpath(p)
        source_uri=quote(relpath,safe="/-._~")
        target_digest=None
        if out is not None:
            try:
                target_digest=digest_bytes(rfc8785.dumps(out))
            except Exception as e:
                unresolved.append({"code":"TARGET_CANONICALIZATION_FAILED","algorithm":TARGET_DIGEST_ALGORITHM,"message":str(e)})
        target_record=out if out is not None and not unresolved else None
        if identity in duplicate_source_keys:
            collision_check="failed"
        elif not isinstance(identity[0],str) or not identity[0].strip() or not isinstance(identity[2],str) or not identity[2].strip():
            collision_check="not_checked_missing_identity"
        else:
            collision_check="passed_typed_primary_key"
        all_changes += [{"path":relpath,"record_type":rt,"source_sha256":src_sha,**x} for x in changes]
        all_unresolved += [{"path":relpath,"record_type":rt,**x} for x in unresolved]
        all_warnings += [{"path":relpath,"record_type":rt,**x} for x in warnings]
        records.append({"source_path":relpath,"source_sha256":src_sha,"source_record_key":{"project_id":rec.get("project_id"),"record_type":rt,"primary_key":primary_key(rec)},"target_record":target_record,"target_sha256":target_digest if target_record is not None else None,"candidate_target_sha256":target_digest if out is not None and unresolved else None})
        mapping_basis="unresolved" if unresolved else ("source_reference_resolution" if any(change.get("from")=="validation_ids" for change in changes) else "explicit_rule")
        rewritten_reference_count=sum(change.get("reference_count",0) for change in changes)
        idmap.append({"source_record_uri":source_uri,"source_record_type":rt,"source_primary_key":primary_key(rec) if isinstance(primary_key(rec),str) else None,"source_sha256":src_sha,"target_record_type":rt if target_record is not None else None,"target_primary_key":primary_key(target_record) if target_record is not None else None,"target_sha256":records[-1]["target_sha256"],"candidate_target_record_type":rt if out is not None and unresolved else None,"candidate_target_primary_key":primary_key(out) if out is not None and unresolved and isinstance(primary_key(out),str) else None,"candidate_target_sha256":records[-1]["candidate_target_sha256"],"mapping_basis":mapping_basis,"mapping_rule_id":"MIG-002","applied_field_mapping_ids":sorted({change["rule_id"] for change in changes if change.get("rule_id","").startswith("MAP-")} ),"review_status":"blocked_unresolved" if unresolved else "pending_review","collision_check":collision_check,"rewritten_reference_count":rewritten_reference_count,"unresolved_count":len(unresolved),"mapped_at_utc":generated_at_utc,"operator":operator_name})
    # Fail closed for migrated validation_ids when a uniquely resolved source
    # target later fails target validation and therefore will not be emitted.
    # Without this pass, a schema-valid Claim could be staged with a dangling
    # validation_plan_ids / validation_activity_ids reference.
    target_records_by_identity={}
    for record in records:
        key=(
            record["source_record_key"].get("project_id"),
            record["source_record_key"].get("record_type"),
            record["source_record_key"].get("primary_key"),
        )
        target_records_by_identity.setdefault(key,[]).append(record)
    for record,idrow in zip(records,idmap):
        if record["target_record"] is None:
            continue
        owner_type=record["source_record_key"].get("record_type")
        owner_project=record["source_record_key"].get("project_id")
        mapped_validation_refs=[
            change for change in all_changes
            if change.get("path")==record["source_path"]
            and change.get("record_type")==owner_type
            and change.get("from")=="validation_ids"
            and change.get("target_id")
            and change.get("to") in {"validation_plan_ids","validation_activity_ids"}
        ]
        withheld_refs=[]
        for change in mapped_validation_refs:
            target_type="validation_plan" if change["to"]=="validation_plan_ids" else "validation_activity"
            target_key=(owner_project,target_type,change["target_id"])
            matches=target_records_by_identity.get(target_key,[])
            if not matches or any(target["target_record"] is None for target in matches):
                withheld_refs.append({
                    "path":record["source_path"],
                    "record_type":owner_type,
                    "code":"VALIDATION_TARGET_WITHHELD",
                    "field":change["to"],
                    "target_id":change["target_id"],
                    "target_record_type":target_type,
                    "message":"the uniquely resolved source target did not produce a valid target record; dependent record is withheld to avoid a dangling typed validation reference",
                })
        if withheld_refs:
            all_unresolved.extend(withheld_refs)
            candidate_digest=record["target_sha256"]
            candidate_primary_key=primary_key(record["target_record"])
            record["candidate_target_sha256"]=candidate_digest
            record["target_sha256"]=None
            record["target_record"]=None
            idrow["target_record_type"]=None
            idrow["target_primary_key"]=None
            idrow["target_sha256"]=None
            idrow["candidate_target_record_type"]=owner_type
            idrow["candidate_target_primary_key"]=candidate_primary_key
            idrow["candidate_target_sha256"]=candidate_digest
            idrow["mapping_basis"]="unresolved"
            idrow["review_status"]="blocked_unresolved"
            idrow["unresolved_count"]+=len(withheld_refs)
    source_files_skipped_count=len(source_files)-len(source_entries)
    snapshot_blockers=[]
    if not source_files:
        snapshot_blockers.append("EMPTY_SOURCE_SNAPSHOT")
    if source_symlinks:
        snapshot_blockers.append("SOURCE_SYMLINK_REJECTED")
    if source_files_skipped_count:
        snapshot_blockers.append("SOURCE_FILES_SKIPPED")
    snapshot_blocked=bool(snapshot_blockers)
    report={"migration_rule_version":RULE_VERSION,"source_schema_version":"1.3","target_schema_version":"1.4","mode":"write_staging" if write_staging else "dry_run","generated_at_utc":generated_at_utc,"mapping_contract_sha256":mapping_contract_sha256,"schema_manifest_sha256":digest_bytes(manifest_bytes),"target_digest_algorithm":TARGET_DIGEST_ALGORITHM,"operator":operator_name,"source_count":len(source_files),"migratable_record_count":sum(record["target_record"] is not None for record in records),"loaded_record_count":len(source_entries),"source_files_skipped_count":source_files_skipped_count,"source_symlink_count":len(source_symlinks),"staging_blocked":snapshot_blocked,"staging_blockers":snapshot_blockers,"staging_written_record_count":0,"schema_validation_failure_count":sum(item.get("code")=="TARGET_SCHEMA_VALIDATION_FAILED" for item in all_unresolved),"canonicalization_failure_count":sum(item.get("code")=="TARGET_CANONICALIZATION_FAILED" for item in all_unresolved),"changes":all_changes,"unresolved":all_unresolved,"warnings":all_warnings,"id_mapping":idmap,"commit_allowed":False,"target_schema_validation":TARGET_SCHEMA_VALIDATION_POLICY,"limitations":["Every provisional target is checked against its complete Draft 2020-12 JSON Schema with a format checker; any schema-invalid target is unresolved and withheld from staging. This does not establish cross-record or historical compatibility.","Source references are resolved only within the same project and only when primary IDs are unique.","A validation activity reference is typed only when the source activity is uniquely identified, its status is supported by an explicit target mapping, and started_at is a timezone-aware ISO date-time.","Source execution statuses outside the v1.4 target enum remain unresolved until an explicit mapping rule is approved.","Non-object JSON files, missing record_type values, malformed JSON, duplicate typed primary keys, and empty source snapshots block migration.","This prototype does not implement transactional commit or pointer-based rollback.","Task Execution Contract targets are withheld when the alternative-identity registry is missing or the source contract hash has not been revalidated under an owner-approved DD-ART-010 payload; this prototype does not recompute TEC contract hashes.","No migration is considered committed; human approval, full cross-record validation, historical compatibility evidence, and transaction safeguards are required."]}
    if write_staging:
        outroot=Path(output_dir)
        outroot.mkdir(parents=True,exist_ok=True)
        if not report["staging_blocked"]:
            for i,rec in enumerate(records):
                if rec["target_record"] is None: continue
                p=outroot/f"{i:05d}-{rec['source_record_key']['record_type']}.json"
                p.write_text(json.dumps(rec["target_record"],ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
                report["staging_written_record_count"]+=1
        (outroot/"migration-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        with (outroot/"id-mapping.csv").open("w",encoding="utf-8-sig",newline="") as f:
            fields=ID_MAPPING_FIELDS
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(idmap)
    return report
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input_dir")
    ap.add_argument("--schemas-dir")
    ap.add_argument("--output")
    ap.add_argument("--unknown-fields",choices=["quarantine","reject","preserve"],default="quarantine")
    ap.add_argument("--write-staging",action="store_true",help="write candidate staging outputs; never commits/overwrites")
    ap.add_argument("--operator",help="operator identifier recorded in the migration report; never implies approval")
    args=ap.parse_args()
    r=migrate(args.input_dir,args.schemas_dir,args.output,args.unknown_fields,args.write_staging,operator=args.operator)
    print(json.dumps({"source_count":r["source_count"],"changes":len(r["changes"]),"unresolved":len(r["unresolved"]),"warnings":len(r["warnings"]),"commit_allowed":False},ensure_ascii=False,indent=2))
    return 0
if __name__=="__main__": sys.exit(main())
