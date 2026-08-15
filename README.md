# RIO Affiliate Engine — Phase 2

India-focused affiliate content engine for compact-home and Home/Kitchen buying guides.

## Current status
- Static site: deployment-ready
- Commercial content frameworks: 3 published locally, 7 queued
- Affiliate disclosure: implemented site-wide and as a dedicated policy page
- Editorial policy and privacy notice: implemented
- Offer registry: real-link placeholders only; no fabricated affiliate IDs or URLs
- Tracking: local click-intent event capture only; no external analytics active
- CI: GitHub Actions validation workflow prepared
- Public deployment: **not activated** (founder publishing gate remains in force)
- Affiliate account/link insertion: pending founder account authorization and current merchant verification

## Run locally
```bash
python3 -m http.server 8000 --directory site
```
Then open `http://localhost:8000`.

## Validate
```bash
python3 scripts/validate.py
python3 tests/test_economics.py
```

## Security
Never commit passwords, API keys, tokens, affiliate secret credentials, card/bank data or government ID data. `.gitignore` blocks common local secret-file patterns, but secrets must remain outside the repository.

## Publication gate
The site is prepared for deployment, but no public deployment workflow is included yet. Public publication requires explicit founder approval under the RIO operating model.
