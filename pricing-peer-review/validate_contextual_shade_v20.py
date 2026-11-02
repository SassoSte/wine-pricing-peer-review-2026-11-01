from pathlib import Path
import json,hashlib
import numpy as np
import contextual_shade_v20 as model
import refit_simple_benchmark_v16 as metrics
from validate_contextual_meaningfulness_v18 import extend_folds
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
SOURCES=['evidence-v19.json','evidence-v20.json','benchmark-targets-v20.json','contextual-fixes-validation-v19.json','contextual-fixes-delivery-v19.json','round39-fixed.json','contextual_shade_v20.py','validate_contextual_shade_v20.py','contextual_fixes_v19.py']
ARMS=('v19','heavy_only','two_contexts')
def main():
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in SOURCES};old=json.loads((R/'contextual-fixes-validation-v19.json').read_text());t=json.loads((R/'benchmark-targets-v20.json').read_text())['rows'];e=json.loads((R/'evidence-v20.json').read_text())['rows'];idx={q['id']:i for i,q in enumerate(t)};direct=metrics.verified_materiality(e);groups=model.previous.utility.arrays(t)[3];runs={a:[] for a in ARMS};audits=[]
 for seed in metrics.SEEDS:
  fs=sorted([a for a in old['nested_cv']['fold_audits'] if a['seed']==seed],key=lambda q:q['fold']);previous=[(np.array([idx[i] for i in f['training_ids']]),np.array([idx[i] for i in f['validation_ids']])) for f in fs];splits=extend_folds(groups,groups[:449],previous,5,seed);mm={a:np.zeros(len(t)) for a in ARMS};rr=np.zeros(len(t))
  for fold,(tr,te) in enumerate(splits):
   f=fs[fold];cfg={'underlying_coefficients':f['underlying_coefficients'],'base_radius':f['base_radius'],'context_kind':f['prior_context']['kind'],'context_coefficient':f['prior_context']['eta'],**f['choices']['boundary']};assert [t[i]['id'] for i in tr if i<449]==f['training_ids'];assert not set(groups[tr])&set(groups[te]);train=[t[i] for i in tr];test=[t[i] for i in te];g,r,h=model.arrays(test,cfg);rr[te]=r;choices={}
   for arm in ARMS:
    choice={'shade_coefficients':[0.,0.]} if arm=='v19' else model.fit(train,[e[i] for i in tr],cfg,arm);choices[arm]=choice;mm[arm][te]=g+h@choice['shade_coefficients']
   audits.append({'seed':seed,'fold':fold,'training_ids':[t[i]['id'] for i in tr],'validation_ids':[t[i]['id'] for i in te],'base_config':cfg,'choices':choices})
  baseline=next(q for q in old['nested_cv']['runs']['boundary'] if q['seed']==seed);np.testing.assert_allclose(mm['v19'][:449],baseline['margins'],atol=1e-12);np.testing.assert_allclose(rr[:449],baseline['radii'],atol=1e-12)
  for arm in ARMS:runs[arm].append({'seed':seed,'margins':mm[arm].tolist(),'radii':rr.tolist(),'score':metrics.score(t,mm[arm],rr,direct)})
  print('Completed seed',seed,flush=True)
 summary=metrics.summarize(runs);base=summary['v19'];checks={}
 for arm in ARMS[1:]:
  s=summary[arm];checks[arm]={'direction_noninferior':s['direction']['accuracy']>=base['direction']['accuracy']-1e-10,'balanced_size_noninferior':s['materiality']['balanced_accuracy']>=base['materiality']['balanced_accuracy']-1e-10,'false_premiums_noninferior':s['materiality']['false_meaningful']<=base['materiality']['false_meaningful']+1e-10,'missed_meaningful_noninferior':s['materiality']['missed_meaningful']<=base['materiality']['missed_meaningful']+1e-10,'direct_size_noninferior':s['directly_supported_materiality']['accuracy']>=base['directly_supported_materiality']['accuracy']-1e-10,'strict_improvement':s['direction']['accuracy']>base['direction']['accuracy']+1e-10 or s['materiality']['balanced_accuracy']>base['materiality']['balanced_accuracy']+1e-10}
 eligible=[a for a in ARMS[1:] if all(checks[a].values())];winner=max(eligible,key=lambda a:(summary[a]['direction']['accuracy']+summary[a]['materiality']['balanced_accuracy'],a=='heavy_only')) if eligible else 'v19'
 cfg=json.loads((R/'contextual-fixes-delivery-v19.json').read_text())['model'];full={}
 for arm in ARMS:full[arm]={**cfg,**({'shade_coefficients':[0.,0.]} if arm=='v19' else model.fit(t,e,cfg,arm)),'calibration_evidence':'evidence-v20.json'}
 predictions={a:{q['id']:model.predict(q['a'],q['b'],c) for q in t if q['id'].startswith(('round36-','round38-','round39-')) or q['id'] in ('revision-13','revision-14','round21-15')} for a,c in full.items()}
 result={'source_hashes':hashes,'protocol':'Prespecified one/two-parameter adjacent shade discount on matched foreign provenance and equal tare, with no age-tradeoff gate. Feature1 >=125lb allforeign; feature2 WesternEurope120lb supported by Round39, kept separate from earlier EE120 preference. Fractions bounded0..1 preserve weak pale ordering at matched age.21-point grid training objective same as v19; outer test labels never used to fit. Original v19 family splits extended label-free; base fits frozen. Pair-dependent comparison score: not standalone price or transitive utility. Exploratory reused-family validation and post-validation delivery gating; no prospective accuracy claim.','row_ids':[q['id'] for q in t],'nested_cv':{'runs':runs,'summary':summary,'fold_audits':audits},'full_models':full,'recent_full_predictions':predictions,'delivery':{'selected':winner,'checks':checks}}
 write_versioned(R/'contextual-shade-validation-v20.json',result);write_versioned(R/'contextual-shade-delivery-v20.json',{'selected_model':winner,'model':full[winner],'evidence':'evidence-v20.json','validation_file':'contextual-shade-validation-v20.json','validation':summary[winner],'baselines_unchanged':True})
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 print(json.dumps({'summary':summary,'delivery':result['delivery'],'coefficients':{a:c['shade_coefficients'] for a,c in full.items()}},indent=2))
if __name__=='__main__':main()
