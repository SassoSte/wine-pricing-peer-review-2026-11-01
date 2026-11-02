"""Test a three-coefficient context repair against selected v16, model-only."""
from pathlib import Path
import hashlib,json
import numpy as np
import refit_simple_benchmark_v16 as prior
import minimal_context_model as context
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent
SOURCES=tuple(dict.fromkeys((*prior.SOURCES,'refit_simple_benchmark_v16.py','simple-benchmark-validation-v16.json','simple-benchmark-v16-delivery.json','simple-direction-feasibility-v16.json','minimal-context-conflict-audit-v16.json','minimal_context_model.py','minimal-context-protocol-v16.json','validate_minimal_context_v16.py')))


def calibration(targets,seed):
    x,m,d,g=context.arrays(targets);outputs={str(a):np.zeros(len(targets)) for a in prior.ALPHAS};audit=[]
    for fold,(tr,va) in enumerate(prior.base.folds(g,3,seed)):
        assert not set(g[tr])&set(g[va]);train=[targets[i] for i in tr]
        for alpha in prior.ALPHAS:outputs[str(alpha)][va]=x[va]@context.fit(train,alpha)
        audit.append({'fold':fold,'training_ids':[targets[i]['id'] for i in tr],'validation_ids':[targets[i]['id'] for i in va]})
    best=None;choice=None;search=[]
    for alpha in prior.ALPHAS:
        margins=outputs[str(alpha)];radii=sorted(set([0.,*prior.previous.RADII,*np.quantile(abs(margins[np.isfinite(m)]),np.linspace(0,1,21)).tolist()]))
        for radius in radii:
            score=prior.score(targets,margins,radius);a=score['direction']['accuracy'];b=score['materiality']['balanced_accuracy'];key=(round(.5*(a+b),12),round(min(a,b),12),-score['direction']['reversals'],alpha,radius)
            search.append({'alpha':alpha,'radius':float(radius),'score':score})
            if best is None or key>best:best=key;choice={'alpha':alpha,'radius':float(radius)}
    return choice,{'partitions':audit,'margins':{a:m.tolist() for a,m in outputs.items()},'search':search}


