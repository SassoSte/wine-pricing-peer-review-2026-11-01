"""V18 model-only pricing comparison; direction and meaningfulness stay separate."""
import argparse
import json
from pathlib import Path
import numpy as np
from contextual_meaningfulness import predict

DEFAULT = Path(__file__).with_name('contextual-boundary-fit-delivery-v18.json')

class Model:
    def __init__(self, path=DEFAULT):
        saved = json.loads(Path(path).read_text())
        cfg = saved['model']
        self.beta = np.asarray(cfg['underlying_coefficients'], dtype=float)
        self.beta.setflags(write=False)
        self.base_radius = cfg['base_radius']
        self.kind = cfg['context_kind']
        self.eta = cfg['context_coefficient']
        if len(self.beta) != 19 or self.base_radius <= 0 or not 0 <= self.eta <= 1:
            raise ValueError('Invalid model parameters')

    def compare(self, a, b):
        result = predict(a, b, self.beta, self.base_radius, self.kind, self.eta)
        result.update(model='v18_contextual_meaningfulness', context_kind=self.kind,
                      units='model score, not money')
        return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--a', required=True)
    parser.add_argument('--b', required=True)
    args = parser.parse_args()
    print(json.dumps(Model().compare(json.loads(args.a), json.loads(args.b)), indent=2))

if __name__ == '__main__':
    main()
