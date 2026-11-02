"""A separately fitted contextual premium head with frozen V28 ranking."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
from predictor_v28 import Model as V28
from predictor_premium_v37 import Model as V37
from premium_winning_gap_v35 import stats
import compare_models as grouping
R=Path(__file__).resolve().parent
RIDGES=(.001,.01,.1,1.)
def features(q,m):
 a,b=q['a'],q['b'];g=m.compare(a,b)['margin'];sg=1 if g>1e-7 else -1 if g<-1e-7 else 0;va,vb=(40-a[2])/20,(40-b[2])/20;ta,tb=(130-a[3])/20,(130-b[3])/20;wv=(va+vb+sg*(va-vb))/2;wt=(ta+tb+sg*(ta-tb))/2
 def shade(o):return (3 if o[1]=='pale/straw' and o[3]==130 else m.domain['shades'].index(o[1]))/4
 sd=sg*(shade(a)-shade(b));c=m._pair(a,b)*m.weights;parts=np.array([sum(c[:9]),sum(c[9:13]),sum(c[13:17]),c[17],c[18],c[19]]);opposition=max(0.,(sum(abs(parts))-abs(g))/2)
 def top(o):return o[0] in ('Western Europe','northeast') and o[1]=='pale/straw' and o[2]==20 and o[3]==110
 completion=abs(int(top(a))-int(top(b)));pure=a[:3]==b[:3] and abs(a[3]-b[3])==5 and not completion
 region=[sd*(float((a if sg>0 else b)[0]==z) if sg else 0.) for z in m.domain['provenances'][1:]]
 return np.array([1.,abs(g),(va+vb)/2,(ta+tb)/2,wv,wt,sd,sg*sum(c[:9]),opposition,sd*wv,sd*wt,float(completion),float(pure),*region])
def fit(x,y,ridge):
 mean=x.mean(axis=0);scale=x.std(axis=0);mean[0]=0;scale[0]=1;scale[scale<1e-6]=1;xx=(x-mean)/scale
 def obj(w):
  z=xx@w;pen=w.copy();pen[0]=0;return float(np.mean(np.logaddexp(0,z)-y*z)+ridge*(pen@pen)/2),xx.T@(expit(z)-y)/len(y)+ridge*pen
 bounds=[(None,None)]*x.shape[1];bounds[1]=(0,None);bounds[11]=(0,None);bounds[12]=(None,0)
 result=minimize(obj,np.zeros(x.shape[1]),jac=True,bounds=bounds,method='L-BFGS-B',options={'ftol':1e-12,'maxiter':1000});assert result.success,result.message
 return {'weights':result.x.tolist(),'mean':mean.tolist(),'scale':scale.tolist(),'ridge':ridge,'solver_message':result.message}
def predict(x,c):return expit(((x-np.array(c['mean']))/np.array(c['scale']))@c['weights'])
def select(x,y,groups,seed):
 parts=list(grouping.folds(groups,3,seed));scores={}
 for ridge in RIDGES:
  prob=np.zeros(len(y))
  for tr,te in parts:prob[te]=predict(x[te],fit(x[tr],y[tr],ridge))
  p=prob>.5;balanced=np.mean([np.mean(p[y==v]==v) for v in (0,1) if np.any(y==v)]);scores[ridge]=(float(balanced),float(np.mean(p==y)))
 ridge=max(RIDGES,key=lambda v:(*scores[v],v));c=fit(x,y,ridge);c['inner_scores']=scores;return c

def main():
 rows=json.loads((R/'benchmark-targets-v38.json').read_text())['rows'];ev=json.loads((R/'evidence-v38.json').read_text())['rows'];m=V28();v37=V37();x=np.array([features(q,m) for q in rows]);g=np.array([m.compare(q['a'],q['b'])['margin'] for q in rows]);known=np.array([q['materiality_target'] is not None for q in rows]);y=np.array([q['materiality_target'] not in (None,0) for q in rows]);direct=np.array([q.get('materiality_support')=='direct_two_axis_response' or q.get('explicit_materiality') is not None for q in ev]);groups=np.array([repr((tuple(sorted([q['a'][0],q['b'][0]])),tuple(sorted([q['a'][1],q['b'][1]])))) for q in rows]);baselines={'v28':stats(rows,g,abs(g)>1+1e-8,direct),'v37':stats(rows,g,np.array([v37.compare(q['a'],q['b'])['predicted_meaningfulness']=='meaningful_difference' for q in rows]),direct)};runs=[];audit=[]
 for seed in (11,29,47,71,103):
  prob=np.zeros(len(rows))
  for fold,(tr,te) in enumerate(grouping.folds(groups,5,seed)):
   labeled=tr[known[tr]];c=select(x[labeled],y[labeled],groups[labeled],seed*100+fold);prob[te]=predict(x[te],c);audit.append({'seed':seed,'fold':fold,'training_ids':[rows[i]['id'] for i in tr],'validation_ids':[rows[i]['id'] for i in te],'fit':c})
  runs.append({'seed':seed,'scores':prob.tolist(),'predicted_meaningful':(prob>.5).tolist(),'metrics':stats(rows,g,prob>.5,direct)});print(seed,runs[-1]['metrics']['all'],flush=True)
 full=select(x[known],y[known],groups[known],38001);pp=predict(x,full);out={'protocol':'Seecontext-head-protocol-v38.json, frozen before fitting.22coefficients,including9regularizedregionalshade deviations. Equalper-case logisticloss, trainonly scaling/ridgeselection, threshold.5,25outerfamilyfolds. RankfrozenV28; conditionalheadvalidation, historicalrankexposure. Prospectiveanswers nowdevelopmentdata.','baselines':baselines,'runs':runs,'fold_audits':audit,'full_fit':full,'full_fit_metrics':stats(rows,g,pp>.5,direct),'full_scores':pp.tolist(),'source_hashes':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['context-head-protocol-v38.json','benchmark-targets-v38.json','evidence-v38.json','contextual_premium_v38.py','model-config-v28.json','premium-config-v37.json']}}
 (R/'context-head-validation-v38.json').write_text(json.dumps(out,indent=2)+'\n');print('baselines',baselines);print('MEAN',{k:float(np.mean([v['metrics']['all'][k] for v in runs])) for k in baselines['v28']['all']})
if __name__=='__main__':main()
