import unittest,json,hashlib
from pathlib import Path
from itertools import product
import numpy as np
import refit_exact_context_v31 as rank
from validate_refit_v31 import predict,relation_score
from predictor_v31 import Model
R=Path(__file__).resolve().parent
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=json.loads((R/'evidence-v31.json').read_text());cls.t=json.loads((R/'benchmark-targets-v31.json').read_text())['rows'];cls.by={q['id']:q for q in cls.t};cls.r=json.loads((R/'v31-refit-validation.json').read_text());cls.a=json.loads((R/'v31-anchored-validation.json').read_text());cls.api=Model()
 def test_reconciliation(self):
  old=json.loads((R/'benchmark-targets-v30.json').read_text())['rows'];self.assertEqual(len(self.t),640);self.assertEqual([q['id'] for q in self.t],[q['id'] for q in old]);self.assertEqual(len({frozenset((tuple(q['a']),tuple(q['b']))) for q in self.t}),640);self.assertEqual(len(self.e['reconciliation']),18);self.assertTrue(all(q['action']=='supersede' for q in self.e['reconciliation']));self.assertEqual(sum(q['known_direction'] is not None for q in self.t),460)
  self.assertEqual({q['id'] for q in self.t if q.get('exact_price_equality') is True},{'round50-9','round6-8','round8-4'});self.assertEqual(self.by['round51-7']['value_relation'],'unspecified');self.assertIsNone(self.by['round51-7']['exact_price_equality'])
  for id in ('round6-10','round6-9','round7-1'):self.assertEqual(self.by[id]['known_direction'],1);self.assertEqual(self.by[id]['materiality_target'],0)
  ev={q['id']:q for q in self.e['rows']};self.assertIn('bottom tier',ev['round50-9']['raw_explanation']);self.assertIn('inventory_qualification',ev['round37-9']);self.assertTrue(ev['round51-7']['selected_option_text']);self.assertTrue(ev['round6-10']['answer_history']);self.assertTrue(ev['round50-2']['meaningfulness_basis'])
 def test_all_supplied_review_judgments(self):
  for q in self.t:
   if not q.get('latest_source_id','').startswith('round57-'):continue
   p=self.api.compare(q['a'],q['b'])
   if q.get('exact_price_equality') is True:self.assertEqual(p['predicted_value_relation'],'equal');self.assertTrue(p['exact_price_equality'])
   elif q['known_direction'] is not None:self.assertEqual(p['predicted_direction'],'A' if q['known_direction']==1 else 'B');self.assertFalse(p['exact_price_equality'])
   self.assertEqual(p['predicted_meaningfulness'],'no_meaningful_difference' if q['materiality_target']==0 else 'meaningful_difference')
 def test_protected_and_domain(self):
  c=self.a['full_model']['ranking_model'];w=np.array(c['coefficients']);self.assertTrue(np.all(rank.structural()@w>=-1e-7))
  for id in rank.base.PROTECTED:
   q=self.by[id];p=self.api.compare(q['a'],q['b']);self.assertEqual(p['predicted_direction'],'A' if q['known_direction']==1 else 'B');self.assertEqual(p['predicted_meaningfulness'],'no_meaningful_difference' if q['materiality_target']==0 else 'meaningful_difference')
  for z,a in product(self.api.domain['provenances'],self.api.domain['vintage_years']):np.testing.assert_array_equal(self.api.features([z,'golden',a,130]),self.api.features([z,'pale/straw',a,130]))
 def test_exact_metric_not_near_tie(self):
  g=np.array([q['known_direction'] or 0 for q in self.t],float);b=np.array([q['materiality_target'] not in(None,0) for q in self.t]);_,_,a=relation_score(self.t,g,b,np.ones(len(g),bool));self.assertEqual(a['exact_ties_correct'],3);i=next(i for i,q in enumerate(self.t) if q.get('exact_price_equality') is True);g[i]=.01;_,_,a=relation_score(self.t,g,b,np.ones(len(g),bool));self.assertEqual(a['exact_ties_correct'],2)
 def test_no_leakage_and_integrity(self):
  def group(q):return tuple(sorted((q['a'][0],q['b'][0]))),tuple(sorted((q['a'][1],q['b'][1])))
  for r in (self.e,self.r,self.a):
   for f,h in r['source_hashes'].items():self.assertEqual(hashlib.sha256((R/f).read_bytes()).hexdigest(),h)
  for r in (self.r,self.a):
   for f in r['fold_audits']:
    tr=set(f['training_ids']);te=set(f['validation_ids']);self.assertFalse({group(self.by[id]) for id in tr}&{group(self.by[id]) for id in te});c=f['fit']['ranking_model'];self.assertTrue(set(c['exact_equality_training_ids'])<=tr);self.assertFalse(set(c['exact_equality_training_ids'])&te)
    for inner in c['inner_selection']['partitions']:self.assertTrue(set(inner['fit']['exact_equality_training_ids'])<=set(inner['training_ids']));self.assertFalse(set(inner['fit']['exact_equality_training_ids'])&set(inner['validation_ids']))
 def test_runtime_parity_and_intrinsic_order(self):
  d=self.api.domain;grid=list(product(d['provenances'],d['shades'],d['vintage_years'],d['tare_lb']));rng=np.random.default_rng(31)
  for o in grid:np.testing.assert_array_equal(self.api.features(o),rank.features(o))
  pairs=[(q['a'],q['b']) for q in self.t]+[(grid[i],grid[j]) for i,j in rng.integers(len(grid),size=(1000,2))]
  for a,b in pairs:
   a,b=list(a),list(b);p=self.api.compare(a,b);g,large,prob=predict([{'a':a,'b':b}],self.a['full_model'],'legacy_reference');self.assertAlmostEqual(p['margin'],g[0]);self.assertEqual(p['premium_justified'],bool(large[0]));self.assertAlmostEqual(p['premium_justification_score'],prob[0]);rev=self.api.compare(b,a);self.assertAlmostEqual(p['margin'],-rev['margin']);self.assertEqual(p['exact_price_equality'],rev['exact_price_equality']);self.assertEqual(p['premium_justified'],rev['premium_justified'])
  for i,j,k in rng.integers(len(grid),size=(100,3)):self.assertAlmostEqual(self.api.compare(grid[i],grid[j])['margin']+self.api.compare(grid[j],grid[k])['margin'],self.api.compare(grid[i],grid[k])['margin'])
if __name__=='__main__':unittest.main()
