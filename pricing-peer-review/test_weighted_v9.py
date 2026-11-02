from collections import Counter
from copy import deepcopy
import hashlib
import json
from itertools import product
import unittest
import numpy as np
import compare_models as base
import compare_tare_models as tare
import provenance_tare_model as offering
import domestic_hierarchy_model as prior
import weighted_domestic_model as weighted
import refit_provenance_v8 as old_protocol
import refit_weighted_v9 as r


class WeightedV9Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parent=json.loads((r.ROOT/'evidence-v8.json').read_text())
        cls.r25=json.loads((r.ROOT/'round25-fixed.json').read_text())
        cls.r26=json.loads((r.ROOT/'round26-isolation.json').read_text())
        cls.evidence=json.loads((r.ROOT/'evidence-v9.json').read_text())
        cls.result=json.loads((r.ROOT/'weighted-hierarchy-comparison-v9.json').read_text())
        cls.rows=cls.evidence['rows'];cls.cfg=cls.result['candidate_fit_all_366']
        off=cls.cfg['offering_snapshot'];cls.design=offering.Design(off['local_contexts']);cls.beta=np.array(off['coefficients'])
        cls.layer=weighted.Layer(cls.design,cls.beta);cls.params=np.array(cls.cfg['parameters'])

    def test_accounting_guidance_no_mutation(self):
        before=deepcopy((self.parent,self.r25,self.r26))
        rows,audit,guidance=r.build_evidence(self.parent,self.r25,self.r26)
        self.assertEqual((self.parent,self.r25,self.r26),before)
        self.assertEqual(rows,self.rows);self.assertEqual(rows[:341],self.parent['rows'])
        self.assertEqual(len(rows),366)
        self.assertEqual(Counter(x['action'] for x in audit),{'new comparison':20,'new component comparison':5})
        self.assertEqual(Counter(x['winner'] for x in rows),{'A':167,'B':71,'tie':128})
        self.assertEqual(len(guidance),25);self.assertEqual(guidance,self.evidence['explanatory_guidance'])
        self.assertEqual(len({x['id'] for x in rows}),366)
        self.assertEqual(len({frozenset((tuple(x['a']),tuple(x['b']))) for x in rows}),366)

    def test_incomplete_or_repeated_source_rejected(self):
        bad=deepcopy(self.r26);bad['questions'][0]['status']='unresolved'
        with self.assertRaises(ValueError):r.build_evidence(self.parent,self.r25,bad)
        bad=deepcopy(self.r26);bad['questions'][0]['revisits']='round25-11'
        with self.assertRaises(ValueError):r.build_evidence(self.parent,self.r25,bad)

    def test_historical_hashes(self):
        for f,h in self.result['method']['historical_file_hashes'].items():
            self.assertEqual(hashlib.sha256((r.ROOT/f).read_bytes()).hexdigest(),h,f)
        self.assertEqual(hashlib.sha256((r.ROOT/'evidence-v9.json').read_bytes()).hexdigest(),self.result['method']['evidence_sha256'])

    def test_family_isolation_and_baseline_reproduction(self):
        _,y,g=old_protocol.common.get_arrays(self.rows,'additive');parentg=g[:341]
        old=json.loads((r.ROOT/'weighted-domestic-comparison.json').read_text())
        for seed in prior.SEEDS:
            original=list(old_protocol.extended_folds(parentg[:310],parentg,seed));count=np.zeros(len(y))
            for fold,(tr,te) in enumerate(r.extended_folds(parentg,g,seed)):
                count[te]+=1;np.testing.assert_array_equal(te[te<341],original[fold][1])
                self.assertFalse(set(g[tr])&set(g[te]))
                for it,iv in base.folds(g[tr],3,seed+fold+7000):self.assertFalse(set(g[tr][it])&set(g[tr][iv]))
            np.testing.assert_array_equal(count,np.ones(len(y)))
            control=next(x for x in self.result['nested_cv']['runs']['v8_evidence_control'] if x['seed']==seed)
            original=next(x for x in old['nested_cv']['runs'] if x['seed']==seed)
            self.assertEqual(control['predictions'][:341],original['predictions'])

    def test_foreign_invariance_exact_ties_and_monotonicity(self):
        for z,s,age,w in product(base.ZONES,base.SHADES,base.AGES,tare.WEIGHTS):
            value=self.layer.score([z,s,age,w],self.params)
            if z not in prior.DOMESTIC:self.assertAlmostEqual(value,self.design.features([z,s,age,w])@self.beta)
            if age>20:self.assertGreaterEqual(self.layer.score([z,s,age-5,w],self.params)+2e-6,value)
            if s!='pale/straw':self.assertGreaterEqual(self.layer.score([z,base.SHADES[base.SHADES.index(s)+1],age,w],self.params)+2e-6,value)
            if w>110:self.assertGreaterEqual(self.layer.score([z,s,age,w-5],self.params)+2e-6,value)
        mask=tare.masks(self.rows)['confirmed_pure_tare_ties']
        x,offset=self.layer.array(self.rows);margin=offset+x@self.params
        np.testing.assert_allclose(margin[mask],0,atol=1e-7)
        np.testing.assert_array_equal(base.classify(-margin,self.cfg['threshold']),-base.classify(margin,self.cfg['threshold']))

    def test_metrics(self):
        _,y,_=old_protocol.common.get_arrays(self.rows,'additive')
        for runs in self.result['nested_cv']['runs'].values():
            for run in runs:self.assertEqual(base.metrics(y,np.array(run['predictions']))['matched'],run['metrics']['all']['matched'])
        self.assertEqual(base.metrics(y,weighted.predict(self.rows,self.layer,self.params,self.cfg['threshold']))['matched'],self.cfg['in_sample']['matched'])


if __name__=='__main__':unittest.main()
