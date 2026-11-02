import hashlib
import json
from itertools import product
import unittest
import numpy as np
from scipy.optimize import check_grad
import compare_models as b
import compare_tare_models as t
import provenance_tare_model as p
import domestic_hierarchy_model as prior
import refit_provenance_v8 as protocol
import weighted_domestic_model as model


class WeightedDomesticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=json.loads((model.ROOT/'weighted-domestic-comparison.json').read_text())
        cls.rows=json.loads((model.ROOT/'evidence-v8.json').read_text())['rows']
        cls.cfg=cls.result['candidate_fit_all_341'];off=cls.cfg['offering_snapshot']
        cls.design=p.Design(off['local_contexts']);cls.beta=np.array(off['coefficients'])
        cls.layer=model.Layer(cls.design,cls.beta);cls.params=np.array(cls.cfg['parameters'])

    def test_data_and_baselines_unchanged(self):
        self.assertEqual(len(self.rows),341)
        for f,h in self.result['method']['historical_file_hashes'].items():
            self.assertEqual(hashlib.sha256((model.ROOT/f).read_bytes()).hexdigest(),h,f)
        self.assertEqual(len(self.layer.prior_pairs),30)

    def test_recover_original_and_keep_foreign_fixed(self):
        for option in product(b.ZONES,b.SHADES,b.AGES,t.WEIGHTS):
            old=self.design.features(option)@self.beta
            self.assertAlmostEqual(self.layer.score(option,self.layer.initial),old)
            if option[0] not in prior.DOMESTIC:self.assertAlmostEqual(self.layer.score(option,self.params),old)

    def test_gradient(self):
        x,offset=self.layer.array(self.rows[:30]);y=np.array([b.LABEL[r['winner']] for r in self.rows[:30]])
        params=self.layer.initial+np.random.default_rng(10).uniform(.01,.05,size=33)
        error=check_grad(lambda q:model.objective(q,x,offset,y,self.layer,1.)[0],lambda q:model.objective(q,x,offset,y,self.layer,1.)[1],params)
        self.assertLess(error,1e-4)

    def test_exact_tare_equalities_and_monotonicity(self):
        for z,s,age in product(b.ZONES,b.SHADES,b.AGES):
            for wa,wb in zip(t.WEIGHTS,t.WEIGHTS[1:]):
                old=(self.design.features([z,s,age,wa])-self.design.features([z,s,age,wb]))@self.beta
                new=self.layer.score([z,s,age,wa],self.params)-self.layer.score([z,s,age,wb],self.params)
                scale=self.params[32] if z in prior.DOMESTIC else 1
                self.assertAlmostEqual(new,scale*old)
        for z,s,age,w in product(b.ZONES,b.SHADES,b.AGES,t.WEIGHTS):
            value=self.layer.score([z,s,age,w],self.params)
            if age>20:self.assertGreaterEqual(self.layer.score([z,s,age-5,w],self.params)+2e-6,value)
            if s!='pale/straw':self.assertGreaterEqual(self.layer.score([z,b.SHADES[b.SHADES.index(s)+1],age,w],self.params)+2e-6,value)
        x,o=self.layer.array(self.rows);m=o+x@self.params
        np.testing.assert_array_equal(b.classify(-m,self.cfg['threshold']),-b.classify(m,self.cfg['threshold']))

    def test_validation_partitions_and_metrics(self):
        _,y,g=protocol.common.get_arrays(self.rows,'additive')
        for seed in prior.SEEDS:
            count=np.zeros(len(y))
            for fold,(tr,te) in enumerate(protocol.extended_folds(g[:310],g,seed)):
                count[te]+=1;self.assertFalse(set(g[tr])&set(g[te]))
                for it,iv in b.folds(g[tr],3,seed+fold+7000):self.assertFalse(set(g[tr][it])&set(g[tr][iv]))
            np.testing.assert_array_equal(count,np.ones(len(y)))
        for run in self.result['nested_cv']['runs']:
            self.assertEqual(b.metrics(y,np.array(run['predictions']))['matched'],run['metrics']['all']['matched'])
        self.assertEqual(b.metrics(y,model.predict(self.rows,self.layer,self.params,self.cfg['threshold']))['matched'],self.cfg['in_sample']['matched'])


if __name__=='__main__':unittest.main()
