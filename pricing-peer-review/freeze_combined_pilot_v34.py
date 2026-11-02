"""Verify consolidation and freeze fresh attribute-stratified questions before elicitation."""
from pathlib import Path
import json,hashlib,itertools,random
import numpy as np
from predictor_combined_v34 import Model
from predictor_v28 import Model as Baseline
import global_positive_v33 as rank
R=Path(__file__).resolve().parent
key=lambda a,b:tuple(sorted((tuple(a),tuple(b))))
def main():
 m=Model();b=Baseline();targets=json.loads((R/'benchmark-targets-v34.json').read_text())['rows'];checks=[];conflicts=[]
 for q in targets:
  p=m.compare(q['a'],q['b']);old=b.compare(q['a'],q['b']);g=float((rank.features(q['a'])-rank.features(q['b']))@m.weights);assert abs(p['margin']-g)<1e-12;assert p['predicted_meaningfulness']==old['predicted_meaningfulness'];rev=m.compare(q['b'],q['a']);assert abs(rev['margin']+p['margin'])<1e-12;assert rev['predicted_meaningfulness']==p['predicted_meaningfulness']
  if p['head_conflict']:conflicts.append(q['id'])
 seen=set()
 def collect(x):
  if isinstance(x,dict):
   a,b=x.get('a'),x.get('b')
   if isinstance(a,list) and isinstance(b,list) and len(a)==len(b)==4 and all(not isinstance(z,(list,dict)) for z in a+b):seen.add(key(a,b))
   for v in x.values():collect(v)
  elif isinstance(x,list):
   for v in x:collect(v)
 files=sorted(set(R.glob('round*.json'))|{R/'evidence-v34.json',R/'comparisons.json'});read=[]
 for f in files:
  if f.exists():collect(json.loads(f.read_text()));read.append(f.name)
 rng=random.Random(34058);D=m.domain;offerings=[list(x) for x in itertools.product(D['provenances'],D['shades'],D['vintage_years'],D['tare_lb'])];sh=lambda o:D['shades'].index(o[1]);top=lambda o:o[2]==20 and o[3]==110 and o[1]=='pale/straw' and o[0] in ['Western Europe','northeast']
 categories=['clear_extreme','small_tare','vintage_tare_tradeoff','older_dark','top_profile','cross_provenance','clear_extreme','small_tare','vintage_tare_tradeoff','older_dark','top_profile','cross_provenance'];questions=[]
 def eligible(cat,a,b):
  same=a[0]==b[0]
  if cat=='clear_extreme':return same and a[2]<=25 and b[2]>=35 and a[3]<=115 and b[3]>=125 and sh(a)>=3 and sh(b)<=1
  if cat=='small_tare':return same and a[1:3]==b[1:3] and abs(a[3]-b[3])==5
  if cat=='vintage_tare_tradeoff':return same and a[1]==b[1] and a[2]+5==b[2] and a[3]-b[3] in (10,15)
  if cat=='older_dark':return same and min(a[2],b[2])>=35 and sh(a)<=2 and sh(b)<=2 and abs(a[2]-b[2])<=5 and abs(a[3]-b[3]) in (5,10)
  if cat=='top_profile':return top(a) and same and b[2]<=25 and b[3]<=120 and sh(b)>=3 and not top(b)
  if cat=='cross_provenance':return not same and a[1]==b[1] and abs(a[2]-b[2]) in (0,5) and abs(a[3]-b[3]) in (0,5)
 for num,cat in enumerate(categories,1):
  # Attribute-only selection; forecasts not consulted.
  pool=[(a,c) for a in offerings for c in offerings if eligible(cat,a,c) and key(a,c) not in seen];assert pool,cat;a,c=rng.choice(pool);a,c=(c,a) if rng.random()<.5 else (a,c);seen.add(key(a,c));questions.append({'number':num,'id':f'combined-pilot-v34-{num}','category':cat,'a':a,'b':c,'status':'unanswered'})
 frozen=[{'id':q['id'],'combined':m.compare(q['a'],q['b']),'v28':b.compare(q['a'],q['b'])} for q in questions];fields=['id','number','category','a','b'];sha=hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in questions],sort_keys=True).encode()).hexdigest()
 out={'status':'in_progress','protocol':'12 fresh unordered pairs, sampled by attributes only before predictions. One at a time. Direction separate from meaningfulness; exact equality, practical nondirection and unresolved distinct. No refitting until all answers complete. Baselinev28 comparator. Fullset andforecasts frozen.','freeze_fields':fields,'questions_sha256':sha,'source_hashes':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['combined-config-v34.json','predictor_combined_v34.py','model-config-v28.json','predictor_v27.py','freeze_combined_pilot_v34.py']},'freshness_files':read,'questions':questions,'frozen_predictions':frozen}
 path=R/'combined-pilot-v34-fixed.json';assert not path.exists();path.write_text(json.dumps(out,indent=2)+'\n');receipt={'evidence_pair_output_checks':len(targets),'rank_outputs_match':True,'premium_outputs_match':True,'swap_checks_pass':True,'historical_head_conflict_ids':conflicts,'fresh_questions':12,'freeze_sha256':sha};(R/'combined-verification-v34.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'checks':len(targets),'head_conflicts':len(conflicts),'question1':questions[0]},indent=2))
if __name__=='__main__':main()
