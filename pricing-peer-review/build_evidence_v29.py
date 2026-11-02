from pathlib import Path
from copy import deepcopy
from collections import Counter
import json,hashlib
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
pair=lambda q:frozenset((tuple(q['a']),tuple(q['b'])))
def main():
 old=json.loads((R/'evidence-v28.json').read_text());view=deepcopy(json.loads((R/'benchmark-targets-v28.json').read_text()));rows=deepcopy(old['rows']);registry={pair(q):deepcopy(q) for q in old['unresolved_pairs']};index={pair(q):i for i,q in enumerate(rows)};reconciliation=[];guidance=[]
 for file in ('round55-tare-context-isolation.json',):
  d=json.loads((R/file).read_text());assert d['status']=='complete'
  if 'freeze_fields' in d:assert hashlib.sha256(json.dumps([{k:q[k] for k in d['freeze_fields']} for q in d['questions']],sort_keys=True).encode()).hexdigest()==d['questions_and_predictions_sha256']
  for f,h in d['file_sha256'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
  guidance+=d.get('rule_statements',[])
  for q in d['questions']:
   key=pair(q);i=index.get(key);prior=deepcopy(rows[i]) if i is not None else deepcopy(registry.get(key));reverse=prior is not None and q['a']==prior['b'];direction=q['direction']
   if reverse and direction in ('A','B'):direction='B' if direction=='A' else 'A'
   size=q['meaningfulness'];pending=q.get('resolution_status')=='unresolved';material=None if size is None else 'no_meaningful_difference' if size=='no_meaningful_difference' else 'meaningful_'+direction
   row={'id':prior['id'] if prior else q['id'],'a':prior['a'] if prior else q['a'],'b':prior['b'] if prior else q['b'],'winner':direction or ('unresolved' if pending else 'practical_similarity'),'direction':direction,'explicit_materiality':material,'materiality_support':'unspecified' if size is None else 'direct_two_axis_response','strength':q.get('strength'),'raw_answer':q['raw_answer'],'raw_explanation':q.get('raw_explanation'),'contextual_explanation':q.get('contextual_explanation'),'answer_interpretation':q['interpretation'],'answer_history':deepcopy(q.get('answer_history',[])),'exact_price_instruction':False,'status':'unresolved' if pending else 'answered','resolution_status':'unresolved' if pending else 'resolved','explicitly_not_tie':q.get('explicitly_not_tie',False),'practical_tie_statement':q.get('practical_tie_statement',False),'shade_premium_statement':q.get('shade_premium_statement'),'zero_adjacent_shade_premium':bool(q.get('shade_premium_statement') and direction is None),'evidence_source':file,'latest_source_id':q['id']}
   if prior:row['clarification_history']=[*prior.get('clarification_history',[]),{'clarification_id':q['id'],'orientation_reversed':reverse,'original_presented_a':q['a'],'original_presented_b':q['b'],'previous_record':prior}]
   target={'id':row['id'],'a':row['a'],'b':row['b'],'known_direction':1 if direction=='A' else -1 if direction=='B' else None,'materiality_target':None if material is None else 0 if material=='no_meaningful_difference' else 1 if direction=='A' else -1,'strength':row.get('strength'),'basis':'Latest explicit judgment from '+q['id']+'; repeated pair reconciled once, retracted answers excluded'}
   if i is None:index[key]=len(rows);rows.append(row);view['rows'].append(target)
   else:rows[i]=row;view['rows'][i]=target
   if pending:registry[key]=deepcopy(row)
   else:registry.pop(key,None)
   reconciliation.append({'source':q['id'],'canonical_id':row['id'],'action':'supersede' if prior else 'append','orientation_reversed':reverse})
 assert len({pair(q) for q in rows})==len(rows);assert not registry
 sources={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ('evidence-v28.json','benchmark-targets-v28.json','round55-tare-context-isolation.json','build_evidence_v29.py')}
 result={'version':29,'parent':'evidence-v28.json','source_hashes':sources,'rows':rows,'row_count':len(rows),'label_counts':dict(Counter(q['winner'] for q in rows)),'unresolved_pairs':list(registry.values()),'reconciliation':reconciliation,'latest_guidance':guidance,'protocol':'Round55 incorporated by unordered pair. Clarifications supersede original active labels, retain histories and original orientation; Round55-10 removes the old direction without asserting exact equality. Round55 all-top exceptions and raw explanations retained. No missing meaningfulness inferred; positive small premiums are not ties. No duplicate weighting.'}
 write_versioned(R/'evidence-v29.json',result);view.update(evidence='evidence-v29.json',evidence_sha256=hashlib.sha256((R/'evidence-v29.json').read_bytes()).hexdigest(),source_hashes=sources,protocol=result['protocol']);view['materiality_counts']=dict(Counter('unspecified' if q['materiality_target'] is None else 'no_meaningful_difference' if q['materiality_target']==0 else 'meaningful_direct_or_proxy' for q in view['rows']));write_versioned(R/'benchmark-targets-v29.json',view);print(json.dumps({'rows':len(rows),'unresolved':len(registry),'directions':sum(q['known_direction'] is not None for q in view['rows']),'sizes':view['materiality_counts'],'superseded':[q for q in reconciliation if q['action']=='supersede']}))
if __name__=='__main__':main()
