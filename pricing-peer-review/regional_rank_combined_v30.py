"""No-new-feature ranking regularizers over the existing foundation model."""
import numpy as np
from scipy import sparse
import osqp
import premium_context_adjacent_shade_v30 as base
KINDS=('combined',)
ORDER=(('northeast','southwest'),('northeast','southeast'),('southwest','central'),('southeast','central'),('central','northwest'))

def penalty_matrix(kind):
 if kind not in ('centered_regions','combined'):return np.eye(23)
 # Canonical centered region effects; mean shift is absorbed into the core increments.
 T=np.zeros((24,23));T[:9,:9]=np.eye(9);T[:8,9:18]+=1/160
 for z in range(10):
  T[9+z,9:18]-=.1
  if z:T[9+z,8+z]+=1
 T[19:23,18:22]=np.eye(4);T[23,22]=1
 return T.T@T

def fit_value(rows,alpha,kind):
 x=base.design(rows);d=np.array([q['known_direction'] or 0 for q in rows]);idx=np.flatnonzero(d);dx=d[idx,None]*x[idx];n=23;k=len(idx);h=len(ORDER) if kind in ('soft_domestic_order','combined') else 0;nv=n+k+h
 P=sparse.block_diag((sparse.csc_matrix(2*alpha*penalty_matrix(kind)),sparse.eye(k)*2/max(1,k),sparse.eye(h)*8*alpha),format='csc');A=[];lo=[];hi=[]
 A.append(sparse.hstack([sparse.csc_matrix(dx),sparse.eye(k),sparse.csc_matrix((k,h))],format='csc'));lo.extend(np.ones(k));hi.extend(np.full(k,np.inf))
 st=base.structural();A.append(sparse.hstack([sparse.csc_matrix(st),sparse.csc_matrix((len(st),k+h))],format='csc'));lo.extend(np.zeros(len(st)));hi.extend(np.full(len(st),np.inf))
 lower=np.zeros(nv);lower[9:18]=-np.inf;A.append(sparse.eye(nv,format='csc'));lo.extend(lower);hi.extend(np.full(nv,np.inf))
 protected=[]
 for i in idx:
  if rows[i]['id'] in base.PROTECTED:
   v=np.r_[d[i]*x[i],np.zeros(k+h)];A.append(sparse.csc_matrix(v[None,:]));lo.append(.01);hi.append(np.inf);protected.append(rows[i]['id'])
 if h:
  for j,(higher,lower) in enumerate(ORDER):
   v=np.zeros(nv);v[8+base.DOMAIN['provenances'].index(higher)]=1;v[8+base.DOMAIN['provenances'].index(lower)]=-1;v[n+k+j]=1;A.append(sparse.csc_matrix(v[None,:]));lo.append(0);hi.append(np.inf)
 mat=sparse.vstack(A,format='csc');lo=np.array(lo);hi=np.array(hi);solver=osqp.OSQP();solver.setup(P=P,q=np.zeros(nv),A=mat,l=lo,u=hi,verbose=False,eps_abs=1e-7,eps_rel=1e-7,max_iter=200000,polishing=True);result=solver.solve()
 if result.info.status_val not in (1,2):raise RuntimeError(result.info.status)
 if np.min(mat@result.x-lo)<-3e-6:raise RuntimeError('Constraint violation')
 return {'coefficients':result.x[:n].tolist(),'alpha':alpha,'regularizer':kind,'solver_status':result.info.status,'protected_training_ids':protected,'feature_names':base.VALUE_NAMES,'soft_order_slacks':result.x[n+k:].tolist(),'regularizer_qualification':'Centered ridge changes only penalty coordinates,not the original parameterization or structural constraints.' if kind=='centered_regions' else 'Soft domestic order from user guidance; strength4xexistingridge,zero requested pricegap,violations allowed. Engineering test strength,not elicited price weights.'}

def fit(rows,seed,kind):
 groups=np.array([repr((tuple(sorted((q['a'][0],q['b'][0]))),tuple(sorted((q['a'][1],q['b'][1]))))) for q in rows]);parts=list(base.grouping.folds(groups,3,seed));d=np.array([q['known_direction'] or 0 for q in rows]);known=d!=0;choices={}
 for alpha in base.ALPHAS:
  hh=np.zeros((len(rows),len(base.HEAD_NAMES)));g=np.zeros(len(rows));audits=[]
  for fold,(tr,te) in enumerate(parts):
   train=[rows[i] for i in tr];test=[rows[i] for i in te];c=fit_value(train,alpha,kind);h,gg=base.head_features(test,c);hh[te]=h;g[te]=gg;audits.append({'fold':fold,'training_ids':[q['id'] for q in train],'validation_ids':[q['id'] for q in test],'fit':c})
  sg=np.where(g>1e-7,1,np.where(g<-1e-7,-1,0));choices[alpha]={'correct':int((sg[known]==d[known]).sum()),'h':hh,'folds':audits}
 alpha=max(base.ALPHAS,key=lambda a:(choices[a]['correct'],a));chosen=choices[alpha];value=fit_value(rows,alpha,kind);full_h,_=base.head_features(rows,value);head=base.fit_head(rows,chosen['h'],full_h,'balanced_size')
 return {'model_id':'shared_context_'+kind+'_v30','domain':base.DOMAIN,'value_model':value,'premium_model':head,'premium_models':{'balanced_size':head},'inner_selection':{'chosen_alpha':alpha,'direction_counts':{str(a):v['correct'] for a,v in choices.items()},'partitions':chosen['folds']},'head_qualification':'Existing adjacent-shade shared-context architecture/ridge/loss/cutoff unchanged; coefficients refit on training-only OOF inputs to match changed value scale.'}
