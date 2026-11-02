from pathlib import Path
import json,hashlib
import numpy as np
import residual_fixes_v22 as model
import refit_simple_benchmark_v16 as metrics
from validate_contextual_meaningfulness_v18 import extend_folds
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
ARMS=('v21','vintage','shade','combined')
SOURCES=['evidence-v21.json','evidence-v22.json','benchmark-targets-v22.json','round41-fixed.json','revision-13-correction.json','shade-vintage-shared-delivery-v21.json','shade-vintage-shared-validation-v21.json','residual_fixes_v22.py','validate_residual_fixes_v22.py','shade_vintage_shared_v21.py']
def main():
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in SOURCES};old=json.loads((R/'shade-vintage-shared-validation-v21.json').read_text());t=json.loads((R/'benchmark-targets-v22.json').read_text())['rows'];e=json.loads((R/'evidence-v22.json').read_text())['rows'];idx={q['id']:i for i,q in enumerate(t)};groups=model.previous.utility.arrays(t)[3];direct=metrics.verified_materiality(e);runs={a:[] for a in ARMS};audits=[]
 for seed in metrics.SEEDS:
  fs=sorted([a for a in old['nested_cv']['fold_audits'] if a['seed']==seed],key=lambda q:q['fold']);oldsplit=[(np.array([idx[i] for i in f['training_ids']]),np.array([idx[i] for i in f['validation_ids']])) for f in fs];mm={a:np.zeros(len(t)) for a in ARMS};rr=np.zeros(len(t))
  for fold,(tr,te) in enumerate(extend_folds(groups,groups[:467],oldsplit,5,seed)):
   f=fs[fold];cfg={**f['base_config'],**f['choices']['pooled'],'selected_arm':'pooled'};assert [t[i]['id'] for i in tr if i<467]==f['training_ids'];assert not set(groups[tr])&set(groups[te]);train=[t[i] for i in tr];test=[t[i] for i in te];g,r,h=model.components(test,cfg);rr[te]=r;choices={}
   for arm in ARMS:
    c={'residual_parameters':[0.,0.]} if arm=='v21' else model.fit(train,[e[i] for i in tr],cfg,arm);choices[arm]=c;mm[arm][te]=g+h@c['residual_parameters']
   audits.append({'seed':seed,'fold':fold,'training_ids':[t[i]['id'] for i in tr],'validation_ids':[t[i]['id'] for i in te],'base_config':cfg,'choices':choices})
  baseline=next(q for q in old['nested_cv']['runs']['pooled'] if q['seed']==seed);np.testing.assert_allclose(mm['v21'][:467],baseline['margins'],atol=1e-12);np.testing.assert_allclose(rr[:467],baseline['radii'],atol=1e-12)
  for arm in ARMS:runs[arm].append({'seed':seed,'margins':mm[arm].tolist(),'radii':rr.tolist(),'score':metrics.score(t,mm[arm],rr,direct)})
 summary=metrics.summarize(runs);base=summary['v21'];checks={}
 for arm in ARMS[1:]:
  s=summary[arm];checks[arm]={'direction_noninferior':s['direction']['accuracy']>=base['direction']['accuracy']-1e-10,'balanced_size_noninferior':s['materiality']['balanced_accuracy']>=base['materiality']['balanced_accuracy']-1e-10,'false_premiums_noninferior':s['materiality']['false_meaningful']<=base['materiality']['false_meaningful']+1e-10,'missed_meaningful_noninferior':s['materiality']['missed_meaningful']<=base['materiality']['missed_meaningful']+1e-10,'direct_size_noninferior':s['directly_supported_materiality']['accuracy']>=base['directly_supported_materiality']['accuracy']-1e-10,'strict_improvement':s['direction']['accuracy']>base['direction']['accuracy']+1e-10 or s['materiality']['balanced_accuracy']>base['materiality']['balanced_accuracy']+1e-10}
 eligible=[a for a in ARMS[1:] if all(checks[a].values())];winner=max(eligible,key=lambda a:(summary[a]['direction']['accuracy']+summary[a]['materiality']['balanced_accuracy'],a!='combined')) if eligible else 'v21'
 cfg=json.loads((R/'shade-vintage-shared-delivery-v21.json').read_text())['model'];full={a:{**cfg,**({'residual_parameters':[0.,0.]} if a=='v21' else model.fit(t,e,cfg,a)),'calibration_evidence':'evidence-v22.json'} for a in ARMS}
 result={'source_hashes':hashes,'protocol':'Prespecified residual1 boosts existing20-year offering advantage by bounded fraction0..1 of frozen20vs25 step, all contexts. Residual2 reduces foreign golden/pale premium at shared minimum tare<=115 and younger vintage>=30, preserving earlier WE25vs30/115. One-coefficient ablations and two-coefficient combination;21-point grid, training objective same as v21. Frozen baseline weights/parameters/cached training fits; original family splits extended label-free. New correction label used in training only for candidates; frozen baseline rescored on corrected targets. Parent prediction margins reproduced. No row lookup/override. Structural zero130 and pure5lb effects unchanged. Exploratory reuse, not prospective accuracy.','row_ids':[q['id'] for q in t],'nested_cv':{'runs':runs,'summary':summary,'fold_audits':audits},'full_models':full,'recent_predictions':{a:{q['id']:model.predict(q['a'],q['b'],c) for q in t if q['id'].startswith(('round36-','round39-','round40-','round41-')) or q['id'] in ('revision-13','revision-14','round21-15')} for a,c in full.items()},'delivery':{'selected':winner,'checks':checks}}
 write_versioned(R/'residual-fixes-validation-v22.json',result);write_versioned(R/'residual-fixes-delivery-v22.json',{'selected_model':winner,'model':full[winner],'validation':summary[winner],'validation_file':'residual-fixes-validation-v22.json','evidence':'evidence-v22.json','baselines_unchanged':True})
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 print(json.dumps({'summary':summary,'delivery':result['delivery'],'parameters':{a:c['residual_parameters'] for a,c in full.items()}},indent=2))
if __name__=='__main__':main()
