"""Small premium-only correction around frozen v28; no ranking refit."""
from pathlib import Path
import itertools,json,hashlib
import numpy as np
from predictor_v28 import Model
import compare_models as grouping
R=Path(__file__).resolve().parent
GRID=(0.,.1,.2,.35,.5,.7,1.)
def context(a,b):
 if abs(a[2]-b[2])!=5 or (a[2]-b[2])*(a[3]-b[3])>=0:return 0.,0.,1.
 gap=abs(a[3]-b[3]);lighter=a if a[3]<b[3] else b;return float(gap==5),max(0.,(gap-10)/5),float(lighter[1]!='brown')
def predict(g,x,params):
 small,big,nonbrown=params;return (abs(g)-1-small*x[:,0]+big*x[:,1]*(x[:,2] if nonbrown else 1.)*x[:,3])>1e-8
def choose(g,x,y,known,arm):
 params=[(0.,v,float(arm=='nonbrown_large_gap')) for v in GRID]
 def score(p):
  pred=predict(g,x,p);return (int(sum(pred[known]==y[known])),-int(sum(pred&known&~y)),-sum(p),-p[0],-p[1])
 return max(params,key=score)
def stats(rows,g,pred,direct):
 d=np.array([q['known_direction'] or 0 for q in rows]);known=np.array([q['materiality_target'] is not None for q in rows]);y=np.array([q['materiality_target'] not in (0,None) for q in rows]);sg=np.sign(g);out={}
 for name,mask in [('all',known),('direct',known&direct)]:
  both=mask&(d!=0);out[name]={'n':int(mask.sum()),'correct':int(sum(pred[mask]==y[mask])),'false_premiums':int(sum(pred&mask&~y)),'missed_premiums':int(sum(~pred&mask&y)),'both_n':int(both.sum()),'both_correct':int(sum((pred==y)&(sg==d)&both))}
 return out
def main():
 rows=json.loads((R/'benchmark-targets-v35.json').read_text())['rows'];evidence=json.loads((R/'evidence-v35.json').read_text())['rows'];assert [q['id'] for q in rows]==[q['id'] for q in evidence];m=Model();g=np.array([m.compare(q['a'],q['b'])['margin'] for q in rows]);x=np.array([context(q['a'],q['b']) for q in rows]);x=np.c_[x,np.array([g[i]*(q['b'][3]-q['a'][3])>1e-7 for i,q in enumerate(rows)])];known=np.array([q['materiality_target'] is not None for q in rows]);y=np.array([q['materiality_target'] not in (0,None) for q in rows]);direct=np.array([q.get('materiality_support')=='direct_two_axis_response' or q.get('explicit_materiality') is not None for q in evidence]);groups=np.array([repr((tuple(sorted([q['a'][0],q['b'][0]])),tuple(sorted([q['a'][1],q['b'][1]])))) for q in rows]);runs=[];audits=[]
 for seed in (11,29,47,71,103):
  preds={arm:np.zeros(len(rows),bool) for arm in ('large_gap_only','nonbrown_large_gap')}
  for fold,(tr,te) in enumerate(grouping.folds(groups,5,seed)):
   for arm in preds:
    params=choose(g[tr],x[tr],y[tr],known[tr],arm);preds[arm][te]=predict(g[te],x[te],params);audits.append({'seed':seed,'fold':fold,'arm':arm,'training_ids':[rows[i]['id'] for i in tr],'validation_ids':[rows[i]['id'] for i in te],'parameters':params})
  runs.append({'seed':seed,'arms':{arm:{'predicted_meaningful':p.tolist(),'metrics':stats(rows,g,p,direct)} for arm,p in preds.items()}})
 full={}
 for arm in ('large_gap_only','nonbrown_large_gap'):
  params=choose(g,x,y,known,arm);p=predict(g,x,params);full[arm]={'parameters':params,'metrics':stats(rows,g,p,direct),'predicted_meaningful':p.tolist()}
 out={'protocol':'Conditional calibration around frozen deployedv28: ranks and sourceweights neverrefit. Repeated5fold unorderedprovenance/shade family exclusions for selecting correctioncoefficients only. Historical baseline already trained on earlier evidence, so these are heldout calibration gains, not independentlyheldout accuracy for entirev28. Freshpilot now designmaterial, not prospectivevalidation. Primaryselection equal-per-case knownmeaningfulness accuracy; ties fewerfalsepremiums then smalleradjustment. Alltop/puretare/vintageonly unchanged byfeature. Onepositive coefficient boost onlywhen frozenranking favors lighteroffering; large opposingtaregap; compare unrestricted versus lighteroffering notbrown. 5lb suppression omitted after initialnegativeablation. Directsubset requires explicitmateriality/supportmetadata,not merely absenceofproxy flag.','source_hashes':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['evidence-v35.json','benchmark-targets-v35.json','model-config-v28.json','predictor_v27.py','premium_winning_gap_v35.py']},'baseline':stats(rows,g,abs(g)>1+1e-8,direct),'runs':runs,'fold_audits':audits,'full_fits':full,'row_ids':[q['id'] for q in rows],'frozen_margins':g.tolist(),'features':x.tolist(),'direct_mask':direct.tolist()}
 (R/'premium-winning-gap-validation-v35.json').write_text(json.dumps(out,indent=2)+'\n');print('baseline',out['baseline']);print('full', {k:{'parameters':v['parameters'],'metrics':v['metrics']} for k,v in full.items()})
 for arm in full:print(arm,{k:float(np.mean([v['arms'][arm]['metrics']['all'][k] for v in runs])) for k in out['baseline']['all']})
if __name__=='__main__':main()
