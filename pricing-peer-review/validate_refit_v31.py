from pathlib import Path
import json,hashlib
import numpy as np
from scipy.special import expit
import refit_exact_context_v31 as ranking
import premium_context_adjacent_shade_v30 as legacy
from premium_refit_v31 import fit_head
import refit_simple_benchmark_v16 as metrics
import joint_objective_v22 as joint
R=Path(__file__).resolve().parent
EPS=1e-7

def new_components(o,cfg):
 f=ranking.features(o)*np.array(cfg['coefficients']);return np.array([f[:4].sum(),f[4:8].sum(),f[8],f[9:18].sum()+f[23:].sum(),f[18:22].sum(),f[22]])

def new_head_features(rows,cfg):
 hh=[];gg=[]
 for q in rows:
  a,b=q['a'],q['b'];delta=new_components(a,cfg)-new_components(b,cfg);g=float(delta.sum());sign=1 if g>EPS else -1 if g<-EPS else 0;va,ta=legacy.qualities(a);vb,tb=legacy.qualities(b);cd=abs(legacy.completion(a)-legacy.completion(b));pure5=a[:3]==b[:3] and abs(a[3]-b[3])==5 and cd==0;opposition=max(0,(abs(delta).sum()-abs(g))/2);y,o=(a,b) if a[2]<b[2] else(b,a);light=a[1] in ('golden','pale/straw') and b[1] in ('golden','pale/straw');shadeok=light or abs(legacy.DOMAIN['shades'].index(a[1])-legacy.DOMAIN['shades'].index(b[1]))<=1;guard=(y[2]==35 and y[3]>o[3]) or (not light and y[2]>30) or (not light and y[2]==30 and o[3]<=115 and y[3]>o[3] and a[1]==b[1]);isolated=shadeok and not guard and a[0]==b[0] and abs(a[2]-b[2])==5 and abs(a[3]-b[3])<=5 and g*np.sign(b[2]-a[2])>EPS
  hh.append([1.,abs(g),*(sign*delta[:5]).tolist(),opposition,cd,(va+vb)/2,(ta+tb)/2,float(pure5),abs(legacy.DOMAIN['shades'].index(a[1])-legacy.DOMAIN['shades'].index(b[1]))/4,float(isolated)]);gg.append(g)
 return np.array(hh),np.array(gg)

def fit_candidate(rows,seed,reference):
 value=ranking.fit(rows,seed);ix={q['id']:i for i,q in enumerate(rows)};newh=np.zeros((len(rows),len(legacy.HEAD_NAMES)));oldh=np.zeros_like(newh)
 for f in value['inner_selection']['partitions']:
  te=[ix[id] for id in f['validation_ids']];hh,_=new_head_features([rows[i] for i in te],f['fit']);newh[te]=hh
 for f in reference['inner_selection']['partitions']:
  te=[ix[id] for id in f['validation_ids']];hh,_=legacy.head_features([rows[i] for i in te],f['fit']);oldh[te]=hh
 fullnew,_=new_head_features(rows,value);fullold,_=legacy.head_features(rows,reference['value_model']);heads={'coupled':fit_head(rows,newh,fullnew,'balanced_size'),'legacy_reference':fit_head(rows,oldh,fullold,'balanced_size')}
 return {'ranking_model':value,'premium_heads':heads,'legacy_reference_value_model':reference['value_model'],'head_feature_names':legacy.HEAD_NAMES,'equality_tolerance':EPS}

def predict(rows,cfg,arm):
 g=ranking.design(rows)@cfg['ranking_model']['coefficients'];h,_=new_head_features(rows,cfg['ranking_model']) if arm=='coupled' else legacy.head_features(rows,cfg['legacy_reference_value_model']);head=cfg['premium_heads'][arm];p=expit(((h-np.array(head['mean']))/np.array(head['scale']))@head['coefficients']);large=(p>.5)&(abs(g)>EPS);return g,large,p

def relation_score(rows,g,large,direct):
 separate,oldjoint=legacy.score_outputs(rows,g,large,direct);m,d,groups=joint.masks(rows);sg=np.where(g>EPS,1,np.where(g<-EPS,-1,0));exact=np.array([q.get('exact_price_equality') is True for q in rows]);relation_known=(d!=0)|exact;rel=np.where(exact,sg==0,sg==d);size=np.isfinite(m);both=relation_known&size;correct=(~relation_known|rel)&(~size|(large==(m!=0)));support=relation_known|size
 masks=[size&(m!=0),size&(m==0)&relation_known,size&(m==0)&~relation_known,~size&relation_known]
 aware={'supported_n':int(support.sum()),'correct':int(correct[support].sum()),'accuracy':float(correct[support].mean()),'both_relation_and_size_n':int(both.sum()),'both_relation_and_size_correct':int(correct[both].sum()),'both_relation_and_size_accuracy':float(correct[both].mean()),'balanced_joint_accuracy':float(np.mean([correct[v].mean() for v in masks if v.any()])),'exact_ties_n':int(exact.sum()),'exact_ties_correct':int((exact&(sg==0)&~large).sum()),'exact_tie_gaps':[{'id':q['id'],'gap':float(g[i]),'premium':bool(large[i])} for i,q in enumerate(rows) if exact[i]]}
 return separate,oldjoint,aware

