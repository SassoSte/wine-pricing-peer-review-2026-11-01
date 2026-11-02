"""Append Round36's independent direction/size responses; retain frozen receipt."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import hashlib,json
from reconcile_and_compare import write_versioned
ROOT=Path(__file__).resolve().parent

def main():
    names=['evidence-v16.json','benchmark-targets-v16.json','round36-fixed.json','round36-findings.json','build_evidence_v17.py'];hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in names}
    old=json.loads((ROOT/'evidence-v16.json').read_text());view=deepcopy(json.loads((ROOT/'benchmark-targets-v16.json').read_text()));round_=json.loads((ROOT/'round36-fixed.json').read_text());fields=round_['freeze_fields']
    assert hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in round_['questions']],sort_keys=True).encode()).hexdigest()==round_['questions_and_predictions_sha256']
    for f,h in round_['file_sha256'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    assert len(round_['questions'])==12 and all(q['status']=='answered' for q in round_['questions'])
    rows=deepcopy(old['rows']);keys={frozenset((tuple(r['a']),tuple(r['b']))) for r in rows}
    for q in round_['questions']:
        key=frozenset((tuple(q['a']),tuple(q['b'])));assert key not in keys;keys.add(key)
        materiality='no_meaningful_difference' if q['meaningfulness']=='practically_similar' else 'meaningful_'+q['direction'];direction=q['direction'];assert direction in ('A','B')
        rows.append({'id':q['id'],'a':q['a'],'b':q['b'],'winner':direction,'direction':direction,'judgment_type':'strict_preference','explicit_materiality':materiality,'materiality_support':'direct_two_axis_response','strength':'slightly' if materiality=='no_meaningful_difference' else None,'raw_answer':q['raw_answer'],'answer_interpretation':q.get('interpretation'),'exact_price_instruction':q['exact_price_instruction'],'status':'answered','evidence_source':'round36-fixed.json'})
        view['rows'].append({'id':q['id'],'a':q['a'],'b':q['b'],'known_direction':1 if direction=='A' else -1,'materiality_target':0 if materiality=='no_meaningful_difference' else 1 if direction=='A' else -1,'basis':'Direct separate direction and meaningfulness answers in frozen Round36; no size inferred from bare A/B.','strength':'slightly' if materiality=='no_meaningful_difference' else None})
    assert len(rows)==425 and rows[:413]==old['rows']
    evidence={'version':17,'parent':'evidence-v16.json','parent_sha256':hashes['evidence-v16.json'],'row_count':425,'label_counts':dict(Counter(r['winner'] for r in rows)),'source_hashes':hashes,'unresolved_pairs':deepcopy(old['unresolved_pairs']),'round36_guidance':round_['rule_statements'],'frozen_round36_receipt':{'file':'round36-fixed.json','sha256':hashes['round36-fixed.json'],'scope':'Pre-incorporation frozen scores, never rewritten as new-model performance.'},'protocol':'413 parent rows unchanged plus12 unique directly elicited direction/size pairs.10 practical similarities retain known tiny directions;2 meaningful preferences use Q10 final clarification and Q11 explicit response. Negligible domestic golden/pale difference is not literal price equality. Old records at different ages/tares not silently corrected.','rows':rows}
    write_versioned(ROOT/'evidence-v17.json',evidence)
    view.update(evidence='evidence-v17.json',evidence_sha256=hashlib.sha256((ROOT/'evidence-v17.json').read_bytes()).hexdigest(),source_hashes=hashes,protocol='Same partial v16 target view plus12 direct two-axis observations. Existing uncertainty and proxy statuses unchanged. Known directions and practical closeness coexist.')
    view['materiality_counts']=dict(Counter('unspecified' if r['materiality_target'] is None else 'no_meaningful_difference' if r['materiality_target']==0 else 'meaningful_direct_or_proxy' for r in view['rows']))
    write_versioned(ROOT/'benchmark-targets-v17.json',view)
    print(json.dumps({'rows':len(rows),'labels':evidence['label_counts'],'materiality':view['materiality_counts']}))
if __name__=='__main__':main()
