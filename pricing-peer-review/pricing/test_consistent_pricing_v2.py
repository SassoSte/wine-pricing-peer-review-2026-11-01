import unittest,json
from pathlib import Path
from test_consistent_pricing import ConsistentPricingTests
from consistent_price_v2 import Model
from consistent_price_layer import Model as Prior
P=Path(__file__).resolve().parent
class RefinedPricingTests(ConsistentPricingTests):
 def setUp(self):self.m=Model()
 def test_boundaries_and_scope(self):
  with self.assertRaises(ValueError):self.m.price(['northeast','golden',25,105])
  self.assertEqual(self.m.price(['Western Europe','pale/straw',20,110])['anchor_status'],'model_inferred')
  self.assertTrue(self.m.price(['northwest','brown',40,130])['regional_low_end_transfer_assumed'])
  self.assertFalse(self.m.price(['northeast','brown',40,130])['extrapolating_attribute_curve'])
 def test_new_judgments(self):
  self.assertAlmostEqual(self.m.price(['northeast','amber',35,120])['price_usd'],450)
  v=self.m.price(['northeast','brown',40,130])['price_usd'];self.assertLessEqual(v,300);self.assertAlmostEqual(v,300)
 def test_old_fit_unchanged(self):
  prior=Prior()
  for o in self.m.config['calibration_offerings']:self.assertEqual(self.m.price(o)['price_usd'],prior.price(o)['price_usd'])
  self.assertEqual(self.m.knots[:len(prior.knots)],prior.knots)
if __name__=='__main__':unittest.main()
