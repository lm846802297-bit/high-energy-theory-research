#!/usr/bin/env python3
import json,hashlib,sys,csv
from pathlib import Path
from jsonschema import Draft202012Validator,FormatChecker
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(root):
 root=Path(root);r={'checks':[],'fixtures':[],'limitations':['No cross-record semantics','No complete state machine/event ledger','No migration execution','No physics correctness']}
 def add(n,ok,detail=None):r['checks'].append({'name':n,'status':'PASS' if ok else 'FAIL','detail':detail or {}})
 m=json.loads((root/'manifest.json').read_text());idx=json.loads((root/'tests/fixture-index.json').read_text()); schemas={}
 for rt,e in m['schema_files'].items():
  p=root/e['path'];ok=p.exists() and sha(p)==e['sha256'];add('schema_hash:'+rt,ok);
  if ok:
   s=json.loads(p.read_text());
   try: Draft202012Validator.check_schema(s);schemas[rt]=s;add('meta:'+rt,True)
   except Exception as ex: add('meta:'+rt,False,{'error':str(ex)})
 add('record_types_match',set(m['record_types'])==set(schemas))
 add('fixture_index_hash',sha(root/m['fixture_index'])==m['fixture_index_sha256'])
 ids=set()
 for x in idx['fixtures']:
  fid=x['fixture_id'];unique=fid not in ids;ids.add(fid);data=json.loads((root/x['file']).read_text());errs=list(Draft202012Validator(schemas[x['record_type']],format_checker=FormatChecker()).iter_errors(data));actual='pass' if not errs else 'fail';ok=unique and actual==x['expected_schema_result'];r['fixtures'].append({'fixture_id':fid,'expected':x['expected_schema_result'],'actual':actual,'ok':ok,'errors':[e.message for e in errs[:4]]})
 add('fixture_ids_unique',len(ids)==len(idx['fixtures']))
 rows=list(csv.DictReader((root/'audit/requirement-test-trace.csv').open(encoding='utf-8-sig')));req=[x['requirement_id'] for x in rows];tests=[x['test_id'] for x in rows];add('requirement_ids_unique',len(req)==len(set(req)));add('test_ids_unique',len(tests)==len(set(tests)))
 fids={x['fixture_id'] for x in idx['fixtures']};traced={fid for x in rows for fid in x['fixture_ids'].split(';')};add('trace_fixture_refs_valid',traced<=fids,{'dangling':sorted(traced-fids)});add('all_fixtures_traced',fids<=traced,{'untraced':sorted(fids-traced)})
 bad=[x for x in r['fixtures'] if not x['ok']];r['summary']={'checks':len(r['checks']),'checks_passed':sum(x['status']=='PASS' for x in r['checks']),'checks_failed':sum(x['status']=='FAIL' for x in r['checks']),'fixtures':len(r['fixtures']),'fixtures_expected_result_matched':len(r['fixtures'])-len(bad),'fixtures_mismatched':len(bad),'record_types':len(schemas),'trace_rows':len(rows)}
 (root/'audit/validation-report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r['summary'],ensure_ascii=False));return 1 if r['summary']['checks_failed'] or bad else 0
if __name__=='__main__':sys.exit(main(sys.argv[1]))
