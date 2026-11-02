from pathlib import Path
import hashlib,json
import numpy as np
import joint_weight_refit_v22 as model
import joint_objective_v22 as joint
import refit_simple_benchmark_v16 as metrics
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
SOURCES=['evidence-v22.json','benchmark-targets-v22.json','residual-fixes-validation-v22.json','shade-vintage-shared-delivery-v21.json','joint_weight_refit_v22.py','validate_joint_weight_refit_v22.py','joint_objective_v22.py','domestic_shade_model.py','shade_vintage_shared_v21.py']
def main():
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in SOURCES};old=json.loads((R/'residual-fixes-validation-v22.json').read_text());t=json.loads((R/'benchmark-targets-v22.json').read_text())['rows'];e=json.loads((R/'evidence-v22.json').read_text())['rows'];ix={q['id']:i for i,q in enumerate(t)};direct=metrics.verified_materiality(e);runs={'v21':old['nested_cv']['runs']['v21'],'joint_refit':[],'ridge_sensitivity':[]};audits=[]
 for seed in metrics.SEEDS:
  mm={a:np.zeros(len(t)) for a in ('joint_refit','ridge_sensitivity')};rr=np.zeros(len(t))
  for f in [q for q in old['nested_cv']['fold_audits'] if q['seed']==seed]:
   tr=[ix[i] for i in f['training_ids']];te=[ix[i] for i in f['validation_ids']];train=[t[i] for i in tr];test=[t[i] for i in te];reference=f['base_config'];x,r=model.design(test,reference);rr[te]=r;fits={}
   for arm,alpha in [('joint_refit',model.PRIMARY_ALPHA),('ridge_sensitivity',model.SENSITIVITY_ALPHA)]:
    cfg=model.fit(train,reference,alpha);fits[arm]=cfg;mm[arm][te]=x@cfg['coefficients']
   audits.append({'seed':seed,'fold':f['fold'],'training_ids':f['training_ids'],'validation_ids':f['validation_ids'],'reference_context':reference,'fits':fits})
  for arm in mm:runs[arm].append({'seed':seed,'margins':mm[arm].tolist(),'radii':rr.tolist(),'score':metrics.score(t,mm[arm],rr,direct)})
 for series in runs.values():
  for run in series:run['joint_score']=joint.score(t,np.array(run['margins']),np.array(run['radii']))
 summary=metrics.summarize(runs);js={a:{k:(series[0]['joint_score'][k] if k.endswith('_n') else float(np.mean([q['joint_score'][k] for q in series]))) for k in ('supported_n','correct','accuracy','balanced_accuracy','both_axes_n','both_axes_correct','both_axes_accuracy','signed_joint_loss')} for a,series in runs.items()};checks={}
 for a in ('joint_refit','ridge_sensitivity'):
  checks[a]={'joint_balanced_improves':js[a]['balanced_accuracy']>js['v21']['balanced_accuracy']+1e-10,'fully_labeled_noninferior':js[a]['both_axes_accuracy']>=js['v21']['both_axes_accuracy']-1e-10,'direction_noninferior':summary[a]['direction']['accuracy']>=summary['v21']['direction']['accuracy']-1e-10,'false_premiums_noninferior':summary[a]['materiality']['false_meaningful']<=summary['v21']['materiality']['false_meaningful']+1e-10,'correct_meaningful_noninferior':summary[a]['materiality']['correct_meaningful_direction']>=summary['v21']['materiality']['correct_meaningful_direction']-1e-10}
 winner='joint_refit' if all(checks['joint_refit'].values()) else 'v21'
 reference=json.loads((R/'shade-vintage-shared-delivery-v21.json').read_text())['model'];full={a:{**model.fit(t,reference,alpha),'reference_context':reference,'evidence':'evidence-v22.json'} for a,alpha in [('joint_refit',model.PRIMARY_ALPHA),('ridge_sensitivity',model.SENSITIVITY_ALPHA)]}
 result={'source_hashes':hashes,'protocol':'Refit all19 underlying coefficients from scratch with convex four-group balanced signed joint hinge loss; direction+meaningfulness coupled, missing axes not inferred. V21 shade-context functions and attribute-dependent boundary/proximity map frozen per outer TRAINING reference model. Fixed primary ridge.001 and prespecified sensitivity.01, no post-hoc selecting sensitivity. No inner hyperparameter search. Same25 family partitions/labels as v22; new weights see only training rows. Monotone original increments, tare per5lb<=base radius, domestic adjacent shade<=base radius hard constraints. Pair transformation guarantees zero golden/pale effect at both130. Context remains pair-dependent, not standalone price. Primary delivery gates joint gain, directional and false-premium nonregression. Reused-family exploration, no prospective claim.','row_ids':old['row_ids'],'nested_cv':{'runs':runs,'summary':summary,'joint_summary':js,'fold_audits':audits},'full_models':full,'recent_full_predictions':{a:{q['id']:model.predict(q['a'],q['b'],c) for q in t if q['id'].startswith(('round39-','round40-','round41-')) or q['id']=='revision-13'} for a,c in full.items()},'delivery':{'selected':winner,'checks':checks}}
 write_versioned(R/'joint-weight-refit-validation-v22.json',result);write_versioned(R/'joint-weight-refit-delivery-v22.json',{'selected_model':winner,'model':full['joint_refit'] if winner=='joint_refit' else reference,'evidence':'evidence-v22.json','validation_file':'joint-weight-refit-validation-v22.json','joint_validation':js[winner],'validation':summary[winner],'baselines_unchanged':True})
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 print(json.dumps({'summary':summary,'joint':js,'delivery':result['delivery']},indent=2))
if __name__=='__main__':main()
