# RIO Affiliate Engine — Phase 2

India-focused affiliate content engine for compact-home and Home/Kitchen buying guides.

## Current status
- Static site: **live and public** — https://vickykenin-lang.github.io/rio-affiliate-engine/ (auto-deployed on every push to main via .github/workflows/deploy-pages.yml, after all 4 commercial validators pass)
- 27 buying-guide articles published, real Amazon.in affiliate links live and tag-verified (tag=rioaffiliate-21) on spot-checked articles across kitchen/bathroom/storage/wardrobe categories
- Affiliate disclosure: implemented site-wide and as a dedicated policy page
- Editorial policy and privacy notice: implemented
- Affiliate account: Amazon Associates India account live (Store ID rioaffiliate-21, tax status Completed) since 2026-08-16
- Tracking: local click-intent event capture only; no external analytics active yet
- CI: GitHub Actions validation workflow live (validate on every push, before deploy) + a heartbeat (scripts/heartbeat.py, every 30 min) that regenerates the CEO dashboard and re-runs all 4 validators
- Public deployment: **ACTIVATED 2026-08-17** by Vicky's explicit go-ahead (previously gated; see git history for the full authorization trail)
- robots.txt / sitemap.xml / meta robots are all indexing-friendly — no known SEO blockers as of 2026-08-17

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

**Public deployment is live** (activated 2026-08-17, Vicky's explicit go-ahead). The site auto-deploys via GitHub Actions on every push to main, gated behind the 4 commercial validators (scripts/validate_offer_integrity.py, validate_product_candidates.py, validate_dashboard.py, validate_production_offer_gate.py) — nothing publishes if any of those fail.

Paid advertising (Google Ads, Meta Ads, etc.) is a separate gate and remains founder-only: no ad account, ad spend, or campaign goes live without Vicky's explicit budget sign-off (see RIO_OPERATING_AGENT_BRIEF.md Section 5/7). Organic social distribution (Instagram/Pinterest/Telegram) needs those accounts created by Vicky first — RIO's operating agent cannot create accounts or hold credentials.
