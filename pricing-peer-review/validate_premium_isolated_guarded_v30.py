from pathlib import Path
import json,hashlib
import numpy as np
import premium_isolated_guarded_v30 as model
import refit_simple_benchmark_v16 as metrics
R=Path(__file__).resolve().parent

def refit(rows,cfg):
 cfg=json.loads(json.dumps(cfg));ix={q['id']:i for i,q in enumerate(rows)};h=np.zeros((len(rows),len(model.HEAD_NAMES)))
 for f in cfg['inner_selection']['partitions']:
  te=[ix[id] for id in f['validation_ids']];hh,_=model.head_features([rows[i] for i in te],f['fit']);h[te]=hh
 full_h,_=model.head_features(rows,cfg['value_model']);heads={k:model.fit_head(rows,h,full_h,k) for k in ('balanced_size','joint_groups')};cfg.update(premium_models=heads,premium_model=heads['balanced_size'],model_id='foundation_amplifiers_robust_premium_v30');return cfg

def main():
 old=json.loads((R/'foundation-amplifiers-validation-v30.json').read_text());t=json.loads((R/'benchmark-targets-v30.json').read_text())['rows'];e=json.loads((R/'evidence-v30.json').read_text())['rows'];by={q['id']:q for q in t};ix={q['id']:i for i,q in enumerate(t)};direct=metrics.verified_materiality(e);runs={k:[] for k in ('guarded_isolated_balanced','guarded_isolated_joint')};audits=[]
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ('evidence-v30.json','benchmark-targets-v30.json','premium-semantics-clarification.json','foundation-amplifiers-validation-v30.json','premium_isolated_guarded_v30.py','validate_premium_isolated_guarded_v30.py','model-config-v28.json','predictor_v28.py','predictor_v27.py')}
 for seed in metrics.SEEDS:
  data={k:{'g':np.zeros(len(t)),'large':np.zeros(len(t),bool),'p':np.zeros(len(t))} for k in runs}
  for f in (f for f in old['fold_audits'] if f['seed']==seed):
   train=[by[id] for id in f['training_ids']];te=[ix[id] for id in f['validation_ids']];cfg=refit(train,f['fit']);audits.append(dict(f,fit=cfg))
   for h,k in (('balanced_size','guarded_isolated_balanced'),('joint_groups','guarded_isolated_joint')):
    g,sg,b,p=model.predict_many([t[i] for i in te],cfg,h);data[k]['g'][te]=g;data[k]['large'][te]=b;data[k]['p'][te]=p
  for k,v in data.items():
   s,j=model.score_outputs(t,v['g'],v['large'],direct);runs[k].append({'seed':seed,'margins':v['g'].tolist(),'predicted_meaningful':v['large'].tolist(),'premium_scores':v['p'].tolist(),'score':s,'joint_score':j})
 full=refit(t,old['full_model']);(R/'premium-isolated-guarded-config-v30.json').write_text(json.dumps(full,indent=2)+'\n');summary=metrics.summarize(runs);js={k:{f:float(np.mean([q['joint_score'][f] for q in rs])) for f in ('both_axes_correct','both_axes_accuracy','balanced_accuracy','correct','accuracy')} for k,rs in runs.items()}
 out={'protocol':'Same contextual foundation utility andtrain-only innerOOF predictions asfirsttwo-head experiment. Oneextra feature: intrinsicwinner isfiveyearsyounger,sameprovenance,bothgolden/pale,taregap<=5. It identifies a relatively isolated vintage distinction instead of inferring clarity solely fromvaluegap. Exclude35-vs40 whenyoungerhasheaviertare, respecting theexisting round51-17/round52-3 slight-premium boundary. Guard selected fromexisting evidence; no independent prospective claim. One addednonnegative premium coefficient; valueweights andoriginal13features unchanged. Attribution experiment didnotimprove results andisnotincluded inthisarm. Both declared weightingvariants evaluated. This refinement followed initialhead diagnostic,so reusedoutervalidation remains exploratory.','source_hashes':hashes,'runs':runs,'summary':summary,'joint_summary':js,'fold_audits':audits,'full_model':full};(R/'premium-isolated-guarded-validation-v30.json').write_text(json.dumps(out,indent=2)+'\n')
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 print(json.dumps({'joint':js,'summary':summary},indent=2))
if __name__=='__main__':main()
