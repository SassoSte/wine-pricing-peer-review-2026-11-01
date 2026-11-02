from collections import Counter
from copy import deepcopy
import hashlib
import json
from itertools import product
import unittest
import numpy as np
import compare_models as base
import compare_interactions as models
import refit_additive_v6 as r


class EvidenceV6Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v5=json.loads((r.ROOT/'evidence-v5.json').read_text())
        cls.r19=json.loads((r.ROOT/'round19-fixed.json').read_text())
        cls.r20=json.loads((r.ROOT/'round20-isolation.json').read_text())
        cls.evidence=json.loads((r.ROOT/'evidence-v6.json').read_text())
        cls.results=json.loads((r.ROOT/'additive-comparison-v6.json').read_text())

    def test_evidence_accounting_and_no_mutation(self):
        original=deepcopy((self.v5,self.r19,self.r20))
        rows,audit=r.build_evidence(self.v5,self.r19,self.r20)
        self.assertEqual((self.v5,self.r19,self.r20),original)
        self.assertEqual(rows,self.evidence['rows'])
        self.assertEqual(rows[:252],self.v5['rows'])
        self.assertEqual(len(rows),281)
        self.assertEqual(Counter(x['action'] for x in audit),{'new comparison':20,'new component comparison':9})
        self.assertEqual(Counter(x['winner'] for x in rows),{'A':126,'B':64,'tie':91})
        self.assertEqual(len({x['id'] for x in rows}),281)
        self.assertEqual(len({frozenset((tuple(x['a']),tuple(x['b']))) for x in rows}),281)

    def test_unresolved_or_repeat_rejected(self):
        bad=deepcopy(self.r20);bad['questions'][0]['status']='unresolved'
        with self.assertRaises(ValueError):r.build_evidence(self.v5,self.r19,bad)
        bad=deepcopy(self.r20);bad['questions'][0]['revisits']='round19-14'
        with self.assertRaises(ValueError):r.build_evidence(self.v5,self.r19,bad)

    def test_historical_hashes_and_frozen_scores(self):
        for f,h in self.results['method']['historical_file_hashes'].items():
            self.assertEqual(hashlib.sha256((r.ROOT/f).read_bytes()).hexdigest(),h,f)
        self.assertEqual(hashlib.sha256((r.ROOT/'evidence-v6.json').read_bytes()).hexdigest(),self.results['method']['evidence_sha256'])
        rescored=self.results['unchanged_baseline_rescoring']
        self.assertEqual(rescored['revision_e']['round19_original_answers']['matched'],self.r19['scores']['revision_e']['matched'])
        self.assertEqual(rescored['frozen_v5_additive']['round19_original_answers']['matched'],self.r19['scores']['additive_v5']['matched'])

    def test_matched_family_folds_and_metrics(self):
        rows=self.evidence['rows'];_,y,g=models.get_arrays(rows,'additive');old=np.arange(len(rows))<252
        for seed in models.SEEDS:
            coverage=np.zeros(len(rows))
            for train,test in base.folds(g,5,seed):
                coverage[test]+=1
                for tr in (train,train[old[train]]):
                    self.assertFalse(set(g[tr])&set(g[test]))
                    for it,iv in base.folds(g[tr],3,seed):self.assertFalse(set(g[tr][it])&set(g[tr][iv]))
            np.testing.assert_array_equal(coverage,np.ones(len(rows)))
        for runs in self.results['nested_cv']['runs'].values():
            for run in runs:
                m=base.metrics(y,np.array(run['predictions']))
                self.assertEqual(m['matched'],run['metrics']['all']['matched'])
                self.assertAlmostEqual(m['balanced_accuracy'],run['metrics']['all']['balanced_accuracy'])

    def test_fit_symmetry_and_full_grid_weak_monotonicity(self):
        cfg=self.results['candidate_fit_all_281'];beta=np.array(cfg['coefficients'])
        x,y,_=models.get_arrays(self.evidence['rows'],'additive')
        self.assertEqual(base.metrics(y,base.classify(x@beta,cfg['threshold']))['matched'],cfg['in_sample']['matched'])
        np.testing.assert_array_equal(base.classify(-x@beta,cfg['threshold']),-base.classify(x@beta,cfg['threshold']))
        for z,s,age,w in product(base.ZONES,base.SHADES,base.AGES,(110,115,120,125,130)):
            value=base.features([z,s,age,w])@beta
            if w>110:self.assertGreaterEqual(base.features([z,s,age,w-5])@beta+1e-8,value)
            if age>20:self.assertGreaterEqual(base.features([z,s,age-5,w])@beta+1e-8,value)
            if s!='pale/straw':self.assertGreaterEqual(base.features([z,base.SHADES[base.SHADES.index(s)+1],age,w])@beta+1e-8,value)


if __name__=='__main__':unittest.main()
