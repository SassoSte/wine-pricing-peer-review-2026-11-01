"""One contextual radius; all intrinsic offering values/directions remain frozen."""
from pathlib import Path
import json,hashlib
import numpy as np
import regional_mature_shade_v30 as model
import joint_objective_v22 as joint
import refit_simple_benchmark_v16 as metrics
R=Path(__file__).resolve().parent
SCALES=(.1,.2,.25,.3,.4,.5,.6,.75,1.)
def eligible(q):
 a,b=q['a'],q['b'];y,o=(a,b) if a[2]<b[2] else (b,a)
 if y[2]==30 and o[3]<=115 and a[1]==b[1]:return False
 return a[0]==b[0] and abs(a[2]-b[2])==5 and y[2]<=30 and y[3]-o[3]==5 and abs(model.DOMAIN['shades'].index(a[1])-model.DOMAIN['shades'].index(b[1]))<=1

def radii(rows,g,scale):
 # Lower the boundary only when the intrinsic model actually prefers the younger offering.
 return np.array([scale if eligible(q) and margin*np.sign(q['b'][2]-q['a'][2])>1e-7 else 1. for q,margin in zip(rows,g)])

def fit(rows,cfg):
 g=model.design(rows,'regional_mature_shade')@cfg['coefficients'];scores={s:joint.score(rows,g,radii(rows,g,s)) for s in SCALES}
 s=max(SCALES,key=lambda s:(round(scores[s]['balanced_accuracy'],12),round(scores[s]['both_axes_accuracy'],12),s))
 return s,scores[s]

def main():
 prior=json.loads((R/'regional-mature-shade-validation-v30.json').read_text());base=json.loads((R/'regional-interaction-validation-v30.json').read_text());t=json.loads((R/'benchmark-targets-v30.json').read_text())['rows'];e=json.loads((R/'evidence-v30.json').read_text())['rows'];ix={q['id']:i for i,q in enumerate(t)};by={q['id']:q for q in t};direct=metrics.verified_materiality(e);runs=[];audits=[]
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ('evidence-v30.json','benchmark-targets-v30.json','regional-mature-shade-validation-v30.json','regional-mature-shade-minnorm-config-v30.json','model-config-v28.json','predictor_v28.py','predictor_v27.py','vintage_tare_guarded_v30.py')}
 for old in prior['runs']['one_feature_minimum_norm']:
  rr=np.ones(len(t))
  for f in (f for f in prior['fold_audits'] if f['seed']==old['seed']):
   tr=[by[id] for id in f['training_ids']];te=[ix[id] for id in f['validation_ids']];s,score=fit(tr,f['polished_fit']);g=np.array(old['margins'])[te];rr[te]=radii([t[i] for i in te],g,s);audits.append({'seed':f['seed'],'fold':f['fold'],'training_ids':f['training_ids'],'validation_ids':f['validation_ids'],'scale':s,'training_score':score,'eligible_training_ids':[q['id'] for q in tr if eligible(q)]})
  g=np.array(old['margins']);runs.append({'seed':old['seed'],'margins':old['margins'],'radii':rr.tolist(),'score':metrics.score(t,g,rr,direct),'joint_score':joint.score(t,g,rr)})
 full=prior['polished_full_model'];s,score=fit(t,full);cfg=dict(full,model_id='v30_intrinsic_vintage_tare_threshold',vintage_tare_radius=s,threshold_scope={'same_provenance':True,'age_gap':5,'maximum_younger_age':30,'younger_heavier_by_lb':5,'maximum_shade_steps':1,'require_younger_predicted_higher':True,'guard_same_shade_younger30_older_tare_at_most115':True},status='experimental_pending_comparison',training_threshold_score=score)
 (R/'vintage-tare-guarded-config-v30.json').write_text(json.dumps(cfg,indent=2)+'\n')
 arms={'v28':base['runs']['v28'],'intrinsic_before':prior['runs']['one_feature_minimum_norm'],'vintage_tare_threshold':runs};js={k:{field:float(np.mean([q['joint_score'][field] for q in rs])) for field in ('both_axes_correct','both_axes_accuracy','balanced_accuracy','accuracy')} for k,rs in arms.items()}
 out={'protocol':'One scalar meaningfulness boundary. Sameprovenance,exact5year gap,younger<=30,younger5lbheavier,atmostone adjacent shade step,and youngerpredictedhigher. Guard: same-shade younger30/older35 witholdertare<=115 retainsnormalradius. Added after finding coarsened recorded non-premium revision-8; no label reinterpreted. Adaptive guard construction informed by current evidence,not independent validation. Threshold learned ontrainingrows only; heldout family partitions unchanged. Intrinsic25weights/margins/directions frozen to previousfoldfits. No new evidence or lookup predictions. Pure5lb and alltop comparisons ageequal are outside scope. Previouswide-WCA threshold is NOT used. Adaptive exploratory validation,not prospective.','source_hashes':hashes,'row_ids':[q['id'] for q in t],'scale_grid':SCALES,'full_scale':s,'fold_audits':audits,'runs':arms,'summary':metrics.summarize(arms),'joint_summary':js,'eligible_pairs':[{**q} for q in t if eligible(q)]}
 (R/'vintage-tare-guarded-validation-v30.json').write_text(json.dumps(out,indent=2)+'\n')
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 print(json.dumps({'scale':s,'joint':js,'summary':out['summary'],'scope_count':len(out['eligible_pairs'])},indent=2))
if __name__=='__main__':main()
