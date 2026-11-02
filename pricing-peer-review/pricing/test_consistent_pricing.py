import unittest,json,itertools,math
from pathlib import Path
from consistent_price_layer import Model
P=Path(__file__).resolve().parent
class ConsistentPricingTests(unittest.TestCase):
 def setUp(self):self.m=Model()
 def test_supplied_anchors(self):
  for z,p in [('northeast',1100),('southeast',1075),('central',1050),('northwest',1000)]:self.assertAlmostEqual(self.m.price([z,'pale/straw',20,110])['price_usd'],p)
 def test_reference_independence(self):
  x=['northeast','golden',25,115]
  for ref in [['northeast','pale/straw',20,110],['northeast','pale/straw',25,110],['northwest','brown',40,130]]:self.assertAlmostEqual(self.m.translate_from_reference(x,ref),self.m.price(x)['price_usd'])
 def test_domain_monotonicity_and_positive_prices(self):
  d=self.m.domain
  for z,s,a,t in itertools.product(d['provenances'],d['shades'],d['vintage_years'],d['tare_lb']):
   v=self.m.price([z,s,a,t])['price_usd'];self.assertTrue(math.isfinite(v) and v>0)
   if a>20:self.assertGreaterEqual(self.m.price([z,s,a-5,t])['price_usd']+1e-8,v)
   if t>110:self.assertGreaterEqual(self.m.price([z,s,a,t-5])['price_usd']+1e-8,v)
   j=d['shades'].index(s)
   if j<4:self.assertGreaterEqual(self.m.price([z,d['shades'][j+1],a,t])['price_usd']+1e-8,v)
 def test_zero_gold_pale_at130(self):
  for z in self.m.domain['provenances']:
   for a in self.m.domain['vintage_years']:self.assertEqual(self.m.price([z,'golden',a,130])['price_usd'],self.m.price([z,'pale/straw',a,130])['price_usd'])
 def test_boundaries_and_scope(self):
  with self.assertRaises(ValueError):self.m.price(['northeast','golden',25,105])
  self.assertEqual(self.m.price(['Western Europe','pale/straw',20,110])['anchor_status'],'model_inferred')
  self.assertTrue(self.m.price(['northeast','brown',40,130])['extrapolating_attribute_curve'])
 def test_telescope_and_symmetry(self):
  a=['northeast','golden',25,115];b=['central','amber',30,120];c=['northwest','brown',40,130]
  self.assertAlmostEqual(self.m.compare(a,b)['difference']+self.m.compare(b,c)['difference'],self.m.compare(a,c)['difference']);self.assertAlmostEqual(self.m.compare(a,b)['difference'],-self.m.compare(b,a)['difference'])
if __name__=='__main__':unittest.main()