def main():
 oldrank=json.loads((R/'regional-rank-frozen-premium-validation-v30.json').read_text());baseval=json.loads((R/'regional-rank-fix-validation-v30.json').read_text());reference=json.loads((R/'foundation-amplifiers-validation-v30.json').read_text());t=json.loads((R/'benchmark-targets-v31.json').read_text())['rows'];e=json.loads((R/'evidence-v31.json').read_text())['rows'];by={q['id']:q for q in t};ix={q['id']:i for i,q in enumerate(t)};direct=np.array(metrics.verified_materiality(e));runs={k:[] for k in ('v28','frozen_v30_candidate','v31_coupled','v31_legacy_reference')};audit=[];cache=R/'v31-refit-zero-shade-cache';cache.mkdir(exist_ok=True)
 sources=['evidence-v30.json','benchmark-targets-v30.json','evidence-v31.json','benchmark-targets-v31.json','round57-consistent-misses-review.json','refit_exact_context_v31.py','premium_refit_v31.py','validate_refit_v31.py','model-config-v28.json','predictor_v28.py','predictor_v27.py','rank-soft-order-frozen-premium-config-v30.json'];hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources}
 for seed in metrics.SEEDS:
  data={k:{'g':np.zeros(len(t)),'b':np.zeros(len(t),bool),'p':None} for k in runs}
  for name,series in [('v28',baseval['runs']['v28']),('frozen_v30_candidate',oldrank['runs']['soft_domestic_order_frozen_premium'])]:
   q=next(q for q in series if q['seed']==seed);data[name]={'g':np.array(q['margins']),'b':np.array(q['predicted_meaningful'],bool),'p':q['premium_scores']}
  for f in (f for f in reference['fold_audits'] if f['seed']==seed):
   p=cache/f"{seed}-{f['fold']}.json";tr=[by[id] for id in f['training_ids']];te=[ix[id] for id in f['validation_ids']]
   if p.exists():item=json.loads(p.read_text());assert item['source_hashes']==hashes
   else:
    cfg=fit_candidate(tr,seed*100+f['fold'],f['fit']);item={'source_hashes':hashes,'seed':seed,'fold':f['fold'],'training_ids':f['training_ids'],'validation_ids':f['validation_ids'],'fit':cfg};p.write_text(json.dumps(item,indent=2)+'\n')
   audit.append(item)
   for arm in ('coupled','legacy_reference'):
    g,b,prob=predict([t[i] for i in te],item['fit'],arm);name='v31_'+arm;data[name]['g'][te]=g;data[name]['b'][te]=b
    if data[name]['p'] is None:data[name]['p']=np.zeros(len(t))
    data[name]['p'][te]=prob
  for name,v in data.items():
   s,j,eq=relation_score(t,v['g'],v['b'],direct);runs[name].append({'seed':seed,'margins':v['g'].tolist(),'predicted_meaningful':v['b'].tolist(),'premium_scores':np.asarray(v['p']).tolist() if v['p'] is not None else None,'score':s,'legacy_joint_score':j,'relation_score':eq})
  print('Completed',seed,[(k,runs[k][-1]['relation_score']['both_relation_and_size_correct'],runs[k][-1]['relation_score']['exact_ties_correct']) for k in runs],flush=True)
 full=fit_candidate(t,30001,reference['full_model']);(R/'v31-refit-full-config.json').write_text(json.dumps(full,indent=2)+'\n');summary={k:{f:float(np.mean([q['relation_score'][f] for q in rs])) for f in ('both_relation_and_size_correct','both_relation_and_size_accuracy','balanced_joint_accuracy','exact_ties_correct')} for k,rs in runs.items()}
 out={'protocol':'Same25familypartitions and640pairs; correctedv31 targets. Baselines frozen andrescored onv31. Explicitexactties are hardvalueequalities in trainingonly,never a practical-size band. Current23valuebasis cannot represent age-specific regional equality plusstrictyounger differences; one sharedmaturity/darkness interaction expanded across9regioncoefficients adds conditionalconvergence,32valuecoefficients total. Softdomesticprior andmonotonicity retained. Latestreviewedstrictdirections andheadjudgments protected onlywhen in training. Comparecoupledrefittedpremium encoder vsfrozenv30referenceencoder withrefittedhead. Bothheads trainedonly onknownsize labels; allheadinputs innerOOF. Mainjointscore includes3exacttie relations; legacystrict-direction metric retained separately. Reusedexploratoryvalidation,notnewprospectiveaccuracy.','source_hashes':hashes,'row_ids':[q['id'] for q in t],'runs':runs,'relation_summary':summary,'separate_summary':metrics.summarize(runs),'fold_audits':audit,'full_model':full}
 (R/'v31-refit-validation.json').write_text(json.dumps(out,indent=2)+'\n')
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
