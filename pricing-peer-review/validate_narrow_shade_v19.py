import json,hashlib
from pathlib import Path
import numpy as np
import narrow_shade_v19 as model
import refit_simple_benchmark_v16 as metrics
from reconcile_and_compare import write_versioned
R=Path(__file__).resolve().parent
SOURCES=['evidence-v19.json','benchmark-targets-v19.json','contextual-fixes-validation-v19.json','contextual-fixes-delivery-v19.json','contextual_fixes_v19.py','narrow_shade_v19.py','validate_narrow_shade_v19.py']
def main():
 hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in SOURCES};old=json.loads((R/'contextual-fixes-validation-v19.json').read_text());t=json.loads((R/'benchmark-targets-v19.json').read_text())['rows'];e=json.loads((R/'evidence-v19.json').read_text())['rows'];idx={q['id']:i for i,q in enumerate(t)};direct=metrics.verified_materiality(e);runs={'v19':old['nested_cv']['runs']['boundary'],'narrow':[]};audits=[]
 for seed in metrics.SEEDS:
  margins=np.zeros(len(t));radii=np.zeros(len(t))
  for fold in [a for a in old['nested_cv']['fold_audits'] if a['seed']==seed]:
   cfg={'underlying_coefficients':fold['underlying_coefficients'],'base_radius':fold['base_radius'],'context_kind':fold['prior_context']['kind'],'context_coefficient':fold['prior_context']['eta'],**fold['choices']['boundary']}
   tr=[idx[i] for i in fold['training_ids']];te=[idx[i] for i in fold['validation_ids']];train=[t[i] for i in tr];test=[t[i] for i in te];coefficient,search=model.fit(train,[e[i] for i in tr],cfg);g,r,h=model.arrays(test,cfg);margins[te]=g+coefficient*h;radii[te]=r
   audits.append({'seed':seed,'fold':fold['fold'],'training_ids':fold['training_ids'],'validation_ids':fold['validation_ids'],'base_config':cfg,'coefficient':coefficient,'search':search})
  runs['narrow'].append({'seed':seed,'margins':margins.tolist(),'radii':radii.tolist(),'score':metrics.score(t,margins,radii,direct)})
 summary=metrics.summarize(runs);base=summary['v19'];s=summary['narrow'];checks={'direction_noninferior':s['direction']['accuracy']>=base['direction']['accuracy']-1e-10,'size_noninferior':s['materiality']['balanced_accuracy']>=base['materiality']['balanced_accuracy']-1e-10,'false_premiums_noninferior':s['materiality']['false_meaningful']<=base['materiality']['false_meaningful']+1e-10,'missed_meaningful_noninferior':s['materiality']['missed_meaningful']<=base['materiality']['missed_meaningful']+1e-10,'direct_size_noninferior':s['directly_supported_materiality']['accuracy']>=base['directly_supported_materiality']['accuracy']-1e-10,'strict_improvement':s['direction']['accuracy']>base['direction']['accuracy']+1e-10 or s['materiality']['balanced_accuracy']>base['materiality']['balanced_accuracy']+1e-10}
 cfg=json.loads((R/'contextual-fixes-delivery-v19.json').read_text())['model'];coefficient,search=model.fit(t,e,cfg);cfg={**cfg,'narrow_shade_coefficient':coefficient};active=[q['id'] for q in t if model.feature(q['a'],q['b'],cfg['underlying_coefficients'])!=0];pred={q['id']:model.predict(q['a'],q['b'],cfg) for q in t if q['id'] in active or q['id'] in ['revision-14','round21-15','round36-12','round38-5']}
 result={'source_hashes':hashes,'protocol':'Single predeclared gate: foreign matched provenance and equal tare, golden/pale opposition with younger golden. Same one bounded coefficient grid and training objective as v19. Cached v19 folds/coefficients/boundaries unchanged; fit coefficient only on training families. Require no regression and strict held-out improvement for promotion. No evidence relabeling. Pair-dependent comparison correction, not a global per-offering price utility; no transitivity claim. Exploratory reused families.','nested_cv':{'runs':runs,'summary':summary,'fold_audits':audits},'full_model':cfg,'full_search':search,'active_evidence_ids':active,'selected_full_predictions':pred,'delivery':{'selected':'narrow' if all(checks.values()) else 'v19','checks':checks}}
 write_versioned(R/'narrow-shade-validation-v19.json',result);write_versioned(R/'narrow-shade-candidate-v19.json',{'model':cfg,'promoted':all(checks.values()),'validation_file':'narrow-shade-validation-v19.json','qualification':'Pair-comparison hypothesis; full fit is not prospective validation.'})
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 print(json.dumps({'summary':summary,'delivery':result['delivery'],'full_coefficient':coefficient,'active_ids':active,'predictions':pred},indent=2))
if __name__=='__main__':main()
