"""Verify the documented model reference; never refit or rewrite an artifact."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
MANIFEST=ROOT/'model-lock-2026-10-31.json'
def main():
 lock=json.loads(MANIFEST.read_text());errors=[]
 for name,expected in lock['sha256'].items():
  path=ROOT/name
  if not path.is_file():errors.append('Missing: '+name)
  elif hashlib.sha256(path.read_bytes()).hexdigest()!=expected:errors.append('Changed: '+name)
 if errors:
  print('\n'.join(errors));return 1
 from predictor_reporting_v2 import Model
 m=Model();assert m.backend==lock['default_backend']=='v28'
 rows=json.loads((ROOT/lock['evidence_targets']).read_text())['rows']
 assert len(rows)==691 and len({tuple(sorted((tuple(q['a']),tuple(q['b'])))) for q in rows})==691
 assert sum(q['known_direction'] is not None for q in rows)==509
 assert sum(q['materiality_target'] is not None for q in rows)==453
 assert sum(q.get('exact_price_equality') is True for q in rows)==4
 print(f"PASS: {len(lock['sha256'])} artifact hashes; V28 default; 691 unique evidence pairs and label counts verified.")
 return 0
if __name__=='__main__':sys.exit(main())
