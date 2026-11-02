"""Freeze 20 fresh attribute-stratified comparisons before any responses."""
from pathlib import Path
import json,hashlib,itertools,random
from predictor_reporting_v2 import Model
R=Path(__file__).resolve().parent
key=lambda a,b:tuple(sorted((tuple(a),tuple(b))))
def main():
 seen=set()
 def collect(x):
  if isinstance(x,dict):
   a,b=x.get('a'),x.get('b')
   if isinstance(a,list) and isinstance(b,list) and len(a)==len(b)==4 and all(not isinstance(v,(list,dict)) for v in a+b):seen.add(key(a,b))
   for v in x.values():collect(v)
  elif isinstance(x,list):
   for v in x:collect(v)
 files=sorted(set(R.glob('round*.json'))|set(R.glob('*sealed.json'))|{R/'evidence-v37.json',R/'comparisons.json',R/'combined-pilot-v34-fixed.json'})
 for f in files:
  if f.exists():collect(json.loads(f.read_text()))
 seen_before=set(seen);domain=Model().engine.domain;offers=list(itertools.product(domain['provenances'],domain['shades'],domain['vintage_years'],domain['tare_lb']));rng=random.Random(3702);categories=['heavy_brown_comparison','lower_tare_shade_control','core_tradeoff','mixed_provenance','aligned_advantages'];questions=[]
 def matches(cat,a,b):
  same=a[0]==b[0]
  if cat=='heavy_brown_comparison':return a[1] in ('copper','amber') and a[3]>=125 and b[1]=='brown' and abs(a[2]-b[2])<=5
  if cat=='lower_tare_shade_control':return same and a[1] in ('copper','amber') and a[3]<=115 and b[1]=='brown' and a[2]==b[2] and abs(a[3]-b[3])<=10
  if cat=='core_tradeoff':return same and a[1]==b[1] and (a[2]-b[2])*(a[3]-b[3])<0 and abs(a[3]-b[3]) in (5,15)
  if cat=='mixed_provenance':return not same and a[1]==b[1] and abs(a[2]-b[2])<=5 and abs(a[3]-b[3])<=5
  return same and a[2]<b[2] and a[3]<b[3] and domain['shades'].index(a[1])>=domain['shades'].index(b[1])
 # Choose all questions without consulting either model's predictions.
 for cat in categories:
  pool=[(a,b) for a in offers for b in offers if matches(cat,a,b) and key(a,b) not in seen]
  for _ in range(4):
   while True:
    a,b=rng.choice(pool)
    if key(a,b) not in seen:break
   seen.add(key(a,b));a,b=(b,a) if rng.random()<.5 else (a,b);questions.append({'stratum':cat,'a':list(a),'b':list(b),'status':'sealed_unasked'})
 rng.shuffle(questions)
 for i,q in enumerate(questions,1):q.update(id=f'prospective-v37-{i}',number=i)
 assert len({key(q['a'],q['b']) for q in questions})==20;assert not any(key(q['a'],q['b']) in seen_before for q in questions)
 models={name:Model(backend=name) for name in ('v28','v37')};predictions=[{'id':q['id'],**{name:m.compare(q['a'],q['b']) for name,m in models.items()}} for q in questions];payload={'questions':questions,'predictions':predictions}
 sourcefiles=['predictor_reporting_v2.py','reporting-config-v2.json','predictor_v28.py','predictor_v27.py','model-config-v28.json','predictor_premium_v35.py','predictor_premium_v37.py','premium-config-v37.json','freeze_prospective_v37.py']
 out={'status':'sealed_unasked','protocol':'20fresh unorderedpairs,5attribute strata of4each, shuffled; selected before predictions, no answer/ranking-based selection. Targeted stress test, not population sample. Keep questions,models,bands,predictions frozen until all20 answered. No answers or elicitation yet.','evaluation_plan':{'primary':'Compare binary size and joint accuracy plus three-zone coverage/errors separately; abstention never counts as correct.','report':['direction accuracy (must be identical acrossmodels)','binary size and joint accuracy','coverage and retained-size errors','false meaningful calls, missed premiums and genuine premiums withheld','per-stratum errors and protected-control regressions'],'success_gate':'Consider promotion only if candidate improves size classification without new confirmed-premium losses in lower-tare controls; reporting should reduce false calls without lower retained accuracy and without more than5percentagepoints coverage loss versusV28. Mixed results inconclusive. Small20case test doesnotprove populationaccuracy.','no_retuning':'Do not use answers to select thresholds or alter this sealed test. Preserve first answers separately from any post-result corrections.'},'freshness_source_hashes':{str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.exists()},'source_hashes':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sourcefiles},'payload_sha256':hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest(),**payload}
 path=R/'prospective-v37-sealed.json';assert not path.exists();path.write_text(json.dumps(out,indent=2)+'\n');print('Frozen20fresh questions and both models\' predictions. No questions displayed.')
if __name__=='__main__':main()
