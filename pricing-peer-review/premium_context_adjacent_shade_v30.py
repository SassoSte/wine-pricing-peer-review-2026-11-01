"""Two heads: contextual intrinsic utility and separately learned premium justification."""
from pathlib import Path
from functools import lru_cache
from itertools import product
import json
import numpy as np
from scipy import sparse
from scipy.optimize import minimize,Bounds,LinearConstraint,linprog
from scipy.special import expit
import osqp
import compare_models as grouping
import joint_objective_v22 as joint
from intrinsic_regional_v30 import ANCHORS,NEW_ANCHORS
DOMAIN=json.loads(Path(__file__).with_name('model-config-v28.json').read_text())['domain']
VALUE_NAMES=['age_to35','age_to30','age_to25','age_to20','tare_to125','tare_to120','tare_to115','tare_to110','vintage_tare_foundation']+['contextual_provenance:'+z for z in DOMAIN['provenances'][1:]]+['contextual_shade:'+s for s in DOMAIN['shades'][1:]]+['all_top_profile']
HEAD_NAMES=['intercept','absolute_value_gap','winner_vintage_contribution','winner_tare_contribution','winner_core_interaction','winner_provenance_contribution','winner_shade_contribution','opposing_contributions','all_top_profile_distinction','mean_vintage_quality','mean_tare_quality','ordinary_pure5lb','shade_distance','shared_vintage_context_adjacent_shade']
ALPHAS=(.001,.01,.1)
HEAD_RIDGE=.03
PROTECTED=(*ANCHORS,*NEW_ANCHORS)

def qualities(o):return (40-o[2])/20,(130-o[3])/20

def completion(o):return float(o[0] in ('Western Europe','northeast') and o[1]=='pale/straw' and o[2]==20 and o[3]==110)

def features(o):
 z,s,a,w=o;d=DOMAIN
 if z not in d['provenances'] or s not in d['shades'] or a not in d['vintage_years'] or w not in d['tare_lb']:raise ValueError(o)
 v,t=qualities(o);context=.5+.25*(v+t)
 f=[float(a<=k) for k in (35,30,25,20)]+[float(w<=k) for k in (125,120,115,110)]+[v*t]
 f += [float(z==k)*context for k in d['provenances'][1:]]
 f += [float(d['shades'].index(s)>=i)*context for i in range(1,5)]
 if s=='pale/straw' and w==130:f[21]=0.
 return np.r_[f,completion(o)]

def design(rows):return np.array([features(q['a'])-features(q['b']) for q in rows])

@lru_cache(None)
def structural():
 cons=[]
 for z,s,a,w in product(DOMAIN['provenances'],DOMAIN['shades'],DOMAIN['vintage_years'],DOMAIN['tare_lb']):
  o=[z,s,a,w];f=features(o)
  if a>20:cons.append(features([z,s,a-5,w])-f)
  if w>110:cons.append(features([z,s,a,w-5])-f)
  j=DOMAIN['shades'].index(s)
  if j<4:cons.append(features([z,DOMAIN['shades'][j+1],a,w])-f)
 # Core total range must cover the combined provenance/shade modifier range.
 # Architectural primary/secondary relation, not elicited monetary weights.
 for i,j in product(range(10),repeat=2):
  row=np.zeros(23);row[:9]=1.;row[18:22]=-1.
  if i:row[8+i]-=1.
  if j:row[8+j]+=1.
  cons.append(row)
 return np.unique(np.array(cons),axis=0)

def fit_value(rows,alpha):
 x=design(rows);direction=np.array([q['known_direction'] or 0 for q in rows]);idx=np.flatnonzero(direction);dx=direction[idx,None]*x[idx];n=23;k=len(idx)
 P=sparse.diags(np.r_[np.full(n,2*alpha),np.full(k,2/max(k,1))],format='csc');constraints=[];lower=[];upper=[]
 constraints.append(sparse.hstack([sparse.csc_matrix(dx),sparse.eye(k)],format='csc'));lower.extend(np.ones(k));upper.extend(np.full(k,np.inf))
 st=structural();constraints.append(sparse.hstack([sparse.csc_matrix(st),sparse.csc_matrix((len(st),k))],format='csc'));lower.extend(np.zeros(len(st)));upper.extend(np.full(len(st),np.inf))
 lo=np.zeros(n+k);lo[9:18]=-np.inf;constraints.append(sparse.eye(n+k,format='csc'));lower.extend(lo);upper.extend(np.full(n+k,np.inf))
 protected=[]
 for i in idx:
  if rows[i]['id'] in PROTECTED:
   row=np.r_[direction[i]*x[i],np.zeros(k)];constraints.append(sparse.csc_matrix(row[None,:]));lower.append(.01);upper.append(np.inf);protected.append(rows[i]['id'])
 A=sparse.vstack(constraints,format='csc');lower=np.array(lower);upper=np.array(upper)
 solver=osqp.OSQP();solver.setup(P=P,q=np.zeros(n+k),A=A,l=lower,u=upper,verbose=False,eps_abs=1e-7,eps_rel=1e-7,max_iter=100000,polishing=True);r=solver.solve()
 if r.info.status_val not in (1,2):raise RuntimeError('Value QP: '+r.info.status)
 if np.min(A@r.x-lower)<-2e-6:raise RuntimeError('Value constraint violation')
 return {'coefficients':r.x[:n].tolist(),'alpha':alpha,'solver_status':r.info.status,'protected_training_ids':protected,'feature_names':VALUE_NAMES}

