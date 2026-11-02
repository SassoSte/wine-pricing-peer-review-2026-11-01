import hashlib
import json
import unittest
from itertools import product
import numpy as np
import compare_interactions as c
import compare_models as b


class InteractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=c.load_rows()
        cls.result=json.loads((c.ROOT/'interaction-comparison.json').read_text())

    def test_read_only_baselines_and_evidence(self):
        for section in ('baseline_hashes','evidence_hashes'):
            for name,digest in self.result['method'][section].items():
                self.assertEqual(hashlib.sha256((c.ROOT/name).read_bytes()).hexdigest(),digest,name)
        self.assertEqual(len(self.rows),158)
        ids=[r['id'] for r in self.rows]
        self.assertNotIn('round11-13',ids)
        self.assertIn('round11-2',ids)
        self.assertNotIn('round9-19',ids)

    def test_interactions_reduce_to_additive(self):
        rng=np.random.default_rng(9);beta=rng.normal(size=18)
        for family in ('shade','vintage'):
            varying=beta[9:13] if family=='shade' else beta[13:17]
            shared=beta[13:17] if family=='shade' else beta[9:13]
            expanded=np.r_[beta[:9],np.tile(varying,10),shared,beta[-1]]
            self.assertAlmostEqual(np.linalg.norm(c.penalty(family,100)@expanded)**2,np.linalg.norm(beta)**2)
            for option in product(b.ZONES,b.SHADES,b.AGES,(110,120,130)):
                self.assertAlmostEqual(c.features(option,family)@expanded,b.features(option)@beta)

    def test_model_can_express_provenance_reversal(self):
        for family in ('shade','vintage'):
            beta=np.zeros(54);beta[49:53]=1
            for zone in range(10):beta[9+4*zone:13+4*zone]=1
            wc=b.ZONES.index('West Central Asia');central=b.ZONES.index('central')
            if family=='shade':
                beta[9+4*wc:13+4*wc]=.1
                beta[9+4*central:13+4*central]=1
            else:
                beta[9+4*wc+3]=5
                beta[9+4*central+3]=1
            margins=[]
            for zone in ('West Central Asia','central'):
                margins.append((c.features([zone,'pale/straw',25,125],family)-c.features([zone,'brown',20,125],family))@beta)
            self.assertLess(margins[0],0);self.assertGreater(margins[1],0)

    def test_group_exclusion_and_coverage(self):
        _,y,g=c.get_arrays(self.rows,'additive')
        for seed in c.SEEDS:
            count=np.zeros(len(y))
            for tr,te in b.folds(g,5,seed):
                self.assertFalse(set(g[tr])&set(g[te]));count[te]+=1
                for it,iv in b.folds(g[tr],3,seed):self.assertFalse(set(g[tr][it])&set(g[tr][iv]))
            np.testing.assert_array_equal(count,np.ones(len(y)))

    def test_candidate_symmetry_and_monotonicity(self):
        for family,cfg in self.result['candidates_fit_all_158'].items():
            beta=np.array(cfg['coefficients']);self.assertEqual(len(beta),len(c.names(family)))
            for z,s,y,w in product(b.ZONES,b.SHADES,b.AGES,(110,115,120,125,130)):
                value=c.features([z,s,y,w],family)@beta
                if w>110:self.assertGreaterEqual(c.features([z,s,y,w-5],family)@beta+1e-8,value)
                if y>20:self.assertGreaterEqual(c.features([z,s,y-5,w],family)@beta+1e-8,value)
                if s!='pale/straw':self.assertGreaterEqual(c.features([z,b.SHADES[b.SHADES.index(s)+1],y,w],family)@beta+1e-8,value)
            x,_,_=c.get_arrays(self.rows,family)
            np.testing.assert_array_equal(b.classify(-x@beta,cfg['threshold']),-b.classify(x@beta,cfg['threshold']))

    def test_metrics_recompute(self):
        _,y,_=c.get_arrays(self.rows,'additive')
        for runs in self.result['nested_cv']['runs'].values():
            for run in runs:
                actual=b.metrics(y,np.array(run['predictions']))
                self.assertEqual(actual['matched'],run['all']['matched'])
                self.assertAlmostEqual(actual['balanced_accuracy'],run['all']['balanced_accuracy'])


if __name__=='__main__':unittest.main()
