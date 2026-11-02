"""Train-only hard equality constraints versus soft equality using identical family folds."""
from pathlib import Path
import json,hashlib,itertools
import numpy as np
from scipy.optimize import linprog
import global_priority_v31 as soft
import global_positive_v33 as hard
from evaluate_voice_v32 import metrics
R=Path(__file__).resolve().parent
def main():
 rows=json.loads((R/'benchmark-targets-v33.json').read_text())['rows'];by={q['id']:q for q in rows};ix={q['id']:i for i,q in enumerate(rows)};prior=json.loads((R/'voice-validation-v32.json').read_text());models={'hard_refit':hard};runs={name:[] for name in models};audits=[]
 for seed in (11,29,47,71,103):
  gaps={name:np.zeros(len(rows)) for name in models}
  for f in [f for f in prior['fold_audits'] if f['seed']==seed]:
   train=[by[id] for id in f['training_ids']];test=[by[id] for id in f['validation_ids']];te=[ix[q['id']] for q in test]
   for name,module in models.items():
    cfg=module.select(train,seed*100+f['fold'],True);gaps[name][te]=module.design(test)@cfg['coefficients'];audits.append({'arm':name,'seed':seed,'fold':f['fold'],'training_ids':f['training_ids'],'validation_ids':f['validation_ids'],'fit':cfg})
    if name=='hard_refit':
     for q in train:
      if q.get('exact_price_equality') is True:assert abs(module.design([q])[0]@cfg['coefficients'])<1e-7
  for name,g in gaps.items():runs[name].append({'seed':seed,'margins':g.tolist(),'metrics':metrics(rows,g)})
  print(seed,{name:runs[name][-1]['metrics'] for name in models},flush=True)
 full={name:module.select(rows,33001,True) for name,module in models.items()};fullmetrics={name:metrics(rows,module.design(rows)@full[name]['coefficients']) for name,module in models.items()}
 # Independently check intrinsic utility monotonicity over all offerings for every hard fit.
 checks=0
 for cfg in [full['hard_refit']]+[f['fit'] for f in audits if f['arm']=='hard_refit']:
  w=np.array(cfg['coefficients'])
  for z,s,a,t in itertools.product(soft.D['provenances'],soft.D['shades'],soft.D['vintage_years'],soft.D['tare_lb']):
   base=hard.features([z,s,a,t])@w
   if a>20:assert hard.features([z,s,a-5,t])@w>=base-1e-6
   if t>110:assert hard.features([z,s,a,t-5])@w>=base-1e-6
   j=soft.D['shades'].index(s)
   if j<4:assert hard.features([z,soft.D['shades'][j+1],a,t])@w>=base-1e-6
   if s=='pale/straw' and t==130:assert abs(base-hard.features([z,'golden',a,t])@w)<1e-7
   checks+=1
 out={'protocol':'v33 single-feature positive margins constrained>=1e-4 using training judgments only; numerical sign floor, not meaningfulness radius or monetary amount. Same642pairs and25familyfolds. Soft global refit versus same21coefficient intrinsic model with train-only hard exact-equality constraints. Inner selection for hard arm scores strict direction plus exact relation. No pair lookups, no equality radius; exactties require absolute utility difference<=1e-7. Premium assessor unchanged. Reused validation exploratory.','runs':runs,'fold_audits':audits,'full_models':full,'full_fit_metrics':fullmetrics,'monotone_profile_checks':checks,'source_hashes':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['evidence-v33.json','benchmark-targets-v33.json','global_positive_v33.py','global_priority_v31.py','evaluate_positive_v33.py','model-config-v28.json']}}
 (R/'positive-validation-v33.json').write_text(json.dumps(out,indent=2)+'\n');print('FULL',fullmetrics,flush=True)
if __name__=='__main__':main()
