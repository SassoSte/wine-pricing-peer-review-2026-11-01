from pathlib import Path
import json,hashlib
import numpy as np
import direct_joint_weights_v22 as model
import joint_weight_refit_v22 as qp
import joint_objective_v22 as joint
import refit_simple_benchmark_v16 as metrics
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
def main():
 source=['evidence-v22.json','benchmark-targets-v22.json','joint-weight-refit-validation-v22.json','joint-weight-ridge-check-v22.json','direct_joint_weights_v22.py','validate_direct_joint_weights_v22.py'];hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in source};old=json.loads((R/'joint-weight-refit-validation-v22.json').read_text());weak=json.loads((R/'joint-weight-ridge-check-v22.json').read_text());t=json.loads((R/'benchmark-targets-v22.json').read_text())['rows'];e=json.loads((R/'evidence-v22.json').read_text())['rows'];ix={q['id']:i for i,q in enumerate(t)};direct=metrics.verified_materiality(e);runs={'v21':old['nested_cv']['runs']['v21'],'direct_joint_refit':[]};audits=[]
 for seed in metrics.SEEDS:
  g=np.zeros(len(t));r=np.zeros(len(t))
  for f in [q for q in old['nested_cv']['fold_audits'] if q['seed']==seed]:
   tr=[ix[i] for i in f['training_ids']];te=[ix[i] for i in f['validation_ids']];reference=f['reference_context'];warm=next(q['fit']['coefficients'] for q in weak['nested_cv']['fold_audits'] if q['alpha']==1e-5 and q['seed']==seed and q['fold']==f['fold']);fit=model.fit([t[i] for i in tr],reference,[reference['underlying_coefficients'],warm]);x,cut=qp.design([t[i] for i in te],reference);g[te]=x@fit['coefficients'];r[te]=cut;audits.append({'seed':seed,'fold':f['fold'],'training_ids':f['training_ids'],'validation_ids':f['validation_ids'],'reference_context':reference,'fit':fit})
  runs['direct_joint_refit'].append({'seed':seed,'margins':g.tolist(),'radii':r.tolist(),'score':metrics.score(t,g,r,direct),'joint_score':joint.score(t,g,r)})
 for run in runs['v21']:run['joint_score']=joint.score(t,np.array(run['margins']),np.array(run['radii']))
 summary=metrics.summarize(runs);js={a:{k:float(np.mean([q['joint_score'][k] for q in series])) for k in ('both_axes_correct','both_axes_accuracy','balanced_accuracy','signed_joint_loss')} for a,series in runs.items()};a='direct_joint_refit';s=summary[a];base=summary['v21'];checks={'joint_improves':js[a]['balanced_accuracy']>js['v21']['balanced_accuracy'],'both_axes_noninferior':js[a]['both_axes_accuracy']>=js['v21']['both_axes_accuracy'],'direction_noninferior':s['direction']['accuracy']>=base['direction']['accuracy'],'false_premiums_noninferior':s['materiality']['false_meaningful']<=base['materiality']['false_meaningful'],'correct_meaningful_noninferior':s['materiality']['correct_meaningful_direction']>=base['materiality']['correct_meaningful_direction']}
 reference=weak['full_models']['1e-05']['reference_context'];full={**model.fit(t,reference,[reference['underlying_coefficients'],weak['full_models']['1e-05']['coefficients']]),'reference_context':reference};result={'source_hashes':hashes,'protocol':'Explicit follow-up to preserved joint hinge/ridge experiments. Same19 weights/contexts/thresholds/folds; train-only two starts: frozen reference and weak-ridge fit. Deterministic constrained coordinate search maximizes joint four-group correctness, then both-axis accuracy, then signed loss. All19 weights allowed to change, no global-optimality claim. Pure5lb and domestic adjacent shade caps remain; zero130 structural. No selection from held-out labels. Repeated/adaptive experiment exploratory.','nested_cv':{'runs':runs,'summary':summary,'joint_summary':js,'fold_audits':audits},'full_model':full,'delivery':{'selected':a if all(checks.values()) else 'retain_existing','checks':checks}}
 write_versioned(R/'direct-joint-weights-validation-v22.json',result);write_versioned(R/'direct-joint-weights-candidate-v22.json',{'model':full,'promoted':all(checks.values()),'validation_file':'direct-joint-weights-validation-v22.json'});print(json.dumps({'summary':summary,'joint':js,'delivery':result['delivery']},indent=2))
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
if __name__=='__main__':main()
