"""V20 pair comparator: direction and practical meaningfulness, not dollar prices."""
import argparse,json
from pathlib import Path
from contextual_shade_v20 import predict
DEFAULT=Path(__file__).with_name('contextual-shade-delivery-v20.json')
class Model:
 def __init__(self,path=DEFAULT):
  saved=json.loads(Path(path).read_text());self.config=saved['model'];self.selected=saved['selected_model']
 def compare(self,a,b):return {**predict(a,b,self.config),'model':'v20_'+self.selected}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);args=p.parse_args();print(json.dumps(Model().compare(json.loads(args.a),json.loads(args.b)),indent=2))
if __name__=='__main__':main()
