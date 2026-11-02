"""Model-only validation separating direction from meaningfulness on v16."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
import compare_models as base
import build_meaningful_benchmark as previous
import refit_weighted_v10 as family_protocol
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent
ALPHAS=previous.ALPHAS
SEEDS=base.SEEDS
ARMS=('v15_recipe_control','v16_blended','v16_direction_first')
SOURCES=('evidence-v15.json','evidence-v16.json','benchmark-targets-v15.json','benchmark-targets-v16.json','meaningful-benchmark-v15.json','build_meaningful_benchmark.py','compare_models.py','refit_weighted_v10.py','simple_benchmark_validation_protocol_v16.json','refit_simple_benchmark_v16.py')


def folds(groups,seed):
    assignments={}
    for fold,(_,test) in enumerate(family_protocol.extended_folds(groups[:366],groups[:401],seed)):
        for g in set(groups[test]):assignments[g]=fold
    sizes=np.array([sum(assignments.get(g)==i for g in groups) for i in range(5)])
    new=sorted(set(groups)-set(assignments));np.random.default_rng(seed).shuffle(new);new.sort(key=lambda g:-sum(groups==g))
    for g in new:
        k=int(np.argmin(sizes));assignments[g]=k;sizes[k]+=sum(groups==g)
    indices=np.array([assignments[g] for g in groups])
    for k in range(5):yield np.flatnonzero(indices!=k),np.flatnonzero(indices==k)


def direction_objective(beta,x,direction,alpha):
    z=direction*(x@beta)
    return float(np.logaddexp(0,-z).sum()+alpha*(beta@beta)),-x.T@(direction*expit(-z))+2*alpha*beta


def fit_direction(targets,alpha):
    x,_,direction,_=previous.arrays(targets);known=direction!=0
    result=minimize(direction_objective,np.zeros(18),args=(x[known],direction[known],alpha),jac=True,method='L-BFGS-B',bounds=[(None,None)]*9+[(0,None)]*9,options={'ftol':1e-12,'gtol':1e-7,'maxiter':3000})
    if not result.success:raise RuntimeError(result.message)
    return result.x


def score(targets,margins,radius,verified_mask=None):
    _,material,direction,_=previous.arrays(targets);margins=np.asarray(margins);radius=np.broadcast_to(radius,margins.shape)
    sign=np.where(margins>1e-7,1,np.where(margins<-1e-7,-1,0));known_dir=direction!=0;known=np.isfinite(material);positive=known&(material!=0);negative=material==0;large=abs(margins)>radius
    def material_score(mask):
        pos=positive&mask;neg=negative&mask;both=pos|neg;recalls=[]
        if np.any(pos):recalls.append(float(np.mean(large[pos])))
        if np.any(neg):recalls.append(float(np.mean(~large[neg])))
        return {'n':int(sum(both)),'meaningful_n':int(sum(pos)),'no_meaningful_n':int(sum(neg)),'accuracy':float(np.mean(large[both]==positive[both])) if np.any(both) else None,'balanced_accuracy':float(np.mean(recalls)) if recalls else None,'meaningful_recall':float(np.mean(large[pos])) if np.any(pos) else None,'no_meananingful_recall':float(np.mean(~large[neg])) if np.any(neg) else None,'false_meaningful':int(sum(large&neg)),'missed_meaningful':int(sum(~large&pos)),'correct_meaningful_direction':int(sum(large&pos&(sign==direction)))}
    result={'direction':{'n':int(sum(known_dir)),'correct':int(sum(known_dir&(sign==direction))),'accuracy':float(np.mean(sign[known_dir]==direction[known_dir])),'reversals':int(sum(known_dir&(sign==-direction))),'zero_or_abstain':int(sum(known_dir&(sign==0)))},'materiality':material_score(np.ones(len(targets),dtype=bool)),'unknown_materiality_n':int(sum(~known))}
    if verified_mask is not None:result['directly_supported_materiality']=material_score(np.array(verified_mask,dtype=bool))
    return result


def calibration(targets,oldtargets,seed):
    x,_,_,g=previous.arrays(targets);outputs={arm:{str(a):np.zeros(len(targets)) for a in ALPHAS} for arm in ARMS};audits=[]
    for fold,(tr,va) in enumerate(base.folds(g,3,seed)):
        assert not set(g[tr])&set(g[va]);train=[targets[i] for i in tr];oldtrain=[oldtargets[i] for i in tr]
        for alpha in ALPHAS:
            for arm,params in [('v15_recipe_control',previous.fit(oldtrain,alpha)),('v16_blended',previous.fit(train,alpha)),('v16_direction_first',fit_direction(train,alpha))]:outputs[arm][str(alpha)][va]=x[va]@params
        audits.append({'fold':fold,'training_ids':[targets[i]['id'] for i in tr],'validation_ids':[targets[i]['id'] for i in va]})
    choices={};search={};_,oldmaterial,_,_=previous.arrays(oldtargets)
    for arm in ARMS:
        best=None;selected=None;search[arm]=[]
        for alpha in ALPHAS:
            margins=outputs[arm][str(alpha)]
            if arm=='v15_recipe_control':radii=previous.RADII
            else:
                _,mat,_,_=previous.arrays(targets);values=abs(margins[np.isfinite(mat)])
                radii=sorted(set([0.,*previous.RADII,*np.quantile(values,np.linspace(0,1,21)).tolist()]))
            for radius in radii:
                metrics=score(targets,margins,radius)
                if arm=='v15_recipe_control':
                    oldscore=previous.materiality_metrics(oldmaterial,previous.predict(margins,radius));key=(round(oldscore['balanced_accuracy'],12),round(oldscore['accuracy'],12),alpha,radius)
                else:
                    a=metrics['direction']['accuracy'];b=metrics['materiality']['balanced_accuracy'];key=(round(.5*(a+b),12),round(min(a,b),12),-metrics['direction']['reversals'],alpha,radius)
                search[arm].append({'alpha':alpha,'radius':float(radius),'score':metrics})
                if best is None or key>best:best=key;selected={'alpha':alpha,'radius':float(radius)}
        choices[arm]=selected
    return choices,{'partitions':audits,'search':search,'inner_margins':{arm:{a:m.tolist() for a,m in vals.items()} for arm,vals in outputs.items()}}


def verified_materiality(rows):
    flags=[]
    for row in rows:
        explicit=row.get('explicit_materiality')
        direct=explicit in ('meaningful_A','meaningful_B','no_meaningful_difference')
        direct|=row['winner']=='practical_similarity'
        direct|=row.get('materiality_clarification',{}).get('value')=='no_meaningful_difference'
        flags.append(bool(direct))
    return flags


def summarize(runs):
    result={}
    for arm,values in runs.items():
        first=values[0]['score'];result[arm]={}
        for kind in ['direction','materiality','directly_supported_materiality']:
            result[arm][kind]={}
            for key,value in first[kind].items():
                if key=='n' or key.endswith('_n'):result[arm][kind][key]=value
                elif value is None:result[arm][kind][key]=None
                else:result[arm][kind][key]=float(np.mean([r['score'][kind][key] for r in values]))
        result[arm]['unknown_materiality_n']=first['unknown_materiality_n']
    return result


def choose_delivery(summary):
    old=summary['v15_recipe_control'];checks={};eligible=[];eps=1e-10
    for arm in ARMS[1:]:
        s=summary[arm];gate={'direction_noninferior':s['direction']['accuracy']+eps>=old['direction']['accuracy'],'materiality_noninferior':s['materiality']['balanced_accuracy']+eps>=old['materiality']['balanced_accuracy'],'reversals_noninferior':s['direction']['reversals']<=old['direction']['reversals']+eps,'improves_one':s['direction']['accuracy']>old['direction']['accuracy']+eps or s['materiality']['balanced_accuracy']>old['materiality']['balanced_accuracy']+eps}
        checks[arm]=gate
        if all(gate.values()):eligible.append(arm)
    winner=max(eligible,key=lambda a:(.5*(summary[a]['direction']['accuracy']+summary[a]['materiality']['balanced_accuracy']),-summary[a]['direction']['reversals'])) if eligible else 'v15_recipe_control'
    return winner,checks


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in SOURCES};targets=json.loads((ROOT/'benchmark-targets-v16.json').read_text())['rows'];oldtargets=json.loads((ROOT/'benchmark-targets-v15.json').read_text())['rows'];evidence=json.loads((ROOT/'evidence-v16.json').read_text())['rows'];assert [r['id'] for r in targets]==[r['id'] for r in oldtargets]==[r['id'] for r in evidence]
    x,_,_,g=previous.arrays(targets);direct=verified_materiality(evidence);runs={a:[] for a in ARMS};audits=[];cache_root=ROOT/'simple-cache-v16';cache_root.mkdir(exist_ok=True);manifest=[]
    for seed in SEEDS:
        margins={a:np.zeros(len(targets)) for a in ARMS};radii={a:np.zeros(len(targets)) for a in ARMS}
        for fold,(tr,te) in enumerate(folds(g,seed)):
            assert not set(g[tr])&set(g[te]);path=cache_root/f'seed-{seed}-fold-{fold}.json';train=[targets[i] for i in tr];oldtrain=[oldtargets[i] for i in tr]
            if path.exists():cache=json.loads(path.read_text());assert cache['source_hashes']==hashes
            else:
                choices,inner=calibration(train,oldtrain,seed+fold+16000);params={};outer={}
                for arm,cfg in choices.items():
                    beta=previous.fit(oldtrain if arm=='v15_recipe_control' else train,cfg['alpha']) if arm!='v16_direction_first' else fit_direction(train,cfg['alpha'])
                    params[arm]=beta.tolist();outer[arm]=(x[te]@beta).tolist()
                cache={'source_hashes':hashes,'seed':seed,'fold':fold,'training_ids':[targets[i]['id'] for i in tr],'validation_ids':[targets[i]['id'] for i in te],'choices':choices,'inner':inner,'coefficients':params,'outer_margins':outer}
                write_versioned(path,cache)
            assert cache['training_ids']==[targets[i]['id'] for i in tr] and cache['validation_ids']==[targets[i]['id'] for i in te]
            for arm,cfg in cache['choices'].items():margins[arm][te]=cache['outer_margins'][arm];radii[arm][te]=cfg['radius']
            audits.append({'seed':seed,'fold':fold,'choices':cache['choices'],'cache_file':str(path.relative_to(ROOT))});manifest.append({'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        for arm in ARMS:runs[arm].append({'seed':seed,'margins':margins[arm].tolist(),'radii':radii[arm].tolist(),'score':score(targets,margins[arm],radii[arm],direct)})
        print(f'Completed simple v16 validation repeat {seed}',flush=True)
    summary=summarize(runs);winner,checks=choose_delivery(summary);choices,inner=calibration(targets,oldtargets,1301);full={}
    oldmodel=json.loads((ROOT/'meaningful-benchmark-v15.json').read_text())
    assert choices['v15_recipe_control']['alpha']==oldmodel['alpha'] and choices['v15_recipe_control']['radius']==oldmodel['decision_radius']
    for arm,cfg in choices.items():
        beta=previous.fit(oldtargets if arm=='v15_recipe_control' else targets,cfg['alpha']) if arm!='v16_direction_first' else fit_direction(targets,cfg['alpha'])
        if arm=='v15_recipe_control':np.testing.assert_allclose(beta,oldmodel['coefficients'],rtol=0,atol=1e-10)
        full[arm]={'kind':arm,'trained_evidence':'evidence-v15.json' if arm=='v15_recipe_control' else 'evidence-v16.json','alpha':cfg['alpha'],'decision_radius':cfg['radius'],'coefficients':beta.tolist(),'feature_names':base.FEATURES,'training_score':score(targets,x@beta,cfg['radius'],direct)}
    result={'method':{'source_hashes':hashes,'protocol':json.loads((ROOT/'simple_benchmark_validation_protocol_v16.json').read_text()),'lookup_policy':'No evidence retrieval in any prediction path: outer margins=x_test@beta_train. No pricing_resolved imports. All thresholds learned inside training partitions.','limits':'Repeated family validation after adaptive evidence collection, not a fresh prospective test. Most positive materiality targets are qualifier proxies; directly supported positives only one. No money calibration.'},'row_ids':[r['id'] for r in targets],'nested_cv':{'runs':runs,'summary':summary,'fold_audits':audits},'cache_manifest':manifest,'full_data_choices':choices,'full_data_models':full,'full_data_calibration':inner,'delivery':{'selected':winner,'checks':checks}}
    write_versioned(ROOT/'simple-benchmark-validation-v16.json',result)
    delivery={'selected_model':winner,'model':full[winner],'evidence':'evidence-v16.json','target_view':'benchmark-targets-v16.json','validation_file':'simple-benchmark-validation-v16.json','validation_sha256':hashlib.sha256((ROOT/'simple-benchmark-validation-v16.json').read_bytes()).hexdigest(),'validation':summary[winner],'prediction_source':'coefficients only; no recorded-answer lookup','qualification':'Direction and materiality estimated separately; no exact-price assertion or calibrated dollar amount.238 unknown materialities excluded from size scoring.'}
    write_versioned(ROOT/'simple-benchmark-v16-delivery.json',delivery)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'selected':winner,'summary':summary,'checks':checks,'full_settings':choices},indent=2))

if __name__=='__main__':main()
