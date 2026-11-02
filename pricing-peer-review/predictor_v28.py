"""V28 entry point using the unchanged standalone20-coefficient prediction engine."""
from pathlib import Path
import argparse,json
from predictor_v27 import Model as Engine
DEFAULT_CONFIG=Path(__file__).with_name('model-config-v28.json')
class Model(Engine):
 def __init__(self,path=DEFAULT_CONFIG):super().__init__(path)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);p.add_argument('--config',default=str(DEFAULT_CONFIG));a=p.parse_args();print(json.dumps(Model(a.config).compare(json.loads(a.a),json.loads(a.b)),indent=2))
if __name__=='__main__':main()
