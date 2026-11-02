"""Model-only simple comparator. No evidence or recorded-answer retrieval."""
import argparse,json
from pathlib import Path
import numpy as np
from compare_models import features

DEFAULT=Path(__file__).with_name('simple-benchmark-v16-delivery.json')

class Model:
    def __init__(self,path=DEFAULT):
        artifact=json.loads(Path(path).read_text());cfg=artifact['model']
        self.coefficients=np.array(cfg['coefficients'],dtype=float);self.radius=float(cfg['decision_radius']);self.kind=artifact['selected_model']
        if self.coefficients.shape!=(18,) or np.any(self.coefficients[9:]<0):raise ValueError('Invalid monotone18-coefficient snapshot')

    def compare(self,a,b):
        gap=float((features(a)-features(b))@self.coefficients)
        direction='A' if gap>1e-7 else 'B' if gap<-1e-7 else None
        meaningful=abs(gap)>self.radius
        return {'prediction_source':'model_only','model':self.kind,'predicted_direction':direction,'predicted_meaningfulness':'meaningful_difference' if meaningful else 'no_meaningful_difference','combined_prediction':f'meaningful_{direction}' if meaningful else 'no_meaningful_difference','margin':gap,'decision_radius':self.radius,'exact_price_equality':None,'units':'model score, not money','qualification':'Meaningfulness calibration includes qualifier proxies; direction and size are estimates, not retrieved judgments.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--a',required=True);parser.add_argument('--b',required=True);args=parser.parse_args();print(json.dumps(Model().compare(json.loads(args.a),json.loads(args.b)),indent=2))

if __name__=='__main__':main()
