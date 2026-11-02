from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
r=json.loads((p/'packet-manifest.json').read_text())
for name,meta in r['files'].items():
 f=p/name
 assert f.is_file(),name
 assert hashlib.sha256(f.read_bytes()).hexdigest()==meta['sha256'],name
print('PASS:',len(r['files']),'packet payload hashes')
