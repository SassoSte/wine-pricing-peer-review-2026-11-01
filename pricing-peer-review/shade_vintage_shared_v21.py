"""Shared comparison-context shade premium; pure tare effects unchanged."""
from itertools import product
import numpy as np
import contextual_shade_v20 as v20
import contextual_fixes_v19 as previous
import domestic_shade_model as utility
import refit_simple_benchmark_v16 as metrics

def components(rows,cfg):
 g,_,r,f=previous.components(rows,cfg['underlying_coefficients'],cfg['base_radius'],cfg['context_kind'],cfg['context_coefficient']);r=r+cfg['boundary_increment']*f
 h=[];tare=[];young=[];foreign=[]
 beta=cfg['underlying_coefficients']
 for q in rows:
  a,b=q['a'],q['b'];contrast={a[1],b[1]}=={'golden','pale/straw'}
  pale=a if a[1]=='pale/straw' else b
  inc=beta[12]+(beta[18] if pale[0] in utility.DOMESTIC else 0)
  h.append((1 if b[1]=='pale/straw' else -1)*inc if contrast else 0.)
  tare.append(min(a[3],b[3]));young.append(min(a[2],b[2])==20);foreign.append(pale[0] not in utility.DOMESTIC)
 return g,r,np.array(h),np.array(tare),np.array(young),np.array(foreign)

def gaps(parts,params):
 g,r,h,tare,young,foreign=parts;p=np.atleast_2d(params)
 # One shared comparison context: not separate shade penalties per vessel's tare.
 shrink=np.where(tare[None,:]>=125,p[:,1,None],np.where(tare[None,:]>=120,p[:,0,None],0.))
 shrink=shrink+(1-shrink)*p[:,2,None]*young[None,:]
 shrink=np.where(foreign[None,:],shrink,0.)
 shrink=np.where(tare[None,:]>=130,1.,shrink)
 return g[None,:]+h[None,:]*shrink

def fit(rows,evidence,cfg,arm):
 grid=np.linspace(0,1,21)
 if arm=='zero_only':params=np.array([[0.,0.,0.]])
 elif arm=='pooled':params=np.array([[s,s,y] for s,y in product(grid,grid)])
 else:params=np.array(list(product(np.linspace(0,1,11),repeat=3)))
 parts=components(rows,cfg);gg=gaps(parts,params);r=parts[1];_,m,d,_=utility.arrays(rows);known=d!=0;pos=np.isfinite(m)&(m!=0);neg=m==0;large=abs(gg)>r;direct=np.array(metrics.verified_materiality(evidence));finite=np.isfinite(m)
 pred=np.where(gg>1e-7,1,np.where(gg<-1e-7,-1,0));direction=(pred[:,known]==d[known]).mean(axis=1)
 balanced=(large[:,pos].mean(axis=1)+(~large[:,neg]).mean(axis=1))/2;obj=(direction+balanced)/2;valid=direct&finite;direct_acc=(large[:,valid]==(m[valid]!=0)).mean(axis=1);fp=large[:,neg].sum(axis=1)
 best=max(range(len(params)),key=lambda i:(round(obj[i],12),round(direct_acc[i],12),-int(fp[i]),-float(params[i].sum()),-float(params[i,2])))
 return {'shade_parameters':params[best].tolist(),'training_objective':float(obj[best]),'grid_size':len(params)}

def predict(a,b,cfg):
 if cfg.get('selected_arm')=='v20':return v20.predict(a,b,cfg)
 parts=components([{'a':a,'b':b}],cfg);gap=float(gaps(parts,cfg['shade_parameters'])[0,0]);cut=float(parts[1][0])
 return {'predicted_direction':'A' if gap>1e-7 else 'B' if gap<-1e-7 else None,'predicted_meaningfulness':'meaningful_difference' if abs(gap)>cut else 'no_meaningful_difference','margin':gap,'decision_radius':cut,'exact_price_equality':None,'prediction_source':'model_only','units':'pair-comparison score, not a standalone price'}
