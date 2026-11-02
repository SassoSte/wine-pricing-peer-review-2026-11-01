"""Selected v19 comparison model. No evidence lookup during prediction."""
import argparse,json
from pathlib import Path
from contextual_fixes_v19 import predict
DEFAULT=Path(__file__).with_name('contextual-fixes-delivery-v19.json')
class Model:
 def __init__(self,path=DEFAULT):
  saved=json.loads(Path(path).read_text());self.config=saved['model'];self.selected=saved['selected_model']
 def compare(self,a,b):return {**predict(a,b,self.config),'model':'v19_'+self.selected}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);a=p.parse_args();print(json.dumps(Model().compare(json.loads(a.a),json.loads(a.b)),indent=2))
if __name__=='__main__':main()
