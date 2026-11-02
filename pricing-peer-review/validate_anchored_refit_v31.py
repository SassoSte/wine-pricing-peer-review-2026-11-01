from pathlib import Path
from copy import deepcopy
import json,hashlib
import numpy as np
import refit_anchored_context_v31 as rank
from validate_refit_v31 import predict,relation_score
import refit_simple_benchmark_v16 as metrics
R=Path(__file__).resolve().parent

def main():
 current=json.loads((R/'v31-refit-validation.json').read_text());old=json.loads((R/'regional-rank-fix-validation-v30.json').read_text());t=json.loads((R/'benchmark-targets-v31.json').read_text())['rows'];e=json.loads((R/'evidence-v31.json').read_text())['rows'];by={q['id']:q for q in t};ix={q['id']:i for i,q in enumerate(t)};direct=np.array(metrics.verified_materiality(e));prior={(f['seed'],f['fold']):f for f in old['fold_audits'] if f['kind']=='soft_domestic_order'};runs=[];audits=[];cache=R/'v31-anchored-zero-shade-cache';cache.mkdir(exist_ok=True)
 sources=['evidence-v31.json','benchmark-targets-v31.json','v31-refit-validation.json','regional-rank-fix-validation-v30.json','refit_anchored_context_v31.py','validate_anchored_refit_v31.py','model-config-v28.json','predictor_v28.py','predictor_v27.py'];hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources}
 for seed in metrics.SEEDS:
  g=np.zeros(len(t));b=np.zeros(len(t),bool);prob=np.zeros(len(t))
  for f in (f for f in current['fold_audits'] if f['seed']==seed):
   p=cache/f"{seed}-{f['fold']}.json";train=[by[id] for id in f['training_ids']];te=[ix[id] for id in f['validation_ids']];oldf=prior[seed,f['fold']];assert f['training_ids']==oldf['training_ids']
   if p.exists():item=json.loads(p.read_text());assert item['source_hashes']==hashes
   else:
    value=rank.fit(train,seed*100+f['fold'],oldf['fit']);cfg=deepcopy(f['fit']);cfg['ranking_model']=value;item={'source_hashes':hashes,'seed':seed,'fold':f['fold'],'training_ids':f['training_ids'],'validation_ids':f['validation_ids'],'fit':cfg};p.write_text(json.dumps(item,indent=2)+'\n')
   gg,bb,pp=predict([t[i] for i in te],item['fit'],'legacy_reference');g[te]=gg;b[te]=bb;prob[te]=pp;audits.append(item)
  s,j,eq=relation_score(t,g,b,direct);runs.append({'seed':seed,'margins':g.tolist(),'predicted_meaningful':b.tolist(),'premium_scores':prob.tolist(),'score':s,'legacy_joint_score':j,'relation_score':eq});print('Anchored',seed,eq['both_relation_and_size_correct'],eq['exact_ties_correct'],flush=True)
 full=deepcopy(current['full_model']);full['ranking_model']=rank.fit(t,30001,old['full_models']['soft_domestic_order']);(R/'v31-anchored-full-config.json').write_text(json.dumps(full,indent=2)+'\n');summary={k:float(np.mean([q['relation_score'][k] for q in runs])) for k in ('both_relation_and_size_correct','both_relation_and_size_accuracy','balanced_joint_accuracy','exact_ties_correct')}
 out={'protocol':'Samev31 targets,conditional32feature architecture,exactequalityconstraints andfamilyfolds asfirstrefit. Replacezero-centered ridge byshrinkage towardmatchingv30rankfit paddedwith9zeros. Everyinnerprior excludesinnerholdout; outerprior excludesouterholdout. Usealreadyrefittedv31premium head withfrozenlegacyreference encoder; no additionalpremium fitting. Tests conservativeweightupdate,not additionaldata ornewlabels.','source_hashes':hashes,'runs':runs,'summary':summary,'fold_audits':audits,'full_model':full};(R/'v31-anchored-validation.json').write_text(json.dumps(out,indent=2)+'\n')
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 print(json.dumps(summary))
if __name__=='__main__':main()
