"""Model-only selected comparator from the minimal-context v16 experiment."""
import argparse,json
from pathlib import Path
import numpy as np
import compare_models as base
import minimal_context_model as context

DEFAULT=Path(__file__).with_name('minimal-context-rule-delivery-v16.json')

class Model:
    def __init__(self,path=DEFAULT):
        saved=json.loads(Path(path).read_text());cfg=saved['model'];self.kind=saved['selected_model'];self.beta=np.array(cfg['coefficients']);self.radius=cfg['decision_radius']
        self.features=context.features if len(self.beta)==21 else base.features
        if len(self.beta) not in (18,21):raise ValueError('Unsupported model size')
        if cfg.get('tare_rule_applied'):self.radius=max(self.radius,abs(float(self.beta[17]))+1e-8)

    def compare(self,a,b):
        gap=float((self.features(a)-self.features(b))@self.beta);direction='A' if gap>1e-7 else 'B' if gap<-1e-7 else None;meaningful=abs(gap)>self.radius
        return {'prediction_source':'model_only','model':self.kind,'predicted_direction':direction,'predicted_meaningfulness':'meaningful_difference' if meaningful else 'no_meaningful_difference','combined_prediction':f'meaningful_{direction}' if meaningful else 'no_meaningful_difference','margin':gap,'decision_radius':self.radius,'exact_price_equality':None,'units':'model score, not money','qualification':'Exploratory model estimate; meaningfulness labels include proxies. No recorded-answer lookup.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);args=p.parse_args();print(json.dumps(Model().compare(json.loads(args.a),json.loads(args.b)),indent=2))

if __name__=='__main__':main()
