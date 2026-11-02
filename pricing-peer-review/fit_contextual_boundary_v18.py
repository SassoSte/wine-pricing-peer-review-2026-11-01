"""Fit one context-boundary scalar inside training partitions, validate kind outside."""
from pathlib import Path
import hashlib,json
import numpy as np
import refit_simple_benchmark_v16 as metrics
import contextual_meaningfulness as context
import validate_contextual_meaningfulness_v18 as original
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent
SOURCES=tuple(dict.fromkeys((*original.SOURCES,'contextual-meaningfulness-validation-v18.json','contextual-meaningfulness-fit-protocol-v18.json','fit_contextual_boundary_v18.py')))


def fit_eta(targets,evidence,beta,radius,kind):
    x,m,d,_=original.underlying.arrays(targets);g=x@np.asarray(beta);f=np.array([context.context_feature(q['a'],q['b'],beta,radius,kind) for q in targets]);positive=np.isfinite(m)&(m!=0);negative=m==0;direct=np.array(metrics.verified_materiality(evidence));baseline_correct_positive=positive&(abs(g)>radius)
    maximum=radius*(1+f);reachable=direct&negative&(f>0)&(abs(g)>radius)&(abs(g)<=maximum)
    eligible=[];records=[]
    for eta in context.ETAS:
        cut=radius*(1+eta*f);large=abs(g)>cut;preserves=bool(np.all(large[baseline_correct_positive]));missed_anchors=int(sum(large&reachable));score=metrics.score(targets,g,np.full(len(targets),radius)*(1+eta*f));rec={'eta':eta,'eligible':preserves,'unmet_reachable_anchors':missed_anchors,'score':score};records.append(rec)
        if preserves:eligible.append(rec)
    best=max(eligible,key=lambda v:(-v['unmet_reachable_anchors'],round(v['score']['materiality']['balanced_accuracy'],12),-v['score']['materiality']['false_meaningful'],-v['eta']))
    return best['eta'],{'training_ids':[t['id'] for t in targets],'reachable_direct_negative_ids':[targets[i]['id'] for i in np.flatnonzero(reachable)],'baseline_correct_meaningful_ids':[targets[i]['id'] for i in np.flatnonzero(baseline_correct_positive)],'unreachable_direct_negative_ids':[targets[i]['id'] for i in np.flatnonzero(direct&negative&(abs(g)>maximum))],'unmet_reachable_anchors':best['unmet_reachable_anchors'],'search':records}


def fit_and_select(targets,evidence,inputs,outer_beta,outer_radius):
    index={q['id']:i for i,q in enumerate(targets)};margins=np.array(inputs['margins']);radii={kind:np.zeros(len(targets)) for kind in context.KINDS};audit=[]
    for part in inputs['partitions']:
        val=[index[i] for i in part['calibration_validation_ids']];val_set=set(val);tr=[i for i in range(len(targets)) if i not in val_set];train=[targets[i] for i in tr];ev=[evidence[i] for i in tr];beta=np.array(part['coefficients']);radius=part['base_radius']
        assert set(part['underlying_training_ids'])<=set(q['id'] for q in train)
        for kind in context.KINDS:
            eta,fit=fit_eta(train,ev,beta,radius,kind)
            radii[kind][val]=[context.radius(targets[i]['a'],targets[i]['b'],beta,radius,kind,eta) for i in val]
            audit.append({'fold':part['fold'],'kind':kind,'eta':eta,'validation_ids':part['calibration_validation_ids'],'fit':fit})
    scores={kind:metrics.score(targets,margins,r) for kind,r in radii.items()}
    selected=max(['mature_shade','shared_light_tare'],key=lambda k:(round(scores[k]['materiality']['balanced_accuracy'],12),-scores[k]['materiality']['false_meaningful'],k=='mature_shade'))
    choices={};full_fits={}
    for kind in context.KINDS:
        eta,fit=fit_eta(targets,evidence,outer_beta,outer_radius,kind);choices[kind]={'kind':kind,'eta':eta};full_fits[kind]=fit
    choices['selected_context']=choices[selected].copy()
    return choices,{'inner_eta_fits':audit,'inner_scores':scores,'inner_decision_radii':{k:r.tolist() for k,r in radii.items()},'full_training_eta_fits':full_fits}


