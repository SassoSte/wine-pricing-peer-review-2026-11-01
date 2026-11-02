"""Intrinsic offering utility: no pair-dependent features or answer lookup."""
from pathlib import Path
from itertools import product
import json,warnings
import numpy as np
from scipy import sparse
from scipy.optimize import milp,Bounds,LinearConstraint
from domestic_vintage_context_v27 import classification_constraints,ANCHORS
DOMAIN=json.loads(Path(__file__).with_name('model-config-v28.json').read_text())['domain']
REFINEMENTS=('regional_mature_shade',)
NEW_ANCHORS=('round53-2','round55-2','round55-9','round55-3','round55-4','round55-5','round55-6','round55-7')
NAMES=['domestic_top_vintage','foreign_young_pale','premium_tare_hinge','young_tare_interaction','all_top_completion']
def features(o,kind="control"):
 z,s,a,w=o;d=DOMAIN
 if z not in d['provenances'] or s not in d['shades'] or a not in d['vintage_years'] or w not in d['tare_lb']:raise ValueError(o)
 f=[float(z==v) for v in d['provenances'][1:]]+[float(d['shades'].index(s)>=i) for i in range(1,5)]+[float(d['vintage_years'].index(a)>=i) for i in range(1,5)]+[(130-w)/5]
 if s=='pale/straw' and w==130:f[12]=0
 base=np.r_[f,float(z in d['domestic'] and a==20),float(z not in d['domestic'] and s=='pale/straw' and a<=25 and w<130),max(0,(120-w)/5),float(a<=30)*(130-w)/5,float(z in ('Western Europe','northeast') and s=='pale/straw' and a==20 and w==110)]
 extra=[]
 if kind=='regional_mature_shade':
  extra.append(float(z=='South/Eastern Asia' and a==20))
  extra.append(float(s in ('golden','pale/straw') and a<=35))
 
 return np.r_[base,extra]
def design(rows,kind='control'):return np.array([features(q['a'],kind)-features(q['b'],kind) for q in rows])
def structural(kind='control'):
 def features(o):return globals()['features'](o,kind)
 rows=[];low=[];high=[]
 for z,s,a,w in product(DOMAIN['provenances'],DOMAIN['shades'],DOMAIN['vintage_years'],DOMAIN['tare_lb']):
  o=[z,s,a,w]
  if w<130:
   rows.append(features(o)-features([z,s,a,w+5]));low.append(0);high.append(np.inf if z in ('Western Europe','northeast') and s=='pale/straw' and a==20 and w==110 else .99999)
  if a>20:rows.append(features([z,s,a-5,w])-features(o));low.append(0);high.append(np.inf)
  j=DOMAIN['shades'].index(s)
  if j<4:rows.append(features([z,DOMAIN['shades'][j+1],a,w])-features(o));low.append(0);high.append(np.inf)
 table=np.unique(np.c_[np.array(rows),low,high],axis=0)
 return table[:,:-2],table[:,-2],table[:,-1]
def fit(rows,kind='control',time_limit=12.):
 x=design(rows,kind);ids,weights,cons=classification_constraints(rows,x);n=x.shape[1];k=len(ids);nv=2*n+k
 lo=np.r_[np.full(9,-8.),np.zeros(n-9),np.zeros(k+n)];hi=np.r_[np.full(n,8.),np.ones(k),np.full(n,8.)];lo[19]=-8.;lo[21]=-8.;lo[23]=-8.
 protected=[]
 for j,i in enumerate(ids):
  if rows[i]['id'] in (*ANCHORS,*NEW_ANCHORS):hi[n+j]=0;protected.append(rows[i]['id'])
 A=[];b=[];upper=[]
 for j,row,target in cons:
  minimum=np.maximum(row,0)@lo[:n]+np.minimum(row,0)@hi[:n];v=np.zeros(nv);v[:n]=row;v[n+j]=max(0,target-minimum);A.append(v);b.append(target);upper.append(np.inf)
 st,l,h=structural(kind)
 for row,lower,u in zip(st,l,h):v=np.zeros(nv);v[:n]=row;A.append(v);b.append(lower);upper.append(u)
 for j in range(n):
  for sign in (-1,1):v=np.zeros(nv);v[j]=sign;v[n+k+j]=1;A.append(v);b.append(0);upper.append(np.inf)
 matrix=sparse.csc_matrix(np.array(A));obj=np.r_[np.zeros(n),weights,np.full(n,1e-8)]
 with warnings.catch_warnings():
  warnings.filterwarnings('ignore',message='Unrecognized options detected')
  r=milp(obj,integrality=np.r_[np.zeros(n),np.ones(k),np.zeros(n)],bounds=Bounds(lo,hi),constraints=LinearConstraint(matrix,b,upper),options={'time_limit':time_limit,'mip_rel_gap':.001,'threads':1})
 if r.x is None:raise RuntimeError(r.message)
 assert np.min(matrix@r.x-np.array(b))>=-1e-6
 assert np.min(np.array(upper)-matrix@r.x)>=-1e-6
 return {'kind':kind,'coefficients':r.x[:n].tolist(),'decision_radius':1.,'protected_training_ids':protected,'solver_status':int(r.status),'solver_message':r.message,'mip_gap':float(r.mip_gap),'objective':float(r.fun),'time_limit_seconds':time_limit,'domain':DOMAIN,'extra_feature_names':NAMES+['SEA_top_vintage_adjustment','light_shade_mature_vintage']}
def value(o,cfg):return float(features(o,cfg['kind'])@cfg['coefficients'])
def predict(a,b,cfg):
 va=value(a,cfg);vb=value(b,cfg);g=va-vb
 return {'value_a':va,'value_b':vb,'margin':g,'predicted_direction':'A' if g>1e-7 else 'B' if g<-1e-7 else None,'predicted_meaningfulness':'meaningful_difference' if abs(g)>1+1e-8 else 'no_meaningful_difference','exact_price_equality':None,'prediction_source':'model_only','units':'intrinsic utility score; not calibrated money'}
