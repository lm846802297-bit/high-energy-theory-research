#!/usr/bin/env python3
"""Minimal JSON Schema candidate-bundle validator; not a cross-record/physics validator."""
import argparse, json, hashlib, sys
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.validators import validator_for

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('bundle',help='Extracted bundle directory')
 ap.add_argument('--output',default='validation-report.json')
 args=ap.parse_args(); root=Path(args.bundle).resolve()
 manifest_path=root/'manifest.json'; idx_path=root/'tests'/'fixture-index.json'
 report={'bundle_root':str(root),'checks':[],'fixture_results':[],'summary':{},'limitations':['No cross-record reference validation','No full state machine/event-chain/checkpoint validation','No migration execution','No physical/scientific correctness validation']}
 def add(name,status,details=None): report['checks'].append({'name':name,'status':status,'details':details or {}})
 try: manifest=json.loads(manifest_path.read_text(encoding='utf-8')); add('manifest_json','PASS')
 except Exception as e: add('manifest_json','FAIL',{'error':str(e)}); manifest={}
 try: idx=json.loads(idx_path.read_text(encoding='utf-8')); add('fixture_index_json','PASS')
 except Exception as e: add('fixture_index_json','FAIL',{'error':str(e)}); idx={'fixtures':[]}
 schemas={}; expected=set(manifest.get('record_types',[])); found=set()
 for rt,entry in manifest.get('schema_files',{}).items():
  p=root/entry.get('path','')
  if not p.is_file(): add('schema_file_exists','FAIL',{'record_type':rt,'path':str(p)}); continue
  if sha(p)!=entry.get('sha256'): add('schema_sha256','FAIL',{'record_type':rt,'expected':entry.get('sha256'),'actual':sha(p)}); continue
  try: sch=json.loads(p.read_text(encoding='utf-8'))
  except Exception as e: add('schema_json','FAIL',{'record_type':rt,'error':str(e)}); continue
  try: Draft202012Validator.check_schema(sch); add('schema_meta_validation','PASS',{'record_type':rt})
  except Exception as e: add('schema_meta_validation','FAIL',{'record_type':rt,'error':str(e)})
  # Check only local JSON Pointer refs; external/network refs are forbidden in this candidate.
  refs=[]
  def walk(x):
   if isinstance(x,dict):
    if '$ref' in x: refs.append(x['$ref'])
    for v in x.values(): walk(v)
   elif isinstance(x,list):
    for v in x: walk(v)
  walk(sch); bad=[]
  for ref in refs:
   if not ref.startswith('#/'):
    bad.append(ref); continue
   cur=sch
   try:
    for part in ref[2:].split('/'):
     part=part.replace('~1','/').replace('~0','~'); cur=cur[part]
   except Exception: bad.append(ref)
  add('local_ref_resolution','FAIL' if bad else 'PASS',{'record_type':rt,'refs':refs,'unresolved_or_external':bad})
  if sch.get('properties',{}).get('record_type',{}).get('const')!=rt: add('record_type_const','FAIL',{'record_type':rt,'const':sch.get('properties',{}).get('record_type',{}).get('const')})
  else: add('record_type_const','PASS',{'record_type':rt})
  schemas[rt]=(p,sch); found.add(rt)
 add('manifest_schema_type_set','PASS' if expected==found else 'FAIL',{'missing':sorted(expected-found),'extra':sorted(found-expected)})
 fixtures=idx.get('fixtures',[])
 for item in fixtures:
  rel=item.get('file',''); p=root/'tests'/rel.removeprefix('tests/') if rel.startswith('tests/') else root/'tests'/rel
  # Index paths are relative to bundle root under tests/; normalize against root.
  p=root/rel if rel.startswith('tests/') else root/'tests'/rel
  rt=item.get('record_type'); expected_result=item.get('expected_schema_result','pass')
  rec={'fixture_id':item.get('fixture_id'),'record_type':rt,'expected':expected_result,'file':rel}
  try:
   obj=json.loads(p.read_text(encoding='utf-8'))
   if rt not in schemas: raise ValueError('no schema for record_type')
   validator=Draft202012Validator(schemas[rt][1],format_checker=FormatChecker())
   errs=sorted(validator.iter_errors(obj),key=lambda e:list(map(str,e.absolute_path)))
   actual='pass' if not errs else 'fail'
   rec.update({'actual':actual,'errors':[{'path':'/'.join(map(str,e.absolute_path)),'message':e.message} for e in errs[:5]]})
   wantpass=expected_result in ('pass','valid','accepted')
   ok=(actual=='pass')==wantpass
   rec['status']='PASS' if ok else 'FAIL'
  except Exception as e: rec.update({'status':'FAIL','actual':'error','errors':[str(e)]})
  report['fixture_results'].append(rec)
 # Schema-only validator deliberately does not evaluate expected_semantic_result.
 report['summary']={'checks_passed':sum(c['status']=='PASS' for c in report['checks']),'checks_failed':sum(c['status']=='FAIL' for c in report['checks']),'fixtures_total':len(report['fixture_results']),'fixtures_passed':sum(f['status']=='PASS' for f in report['fixture_results']),'fixtures_failed':sum(f['status']=='FAIL' for f in report['fixture_results']),'semantic_checks':'NOT_RUN'}
 out=Path(args.output); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report['summary'],ensure_ascii=False,indent=2)); print('report:',out)
 return 1 if report['summary']['checks_failed'] or report['summary']['fixtures_failed'] else 0
if __name__=='__main__': sys.exit(main())
