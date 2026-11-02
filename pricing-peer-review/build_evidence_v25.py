from pathlib import Path
from copy import deepcopy
from collections import Counter
import json,hashlib
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
def main():
 old=json.loads((R/'evidence-v24.json').read_text());view=deepcopy(json.loads((R/'benchmark-targets-v24.json').read_text()));rows=deepcopy(old['rows']);unresolved=deepcopy(old['unresolved_pairs']);guidance=[]
 for file in ('round44-fixed.json','round45-fixed.json'):
  d=json.loads((R/file).read_text());assert d['status']=='complete';assert hashlib.sha256(json.dumps([{k:q[k] for k in d['freeze_fields']} for q in d['questions']],sort_keys=True).encode()).hexdigest()==d['questions_and_predictions_sha256']
  for f,h in d['file_sha256'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
  guidance.extend(d['rule_statements'])
  for q in d['questions']:
   direction=q['direction'];size=q['meaningfulness'];pending=q.get('resolution_status')=='unresolved';target=None if size is None else 0 if size=='no_meaningful_difference' else 1 if direction=='A' else -1
   row={'id':q['id'],'a':q['a'],'b':q['b'],'winner':direction or ('unresolved' if pending else 'practical_similarity'),'direction':direction,'explicit_materiality':None if size is None else 'no_meaningful_difference' if target==0 else 'meaningful_'+direction,'materiality_support':'unspecified' if size is None else 'direct_two_axis_response','strength':q.get('strength'),'raw_answer':q['raw_answer'],'answer_interpretation':q['interpretation'],'exact_price_instruction':False,'status':'unresolved' if pending else 'answered','resolution_status':q.get('resolution_status','resolved'),'explicitly_not_tie':q.get('explicitly_not_tie',False),'practical_tie_statement':q.get('practical_tie_statement',False),'shade_premium_statement':q.get('shade_premium_statement'),'zero_adjacent_shade_premium':bool(q.get('shade_premium_statement') and direction is None),'evidence_source':file}
   rows.append(row)
   if pending:unresolved.append(deepcopy(row))
   view['rows'].append({'id':q['id'],'a':q['a'],'b':q['b'],'known_direction':1 if direction=='A' else -1 if direction=='B' else None,'materiality_target':target,'strength':q.get('strength'),'basis':'Explicit unresolved, no label inferred' if pending else 'Explicit axes from '+file+'; slightly alone remains size-unspecified'})
 assert rows[:491]==old['rows'];sources={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ('evidence-v24.json','benchmark-targets-v24.json','round44-fixed.json','round45-fixed.json','build_evidence_v25.py')}
 result={'version':25,'parent':'evidence-v24.json','source_hashes':sources,'rows':rows,'row_count':len(rows),'label_counts':dict(Counter(q['winner'] for q in rows)),'unresolved_pairs':unresolved,'unresolved_isolation_analysis':deepcopy(old.get('unresolved_isolation_analysis',{})),'round44_45_guidance':guidance,'protocol':'491 parent rows unchanged;32 records appended from Rounds44/45. Round45-Q12 unresolved on both axes;Q1/Q2 direction-only with slightly qualifier, no size inferred. Prior clarifications/history/unresolved records unchanged.'}
 write_versioned(R/'evidence-v25.json',result);view.update(evidence='evidence-v25.json',evidence_sha256=hashlib.sha256((R/'evidence-v25.json').read_bytes()).hexdigest(),source_hashes=sources,protocol=result['protocol']);view['materiality_counts']=dict(Counter('unspecified' if q['materiality_target'] is None else 'no_meaningful_difference' if q['materiality_target']==0 else 'meaningful_direct_or_proxy' for q in view['rows']));write_versioned(R/'benchmark-targets-v25.json',view);print(len(rows),view['materiality_counts'])
if __name__=='__main__':main()
