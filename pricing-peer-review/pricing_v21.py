"""V21 comparative direction and meaningfulness model; not monetary pricing."""
import argparse,json
from pathlib import Path
from shade_vintage_shared_v21 import predict
DEFAULT=Path(__file__).with_name('shade-vintage-shared-delivery-v21.json')
class Model:
 def __init__(self,path=DEFAULT):
  saved=json.loads(Path(path).read_text());self.config=saved['model'];self.selected=saved['selected_model']
 def compare(self,a,b):return {**predict(a,b,self.config),'model':'v21_'+self.selected}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a',required=True);p.add_argument('--b',required=True);a=p.parse_args();print(json.dumps(Model().compare(json.loads(a.a),json.loads(a.b)),indent=2))
if __name__=='__main__':main()
