"""All-weight joint refit; coefficient inference only, no evidence lookup."""
from pathlib import Path
import argparse,json
from joint_weight_refit_v22 import predict
DEFAULT=Path(__file__).with_name('direct-joint-weights-delivery-v22.json')
class Model:
 def __init__(self,path=DEFAULT):self.config=json.loads(Path(path).read_text())['model']
 def compare(self,a,b):return {**predict(a,b,self.config),'model':'v22_direct_joint_weights'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);a=p.parse_args();print(json.dumps(Model().compare(json.loads(a.a),json.loads(a.b)),indent=2))
if __name__=='__main__':main()
