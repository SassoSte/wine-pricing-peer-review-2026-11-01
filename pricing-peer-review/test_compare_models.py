"""Checks for evidence isolation, symmetry, and candidate behavior."""
import hashlib
import json
import unittest
from itertools import product
import numpy as np
import compare_models as c


class ModelComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=json.loads((c.ROOT/'model-comparison.json').read_text())
        cls.old,cls.held=c.load_rows()

    def test_evidence_counts_and_frozen_production(self):
        self.assertEqual((len(self.old),len(self.held)),(101,18))
        self.assertEqual(hashlib.sha256((c.ROOT/'pricing.py').read_bytes()).hexdigest(),
                         self.result['method']['production_sha256'])
        self.assertTrue(all(r['winner'] in c.LABEL for r in self.old+self.held))
        self.assertNotIn('round9-19',[r['id'] for r in self.held])
        self.assertNotIn('r4-10',[r['id'] for r in self.old])

    def test_group_isolation_and_coverage(self):
        x,y,g=c.arrays(self.old+self.held)
        for seed in c.SEEDS:
            counts=np.zeros(len(y),dtype=int)
            for tr,te in c.folds(g,5,seed):
                self.assertFalse(set(g[tr]) & set(g[te]))
                counts[te]+=1
                for it,iv in c.folds(g[tr],3,seed):
                    self.assertFalse(set(g[tr][it]) & set(g[tr][iv]))
            np.testing.assert_array_equal(counts,np.ones(len(y)))

    def test_swap_symmetry_and_tie_band(self):
        margins=np.array([-2.,-.3,0.,.3,2.])
        np.testing.assert_array_equal(c.classify(margins,.3),[-1,0,0,0,1])
        np.testing.assert_array_equal(c.classify(-margins,.3),-c.classify(margins,.3))
        x,y,_=c.arrays(self.old)
        b=c.fit(x,y,1.)
        swapped=c.fit(-x,-y,1.)
        np.testing.assert_allclose(b,swapped,atol=1e-8)

    def test_candidate_monotonicity_on_full_grid(self):
        for candidate in self.result['candidates_fit_all_119'].values():
            beta=np.array([candidate['coefficients'][f] for f in c.FEATURES])
            for z,s,y,w in product(c.ZONES,c.SHADES,c.AGES,(110,115,120,125,130)):
                value=c.features([z,s,y,w])@beta
                if w>110:self.assertGreaterEqual(c.features([z,s,y,w-5])@beta+1e-9,value)
                if y>20:self.assertGreaterEqual(c.features([z,s,y-5,w])@beta+1e-9,value)
                if s!='pale/straw':
                    self.assertGreaterEqual(c.features([z,c.SHADES[c.SHADES.index(s)+1],y,w])@beta+1e-9,value)

    def test_metrics_recomputed(self):
        _,y,_=c.arrays(self.old+self.held)
        for runs in self.result['grouped_cv']['runs'].values():
            for run in runs:
                m=c.metrics(y,np.array(run['predictions']))
                self.assertEqual(m['matched'],run['matched'])
                self.assertAlmostEqual(m['balanced_accuracy'],run['balanced_accuracy'])


if __name__=='__main__':unittest.main()
