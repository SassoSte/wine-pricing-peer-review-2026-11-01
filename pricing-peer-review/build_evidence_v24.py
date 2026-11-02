from pathlib import Path
from copy import deepcopy
import json,hashlib
from reconcile_and_compare import write_versioned
from collections import Counter
R=Path(__file__).resolve().parent
def main():
 old=json.loads((R/'evidence-v23.json').read_text());view=deepcopy(json.loads((R/'benchmark-targets-v23.json').read_text()));d=json.loads((R/'round43-fixed.json').read_text());fields=d['freeze_fields'];assert hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in d['questions']],sort_keys=True).encode()).hexdigest()==d['questions_and_predictions_sha256']
 for f,h in d['file_sha256'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 rows=deepcopy(old['rows']);ix={q['id']:i for i,q in enumerate(rows)}
 for q in d['questions']:
  i=ix[q['revisits']];row=rows[i];assert row['a']==q['a'] and row['b']==q['b'];previous=deepcopy(row);direction=q['direction'];assert q['meaningfulness']=='meaningful_difference'
  row.update(winner=direction,direction=direction,strength=None,explicit_materiality='meaningful_'+direction,materiality_support='direct_two_axis_response',raw_answer=q['raw_answer'],answer_interpretation=q['interpretation'],clarified_by=q['id'],judgment_type='strict_preference',status='answered',clarification_history=[*row.get('clarification_history',[]),{'clarification_file':'round43-fixed.json','clarification_id':q['id'],'previous_record':previous}])
  view['rows'][i].update(known_direction=1 if direction=='A' else -1,materiality_target=1 if direction=='A' else -1,strength=None,basis='Explicit neutral115lb revisit '+q['id']+' supersedes active answer, history retained; no duplicate pair added')
 # Record decomposition, not inferred answers, for unresolved mixed comparisons.
 analysis={
 'round42-3':{'a_advantage':'Five-year younger vintage','b_advantage':'10lb lower tare; foreign premium provenance versus premium domestic provenance','crux':'Whether5-year age advantage offsets10lb tare difference plus the cross-provenance tradeoff. The two115lb clarifications hold provenance and tare equal and do not answer this.','still_missing':'Net comparison of this combined tradeoff; user called it very close without selecting either axis.'},
 'round42-10':{'a_advantage':'Northeast provenance advantage and5lb lower tare','b_advantage':'Five-year younger vintage','crux':'Size of Northeast/Northwest provenance premium relative to the remaining vintage advantage after tare. Pure5lb insignificance does not imply it is irrelevant when combined with provenance.','still_missing':'Net winner and meaningfulness; user explicitly said not a tie.'},
 'round42-12':{'a_advantage':'Five-year younger vintage','b_advantage':'Lighter amber versus copper shade and10lb lower tare','crux':'Age-versus10lb tare plus copper/amber shade tradeoff. The golden/pale clarification does not establish copper/amber equivalence.','still_missing':'Net winner and meaningfulness; user explicitly requested unresolved, not tied.'}}
 seen={frozenset((tuple(q['a']),tuple(q['b']))):q for q in rows if q.get('winner')!='unresolved'}
 for id,audit in analysis.items():
  row=rows[ix[id]];assert row['direction'] is None and row['explicit_materiality'] is None;audit.update(status='unresolved',no_label_inferred=True,raw_answer=row['raw_answer'],raw_clarification=row.get('raw_clarification'));hits=[]
  for side in ('a','b'):
   anchor=row[side];other=row['b' if side=='a' else 'a']
   for col,name in enumerate(('provenance','shade','vintage','tare')):
    if anchor[col]==other[col]:continue
    changed=anchor.copy();changed[col]=other[col];match=seen.get(frozenset((tuple(anchor),tuple(changed))))
    if match:hits.append({'attribute':name,'anchor_side':side,'evidence_id':match['id'],'a':match['a'],'b':match['b'],'winner':match.get('winner'),'explicit_materiality':match.get('explicit_materiality')})
  audit['existing_exact_one_factor_controls']=hits
 sources={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ('evidence-v23.json','benchmark-targets-v23.json','round43-fixed.json','round42-fixed.json','build_evidence_v24.py')}
 changed=[a['id'] for a,b in zip(rows,old['rows']) if a!=b];assert set(changed)=={'round36-9','round36-12'}
 result={'version':24,'parent':'evidence-v23.json','source_hashes':sources,'rows':rows,'row_count':len(rows),'label_counts':dict(Counter(q['winner'] for q in rows)),'unresolved_pairs':deepcopy(old['unresolved_pairs']),'unresolved_isolation_analysis':analysis,'clarifications':[{'id':q['id'],'supersedes':q['revisits']} for q in d['questions']],'protocol':'491 rows unchanged in count. Two neutral115lb revisits supersede active labels in-place with historical records retained, no duplicate weighting. Q42-3/10/12 decomposed using existing evidence but remain unresolved on both axes; no questionnaire, no guessed labels. Other489 active rows unchanged.'}
 write_versioned(R/'evidence-v24.json',result);view.update(evidence='evidence-v24.json',evidence_sha256=hashlib.sha256((R/'evidence-v24.json').read_bytes()).hexdigest(),source_hashes=sources,protocol=result['protocol']);view['materiality_counts']=dict(Counter('unspecified' if q['materiality_target'] is None else 'no_meaningful_difference' if q['materiality_target']==0 else 'meaningful_direct_or_proxy' for q in view['rows']));write_versioned(R/'benchmark-targets-v24.json',view);write_versioned(R/'unresolved-isolation-v24.json',analysis);print(json.dumps({'counts':view['materiality_counts'],'one_factor_controls':{id:len(a['existing_exact_one_factor_controls']) for id,a in analysis.items()}}))
if __name__=='__main__':main()
