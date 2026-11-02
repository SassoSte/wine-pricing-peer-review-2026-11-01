from pathlib import Path
import json,hashlib
import numpy as np
import contextual_fixes_v19 as model
import refit_simple_benchmark_v16 as metrics
import validate_contextual_meaningfulness_v18 as oldfolds
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
ARMS=('v18','boundary','shade','combined')
SOURCES=['evidence-v18.json','evidence-v19.json','benchmark-targets-v19.json','contextual-boundary-fit-delivery-v18.json','contextual-boundary-fit-validation-v18.json','contextual-meaningfulness-validation-v18.json','precision-shade-candidate-v17.json','contextual_fixes_v19.py','validate_contextual_fixes_v19.py']
def main():
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in SOURCES}
 t=json.loads((R/'benchmark-targets-v19.json').read_text())['rows'];e=json.loads((R/'evidence-v19.json').read_text())['rows'];old=json.loads((R/'contextual-boundary-fit-validation-v18.json').read_text());cachemanifest=json.loads((R/'contextual-meaningfulness-validation-v18.json').read_text())['cache_manifest'];caches={}
 for entry in cachemanifest:
  p=R/entry['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'];c=json.loads(p.read_text());caches[c['seed'],c['fold']]=c
 _,_,_,groups=model.utility.arrays(t);direct=metrics.verified_materiality(e);runs={a:[] for a in ARMS};audits=[]
 for seed in metrics.SEEDS:
  margins={a:np.zeros(len(t)) for a in ARMS};radii={a:np.zeros(len(t)) for a in ARMS}
  splits=oldfolds.extend_folds(groups,groups[:437],list(oldfolds.outer_folds(groups[:437],seed)),5,seed)
  for fold,(tr,te) in enumerate(splits):
   c=caches[seed,fold];prior=next(a for a in old['nested_cv']['fold_audits'] if a['seed']==seed and a['fold']==fold)['choices']['selected_context'];beta=c['underlying_coefficients'];rad=c['base_radius'];kind=prior['kind'];eta=prior['eta'];train=[t[i] for i in tr];ev=[e[i] for i in tr];test=[t[i] for i in te]
   assert c['training_ids']==[t[i]['id'] for i in tr if i<437]
   assert not set(groups[tr])&set(groups[te]);g,h,r,f=model.components(test,beta,rad,kind,eta);choices={}
   for arm in ARMS:
    choice={'shade_fraction':0.,'boundary_increment':0.} if arm=='v18' else model.fit(train,ev,beta,rad,kind,eta,arm);choices[arm]=choice;margins[arm][te]=g+choice['shade_fraction']*h;radii[arm][te]=r+choice['boundary_increment']*f
   audits.append({'seed':seed,'fold':fold,'training_ids':[t[i]['id'] for i in tr],'validation_ids':[t[i]['id'] for i in te],'choices':choices,'underlying_coefficients':beta,'base_radius':rad,'prior_context':prior})
  original=next(q for q in old['nested_cv']['runs']['selected_context'] if q['seed']==seed)
  np.testing.assert_allclose(margins['v18'][:437],original['margins'],atol=1e-12);np.testing.assert_allclose(radii['v18'][:437],original['radii'],atol=1e-12)
  for arm in ARMS:runs[arm].append({'seed':seed,'margins':margins[arm].tolist(),'radii':radii[arm].tolist(),'score':metrics.score(t,margins[arm],radii[arm],direct)})
  print('Completed seed',seed,flush=True)
 summary=metrics.summarize(runs);base=summary['v18'];checks={}
 for arm in ARMS[1:]:
  s=summary[arm];checks[arm]={'direction_noninferior':s['direction']['accuracy']>=base['direction']['accuracy']-1e-10,'balanced_size_noninferior':s['materiality']['balanced_accuracy']>=base['materiality']['balanced_accuracy']-1e-10,'false_premiums_noninferior':s['materiality']['false_meaningful']<=base['materiality']['false_meaningful']+1e-10,'missed_meaningful_noninferior':s['materiality']['missed_meaningful']<=base['materiality']['missed_meaningful']+1e-10,'direct_size_noninferior':s['directly_supported_materiality']['accuracy']>=base['directly_supported_materiality']['accuracy']-1e-10}
 eligible=[a for a in ARMS[1:] if all(checks[a].values())];winner=max(eligible,key=lambda a:(summary[a]['direction']['accuracy']+summary[a]['materiality']['balanced_accuracy'],-(a=='combined'))) if eligible else 'v18'
 cfg=json.loads((R/'contextual-boundary-fit-delivery-v18.json').read_text())['model'];full={}
 for arm in ARMS:
  choice={'shade_fraction':0.,'boundary_increment':0.} if arm=='v18' else model.fit(t,e,cfg['underlying_coefficients'],cfg['base_radius'],cfg['context_kind'],cfg['context_coefficient'],arm)
  full[arm]={**cfg,**choice,'calibration_evidence':'evidence-v19.json'}
 result={'source_hashes':hashes,'protocol':'Two prespecified bounded residual coefficients.21-point grid per coefficient; equally weighted training direction accuracy and balanced materiality, then direct-size accuracy, fewer false positives and minimum correction. Same family splits; cached v18 base fits exclude validation families. Residual fitting train-only. Models differ in data access: frozen v18 uses old evidence; corrections learn v19 training rows. Exploratory, not new prospective accuracy. No parameter selection on outer test labels. Delivery gates applied to outer metrics; repeated reuse limits independence.','row_ids':[q['id'] for q in t],'nested_cv':{'runs':runs,'summary':summary,'fold_audits':audits},'full_models':full,'delivery':{'selected':winner,'checks':checks},'recent_full_predictions':{arm:{q['id']:model.predict(q['a'],q['b'],fc) for q in t if q['id'].startswith(('round36-','round37-','round38-'))} for arm,fc in full.items()}}
 write_versioned(R/'contextual-fixes-validation-v19.json',result)
 write_versioned(R/'contextual-fixes-delivery-v19.json',{'selected_model':winner,'model':full[winner],'evidence':'evidence-v19.json','validation':summary[winner],'validation_file':'contextual-fixes-validation-v19.json','baselines_unchanged':True})
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 print(json.dumps({'summary':summary,'winner':winner,'checks':checks,'full_choices':{a:{k:v[k] for k in ['shade_fraction','boundary_increment']} for a,v in full.items()}},indent=2))
if __name__=='__main__':main()