def choose_delivery(summary):
    old=summary['v16_baseline'];new=summary['minimal_context'];eps=1e-10
    checks={'direction_noninferior':new['direction']['accuracy']+eps>=old['direction']['accuracy'],'materiality_noninferior':new['materiality']['balanced_accuracy']+eps>=old['materiality']['balanced_accuracy'],'reversals_noninferior':new['direction']['reversals']<=old['direction']['reversals']+eps,'false_meaningful_noninferior':new['materiality']['false_meaningful']<=old['materiality']['false_meaningful']+eps,'direct_materiality_noninferior':new['directly_supported_materiality']['accuracy']+eps>=old['directly_supported_materiality']['accuracy'],'improves_one':new['direction']['accuracy']>old['direction']['accuracy']+eps or new['materiality']['balanced_accuracy']>old['materiality']['balanced_accuracy']+eps}
    return ('minimal_context' if all(checks.values()) else 'v16_baseline'),checks


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in SOURCES};targets=json.loads((ROOT/'benchmark-targets-v16.json').read_text())['rows'];evidence=json.loads((ROOT/'evidence-v16.json').read_text())['rows'];old=json.loads((ROOT/'simple-benchmark-validation-v16.json').read_text());oldmodel=json.loads((ROOT/'simple-benchmark-v16-delivery.json').read_text());assert oldmodel['selected_model']=='v16_blended'
    cache_hashes={c['file']:c['sha256'] for c in old['cache_manifest']};x,_,_,g=context.arrays(targets);direct=prior.verified_materiality(evidence);runs={'v16_baseline':[],'minimal_context':[]};audits=[];manifest=[];root=ROOT/'minimal-context-cache-v16';root.mkdir(exist_ok=True)
    for seed in prior.SEEDS:
        margins=np.zeros(len(targets));radii=np.zeros(len(targets))
        for fold,(tr,te) in enumerate(prior.folds(g,seed)):
            assert not set(g[tr])&set(g[te]);train=[targets[i] for i in tr];path=root/f'seed-{seed}-fold-{fold}.json'
            oldpath=f'simple-cache-v16/seed-{seed}-fold-{fold}.json';assert hashlib.sha256((ROOT/oldpath).read_bytes()).hexdigest()==cache_hashes[oldpath]
            if path.exists():cache=json.loads(path.read_text());assert cache['source_hashes']==hashes
            else:
                cfg,inner=calibration(train,seed+fold+16000);beta=context.fit(train,cfg['alpha']);cache={'source_hashes':hashes,'seed':seed,'fold':fold,'training_ids':[targets[i]['id'] for i in tr],'validation_ids':[targets[i]['id'] for i in te],'choice':cfg,'inner':inner,'coefficients':beta.tolist(),'outer_margins':(x[te]@beta).tolist()};write_versioned(path,cache)
            assert cache['training_ids']==[targets[i]['id'] for i in tr] and cache['validation_ids']==[targets[i]['id'] for i in te]
            margins[te]=cache['outer_margins'];radii[te]=cache['choice']['radius'];audits.append({'seed':seed,'fold':fold,'choice':cache['choice'],'cache_file':str(path.relative_to(ROOT))});manifest.append({'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        baseline=next(v for v in old['nested_cv']['runs']['v16_blended'] if v['seed']==seed)
        assert prior.score(targets,baseline['margins'],baseline['radii'],direct)==baseline['score']
        runs['v16_baseline'].append(baseline);runs['minimal_context'].append({'seed':seed,'margins':margins.tolist(),'radii':radii.tolist(),'score':prior.score(targets,margins,radii,direct)})
        print(f'Completed minimal-context validation repeat {seed}',flush=True)
    summary=prior.summarize(runs);winner,checks=choose_delivery(summary);cfg,inner=calibration(targets,1301);beta=context.fit(targets,cfg['alpha']);full={'kind':'minimal_context','trained_evidence':'evidence-v16.json','alpha':cfg['alpha'],'decision_radius':cfg['radius'],'coefficients':beta.tolist(),'feature_names':[*prior.base.FEATURES,*context.TERMS],'training_score':prior.score(targets,x@beta,cfg['radius'],direct)}
    conflict=json.loads((ROOT/'simple-direction-feasibility-v16.json').read_text())['identical_feature_direction_conflicts'];conflict_ids={q['id'] for group in conflict for q in group};pos={r['id']:i for i,r in enumerate(targets)};diagnostics={}
    for name,values in runs.items():
        diagnostics[name]=[{'seed':v['seed'],'n':len(conflict_ids),'correct':sum((1 if v['margins'][pos[i]]>1e-7 else -1 if v['margins'][pos[i]]<-1e-7 else 0)==targets[pos[i]]['known_direction'] for i in conflict_ids)} for v in values]
    result={'method':{'source_hashes':hashes,'protocol':json.loads((ROOT/'minimal-context-protocol-v16.json').read_text()),'baseline_cache_hashes':cache_hashes,'lookup_policy':'Every outer prediction is context_feature_difference@test_training_coefficients; baseline uses verified cached model-only margins. No recorded-answer retrieval.','limits':'Known conflict cases motivated features before this run; same repeatedly used evidence/family folds. Four records have verbatim text and11 only structured direction history. No label corrections or new prospective claims.'},'row_ids':[t['id'] for t in targets],'nested_cv':{'runs':runs,'summary':summary,'fold_audits':audits},'cache_manifest':manifest,'conflict_case_oof_diagnostics':diagnostics,'candidate_fit_all_413':full,'full_data_calibration':inner,'delivery':{'selected':winner,'checks':checks}}
    write_versioned(ROOT/'minimal-context-validation-v16.json',result)
    delivered=full if winner=='minimal_context' else oldmodel['model']
    artifact={'selected_model':winner,'model':delivered,'evidence':'evidence-v16.json','target_view':'benchmark-targets-v16.json','validation_file':'minimal-context-validation-v16.json','validation_sha256':hashlib.sha256((ROOT/'minimal-context-validation-v16.json').read_bytes()).hexdigest(),'validation':summary[winner],'prediction_source':'model coefficients only; no answer lookup','qualification':'Best retained under prespecified direction/materiality/error safeguards on exploratory family validation; not monetary calibration.'}
    write_versioned(ROOT/'minimal-context-delivery-v16.json',artifact)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'winner':winner,'scores':summary,'checks':checks,'contexts':dict(zip(context.TERMS,beta[18:].tolist())),'conflict_oof':diagnostics},indent=2))

if __name__=='__main__':main()
