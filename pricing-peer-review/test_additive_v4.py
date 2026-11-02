from collections import Counter
from copy import deepcopy
import hashlib
import json
from itertools import product
import unittest
import numpy as np
import compare_models as base
import compare_interactions as models
import refit_additive_v4 as r


class EvidenceV4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v3=json.loads((r.ROOT/'evidence-v3.json').read_text())
        cls.r15=json.loads((r.ROOT/'round15-fixed.json').read_text())
        cls.r16=json.loads((r.ROOT/'round16-isolation.json').read_text())
        cls.sources={i['source_file']:json.loads((r.ROOT/i['source_file']).read_text()) for i in cls.r16['unresolved_queue']}
        cls.evidence=json.loads((r.ROOT/'evidence-v4.json').read_text())
        cls.results=json.loads((r.ROOT/'additive-comparison-v4.json').read_text())

    def test_evidence_accounting_and_resolution_provenance(self):
        originals=deepcopy((self.v3,self.r15,self.r16,self.sources))
        rows,audit=r.build_evidence(self.v3,self.r15,self.r16,self.sources)
        self.assertEqual((self.v3,self.r15,self.r16,self.sources),originals)
        self.assertEqual(rows,self.evidence['rows'])
        self.assertEqual(rows[:183],self.v3['rows'])
        self.assertEqual(len(rows),224)
        self.assertEqual(Counter(a['action'] for a in audit),{'new comparison':18,'new component comparison':8,'resolved previously unanswered':15})
        self.assertEqual(Counter(x['winner'] for x in rows),{'A':95,'B':61,'tie':68})
        self.assertEqual(len({x['id'] for x in rows}),224)
        self.assertEqual(len({frozenset((tuple(x['a']),tuple(x['b']))) for x in rows}),224)
        by_id={x['id']:x for x in rows}
        for item in self.r16['unresolved_queue']:
            row=by_id[item['source_id']]
            self.assertEqual(row['winner'],item['winner'])
            self.assertEqual(row['current_answer_source'],item['resolution_id'])
            self.assertIn(row['prior_answer']['status'],('unresolved','deferred'))
            self.assertNotIn(item['resolution_id'],by_id)
        self.assertTrue(all(x['winner'] in ('A','B','tie') for x in rows))

    def test_mismatched_resolution_rejected(self):
        bad=deepcopy(self.r16);bad['unresolved_queue'][0]['winner']='tie'
        with self.assertRaises(ValueError):r.build_evidence(self.v3,self.r15,bad,self.sources)
        bad=deepcopy(self.r16);bad['unresolved_queue'][0]['status']='queued'
        with self.assertRaises(ValueError):r.build_evidence(self.v3,self.r15,bad,self.sources)

    def test_baselines_and_historical_receipts_unchanged(self):
        for f,h in self.results['method']['historical_file_hashes'].items():
            self.assertEqual(hashlib.sha256((r.ROOT/f).read_bytes()).hexdigest(),h,f)
        self.assertEqual(hashlib.sha256((r.ROOT/'evidence-v4.json').read_bytes()).hexdigest(),self.results['method']['evidence_sha256'])
        scores=self.r15['scores']
        rescored=self.results['unchanged_baseline_rescoring']
        self.assertEqual(rescored['revision_e']['round15_original_answers']['matched'],scores['revision_e']['matched'])
        self.assertEqual(rescored['frozen_v3_additive']['round15_original_answers']['matched'],scores['additive_v3']['matched'])

    def test_matched_family_folds_and_metrics(self):
        rows=self.evidence['rows'];_,y,g=models.get_arrays(rows,'additive');old=np.arange(len(rows))<183
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
                metric=base.metrics(y,np.array(run['predictions']))
                self.assertEqual(metric['matched'],run['metrics']['all']['matched'])
                self.assertAlmostEqual(metric['balanced_accuracy'],run['metrics']['all']['balanced_accuracy'])

    def test_candidate_symmetry_and_weak_monotonicity(self):
        cfg=self.results['candidate_fit_all_224'];beta=np.array(cfg['coefficients'])
        x,y,_=models.get_arrays(self.evidence['rows'],'additive')
        self.assertEqual(base.metrics(y,base.classify(x@beta,cfg['threshold']))['matched'],cfg['in_sample']['matched'])
        np.testing.assert_array_equal(base.classify(-x@beta,cfg['threshold']),-base.classify(x@beta,cfg['threshold']))
        for z,s,age,w in product(base.ZONES,base.SHADES,base.AGES,(110,115,120,125,130)):
            value=base.features([z,s,age,w])@beta
            if w>110:self.assertGreaterEqual(base.features([z,s,age,w-5])@beta+1e-8,value)
            if age>20:self.assertGreaterEqual(base.features([z,s,age-5,w])@beta+1e-8,value)
            if s!='pale/straw':self.assertGreaterEqual(base.features([z,base.SHADES[base.SHADES.index(s)+1],age,w])@beta+1e-8,value)


if __name__=='__main__':unittest.main()
