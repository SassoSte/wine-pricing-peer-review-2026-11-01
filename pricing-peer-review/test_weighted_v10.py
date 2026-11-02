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
import refit_weighted_v10 as r
import refit_weighted_v9 as previous_protocol


class WeightedV10Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parent=json.loads((r.ROOT/'evidence-v9.json').read_text())
        cls.documents=[json.loads((r.ROOT/f).read_text()) for f in r.ROUND_FILES]
        cls.evidence=json.loads((r.ROOT/'evidence-v10.json').read_text())
        cls.result=json.loads((r.ROOT/'weighted-hierarchy-comparison-v10.json').read_text())
        cls.rows=cls.evidence['rows'];cls.cfg=cls.result['candidate_fit_all_401']
        off=cls.cfg['offering_snapshot'];cls.design=offering.Design(off['local_contexts']);cls.beta=np.array(off['coefficients'])
        cls.layer=weighted.Layer(cls.design,cls.beta);cls.params=np.array(cls.cfg['parameters'])

    def test_accounting_guidance_no_mutation(self):
        before=deepcopy((self.parent,self.documents))
        rows,audit,guidance,unresolved=r.build_evidence(self.parent,self.documents)
        self.assertEqual((self.parent,self.documents),before)
        self.assertEqual(rows,self.rows);self.assertEqual(rows[:366],self.parent['rows'])
        self.assertEqual(len(rows),401)
        self.assertEqual(Counter(x['action'] for x in audit),{'new comparison':33,'resolved original':2,'confirmation; no extra sample':1,'excluded unresolved':8})
        self.assertEqual(Counter(x['winner'] for x in rows),{'A':178,'B':83,'tie':140})
        self.assertEqual(guidance,self.evidence['explanatory_guidance'])
        self.assertEqual({x['id'] for x in unresolved},{'round27-7','round27-11'})
        self.assertEqual(len({x['id'] for x in rows}),401)
        self.assertEqual(len({frozenset((tuple(x['a']),tuple(x['b']))) for x in rows}),401)
        ids={x['id']:x for x in rows}
        self.assertNotIn('round27-7',ids);self.assertNotIn('round27-11',ids)
        self.assertEqual(ids['round27-15']['resolved_by'],'round30-3')
        self.assertEqual(ids['round27-20']['resolved_by'],'round31-3')
        self.assertEqual(ids['round27-15']['winner'],'A')
        self.assertEqual(ids['round27-20']['winner'],'tie')
        self.assertEqual(ids['round27-2-provenance-swap']['winner'],'A')
        self.assertNotIn('round32-1',ids)

    def test_conflicts_unresolved_and_freeze_guards(self):
        for document in self.documents:r.verify_freeze(document)
        bad=deepcopy(self.documents);bad[-1]['questions'][0]['winner']='B'
        with self.assertRaises(ValueError):r.build_evidence(self.parent,bad)
        bad=deepcopy(self.documents);bad[0]['questions'][6]['winner']='tie'
        with self.assertRaises(ValueError):r.build_evidence(self.parent,bad)
        bad=deepcopy(self.documents[0]);bad['questions'][0]['a'][3]=130
        with self.assertRaises(AssertionError):r.verify_freeze(bad)

    def test_historical_hashes(self):
        for f,h in self.result['method']['historical_file_hashes'].items():
            self.assertEqual(hashlib.sha256((r.ROOT/f).read_bytes()).hexdigest(),h,f)
        self.assertEqual(hashlib.sha256((r.ROOT/'evidence-v10.json').read_bytes()).hexdigest(),self.result['method']['evidence_sha256'])

    def test_family_isolation_and_baseline_reproduction(self):
        _,y,g=old_protocol.common.get_arrays(self.rows,'additive');parentg=g[:366]
        old=json.loads((r.ROOT/'weighted-hierarchy-comparison-v9.json').read_text())
        for seed in prior.SEEDS:
            original=list(previous_protocol.extended_folds(parentg[:341],parentg,seed));count=np.zeros(len(y))
            for fold,(tr,te) in enumerate(r.extended_folds(parentg,g,seed)):
                count[te]+=1;np.testing.assert_array_equal(te[te<366],original[fold][1])
                self.assertFalse(set(g[tr])&set(g[te]))
                for name in ('v9_evidence_control','v10_evidence_candidate'):
                    indices=tr[tr<366] if name=='v9_evidence_control' else tr
                    expected={tuple(self.rows[i]['a'][:3]) for i in indices if self.rows[i]['a'][:3]==self.rows[i]['b'][:3] and self.rows[i]['a'][3]!=self.rows[i]['b'][3]}
                    audit=next(a for a in self.result['nested_cv']['fold_audits'] if a['seed']==seed and a['fold']==fold and a['model']==name)
                    self.assertEqual({tuple(c) for c in audit['local_contexts']},expected)
                for it,iv in base.folds(g[tr],3,seed+fold+7000):self.assertFalse(set(g[tr][it])&set(g[tr][iv]))
            np.testing.assert_array_equal(count,np.ones(len(y)))
            control=next(x for x in self.result['nested_cv']['runs']['v9_evidence_control'] if x['seed']==seed)
            original=next(x for x in old['nested_cv']['runs']['v9_evidence_candidate'] if x['seed']==seed)
            self.assertEqual(control['predictions'][:366],original['predictions'])

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
