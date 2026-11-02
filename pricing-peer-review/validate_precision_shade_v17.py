"""Reduce false premiums with train-only budgets and unchanged19-feature structure."""
from pathlib import Path
import ast,hashlib,json
import numpy as np
import domestic_shade_model as original_model
import precision_shade_model as model
import validate_domestic_shade_v17 as original
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent
WEIGHTS=(2.,4.)
ARMS=('v16_control','v17_original','v17_precision_selection','v17_precision_weighted')
SOURCES=tuple(dict.fromkeys((*original.SOURCES,'domestic-shade-validation-v17.json','domestic-shade-candidate-v17.json','precision_shade_model.py','precision-shade-protocol-v17.json','validate_precision_shade_v17.py')))


def old_pool(inner):
    result={}
    for key,output in inner['outputs']['v17_shade_protected'].items():
        alpha,radius=ast.literal_eval(key);result[str((1.,alpha,radius))]=output
    return result


def build_pool(targets,evidence,oldinner):
    pool=old_pool(oldinner);index={r['id']:i for i,r in enumerate(targets)};x,_,_,_=model.arrays(targets)
    for weight in WEIGHTS:
        for alpha in original.ALPHAS:
            for radius in original.RADII:pool[str((weight,alpha,radius))]={'margins':np.zeros(len(targets)),'radii':np.zeros(len(targets))}
    for partition in oldinner['partitions']:
        tr=[index[i] for i in partition['training_ids']];va=[index[i] for i in partition['validation_ids']];train=[targets[i] for i in tr];ev=[evidence[i] for i in tr]
        for weight in WEIGHTS:
            for alpha in original.ALPHAS:
                for radius in original.RADII:
                    beta=model.fit(train,ev,alpha,radius,weight);out=pool[str((weight,alpha,radius))];out['margins'][va]=x[va]@beta;out['radii'][va]=original.effective_radius(beta,radius)
    return {key:{k:v.tolist() if isinstance(v,np.ndarray) else v for k,v in out.items()} for key,out in pool.items()}


def select(targets,evidence,pool,original_choice,reference):
    index={r['id']:i for i,r in enumerate(targets)};shared=np.array([index[i] for i in reference['row_ids']]);refrows=[targets[i] for i in shared];refscore=original.previous.score(refrows,reference['margins'],reference['radius']);budget=refscore['materiality']['false_meaningful']
    original_key=str((1.,original_choice['alpha'],original_choice['training_radius']));old=pool[original_key];om=np.array(old['margins']);orr=np.array(old['radii']);_,mat,d,_=original.simple.arrays(targets);direct=np.array(original.previous.verified_materiality(evidence));os=np.where(om>1e-7,1,np.where(om<-1e-7,-1,0));size_correct=(abs(om)>orr)==(mat!=0);keep_size=direct&np.isfinite(mat)&size_correct;keep_direction=direct&(d!=0)&(os==d)
    records=[];eligible=[]
    for key,out in pool.items():
        weight,alpha,radius=ast.literal_eval(key);m=np.array(out['margins']);r=np.array(out['radii']);sign=np.where(m>1e-7,1,np.where(m<-1e-7,-1,0));size=(abs(m)>r)==(mat!=0);shared_score=original.previous.score(refrows,m[shared],r[shared]);allscore=original.previous.score(targets,m,r)
        gates={'false_call_budget':shared_score['materiality']['false_meaningful']<=budget,'shared_direction_noninferior':shared_score['direction']['accuracy']+1e-10>=refscore['direction']['accuracy'],'preserve_correct_direct_materiality':bool(np.all(size[keep_size])),'preserve_correct_direct_direction':bool(np.all((sign==d)[keep_direction]))}
        rec={'key':key,'weight':weight,'alpha':alpha,'training_radius':radius,'eligible':all(gates.values()),'checks':gates,'shared_score':shared_score,'score':allscore};records.append(rec)
        if rec['eligible']:eligible.append(rec)
    def rank(rec):
        s=rec['score'];a=s['direction']['accuracy'];b=s['materiality']['balanced_accuracy'];return (round(.5*(a+b),12),-s['materiality']['false_meaningful'],round(min(a,b),12),-s['direction']['reversals'],-rec['weight'],rec['alpha'],rec['training_radius'])
    selected=max(eligible,key=rank) if eligible else next(rec for rec in records if rec['key']==original_key)
    return {'weight':selected['weight'],'alpha':selected['alpha'],'training_radius':selected['training_radius'],'key':selected['key'],'budget_feasible':bool(eligible),'fallback_original_v17':not bool(eligible)}, {'v16_reference':reference,'v16_reference_score':refscore,'shared_negative_budget':budget,'shared_ids':reference['row_ids'],'preserved_direct_materiality_ids':[targets[i]['id'] for i in np.flatnonzero(keep_size)],'preserved_direct_direction_ids':[targets[i]['id'] for i in np.flatnonzero(keep_direction)],'candidate_scores':records}


