"""Focused premium-size test: discount opposing attribute contributions, preserve frozen v28 ranking."""
from pathlib import Path
import json,hashlib
import numpy as np
from predictor_v28 import Model
from premium_winning_gap_v35 import stats,context,choose,predict
R=Path(__file__).resolve().parent
GRID=(0.,.1,.25,.5,.75,1.,1.5,2.)
def components(m,a,b):
 c=m._pair(a,b)*m.weights
 return np.array([sum(c[:9]),sum(c[9:13]),sum(c[13:17]),c[17],c[18],c[19]])
def select(g,x,base_score,y,known):
 def score(gamma):
  p=base_score-gamma*x>1e-8
  return (int(sum(p[known]==y[known])),-int(sum(p&known&~y)),-gamma)
 return max(GRID,key=score)
def main():
 rows=json.loads((R/'benchmark-targets-v35.json').read_text())['rows'];evidence=json.loads((R/'evidence-v35.json').read_text())['rows'];prior=json.loads((R/'premium-winning-gap-validation-v35.json').read_text());by={q['id']:i for i,q in enumerate(rows)};m=Model();g=np.array(prior['frozen_margins']);xx=np.array(prior['features']);known=np.array([q['materiality_target'] is not None for q in rows]);y=np.array([q['materiality_target'] not in (None,0) for q in rows]);direct=np.array(prior['direct_mask']);cc=np.array([components(m,q['a'],q['b']) for q in rows]);assert np.allclose(cc.sum(axis=1),g)
 opp=(abs(cc).sum(axis=1)-abs(g))/2;opp=np.maximum(opp,0.);ratio=opp/(abs(g)+opp+1e-12);features={'absolute_opposition':opp,'relative_opposition':ratio};runs=[];audits=[]
 for seed in (11,29,47,71,103):
  preds={arm:np.zeros(len(rows),bool) for arm in features}
  for f in [f for f in prior['fold_audits'] if f['seed']==seed and f['arm']=='large_gap_only']:
   tr=np.array([by[id] for id in f['training_ids']]);te=np.array([by[id] for id in f['validation_ids']]);beta=f['parameters'][1];base_score=abs(g)-1+beta*xx[:,1]*xx[:,3]
   for arm,x in features.items():
    gamma=select(g[tr],x[tr],base_score[tr],y[tr],known[tr]);preds[arm][te]=base_score[te]-gamma*x[te]>1e-8;audits.append({'seed':seed,'fold':f['fold'],'arm':arm,'beta':beta,'gamma':gamma,'training_ids':f['training_ids'],'validation_ids':f['validation_ids']})
  runs.append({'seed':seed,'arms':{arm:{'metrics':stats(rows,g,p,direct),'predicted_meaningful':p.tolist()} for arm,p in preds.items()}})
 full={};base_score=abs(g)-1+.7*xx[:,1]*xx[:,3]
 for arm,x in features.items():
  gamma=select(g,x,base_score,y,known);pr=base_score-gamma*x>1e-8;full[arm]={'gamma':gamma,'metrics':stats(rows,g,pr,direct),'predicted_meaningful':pr.tolist(),'sweep':[{'gamma':v,'metrics':stats(rows,g,base_score-v*x>1e-8,direct)} for v in GRID]}
 details=[]
 for id in ['combined-pilot-v34-4','combined-pilot-v34-6','combined-pilot-v34-9']:
  i=by[id];details.append({'id':id,'a':rows[i]['a'],'b':rows[i]['b'],'contributions':dict(zip(['provenance','shade','vintage','tare','matched_vintage','tare_compensation'],cc[i].tolist())),'margin':float(g[i]),'opposing_contribution':float(opp[i]),'relative_opposition':float(ratio[i])})
 out={'protocol':'Two predefined single-coefficient opposition-discount variants, added to train-only selected large-tare correction; ranks and baseline coefficients frozen. Same25family splits as priorv35calibration. Scalar selection maximizes known size accuracy, then fewer falsepremiums, then smaller gamma. All655pairs retained; only413knownsize rows scored. Conditional calibration not independentlyheldout wholemodel. Questions4/6were hypothesis motivation; no freshvalidation claim.','baseline':prior['baseline'],'large_tare_runs':[{'seed':v['seed'],'metrics':v['arms']['large_gap_only']['metrics']} for v in prior['runs']],'runs':runs,'fold_audits':audits,'full_fits':full,'target_decomposition':details,'source_hashes':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['evidence-v35.json','benchmark-targets-v35.json','model-config-v28.json','premium-config-v35.json','premium_opposition_test_v35.py','premium-winning-gap-validation-v35.json']}}
 (R/'premium-opposition-validation-v35.json').write_text(json.dumps(out,indent=2)+'\n')
 print('targets',details)
 for arm in features:
  print(arm,'fullgamma',full[arm]['gamma'],'mean',{k:float(np.mean([v['arms'][arm]['metrics']['all'][k] for v in runs])) for k in prior['baseline']['all']});print('sweep',[(v['gamma'],v['metrics']['all']['correct'],v['metrics']['all']['false_premiums'],v['metrics']['all']['missed_premiums']) for v in full[arm]['sweep']])
if __name__=='__main__':main()