def components(o,cfg):
 f=features(o)*np.array(cfg['coefficients']);return np.array([f[:4].sum(),f[4:8].sum(),f[8],f[9:18].sum(),f[18:22].sum(),f[22]])

def head_features(rows,value_cfg):
 hh=[];g=[]
 for q in rows:
  a,b=q['a'],q['b'];delta=components(a,value_cfg)-components(b,value_cfg);gap=float(delta.sum());sign=1 if gap>1e-7 else -1 if gap<-1e-7 else 0;va,ta=qualities(a);vb,tb=qualities(b);cd=abs(completion(a)-completion(b));pure5=a[:3]==b[:3] and abs(a[3]-b[3])==5 and cd==0
  opposition=max(0.,(abs(delta).sum()-abs(gap))/2)
  younger,older=(a,b) if a[2]<b[2] else (b,a)
  light_pair=a[1] in ('golden','pale/straw') and b[1] in ('golden','pale/straw')
  shade_ok=light_pair or (abs(DOMAIN['shades'].index(a[1])-DOMAIN['shades'].index(b[1]))<=1 if True else a[1]==b[1])
  old_bracket_counterweight=younger[2]==35 and younger[3]>older[3]
  older_nonlight=not light_pair and younger[2]>30
  low_tare_counterweight=not light_pair and younger[2]==30 and older[3]<=115 and younger[3]>older[3] and a[1]==b[1]
  isolated=shade_ok and not(old_bracket_counterweight or older_nonlight or low_tare_counterweight) and a[0]==b[0] and abs(a[2]-b[2])==5 and abs(a[3]-b[3])<=5 and gap*np.sign(b[2]-a[2])>1e-7
  hh.append([1.,abs(gap),*(sign*delta[:5]).tolist(),opposition,cd,(va+vb)/2,(ta+tb)/2,float(pure5),abs(DOMAIN['shades'].index(a[1])-DOMAIN['shades'].index(b[1]))/4,float(isolated)]);g.append(gap)
 return np.array(hh),np.array(g)

def fit_head(rows,oof_h,full_h,weighting="joint_groups"):
 m,d,_=joint.masks(rows);known=np.isfinite(m);y=(m[known]!=0).astype(float);h=oof_h[known];mean=h.mean(axis=0);std=h.std(axis=0);mean[0]=0.;std[0]=1.;std[std<1e-6]=1.;x=(h-mean)/std
 n=len(y);pos=max(1,sum(y));neg=max(1,n-sum(y));weights=np.where(y==1,.5/pos,.5/neg)
 if weighting=='joint_groups':
  groups=[y==1,(y==0)&(d[known]!=0),(y==0)&(d[known]==0)];active=sum(v.any() for v in groups);weights=np.zeros(n)
  for mask in groups:
   if mask.any():weights[mask]=1/(active*mask.sum())
 def objective(b):
  z=x@b;pen=b.copy();pen[0]=0
  return float(np.sum(weights*(np.logaddexp(0,z)-y*z))+.5*HEAD_RIDGE*(pen@pen)),x.T@(weights*(expit(z)-y))+HEAD_RIDGE*pen
 # Meaningfulness protection uses only known training rows under the fitted training utility.
 C=[];ids=[]
 for i,q in enumerate(rows):
  if q['id'] in PROTECTED and np.isfinite(m[i]):
   C.append((1 if m[i]!=0 else -1)*(full_h[i]-mean)/std);ids.append(q['id'])
 constraints=[]
 if C:constraints=[LinearConstraint(np.array(C),np.full(len(C),.02),np.full(len(C),np.inf))]
 lo=np.full(x.shape[1],-np.inf);hi=np.full(x.shape[1],np.inf);lo[1]=0.;lo[8]=0.;lo[13]=0.;hi[11]=0.
 r=minimize(objective,np.zeros(x.shape[1]),jac=True,method='SLSQP',bounds=Bounds(lo,hi),constraints=constraints,options={'ftol':1e-10,'maxiter':1500})
 if not r.success:raise RuntimeError('Premium head: '+r.message)
 if C and np.min(np.array(C)@r.x)<.02-1e-6:raise RuntimeError('Premium head control violation')
 return {'coefficients':r.x.tolist(),'mean':mean.tolist(),'scale':std.tolist(),'feature_names':HEAD_NAMES,'ridge':HEAD_RIDGE,'weighting':weighting,'protected_training_ids':ids,'solver_message':r.message,'cutoff':.5}

