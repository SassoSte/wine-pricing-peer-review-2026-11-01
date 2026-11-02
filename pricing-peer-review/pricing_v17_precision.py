"""Precision-improved v17 candidate; same19 features, no answer lookup."""
import argparse
from pathlib import Path
import json
from pricing_v17 import Model as OriginalModel

DEFAULT=Path(__file__).with_name('precision-shade-candidate-v17.json')

class Model(OriginalModel):
    def __init__(self,path=DEFAULT):super().__init__(path)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);args=p.parse_args();print(json.dumps(Model().compare(json.loads(args.a),json.loads(args.b)),indent=2))

if __name__=='__main__':main()
