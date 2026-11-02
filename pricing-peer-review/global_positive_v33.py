"""Global learned curves with normalized attribute-range ordering; experimental only."""
from pathlib import Path
import json,hashlib,numpy as np
from scipy import sparse
import osqp
import compare_models as grouping
R=Path(__file__).resolve().parent
D=json.loads((R/'model-config-v28.json').read_text())['domain']
def features(o):
 z,s,a,w=o
 f=[float(z==p) for p in D['provenances'][1:]]+[float(D['shades'].index(s)>=i) for i in range(1,5)]+[float(a<=i) for i in (35,30,25,20)]+[float(w<=i) for i in (125,120,115,110)]
 if s=='pale/straw' and w==130:f[12]=0
 return np.array(f)
def design(rows):return np.array([features(q['a'])-features(q['b']) for q in rows])
def fit(rows,alpha,ordered):
 x=design(rows);d=np.array([q['known_direction'] or 0 for q in rows]);known=d!=0;xx=d[known,None]*x[known];n=21;k=int(known.sum());eq=np.array([q.get('exact_price_equality') is True for q in rows]);P0=2*alpha*np.eye(n)+2/max(1,k+eq.sum())*(x[eq].T@x[eq]);P=sparse.block_diag((sparse.csc_matrix(P0),sparse.eye(k)*2/max(1,k+eq.sum())),format='csc');A=[sparse.hstack([sparse.csc_matrix(xx),sparse.eye(k)],format='csc'),sparse.eye(n+k,format='csc')];lo=[*np.ones(k),*np.r_[np.full(9,-np.inf),np.zeros(n-9+k)]];hi=list(np.full(k+n+k,np.inf));extremes=None
 if ordered:
  pilot=fit(rows,alpha,False);ps=np.r_[0,pilot['coefficients'][:9]];top=int(ps.argmax());bottom=int(ps.argmin());extremes={'top':D['provenances'][top],'bottom':D['provenances'][bottom]}
  def zvec(i):
   v=np.zeros(n+k)
   if i:v[i-1]=1
   return v
  pv=zvec(top)-zvec(bottom);cons=[]
  for i in range(10):cons.extend([zvec(top)-zvec(i),zvec(i)-zvec(bottom)])
  v=np.zeros(n+k);v[13:17]=1;v[17:21]=-1;cons.append(v)
  v=-pv.copy();v[17:21]+=1;cons.append(v)
  v=pv.copy();v[9:13]-=1;cons.append(v)
  A.append(sparse.csc_matrix(np.array(cons)));lo.extend([0.]*(len(cons)-3)+[1e-5]*3);hi.extend([np.inf]*len(cons))
 
 if eq.any():
  A.append(sparse.hstack([sparse.csc_matrix(x[eq]),sparse.csc_matrix((int(eq.sum()),k))],format='csc'));lo.extend([0.]*int(eq.sum()));hi.extend([0.]*int(eq.sum()))
 
 # Preserve explicit single-feature directional judgments using training rows only.
 pure=(np.count_nonzero(abs(x)>1e-12,axis=1)==1)&known
 if pure.any():
  A.append(sparse.hstack([sparse.csc_matrix(d[pure,None]*x[pure]),sparse.csc_matrix((int(pure.sum()),k))],format='csc'));lo.extend([1e-4]*int(pure.sum()));hi.extend([np.inf]*int(pure.sum()))
 mat=sparse.vstack(A,format='csc');s=osqp.OSQP();s.setup(P=P,q=np.zeros(n+k),A=mat,l=np.array(lo),u=np.array(hi),verbose=False,eps_abs=1e-8,eps_rel=1e-8,max_iter=100000,polishing=True);r=s.solve()
 if r.info.status_val not in (1,2):raise RuntimeError(r.info.status)
 w=r.x[:n];p=np.r_[0,w[:9]];ranges={'vintage':float(w[13:17].sum()),'tare':float(w[17:21].sum()),'provenance':float(p.max()-p.min()),'shade':float(w[9:13].sum())}
 if ordered:assert ranges['vintage']+1e-6>=ranges['tare'] and ranges['tare']+1e-6>=ranges['provenance'] and ranges['provenance']+1e-6>=ranges['shade']
 return {'coefficients':w.tolist(),'alpha':alpha,'ordered':ordered,'learned_ranges':ranges,'training_pilot_extremes':extremes,'solver_status':r.info.status}
def select(rows,seed,ordered):
 g=np.array([repr((tuple(sorted((q['a'][0],q['b'][0]))),tuple(sorted((q['a'][1],q['b'][1]))))) for q in rows]);d=np.array([q['known_direction'] or 0 for q in rows]);scores={}
 for alpha in (.001,.01,.1):
  margins=np.zeros(len(rows))
  for tr,te in grouping.folds(g,3,seed):margins[te]=design([rows[i] for i in te])@fit([rows[i] for i in tr],alpha,ordered)['coefficients']
  sign=np.where(margins>1e-7,1,np.where(margins<-1e-7,-1,0));eq=np.array([q.get('exact_price_equality') is True for q in rows]);scores[alpha]=int(sum(sign[d!=0]==d[d!=0])+sum(sign[eq]==0))
 alpha=max(scores,key=lambda a:(scores[a],a));c=fit(rows,alpha,ordered);c['inner_direction_counts']=scores;return c

