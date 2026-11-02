"""Focused v17 correction: one shade context term and reliable two-axis constraints."""
from pathlib import Path
from copy import deepcopy
import hashlib,json
import numpy as np
import compare_models as base
import build_meaningful_benchmark as simple
import refit_simple_benchmark_v16 as previous
import domestic_shade_model as shade
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent
ARMS=('v16_control','v17_additive','v17_shade_soft','v17_shade_protected')
ALPHAS=simple.ALPHAS
RADII=simple.RADII
TOL=1e-7
SOURCES=tuple(dict.fromkeys((*previous.SOURCES,'simple-benchmark-validation-v16.json','simple-benchmark-v16-delivery.json','evidence-v17.json','benchmark-targets-v17.json','round36-fixed.json','build_evidence_v17.py','domestic_shade_model.py','domestic-shade-protocol-v17.json','validate_domestic_shade_v17.py')))


def folds(groups,seed):
    assignment={}
    for k,(_,test) in enumerate(previous.folds(groups[:413],seed)):
        for g in set(groups[test]):assignment[g]=k
    sizes=np.array([sum(assignment.get(g)==k for g in groups) for k in range(5)]);extra=sorted(set(groups)-set(assignment));np.random.default_rng(seed).shuffle(extra);extra.sort(key=lambda g:-sum(groups==g))
    for g in extra:k=int(np.argmin(sizes));assignment[g]=k;sizes[k]+=sum(groups==g)
    bins=np.array([assignment[g] for g in groups])
    for k in range(5):yield np.flatnonzero(bins!=k),np.flatnonzero(bins==k)


def effective_radius(beta,radius):
    pale=float(beta[12]+(beta[18] if len(beta)==19 else 0.))
    return max(float(radius),abs(float(beta[17])),abs(pale))+TOL


def calibration(targets,evidence,seed):
    x18,m,d,g=simple.arrays(targets);x19=shade.arrays(targets)[0]
    keys=[(a,r) for a in ALPHAS for r in RADII];outputs={arm:{str((a,r)):{'margins':np.zeros(len(targets)),'radii':np.zeros(len(targets))} for a,r in keys} for arm in ARMS[1:]};audits=[]
    for fold,(tr,va) in enumerate(base.folds(g,3,seed)):
        assert not set(g[tr])&set(g[va]);train=[targets[i] for i in tr];ev=[evidence[i] for i in tr]
        for alpha in ALPHAS:
            add=simple.fit(train,alpha)
            for radius in RADII:
                key=str((alpha,radius));params={'v17_additive':add,'v17_shade_soft':shade.fit(train,ev,alpha,radius,False),'v17_shade_protected':shade.fit(train,ev,alpha,radius,True)}
                for arm,beta in params.items():
                    outputs[arm][key]['margins'][va]=(x18 if len(beta)==18 else x19)[va]@beta;outputs[arm][key]['radii'][va]=effective_radius(beta,radius)
        audits.append({'fold':fold,'training_ids':[r['id'] for r in train],'validation_ids':[targets[i]['id'] for i in va],'protected_ids':[r['id'] for r,ok in zip(train,previous.verified_materiality(ev)) if ok and r['materiality_target'] is not None]})
    choices={};search={}
    for arm in ARMS[1:]:
        best=None;selected=None;search[arm]=[]
        for alpha,radius in keys:
            o=outputs[arm][str((alpha,radius))];s=previous.score(targets,o['margins'],o['radii']);a=s['direction']['accuracy'];b=s['materiality']['balanced_accuracy'];key=(round(.5*(a+b),12),round(min(a,b),12),-s['direction']['reversals'],alpha,radius)
            search[arm].append({'alpha':alpha,'training_radius':radius,'score':s})
            if best is None or key>best:best=key;selected={'alpha':alpha,'training_radius':radius}
        choices[arm]=selected
    return choices,{'partitions':audits,'search':search,'outputs':{arm:{key:{k:v.tolist() for k,v in o.items()} for key,o in values.items()} for arm,values in outputs.items()}}


