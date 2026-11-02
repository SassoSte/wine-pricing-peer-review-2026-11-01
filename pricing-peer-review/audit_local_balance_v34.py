"""Diagnose local older-WE equality without adding a pair-specific prediction rule."""
import json,hashlib
from pathlib import Path
import numpy as np
import global_positive_v33 as model
R=Path(__file__).resolve().parent
def main():
 r=json.loads((R/'brown-validation-v34.json').read_text());rows=json.loads((R/'benchmark-targets-v34.json').read_text())['rows'];by={q['id']:q for q in rows};tie=by['round50-9'];slight=by['voice-older-we-equal-tare'];out=[]
 for f in r['fold_audits']:
  if f['arm']!='unchanged_structure' or tie['id'] not in f['validation_ids']:continue
  w=np.array(f['fit']['coefficients']);train=[by[id] for id in f['training_ids']];x=model.design(train);d=np.array([q['known_direction'] or 0 for q in train]);eq=np.array([q.get('exact_price_equality') is True for q in train]);g=float(model.design([tie])[0]@w);step=w[19] if g>=0 else w[20];balance=float(115+5*g/step);assert 110<=balance<=120
  # Shift a tiny contribution between adjacent tare steps. Total range unchanged.
  # Both other confirmed equalities depend on their sum, so they remain exact.
  alternatives=[]
  for delta in (-1e-5,1e-5):
   v=w.copy();v[19]+=delta;v[18]-=delta;assert min(v[9:])>=-1e-7
   assert np.allclose(x[eq]@v,0,atol=1e-7)
   pure=(np.count_nonzero(abs(x)>1e-12,axis=1)==1)&(d!=0);assert np.all(d[pure]*(x[pure]@v)>=1e-4-1e-7)
   correct=int(sum((x@v)[d!=0]*d[d!=0]>1e-7));before=int(sum((x@w)[d!=0]*d[d!=0]>1e-7));alternatives.append({'delta':delta,'training_direction_count_before':before,'training_direction_count_after':correct,'older_pair_gap':float(model.design([tie])[0]@v),'training_equalities_preserved':True,'training_single_step_sign_constraints_preserved':True})
  out.append({'seed':f['seed'],'older_tie_gap':g,'equal_tare_gap':float(model.design([slight])[0]@w),'interpolated_balance_tare_lb':balance,'interpolation_note':'Diagnostic linear interpolation between learned5lb steps; off-grid weights not independently validated.','nearby_alternative_weights':alternatives})
 full=r['full_models']['unchanged_structure']['fit'];w=np.array(full['coefficients']);ids=['round50-9','voice-older-we-equal-tare','round50-10','round50-11','round50-12'];local=[{'id':id,'gap':float(model.design([by[id]])[0]@w),'direction':by[id]['known_direction'],'exact':by[id].get('exact_price_equality')} for id in ids]
 result={'scope':'No new evidence or coefficients adopted. Read-only residual/identifiability audit of savedv34fits plus feasible tiny perturbations.','heldout_fits':out,'local_full_fit':local,'finding':'Existing architecture represents linked judgments and local ranking constraints. Heldout family has no exact equality identifying the specific35/40,brown/amber,115/120 exchange. Nearby valid tare-step allocations preserve known equality constraints and single-step signs while moving the older gap.','decision':'Do not add another regional or shade penalty. Preserve confirmed equality in training; report its limited transfer. No wider equality band, no answer lookup counted as prediction, no numerical premium inferred.','limitation':'Training direction counts preserved by small perturbations do not mean identical loss or equal statistical likelihood. Off-grid crossing is illustrative only. Exact equality of unobserved tradeoffs remains unsupported.','source_hashes':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['benchmark-targets-v34.json','brown-validation-v34.json','audit_local_balance_v34.py']}}
 (R/'local-balance-audit-v34.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'crossings':[q['interpolated_balance_tare_lb'] for q in out],'perturbed_training_counts':[[[a['training_direction_count_before'],a['training_direction_count_after']] for a in q['nearby_alternative_weights']] for q in out],'local_full_fit':local},indent=2))
if __name__=='__main__':main()
