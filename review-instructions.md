# Begin the independent pricing peer review

Read `pricing-peer-review/pricing-peer-review.md` for the full mathematical review request,
then `pricing-peer-review/pricing/domestic-release-reference-v2.md` and both lock manifests.
Treat paths in the full prompt as relative to `pricing-peer-review/`, not the repository root.
Original absolute Mac workspace paths are historical context, not prerequisites.

Independently challenge the price mathematics, calibration, anchor assumptions, regional
transfer, validation methodology and operational scope. Distinguish structural consistency
from accurate market prices and post-disclosure expert endorsement from independent evidence.
Recommend retention, narrower use, or up to three justified, falsifiable experiments.
A recommendation to retain the current lock is acceptable; do not force a new model idea.

## Verification

From the `pricing-peer-review/` directory, in a suitable isolated Python environment:

```sh
PYTHONDONTWRITEBYTECODE=1 python verify_packet.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python pricing/verify_pricing_lock.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python verify_model_lock.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python pricing/test_consistent_pricing_v2.py -v
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python -m unittest test_reporting test_reporting_v2 -q
```

See `requirements-review.txt` inside the packet. The original virtual environment is not
included. All33pricinghashes,46comparativehashes,14pricingtests and9reportingtests passed
before publication. Report what you actually reproduce rather than copying these claims.

## Boundaries and submission

Keep every input under `pricing-peer-review/`, both lock manifests and the ZIP unchanged.
Do not refit, edit labels, alter configurations or run export scripts that overwrite inputs.
Read-only diagnostics and isolated environment setup for verification are permitted.

Write your review to `reviews/YYYY-MM-DD-reviewer.md`, with small diagnostic receipts or
scripts under `reviews/YYYY-MM-DD-reviewer/`. Include the commit reviewed, packet checksum,
files inspected, checks executed, ranked findings, recommendations and limitations. No secrets,
credentials or local environment files in the submission.

Create a branch, commit only review outputs, push, and open a pull request against `main`.
If you lack write access, fork the repository and open a pull request from your fork. Do not
merge your own PR. Preserve review history through follow-up commits and PR discussion.
Follow your harness's normal author-attribution requirements.

If upload is unavailable, finish the review and return Markdown plus supporting attachments;
briefly explain the tool/access limitation. Do not claim publication without a receipt. End
with the PR URL when submitted. Do not request tokens in chat or bypass repository permissions.
