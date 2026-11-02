from pathlib import Path
from copy import deepcopy
from collections import Counter
import json,hashlib
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
key=lambda q:frozenset((tuple(q['a']),tuple(q['b'])))
def main():
 old=json.loads((R/'evidence-v30.json').read_text());view=deepcopy(json.loads((R/'benchmark-targets-v30.json').read_text()));review=json.loads((R/'round57-consistent-misses-review.json').read_text());assert review['status']=='complete';fields=review['freeze_fields'];assert hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in review['questions']],sort_keys=True).encode()).hexdigest()==review['questions_sha256']
 for f,h in review['file_sha256'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 rows=deepcopy(old['rows']);index={key(q):i for i,q in enumerate(rows)};reconciled=[]
 for q in view['rows']:
  q['exact_price_equality']=None;q['value_relation']='A_higher' if q['known_direction']==1 else 'B_higher' if q['known_direction']==-1 else 'unspecified'
 for q in review['questions']:
  assert q['status']=='answered' and q['evidence_reconciliation_ready'];i=index[key(q)];prior=deepcopy(rows[i]);assert prior['id']==q['source_id'];reverse=q['a']==prior['b'];direction=q['direction']
  if reverse and direction in ('A','B'):direction='B' if direction=='A' else 'A'
  exact=bool(q.get('exact_price_instruction'));material=0 if q['meaningfulness']=='no_meaningful_difference' else 1 if direction=='A' else -1;relation='equal' if exact else 'A_higher' if direction=='A' else 'B_higher' if direction=='B' else 'unspecified'
  row=deepcopy(prior);row.update(winner='tie' if exact else direction or 'practical_similarity',direction=direction,explicit_materiality='no_meaningful_difference' if material==0 else 'meaningful_'+direction,materiality_support='direct_two_axis_response',strength=q.get('strength'),judgment_type=q['judgment_type'],exact_price_instruction=exact,exact_price_equality=True if exact else None,value_relation=relation,explicitly_not_tie=q.get('explicitly_not_tie',False),status='answered',resolution_status='resolved',raw_answer=q['raw_answer'],raw_explanation=q.get('raw_explanation'),answer_history=deepcopy(q.get('answer_history',[])),answer_interpretation=q['interpretation'],evidence_source='round57-consistent-misses-review.json',latest_source_id=q['id'])
  for name in ('inventory_qualification','meaningfulness_basis','selected_option_text'):
   if name in q:row[name]=deepcopy(q[name])
  row['clarification_history']=[*prior.get('clarification_history',[]),{'clarification_id':q['id'],'orientation_reversed':reverse,'original_presented_a':q['a'],'original_presented_b':q['b'],'previous_record':prior}];rows[i]=row
  view['rows'][i]={'id':row['id'],'a':row['a'],'b':row['b'],'known_direction':1 if direction=='A' else -1 if direction=='B' else None,'materiality_target':material,'strength':q.get('strength'),'exact_price_equality':True if exact else None,'value_relation':relation,'latest_source_id':q['id'],'basis':'Round57 clarification replaces prior active judgment once. Exact equality distinct from practical similarity and missing direction. '+q.get('meaningfulness_basis','')}
  reconciled.append({'case':q['number'],'source_id':q['id'],'canonical_id':row['id'],'action':'supersede','orientation_reversed':reverse,'relation':relation})
 assert len(rows)==640 and len({key(q) for q in rows})==640;assert [q['id'] for q in rows]==[q['id'] for q in view['rows']];assert sum(q['exact_price_equality'] is True for q in view['rows'])==3
 sources={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ('evidence-v30.json','benchmark-targets-v30.json','round57-consistent-misses-review.json','build_evidence_v31.py')}
 protocol='All18Round57reviews supersede existing unorderedpairs,not appended orduplicateweighted. Rawexplanations,answerhistories,inventoryqualification andinterpretationbasis preserved. Exactties only the3newexplicitabsoluteprice confirmations; historicalcoarsenedties notautomaticallyupgraded. Smallpositive directions remainstrict withnonmeaningfulsize. Practicalnondirection remainsunspecified relation. No unresolvedlabels invented.'
 out={'version':31,'parent':'evidence-v30.json','source_hashes':sources,'rows':rows,'row_count':len(rows),'label_counts':dict(Counter(q['winner'] for q in rows)),'unresolved_pairs':deepcopy(old['unresolved_pairs']),'reconciliation':reconciled,'latest_guidance':review['rule_statements'],'protocol':protocol}
 write_versioned(R/'evidence-v31.json',out);view.update(evidence='evidence-v31.json',evidence_sha256=hashlib.sha256((R/'evidence-v31.json').read_bytes()).hexdigest(),source_hashes=sources,protocol=protocol,exact_equality_ids=[q['id'] for q in view['rows'] if q['exact_price_equality'] is True]);view['materiality_counts']=dict(Counter('unspecified' if q['materiality_target'] is None else 'nonmeaningful' if q['materiality_target']==0 else 'meaningful' for q in view['rows']));write_versioned(R/'benchmark-targets-v31.json',view)
 print(json.dumps({'rows':len(rows),'strict_directions':sum(q['known_direction'] is not None for q in view['rows']),'exact_ties':view['exact_equality_ids'],'sizes':view['materiality_counts'],'reconciled':len(reconciled)},indent=2))
if __name__=='__main__':main()
