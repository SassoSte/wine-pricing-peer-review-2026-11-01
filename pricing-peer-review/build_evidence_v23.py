from pathlib import Path
from copy import deepcopy
import json,hashlib
from collections import Counter
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
def main():
 old=json.loads((R/'evidence-v22.json').read_text());view=deepcopy(json.loads((R/'benchmark-targets-v22.json').read_text()));d=json.loads((R/'round42-fixed.json').read_text());fields=d['freeze_fields'];assert hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in d['questions']],sort_keys=True).encode()).hexdigest()==d['questions_and_predictions_sha256']
 for f,h in d['file_sha256'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 rows=deepcopy(old['rows']);unresolved=deepcopy(old['unresolved_pairs'])
 for q in d['questions']:
  direction=q['direction'];size=q['meaningfulness'];pending=q.get('resolution_status')=='unresolved';target=None if size is None else 0 if size=='no_meaningful_difference' else 1 if direction=='A' else -1
  row={'id':q['id'],'a':q['a'],'b':q['b'],'winner':direction or ('unresolved' if pending else 'practical_similarity'),'direction':direction,'explicit_materiality':None if size is None else 'no_meaningful_difference' if target==0 else 'meaningful_'+direction,'materiality_support':'unspecified' if size is None else 'direct_two_axis_response','strength':None,'raw_answer':q['raw_answer'],'raw_clarification':q.get('raw_clarification'),'answer_interpretation':q['interpretation'],'exact_price_instruction':False,'status':'unresolved' if pending else 'answered','resolution_status':q.get('resolution_status','resolved'),'explicitly_not_tie':q.get('explicitly_not_tie',False),'shade_premium_statement':q.get('shade_premium_statement'),'zero_adjacent_shade_premium':bool(q.get('shade_premium_statement') and direction is None),'evidence_source':'round42-fixed.json'}
  rows.append(row)
  if pending:unresolved.append(deepcopy(row))
  view['rows'].append({'id':q['id'],'a':q['a'],'b':q['b'],'known_direction':1 if direction=='A' else -1 if direction=='B' else None,'materiality_target':target,'basis':'Explicit unresolved, no labels inferred' if pending else 'Round42 explicit axes','strength':None})
 assert rows[:479]==old['rows'];assert [q['number'] for q in d['questions'] if q.get('resolution_status')=='unresolved']==[3,10,12]
 sources={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ('evidence-v22.json','benchmark-targets-v22.json','round42-fixed.json','build_evidence_v23.py')}
 result={'version':23,'parent':'evidence-v22.json','source_hashes':sources,'rows':rows,'row_count':len(rows),'label_counts':dict(Counter(q['winner'] for q in rows)),'unresolved_pairs':unresolved,'round42_guidance':d['rule_statements'],'protocol':'All479 parent rows unchanged;12 Round42 records appended. Q3/10/12 explicitly unresolved on both axes, retained with explanations and in unresolved registry, no tie/practical/meaningful labels inferred. Previous EasternEurope correction and unresolved pairs retained.'}
 write_versioned(R/'evidence-v23.json',result);view.update(evidence='evidence-v23.json',evidence_sha256=hashlib.sha256((R/'evidence-v23.json').read_bytes()).hexdigest(),source_hashes=sources,protocol=result['protocol']);view['materiality_counts']=dict(Counter('unspecified' if q['materiality_target'] is None else 'no_meaningful_difference' if q['materiality_target']==0 else 'meaningful_direct_or_proxy' for q in view['rows']));write_versioned(R/'benchmark-targets-v23.json',view);print(view['materiality_counts'])
if __name__=='__main__':main()
