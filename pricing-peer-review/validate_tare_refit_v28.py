"""Refit the existing20-coefficient tare model on reconciledv28 evidence."""
from pathlib import Path
import json,hashlib
import numpy as np
import tare_compensation_v27 as model
import joint_objective_v22 as joint
import refit_simple_benchmark_v16 as metrics
from validate_contextual_meaningfulness_v18 import extend_folds
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
FILES=['evidence-v27.json','evidence-v28.json','benchmark-targets-v28.json','round51-fixed.json','round52-clarifications.json','round53-isolation.json','round54-unresolved-isolation.json','tare-compensation-validation-v27.json','model-config-v27.json','tare_compensation_v27.py','validate_tare_refit_v28.py']
def main():
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in FILES};old=json.loads((R/'tare-compensation-validation-v27.json').read_text());t=json.loads((R/'benchmark-targets-v28.json').read_text())['rows'];e=json.loads((R/'evidence-v28.json').read_text())['rows'];ix={q['id']:i for i,q in enumerate(t)};groups=model.parent.parent.additive.features.arrays(t)[3];direct=metrics.verified_materiality(e);runs={'current_tare':[],'refit_v28':[]};audits=[]
 for seed in metrics.SEEDS:
  fs=sorted([q for q in old['nested_cv']['fold_audits'] if q['seed']==seed],key=lambda q:q['fold']);splits=[(np.array([ix[i] for i in f['training_ids']]),np.array([ix[i] for i in f['validation_ids']])) for f in fs];g={a:np.zeros(len(t)) for a in runs};r=np.ones(len(t))
  for fold,(tr,te) in enumerate(extend_folds(groups,groups[:587],splits,5,seed)):
   f=fs[fold];assert [t[i]['id'] for i in tr if i<587]==f['training_ids'];assert not set(groups[tr])&set(groups[te]);train=[t[i] for i in tr];test=[t[i] for i in te];cfg=model.fit(train);x=model.design(test);g['current_tare'][te]=x@f['fit']['coefficients'];g['refit_v28'][te]=x@cfg['coefficients'];audits.append({'seed':seed,'fold':fold,'training_ids':[t[i]['id'] for i in tr],'validation_ids':[t[i]['id'] for i in te],'fit':cfg})
  prior=next(q for q in old['nested_cv']['runs']['tare_compensation'] if q['seed']==seed);np.testing.assert_allclose(g['current_tare'][:587],prior['margins'],atol=1e-12)
  for arm in runs:runs[arm].append({'seed':seed,'margins':g[arm].tolist(),'radii':r.tolist(),'score':metrics.score(t,g[arm],r,direct),'joint_score':joint.score(t,g[arm],r)})
  print('Completed refit seed',seed,flush=True)
 summary=metrics.summarize(runs);js={a:{k:(series[0]['joint_score'][k] if k.endswith('_n') else float(np.mean([q['joint_score'][k] for q in series]))) for k in ('supported_n','correct','accuracy','both_axes_n','both_axes_correct','both_axes_accuracy','balanced_accuracy','signed_joint_loss')} for a,series in runs.items()};full=model.fit(t,time_limit=12.);anchor_predictions={id:model.predict(t[ix[id]]['a'],t[ix[id]]['b'],full) for id in model.ANCHORS}
 result={'source_hashes':hashes,'protocol':'Same20-coefficient model, joint objective, constraints,training-only anchor protection and single-thread MILP budgets3sec per fold/12sec full. Reconciledv28 labels; original25 family assignments extended label-free. Frozen current model coefficients reused for baseline and rescored on same current targets. New weights fit only training rows; unknown size remains missing, not inferred. No new features/thresholds. Inspect aggregate and per-repeat joint/direction/false-premium tradeoffs before selecting; no automatic promotion from one metric. Reused-family exploratory validation,not prospective.','row_ids':[q['id'] for q in t],'nested_cv':{'runs':runs,'summary':summary,'joint_summary':js,'fold_audits':audits},'full_model':full,'anchor_predictions':anchor_predictions,'selection_status':'pending_comparative_review'}
 write_versioned(R/'tare-refit-validation-v28.json',result);write_versioned(R/'tare-refit-candidate-v28.json',{'model':full,'validation_file':'tare-refit-validation-v28.json','evidence':'evidence-v28.json'})
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 print(json.dumps({'summary':summary,'joint':js,'anchors':anchor_predictions,'full_solver_gap':full['mip_gap']},indent=2))
if __name__=='__main__':main()
