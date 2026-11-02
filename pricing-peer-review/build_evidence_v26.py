from pathlib import Path
from copy import deepcopy
from collections import Counter
import json,hashlib
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent

def check(file):
 d=json.loads((R/file).read_text());assert d['status']=='complete';assert hashlib.sha256(json.dumps([{k:q[k] for k in d['freeze_fields']} for q in d['questions']],sort_keys=True).encode()).hexdigest()==d['questions_and_predictions_sha256']
 for f,h in d['file_sha256'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 return d

def row_from(q,file,id=None):
 direction=q['direction'];size=q['meaningfulness'];pending=q.get('resolution_status')=='unresolved'
 return {'id':id or q['id'],'a':q['a'],'b':q['b'],'winner':direction or ('unresolved' if pending else 'practical_similarity'),'direction':direction,'explicit_materiality':None if size is None else 'no_meaningful_difference' if size=='no_meaningful_difference' else 'meaningful_'+direction,'materiality_support':'unspecified' if size is None else 'direct_two_axis_response','strength':q.get('strength'),'raw_answer':q['raw_answer'],'answer_interpretation':q['interpretation'],'exact_price_instruction':False,'status':'unresolved' if pending else 'answered','resolution_status':'unresolved' if pending else 'resolved','explicitly_not_tie':q.get('explicitly_not_tie',False),'practical_tie_statement':q.get('practical_tie_statement',False),'shade_premium_statement':q.get('shade_premium_statement'),'zero_adjacent_shade_premium':bool(q.get('shade_premium_statement') and direction is None),'evidence_source':file}

def target(row):
 material=row['explicit_materiality'];direction=row['direction'];return {'id':row['id'],'a':row['a'],'b':row['b'],'known_direction':1 if direction=='A' else -1 if direction=='B' else None,'materiality_target':None if material is None else 0 if material=='no_meaningful_difference' else 1 if material=='meaningful_A' else -1,'strength':row.get('strength'),'basis':'Explicit supplied axes; unresolved is not tie, no missing size inferred. Source '+row['evidence_source']}

def main():
 old=json.loads((R/'evidence-v25.json').read_text());view=deepcopy(json.loads((R/'benchmark-targets-v25.json').read_text()));rows=deepcopy(old['rows']);registry={q['id']:deepcopy(q) for q in old['unresolved_pairs']};guidance=[]
 for file in ('round46-fixed.json','round47-fixed.json'):
  d=check(file);guidance+=d['rule_statements']
  for q in d['questions']:
   row=row_from(q,file);rows.append(row);view['rows'].append(target(row))
   if row['status']=='unresolved':registry[row['id']]=deepcopy(row)
 ix={q['id']:i for i,q in enumerate(rows)};revisit=check('round48-fixed.json');guidance+=revisit['rule_statements']
 for q in revisit['questions']:
  id=q['revisits'];prior=deepcopy(rows[ix[id]] if id in ix else registry[id]);row=row_from(q,'round48-fixed.json',id);assert row['a']==prior['a'] and row['b']==prior['b'];row.update(clarified_by=q['id'],clarification_history=[*prior.get('clarification_history',[]),{'clarification_id':q['id'],'previous_record':prior}])
  if id in ix:rows[ix[id]]=row;view['rows'][ix[id]]=target(row)
  elif row['status']!='unresolved':ix[id]=len(rows);rows.append(row);view['rows'].append(target(row))
  if row['status']=='unresolved':registry[id]=deepcopy(row)
  else:registry.pop(id,None)
 assert len(registry)==8;assert all(q['direction'] is None and q['explicit_materiality'] is None and q['explicitly_not_tie'] for q in registry.values())
 sources={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ('evidence-v25.json','benchmark-targets-v25.json','round46-fixed.json','round47-fixed.json','round48-fixed.json','build_evidence_v26.py')}
 result={'version':26,'parent':'evidence-v25.json','source_hashes':sources,'rows':rows,'row_count':len(rows),'label_counts':dict(Counter(q['winner'] for q in rows)),'unresolved_pairs':list(registry.values()),'latest_guidance':guidance,'clarifications':[{'id':q['id'],'supersedes':q['revisits']} for q in revisit['questions']],'protocol':'Rounds46/47 appended;Round48 reconciles original source pairs in-place with prior records retained, no duplicate weighting. Eight unresolved pairs kept in separate registry, seven also appear as entirely unlabelled rows; legacy round27-11 remains registry-only. round27-7 now Blean/direction-only and added once; round38-3 now practical/no direction. Missing size labels remain missing. Frozen old evidence/models unchanged.'}
 write_versioned(R/'evidence-v26.json',result);view.update(evidence='evidence-v26.json',evidence_sha256=hashlib.sha256((R/'evidence-v26.json').read_bytes()).hexdigest(),source_hashes=sources,protocol=result['protocol']);view['materiality_counts']=dict(Counter('unspecified' if q['materiality_target'] is None else 'no_meaningful_difference' if q['materiality_target']==0 else 'meaningful_direct_or_proxy' for q in view['rows']));write_versioned(R/'benchmark-targets-v26.json',view);print(json.dumps({'rows':len(rows),'unresolved':len(registry),'directions':sum(q['known_direction'] is not None for q in view['rows']),'sizes':view['materiality_counts']}))
if __name__=='__main__':main()
