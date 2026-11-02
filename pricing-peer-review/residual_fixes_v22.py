"""Two small residual adjustments over frozen v21."""
from itertools import product
import numpy as np
import shade_vintage_shared_v21 as previous
import refit_simple_benchmark_v16 as metrics

def components(rows,cfg):
 parts=previous.components(rows,cfg);g=previous.gaps(parts,cfg['shade_parameters'])[0];r=parts[1];h=[]
 for q in rows:
  a,b=q['a'],q['b'];young=float(a[2]==20)-float(b[2]==20)
  h.append(young*max(0.,cfg['underlying_coefficients'][16]))
 _,_,shade,tare,_,foreign=parts
 mature=np.array([min(q['a'][2],q['b'][2])>=30 for q in rows]);low=shade*(tare<=115)*foreign*mature
 return g,r,np.column_stack([h,low])

def fit(rows,evidence,cfg,arm):
 grid=np.linspace(0,1,21);params=np.array(list(product(grid if arm in ('vintage','combined') else [0.],grid if arm in ('shade','combined') else [0.])))
 g,r,h=components(rows,cfg);gg=g[None,:]+params@h.T;_,m,d,_=previous.utility.arrays(rows);known=d!=0;pos=np.isfinite(m)&(m!=0);neg=m==0;large=abs(gg)>r;direct=np.array(metrics.verified_materiality(evidence))&np.isfinite(m)
 pred=np.where(gg>1e-7,1,np.where(gg<-1e-7,-1,0));da=(pred[:,known]==d[known]).mean(axis=1);ba=(large[:,pos].mean(axis=1)+(~large[:,neg]).mean(axis=1))/2;obj=(da+ba)/2;directacc=(large[:,direct]==(m[direct]!=0)).mean(axis=1);fp=large[:,neg].sum(axis=1)
 i=max(range(len(params)),key=lambda i:(round(obj[i],12),round(directacc[i],12),-int(fp[i]),-float(params[i].sum()),-float(params[i,1])))
 return {'residual_parameters':params[i].tolist(),'training_objective':float(obj[i])}

def predict(a,b,cfg):
 g,r,h=components([{'a':a,'b':b}],cfg);gap=float((g+h@cfg.get('residual_parameters',[0.,0.]))[0]);cut=float(r[0])
 return {'predicted_direction':'A' if gap>1e-7 else 'B' if gap<-1e-7 else None,'predicted_meaningfulness':'meaningful_difference' if abs(gap)>cut else 'no_meaningful_difference','margin':gap,'decision_radius':cut,'exact_price_equality':None,'prediction_source':'model_only','units':'pair-comparison score, not a standalone price'}
