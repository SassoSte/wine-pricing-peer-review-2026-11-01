"""One-parameter context calibration with frozen direction models and no lookups."""
from pathlib import Path
from copy import deepcopy
import hashlib,json
import numpy as np
import compare_models as base
import domestic_shade_model as underlying
import precision_shade_model as fit_underlying
import refit_simple_benchmark_v16 as metrics
import validate_domestic_shade_v17 as parent_folds
import contextual_meaningfulness as context
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent
ARMS=('v16_control','v17_precision','matched_control','mature_shade','shared_light_tare','selected_context')
SOURCES=('evidence-v17.json','evidence-v18.json','benchmark-targets-v18.json','round37-fixed.json','build_evidence_v18.py','simple-benchmark-validation-v16.json','precision-shade-validation-v17.json','precision-shade-candidate-v17.json','domestic-shade-validation-v17.json','domestic_shade_model.py','precision_shade_model.py','contextual_meaningfulness.py','contextual-meaningfulness-protocol-v18.json','validate_contextual_meaningfulness_v18.py')


def extend_folds(groups,old_groups,old_folds,k,seed):
    assignment={}
    for i,(_,test) in enumerate(old_folds):
        for g in set(old_groups[test]):assignment[g]=i
    sizes=np.array([sum(assignment.get(g)==i for g in groups) for i in range(k)]);extra=sorted(set(groups)-set(assignment));np.random.default_rng(seed).shuffle(extra);extra.sort(key=lambda g:-sum(groups==g))
    for g in extra:i=int(np.argmin(sizes));assignment[g]=i;sizes[i]+=sum(groups==g)
    bins=np.array([assignment[g] for g in groups])
    for i in range(k):yield np.flatnonzero(bins!=i),np.flatnonzero(bins==i)


def outer_folds(groups,seed):return extend_folds(groups,groups[:425],list(parent_folds.folds(groups[:425],seed)),5,seed)


def calibration_inputs(targets,evidence,oldtargets,oldevidence,partitions,configuration):
    index={r['id']:i for i,r in enumerate(targets)};old_index={r['id']:i for i,r in enumerate(oldtargets)};_,_,_,groups=metrics.previous.arrays(targets);_,_,_,oldgroups=metrics.previous.arrays(oldtargets)
    old_folds=[(np.array([old_index[i] for i in p['training_ids']]),np.array([old_index[i] for i in p['validation_ids']])) for p in partitions]
    splits=list(extend_folds(groups,oldgroups,old_folds,3,18001));margins=np.zeros(len(targets));radii=np.zeros(len(targets));features={kind:np.zeros(len(targets)) for kind in context.KINDS};audit=[]
    for fold,(_,va) in enumerate(splits):
        p=partitions[fold];train=[oldtargets[old_index[i]] for i in p['training_ids']];ev=[oldevidence[old_index[i]] for i in p['training_ids']];valid=[targets[i] for i in va]
        _,_,_,tg=metrics.previous.arrays(train);_,_,_,vg=metrics.previous.arrays(valid);assert not set(tg)&set(vg)
        beta=fit_underlying.fit(train,ev,configuration['alpha'],configuration['training_radius'],configuration['weight']);radius=parent_folds.effective_radius(beta,configuration['training_radius']);x=underlying.arrays(valid)[0];margins[va]=x@beta;radii[va]=radius
        for kind in context.KINDS:features[kind][va]=[context.context_feature(r['a'],r['b'],beta,radius,kind) for r in valid]
        audit.append({'fold':fold,'underlying_training_ids':p['training_ids'],'calibration_validation_ids':[r['id'] for r in valid],'configuration':configuration,'coefficients':beta.tolist(),'base_radius':radius})
    return {'row_ids':[r['id'] for r in targets],'margins':margins.tolist(),'base_radii':radii.tolist(),'context_features':{k:v.tolist() for k,v in features.items()},'partitions':audit}


def choose(targets,inputs):
    _,material,_,_=metrics.previous.arrays(targets);m=np.array(inputs['margins']);r=np.array(inputs['base_radii']);positive=np.isfinite(material)&(material!=0);protect=positive&(abs(m)>r);choices={};search={}
    for kind in context.KINDS:
        best=None;selected=None;search[kind]=[];f=np.array(inputs['context_features'][kind])
        for eta in context.ETAS:
            radii=r*(1+eta*f);preserve=bool(np.all(abs(m[protect])>radii[protect]));s=metrics.score(targets,m,radii);key=(round(s['materiality']['balanced_accuracy'],12),-s['materiality']['false_meaningful'],-eta)
            search[kind].append({'eta':eta,'eligible':preserve,'score':s})
            if preserve and (best is None or key>best):best=key;selected={'kind':kind,'eta':eta,'selection_score':s}
        assert selected is not None;choices[kind]=selected
    selected=max([choices['mature_shade'],choices['shared_light_tare']],key=lambda c:(round(c['selection_score']['materiality']['balanced_accuracy'],12),-c['selection_score']['materiality']['false_meaningful'],-c['eta'],c['kind']=='mature_shade'))
    choices['selected_context']=deepcopy(selected)
    return choices,search


