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
  sign=np.where(margins>1e-7,1,np.where(margins<-1e-7,-1,0));scores[alpha]=int(sum(sign[d!=0]==d[d!=0]))
 alpha=max(scores,key=lambda a:(scores[a],a));c=fit(rows,alpha,ordered);c['inner_direction_counts']=scores;return c

def main():
 t=json.loads((R/'benchmark-targets-v31.json').read_text())['rows'];by={q['id']:q for q in t};ix={q['id']:i for i,q in enumerate(t)};prior=json.loads((R/'v31-refit-validation.json').read_text());runs={k:[] for k in ('unconstrained','ordered')};audits=[]
 for seed in (11,29,47,71,103):
  gs={k:np.zeros(len(t)) for k in runs}
  for f in (f for f in prior['fold_audits'] if f['seed']==seed):
   train=[by[id] for id in f['training_ids']];test=[by[id] for id in f['validation_ids']];te=[ix[id] for id in f['validation_ids']]
   for name in runs:
    c=select(train,seed*100+f['fold'],name=='ordered');gs[name][te]=design(test)@c['coefficients'];audits.append({'arm':name,'seed':seed,'fold':f['fold'],'training_ids':f['training_ids'],'validation_ids':f['validation_ids'],'fit':c})
  d=np.array([q['known_direction'] or 0 for q in t]);mask=d!=0
  for name,g in gs.items():sg=np.where(g>1e-7,1,np.where(g<-1e-7,-1,0));runs[name].append({'seed':seed,'margins':g.tolist(),'direction_n':int(mask.sum()),'direction_correct':int(sum(sg[mask]==d[mask])),'direction_accuracy':float(np.mean(sg[mask]==d[mask]))})
  print('Completed',seed,[(k,runs[k][-1]['direction_correct']) for k in runs],flush=True)
 full=select(t,31001,True);out={'source_hashes':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ('evidence-v31.json','benchmark-targets-v31.json','model-config-v28.json','predictor_v28.py','predictor_v27.py','global_priority_v31.py')},'protocol':'Globalfirst ranking test onv31. Nonnegative learnedvintage/tare/shade stepcurves,learnedregional effects. Orderedarm enforces TOTALnormalizedattribute ranges Vintage>Tare>Provenance>Shade with numerical1e-5separation,notfixed5/4/3/2 coefficients andnotuniversalper-step dominance. Provinceextreme identities selectedbytraining-only pilot,notinventedregionalordering. Exactties retained assoftzero constraints; localcontext equality beyondglobalcapacity isnotclaimedsolved. No premiumhead changes orspecialists yet. Same25outerfamilyfolds andtraining-only innerselection. Baselines untouched; exploratoryreusedvalidation.','runs':runs,'fold_audits':audits,'full_model':full,'mean_direction_accuracy':{k:float(np.mean([q['direction_accuracy'] for q in rs])) for k,rs in runs.items()}}
 (R/'global-priority-validation-v31.json').write_text(json.dumps(out,indent=2)+'\n');(R/'global-priority-config-v31.json').write_text(json.dumps(full,indent=2)+'\n');print(json.dumps({'accuracy':out['mean_direction_accuracy'],'ranges':full['learned_ranges']},indent=2))
if __name__=='__main__':main()
