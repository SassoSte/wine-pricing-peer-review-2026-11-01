from pathlib import Path
import json,hashlib
import numpy as np
import regional_mature_shade_v30 as model
from regional_minimum_norm_v30 import polish
import joint_objective_v22 as joint
import refit_simple_benchmark_v16 as metrics
R=Path(__file__).resolve().parent

def main():
 prior=json.loads((R/'regional-interaction-validation-v30.json').read_text());t=json.loads((R/'benchmark-targets-v30.json').read_text())['rows'];e=json.loads((R/'evidence-v30.json').read_text())['rows'];by={q['id']:q for q in t};ix={q['id']:i for i,q in enumerate(t)};direct=metrics.verified_materiality(e);audits=[];runs={'one_feature':[],'one_feature_minimum_norm':[]};cache=R/'regional-mature-shade-cache-v30';cache.mkdir(exist_ok=True)
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ('evidence-v30.json','benchmark-targets-v30.json','regional-interaction-validation-v30.json','regional_mature_shade_v30.py','regional_minimum_norm_v30.py','validate_regional_mature_shade_v30.py','model-config-v28.json','predictor_v28.py','predictor_v27.py')}
 for seed in metrics.SEEDS:
  gg={k:np.zeros(len(t)) for k in runs}
  for f in (f for f in prior['fold_audits'] if f['seed']==seed):
   p=cache/f"{seed}-{f['fold']}.json";train=[by[i] for i in f['training_ids']];test=[by[i] for i in f['validation_ids']];te=[ix[i] for i in f['validation_ids']]
   if p.exists():item=json.loads(p.read_text());assert item['source_hashes']==hashes
   else:
    c=model.fit(train,'regional_mature_shade',30.);pol=polish(train,c,lambda rows:model.design(rows,'regional_mature_shade'),lambda:model.structural('regional_mature_shade'));item={'source_hashes':hashes,'seed':seed,'fold':f['fold'],'training_ids':f['training_ids'],'validation_ids':f['validation_ids'],'fit':c,'polished_fit':pol};p.write_text(json.dumps(item,indent=2)+'\n')
   x=model.design(test,'regional_mature_shade');gg['one_feature'][te]=x@item['fit']['coefficients'];gg['one_feature_minimum_norm'][te]=x@item['polished_fit']['coefficients'];audits.append(item)
  for k in runs:runs[k].append({'seed':seed,'margins':gg[k].tolist(),'score':metrics.score(t,gg[k],1.,direct),'joint_score':joint.score(t,gg[k],1.)})
  print('Completed feature seed',seed,[(k,runs[k][-1]['joint_score']['both_axes_correct']) for k in runs],flush=True)
 full=model.fit(t,'regional_mature_shade',90.);pol=polish(t,full,lambda rows:model.design(rows,'regional_mature_shade'),lambda:model.structural('regional_mature_shade'));(R/'regional-mature-shade-config-v30.json').write_text(json.dumps(full,indent=2)+'\n');(R/'regional-mature-shade-minnorm-config-v30.json').write_text(json.dumps(pol,indent=2)+'\n')
 out={'protocol':'One additional intrinsic offering coefficient: golden/pale offerings35years or younger. Separates verified older light-shade vintage conflict while all same-profile5lb steps and golden/pale130 equality are unchanged by new term. Same25 family partitions, training-only anchors and objective.30sec/fold,90sec/full. Also minimum-L2 correct-training-set polish, no additional features. Adaptive exploratory test on v30, not fresh validation.','source_hashes':hashes,'runs':runs,'summary':metrics.summarize(runs),'fold_audits':audits,'full_model':full,'polished_full_model':pol}
 (R/'regional-mature-shade-validation-v30.json').write_text(json.dumps(out,indent=2)+'\n')
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 print('Finished feature validation',flush=True)
if __name__=='__main__':main()
