"""Preserved follow-up sensitivity: weaker penalties, no baseline mutation."""
import json,hashlib
from pathlib import Path
import numpy as np
import joint_weight_refit_v22 as model
import joint_objective_v22 as joint
import refit_simple_benchmark_v16 as metrics
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
def main():
 old=json.loads((R/'joint-weight-refit-validation-v22.json').read_text());t=json.loads((R/'benchmark-targets-v22.json').read_text())['rows'];e=json.loads((R/'evidence-v22.json').read_text())['rows'];ix={q['id']:i for i,q in enumerate(t)};direct=metrics.verified_materiality(e);runs={};audits=[]
 for alpha in (1e-5,1e-4):
  arm=str(alpha);runs[arm]=[]
  for seed in metrics.SEEDS:
   margins=np.zeros(len(t));radii=np.zeros(len(t))
   for f in [q for q in old['nested_cv']['fold_audits'] if q['seed']==seed]:
    tr=[ix[i] for i in f['training_ids']];te=[ix[i] for i in f['validation_ids']];reference=f['reference_context'];fit=model.fit([t[i] for i in tr],reference,alpha);x,r=model.design([t[i] for i in te],reference);margins[te]=x@fit['coefficients'];radii[te]=r;audits.append({'alpha':alpha,'seed':seed,'fold':f['fold'],'fit':fit})
   runs[arm].append({'seed':seed,'margins':margins.tolist(),'radii':radii.tolist(),'score':metrics.score(t,margins,radii,direct),'joint_score':joint.score(t,margins,radii)})
 summary=metrics.summarize(runs);js={a:{k:float(np.mean([q['joint_score'][k] for q in s])) for k in ('both_axes_correct','both_axes_accuracy','balanced_accuracy','signed_joint_loss')} for a,s in runs.items()};reference=json.loads((R/'shade-vintage-shared-delivery-v21.json').read_text())['model'];full={str(alpha):{**model.fit(t,reference,alpha),'reference_context':reference} for alpha in (1e-5,1e-4)}
 result={'source_hashes':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ('joint-weight-refit-validation-v22.json','joint_weight_refit_v22.py','joint_weight_ridge_check_v22.py','evidence-v22.json','benchmark-targets-v22.json')},'protocol':'Follow-up weaker-ridge sensitivity after primary showed compression; same data/folds/objective/context constraints. Exploratory extra comparisons; no post-hoc silent change to primary result. No evidence or baseline modifications.','nested_cv':{'runs':runs,'summary':summary,'joint_summary':js,'fold_audits':audits},'full_models':full}
 write_versioned(R/'joint-weight-ridge-check-v22.json',result);print(json.dumps({'summary':summary,'joint':js},indent=2))
if __name__=='__main__':main()
