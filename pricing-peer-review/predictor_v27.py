"""Selected20-coefficient comparator. Runtime needs only NumPy and one JSON config."""
from pathlib import Path
import argparse,json
import numpy as np
DEFAULT_CONFIG=Path(__file__).with_name('model-config-v27.json')

class Model:
    def __init__(self,path=DEFAULT_CONFIG):
        self.config=json.loads(Path(path).read_text());c=self.config
        if c['schema_version']!=1:raise ValueError('Unsupported configuration schema')
        self.domain=c['domain'];self.weights=np.asarray(c['coefficients'],dtype=float)
        if self.weights.shape!=(20,) or not np.all(np.isfinite(self.weights)):raise ValueError('Invalid coefficients')
        if not -1e-7<=self.weights[19]<=self.weights[17]+1e-7:raise ValueError('Invalid tare-compensation bound')
        self.weights.setflags(write=False)

    def _offering(self,o):
        if len(o)!=4:raise ValueError('Expected provenance,shade,vintage,tare')
        z,s,a,w=o;d=self.domain;rules=self.config['offering_rules']
        if z not in d['provenances'] or s not in d['shades'] or a not in d['vintage_years'] or w not in d['tare_lb']:raise ValueError(f'Unsupported option: {o}')
        f=np.array([float(z==v) for v in d['provenances'][1:]]+[float(d['shades'].index(s)>=i) for i in range(1,5)]+[float(d['vintage_years'].index(a)>=i) for i in range(1,5)]+[(rules['tare_reference']-w)/rules['tare_step']])
        if s=='pale/straw' and w==rules['zero_golden_pale_tare']:f[12]=0.
        return f

    def _pair(self,a,b):
        raw=self._offering(a)-self._offering(b);v=self.config['matched_vintage'];t=self.config['tare_compensation'];same=a[0]==b[0];sign=float(np.sign(b[2]-a[2]))
        match=same and abs(a[2]-b[2])==v['age_gap'] and {a[1],b[1]}==set(v['shade_pair'])
        younger,older=(a,b) if a[2]<b[2] else (b,a)
        compensate=same and abs(a[2]-b[2])==t['age_gap'] and younger[2]<=t['maximum_younger_age'] and younger[3]-older[3]==t['heavier_by_lb']
        return np.r_[raw,sign if match else 0.,sign if compensate else 0.]

    def compare(self,a,b):
        g=float(self._pair(a,b)@self.weights);c=self.config['classification'];r=c['decision_radius']
        return {'predicted_direction':'A' if g>c['direction_epsilon'] else 'B' if g<-c['direction_epsilon'] else None,'predicted_meaningfulness':'meaningful_difference' if abs(g)>r+c['meaningfulness_epsilon'] else 'no_meaningful_difference','margin':g,'decision_radius':r,'exact_price_equality':c['exact_price_equality'],'prediction_source':'model_only','units':c['units'],'model':self.config['model_id']}

    def compare_many(self,pairs):return [self.compare(a,b) for a,b in pairs]

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);p.add_argument('--config',default=str(DEFAULT_CONFIG));args=p.parse_args();print(json.dumps(Model(args.config).compare(json.loads(args.a),json.loads(args.b)),indent=2))
if __name__=='__main__':main()
