from pathlib import Path
import json,hashlib
import numpy as np
import tare_compensation_v27 as model
import joint_objective_v22 as joint
import refit_simple_benchmark_v16 as metrics
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
FILES=['evidence-v27.json','benchmark-targets-v27.json','matched-vintage-context-validation-v27.json','tare-compensation-protocol-v27.json','tare_compensation_v27.py','validate_tare_compensation_v27.py']
def main():
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in FILES};old=json.loads((R/'matched-vintage-context-validation-v27.json').read_text());t=json.loads((R/'benchmark-targets-v27.json').read_text())['rows'];e=json.loads((R/'evidence-v27.json').read_text())['rows'];ix={q['id']:i for i,q in enumerate(t)};direct=metrics.verified_materiality(e);runs={'v26':old['nested_cv']['runs']['v26'],'matched_vintage':old['nested_cv']['runs']['matched_vintage'],'tare_compensation':[]};audits=[]
 for seed in metrics.SEEDS:
  g=np.zeros(len(t));r=np.ones(len(t))
  for f in [q for q in old['nested_cv']['fold_audits'] if q['seed']==seed]:
   tr=[ix[i] for i in f['training_ids']];te=[ix[i] for i in f['validation_ids']];cfg=model.fit([t[i] for i in tr]);g[te]=model.design([t[i] for i in te])@cfg['coefficients'];audits.append({'seed':seed,'fold':f['fold'],'training_ids':f['training_ids'],'validation_ids':f['validation_ids'],'fit':cfg})
  runs['tare_compensation'].append({'seed':seed,'margins':g.tolist(),'radii':r.tolist(),'score':metrics.score(t,g,r,direct),'joint_score':joint.score(t,g,r)});print('Completed tare compensation seed',seed,flush=True)
 summary=metrics.summarize(runs);js={a:{k:float(np.mean([q['joint_score'][k] for q in series])) for k in ('both_axes_correct','both_axes_accuracy','balanced_accuracy','signed_joint_loss')} for a,series in runs.items()};full=model.fit(t,time_limit=12.);anchors=[t[ix[i]] for i in model.ANCHORS];ap={q['id']:model.predict(q['a'],q['b'],full) for q in anchors};s=summary['tare_compensation'];base=summary['v26'];checks={'reconciles_three':all(p['predicted_direction']=='A' and p['predicted_meaningfulness']==('meaningful_difference' if t[ix[id]]['materiality_target'] else 'no_meaningful_difference') for id,p in ap.items()),'joint_improves':js['tare_compensation']['balanced_accuracy']>js['v26']['balanced_accuracy']+1e-10,'both_axes_noninferior':js['tare_compensation']['both_axes_accuracy']>=js['v26']['both_axes_accuracy']-1e-10,'direction_noninferior':s['direction']['accuracy']>=base['direction']['accuracy']-1e-10,'false_premiums_noninferior':s['materiality']['false_meaningful']<=base['materiality']['false_meaningful']+1e-10}
 result={'source_hashes':hashes,'protocol':json.loads((R/'tare-compensation-protocol-v27.json').read_text()),'nested_cv':{'runs':runs,'summary':summary,'joint_summary':js,'fold_audits':audits},'full_model':full,'anchor_predictions':ap,'target_predictions':{id:model.predict(t[ix[id]]['a'],t[ix[id]]['b'],full) for id in ('round44-8','round44-9','round37-2')},'delivery':{'selected':'tare_compensation' if all(checks.values()) else 'v26','checks':checks}}
 write_versioned(R/'tare-compensation-validation-v27.json',result);write_versioned(R/'tare-compensation-candidate-v27.json',{'model':full,'promoted':all(checks.values()),'validation_file':'tare-compensation-validation-v27.json'})
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 print(json.dumps({'summary':summary,'joint':js,'delivery':result['delivery'],'extra_coefficient':full['coefficients'][-1],'tare_coefficient':full['coefficients'][17],'targets':result['target_predictions']},indent=2))
if __name__=='__main__':main()
