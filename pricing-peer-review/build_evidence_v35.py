"""Reconcile twelve frozen-pilot clarifications once; preserve prior snapshots and histories."""
from pathlib import Path
from copy import deepcopy
import json,hashlib
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
key=lambda q:frozenset((tuple(q['a']),tuple(q['b'])))
def main():
 old=json.loads((R/'evidence-v34.json').read_text());view=deepcopy(json.loads((R/'benchmark-targets-v34.json').read_text()));rows=deepcopy(old['rows']);ix={key(q):i for i,q in enumerate(rows)};actions=[]
 sources=['pilot-clarifications-v34.json']
 for source in sources:
  for n,q in enumerate(json.loads((R/source).read_text())['rows']):
   assert not q.get('exclude_from_reconciliation_until_confirmed');k=key(q);i=ix.get(k);prior=deepcopy(rows[i]) if i is not None else None;reverse=prior is not None and q['a']==prior['b'];d=q['known_direction'];d=-d if reverse and d is not None else d;mat=q['materiality_target'];mat=-mat if reverse and mat else mat;exact=q.get('exact_price_equality') is True;cid=q.get('clarification_id',q.get('target_id',str(n)));id=prior['id'] if prior else cid;direction='A' if d==1 else 'B' if d==-1 else None;relation='equal' if exact else 'A_higher' if d==1 else 'B_higher' if d==-1 else 'unspecified'
   row=deepcopy(prior) if prior else {'id':id,'a':q['a'],'b':q['b']};row.update(winner='tie' if exact else direction or 'practical_similarity',direction=direction,explicit_materiality='no_meaningful_difference' if mat==0 else 'meaningful_'+direction,materiality_support='direct_two_axis_response',exact_price_instruction=exact,exact_price_equality=exact,value_relation=relation,status='answered',resolution_status='resolved',raw_answer=q.get('raw_answer',q.get('user_answer',q.get('reasoning'))),raw_explanation=q.get('reasoning'),evidence_source=source,latest_source_id='voice-v35:'+cid,answer_interpretation=deepcopy(q),strength='slight' if d and mat==0 else None)
   row['clarification_history']=[*(prior or {}).get('clarification_history',[]),{'clarification_id':'voice-v35:'+cid,'previous_record':prior,'presented_record':q,'orientation_reversed':reverse}]
   target={'id':id,'a':row['a'],'b':row['b'],'known_direction':d,'materiality_target':mat,'exact_price_equality':exact,'value_relation':relation,'latest_source_id':'voice-v35:'+cid,'basis':'Explicit voice clarification; raw interpretation and tentative qualification retained in evidence.','strength':row['strength']}
   if i is None:ix[k]=len(rows);rows.append(row);view['rows'].append(target)
   else:rows[i]=row;view['rows'][i]=target
   actions.append({'id':id,'action':'supersede' if prior else 'add','source':source,'relation':relation,'materiality_target':mat})
 assert len(rows)==len({key(q) for q in rows});assert [q['id'] for q in rows]==[q['id'] for q in view['rows']]
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['evidence-v34.json','benchmark-targets-v34.json',*sources,'build_evidence_v35.py']}
 out=deepcopy(old);out.update(version=35,parent='evidence-v34.json',rows=rows,row_count=len(rows),source_hashes=hashes,reconciliation=actions,protocol='Twelve frozen-pilot clarifications deduplicated by unordered pair. Exact equality, practical similarity without direction, slight direction and meaningful direction separate. No inferred blanket exchange rate. Prior records preserved.')
 from collections import Counter
 out['label_counts']=dict(Counter(q['winner'] for q in rows));write_versioned(R/'evidence-v35.json',out);view.update(evidence='evidence-v35.json',evidence_sha256=hashlib.sha256((R/'evidence-v35.json').read_bytes()).hexdigest(),source_hashes=hashes,exact_equality_ids=[q['id'] for q in view['rows'] if q.get('exact_price_equality') is True],protocol=out['protocol']);view['materiality_counts']=dict(Counter('unspecified' if q['materiality_target'] is None else 'nonmeaningful' if q['materiality_target']==0 else 'meaningful' for q in view['rows']));write_versioned(R/'benchmark-targets-v35.json',view);print(json.dumps(actions,indent=2));print('Rows',len(rows))
if __name__=='__main__':main()
