from pathlib import Path
import json,hashlib
import numpy as np
import additive_milp_v27 as solver
import joint_models_v27 as models
import joint_objective_v22 as joint
import refit_simple_benchmark_v16 as metrics
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
def main():
 files=['joint-models-validation-v27.json','evidence-v27.json','benchmark-targets-v27.json','additive_milp_v27.py','validate_additive_milp_v27.py'];hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in files};old=json.loads((R/'joint-models-validation-v27.json').read_text());t=json.loads((R/'benchmark-targets-v27.json').read_text())['rows'];e=json.loads((R/'evidence-v27.json').read_text())['rows'];ix={q['id']:i for i,q in enumerate(t)};direct=metrics.verified_materiality(e);runs={'v26':old['nested_cv']['runs']['v26'],'additive_milp':[]};audits=[]
 for seed in metrics.SEEDS:
  g=np.zeros(len(t));r=np.ones(len(t))
  for f in [q for q in old['nested_cv']['fold_audits'] if q['seed']==seed]:
   tr=[ix[i] for i in f['training_ids']];te=[ix[i] for i in f['validation_ids']];fit=solver.fit([t[i] for i in tr]);gg,rr=models.margins([t[i] for i in te],fit);g[te]=gg;r[te]=rr;audits.append({'seed':seed,'fold':f['fold'],'training_ids':f['training_ids'],'validation_ids':f['validation_ids'],'fit':fit})
  runs['additive_milp'].append({'seed':seed,'margins':g.tolist(),'radii':r.tolist(),'score':metrics.score(t,g,r,direct),'joint_score':joint.score(t,g,r)});print('Completed MILP seed',seed,flush=True)
 summary=metrics.summarize(runs);js={a:{k:float(np.mean([q['joint_score'][k] for q in series])) for k in ('both_axes_correct','both_axes_accuracy','balanced_accuracy','signed_joint_loss')} for a,series in runs.items()};s=summary['additive_milp'];base=summary['v26'];checks={'joint_improves':js['additive_milp']['balanced_accuracy']>js['v26']['balanced_accuracy']+1e-10,'both_axes_noninferior':js['additive_milp']['both_axes_accuracy']>=js['v26']['both_axes_accuracy']-1e-10,'direction_noninferior':s['direction']['accuracy']>=base['direction']['accuracy']-1e-10,'false_premiums_noninferior':s['materiality']['false_meaningful']<=base['materiality']['false_meaningful']+1e-10};full=solver.fit(t,time_limit=12.)
 result={'source_hashes':hashes,'protocol':'Follow-up optimizer check on same18-parameter additive architecture, same labels/folds. Joint error binary shared across both supplied axes. Single-thread time-limited MILP3sec/fold,12sec full fit; gaps/status explicitly reported, no optimum claim unless solver proves it. Repeated exploratory validation, not independent confirmation.','nested_cv':{'runs':runs,'summary':summary,'joint_summary':js,'fold_audits':audits},'full_model':full,'delivery':{'selected':'additive_milp' if all(checks.values()) else 'v26','checks':checks}}
 write_versioned(R/'additive-milp-validation-v27.json',result);print(json.dumps({'summary':summary,'joint':js,'delivery':result['delivery'],'full_solver':{k:v for k,v in full.items() if k!='coefficients'}},indent=2))
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
if __name__=='__main__':main()