def choose_delivery(summary):
    old=summary['v16_control'];checks={};eligible=[];eps=1e-10
    for arm in ARMS[1:]:
        s=summary[arm];g={'direction_noninferior':s['direction']['accuracy']+eps>=old['direction']['accuracy'],'materiality_noninferior':s['materiality']['balanced_accuracy']+eps>=old['materiality']['balanced_accuracy'],'reversals_noninferior':s['direction']['reversals']<=old['direction']['reversals']+eps,'false_meaningful_noninferior':s['materiality']['false_meaningful']<=old['materiality']['false_meaningful']+eps,'direct_materiality_noninferior':s['directly_supported_materiality']['accuracy']+eps>=old['directly_supported_materiality']['accuracy'],'gain':s['direction']['accuracy']>old['direction']['accuracy']+eps or s['materiality']['balanced_accuracy']>old['materiality']['balanced_accuracy']+eps}
        checks[arm]=g
        if all(g.values()):eligible.append(arm)
    winner=max(eligible,key=lambda a:(.5*(summary[a]['direction']['accuracy']+summary[a]['materiality']['balanced_accuracy']),-summary[a]['direction']['reversals'],a=='v17_additive')) if eligible else 'v16_control'
    return winner,checks


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in SOURCES};targets=json.loads((ROOT/'benchmark-targets-v17.json').read_text())['rows'];evidence=json.loads((ROOT/'evidence-v17.json').read_text())['rows'];parent=json.loads((ROOT/'simple-benchmark-validation-v16.json').read_text());parent_delivery=json.loads((ROOT/'simple-benchmark-v16-delivery.json').read_text());assert parent_delivery['selected_model']=='v16_blended'
    cache_hashes={c['file']:c['sha256'] for c in parent['cache_manifest']};x18,_,_,g=simple.arrays(targets);x19=shade.arrays(targets)[0];direct=previous.verified_materiality(evidence);runs={a:[] for a in ARMS};manifest=[];audits=[];root=ROOT/'domestic-shade-cache-v17';root.mkdir(exist_ok=True)
    for seed in previous.SEEDS:
        margins={a:np.zeros(len(targets)) for a in ARMS};radii={a:np.zeros(len(targets)) for a in ARMS}
        for fold,(tr,te) in enumerate(folds(g,seed)):
            assert not set(g[tr])&set(g[te]);oldpath=f'simple-cache-v16/seed-{seed}-fold-{fold}.json';assert hashlib.sha256((ROOT/oldpath).read_bytes()).hexdigest()==cache_hashes[oldpath];old=json.loads((ROOT/oldpath).read_text());assert old['training_ids']==[targets[i]['id'] for i in tr if i<413];assert old['validation_ids']==[targets[i]['id'] for i in te if i<413]
            bp=np.array(old['coefficients']['v16_blended']);margins['v16_control'][te]=x18[te]@bp;radii['v16_control'][te]=old['choices']['v16_blended']['radius']
            train=[targets[i] for i in tr];ev=[evidence[i] for i in tr];path=root/f'seed-{seed}-fold-{fold}.json'
            if path.exists():cache=json.loads(path.read_text());assert cache['source_hashes']==hashes
            else:
                choices,inner=calibration(train,ev,seed+fold+17000);params={};outer={};actual={}
                for arm,cfg in choices.items():
                    beta=simple.fit(train,cfg['alpha']) if arm=='v17_additive' else shade.fit(train,ev,cfg['alpha'],cfg['training_radius'],arm=='v17_shade_protected')
                    params[arm]=beta.tolist();outer[arm]=((x18 if len(beta)==18 else x19)[te]@beta).tolist();actual[arm]=effective_radius(beta,cfg['training_radius'])
                cache={'source_hashes':hashes,'seed':seed,'fold':fold,'training_ids':[r['id'] for r in train],'validation_ids':[targets[i]['id'] for i in te],'choices':choices,'inner':inner,'coefficients':params,'outer_margins':outer,'decision_radii':actual,'protected_ids':[r['id'] for r,ok in zip(train,previous.verified_materiality(ev)) if ok and r['materiality_target'] is not None]};write_versioned(path,cache)
            assert cache['training_ids']==[r['id'] for r in train]
            for arm in ARMS[1:]:margins[arm][te]=cache['outer_margins'][arm];radii[arm][te]=cache['decision_radii'][arm]
            audits.append({'seed':seed,'fold':fold,'choices':cache['choices'],'decision_radii':cache['decision_radii'],'cache_file':str(path.relative_to(ROOT))});manifest.append({'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
            print(f'Completed domestic-shade v17 seed {seed}, fold {fold+1}/5',flush=True)
        oldrun=next(r for r in parent['nested_cv']['runs']['v16_blended'] if r['seed']==seed);np.testing.assert_allclose(margins['v16_control'][:413],oldrun['margins'],rtol=0,atol=1e-10)
        for arm in ARMS:runs[arm].append({'seed':seed,'margins':margins[arm].tolist(),'radii':radii[arm].tolist(),'score':previous.score(targets,margins[arm],radii[arm],direct)})
    summary=previous.summarize(runs);winner,gates=choose_delivery(summary);choices,inner=calibration(targets,evidence,17001);full={}
    full['v16_control']=deepcopy(parent_delivery['model'])
    for arm,cfg in choices.items():
        beta=simple.fit(targets,cfg['alpha']) if arm=='v17_additive' else shade.fit(targets,evidence,cfg['alpha'],cfg['training_radius'],arm=='v17_shade_protected');radius=effective_radius(beta,cfg['training_radius']);x=x18 if len(beta)==18 else x19
        full[arm]={'kind':arm,'trained_evidence':'evidence-v17.json','alpha':cfg['alpha'],'training_radius':cfg['training_radius'],'decision_radius':radius,'coefficients':beta.tolist(),'feature_names':[*base.FEATURES,*([shade.FEATURE] if len(beta)==19 else [])],'global_rules':{'five_pound_tare_contribution':float(beta[17]),'domestic_golden_pale_contribution':float(beta[12]+(beta[18] if len(beta)==19 else 0))},'training_score':previous.score(targets,x@beta,radius,direct),'round36_training_predictions':[{'id':targets[i]['id'],'direction':'A' if (x[i]@beta)>1e-7 else 'B' if (x[i]@beta)<-1e-7 else None,'materiality':'meaningful_difference' if abs(x[i]@beta)>radius else 'no_meaningful_difference','margin':float(x[i]@beta)} for i in range(413,425)]}
    result={'method':{'source_hashes':hashes,'protocol':json.loads((ROOT/'domestic-shade-protocol-v17.json').read_text()),'baseline_cache_hashes':cache_hashes,'lookup_policy':'All margins computed as offer-feature differences times training coefficients. Direct-evidence constraints exist only during fitting; no per-pair overrides in prediction.','limits':'New user guidance and architecture are known before this exploratory run; not another prospective test. Round36 original6/12 versus5/12 directions and10/12 size each remain unchanged. Training predictions on those rows are not new validation accuracy.'},'row_ids':[r['id'] for r in targets],'nested_cv':{'runs':runs,'summary':summary,'fold_audits':audits},'cache_manifest':manifest,'full_data_models':full,'full_data_choices':choices,'full_data_calibration':inner,'delivery':{'selected':winner,'checks':gates}}
    write_versioned(ROOT/'domestic-shade-validation-v17.json',result)
    artifact={'selected_model':winner,'model':full[winner],'evidence':'evidence-v17.json','target_view':'benchmark-targets-v17.json','validation_file':'domestic-shade-validation-v17.json','validation_sha256':hashlib.sha256((ROOT/'domestic-shade-validation-v17.json').read_bytes()).hexdigest(),'validation':summary[winner],'prediction_source':'model coefficients only; no answer lookup','qualification':'Direction and meaningfulness separately estimated; no currency calibration or exact-price claim. Prior models unchanged.'}
    write_versioned(ROOT/'domestic-shade-delivery-v17.json',artifact)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'selected':winner,'summary':summary,'checks':gates,'full_choices':choices},indent=2))

if __name__=='__main__':main()
