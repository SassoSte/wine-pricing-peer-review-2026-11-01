import json,unittest,itertools
from pathlib import Path
import numpy as np
from predictor_reporting import Model
from predictor_v28 import Model as V28
from predictor_premium_v35 import Model as Candidate
from equality_span import LinearEqualityCertificate
import global_positive_v33 as intrinsic
R=Path(__file__).resolve().parent
class ReportingTests(unittest.TestCase):
 def test_all_saved_predictions_and_swap(self):
  rows=json.loads((R/'benchmark-targets-v35.json').read_text())['rows']
  for name,baseline in [('v28',V28()),('large_tare_candidate',Candidate())]:
   m=Model(backend=name)
   for q in rows:
    a,b=q['a'],q['b'];p=m.compare(a,b);self.assertEqual(p['legacy_prediction'],baseline.compare(a,b));self.assertEqual(p['premium_zone'],m.compare(b,a)['premium_zone']);self.assertIsNone(p['exact_price_equality'])
 def test_boundary_semantics(self):
  m=Model();a=['Western Europe','golden',20,120]
  for gap,want in [(0.,'no_meaningful_premium'),(.999,'small_directional_advantage'),(1.,'borderline_premium'),(1.499,'borderline_premium'),(1.5,'meaningful_premium')]:
   class Fake:
    def compare(self,a,b):return {'margin':gap,'predicted_direction':'A' if gap else None}
   m.engine=Fake();p=m.compare(a,a);self.assertEqual(p['premium_zone'],want);self.assertIsNone(p['exact_price_equality'])
 def test_invalid_offering(self):
  with self.assertRaises(ValueError):Model().compare(['fake','brown',20,110],['central','brown',20,110])
 def test_span_no_strict_preferences_erased(self):
  rows=json.loads((R/'benchmark-targets-v35.json').read_text())['rows'];ties=[q for q in rows if q.get('exact_price_equality') is True];w=json.loads((R/'global-positive-config-v33.json').read_text())['value_model']['coefficients'];c=LinearEqualityCertificate(intrinsic.design(ties),w);self.assertEqual(c.rank,2)
  for q in ties:self.assertTrue(c.check(intrinsic.design([q])[0])['supported'])
  for q in rows:
   if q['known_direction'] is not None:self.assertFalse(c.check(intrinsic.design([q])[0])['supported'],q['id'])
  # Removing unique older identity eliminates its implication, even if fitted gap is zero.
  old=next(q for q in ties if q['id']=='round50-9');other=[q for q in ties if q['id']!=old['id']];self.assertFalse(LinearEqualityCertificate(intrinsic.design(other),w).check(intrinsic.design([old])[0])['supported'])
  # A connected equality group must have bounded total span, not just adjacent closeness.
  offerings=list(itertools.product(intrinsic.D['provenances'],intrinsic.D['shades'],intrinsic.D['vintage_years'],intrinsic.D['tare_lb']));f=np.array([intrinsic.features(o) for o in offerings]);projected=f-(f@c.basis.T)@c.basis;groups={}
  for i,v in enumerate(projected):groups.setdefault(tuple(np.round(v,8)),[]).append(i)
  for ids in groups.values():
   vals=f[ids]@w;self.assertLessEqual(float(max(vals)-min(vals)),1e-7)
   for i in ids:self.assertTrue(c.check(f[i]-f[ids[0]])['supported'])
 def test_span_rejects_incompatible_weights(self):
  with self.assertRaises(ValueError):LinearEqualityCertificate([[1,0]],[1,1])
if __name__=='__main__':unittest.main()
