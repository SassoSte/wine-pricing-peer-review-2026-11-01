from pathlib import Path
import json,hashlib
import numpy as np
import shade_vintage_shared_v21 as model
import refit_simple_benchmark_v16 as metrics
from validate_contextual_meaningfulness_v18 import extend_folds
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
ARMS=('v20','zero_only','pooled','bands')
SOURCES=['evidence-v20.json','evidence-v21.json','benchmark-targets-v21.json','round40-fixed.json','contextual-shade-delivery-v20.json','contextual-shade-validation-v20.json','contextual_shade_v20.py','shade_vintage_shared_v21.py','validate_shade_vintage_shared_v21.py','contextual_fixes_v19.py']
def main():
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in SOURCES};old=json.loads((R/'contextual-shade-validation-v20.json').read_text());t=json.loads((R/'benchmark-targets-v21.json').read_text())['rows'];e=json.loads((R/'evidence-v21.json').read_text())['rows'];idx={q['id']:i for i,q in enumerate(t)};direct=metrics.verified_materiality(e);groups=model.utility.arrays(t)[3];runs={a:[] for a in ARMS};audits=[]
 for seed in metrics.SEEDS:
  fs=sorted([a for a in old['nested_cv']['fold_audits'] if a['seed']==seed],key=lambda q:q['fold']);oldsplit=[(np.array([idx[i] for i in f['training_ids']]),np.array([idx[i] for i in f['validation_ids']])) for f in fs];splits=extend_folds(groups,groups[:455],oldsplit,5,seed);mm={a:np.zeros(len(t)) for a in ARMS};rr=np.zeros(len(t))
  for fold,(tr,te) in enumerate(splits):
   f=fs[fold];cfg={**f['base_config'],**f['choices']['heavy_only']};assert [t[i]['id'] for i in tr if i<455]==f['training_ids'];assert not set(groups[tr])&set(groups[te]);train=[t[i] for i in tr];test=[t[i] for i in te];parts=model.components(test,cfg);rr[te]=parts[1];g,r,h=model.v20.arrays(test,cfg);mm['v20'][te]=g+h@cfg['shade_coefficients'];choices={}
   for arm in ARMS[1:]:
    c=model.fit(train,[e[i] for i in tr],cfg,arm);choices[arm]=c;mm[arm][te]=model.gaps(parts,c['shade_parameters'])[0]
   audits.append({'seed':seed,'fold':fold,'training_ids':[t[i]['id'] for i in tr],'validation_ids':[t[i]['id'] for i in te],'base_config':cfg,'choices':choices})
  baseline=next(q for q in old['nested_cv']['runs']['heavy_only'] if q['seed']==seed);np.testing.assert_allclose(mm['v20'][:455],baseline['margins'],atol=1e-12);np.testing.assert_allclose(rr[:455],baseline['radii'],atol=1e-12)
  for arm in ARMS:runs[arm].append({'seed':seed,'margins':mm[arm].tolist(),'radii':rr.tolist(),'score':metrics.score(t,mm[arm],rr,direct)})
 summary=metrics.summarize(runs);base=summary['v20'];checks={}
 for arm in ARMS[1:]:
  s=summary[arm];checks[arm]={'direction_noninferior':s['direction']['accuracy']>=base['direction']['accuracy']-1e-10,'balanced_size_noninferior':s['materiality']['balanced_accuracy']>=base['materiality']['balanced_accuracy']-1e-10,'false_premiums_noninferior':s['materiality']['false_meaningful']<=base['materiality']['false_meaningful']+1e-10,'missed_meaningful_noninferior':s['materiality']['missed_meaningful']<=base['materiality']['missed_meaningful']+1e-10,'direct_size_noninferior':s['directly_supported_materiality']['accuracy']>=base['directly_supported_materiality']['accuracy']-1e-10}
 eligible=[a for a in ARMS[1:] if all(checks[a].values())];winner=max(eligible,key=lambda a:(summary[a]['direction']['accuracy']+summary[a]['materiality']['balanced_accuracy'],-ARMS.index(a))) if eligible else 'v20'
 cfg=json.loads((R/'contextual-shade-delivery-v20.json').read_text())['model'];full={a:{**cfg,**({'shade_parameters':[0.,0.,0.]} if a=='v20' else model.fit(t,e,cfg,a)),'selected_arm':a,'calibration_evidence':'evidence-v21.json'} for a in ARMS}
 result={'source_hashes':hashes,'protocol':'Follow-up to preserved max-tare experiment: use MINIMUM tare as shared context, so both vessels must reach a threshold; avoid extrapolating the heavier vessel context to lighter vessel. Replace v20 exact-match gate with shared comparison-context golden/pale premium. Applies to mixed tare/provenance; shade increment uses pale provenance. Negligible pure5lb effects unchanged algebraically. Zero premium when BOTH tares130 is a mandated structural prior from current user instruction, not independently learned/validated discovery. At lower tare, foreign shrinkage at120/125 plus age20 modifier fitted; domestic otherwise unchanged. Pooled2 coefficients vs bands3, and zero-only control. Frozen baseline coefficients and boundary. Grid fitting training families only, original folds extended label-free. Selection objective same as v20, outer gates choose delivery. Hypothesis informed by prior evidence; repeated-family results exploratory. Pair context is not a transitive offering price function.','row_ids':[q['id'] for q in t],'nested_cv':{'runs':runs,'summary':summary,'fold_audits':audits},'full_models':full,'recent_predictions':{a:{q['id']:model.predict(q['a'],q['b'],c) for q in t if q['id'].startswith(('round36-','round39-','round40-')) or q['id'] in ('revision-13','revision-14','round21-15')} for a,c in full.items()},'delivery':{'selected':winner,'checks':checks}}
 write_versioned(R/'shade-vintage-shared-validation-v21.json',result);write_versioned(R/'shade-vintage-shared-delivery-v21.json',{'selected_model':winner,'model':full[winner],'validation':summary[winner],'validation_file':'shade-vintage-shared-validation-v21.json','evidence':'evidence-v21.json','baselines_unchanged':True})
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 print(json.dumps({'summary':summary,'delivery':result['delivery'],'parameters':{a:c['shade_parameters'] for a,c in full.items()}},indent=2))
if __name__=='__main__':main()