def reference_cache(cache):
    c=cache['choices']['v16_blended']
    return {'row_ids':cache['training_ids'],'alpha':c['alpha'],'radius':c['radius'],'margins':cache['inner']['inner_margins']['v16_blended'][str(c['alpha'])],'source':'cached v16 inner out-of-fold predictions; each family excluded from its training fit'}


def extended_score(targets,evidence,m,radii):
    s=original.previous.score(targets,m,radii,original.previous.verified_materiality(evidence));idx={q['id']:i for i,q in enumerate(targets)}
    for name,ids in [('provenance_round36',[f'round36-{i}' for i in range(1,9)]),('shade_vintage_round36',[f'round36-{i}' for i in range(9,13)])]:
        indices=np.array([idx[i] for i in ids if i in idx]);sub=[targets[i] for i in indices];ev=[evidence[i] for i in indices];panel=original.previous.score(sub,np.asarray(m)[indices],np.asarray(radii)[indices],original.previous.verified_materiality(ev));_,mat,d,_=original.simple.arrays(sub);sign=np.where(np.asarray(m)[indices]>1e-7,1,np.where(np.asarray(m)[indices]<-1e-7,-1,0));correct=(sign==d)&((abs(np.asarray(m)[indices])>np.asarray(radii)[indices])==(mat!=0));panel['joint_correct']=int(sum(correct));s[name]=panel
    return s


def summarize(runs):
    summary=original.previous.summarize(runs)
    for arm,values in runs.items():
        for panel in ['provenance_round36','shade_vintage_round36']:
            summary[arm][panel]={'n':values[0]['score'][panel]['direction']['n'],'direction_accuracy':float(np.mean([r['score'][panel]['direction']['accuracy'] for r in values])),'materiality_accuracy':float(np.mean([r['score'][panel]['materiality']['accuracy'] for r in values])),'joint_correct':float(np.mean([r['score'][panel]['joint_correct'] for r in values]))}
    return summary