def delivery(summary):
    base=summary['v16_control'];old=summary['v17_precision'];eligible=[];checks={};eps=1e-10
    for name in ['mature_shade','shared_light_tare','selected_context']:
        s=summary[name];g={'direction_unchanged':abs(s['direction']['accuracy']-old['direction']['accuracy'])<eps,'false_calls_reduced':s['materiality']['false_meaningful']<old['materiality']['false_meaningful']-eps,'false_calls_at_most_v16':s['materiality']['false_meaningful']<=base['materiality']['false_meaningful']+eps,'balanced_noninferior':s['materiality']['balanced_accuracy']+eps>=max(old['materiality']['balanced_accuracy'],base['materiality']['balanced_accuracy']),'direct_materiality_preserved':s['directly_supported_materiality']['accuracy']+eps>=old['directly_supported_materiality']['accuracy'],'direct_meaningful_preserved':s['directly_supported_materiality']['meaningful_recall']+eps>=old['directly_supported_materiality']['meaningful_recall'],'overall_meaningful_at_least_v16':s['materiality']['meaningful_recall']+eps>=base['materiality']['meaningful_recall']}
        checks[name]=g
        if all(g.values()):eligible.append(name)
    chosen=max(eligible,key=lambda k:(summary[k]['materiality']['balanced_accuracy'],-summary[k]['materiality']['false_meaningful'],k=='selected_context')) if eligible else 'v17_precision'
    return chosen,checks


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in SOURCES};old=json.loads((ROOT/'contextual-meaningfulness-validation-v18.json').read_text());targets=json.loads((ROOT/'benchmark-targets-v18.json').read_text())['rows'];evidence=json.loads((ROOT/'evidence-v18.json').read_text())['rows'];index={q['id']:i for i,q in enumerate(targets)};direct=metrics.verified_materiality(evidence);runs={'v16_control':old['nested_cv']['runs']['v16_control'],'v17_precision':old['nested_cv']['runs']['v17_precision'],**{k:[] for k in ['matched_control','mature_shade','shared_light_tare','selected_context']}};audits=[]
    by_seed={seed:[] for seed in metrics.SEEDS}
    for entry in old['cache_manifest']:
        path=ROOT/entry['file'];assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256'];cache=json.loads(path.read_text());by_seed[cache['seed']].append(cache)
    for seed in metrics.SEEDS:
        baseline=next(q for q in runs['v17_precision'] if q['seed']==seed);m=np.array(baseline['margins']);radii={k:np.zeros(len(targets)) for k in ['matched_control','mature_shade','shared_light_tare','selected_context']}
        for c in sorted(by_seed[seed],key=lambda q:q['fold']):
            tr=[index[i] for i in c['training_ids']];te=[index[i] for i in c['validation_ids']];train=[targets[i] for i in tr];ev=[evidence[i] for i in tr];beta=np.array(c['underlying_coefficients']);radius=c['base_radius'];choices,audit=fit_and_select(train,ev,c['inputs'],beta,radius)
            for kind in radii:
                choice=choices[kind];radii[kind][te]=[context.radius(targets[i]['a'],targets[i]['b'],beta,radius,choice['kind'],choice['eta']) for i in te]
            audits.append({'seed':seed,'fold':c['fold'],'training_ids':c['training_ids'],'validation_ids':c['validation_ids'],'choices':choices,'calibration':audit})
        for kind,r in radii.items():runs[kind].append({'seed':seed,'margins':baseline['margins'],'radii':r.tolist(),'score':metrics.score(targets,m,r,direct)})
    summary=metrics.summarize(runs);winner,gates=delivery(summary);base_model=json.loads((ROOT/'precision-shade-candidate-v17.json').read_text())['model'];beta=np.array(base_model['coefficients']);base_radius=base_model['decision_radius'];choices,calibration=fit_and_select(targets,evidence,old['full_data_calibration']['inputs'],beta,base_radius);choice=choices[winner] if winner!='v17_precision' else {'kind':'mature_shade','eta':0.}
    model={'kind':'contextual_meaningfulness','underlying_source':'precision-shade-candidate-v17.json','underlying_coefficients':base_model['coefficients'],'base_radius':base_radius,'context_kind':choice['kind'],'context_coefficient':choice['eta'],'direction_weights_changed':False,'calibration_evidence':'evidence-v18.json'}
    full_outputs={q['id']:context.predict(q['a'],q['b'],beta,base_radius,choice['kind'],choice['eta']) for q in targets if q['id'].startswith(('round36-','round37-'))}
    result={'method':{'source_hashes':hashes,'protocol':json.loads((ROOT/'contextual-meaningfulness-fit-protocol-v18.json').read_text()),'parent_cache_manifest':old['cache_manifest'],'lookup_policy':'One scalar fitted from training labels. Prediction uses only input attributes, immutable underlying coefficients and scalar. No row overrides.'},'row_ids':old['row_ids'],'nested_cv':{'runs':runs,'summary':summary,'fold_audits':audits},'full_data_calibration':{'choices':choices,'audit':calibration},'candidate_model':model,'full_data_recent_outputs':full_outputs,'delivery':{'selected':winner,'checks':gates}}
    write_versioned(ROOT/'contextual-boundary-fit-validation-v18.json',result)
    artifact={'selected_model':winner,'model':model,'evidence':'evidence-v18.json','validation_file':'contextual-boundary-fit-validation-v18.json','validation_sha256':hashlib.sha256((ROOT/'contextual-boundary-fit-validation-v18.json').read_bytes()).hexdigest(),'validation':summary[winner],'prediction_source':'frozen19 utility coefficients plus one learned materiality parameter; no answer lookup','qualification':'Exploratory family validation. Does not establish shade-versus-tare causality or dollar prices.'}
    write_versioned(ROOT/'contextual-boundary-fit-delivery-v18.json',artifact)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'selected':winner,'summary':summary,'checks':gates,'full_choices':choices},indent=2))

if __name__=='__main__':main()
