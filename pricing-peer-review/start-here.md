# Pricing peer review packet

Start with `pricing-peer-review.md`. It defines the review scope, mathematics, evidence,
known limitations and requested verdict. Then read `pricing/domestic-release-reference-v2.md`.

The current subject is the separate locked Domestic Release Pricing v2 layer, not another
attempt to tune comparative V28. Older comparison experiments are included as dependencies
and context. Their presence does not authorize rerunning fits or treating them as current.

All project files retain their original paths and bytes. The33-artifact pricing lock and
46-artifact comparative lock are unchanged. `packet-manifest.json` hashes all payload files
except itself. Run `python verify_packet.py` to check archive integrity after extraction.

From this directory in a suitable isolated Python environment:

```sh
PYTHONDONTWRITEBYTECODE=1 python verify_packet.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python pricing/verify_pricing_lock.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python verify_model_lock.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python pricing/test_consistent_pricing_v2.py -v
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python -m unittest test_reporting test_reporting_v2 -q
```

`requirements-review.txt` lists the numerical-library versions used for the packet smoke
test; no virtual environment is bundled. The XLSX files are read-only review artifacts,
already recalculated; do not run export/calibration scripts that rewrite their outputs.
Original Mac paths in documentation are historical; use this extracted root.

Keep the packet read-only. Return your review as Markdown and optional small diagnostic
receipts outside the packet. Nothing has been uploaded publicly by creating this ZIP.

Main distinction: consistency and monotonicity are verified computational properties.
Prices are anchored by four initial-release offers plus expert judgments, not independent
transaction data. Both the original estimates and later endorsements are included.
