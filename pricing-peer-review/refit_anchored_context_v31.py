"""Intrinsic value refit with explicit equality and mature/shade-dependent regional convergence."""
from pathlib import Path
from functools import lru_cache
from itertools import product
import json,numpy as np
from scipy import sparse
import osqp
import premium_context_adjacent_shade_v30 as base
from regional_rank_regularization_v30 import ORDER
N=32

def weakness(o):
 shade_index=3 if o[1]=='pale/straw' and o[3]==130 else base.DOMAIN['shades'].index(o[1])
 return min((o[2]-20)/15,1.)*(4-shade_index)/4

def features(o):
 old=base.features(o);v,t=base.qualities(o);c=.5+.25*(v+t);return np.r_[old,[float(o[0]==z)*c*weakness(o) for z in base.DOMAIN['provenances'][1:]]]
def design(rows):return np.array([features(q['a'])-features(q['b']) for q in rows])
@lru_cache(None)
def structural():
 out=[]
 for z,s,a,w in product(base.DOMAIN['provenances'],base.DOMAIN['shades'],base.DOMAIN['vintage_years'],base.DOMAIN['tare_lb']):
  o=[z,s,a,w];f=features(o)
  if a>20:out.append(features([z,s,a-5,w])-f)
  if w>110:out.append(features([z,s,a,w-5])-f)
  j=base.DOMAIN['shades'].index(s)
  if j<4:out.append(features([z,base.DOMAIN['shades'][j+1],a,w])-f)
 for i,j,u,v in product(range(10),range(10),(0.,1.),(0.,1.)):
  row=np.zeros(N);row[:9]=1;row[18:22]=-1
  if i:row[8+i]-=1;row[22+i]-=u
  if j:row[8+j]+=1;row[22+j]+=v
  out.append(row)
 return np.unique(np.array(out),axis=0)

def fit_value(rows,alpha,reference):
 x=design(rows);d=np.array([q['known_direction'] or 0 for q in rows]);idx=np.flatnonzero(d);k=len(idx);n=N;h=len(ORDER);nv=n+k+h
 P=sparse.diags(np.r_[np.full(n,2*alpha),np.full(k,2/max(k,1)),np.full(h,8*alpha)],format='csc');A=[];lo=[];hi=[];A.append(sparse.hstack([sparse.csc_matrix(d[idx,None]*x[idx]),sparse.eye(k),sparse.csc_matrix((k,h))],format='csc'));lo.extend(np.ones(k));hi.extend(np.full(k,np.inf))
 st=structural();A.append(sparse.hstack([sparse.csc_matrix(st),sparse.csc_matrix((len(st),k+h))],format='csc'));lo.extend(np.zeros(len(st)));hi.extend(np.full(len(st),np.inf));lower=np.zeros(nv);lower[9:18]=-np.inf;lower[23:32]=-np.inf;A.append(sparse.eye(nv,format='csc'));lo.extend(lower);hi.extend(np.full(nv,np.inf));protected=[];ties=[]
 for i,q in enumerate(rows):
  if q.get('exact_price_equality') is True:
   A.append(sparse.csc_matrix(np.r_[x[i],np.zeros(k+h)][None,:]));lo.append(0.);hi.append(0.);ties.append(q['id'])
  elif d[i] and (q['id'] in base.PROTECTED or q.get('latest_source_id','').startswith('round57-')):
   A.append(sparse.csc_matrix(np.r_[d[i]*x[i],np.zeros(k+h)][None,:]));lo.append(.01);hi.append(np.inf);protected.append(q['id'])
 for j,(higher,lower_zone) in enumerate(ORDER):
  row=np.zeros(nv);row[8+base.DOMAIN['provenances'].index(higher)]=1;row[8+base.DOMAIN['provenances'].index(lower_zone)]=-1;row[n+k+j]=1;A.append(sparse.csc_matrix(row[None,:]));lo.append(0.);hi.append(np.inf)
 mat=sparse.vstack(A,format='csc');lo=np.array(lo);hi=np.array(hi);linear=np.zeros(nv);linear[:n]=-2*alpha*np.r_[reference['coefficients'],np.zeros(9)];s=osqp.OSQP();s.setup(P=P,q=linear,A=mat,l=lo,u=hi,verbose=False,eps_abs=1e-9,eps_rel=1e-9,max_iter=300000,polishing=True);r=s.solve()
 if r.info.status_val not in (1,2):raise RuntimeError('Value QP: '+r.info.status)
 if np.min(mat@r.x-lo)<-1e-7 or np.min(hi-mat@r.x)<-1e-7:raise RuntimeError('Constraint violation')
 for q in rows:
  if q['id'] in ties:assert abs((features(q['a'])-features(q['b']))@r.x[:n])<1e-7
 return {'coefficients':r.x[:n].tolist(),'alpha':alpha,'solver_status':r.info.status,'protected_training_ids':protected,'exact_equality_training_ids':ties,'feature_names':base.VALUE_NAMES+['mature_dark_provenance:'+z for z in base.DOMAIN['provenances'][1:]],'soft_order_slacks':r.x[n+k:].tolist(),'equality_tolerance':1e-7,'regularizer':'minimum_change_from_matching_v30_training_fit'}

def fit(rows,seed,reference):
 groups=np.array([repr((tuple(sorted((q['a'][0],q['b'][0]))),tuple(sorted((q['a'][1],q['b'][1]))))) for q in rows]);d=np.array([q['known_direction'] or 0 for q in rows]);ex=np.array([q.get('exact_price_equality') is True for q in rows]);known=(d!=0)|ex;choices={}
 oldfolds=reference['inner_selection']['partitions']
 for alpha in base.ALPHAS:
  g=np.zeros(len(rows));audit=[]
  for fold,(tr,te) in enumerate(base.grouping.folds(groups,3,seed)):
   train=[rows[i] for i in tr];test=[rows[i] for i in te];old=oldfolds[fold];assert [q['id'] for q in train]==old['training_ids'];assert [q['id'] for q in test]==old['validation_ids'];c=fit_value(train,alpha,old['fit']);g[te]=design(test)@c['coefficients'];audit.append({'fold':fold,'training_ids':[q['id'] for q in train],'validation_ids':[q['id'] for q in test],'fit':c})
  sg=np.where(g>1e-7,1,np.where(g<-1e-7,-1,0));correct=np.where(ex,sg==0,sg==d);choices[alpha]={'correct':int(correct[known].sum()),'folds':audit}
 alpha=max(base.ALPHAS,key=lambda a:(choices[a]['correct'],a));c=fit_value(rows,alpha,reference['value_model']);c['inner_selection']={'chosen_alpha':alpha,'relation_correct':{str(a):v['correct'] for a,v in choices.items()},'partitions':choices[alpha]['folds']};return c
