from pathlib import Path
import json,hashlib,copy
from collections import Counter
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent

def main():
 old=json.loads((R/'evidence-v19.json').read_text());view=copy.deepcopy(json.loads((R/'benchmark-targets-v19.json').read_text()));round=json.loads((R/'round39-fixed.json').read_text());rows=copy.deepcopy(old['rows'])
 assert hashlib.sha256(json.dumps([{k:q[k] for k in round['freeze_fields']} for q in round['questions']],sort_keys=True).encode()).hexdigest()==round['questions_and_predictions_sha256']
 for f,h in round['file_sha256'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 for q in round['questions']:
  direction=q['direction'];size=q['meaningfulness'];qualified=q.get('materiality_support')=='strength_qualified_response';target=None if size is None else 0 if size=='no_meaningful_difference' else 1 if direction=='A' else -1
  row={'id':q['id'],'a':q['a'],'b':q['b'],'winner':direction or ('practical_similarity' if size=='no_meaningful_difference' else 'unresolved'),'direction':direction,'explicit_materiality':None if qualified or size is None else ('meaningful_'+direction if target else 'no_meaningful_difference'),'materiality_support':'strength_qualified_response' if qualified else 'unspecified' if size is None else 'direct_two_axis_response','strength':q.get('strength'),'raw_answer':q['raw_answer'],'answer_interpretation':q['interpretation'],'exact_price_instruction':False,'status':'answered','evidence_source':'round39-fixed.json'}
  rows.append(row);view['rows'].append({'id':q['id'],'a':q['a'],'b':q['b'],'known_direction':1 if direction=='A' else -1 if direction=='B' else None,'materiality_target':target,'basis':'Strength-derived meaningfulness from strongly' if qualified else 'Round39 explicit axes; missing axes remain missing','strength':q.get('strength')})
 sources={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['evidence-v19.json','benchmark-targets-v19.json','round39-fixed.json','build_evidence_v20.py']}
 result={'version':20,'parent':'evidence-v19.json','source_hashes':sources,'rows':rows,'row_count':len(rows),'label_counts':dict(Counter(q['winner'] for q in rows)),'unresolved_pairs':old['unresolved_pairs'],'round39_guidance':round['rule_statements'],'protocol':'All449 parent rows unchanged;6 explicit two-axis Round39 isolation judgments added. Missing and qualifier-derived prior labels preserved; no prior answers overwritten.'}
 write_versioned(R/'evidence-v20.json',result);view.update(evidence='evidence-v20.json',evidence_sha256=hashlib.sha256((R/'evidence-v20.json').read_bytes()).hexdigest(),source_hashes=sources,protocol=result['protocol']);view['materiality_counts']=dict(Counter('unspecified' if q['materiality_target'] is None else 'no_meaningful_difference' if q['materiality_target']==0 else 'meaningful_direct_or_proxy' for q in view['rows']));write_versioned(R/'benchmark-targets-v20.json',view);print(view['materiality_counts'])
if __name__=='__main__':main()
