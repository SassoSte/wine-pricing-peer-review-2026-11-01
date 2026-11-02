"""One-coefficient context penalty on premium only; frozen value rankings."""
from pathlib import Path
import itertools,json,hashlib
import numpy as np
import compare_models as grouping
from predictor_v28 import Model as Baseline
from predictor_premium_v35 import Model as LargeTare
from premium_winning_gap_v35 import stats
R=Path(__file__).resolve().parent
GRID=(0.,.25,.5,.75,1.)
def feature(m,a,b,near=True):
 g=m.compare(a,b)['margin']
 if abs(g)<=1e-7:return 0.
 winner,loser=(a,b) if g>0 else (b,a)
 if loser[1]!='brown' or winner[1]=='brown' or (near and winner[1] not in ('copper','amber')):return 0.
 heaviness=max(0.,(winner[3]-120)/10)
 c=m._pair(a,b)*m.weights;sg=1 if g>0 else -1
 secondary=max(0.,sg*sum(c[:9]))+max(0.,sg*sum(c[9:13]))
 return heaviness*secondary

def choose(score,x,y,known):
 base=score>1e-8;valid=[]
 for gamma in GRID:
  pred=score-gamma*x>1e-8
  # Do not suppress a confirmed meaningful premium correctly recognized by the reference on training rows.
  if np.any(known&y&base&~pred):continue
  valid.append((int(sum(pred[known]==y[known])),-int(sum(known&~y&pred)),-gamma,gamma))
 return max(valid)[-1]
def main():
 rows=json.loads((R/'benchmark-targets-v37.json').read_text())['rows'];ev=json.loads((R/'evidence-v37.json').read_text())['rows'];b=Baseline();m=LargeTare();g=np.array([b.compare(q['a'],q['b'])['margin'] for q in rows]);score=np.array([m.compare(q['a'],q['b'])['premium_decision_score'] for q in rows]);xs={name:np.array([feature(b,q['a'],q['b'],near) for q in rows]) for name,near in [('heavy_secondary',False),('near_shade_heavy_secondary',True)]};y=np.array([q['materiality_target'] not in (None,0) for q in rows]);known=np.array([q['materiality_target'] is not None for q in rows]);direct=np.array([q.get('materiality_support')=='direct_two_axis_response' or q.get('explicit_materiality') is not None for q in ev]);groups=np.array([repr((tuple(sorted([q['a'][0],q['b'][0]])),tuple(sorted([q['a'][1],q['b'][1]])))) for q in rows]);runs=[];audits=[]
 for seed in (11,29,47,71,103):
  preds={name:np.zeros(len(rows),bool) for name in xs}
  for fold,(tr,te) in enumerate(grouping.folds(groups,5,seed)):
   for name,x in xs.items():
    gamma=choose(score[tr],x[tr],y[tr],known[tr]);preds[name][te]=score[te]-gamma*x[te]>1e-8;audits.append({'seed':seed,'fold':fold,'arm':name,'gamma':gamma,'training_ids':[rows[i]['id'] for i in tr],'validation_ids':[rows[i]['id'] for i in te]})
  runs.append({'seed':seed,'arms':{name:{'predicted_meaningful':v.tolist(),'metrics':stats(rows,g,v,direct)} for name,v in preds.items()}})
 full={}
 for name,x in xs.items():
  gamma=choose(score,x,y,known);pred=score-gamma*x>1e-8;full[name]={'gamma':gamma,'metrics':stats(rows,g,pred,direct),'predicted_meaningful':pred.tolist(),'changed_ids':[q['id'] for i,q in enumerate(rows) if pred[i]!=(score[i]>1e-8)]}
 out={'protocol':'v37 includes16prospectiveanswers once; question11post-disclosure correction retained. FrozenV28 ranking and frozen0.7large-tare correction. Two one-coefficient context alternatives, fixedfraction grid0/.25/.5/.75/1;trainingonly coefficientselection on25familyfolds, with no loss of reference-correct meaningful labels on training rows. Penalty affects positiveprovenance/shade contributions to premium only, losingofferingbrown, winnerheaviness ramp120to130lb; narrowarmrestrictswinnercopper/amber. No region/IDlookup. Conditional posthoccalibration, notfresh wholemodelvalidation.','baselines':{'v28':stats(rows,g,abs(g)>1+1e-8,direct),'large_tare':stats(rows,g,score>1e-8,direct)},'runs':runs,'fold_audits':audits,'full_fits':full,'row_ids':[q['id'] for q in rows],'features':{k:v.tolist() for k,v in xs.items()},'frozen_scores':score.tolist(),'source_hashes':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['evidence-v37.json','benchmark-targets-v37.json','model-config-v28.json','premium-config-v35.json','premium_context_v37.py']}}
 (R/'premium-context-validation-v37.json').write_text(json.dumps(out,indent=2)+'\n');print('BASE',out['baselines'])
 for name in xs:print(name,'full',full[name]['gamma'],full[name]['metrics'],'changes',full[name]['changed_ids']);print('mean',{k:float(np.mean([r['arms'][name]['metrics']['all'][k] for r in runs])) for k in out['baselines']['v28']['all']})
if __name__=='__main__':main()
