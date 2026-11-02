"""Read-only verification of the locked domestic pricing reference."""
from pathlib import Path
import json,hashlib,itertools
from domestic_release_pricing import Model
ROOT=Path(__file__).resolve().parent.parent

def main():
 lock=json.loads((ROOT/'pricing/pricing-lock-v2.json').read_text())
 for name,digest in lock['sha256'].items():
  path=ROOT/name
  if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise RuntimeError('Missing or changed pricing artifact: '+name)
 m=Model();n=0
 for z,s,a,t in itertools.product(m.policy['approved_regions'],m.engine.domain['shades'],m.engine.domain['vintage_years'],m.engine.domain['tare_lb']):
  o=[z,s,a,t];assert m.price(o)['price_usd']==m.engine.price(o)['price_usd'];assert m.price(o)['price_usd']>0;n+=1
 assert n==500
 for z in ['southwest','Western Europe']:
  try:m.price([z,'pale/straw',20,110])
  except ValueError:pass
  else:raise AssertionError('Unsupported region accepted')
 for z,v in [('northeast',1100),('southeast',1075),('central',1050),('northwest',1000)]:assert abs(m.price([z,'pale/straw',20,110])['price_usd']-v)<1e-8
 print(f'PASS: {len(lock["sha256"])} pricing artifact hashes; 500 domestic profile outputs unchanged; 4 anchors verified; unsupported regions rejected.')
if __name__=='__main__':main()