def fit(rows,seed):
 groups=np.array([repr((tuple(sorted((q['a'][0],q['b'][0]))),tuple(sorted((q['a'][1],q['b'][1]))))) for q in rows]);parts=list(grouping.folds(groups,3,seed));d=np.array([q['known_direction'] or 0 for q in rows]);known=d!=0;choices={};inner=[]
 for alpha in ALPHAS:
  h=np.zeros((len(rows),len(HEAD_NAMES)));g=np.zeros(len(rows));folds=[]
  for fold,(tr,te) in enumerate(parts):
   train=[rows[i] for i in tr];test=[rows[i] for i in te];c=fit_value(train,alpha);hh,gg=head_features(test,c);h[te]=hh;g[te]=gg;folds.append({'fold':fold,'training_ids':[q['id'] for q in train],'validation_ids':[q['id'] for q in test],'fit':c})
  signs=np.where(g>1e-7,1,np.where(g<-1e-7,-1,0));choices[alpha]={'correct_direction':int(sum(signs[known]==d[known])),'h':h,'g':g,'folds':folds}
 alpha=max(ALPHAS,key=lambda a:(choices[a]['correct_direction'],a));selected=choices[alpha];value=fit_value(rows,alpha);full_h,full_g=head_features(rows,value);premium=fit_head(rows,selected['h'],full_h,'joint_groups');balanced=fit_head(rows,selected['h'],full_h,'balanced_size')
 # Ablation: same value model with a single gap boundary, selected using train-only OOF margins.
 material,_,_=joint.masks(rows);known_size=np.isfinite(material);values=abs(selected['g'][known_size]);radii=sorted(set([.01,.1,.25,.5,1.,*np.quantile(values,np.linspace(0,1,31)).tolist()]));radius=max(radii,key=lambda rad:(joint.score(rows,selected['g'],max(rad,1e-6))['balanced_accuracy'],rad))
 return {'schema_version':1,'model_id':'foundation_contextual_amplifiers_two_head_v30','domain':DOMAIN,'value_model':value,'premium_model':premium,'premium_models':{'joint_groups':premium,'balanced_size':balanced},'ablation_radius':max(radius,1e-6),'inner_selection':{'chosen_alpha':alpha,'direction_counts':{str(a):v['correct_direction'] for a,v in choices.items()},'partitions':selected['folds']},'semantic_qualification':'Premium score estimates supplied justification labels, not market scarcity,consumer-choice probability or monetary price. No pair labels queried at inference.'}

def predict_many(rows,cfg,head="joint_groups"):
 h,g=head_features(rows,cfg['value_model']);p=cfg['premium_models'][head];prob=expit(((h-np.array(p['mean']))/np.array(p['scale']))@p['coefficients']);sign=np.where(g>1e-7,1,np.where(g<-1e-7,-1,0));large=(prob>.5)&(sign!=0)
 return g,sign,large,prob

def score_outputs(rows,g,large,direct):
 m,d,groups=joint.masks(rows);sign=np.where(g>1e-7,1,np.where(g<-1e-7,-1,0));kd=d!=0;known=np.isfinite(m);positive=known&(m!=0);negative=m==0
 def size_score(mask):
  pos=positive&mask;neg=negative&mask;all_=pos|neg;recalls=[]
  if pos.any():recalls.append(float(large[pos].mean()))
  if neg.any():recalls.append(float((~large[neg]).mean()))
  return {'n':int(all_.sum()),'meaningful_n':int(pos.sum()),'no_meaningful_n':int(neg.sum()),'accuracy':float((large[all_]==positive[all_]).mean()),'balanced_accuracy':float(np.mean(recalls)),'false_meaningful':int((large&neg).sum()),'missed_meaningful':int((~large&pos).sum()),'correct_meaningful_direction':int((large&pos&(sign==d)).sum())}
 score={'direction':{'n':int(kd.sum()),'correct':int((kd&(sign==d)).sum()),'accuracy':float((sign[kd]==d[kd]).mean()),'reversals':int((kd&(sign==-d)).sum()),'zero_or_abstain':int((kd&(sign==0)).sum())},'materiality':size_score(np.ones(len(rows),bool)),'directly_supported_materiality':size_score(np.array(direct,bool)),'unknown_materiality_n':int((~known).sum())}
 c=np.ones(len(rows),bool)
 for name,mask in groups.items():
  c[mask]=(large[mask]&(sign[mask]==d[mask])) if name=='meaningful' else ((~large[mask])&(sign[mask]==d[mask])) if name=='practical_direction' else (~large[mask]) if name=='practical_only' else (sign[mask]==d[mask])
 supported=np.logical_or.reduce(list(groups.values()));both=known&kd
 js={'supported_n':int(supported.sum()),'correct':int(c[supported].sum()),'accuracy':float(c[supported].mean()),'both_axes_n':int(both.sum()),'both_axes_correct':int(c[both].sum()),'both_axes_accuracy':float(c[both].mean()),'balanced_accuracy':float(np.mean([c[v].mean() for v in groups.values() if v.any()])),'by_group':{k:{'n':int(v.sum()),'correct':int(c[v].sum())} for k,v in groups.items()}}
 return score,js
