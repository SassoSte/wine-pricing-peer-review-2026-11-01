"""Train-selected uncertainty bands for frozen V28 and frozen v37 premium scores."""
from pathlib import Path
import json,hashlib,collections
import numpy as np
from predictor_v28 import Model as V28
from predictor_premium_v37 import Model as V37
R=Path(__file__).resolve().parent
BANDS=[(lo,hi) for lo in (.7,.8,.9,.95,1.) for hi in (1.1,1.3,1.5,1.7,2.)]
CAP=.15

def metrics(score,y,lo,hi):
 band=(score>=lo)&(score<hi);keep=~band;pred=score>=hi
 return {'n':len(y),'withheld':int(sum(band)),'retained':int(sum(keep)),'coverage':float(np.mean(keep)),'retained_correct':int(sum(keep&(pred==y))),'retained_accuracy':float(np.mean(pred[keep]==y[keep])) if keep.any() else None,'false_premiums':int(sum(keep&pred&~y)),'missed_premiums':int(sum(keep&~pred&y)),'true_premiums_withheld':int(sum(band&y)),'nonpremiums_withheld':int(sum(band&~y))}
def choose(score,y):
 candidates=[]
 for lo,hi in BANDS:
  s=metrics(score,y,lo,hi)
  if s['withheld']/len(y)<=CAP:candidates.append((s['retained_accuracy'],-s['withheld'],lo,hi))
 if not candidates:raise ValueError('No band meets coverage constraint')
 return max(candidates)[2:]
def summarize_predictions(pred,y):
 known=pred!=-1;return {'n':len(y),'withheld':int(sum(~known)),'retained':int(sum(known)),'coverage':float(np.mean(known)),'retained_correct':int(sum(known&(pred==y))),'retained_accuracy':float(np.mean(pred[known]==y[known])),'false_premiums':int(sum(known&(pred==1)&~y)),'missed_premiums':int(sum(known&(pred==0)&y)),'true_premiums_withheld':int(sum(~known&y)),'nonpremiums_withheld':int(sum(~known&~y))}
def main():
 rows=json.loads((R/'benchmark-targets-v37.json').read_text())['rows'];ev=json.loads((R/'evidence-v37.json').read_text())['rows'];by={q['id']:i for i,q in enumerate(rows)};known=np.array([q['materiality_target'] is not None for q in rows]);truth=np.array([q['materiality_target'] not in (None,0) for q in rows]);direct=np.array([q.get('materiality_support')=='direct_two_axis_response' or q.get('explicit_materiality') is not None for q in ev]);b=V28();c=V37();scores={'v28':np.array([abs(b.compare(q['a'],q['b'])['margin']) for q in rows]),'v37':np.array([c.compare(q['a'],q['b'])['premium_decision_score']+1 for q in rows])};prior=json.loads((R/'premium-context-validation-v37.json').read_text());folds=[f for f in prior['fold_audits'] if f['arm']=='near_shade_heavy_secondary'];runs=[];audit=[]
 for seed in (11,29,47,71,103):
  pred={name:np.full(len(rows),-2,int) for name in scores}
  for f in [f for f in folds if f['seed']==seed]:
   tr=np.array([by[id] for id in f['training_ids'] if known[by[id]]]);te=np.array([by[id] for id in f['validation_ids']])
   for name,score in scores.items():
    lo,hi=choose(score[tr],truth[tr]);pred[name][te]=np.where(score[te]<lo,0,np.where(score[te]<hi,-1,1));audit.append({'seed':seed,'fold':f['fold'],'model':name,'band':[lo,hi],'training_ids':f['training_ids'],'validation_ids':f['validation_ids']})
  assert all(np.all(x!=-2) for x in pred.values())
  runs.append({'seed':seed,'models':{name:{'all':summarize_predictions(pr[known],truth[known]),'direct':summarize_predictions(pr[known&direct],truth[known&direct]),'predictions':pr.tolist()} for name,pr in pred.items()}})
 full={}
 for name,score in scores.items():
  lo,hi=choose(score[known],truth[known]);full[name]={'band':[lo,hi],'all':metrics(score[known],truth[known],lo,hi),'direct':metrics(score[known&direct],truth[known&direct],lo,hi),'withheld_ids':[q['id'] for q,s in zip(rows,score) if lo<=s<hi]}
 means={name:{section:{k:float(np.mean([r['models'][name][section][k] for r in runs])) for k in runs[0]['models'][name][section]} for section in ['all','direct']} for name in scores}
 out={'protocol':'No refitting ofV28orv37. Band chosen usingtraininglabels only in same25v37familyfolds. Maximize retainedsizeaccuracy subjectto<=15%trainingwithheld, tie-break fewerwithheldthenhigherbounds. Selectedband maywithholdmorethan15%invalidation. Scores:V28absrawgap;v37premium_decision_score+1, neverv37rawgap. Conditionalbandcalibration aroundalready-trained frozenmodels; not endtoend heldoutaccuracy. Peergrid retained,featuresearch paused.','source_hashes':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['model-config-v28.json','premium-config-v35.json','premium-config-v37.json','predictor_premium_v37.py','benchmark-targets-v37.json','premium-context-validation-v37.json','calibrate_reporting_v37.py']},'runs':runs,'fold_audits':audit,'full_calibration':full,'mean_conditional_validation':means,'band_counts':{name:dict(collections.Counter(str(f['band']) for f in audit if f['model']==name)) for name in scores}}
 (R/'reporting-calibration-v37.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'full':full,'mean':means,'bands':out['band_counts']},indent=2))
if __name__=='__main__':main()
