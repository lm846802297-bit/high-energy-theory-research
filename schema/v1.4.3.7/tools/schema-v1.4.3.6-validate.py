#!/usr/bin/env python3
import json,hashlib,csv,sys,os
from datetime import datetime, timezone
from pathlib import Path
from jsonschema import Draft202012Validator,FormatChecker

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main(root):
 root=Path(root); report={'checks':[],'fixtures':[],'semantic_tests':[],'legacy_fixture_compatibility':{},'limitations':['Full state machine/event ledger is not implemented.','Migration and backward compatibility are not validated.','No filesystem walk, network retrieval, raw-byte hash recomputation, or JCS directory manifest hash recomputation.','No physics/scientific correctness validation.']}
 def add(n,ok,detail=None): report['checks'].append({'name':n,'status':'PASS' if ok else 'FAIL','detail':detail or {}})
 m=json.loads((root/'manifest.json').read_text()); idx=json.loads((root/m['fixture_index']).read_text()); legacy_idx=json.loads((root/m['legacy_fixture_index']).read_text()); schemas={}
 add('candidate_release_status',m.get('schema_version')=='1.4.3.7-candidate' and m.get('bundle_status')=='candidate' and m.get('release_status')=='not_released',{'schema_version':m.get('schema_version'),'bundle_status':m.get('bundle_status'),'release_status':m.get('release_status')})
 for rt,e in m['schema_files'].items():
  p=root/e['path']; ok=p.exists() and sha(p)==e['sha256']; add('schema_hash:'+rt,ok)
  if ok:
   s=json.loads(p.read_text())
   try: Draft202012Validator.check_schema(s); Draft202012Validator(s,format_checker=FormatChecker()); schemas[rt]=s; add('schema_meta:'+rt,True)
   except Exception as ex: add('schema_meta:'+rt,False,{'error':str(ex)})
 add('record_types_match',set(m['record_types'])==set(schemas),{'declared':len(m['record_types']),'loaded':len(schemas)})
 test_case_schema=schemas.get('test_case',{}); test_id_schema=test_case_schema.get('properties',{}).get('test_id',{})
 add('manifest_test_id_pattern_matches_schema',isinstance(m.get('test_id_pattern'),str) and bool(m.get('test_id_pattern')) and m.get('test_id_pattern')==test_id_schema.get('pattern'),{'manifest_pattern':m.get('test_id_pattern'),'schema_pattern':test_id_schema.get('pattern')})
 add('strict_unknown_fields_enabled',m.get('strict_unknown_fields') is True)
 add('extensions_disabled',m.get('extensions_supported') is False)
 add('fixture_index_hash',sha(root/m['fixture_index'])==m['fixture_index_sha256'])
 add('legacy_fixture_index_hash',sha(root/m['legacy_fixture_index'])==m['legacy_fixture_index_sha256'])
 add('fixture_index_version_matches_bundle',idx.get('schema_version')==m.get('schema_version'),{'index_version':idx.get('schema_version'),'bundle_version':m.get('schema_version')})
 add('legacy_fixture_index_version_matches_declared_baseline',legacy_idx.get('schema_version')==m.get('legacy_fixture_index_schema_version')=='1.4.3.6-candidate',{'index_version':legacy_idx.get('schema_version'),'declared_baseline':m.get('legacy_fixture_index_schema_version')})
 ids=set()
 for x in idx['fixtures']:
  fid=x['fixture_id']; unique=fid not in ids; ids.add(fid)
  try: data=json.loads((root/x['file']).read_text())
  except Exception as ex:
   report['fixtures'].append({'fixture_id':fid,'expected':x['expected_schema_result'],'actual':'invalid_json','ok':False,'errors':[str(ex)]}); continue
  errs=list(Draft202012Validator(schemas[x['record_type']],format_checker=FormatChecker()).iter_errors(data))
  actual='pass' if not errs else 'fail'; ok=unique and actual==x['expected_schema_result']
  report['fixtures'].append({'fixture_id':fid,'record_type':x['record_type'],'expected':x['expected_schema_result'],'actual':actual,'ok':ok,'errors':[e.message for e in errs[:4]]})
 add('fixture_ids_unique',len(ids)==len(idx['fixtures']))
 with (root/'audit/requirement-test-trace.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
 add('manifest_traceability_row_count_matches',m.get('requirement_traceability_rows')==len(rows),{'manifest_rows':m.get('requirement_traceability_rows'),'actual_rows':len(rows)})
 add('manifest_release_evidence_traceability_rows_matches',m.get('release_evidence',{}).get('traceability_rows')==len(rows),{'release_evidence_rows':m.get('release_evidence',{}).get('traceability_rows'),'actual_rows':len(rows)})
 req=[x['requirement_id'] for x in rows]; tests=[x['test_id'] for x in rows]
 add('requirement_ids_unique',len(req)==len(set(req))); add('test_ids_unique',len(tests)==len(set(tests)))
 fids={x['fixture_id'] for x in idx['fixtures']}; traced={fid for x in rows for fid in x['fixture_ids'].split(';') if fid}
 add('trace_fixture_refs_valid',traced<=fids,{'dangling':sorted(traced-fids)}); add('all_fixtures_traced',fids<=traced,{'untraced':sorted(fids-traced)})
 legacy_mismatches=[]
 for x in legacy_idx['fixtures']:
  try: legacy_data=json.loads((root/x['file']).read_text())
  except Exception as ex:
   legacy_mismatches.append({'fixture_id':x['fixture_id'],'expected':x['expected_schema_result'],'actual':'invalid_json','error':str(ex)}); continue
  legacy_errors=list(Draft202012Validator(schemas[x['record_type']],format_checker=FormatChecker()).iter_errors(legacy_data))
  legacy_actual='pass' if not legacy_errors else 'fail'
  if legacy_actual!=x['expected_schema_result']:
   legacy_mismatches.append({'fixture_id':x['fixture_id'],'record_type':x['record_type'],'expected':x['expected_schema_result'],'actual':legacy_actual,'errors':[e.message for e in legacy_errors[:4]]})
 report['legacy_fixture_compatibility']={'index_version':legacy_idx.get('schema_version'),'candidate_schema_version':m.get('schema_version'),'versions_differ':legacy_idx.get('schema_version')!=m.get('schema_version'),'total':len(legacy_idx['fixtures']),'mismatches_against_candidate_schemas':len(legacy_mismatches),'mismatches':legacy_mismatches,'interpretation':'The canonical fixture index is version-matched to the candidate bundle; the separately declared legacy index is retained as a historical expectation baseline.'}
 if legacy_mismatches:
  report['limitations'].append(f"Inherited fixture index {legacy_idx.get('schema_version')} has {len(legacy_mismatches)} expected-outcome mismatches when evaluated against {m.get('schema_version')}; see legacy_fixture_compatibility. These do not replace the version-matched candidate fixture suite.")
 # DD-ART-006 cross-record checks over test bundles. These are explicit candidate semantics only.
 sem_path=root/'tests/semantic/alternative-identity-cases.json'
 if sem_path.exists():
  cases=json.loads(sem_path.read_text())
  def sem(a,c,s):
   e=[]
   if a.get('project_id')!=c.get('project_id'): e.append('PROJECT_MISMATCH')
   if c.get('contract_status')!='approved': e.append('CONTRACT_NOT_APPROVED')
   alt=a.get('alternative_identity')
   if a.get('content_sha256') is not None:
    if alt is not None: e.append('ALT_IDENTITY_WITH_CONTENT_HASH')
    return e
   if a.get('origin_kind')!='ingested_external' or a.get('artifact_storage_kind')!='file':
    if alt is not None: e.append('ALT_IDENTITY_SCOPE_INVALID')
    return e
   if not a.get('hash_unavailable_reason'): e.append('HASH_MISSING_REASON')
   if alt is None:
    if a.get('artifact_integrity_status')!='needs_review': e.append('HASHLESS_EXTERNAL_MUST_NEEDS_REVIEW')
    return e
   if a.get('acquired_from_source_id')!=s.get('source_id'): e.append('SOURCE_ID_MISMATCH')
   if s.get('project_id')!=a.get('project_id'): e.append('SOURCE_PROJECT_MISMATCH')
   if c.get('contract_id')!=alt.get('approved_contract_id'): e.append('CONTRACT_ID_MISMATCH')
   if c.get('contract_sha256')!=alt.get('approved_contract_sha256'): e.append('CONTRACT_HASH_MISMATCH')
   methods=c.get('alternative_identity_methods',[]); ids2=[m.get('method_id') for m in methods]
   if len(ids2)!=len(set(ids2)): e.append('DUPLICATE_METHOD_ID_IN_CONTRACT')
   matches=[m for m in methods if m.get('method_id')==alt.get('method_id') and m.get('method_version')==alt.get('method_version')]
   if len(matches)!=1: e.append('METHOD_NOT_FOUND_OR_AMBIGUOUS')
   else:
    mm=matches[0]
    if mm.get('method_status')!='approved': e.append('METHOD_NOT_APPROVED')
    if s.get('source_type') not in mm.get('applicable_source_types',[]): e.append('SOURCE_TYPE_NOT_APPLICABLE')
    if a.get('artifact_storage_kind') not in mm.get('applicable_artifact_storage_kinds',[]): e.append('STORAGE_KIND_NOT_APPLICABLE')
   if alt.get('verification_status')=='verified' and (not alt.get('verified_at') or not alt.get('verified_by') or not alt.get('evidence_artifact_ids')): e.append('VERIFICATION_EVIDENCE_INCOMPLETE')
   if a.get('artifact_integrity_status')=='passed': e.append('HASHLESS_ARTIFACT_CANNOT_PASS_BYTE_INTEGRITY')
   return e
  for case in cases:
   a,c,s=case['artifact'],case['contract'],case['source']
   errs=[]
   for rt,obj in [('artifact',a),('task_execution_contract',c),('source',s)]:
    es=list(Draft202012Validator(schemas[rt],format_checker=FormatChecker()).iter_errors(obj))
    if es: errs.append({'record_type':rt,'errors':[e.message for e in es[:4]]})
   sem_errors=sem(a,c,s)
   schema_valid=not errs
   actual='pass' if schema_valid and not sem_errors else ('schema_reject' if not schema_valid else 'semantic_reject')
   ok=actual==case['expected']
   report['semantic_tests'].append({'test_id':case['test_id'],'expected':case['expected'],'actual':actual,'ok':ok,'schema_errors':errs,'semantic_errors':sem_errors})
 add('semantic_test_expectations_match',all(x['ok'] for x in report['semantic_tests']),{'total':len(report['semantic_tests']),'failed':[x['test_id'] for x in report['semantic_tests'] if not x['ok']]})
 bad=[x for x in report['fixtures'] if not x['ok']]; sem_bad=[x for x in report['semantic_tests'] if not x['ok']]
 report['summary']={'checks_total':len(report['checks']),'checks_passed':sum(x['status']=='PASS' for x in report['checks']),'checks_failed':sum(x['status']=='FAIL' for x in report['checks']),'fixtures_total':len(report['fixtures']),'fixtures_expected_result_matched':len(report['fixtures'])-len(bad),'fixtures_mismatched':len(bad),'legacy_fixture_total':len(legacy_idx['fixtures']),'legacy_fixture_mismatches_against_candidate_schemas':len(report['legacy_fixture_compatibility']['mismatches']),'legacy_fixture_index_version':legacy_idx.get('schema_version'),'fixture_index_version':idx.get('schema_version'),'record_types_loaded':len(schemas),'semantic_tests_total':len(report['semantic_tests']),'semantic_tests_expected_result_matched':len(report['semantic_tests'])-len(sem_bad),'semantic_tests_mismatched':len(sem_bad),'trace_rows':len(rows)}
 validation_status='passed' if report['summary']['checks_failed']==0 and not bad and not sem_bad else 'failed'
 report['provenance']={'validation_status':validation_status,'validated_commit_sha':os.environ.get('SCHEMA_VALIDATED_HEAD_SHA') or os.environ.get('GITHUB_SHA'),'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'workflow_run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),'generated_at_utc':datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z'),'validator_path':'schema/v1.4.3.7/tools/schema-v1.4.3.6-validate.py','validator_sha256':sha(Path(__file__).resolve()),'manifest_sha256':sha(root/'manifest.json'),'traceability_csv_sha256':sha(root/'audit/requirement-test-trace.csv'),'execution_environment':'github_actions' if os.environ.get('GITHUB_ACTIONS')=='true' else 'local'}
 (root/'audit/validation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report['summary'],ensure_ascii=False,indent=2)); return 1 if report['summary']['checks_failed'] or bad or sem_bad else 0
if __name__=='__main__': sys.exit(main(sys.argv[1]))
