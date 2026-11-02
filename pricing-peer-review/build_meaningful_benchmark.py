"""Scoped tare clarification and one small benchmark for a fresh materiality test."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import hashlib,json
import numpy as np
from scipy.optimize import minimize
import compare_models as base
from reconcile_and_compare import write_versioned

ROOT=Path(__file__).resolve().parent
CLARIFICATION="2. Practically similar—a tiny premium for the lighter vessel may exist, but a 5 lb difference alone isn't enough to make a meaningful distinction when everything else matches."
STRONG={'moderately','strongly','overwhelmingly','much more','much more valuable','easily'}
ALPHAS=(.001,.01,.1,1.)
RADII=(.1,.2,.25,.3,.5,.75)


def target_view(rows):
    targets=[]
    for row in rows:
        winner=row['winner'];direction=1 if winner=='A' else -1 if winner=='B' else 0
        matched5=row['a'][:3]==row['b'][:3] and abs(row['a'][3]-row['b'][3])==5
        if matched5:
            value=0;basis='user clarified matched5lb tare differences as not meaningful; any known direction retained'
        elif winner=='practical_similarity':value=0;basis='explicit practical similarity'
        elif winner=='tie':value=0;basis='coarsened recorded tie: no expressed meaningful preference; exact/practical interpretation remains as audited'
        elif row.get('strength') in STRONG:value=direction;basis='qualifier-derived meaningfulness PROXY; explicit moderate/strong language, not a numeric economic anchor'
        else:value=None;basis='direction known; meaningfulness unspecified, not assumed from A/B or slight adjective'
        targets.append({'id':row['id'],'a':row['a'],'b':row['b'],'known_direction':direction if direction else None,'materiality_target':value,'basis':basis,'strength':row.get('strength')})
    return targets


def arrays(targets):
    x=np.array([base.features(r['a'])-base.features(r['b']) for r in targets])
    material=np.array([np.nan if r['materiality_target'] is None else r['materiality_target'] for r in targets]);direction=np.array([r['known_direction'] or 0 for r in targets])
    g=np.array([repr((tuple(sorted((r['a'][0],r['b'][0]))),tuple(sorted((r['a'][1],r['b'][1]))))) for r in targets])
    return x,material,direction,g


def objective(beta,x,material,direction,alpha):
    m=x@beta;res=np.zeros(len(m));value=0.
    meaningful=np.isfinite(material)&(material!=0);similar=material==0
    # Unit1 separates meaningful examples;0.05 is numerical sign separation for
    # direction-only judgments, not an elicited premium magnitude.
    h=np.maximum(0.,1-material[meaningful]*m[meaningful]);value+=h@h;res[meaningful]-=material[meaningful]*h
    h=np.maximum(0.,abs(m[similar])-.25);value+=h@h;res[similar]+=np.sign(m[similar])*h
    directional=(direction!=0)&~meaningful
    h=np.maximum(0.,.05-direction[directional]*m[directional]);value+=h@h;res[directional]-=direction[directional]*h
    return float(value+alpha*(beta@beta)),2*x.T@res+2*alpha*beta


def fit(targets,alpha):
    x,m,d,_=arrays(targets)
    r=minimize(objective,np.zeros(18),args=(x,m,d,alpha),jac=True,method='L-BFGS-B',bounds=[(None,None)]*9+[(0,None)]*9,options={'ftol':1e-12,'gtol':1e-7,'maxiter':3000})
    if not r.success:raise RuntimeError(r.message)
    return r.x


def predict(margins,radius):return np.where(margins>radius,1,np.where(margins<-radius,-1,0))


def materiality_metrics(material,pred):
    known=np.isfinite(material);meaningful=known&(material!=0);similar=material==0
    recalls=[float(np.mean(pred[mask]==material[mask])) for mask in [meaningful,similar] if np.any(mask)]
    return {'known_n':int(sum(known)),'meaningful_proxy_n':int(sum(meaningful)),'no_meaningful_preference_n':int(sum(similar)),'balanced_accuracy':float(np.mean(recalls)),'accuracy':float(np.mean(pred[known]==material[known])),'note':'Calibration diagnostics on a coarsened/partly proxy target, not independent or dollar-price validation.'}


def main():
    files=['evidence-v12.json','equality-wording-audit-v12.json','pricing-reset-plan.json','compare_models.py','build_meaningful_benchmark.py']
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}
    old=json.loads((ROOT/'evidence-v12.json').read_text());audit=json.loads((ROOT/'equality-wording-audit-v12.json').read_text());rows=deepcopy(old['rows']);ids=set(audit['hard_tare_constraints']['ids']);changes=[];qualified=[]
    for row in rows:
        matched5=row['a'][:3]==row['b'][:3] and abs(row['a'][3]-row['b'][3])==5
        if row['id'] in ids:
            assert row['winner']=='tie' and matched5;previous=deepcopy(row)
            row.update(winner='practical_similarity',judgment_type='practical_similarity',direction=None,strength=None)
            row['semantic_reconciliation']={'source':'reset-semantics-1','raw_answer':CLARIFICATION,'prior_version':'evidence-v12.json','prior_row':previous,'scope':'Previously equal-labeled otherwise matched5lb tare comparisons; user explicitly chose practical similarity. No direction or numerical premium invented.'}
            changes.append(row['id'])
        if matched5:
            row['materiality_clarification']={'value':'no_meaningful_difference','source':'reset-semantics-1','raw_answer':CLARIFICATION,'scope':'Five pounds alone with provenance/shade/vintage matched. Any existing strict direction is retained separately.'}
            if row['winner'] in ('A','B'):qualified.append(row['id'])
    assert len(changes)==27 and len(qualified)==5
    assert Counter(r['winner'] for r in rows)=={'A':176,'B':83,'tie':109,'practical_similarity':33}
    ev={'version':13,'parent':'evidence-v12.json','parent_sha256':hashes['evidence-v12.json'],'row_count':401,'label_counts':dict(Counter(r['winner'] for r in rows)),'source_hashes':hashes,'clarification':{'id':'reset-semantics-1','raw_answer':CLARIFICATION,'reclassified_ids':changes,'direction_retained_materiality_qualified_ids':qualified},'unresolved_pairs':deepcopy(old['unresolved_pairs']),'equality_wording_audit_reference':'equality-wording-audit-v12.json','protocol':'Only27 retained matched5lb ties become practical similarity;5 existing matched5lb strict directions retained with separate not-meaningful qualification. Other labels unchanged. Earlier exact/practical ambiguity remains visible. No extra samples, no invented premium directions or monetary tolerances.','rows':rows}
    write_versioned(ROOT/'evidence-v13.json',ev)
    targets=target_view(rows)
    view={'evidence':'evidence-v13.json','evidence_sha256':hashlib.sha256((ROOT/'evidence-v13.json').read_bytes()).hexdigest(),'protocol':'Meaningfulness primary, known direction secondary. Historical ties are coarsened only to absence of expressed meaningful preference, never forced zero. Moderate/strong qualifiers are flagged positive proxies pending fresh direct validation. Unspecified meaningfulness remains missing, not silently converted. Exact-price semantics remain in original evidence/audit.','materiality_counts':dict(Counter('unspecified' if r['materiality_target'] is None else 'no_meaningful_difference' if r['materiality_target']==0 else 'meaningful_proxy' for r in targets)),'rows':targets}
    write_versioned(ROOT/'benchmark-targets-v13.json',view)
    x,material,direction,g=arrays(targets);scores={};best=None;choice=None
    for alpha in ALPHAS:
        margins=np.zeros(len(rows))
        for tr,va in base.folds(g,3,1301):margins[va]=x[va]@fit([targets[i] for i in tr],alpha)
        for radius in RADII:
            metrics=materiality_metrics(material,predict(margins,radius));key=(round(metrics['balanced_accuracy'],12),round(metrics['accuracy'],12),alpha,radius)
            scores[f'{alpha}/{radius}']=metrics
            if best is None or key>best:best=key;choice=(alpha,radius)
    alpha,radius=choice;beta=fit(targets,alpha)
    result={'status':'fitted simple benchmark; not prospectively validated','evidence':'evidence-v13.json','target_view':'benchmark-targets-v13.json','source_hashes':hashes,'architecture':'18 additive coefficients:9 provenance offsets,4 monotone shade increments,4 monotone vintage increments,1 nonnegative lighter-tare slope. No regional hierarchy overlays, context curves, fusion, or hard zero-price constraints.','target_cautions':view['protocol'],'loss_conventions':{'meaningful_proxy_unit_margin':1,'direction_only_numerical_margin':.05,'practical_training_band':.25,'note':'Model-scale conventions, not user-supplied percentages or prices. One observation can constrain direction and practical closeness without becoming two samples.'},'alpha':alpha,'decision_radius':radius,'coefficients':beta.tolist(),'feature_names':base.FEATURES,'inner_calibration_scores':scores,'materiality_counts':view['materiality_counts'],'next':'Freeze a short fresh batch with direct meaningfulness options; no model updates during it. No claimed new accuracy until those answers exist.'}
    write_versioned(ROOT/'meaningful-benchmark-v13.json',result)
    for f,h in hashes.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    print(json.dumps({'evidence':ev['label_counts'],'primary_targets':view['materiality_counts'],'benchmark_parameters':len(beta),'alpha':alpha,'radius':radius,'prior_models_unchanged':True}))

if __name__=='__main__':main()
