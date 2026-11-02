"""Append clarified Round37, preserving missing directions and frozen scores."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import hashlib,json
from reconcile_and_compare import write_versioned
ROOT=Path(__file__).resolve().parent

def main():
    files=['evidence-v17.json','benchmark-targets-v17.json','round37-fixed.json','round37-findings.json','build_evidence_v18.py'];hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}
    parent=json.loads((ROOT/'evidence-v17.json').read_text());view=deepcopy(json.loads((ROOT/'benchmark-targets-v17.json').read_text()));d=json.loads((ROOT/'round37-fixed.json').read_text());fields=d['freeze_fields']
    assert hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in d['questions']],sort_keys=True).encode()).hexdigest()==d['questions_and_predictions_sha256']
    for f,h in d['file_sha256'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    assert all(q['status']=='answered' for q in d['questions']) and all(c['status']=='answered' for c in d['post_round_clarifications'])
    rows=deepcopy(parent['rows']);seen={frozenset((tuple(r['a']),tuple(r['b']))) for r in rows}
    for q in d['questions']:
        key=frozenset((tuple(q['a']),tuple(q['b'])));assert key not in seen;seen.add(key)
        direction=q['direction'];meaningful=q['meaningfulness']=='meaningful_difference';assert not meaningful or direction in ('A','B')
        winner=direction if direction in ('A','B') else 'practical_similarity';materiality='meaningful_'+direction if meaningful else 'no_meaningful_difference'
        row={'id':q['id'],'a':q['a'],'b':q['b'],'winner':winner,'direction':direction,'judgment_type':'strict_preference' if direction else 'practical_similarity','explicit_materiality':materiality,'materiality_support':'direct_two_axis_response','strength':'slightly' if direction and not meaningful else None,'raw_answer':q['raw_answer'],'answer_history':q.get('answer_history',[]),'clarified_by':q.get('clarified_by'),'answer_interpretation':q.get('interpretation'),'exact_price_instruction':q['exact_price_instruction'],'status':'answered','evidence_source':'round37-fixed.json'}
        rows.append(row);view['rows'].append({'id':q['id'],'a':q['a'],'b':q['b'],'known_direction':1 if direction=='A' else -1 if direction=='B' else None,'materiality_target':1 if meaningful and direction=='A' else -1 if meaningful else 0,'basis':'Explicit Round37 size, including Q2/Q9 clarifications. No clear direction stays missing; not an equality or guessed winner.','strength':row['strength']})
    assert len(rows)==437 and rows[:425]==parent['rows'];assert Counter(r['winner'] for r in rows)=={'A':193,'B':95,'tie':109,'practical_similarity':40}
    evidence={'version':18,'parent':'evidence-v17.json','parent_sha256':hashes['evidence-v17.json'],'row_count':437,'label_counts':dict(Counter(r['winner'] for r in rows)),'source_hashes':hashes,'unresolved_pairs':deepcopy(parent['unresolved_pairs']),'round37_guidance':d['rule_statements'],'frozen_round37_receipt':{'file':'round37-fixed.json','sha256':hashes['round37-fixed.json'],'note':'Final clarified score unchanged; initial incomplete-axis receipt also preserved.'},'protocol':'425 parent rows unchanged +12 unique pairs:6 explicit directions,6 missing directions;5 meaningful,7 practical. Q2/Q9 size clarifications included. No clear direction is not exact equality or unresolved size. Older conflicting contexts not relabeled.','rows':rows}
    write_versioned(ROOT/'evidence-v18.json',evidence)
    view.update(evidence='evidence-v18.json',evidence_sha256=hashlib.sha256((ROOT/'evidence-v18.json').read_bytes()).hexdigest(),source_hashes=hashes,protocol='v17 partial targets unchanged;12 clarified Round37 size targets added. Missing directions remain None. Exact equality, practical similarity and unresolved remain distinct in evidence.')
    view['materiality_counts']=dict(Counter('unspecified' if r['materiality_target'] is None else 'no_meaningful_difference' if r['materiality_target']==0 else 'meaningful_direct_or_proxy' for r in view['rows']))
    write_versioned(ROOT/'benchmark-targets-v18.json',view)
    print(json.dumps({'rows':len(rows),'labels':evidence['label_counts'],'materiality':view['materiality_counts']}))
if __name__=='__main__':main()
