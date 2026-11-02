import json,unittest,itertools
from pathlib import Path
from predictor_reporting_v2 import Model
from predictor_reporting import Model as OldReport
from predictor_v28 import Model as V28
from predictor_premium_v37 import Model as V37
R=Path(__file__).resolve().parent
class ReportingV2Tests(unittest.TestCase):
 def test_parity_and_swap(self):
  rows=json.loads((R/'benchmark-targets-v37.json').read_text())['rows']
  for name,raw in [('v28',V28()),('v37',V37())]:
   m=Model(backend=name)
   for q in rows:
    a,b=q['a'],q['b'];r=m.compare(a,b);rev=m.compare(b,a);self.assertEqual(r['legacy_prediction'],raw.compare(a,b));self.assertEqual(r['premium_zone'],rev['premium_zone']);self.assertAlmostEqual(r['premium_reporting_score'],rev['premium_reporting_score']);self.assertIsNone(r['exact_price_equality'])
    if name=='v28':self.assertEqual(r['premium_zone'],OldReport().compare(a,b)['premium_zone'])
 def test_uses_corrected_score(self):
  a=['central','brown',40,125];b=['central','amber',35,130];m=Model(backend='v37');r=m.compare(a,b);self.assertEqual(r['premium_reporting_score'],V37().compare(a,b)['premium_decision_score']+1);self.assertNotEqual(r['premium_reporting_score'],abs(r['legacy_prediction']['margin']));self.assertEqual(r['premium_zone'],'small_directional_advantage')
 def test_candidate_boundaries(self):
  m=Model(backend='v37')
  for score,zone in [(0.,'small_directional_advantage'),(.999,'small_directional_advantage'),(1.,'borderline_premium'),(1.499,'borderline_premium'),(1.5,'meaningful_premium')]:
   class Fake:
    def compare(self,a,b):return {'margin':2.,'predicted_direction':'A','premium_decision_score':score-1}
   m.engine=Fake();self.assertEqual(m.compare([],[])['premium_zone'],zone)
 def test_invalid_backend(self):
  with self.assertRaises(ValueError):Model(backend='unknown')
if __name__=='__main__':unittest.main()
