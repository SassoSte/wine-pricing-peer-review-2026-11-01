"""Separate recorded directions from unconfirmed magnitude; preserve all baselines."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import hashlib,json,re
import numpy as np
import compare_models as base
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent
TARGETS=('round35-4','round35-6','round35-9')


def contributions(row,beta):
    v=(base.features(row['a'])-base.features(row['b']))*np.asarray(beta)
    return {'provenance':float(sum(v[:9])),'shade':float(sum(v[9:13])),'vintage':float(sum(v[13:17])),'tare':float(v[17]),'total':float(sum(v))}


def main():
    files=['evidence-v15.json','benchmark-targets-v15.json','meaningful-benchmark-v13.json','meaningful-benchmark-v15.json','round35-fixed.json','compare_models.py','resolve_mixed_misses.py']
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}
    parent=json.loads((ROOT/'evidence-v15.json').read_text());view=json.loads((ROOT/'benchmark-targets-v15.json').read_text());frozen=json.loads((ROOT/'meaningful-benchmark-v13.json').read_text());current=json.loads((ROOT/'meaningful-benchmark-v15.json').read_text());round_=json.loads((ROOT/'round35-fixed.json').read_text())
    rows=deepcopy(parent['rows']);byid={r['id']:r for r in rows};newview=deepcopy(view);tv={r['id']:r for r in newview['rows']};audit=[]
    # Apply one provenance rule to the entire round, not just model misses.
    # Strong verbal qualification and explicit similarity survive; an A/B choice
    # without independent magnitude wording remains a directional observation.
    for q in round_['questions']:
        row=byid[q['id']]
        if row.get('explicit_materiality') not in ('meaningful_A','meaningful_B'):continue
        raw=q['raw_answer'];lower=raw.lower()
        strong=any(t in lower for t in ['by a long shot','long shot','lonf ahor','meaningful premium','substantial','overwhelming','strongly','moderately'])
        if strong:continue
        previous=deepcopy(row);prior_materiality=row['explicit_materiality']
        row['explicit_materiality']=None
        row['prompt_inferred_materiality']=prior_materiality
        row['materiality_assertion_audit']={'source':'Round35 raw response and subsequent round35-3 clarification','raw_answer':raw,'finding':'Direction selected; size was inferred from question wording, not independently stated. Meaningful premium remains possible, not disproven.','prior_materiality':prior_materiality,'prior_row':previous,'action':'Keep direction, retain prior contextual interpretation as tentative metadata, mark size unconfirmed. Do not relabel practical similarity or exact equality.'}
        tv[q['id']]['materiality_target']=None;tv[q['id']]['basis']='direction confirmed; materiality inferred from prompt but unconfirmed in response; prior interpretation retained in evidence, not a verified magnitude target'
        audit.append({'id':q['id'],'raw_answer':raw,'direction_retained':row['direction'],'previous_materiality':prior_materiality,'current_materiality':'unconfirmed'})
    assert len(audit)==9
    ev={'version':16,'parent':'evidence-v15.json','parent_sha256':hashes['evidence-v15.json'],'row_count':len(rows),'label_counts':parent['label_counts'],'source_hashes':hashes,'unresolved_pairs':deepcopy(parent['unresolved_pairs']),'materiality_assertion_audit':audit,'protocol':'No user direction, tie, practical-similarity or unresolved label changed. Nine Round35 magnitude interpretations demoted from explicit to unconfirmed because response text supplies no independent size statement; prior prompt-based interpretations preserved. Uniform whole-round rule, not outcome-driven relabeling. The long-shot answer and two practical-similarity judgments remain. No new questions or refit.','rows':rows}
    write_versioned(ROOT/'evidence-v16.json',ev)
    newview.update(evidence='evidence-v16.json',evidence_sha256=hashlib.sha256((ROOT/'evidence-v16.json').read_bytes()).hexdigest(),source_hashes=hashes,protocol='Direction-only evidence retained; unconfirmed prompt-inferred magnitude omitted from supervised materiality targets, not changed to similarity. This is a confidence/provenance correction, not a claim the original meaningful interpretation was false.')
    newview['materiality_counts']=dict(Counter('unspecified' if r['materiality_target'] is None else 'no_meaningful_difference' if r['materiality_target']==0 else 'meaningful_direct_or_proxy' for r in newview['rows']))
    write_versioned(ROOT/'benchmark-targets-v16.json',newview)
    cases=[]
    for ident in TARGETS:
        r=byid[ident];old=contributions(r,frozen['coefficients']);new=contributions(r,current['coefficients'])
        cases.append({'id':ident,'a':r['a'],'b':r['b'],'raw_answer':r['raw_answer'],'verified_direction':'A','magnitude':'unconfirmed; prior meaningful-A interpretation retained as tentative','frozen_v13_contributions':old,'current_v15_contributions':new,'current_threshold':current['decision_radius'],'diagnosis':'The frozen direction was wrong, but the current fit now favors A; remaining mismatch concerns an unconfirmed magnitude interpretation.' if old['total']<0 else 'Direction was and remains A; the mismatch is solely the unconfirmed meaningfulness threshold.'})
    x=np.array([base.features(r['a'])-base.features(r['b']) for r in view['rows']]);m=x@np.array(current['coefficients']);no=np.array([r['materiality_target']==0 for r in view['rows']])
    result={'source_hashes':hashes,'cases':cases,'threshold_sensitivity':{'scope':'In-sample target sensitivity only, not a selected calibration or generalization score. Includes coarsened/proxy labels.','no_meaningful_target_n':int(sum(no)),'called_meaningful_at_current_0_5':int(sum(abs(m[no])>.5)),'called_meaningful_at_target_fitting_0_15':int(sum(abs(m[no])>.15)),'action':'Do not lower threshold solely to make these three inferred labels appear correct.'},'implemented_fix':'Preserve all observed directions, distinguish tentative magnitude interpretations, and expose recorded judgment separately from model estimates. No weight changes, lookup-inflated validation, new accuracy claims or baseline modifications.','uniform_round_audit':audit,'model_limit':'The current18-coefficient model is trained on the preceding target view; estimates are provisional. This fix does not claim improved generalization or numerical price calibration.'}
    write_versioned(ROOT/'mixed-miss-analysis-v16.json',result)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'cases':[(c['id'],c['frozen_v13_contributions']['total'],c['current_v15_contributions']['total']) for c in cases],'size_assertions_qualified':len(audit),'new_primary_counts':newview['materiality_counts'],'threshold_sensitivity':result['threshold_sensitivity']}))

if __name__=='__main__':main()
