from pathlib import Path
import json,hashlib
import numpy as np
import foundation_amplifiers_v30 as parent
import premium_context_same_shade_v30 as same
import premium_context_adjacent_shade_v30 as adjacent
import refit_simple_benchmark_v16 as metrics
from validate_premium_losses_v30 import claim_metrics
R=Path(__file__).resolve().parent
MODELS={'same_shade_extension':same,'adjacent_shade_extension':adjacent}
def refit(rows,cfg,mod):
 cfg=json.loads(json.dumps(cfg));ix={q['id']:i for i,q in enumerate(rows)};h=np.zeros((len(rows),len(mod.HEAD_NAMES)))
 for f in cfg['inner_selection']['partitions']:
  te=[ix[id] for id in f['validation_ids']];hh,_=mod.head_features([rows[i] for i in te],f['fit']);h[te]=hh
 full_h,_=mod.head_features(rows,cfg['value_model']);head=mod.fit_head(rows,h,full_h,'balanced_size');cfg.update(premium_models={'balanced_size':head},premium_model=head);return cfg

def main():
 parentval=json.loads((R/'foundation-amplifiers-validation-v30.json').read_text());previous=json.loads((R/'premium-isolated-guarded-validation-v30.json').read_text());t=json.loads((R/'benchmark-targets-v30.json').read_text())['rows'];e=json.loads((R/'evidence-v30.json').read_text())['rows'];by={q['id']:q for q in t};ix={q['id']:i for i,q in enumerate(t)};direct=np.array(metrics.verified_materiality(e));runs={k:[] for k in ('v28','shared_context',*MODELS)};audits=[]
 sources=['evidence-v30.json','benchmark-targets-v30.json','foundation-amplifiers-validation-v30.json','premium-isolated-guarded-validation-v30.json','premium_context_same_shade_v30.py','premium_context_adjacent_shade_v30.py','validate_premium_context_extension_v30.py','model-config-v28.json','predictor_v28.py','predictor_v27.py'];hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources}
 for seed in metrics.SEEDS:
  data={k:{'g':np.zeros(len(t)),'b':np.zeros(len(t),bool),'p':np.zeros(len(t))} for k in runs}
  for name,rs in [('v28',parentval['runs']['v28']),('shared_context',previous['runs']['guarded_isolated_balanced'])]:
   run=next(q for q in rs if q['seed']==seed);data[name]={'g':np.array(run['margins']),'b':np.array(run['predicted_meaningful'],bool),'p':run['premium_scores']}
  for f in (f for f in parentval['fold_audits'] if f['seed']==seed):
   train=[by[id] for id in f['training_ids']];te=[ix[id] for id in f['validation_ids']]
   for name,mod in MODELS.items():
    cfg=refit(train,f['fit'],mod);g,sg,b,p=mod.predict_many([t[i] for i in te],cfg,'balanced_size');data[name]['g'][te]=g;data[name]['b'][te]=b;data[name]['p'][te]=p;audits.append({'arm':name,'seed':seed,'fold':f['fold'],'training_ids':f['training_ids'],'validation_ids':f['validation_ids'],'fit':cfg})
  for name,v in data.items():
   if name in MODELS:np.testing.assert_array_equal(v['g'],data['shared_context']['g'])
   s,j=parent.score_outputs(t,v['g'],v['b'],direct);runs[name].append({'seed':seed,'margins':v['g'].tolist(),'predicted_meaningful':v['b'].tolist(),'premium_scores':np.asarray(v['p']).tolist() if v['p'] is not None else None,'score':s,'joint_score':j,'all_labels':claim_metrics(t,v['g'],v['b'],np.ones(len(t),bool)),'direct_labels':claim_metrics(t,v['g'],v['b'],direct)})
  print('Completed',seed,[(k,runs[k][-1]['joint_score']['both_axes_correct']) for k in runs],flush=True)
 full={}
 for name,mod in MODELS.items():
  full[name]=refit(t,parentval['full_model'],mod);(R/f'premium-{name}-full-v30.json').write_text(json.dumps(full[name],indent=2)+'\n')
 summary={k:{v:{f:(rs[0][v][f] if f in ('n','meaningful_n','nonpremium_n') else float(np.mean([q[v][f] for q in rs]))) for f in rs[0][v]} for v in ('all_labels','direct_labels')} for k,rs in runs.items()};js={k:{f:float(np.mean([q['joint_score'][f] for q in rs])) for f in ('both_axes_correct','both_axes_accuracy','balanced_accuracy')} for k,rs in runs.items()}
 out={'protocol':'Widen existing sharedcontext feature; no addedcoefficient. Same-shade thenadjacent-shade variants foryounger<=30 outsidegold/pale; preserveold35vs40counterweightguard andnewnonlightmatching-shade30vs35lowtareguard justified byrevision-8. Original14-headfeatures,loss,ridge,cutoff,valueweights,innerOOF valueinputs and25outerfamilies unchanged. Training-onlyheadfit. Adaptiveexploratory v30test,notfreshvalidation.','source_hashes':hashes,'runs':runs,'claim_summary':summary,'joint_summary':js,'fold_audits':audits,'full_models':full}
 (R/'premium-context-extension-validation-v30.json').write_text(json.dumps(out,indent=2)+'\n')
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 print(json.dumps({'joint':js,'claims':summary},indent=2))
if __name__=='__main__':main()
