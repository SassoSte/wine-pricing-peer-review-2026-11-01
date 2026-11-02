"""Separate ranking, exact equality and meaningfulness after voice corrections."""
from pathlib import Path
import json,hashlib,numpy as np
import global_priority_v31 as global_model
from predictor_v28 import Model as Baseline
from predictor_rank_soft_order_v30 import Model as PremiumCandidate
R=Path(__file__).resolve().parent
def metrics(rows,g,p=None):
 d=np.array([q['known_direction'] or 0 for q in rows]);ex=np.array([q.get('exact_price_equality') is True for q in rows]);sg=np.where(np.array(g)>1e-7,1,np.where(np.array(g)<-1e-7,-1,0));mask=d!=0
 out={'direction_n':int(mask.sum()),'direction_correct':int(sum(sg[mask]==d[mask])),'exact_n':int(ex.sum()),'exact_correct':int(sum(sg[ex]==0))}
 if p is not None:
  size=np.array([q['materiality_target'] is not None for q in rows]);truth=np.array([q['materiality_target'] not in (None,0) for q in rows]);pr=np.array(p,dtype=bool);out.update(size_n=int(size.sum()),size_correct=int(sum(pr[size]==truth[size])),false_premiums=int(sum(size&~truth&pr)),missed_premiums=int(sum(size&truth&~pr)))
 return out
def family(q):return (tuple(sorted([q['a'][0],q['b'][0]])),tuple(sorted([q['a'][1],q['b'][1]])))
def main():
 rows=json.loads((R/'benchmark-targets-v32.json').read_text())['rows'];oldrows=json.loads((R/'benchmark-targets-v31.json').read_text())['rows'];by={q['id']:q for q in rows};ix={q['id']:i for i,q in enumerate(rows)};prior=json.loads((R/'global-priority-validation-v31.json').read_text());common=[by[q['id']] for q in oldrows];cached=json.loads((R/'v31-refit-validation.json').read_text());rescore={}
 for name in ('v28','frozen_v30_candidate'):
  rescore[name]=[metrics(common,x['margins'],x['predicted_meaningful']) for x in cached['runs'][name]]
 rescore['frozen_global']=[metrics(common,x['margins']) for x in prior['runs']['ordered']]
 runs=[];audits=[]
 for seed in (11,29,47,71,103):
  g=np.zeros(len(rows));seen=set()
  for f in [f for f in prior['fold_audits'] if f['seed']==seed and f['arm']=='ordered']:
   families={family(by[id]) for id in f['validation_ids']};test=[q for q in rows if family(q) in families];train=[q for q in rows if family(q) not in families];assert not seen.intersection(q['id'] for q in test);seen.update(q['id'] for q in test)
   cfg=global_model.select(train,seed*100+f['fold'],True);positions=[ix[q['id']] for q in test];g[positions]=global_model.design(test)@cfg['coefficients'];audits.append({'seed':seed,'fold':f['fold'],'training_ids':[q['id'] for q in train],'validation_ids':[q['id'] for q in test],'fit':cfg})
  assert len(seen)==len(rows);runs.append({'seed':seed,'margins':g.tolist(),'metrics_all':metrics(rows,g),'metrics_common':metrics(common,g[:len(common)])});print('seed',seed,runs[-1]['metrics_all'],flush=True)
 full=global_model.select(rows,31001,True);latest=[q for q in rows if q.get('latest_source_id','').startswith('voice-v32:')];diagnostics={}
 for name,model in [('v28',Baseline()),('frozen_premium_candidate',PremiumCandidate())]:
  diagnostics[name]=[{'id':q['id'],'prediction':model.compare(q['a'],q['b']),'target':q} for q in latest]
 out={'protocol':'Frozen existing OOF predictions rescored on640common pairs with correctedv32 labels. New642row global ranking refit uses same outer family membership; two added rows assigned by existing family, train-only inner selection. Premium assessor not refitted: full-config six-case diagnostics are seen-data checks, not heldout validation. Exact equality never approximated by meaningfulness band.','frozen_common_rescore':rescore,'global_v32_runs':runs,'fold_audits':audits,'full_global_model':full,'six_case_frozen_diagnostics':diagnostics,'source_hashes':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['evidence-v32.json','benchmark-targets-v32.json','evaluate_voice_v32.py','global-priority-validation-v31.json','model-config-v28.json']}}
 (R/'voice-validation-v32.json').write_text(json.dumps(out,indent=2)+'\n')
 for name,rs in rescore.items():print(name,{k:float(np.mean([r[k] for r in rs])) for k in rs[0]})
 for name,rs in diagnostics.items():print('DIAG',name,[(r['id'],r['prediction'].get('predicted_direction'),r['prediction'].get('predicted_meaningful'),r['prediction'].keys()) for r in rs][:1])
if __name__=='__main__':main()
