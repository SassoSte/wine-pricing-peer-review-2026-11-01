"""Six one-factor isolation comparisons anchored to Round38 Q8."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from pricing_v19 import Model
import narrow_shade_v19 as narrow
R=Path(__file__).resolve().parent

def main():
 out=R/'round39-fixed.json'
 if out.exists():raise FileExistsError(out)
 anchor=json.loads((R/'round38-fixed.json').read_text())['questions'][7]
 a,b=anchor['a'],anchor['b'];assert a==['Western Europe','golden',25,125] and b==['Western Europe','pale/straw',30,125]
 # Tare crossover, provenance crossover, then age gap removed and widened.
 specs=[('tare',3,120,'both'),('provenance',0,'Eastern Europe','both'),('tare',3,130,'both'),('provenance',0,'West Central Asia','both'),('vintage',2,25,'b'),('vintage',2,20,'a')]
 baseline=Model();candidate=json.loads((R/'narrow-shade-candidate-v19.json').read_text());questions=[]
 for i,(factor,col,value,side) in enumerate(specs,1):
  aa=a.copy();bb=b.copy()
  if side in ('a','both'):aa[col]=value
  if side in ('b','both'):bb[col]=value
  changed={j for j in range(4) if aa[j]!=a[j] or bb[j]!=b[j]};assert changed=={col}
  questions.append({'id':f'round39-{i}','number':i,'a':aa,'b':bb,'factor_changed':factor,'changed_sides':side,'anchor':'round38-8','predictions':{'v19':baseline.compare(aa,bb),'narrow_shade_candidate':narrow.predict(aa,bb,candidate['model'])},'status':'pending','direction':None,'meaningfulness':None,'raw_answer':None,'exact_price_instruction':False})
 files=['evidence-v19.json','benchmark-targets-v19.json','round38-fixed.json','contextual-fixes-delivery-v19.json','narrow-shade-candidate-v19.json','contextual-boundary-fit-delivery-v18.json','precision-shade-candidate-v17.json','pricing_v19.py','contextual_fixes_v19.py','narrow_shade_v19.py','domestic_shade_model.py','compare_models.py','contextual_meaningfulness.py','freeze_round39.py']
 fields=['id','number','a','b','factor_changed','changed_sides','anchor','predictions']
 data={'round':39,'created_at':datetime.now(timezone.utc).isoformat(),'status':'in_progress','purpose':'Diagnostic isolation, not fresh predictive accuracy. Six fixed questions change one attribute dimension relative to round38-8: shared tare120/130, shared provenance EE/WCA, vintage gap0/10 by changing one side. No feedback or refits until completion. Direction and size separate; missing and unresolved allowed; practical similarity not exact equality.','anchor':{'id':'round38-8','a':a,'b':b},'models':{'v19':json.loads((R/'contextual-fixes-delivery-v19.json').read_text()),'narrow_shade_candidate':candidate},'file_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in files},'freeze_fields':fields,'questions_and_predictions_sha256':hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in questions],sort_keys=True).encode()).hexdigest(),'questions':questions,'rule_statements':[],'scores':None}
 out.write_text(json.dumps(data,indent=2)+'\n');saved=json.loads(out.read_text());assert hashlib.sha256(json.dumps([{k:q[k] for k in fields} for q in saved['questions']],sort_keys=True).encode()).hexdigest()==data['questions_and_predictions_sha256']
 for q in saved['questions']:
  assert baseline.compare(q['a'],q['b'])==q['predictions']['v19'];assert narrow.predict(q['a'],q['b'],candidate['model'])==q['predictions']['narrow_shade_candidate']
 p=R/'pricing-reset-progress.json';d=json.loads(p.read_text());d.update(status='Round39 Q8 isolation frozen; awaiting question1',active_round=out.name,next_question=1,answered_questions=0,note='Six fixed one-factor questions anchored to round38-8. Diagnostic, not fresh accuracy. V19 and rejected narrower candidate frozen; no refits.');p.write_text(json.dumps(d,indent=2)+'\n')
 block='## Active Round39 — Question8 one-factor isolation\n\nSix questions frozen in round39-fixed.json. Each varies only provenance, vintage\nor tare relative to round38-8. Diagnostic isolation, not fresh accuracy. V19 and\nrejected narrow-shade candidate snapshots/predictions frozen; evidence unchanged.\nOne question at a time, hide predictions and earlier answers, record direction and\nmeaningfulness separately. Unresolved/save for later allowed. Q1 awaiting answer.\n\n'
 for name in ('README.md','HANDOFF.md'):
  p=R/name;first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+block+rest.lstrip('\n'))
 print(json.dumps({'frozen':6,'one_factor_checks':6,'prediction_rechecks':12,'first':{k:questions[0][k] for k in ('a','b')}}))
if __name__=='__main__':main()
