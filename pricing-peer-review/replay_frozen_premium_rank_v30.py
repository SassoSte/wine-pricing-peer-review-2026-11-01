from pathlib import Path
import json,hashlib
import numpy as np
from regional_rank_regularization_v30 import base
from validate_premium_losses_v30 import claim_metrics
import refit_simple_benchmark_v16 as metrics
R=Path(__file__).resolve().parent

def main():
 a=json.loads((R/'regional-rank-fix-validation-v30.json').read_text());b=json.loads((R/'regional-rank-combined-validation-v30.json').read_text());t=json.loads((R/'benchmark-targets-v30.json').read_text())['rows'];e=json.loads((R/'evidence-v30.json').read_text());direct=np.array(metrics.verified_materiality(e['rows']));runs={}
 for kind,source in [('centered_regions',a),('soft_domestic_order',a),('combined',b)]:
  series=[]
  for ranking,premium in zip(source['runs'][kind],a['runs']['shared_context']):
   assert ranking['seed']==premium['seed'];g=np.array(ranking['margins']);large=np.array(premium['predicted_meaningful']);s,j=base.score_outputs(t,g,large,direct);series.append({'seed':ranking['seed'],'margins':g.tolist(),'predicted_meaningful':premium['predicted_meaningful'],'premium_scores':premium['premium_scores'],'score':s,'joint_score':j,'all_labels':claim_metrics(t,g,large,np.ones(len(t),bool)),'direct_labels':claim_metrics(t,g,large,direct)})
  runs[kind+'_frozen_premium']=series
 summary={k:{view:{f:float(np.mean([q[view][f] for q in rs])) for f in ('premium_precision','correct_premium_recall','false_premiums','wrong_winner_premiums','missed_premiums')} for view in ('all_labels','direct_labels')} for k,rs in runs.items()};js={k:{f:float(np.mean([q['joint_score'][f] for q in rs])) for f in ('both_axes_correct','both_axes_accuracy','balanced_accuracy')} for k,rs in runs.items()}
 out={'protocol':'No additional fitting. Pair eachtraining-only rankingfold withmatching frozenpremium assessor. Referenceencoder/head/score/meaningfulness frozen; updatedintrinsic ranking independent. Wrongwinner premiumundernewrank counted aserror. No pair-routing oranswerlookup. Sameouterfamily exclusions.','source_hashes':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ('regional-rank-fix-validation-v30.json','regional-rank-combined-validation-v30.json','evidence-v30.json','benchmark-targets-v30.json','replay_frozen_premium_rank_v30.py')},'runs':runs,'claim_summary':summary,'joint_summary':js};(R/'regional-rank-frozen-premium-validation-v30.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
