"""Apply the existing user5lb rule algebraically, without refitting or label tuning."""
from pathlib import Path
from copy import deepcopy
import hashlib,json
import numpy as np
import refit_simple_benchmark_v16 as scorecard
import validate_minimal_context_v16 as context_run
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent
TOL=1e-8


def radius_with_tare_rule(radius,coefficients):
    # First18 features are unchanged. Same provenance/shade/vintage and5lb
    # difference changes exactly feature17 by one. Context features do not use tare.
    return max(float(radius),abs(float(coefficients[17]))+TOL)


def main():
    files=['minimal-context-validation-v16.json','simple-benchmark-validation-v16.json','evidence-v13.json','evidence-v16.json','benchmark-targets-v16.json','minimal_context_model.py','validate_minimal_context_rule_v16.py']
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files};result=json.loads((ROOT/'minimal-context-validation-v16.json').read_text());baseline=json.loads((ROOT/'simple-benchmark-validation-v16.json').read_text());targets=json.loads((ROOT/'benchmark-targets-v16.json').read_text())['rows'];evidence=json.loads((ROOT/'evidence-v16.json').read_text())['rows'];ids={r['id']:i for i,r in enumerate(targets)};direct=scorecard.verified_materiality(evidence)
    runs={'v16_native':deepcopy(result['nested_cv']['runs']['v16_baseline']),'v16_with_rule':[],'minimal_context_with_rule':[]};changes=[];cache_hashes={c['file']:c['sha256'] for c in result['cache_manifest']};baseline_hashes={c['file']:c['sha256'] for c in baseline['cache_manifest']}
    for seed in scorecard.SEEDS:
        br=np.array(next(r for r in result['nested_cv']['runs']['v16_baseline'] if r['seed']==seed)['radii']);cr=np.array(next(r for r in result['nested_cv']['runs']['minimal_context'] if r['seed']==seed)['radii'])
        for fold in range(5):
            cpath=f'minimal-context-cache-v16/seed-{seed}-fold-{fold}.json';bpath=f'simple-cache-v16/seed-{seed}-fold-{fold}.json'
            assert hashlib.sha256((ROOT/cpath).read_bytes()).hexdigest()==cache_hashes[cpath];assert hashlib.sha256((ROOT/bpath).read_bytes()).hexdigest()==baseline_hashes[bpath]
            c=json.loads((ROOT/cpath).read_text());b=json.loads((ROOT/bpath).read_text());te=[ids[i] for i in c['validation_ids']];assert c['validation_ids']==b['validation_ids']
            for name,radii,coefficients,radius in [('v16_with_rule',br,b['coefficients']['v16_blended'],b['choices']['v16_blended']['radius']),('minimal_context_with_rule',cr,c['coefficients'],c['choice']['radius'])]:
                adjusted=radius_with_tare_rule(radius,coefficients);radii[te]=adjusted
                changes.append({'model':name,'seed':seed,'fold':fold,'original_radius':radius,'tare_5lb_contribution':coefficients[17],'adjusted_radius':adjusted,'changed':adjusted!=radius,'basis':'Coefficients and prior user rule only; no validation labels used.'})
        for name,original,radius in [('v16_with_rule','v16_baseline',br),('minimal_context_with_rule','minimal_context',cr)]:
            old=next(r for r in result['nested_cv']['runs'][original] if r['seed']==seed);m=np.array(old['margins']);runs[name].append({'seed':seed,'margins':old['margins'],'radii':radius.tolist(),'score':scorecard.score(targets,m,radius,direct)})
    summary=scorecard.summarize(runs)
    chosen_native,gates_native=context_run.choose_delivery({'v16_baseline':summary['v16_native'],'minimal_context':summary['minimal_context_with_rule']})
    chosen_rule,gates_rule=context_run.choose_delivery({'v16_baseline':summary['v16_with_rule'],'minimal_context':summary['minimal_context_with_rule']})
    chosen='minimal_context_with_rule' if chosen_native=='minimal_context' and chosen_rule=='minimal_context' else 'v16_baseline'
    cfg=deepcopy(result['candidate_fit_all_413'] if chosen=='minimal_context_with_rule' else baseline['full_data_models']['v16_blended']);cfg['uncorrected_calibrated_radius']=cfg['decision_radius'];cfg['decision_radius']=radius_with_tare_rule(cfg['decision_radius'],cfg['coefficients']);cfg['tare_rule_applied']=True
    evidence13=json.loads((ROOT/'evidence-v13.json').read_text())
    out={'method':{'source_hashes':hashes,'rule_source':{'file':'evidence-v13.json','raw_answer':evidence13['clarification']['raw_answer']},'rule':'radius=max(calibrated_radius,abs(tare_coefficient_for5lb)+1e-8). No coefficient or label changes. Applies to both18- and21-feature models because context terms are tare-independent. No new estimated parameter.','validation':'Reuse untouched held-out margins; threshold floor determined entirely by each training fit and prior global user rule. Apply to both baseline and candidate, also compare to native v16. Identified after exploratory error inspection, not a new untouched holdout.','semantics':'This is an operational materiality constraint, not a hard price-equality constraint; small directional preference can remain.'},'nested_cv':{'runs':runs,'summary':summary},'fold_rule_applications':changes,'cache_hashes':cache_hashes,'baseline_cache_hashes':baseline_hashes,'delivery':{'selected':chosen,'against_native_v16':gates_native,'against_rule_v16':gates_rule}}
    write_versioned(ROOT/'minimal-context-rule-validation-v16.json',out)
    delivery={'selected_model':chosen,'model':cfg,'evidence':'evidence-v16.json','target_view':'benchmark-targets-v16.json','validation_file':'minimal-context-rule-validation-v16.json','validation_sha256':hashlib.sha256((ROOT/'minimal-context-rule-validation-v16.json').read_bytes()).hexdigest(),'validation':summary['minimal_context_with_rule'] if chosen=='minimal_context_with_rule' else summary['v16_with_rule'],'prediction_source':'model coefficients only; no answer lookup','qualification':'Three context terms plus prior5lb materiality rule. Exploratory grouped validation; positive materiality proxies remain limited.'}
    write_versioned(ROOT/'minimal-context-rule-delivery-v16.json',delivery)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'selected':chosen,'summary':summary,'gates':out['delivery'],'changed_folds':[x for x in changes if x['changed']]},indent=2))

if __name__=='__main__':main()
