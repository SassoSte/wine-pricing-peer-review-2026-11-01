from pathlib import Path
import json,hashlib
import numpy as np
import five_year_premium_v23 as model
import joint_objective_v22 as joint
import refit_simple_benchmark_v16 as metrics
from validate_contextual_meaningfulness_v18 import extend_folds
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
ARMS=('joint_weight_refit','adjacent_shade','same_provenance')
SOURCES=['evidence-v22.json','evidence-v23.json','benchmark-targets-v23.json','round42-fixed.json','direct-joint-weights-delivery-v22.json','direct-joint-weights-validation-v22.json','five_year_premium_v23.py','validate_five_year_premium_v23.py','joint_weight_refit_v22.py','joint_objective_v22.py']
def main():
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in SOURCES};old=json.loads((R/'direct-joint-weights-validation-v22.json').read_text());t=json.loads((R/'benchmark-targets-v23.json').read_text())['rows'];e=json.loads((R/'evidence-v23.json').read_text())['rows'];ix={q['id']:i for i,q in enumerate(t)};groups=model.base.utility.arrays(t)[3];direct=metrics.verified_materiality(e);runs={a:[] for a in ARMS};audits=[]
 for seed in metrics.SEEDS:
  fs=sorted([q for q in old['nested_cv']['fold_audits'] if q['seed']==seed],key=lambda q:q['fold']);oldsplit=[(np.array([ix[i] for i in f['training_ids']]),np.array([ix[i] for i in f['validation_ids']])) for f in fs];mm={a:np.zeros(len(t)) for a in ARMS};rr=np.zeros(len(t))
  for fold,(tr,te) in enumerate(extend_folds(groups,groups[:479],oldsplit,5,seed)):
   f=fs[fold];cfg={**f['fit'],'reference_context':f['reference_context']};assert [t[i]['id'] for i in tr if i<479]==f['training_ids'];assert not set(groups[tr])&set(groups[te]);train=[t[i] for i in tr];test=[t[i] for i in te];g,r,h=model.components(test,cfg,'adjacent_shade');mm['joint_weight_refit'][te]=g;rr[te]=r;choices={}
   for arm in ARMS[1:]:
    c=model.fit(train,cfg,arm);choices[arm]=c;g,r,h=model.components(test,cfg,arm);mm[arm][te]=g+c['five_year_fraction']*h
   audits.append({'seed':seed,'fold':fold,'training_ids':[t[i]['id'] for i in tr],'validation_ids':[t[i]['id'] for i in te],'base_model':cfg,'choices':choices})
  prior=next(q for q in old['nested_cv']['runs']['direct_joint_refit'] if q['seed']==seed);np.testing.assert_allclose(mm['joint_weight_refit'][:479],prior['margins'],atol=1e-12);np.testing.assert_allclose(rr[:479],prior['radii'],atol=1e-12)
  for arm in ARMS:runs[arm].append({'seed':seed,'margins':mm[arm].tolist(),'radii':rr.tolist(),'score':metrics.score(t,mm[arm],rr,direct),'joint_score':joint.score(t,mm[arm],rr)})
 summary=metrics.summarize(runs);js={a:{k:float(np.mean([q['joint_score'][k] for q in series])) for k in ('both_axes_correct','both_axes_accuracy','balanced_accuracy','signed_joint_loss')} for a,series in runs.items()};base=summary['joint_weight_refit'];checks={}
 for a in ARMS[1:]:
  s=summary[a];checks[a]={'joint_improves':js[a]['balanced_accuracy']>js['joint_weight_refit']['balanced_accuracy']+1e-10,'both_axes_noninferior':js[a]['both_axes_accuracy']>=js['joint_weight_refit']['both_axes_accuracy']-1e-10,'direction_noninferior':s['direction']['accuracy']>=base['direction']['accuracy']-1e-10,'false_premiums_noninferior':s['materiality']['false_meaningful']<=base['materiality']['false_meaningful']+1e-10,'correct_meaningful_noninferior':s['materiality']['correct_meaningful_direction']>=base['materiality']['correct_meaningful_direction']-1e-10}
 eligible=[a for a in ARMS[1:] if all(checks[a].values())];winner=max(eligible,key=lambda a:(js[a]['balanced_accuracy'],a=='adjacent_shade')) if eligible else 'joint_weight_refit';cfg=json.loads((R/'direct-joint-weights-delivery-v22.json').read_text())['model'];full={a:{'base_model':cfg,**({'five_year_fraction':0.,'scope':'adjacent_shade'} if a=='joint_weight_refit' else model.fit(t,cfg,a))} for a in ARMS}
 result={'source_hashes':hashes,'protocol':'One bounded fraction0..1 adds up to one existing five-year age-step premium for matched provenance and exactly5-year gap. Primary scope golden/pale contrasts, comparison broader all-shades scope. Age direction determines sign; no recorded winner lookup. Joint four-group accuracy, both-axis accuracy, signed-loss tie-break; coefficient fit only training families. Original frozen refit folds extended label-free; all old479 predictions reproduce. Missing axes excluded, unresolved labels never inferred. Fixed decision boundaries/underlying weights. Zero130 and pure5lb unaffected by exact5-year gate. Exploratory reused families; no prospective claim.','row_ids':[q['id'] for q in t],'nested_cv':{'runs':runs,'summary':summary,'joint_summary':js,'fold_audits':audits},'full_models':full,'recent_predictions':{a:{q['id']:model.predict(q['a'],q['b'],c) for q in t if q['id'].startswith(('round41-','round42-')) or q['id']=='revision-13'} for a,c in full.items()},'delivery':{'selected':winner,'checks':checks}}
 write_versioned(R/'five-year-premium-validation-v23.json',result);write_versioned(R/'five-year-premium-delivery-v23.json',{'selected_model':winner,'model':full[winner],'evidence':'evidence-v23.json','validation_file':'five-year-premium-validation-v23.json','validation':summary[winner],'joint_validation':js[winner],'baselines_unchanged':True})
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 print(json.dumps({'summary':summary,'joint':js,'delivery':result['delivery'],'fractions':{a:c['five_year_fraction'] for a,c in full.items()}},indent=2))
if __name__=='__main__':main()
