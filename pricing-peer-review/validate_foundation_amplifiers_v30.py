from pathlib import Path
import json,hashlib
import numpy as np
import foundation_amplifiers_v30 as model
import refit_simple_benchmark_v16 as metrics
R=Path(__file__).resolve().parent

def main():
 prior=json.loads((R/'regional-interaction-validation-v30.json').read_text());t=json.loads((R/'benchmark-targets-v30.json').read_text())['rows'];e=json.loads((R/'evidence-v30.json').read_text())['rows'];by={q['id']:q for q in t};ix={q['id']:i for i,q in enumerate(t)};direct=metrics.verified_materiality(e)
 sources=['evidence-v30.json','benchmark-targets-v30.json','premium-semantics-clarification.json','model-config-v28.json','predictor_v28.py','predictor_v27.py','regional-interaction-validation-v30.json','foundation_amplifiers_v30.py','validate_foundation_amplifiers_v30.py'];hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources}
 cache=R/'foundation-amplifiers-cache-v30';cache.mkdir(exist_ok=True);runs={k:[] for k in ('v28','value_with_gap_threshold','separate_premium_balanced','separate_premium_joint')};audits=[]
 for seed in metrics.SEEDS:
  data={k:{'g':np.zeros(len(t)),'large':np.zeros(len(t),bool),'premium_score':np.zeros(len(t))} for k in runs}
  baseline=next(q for q in prior['runs']['v28'] if q['seed']==seed);data['v28']['g']=np.array(baseline['margins']);data['v28']['large']=abs(data['v28']['g'])>1+1e-8
  for f in (f for f in prior['fold_audits'] if f['seed']==seed):
   p=cache/f"{seed}-{f['fold']}.json";train=[by[id] for id in f['training_ids']];test=[by[id] for id in f['validation_ids']];te=[ix[id] for id in f['validation_ids']]
   if p.exists():item=json.loads(p.read_text());assert item['source_hashes']==hashes
   else:
    cfg=model.fit(train,seed*100+f['fold']);item={'source_hashes':hashes,'seed':seed,'fold':f['fold'],'training_ids':f['training_ids'],'validation_ids':f['validation_ids'],'fit':cfg};p.write_text(json.dumps(item,indent=2)+'\n')
   cfg=item['fit'];audits.append(item)
   for head,arm in (('balanced_size','separate_premium_balanced'),('joint_groups','separate_premium_joint')):
    g,sign,large,score=model.predict_many(test,cfg,head);data[arm]['g'][te]=g;data[arm]['large'][te]=large;data[arm]['premium_score'][te]=score
   data['value_with_gap_threshold']['g'][te]=g;data['value_with_gap_threshold']['large'][te]=abs(g)>cfg['ablation_radius']+1e-8
  for arm,v in data.items():
   score,js=model.score_outputs(t,v['g'],v['large'],direct);runs[arm].append({'seed':seed,'margins':v['g'].tolist(),'predicted_meaningful':v['large'].tolist(),'premium_scores':v['premium_score'].tolist() if arm.startswith('separate') else None,'score':score,'joint_score':js})
  print('Completed seed',seed,[(k,runs[k][-1]['joint_score']['both_axes_correct'],runs[k][-1]['score']['direction']['correct']) for k in runs],flush=True)
 full=model.fit(t,30001);(R/'foundation-amplifiers-config-v30.json').write_text(json.dumps(full,indent=2)+'\n');summary=metrics.summarize(runs);js={k:{field:float(np.mean([q['joint_score'][field] for q in rs])) for field in ('both_axes_correct','both_axes_accuracy','balanced_accuracy','correct','accuracy')} for k,rs in runs.items()}
 out={'protocol':'New two-head architecture on unchangedv30. Intrinsic23-term utility:9vintage/tarefoundation features,9provenance and4shade terms scaled by fixedcorecontext,1alltopcompletion term. No universal standalone provenance/shade offsets; foundation range constrained tocover combinedmodifier range; monotonic age/tare/shade. Value trained only on known directions; threefold training-only grouped selection of ridge. Premium justification logistic trained on cross-fitted value contributions plus opposingattributes andprofiledistinction,not onscoregaplabels; missing size staysmissing. Two declared premium weighting variants andsame-value common-radius ablation. Same25outerfamily partitions;v28frozenfoldpredictions rescored. Preservedanchor constraints use trainingrows only. No evidence relabeling; semanticclarification is guidance,not added trainingrow. Reused/adaptive validation; not freshprospective accuracy or market calibration.','source_hashes':hashes,'runs':runs,'summary':summary,'joint_summary':js,'fold_audits':audits,'full_model':full,'architecture':{'value_features':model.VALUE_NAMES,'premium_features':model.HEAD_NAMES,'value_ridges':model.ALPHAS,'premium_ridge':model.HEAD_RIDGE,'context_multiplier_formula':'.5+.25*(normalized_vintage_quality+normalized_tare_quality)','context_formula_qualification':'Predeclared engineering hypothesis implementing conditional amplification; not elicited economic weights or measured rarity.'}}
 (R/'foundation-amplifiers-validation-v30.json').write_text(json.dumps(out,indent=2)+'\n')
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 print(json.dumps({'joint':js,'summary':summary},indent=2))
if __name__=='__main__':main()
