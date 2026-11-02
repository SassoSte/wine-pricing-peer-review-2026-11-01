from pathlib import Path
import json,hashlib
import numpy as np
import intrinsic_regional_v30 as model
import intrinsic_v29 as original
import tare_compensation_v27 as baseline
import joint_objective_v22 as joint
import refit_simple_benchmark_v16 as metrics
from validate_contextual_meaningfulness_v18 import extend_folds
R=Path(__file__).resolve().parent
def main():
 prior=json.loads((R/'intrinsic-long-validation-v29.json').read_text());v28=json.loads((R/'tare-refit-validation-v28.json').read_text());t=json.loads((R/'benchmark-targets-v30.json').read_text())['rows'];e=json.loads((R/'evidence-v30.json').read_text())['rows'];ix={q['id']:i for i,q in enumerate(t)};groups=baseline.parent.parent.additive.features.arrays(t)[3];direct=metrics.verified_materiality(e)
 sources=['evidence-v29.json','evidence-v30.json','benchmark-targets-v30.json','round56-fixed.json','model-config-v28.json','predictor_v28.py','predictor_v27.py','intrinsic-long-validation-v29.json','intrinsic_regional_v30.py','validate_intrinsic_regional_v30.py']
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources};runs={k:[] for k in ('v28','intrinsic23',*model.REFINEMENTS)};audits=[];cache=R/'regional-interaction-cache-v30';cache.mkdir(exist_ok=True)
 for seed in metrics.SEEDS:
  fs=sorted([f for f in prior['fold_audits'] if f['seed']==seed],key=lambda f:f['fold']);bs=sorted([f for f in v28['nested_cv']['fold_audits'] if f['seed']==seed],key=lambda f:f['fold']);splits=[(np.array([ix[i] for i in f['training_ids']]),np.array([ix[i] for i in f['validation_ids']])) for f in fs];g={k:np.zeros(len(t)) for k in runs}
  for fold,(tr,te) in enumerate(extend_folds(groups,groups[:628],splits,5,seed)):
   assert not set(groups[tr])&set(groups[te]);train=[t[i] for i in tr];test=[t[i] for i in te];g['v28'][te]=baseline.design(test)@bs[fold]['fit']['coefficients'];g['intrinsic23'][te]=original.design(test)@fs[fold]['fit']['coefficients']
   for kind in model.REFINEMENTS:
    p=cache/f'{kind}-{seed}-{fold}.json'
    if p.exists():
     f=json.loads(p.read_text());assert f['source_hashes']==hashes
    else:
     c=model.fit(train,kind,12.);f={'source_hashes':hashes,'kind':kind,'seed':seed,'fold':fold,'training_ids':[t[i]['id'] for i in tr],'validation_ids':[t[i]['id'] for i in te],'fit':c};p.write_text(json.dumps(f,indent=2)+'\n')
    g[kind][te]=model.design(test,kind)@f['fit']['coefficients'];audits.append(f)
  for kind in runs:runs[kind].append({'seed':seed,'margins':g[kind].tolist(),'score':metrics.score(t,g[kind],1.,direct),'joint_score':joint.score(t,g[kind],1.)})
  print('Completed seed',seed,[(k,runs[k][-1]['joint_score']['both_axes_correct']) for k in runs],flush=True)
 full={}
 for kind in model.REFINEMENTS:
  full[kind]=model.fit(t,kind,45.);(R/f'interaction-config-{kind}-v30.json').write_text(json.dumps(full[kind],indent=2)+'\n');print('Full fit',kind,full[kind]['mip_gap'],flush=True)
 js={k:{n:float(np.mean([q['joint_score'][n] for q in rs])) for n in ('correct','accuracy','both_axes_n','both_axes_correct','both_axes_accuracy','balanced_accuracy')} for k,rs in runs.items()}
 result={'protocol':'Evidencev30, same25 repeated family folds extended label-free. Frozen v28 and intrinsic23 fold models rescored on current labels. One24-coefficient regional-vintage alternative motivated by verified4-label representation conflict: adds signedSEA20-year offering interaction. Adaptive exploratory architecture check,not confirmatory test. Shared intrinsic offering utility, no pair-specific premium or reduced threshold. Joint objective; required old judgments protected only when in training. Ordinary5lb cap and130lb golden/pale equality.12sec/fold,45sec/full. Reused exploratory validation, not prospective. Round56 full-fit checks are in-sample and not a fresh retest.','source_hashes':hashes,'row_ids':[q['id'] for q in t],'runs':runs,'summary':metrics.summarize(runs),'joint_summary':js,'fold_audits':audits,'full_models':full}
 (R/'regional-interaction-validation-v30.json').write_text(json.dumps(result,indent=2)+'\n')
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 print(json.dumps(js,indent=2))
if __name__=='__main__':main()
