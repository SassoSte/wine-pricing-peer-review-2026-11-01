from pathlib import Path
import json,hashlib
import numpy as np
import foundation_amplifiers_v30 as model
from premium_losses_v30 import fit_head
import refit_simple_benchmark_v16 as metrics
R=Path(__file__).resolve().parent
ARMS=('equal_case','false_premium_2x')

def refit(rows,cfg):
 cfg=json.loads(json.dumps(cfg));ix={q['id']:i for i,q in enumerate(rows)};h=np.zeros((len(rows),len(model.HEAD_NAMES)))
 for f in cfg['inner_selection']['partitions']:
  te=[ix[id] for id in f['validation_ids']];hh,_=model.head_features([rows[i] for i in te],f['fit']);h[te]=hh
 full_h,_=model.head_features(rows,cfg['value_model']);heads={k:fit_head(rows,h,full_h,k) for k in ARMS};cfg.update(premium_models=heads,premium_model=heads['equal_case']);return cfg

def claim_metrics(rows,g,large,mask):
 direction=np.array([q['known_direction'] or 0 for q in rows]);mat=np.array([np.nan if q['materiality_target'] is None else q['materiality_target'] for q in rows]);known=np.isfinite(mat)&mask;pos=known&(mat!=0);neg=known&(mat==0);sign=np.where(g>1e-7,1,np.where(g<-1e-7,-1,0));tp=pos&large&(sign==direction);fp=neg&large;wrong=pos&large&(sign!=direction);miss=pos&~large;claims=tp.sum()+fp.sum()+wrong.sum()
 return {'n':int(known.sum()),'meaningful_n':int(pos.sum()),'nonpremium_n':int(neg.sum()),'correct_premiums':int(tp.sum()),'false_premiums':int(fp.sum()),'wrong_winner_premiums':int(wrong.sum()),'missed_premiums':int(miss.sum()),'premium_precision':float(tp.sum()/claims) if claims else None,'correct_premium_recall':float(tp.sum()/pos.sum()),'premium_calls':int(claims),'cost_1x':float(fp.sum()+wrong.sum()+miss.sum()),'cost_2x':float(2*(fp.sum()+wrong.sum())+miss.sum())}

def main():
 old=json.loads((R/'foundation-amplifiers-validation-v30.json').read_text());t=json.loads((R/'benchmark-targets-v30.json').read_text())['rows'];e=json.loads((R/'evidence-v30.json').read_text())['rows'];by={q['id']:q for q in t};ix={q['id']:i for i,q in enumerate(t)};direct=np.array(metrics.verified_materiality(e));runs={k:[] for k in ('v28','class_balanced',*ARMS)};audits=[]
 sources=['evidence-v30.json','benchmark-targets-v30.json','foundation-amplifiers-validation-v30.json','foundation-amplifiers-selected-config-v30.json','foundation_amplifiers_v30.py','premium_losses_v30.py','validate_premium_losses_v30.py','model-config-v28.json','predictor_v28.py','predictor_v27.py'];hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources}
 for seed in metrics.SEEDS:
  data={k:{'g':np.zeros(len(t)),'large':np.zeros(len(t),bool),'p':None} for k in runs}
  for src,name in [('v28','v28'),('separate_premium_balanced','class_balanced')]:
   q=next(q for q in old['runs'][src] if q['seed']==seed);data[name]={'g':np.array(q['margins']),'large':np.array(q['predicted_meaningful'],bool),'p':q['premium_scores']}
  for f in (f for f in old['fold_audits'] if f['seed']==seed):
   tr=[by[id] for id in f['training_ids']];te=[ix[id] for id in f['validation_ids']];cfg=refit(tr,f['fit']);assert cfg['value_model']==f['fit']['value_model'];audits.append({'seed':seed,'fold':f['fold'],'training_ids':f['training_ids'],'validation_ids':f['validation_ids'],'fit':cfg})
   for k in ARMS:
    g,sg,b,p=model.predict_many([t[i] for i in te],cfg,k);data[k]['g'][te]=g;data[k]['large'][te]=b
    if data[k]['p'] is None:data[k]['p']=np.zeros(len(t))
    data[k]['p'][te]=p
  for k,v in data.items():
   if k in ARMS:np.testing.assert_array_equal(v['g'],data['class_balanced']['g'])
   s,j=model.score_outputs(t,v['g'],v['large'],direct);runs[k].append({'seed':seed,'margins':v['g'].tolist(),'predicted_meaningful':v['large'].tolist(),'premium_scores':np.asarray(v['p']).tolist() if v['p'] is not None else None,'score':s,'joint_score':j,'all_labels':claim_metrics(t,v['g'],v['large'],np.ones(len(t),bool)),'direct_labels':claim_metrics(t,v['g'],v['large'],direct)})
  print('Completed',seed,[(k,runs[k][-1]['all_labels']['false_premiums'],runs[k][-1]['all_labels']['missed_premiums']) for k in runs],flush=True)
 full=refit(t,old['full_model']);(R/'premium-losses-full-v30.json').write_text(json.dumps(full,indent=2)+'\n');template=json.loads((R/'foundation-amplifiers-selected-config-v30.json').read_text())
 for k in ARMS:
  cfg=json.loads(json.dumps(template));cfg['model_id']='foundation_premium_'+k+'_v30_experimental';cfg['premium_model']=full['premium_models'][k];cfg['status']='experimental_v28_remains_active';(R/f'premium-loss-{k}-config-v30.json').write_text(json.dumps(cfg,indent=2)+'\n')
 summary={k:{view:{field:(rs[0][view][field] if field in ('n','meaningful_n','nonpremium_n') else float(np.mean([q[view][field] for q in rs]))) for field in rs[0][view]} for view in ('all_labels','direct_labels')} for k,rs in runs.items()};js={k:{f:float(np.mean([q['joint_score'][f] for q in rs])) for f in ('both_axes_correct','both_axes_accuracy','balanced_accuracy')} for k,rs in runs.items()}
 out={'protocol':'Only premiumhead loss weights change: equal per-case1:1 orfalse-premium2:1, versusoriginalbalancedclasses. Each loss normalized tosum1; ridge.03,features,standardization,0.5cutoff,protectedtrainingcontrols andallvalueweights fixed. Newhead usesoriginaltraining-only innerOOF inputs. No threshold tuning orvalue refit. Same25outerfamilyfolds; v28frozenbenchmark. All-size anddirect-size views reported; no older labels dropped. Twofold falsecost is a testscenario,not elicited requirement.','source_hashes':hashes,'row_ids':[q['id'] for q in t],'runs':runs,'claim_summary':summary,'joint_summary':js,'separate_summary':metrics.summarize(runs),'fold_audits':audits,'full_model':full}
 (R/'premium-loss-validation-v30.json').write_text(json.dumps(out,indent=2)+'\n')
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 print(json.dumps({'claim_summary':summary,'joint_summary':js},indent=2))
if __name__=='__main__':main()