def delivery_choice(summary):
    v16=summary['v16_control'];old=summary['v17_precision'];checks={};eligible=[];eps=1e-10
    for kind in ('mature_shade','shared_light_tare','selected_context'):
        s=summary[kind];g={'direction_unchanged':abs(s['direction']['accuracy']-old['direction']['accuracy'])<eps,'false_calls_reduced':s['materiality']['false_meaningful']<old['materiality']['false_meaningful']-eps,'false_calls_at_most_v16':s['materiality']['false_meaningful']<=v16['materiality']['false_meaningful']+eps,'balanced_materiality_noninferior':s['materiality']['balanced_accuracy']+eps>=max(v16['materiality']['balanced_accuracy'],old['materiality']['balanced_accuracy']),'meaningful_recall_preserved':s['materiality']['meaningful_recall']+eps>=old['materiality']['meaningful_recall'],'direct_materiality_preserved':s['directly_supported_materiality']['accuracy']+eps>=old['directly_supported_materiality']['accuracy']}
        checks[kind]=g
        if all(g.values()):eligible.append(kind)
    winner=max(eligible,key=lambda k:(summary[k]['materiality']['balanced_accuracy'],-summary[k]['materiality']['false_meaningful'],k=='selected_context')) if eligible else 'v17_precision'
    return winner,checks


