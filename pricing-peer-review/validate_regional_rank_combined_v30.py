from pathlib import Path
import json,hashlib
import numpy as np
import regional_rank_combined_v30 as fit
from regional_rank_combined_v30 import base
from validate_premium_losses_v30 import claim_metrics
import refit_simple_benchmark_v16 as metrics
R=Path(__file__).resolve().parent

def main():
 prior=json.loads((R/'foundation-amplifiers-validation-v30.json').read_text());context=json.loads((R/'premium-context-extension-validation-v30.json').read_text());t=json.loads((R/'benchmark-targets-v30.json').read_text())['rows'];e=json.loads((R/'evidence-v30.json').read_text())['rows'];by={q['id']:q for q in t};ix={q['id']:i for i,q in enumerate(t)};direct=np.array(metrics.verified_materiality(e));runs={k:[] for k in ('v28','shared_context',*fit.KINDS)};audits=[];cache=R/'regional-rank-combined-cache-v30';cache.mkdir(exist_ok=True)
 sources=['evidence-v30.json','benchmark-targets-v30.json','model-config-v28.json','predictor_v28.py','predictor_v27.py','premium-context-extension-validation-v30.json','foundation-amplifiers-validation-v30.json','regional_rank_combined_v30.py','validate_regional_rank_combined_v30.py'];hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources}
 for seed in metrics.SEEDS:
  data={k:{'g':np.zeros(len(t)),'b':np.zeros(len(t),bool),'p':np.zeros(len(t))} for k in runs}
  for k,rs in [('v28',context['runs']['v28']),('shared_context',context['runs']['adjacent_shade_extension'])]:
   q=next(q for q in rs if q['seed']==seed);data[k]={'g':np.array(q['margins']),'b':np.array(q['predicted_meaningful'],bool),'p':q['premium_scores']}
  for f in (f for f in prior['fold_audits'] if f['seed']==seed):
   train=[by[id] for id in f['training_ids']];te=[ix[id] for id in f['validation_ids']]
   for kind in fit.KINDS:
    p=cache/f"{kind}-{seed}-{f['fold']}.json"
    if p.exists():item=json.loads(p.read_text());assert item['source_hashes']==hashes
    else:
     cfg=fit.fit(train,seed*100+f['fold'],kind);item={'source_hashes':hashes,'kind':kind,'seed':seed,'fold':f['fold'],'training_ids':f['training_ids'],'validation_ids':f['validation_ids'],'fit':cfg};p.write_text(json.dumps(item,indent=2)+'\n')
    cfg=item['fit'];g,sg,b,pred=base.predict_many([t[i] for i in te],cfg,'balanced_size');data[kind]['g'][te]=g;data[kind]['b'][te]=b;data[kind]['p'][te]=pred;audits.append(item)
  for k,v in data.items():
   s,j=base.score_outputs(t,v['g'],v['b'],direct);runs[k].append({'seed':seed,'margins':v['g'].tolist(),'predicted_meaningful':v['b'].tolist(),'premium_scores':np.asarray(v['p']).tolist() if v['p'] is not None else None,'score':s,'joint_score':j,'all_labels':claim_metrics(t,v['g'],v['b'],np.ones(len(t),bool)),'direct_labels':claim_metrics(t,v['g'],v['b'],direct)})
  print('Completed',seed,[(k,runs[k][-1]['score']['direction']['correct'],runs[k][-1]['joint_score']['both_axes_correct']) for k in runs],flush=True)
 full={}
 for kind in fit.KINDS:
  full[kind]=fit.fit(t,30001,kind);(R/f'regional-rank-{kind}-full-v30.json').write_text(json.dumps(full[kind],indent=2)+'\n')
 summary={k:{v:{f:(rs[0][v][f] if f in ('n','meaningful_n','nonpremium_n') else float(np.mean([q[v][f] for q in rs]))) for f in rs[0][v]} for v in ('all_labels','direct_labels')} for k,rs in runs.items()};js={k:{f:float(np.mean([q['joint_score'][f] for q in rs])) for f in ('both_axes_correct','both_axes_accuracy','balanced_accuracy')} for k,rs in runs.items()}
 out={'protocol':'Samev30 and25outerfamilyfolds. Combinedcenteredregional ridge andsoftdomesticordering penalty,afterindividualablations; no newvaluefeatures. Adaptiveexploratory combination,not preregistered independenttest. Ridge strength chosen ontraining-only grouped innerdirection accuracy. Existing extendedpremium architecture,loss,ridge,cutoff andprotectedcases retained,head refit fromnewinnerOOF inputs. Frozenv28 andprevioussharedcontext controls. No evidence change orquestionnaire. Adaptive exploratory comparison,not prospective.','source_hashes':hashes,'runs':runs,'claim_summary':summary,'joint_summary':js,'separate_summary':metrics.summarize(runs),'fold_audits':audits,'full_models':full,'order_prior_source':'User Monopoly-board hierarchy: northeast first, southwest/southeast next,central/northwest slightlybelow; laterclarification northwestweakestdomestic. Soft preference only; no enforcedstrict ranking or numericalpremium.'}
 (R/'regional-rank-combined-validation-v30.json').write_text(json.dumps(out,indent=2)+'\n')
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 print(json.dumps(js,indent=2))
if __name__=='__main__':main()
