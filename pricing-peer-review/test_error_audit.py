import hashlib
import json
from collections import Counter,defaultdict
import unittest
from pathlib import Path
import numpy as np
import compare_models as b
import compare_interactions as m
import audit_model_errors as audit


class ErrorAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=json.loads((audit.ROOT/'error-audit-v6.json').read_text())
        cls.evidence=json.loads((audit.ROOT/'evidence-v6.json').read_text())
        cls.cv=json.loads((audit.ROOT/'additive-comparison-v6.json').read_text())

    def test_models_and_evidence_unchanged(self):
        for f,h in self.result['method']['source_hashes'].items():
            self.assertEqual(hashlib.sha256((audit.ROOT/f).read_bytes()).hexdigest(),h,f)

    def test_exact_reconstruction_and_coverage(self):
        events=self.result['out_of_fold_events'];ids=self.cv['nested_cv']['row_ids']
        self.assertEqual(len(events),281*5)
        count=Counter((e['seed'],e['id']) for e in events)
        self.assertTrue(all(v==1 for v in count.values()))
        for run in self.cv['nested_cv']['runs']['v6_evidence_candidate']:
            saved=dict(zip(ids,run['predictions']))
            for event in [e for e in events if e['seed']==run['seed']]:
                self.assertEqual(b.LABEL[event['prediction']],saved[event['id']])
                self.assertEqual(audit.bucket(b.LABEL[event['actual']],saved[event['id']]),event['error_type'])

    def test_decomposition_and_persistent_counts(self):
        events=self.result['out_of_fold_events'];totals=Counter(e['error_type'] for e in events)
        wrong=len(events)-totals['correct'];self.assertEqual(wrong,357)
        for k,v in totals.items():
            self.assertEqual(self.result['error_decomposition'][k]['mean_per_repeat'],v/5)
        pairs=defaultdict(int)
        for e in events:pairs[e['id']]+=e['error_type']!='correct'
        self.assertEqual(sum(v==5 for v in pairs.values()),43)
        for item in self.result['persistent_misses']:self.assertEqual(item['misses'],pairs[item['id']])

    def test_feature_collisions_are_same_representation(self):
        rows=self.evidence['rows'];x,y,_=m.get_arrays(rows,'additive')
        by_id={r['id']:i for i,r in enumerate(rows)}
        for group in self.result['feature_collisions']:
            vectors=[];labels=[]
            for item in group:
                i=by_id[item['id']];v=x[i];nz=np.flatnonzero(abs(v)>1e-10)
                sign=1 if not len(nz) or v[nz[0]]>0 else -1
                vectors.append(v*sign);labels.append(y[i]*sign)
            self.assertGreater(len(set(labels)),1)
            for v in vectors:np.testing.assert_allclose(v,vectors[0])


if __name__=='__main__':unittest.main()
