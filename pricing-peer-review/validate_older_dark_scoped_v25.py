from pathlib import Path
import json,hashlib
import numpy as np
import older_dark_scoped_v25 as model
import joint_objective_v22 as joint
import refit_simple_benchmark_v16 as metrics
from validate_contextual_meaningfulness_v18 import extend_folds
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
ARMS=('v24','older','dark','combined')
SOURCES=['evidence-v24.json','evidence-v25.json','benchmark-targets-v25.json','round44-fixed.json','round45-fixed.json','five-year-premium-delivery-v24.json','five-year-premium-validation-v24.json','five_year_premium_v23.py','older_dark_scoped_v25.py','validate_older_dark_scoped_v25.py','joint_objective_v22.py']
def main():
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in SOURCES};old=json.loads((R/'five-year-premium-validation-v24.json').read_text());t=json.loads((R/'benchmark-targets-v25.json').read_text())['rows'];e=json.loads((R/'evidence-v25.json').read_text())['rows'];ix={q['id']:i for i,q in enumerate(t)};groups=model.baseline.base.utility.arrays(t)[3];direct=metrics.verified_materiality(e);runs={a:[] for a in ARMS};audits=[]
 for seed in metrics.SEEDS:
  fs=sorted([q for q in old['nested_cv']['fold_audits'] if q['seed']==seed],key=lambda q:q['fold']);splits=[(np.array([ix[i] for i in f['training_ids']]),np.array([ix[i] for i in f['validation_ids']])) for f in fs];mm={a:np.zeros(len(t)) for a in ARMS};rr=np.zeros(len(t))
  for fold,(tr,te) in enumerate(extend_folds(groups,groups[:491],splits,5,seed)):
   f=fs[fold];cfg={'base_model':f['base_model'],**f['choices']['adjacent_shade']};assert [t[i]['id'] for i in tr if i<491]==f['training_ids'];assert not set(groups[tr])&set(groups[te]);train=[t[i] for i in tr];test=[t[i] for i in te];g,r,h=model.components(test,cfg);rr[te]=r;choices={}
   for arm in ARMS:
    c={'adjustments':[0.,0.,0.]} if arm=='v24' else model.fit(train,cfg,arm);choices[arm]=c;mm[arm][te]=g+h@c['adjustments']
   audits.append({'seed':seed,'fold':fold,'training_ids':[t[i]['id'] for i in tr],'validation_ids':[t[i]['id'] for i in te],'base_model':cfg,'choices':choices})
  prior=next(q for q in old['nested_cv']['runs']['adjacent_shade'] if q['seed']==seed);np.testing.assert_allclose(mm['v24'][:491],prior['margins'],atol=1e-12);np.testing.assert_allclose(rr[:491],prior['radii'],atol=1e-12)
  for arm in ARMS:runs[arm].append({'seed':seed,'margins':mm[arm].tolist(),'radii':rr.tolist(),'score':metrics.score(t,mm[arm],rr,direct),'joint_score':joint.score(t,mm[arm],rr)})
 summary=metrics.summarize(runs);js={a:{k:float(np.mean([q['joint_score'][k] for q in series])) for k in ('both_axes_correct','both_axes_accuracy','balanced_accuracy','signed_joint_loss')} for a,series in runs.items()};base=summary['v24'];checks={}
 for a in ARMS[1:]:
  s=summary[a];checks[a]={'joint_improves':js[a]['balanced_accuracy']>js['v24']['balanced_accuracy']+1e-10,'both_axes_noninferior':js[a]['both_axes_accuracy']>=js['v24']['both_axes_accuracy']-1e-10,'direction_noninferior':s['direction']['accuracy']>=base['direction']['accuracy']-1e-10,'false_premiums_noninferior':s['materiality']['false_meaningful']<=base['materiality']['false_meaningful']+1e-10,'correct_meaningful_noninferior':s['materiality']['correct_meaningful_direction']>=base['materiality']['correct_meaningful_direction']-1e-10}
 eligible=[a for a in ARMS[1:] if all(checks[a].values())];winner=max(eligible,key=lambda a:(js[a]['balanced_accuracy'],-ARMS.index(a))) if eligible else 'v24';cfg=json.loads((R/'five-year-premium-delivery-v24.json').read_text())['model'];full={a:{'base_model':cfg,**({'adjustments':[0.,0.,0.]} if a=='v24' else model.fit(t,cfg,a))} for a in ARMS}
 result={'source_hashes':hashes,'protocol':'Follow-up to preserved broader experiment: age correction restricted to matched provenance golden/pale35vs40, microshade correction restricted to same-provenance/age/tare amber/copper-only; brown step unchanged. These restrictions informed by observed collateral errors, validation remains exploratory. Three additive features: age35-vs40 cumulative step bounded0..2 baseline-radius units, brown->copper step0..2radius, copper->amber0..1 of available headroom below pure-shade meaningful radius. One older parameter, two dark parameters and three combined; joint objective same as prior. All fitting training-only with frozen v24 base weights/boundaries/context and original family splits extended label-free. Prior491 margins reproduce. Unresolved/missing axes never inferred. Pure5lb and zero golden/pale130 algebraically unchanged. Exploratory reused families; no prospective claim.','row_ids':[q['id'] for q in t],'nested_cv':{'runs':runs,'summary':summary,'joint_summary':js,'fold_audits':audits},'full_models':full,'recent_predictions':{a:{q['id']:model.predict(q['a'],q['b'],c) for q in t if q['id'].startswith(('round44-','round45-'))} for a,c in full.items()},'delivery':{'selected':winner,'checks':checks}}
 write_versioned(R/'older-dark-scoped-validation-v25.json',result);write_versioned(R/'older-dark-scoped-delivery-v25.json',{'selected_model':winner,'model':full[winner],'evidence':'evidence-v25.json','validation_file':'older-dark-scoped-validation-v25.json','validation':summary[winner],'joint_validation':js[winner],'baselines_unchanged':True})
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 print(json.dumps({'summary':summary,'joint':js,'delivery':result['delivery'],'parameters':{a:c['adjustments'] for a,c in full.items()}},indent=2))
if __name__=='__main__':main()