def main():
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in SOURCES};targets=json.loads((ROOT/'benchmark-targets-v18.json').read_text())['rows'];evidence=json.loads((ROOT/'evidence-v18.json').read_text())['rows'];old=json.loads((ROOT/'precision-shade-validation-v17.json').read_text());v16=json.loads((ROOT/'simple-benchmark-validation-v16.json').read_text());v17source=json.loads((ROOT/'domestic-shade-validation-v17.json').read_text());fullbase=json.loads((ROOT/'precision-shade-candidate-v17.json').read_text())['model'];index={r['id']:i for i,r in enumerate(targets)}
    oldhash={c['file']:c['sha256'] for c in old['cache_manifest']};v16hash={c['file']:c['sha256'] for c in v16['cache_manifest']};_,_,_,g=metrics.previous.arrays(targets);direct=metrics.verified_materiality(evidence);runs={name:[] for name in ARMS};audits=[];manifest=[];root=ROOT/'contextual-meaningfulness-cache-v18';root.mkdir(exist_ok=True)
    for seed in metrics.SEEDS:
        ms={a:np.zeros(len(targets)) for a in ARMS};rs={a:np.zeros(len(targets)) for a in ARMS}
        for fold,(tr,te) in enumerate(outer_folds(g,seed)):
            op=f'precision-shade-cache-v17/seed-{seed}-fold-{fold}.json';bp=f'simple-cache-v16/seed-{seed}-fold-{fold}.json';assert hashlib.sha256((ROOT/op).read_bytes()).hexdigest()==oldhash[op];assert hashlib.sha256((ROOT/bp).read_bytes()).hexdigest()==v16hash[bp];oc=json.loads((ROOT/op).read_text());bc=json.loads((ROOT/bp).read_text())
            assert oc['training_ids']==[targets[i]['id'] for i in tr if i<425];assert bc['training_ids']==[targets[i]['id'] for i in tr if i<413]
            test=[targets[i] for i in te];x18=metrics.previous.arrays(test)[0];x19=underlying.arrays(test)[0];beta=np.array(oc['coefficients']['v17_precision_weighted']);radius=oc['decision_radii']['v17_precision_weighted'];base_m=x19@beta
            ms['v17_precision'][te]=base_m;rs['v17_precision'][te]=radius;ms['v16_control'][te]=x18@np.array(bc['coefficients']['v16_blended']);rs['v16_control'][te]=bc['choices']['v16_blended']['radius']
            train=[targets[i] for i in tr];ev=[evidence[i] for i in tr];oldtrain=[targets[index[i]] for i in oc['training_ids']];oldev=[evidence[index[i]] for i in oc['training_ids']];path=root/f'seed-{seed}-fold-{fold}.json'
            if path.exists():cache=json.loads(path.read_text());assert cache['source_hashes']==hashes
            else:
                config=oc['choices']['v17_precision_weighted'];inputs=calibration_inputs(train,ev,oldtrain,oldev,oc['inner_partitions'],config)
                # Old rows reproduce the cached training-only baseline predictions.
                pos={q['id']:i for i,q in enumerate(train)};shared=[pos[i] for i in oc['training_ids']];cached=oc['inner_pool'][config['key']]
                np.testing.assert_allclose(np.array(inputs['margins'])[shared],cached['margins'],rtol=0,atol=1e-8)
                choices,search=choose(train,inputs);cache={'source_hashes':hashes,'seed':seed,'fold':fold,'training_ids':[q['id'] for q in train],'validation_ids':[q['id'] for q in test],'underlying_baseline_cache':op,'underlying_coefficients':beta.tolist(),'base_radius':radius,'inputs':inputs,'choices':choices,'search':search};write_versioned(path,cache)
            assert cache['training_ids']==[q['id'] for q in train]
            for arm in ARMS[2:]:
                choice=cache['choices'][arm];ms[arm][te]=base_m;rs[arm][te]=[context.radius(q['a'],q['b'],beta,radius,choice['kind'],choice['eta']) for q in test]
            audits.append({'seed':seed,'fold':fold,'choices':cache['choices'],'cache_file':str(path.relative_to(ROOT))});manifest.append({'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()});print(f'Completed contextual boundary seed {seed}, fold {fold+1}/5',flush=True)
        ov=next(v for v in old['nested_cv']['runs']['v17_precision_weighted'] if v['seed']==seed);np.testing.assert_allclose(ms['v17_precision'][:425],ov['margins'],rtol=0,atol=1e-10)
        b=next(v for v in v16['nested_cv']['runs']['v16_blended'] if v['seed']==seed);np.testing.assert_allclose(ms['v16_control'][:413],b['margins'],rtol=0,atol=1e-10)
        for arm in ARMS:runs[arm].append({'seed':seed,'margins':ms[arm].tolist(),'radii':rs[arm].tolist(),'score':metrics.score(targets,ms[arm],rs[arm],direct)})
    summary=metrics.summarize(runs);winner,gates=delivery_choice(summary)
    config=old['full_data_choices']['v17_precision_weighted'];inputs=calibration_inputs(targets,evidence,targets[:425],evidence[:425],v17source['full_data_calibration']['partitions'],config);choices,search=choose(targets,inputs);choice=choices[winner] if winner!='v17_precision' else {'kind':'mature_shade','eta':0.}
    model={'kind':'contextual_meaningfulness','underlying_source':'precision-shade-candidate-v17.json','underlying_coefficients':fullbase['coefficients'],'base_radius':fullbase['decision_radius'],'context_kind':choice['kind'],'context_coefficient':choice['eta'],'direction_weights_changed':False,'calibration_evidence':'evidence-v18.json'}
    beta=np.array(model['underlying_coefficients']);full_m=underlying.arrays(targets)[0]@beta;full_r=np.array([context.radius(q['a'],q['b'],beta,model['base_radius'],model['context_kind'],model['context_coefficient']) for q in targets])
    result={'method':{'source_hashes':hashes,'protocol':json.loads((ROOT/'contextual-meaningfulness-protocol-v18.json').read_text()),'baseline_cache_hashes':oldhash,'v16_cache_hashes':v16hash,'lookup_policy':'All direction predictions use frozen coefficients; contextual radius uses only attributes, frozen provenance offsets, and one calibrated scalar. No recorded-answer retrieval.','limits':'Context hypotheses derived from prior qualitative guidance and observed feature collision. Repeated-family validation is exploratory; no causal identification or fresh-test claim.'},'row_ids':[q['id'] for q in targets],'nested_cv':{'runs':runs,'summary':summary,'fold_audits':audits},'cache_manifest':manifest,'full_data_calibration':{'inputs':inputs,'choices':choices,'search':search},'delivery':{'selected':winner,'checks':gates},'candidate_model':model,'full_data_score':metrics.score(targets,full_m,full_r,direct)}
    write_versioned(ROOT/'contextual-meaningfulness-validation-v18.json',result)
    artifact={'selected_model':winner,'model':model,'evidence':'evidence-v18.json','validation_file':'contextual-meaningfulness-validation-v18.json','validation_sha256':hashlib.sha256((ROOT/'contextual-meaningfulness-validation-v18.json').read_bytes()).hexdigest(),'validation':summary[winner],'prediction_source':'frozen utility coefficients plus one context calibration parameter; no answer lookup','qualification':'Context-dependent practical meaningfulness, not exact price equality or dollar calibration. Both baselines unchanged.'}
    write_versioned(ROOT/'contextual-meaningfulness-delivery-v18.json',artifact)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'winner':winner,'summary':summary,'checks':gates,'full_choices':choices},indent=2))

if __name__=='__main__':main()