def delivery_choice(summary):
    base=summary['v16_control'];old=summary['v17_original'];checks={};eligible=[];eps=1e-10
    for arm in ARMS[2:]:
        s=summary[arm];g={'direction_at_least_v16':s['direction']['accuracy']+eps>=base['direction']['accuracy'],'balanced_materiality_at_least_v16':s['materiality']['balanced_accuracy']+eps>=base['materiality']['balanced_accuracy'],'reversals_at_most_v16':s['direction']['reversals']<=base['direction']['reversals']+eps,'false_calls_at_most_v16':s['materiality']['false_meaningful']<=base['materiality']['false_meaningful']+eps,'false_calls_less_than_v17':s['materiality']['false_meaningful']<old['materiality']['false_meaningful']-eps,'direct_materiality_preserved':s['directly_supported_materiality']['accuracy']+eps>=old['directly_supported_materiality']['accuracy'],'direct_meaningful_recall_preserved':s['directly_supported_materiality']['meaningful_recall']+eps>=old['directly_supported_materiality']['meaningful_recall'],'provenance_direction_preserved':s['provenance_round36']['direction_accuracy']+eps>=old['provenance_round36']['direction_accuracy'],'provenance_size_preserved':s['provenance_round36']['materiality_accuracy']+eps>=old['provenance_round36']['materiality_accuracy'],'shade_vintage_joint_preserved':s['shade_vintage_round36']['joint_correct']+eps>=old['shade_vintage_round36']['joint_correct']}
        checks[arm]=g
        if all(g.values()):eligible.append(arm)
    winner=max(eligible,key=lambda a:(.5*(summary[a]['direction']['accuracy']+summary[a]['materiality']['balanced_accuracy']),-summary[a]['materiality']['false_meaningful'])) if eligible else 'v17_original'
    return winner,checks


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in SOURCES};targets=json.loads((ROOT/'benchmark-targets-v17.json').read_text())['rows'];evidence=json.loads((ROOT/'evidence-v17.json').read_text())['rows'];old=json.loads((ROOT/'domestic-shade-validation-v17.json').read_text());v16=json.loads((ROOT/'simple-benchmark-validation-v16.json').read_text());oldhashes={r['file']:r['sha256'] for r in old['cache_manifest']};basehashes=old['method']['baseline_cache_hashes'];x,_,_,g=model.arrays(targets);runs={a:[] for a in ARMS};manifest=[];audits=[];root=ROOT/'precision-shade-cache-v17';root.mkdir(exist_ok=True)
    for seed in original.previous.SEEDS:
        margins={a:np.zeros(len(targets)) for a in ARMS[2:]};radii={a:np.zeros(len(targets)) for a in ARMS[2:]}
        for fold,(tr,te) in enumerate(original.folds(g,seed)):
            train=[targets[i] for i in tr];ev=[evidence[i] for i in tr];oldpath=f'domestic-shade-cache-v17/seed-{seed}-fold-{fold}.json';basepath=f'simple-cache-v16/seed-{seed}-fold-{fold}.json'
            assert hashlib.sha256((ROOT/oldpath).read_bytes()).hexdigest()==oldhashes[oldpath];assert hashlib.sha256((ROOT/basepath).read_bytes()).hexdigest()==basehashes[basepath]
            oc=json.loads((ROOT/oldpath).read_text());bc=json.loads((ROOT/basepath).read_text());assert oc['training_ids']==[r['id'] for r in train];path=root/f'seed-{seed}-fold-{fold}.json'
            if path.exists():c=json.loads(path.read_text());assert c['source_hashes']==hashes
            else:
                ref=reference_cache(bc);pool=build_pool(train,ev,oc['inner']);selection,audit_s=select(train,ev,old_pool(oc['inner']),oc['choices']['v17_shade_protected'],ref);weighted,audit_w=select(train,ev,pool,oc['choices']['v17_shade_protected'],ref);choices={'v17_precision_selection':selection,'v17_precision_weighted':weighted};params={};outer={};rr={}
                for arm,cfg in choices.items():
                    oldcfg=oc['choices']['v17_shade_protected']
                    if cfg['weight']==1. and cfg['alpha']==oldcfg['alpha'] and cfg['training_radius']==oldcfg['training_radius']:beta=np.array(oc['coefficients']['v17_shade_protected'])
                    else:beta=model.fit(train,ev,cfg['alpha'],cfg['training_radius'],cfg['weight'])
                    params[arm]=beta.tolist();outer[arm]=(x[te]@beta).tolist();rr[arm]=original.effective_radius(beta,cfg['training_radius'])
                c={'source_hashes':hashes,'seed':seed,'fold':fold,'training_ids':oc['training_ids'],'validation_ids':oc['validation_ids'],'inner_partitions':oc['inner']['partitions'],'inner_pool':pool,'choices':choices,'selection_audits':{'v17_precision_selection':audit_s,'v17_precision_weighted':audit_w},'coefficients':params,'outer_margins':outer,'decision_radii':rr};write_versioned(path,c)
            for arm in ARMS[2:]:margins[arm][te]=c['outer_margins'][arm];radii[arm][te]=c['decision_radii'][arm]
            manifest.append({'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()});audits.append({'seed':seed,'fold':fold,'choices':c['choices'],'cache_file':str(path.relative_to(ROOT))});print(f'Completed precision repair seed {seed}, fold {fold+1}/5',flush=True)
        for name,source in [('v16_control','v16_control'),('v17_original','v17_shade_protected')]:
            prior=next(r for r in old['nested_cv']['runs'][source] if r['seed']==seed);runs[name].append({'seed':seed,'margins':prior['margins'],'radii':prior['radii'],'score':extended_score(targets,evidence,prior['margins'],prior['radii'])})
        for arm in ARMS[2:]:runs[arm].append({'seed':seed,'margins':margins[arm].tolist(),'radii':radii[arm].tolist(),'score':extended_score(targets,evidence,margins[arm],radii[arm])})
    summaries=summarize(runs);winner,checks=delivery_choice(summaries)
    oc={'choices':old['full_data_choices'],'inner':old['full_data_calibration']};refcfg=v16['full_data_choices']['v16_blended'];ref={'row_ids':v16['row_ids'],'alpha':refcfg['alpha'],'radius':refcfg['radius'],'margins':v16['full_data_calibration']['inner_margins']['v16_blended'][str(refcfg['alpha'])],'source':'v16 full-data inner OOF predictions; no new425-row labels used by reference fits'}
    full_pool=build_pool(targets,evidence,oc['inner']);cs,as_=select(targets,evidence,old_pool(oc['inner']),oc['choices']['v17_shade_protected'],ref);cw,aw=select(targets,evidence,full_pool,oc['choices']['v17_shade_protected'],ref);choices={'v17_precision_selection':cs,'v17_precision_weighted':cw};full={'v17_original':old['full_data_models']['v17_shade_protected']}
    for arm,cfg in choices.items():
        beta=model.fit(targets,evidence,cfg['alpha'],cfg['training_radius'],cfg['weight']);radius=original.effective_radius(beta,cfg['training_radius']);margins=x@beta
        full[arm]={'kind':arm,'trained_evidence':'evidence-v17.json','alpha':cfg['alpha'],'legacy_negative_weight':cfg['weight'],'training_radius':cfg['training_radius'],'decision_radius':radius,'coefficients':beta.tolist(),'feature_names':old['full_data_models']['v17_shade_protected']['feature_names'],'training_score':extended_score(targets,evidence,margins,np.full(len(targets),radius)),'round36_training_predictions':[{'id':targets[i]['id'],'direction':'A' if margins[i]>1e-7 else 'B' if margins[i]<-1e-7 else None,'materiality':'meaningful_difference' if abs(margins[i])>radius else 'no_meaningful_difference'} for i in range(413,425)]}
    result={'method':{'source_hashes':hashes,'protocol':json.loads((ROOT/'precision-shade-protocol-v17.json').read_text()),'old_cache_hashes':oldhashes,'reference_cache_hashes':basehashes},'row_ids':[r['id'] for r in targets],'nested_cv':{'runs':runs,'summary':summaries,'fold_audits':audits},'cache_manifest':manifest,'full_data_choices':choices,'full_data_selection_audits':{'selection_only':as_,'weighted':aw},'full_data_models':full,'delivery':{'selected':winner,'checks':checks}}
    write_versioned(ROOT/'precision-shade-validation-v17.json',result)
    artifact={'selected_model':winner,'model':full[winner],'evidence':'evidence-v17.json','target_view':'benchmark-targets-v17.json','validation_file':'precision-shade-validation-v17.json','validation_sha256':hashlib.sha256((ROOT/'precision-shade-validation-v17.json').read_bytes()).hexdigest(),'validation':summaries[winner],'prediction_source':'model coefficients only; no answer lookup','qualification':'Exploratory paired validation; prior baselines unchanged; no numeric price calibration.'}
    write_versioned(ROOT/'precision-shade-delivery-v17.json',artifact)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'winner':winner,'summary':summaries,'checks':checks,'full_choices':choices},indent=2))

if __name__=='__main__':main()
