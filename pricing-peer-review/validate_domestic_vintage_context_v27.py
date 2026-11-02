from pathlib import Path
import json,hashlib
import numpy as np
import domestic_vintage_context_v27 as model
import joint_objective_v22 as joint
import refit_simple_benchmark_v16 as metrics
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
FILES=['evidence-v27.json','benchmark-targets-v27.json','joint-models-validation-v27.json','additive-milp-validation-v27.json','domestic-vintage-context-protocol-v27.json','domestic_vintage_context_v27.py','validate_domestic_vintage_context_v27.py']
def main():
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in FILES};old=json.loads((R/'joint-models-validation-v27.json').read_text());add=json.loads((R/'additive-milp-validation-v27.json').read_text());t=json.loads((R/'benchmark-targets-v27.json').read_text())['rows'];e=json.loads((R/'evidence-v27.json').read_text())['rows'];ix={q['id']:i for i,q in enumerate(t)};direct=metrics.verified_materiality(e);anchors=[t[ix[id]] for id in model.ANCHORS];feasibility={'additive18':model.feasibility(anchors,False),'domestic20_19':model.feasibility(anchors,True)};assert not feasibility['additive18']['feasible'] and feasibility['domestic20_19']['feasible']
 runs={'v26':old['nested_cv']['runs']['v26'],'additive18':add['nested_cv']['runs']['additive_milp'],'domestic20':[],'domestic20_anchored':[]};audits=[]
 for seed in metrics.SEEDS:
  mm={a:np.zeros(len(t)) for a in ('domestic20','domestic20_anchored')};r=np.ones(len(t))
  for f in [q for q in old['nested_cv']['fold_audits'] if q['seed']==seed]:
   tr=[ix[i] for i in f['training_ids']];te=[ix[i] for i in f['validation_ids']];train=[t[i] for i in tr];test=[t[i] for i in te];x=model.design(test);fits={}
   for arm in mm:
    cfg=model.fit(train,protect_anchors=arm=='domestic20_anchored');fits[arm]=cfg;mm[arm][te]=x@cfg['coefficients']
   audits.append({'seed':seed,'fold':f['fold'],'training_ids':f['training_ids'],'validation_ids':f['validation_ids'],'fits':fits})
  for arm in mm:runs[arm].append({'seed':seed,'margins':mm[arm].tolist(),'radii':r.tolist(),'score':metrics.score(t,mm[arm],r,direct),'joint_score':joint.score(t,mm[arm],r)})
  print('Completed domestic20 seed',seed,flush=True)
 summary=metrics.summarize(runs);js={a:{k:float(np.mean([q['joint_score'][k] for q in series])) for k in ('both_axes_correct','both_axes_accuracy','balanced_accuracy','signed_joint_loss')} for a,series in runs.items()};full={a:model.fit(t,protect_anchors=a=='domestic20_anchored',time_limit=12.) for a in ('domestic20','domestic20_anchored')};anchor_predictions={a:{q['id']:model.predict(q['a'],q['b'],cfg) for q in anchors} for a,cfg in full.items()};checks={}
 for a in full:
  s=summary[a];base=summary['v26'];reconciles=all(p['predicted_direction']==('A' if t[ix[id]]['known_direction']==1 else 'B') and p['predicted_meaningfulness']==('meaningful_difference' if t[ix[id]]['materiality_target'] else 'no_meaningful_difference') for id,p in anchor_predictions[a].items());checks[a]={'reconciles_three':reconciles,'joint_improves':js[a]['balanced_accuracy']>js['v26']['balanced_accuracy']+1e-10,'both_axes_noninferior':js[a]['both_axes_accuracy']>=js['v26']['both_axes_accuracy']-1e-10,'direction_noninferior':s['direction']['accuracy']>=base['direction']['accuracy']-1e-10,'false_premiums_noninferior':s['materiality']['false_meaningful']<=base['materiality']['false_meaningful']+1e-10}
 eligible=[a for a,c in checks.items() if all(c.values())];winner=max(eligible,key=lambda a:js[a]['balanced_accuracy']) if eligible else 'v26'
 result={'source_hashes':hashes,'protocol':json.loads((R/'domestic-vintage-context-protocol-v27.json').read_text()),'feasibility':feasibility,'nested_cv':{'runs':runs,'summary':summary,'joint_summary':js,'fold_audits':audits},'full_models':full,'anchor_predictions':anchor_predictions,'delivery':{'selected':winner,'checks':checks},'qualification':'18->19 feature feasibility demonstrated. Anchor constraints only when train-present; full reconciliation is a requirement, not evidence of generalization. Tolerance-limited MILP, gaps reported. No new evidence labels.'}
 write_versioned(R/'domestic-vintage-context-validation-v27.json',result)
 for a,cfg in full.items():write_versioned(R/(a.replace('_','-')+'-candidate-v27.json'),{'model':cfg,'promoted':winner==a,'validation_file':'domestic-vintage-context-validation-v27.json'})
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 print(json.dumps({'summary':summary,'joint':js,'delivery':result['delivery'],'coefficients':{a:c['coefficients'][-1] for a,c in full.items()},'anchors':anchor_predictions},indent=2))
if __name__=='__main__':main()
