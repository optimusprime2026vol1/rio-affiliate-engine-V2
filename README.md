# RIO Affiliate Engine — Version 3.0

India-focused affiliate content and authority engine.

## Locked objective (RIO 3.0)

Build an automated, scalable affiliate business toward **₹10 lakh/month net approved commission**, with a long-term ₹50 lakh+/month goal.

**Primary positioning**:
Help Indian interior designers, contractors, and small offices use AI tools and practical digital products to design faster, present better, and manage projects more efficiently.

**Supporting layer** (already live):
Compact-home storage, kitchen/bathroom/wardrobe/balcony organisers, and baby-proofing/home-safety products for Indian rented homes.

Core discipline remains unchanged: **Discovery → Live-verify → Score → Publish**. Nothing goes live without real verification.

Full definition: `data/RIO_3.0_DEFINITION.md`

## Evidence-backed status

The repository currently contains:

- 27 content items
- 35 product candidates: 17 READY, others in discovery/rejected
- 17 Amazon.in offers marked READY with tracking ID `rioaffiliate-21`
- A heartbeat with real production reachability plus validators
- Daily content QA and product-discovery suggestions
- Founder-approved Instagram publishing (currently blocked on token)

Do not call the system earning from local validators alone. Current truth is stored in:

- `data/status.json` — heartbeat and validator state
- `data/production_status.json` — real HTTP checks
- `data/dashboard_snapshot.json` — pipeline counts
- `data/content_review_report.json` — content trust assessment
- `data/ig_published.json` — confirmed Instagram media IDs only
- `data/instagram_approval.json` — Founder approval and per-offer publish state
- `data/instagram_run_status.json` — latest real publish outcome or blocker
- `data/RIO_3.0_DEFINITION.md` — Version 3.0 objective and initial workflow

## Validate locally

```bash
python3 scripts/validate.py
python3 scripts/validate_offer_integrity.py
python3 scripts/validate_product_candidates.py
python3 scripts/validate_dashboard.py
python3 scripts/validate_production_offer_gate.py
```

## Verify production

```bash
python3 scripts/check_production.py
```

Set `RIO_PUBLIC_SITE_BASE` when a different public deployment URL is selected.

## Security and compliance

- Never commit passwords, API keys, tokens, payment data, government IDs or private customer/order data.
- Amazon links must carry the approved tracking ID.
- Customer review text and star ratings must not be published without an approved Amazon Product Advertising API source and its license requirements.
- Revenue remains ₹0 until a real Associates report proves approved commission.
- Paid promotion requires explicit Founder budget approval.
- No Founder name or professional claim goes public without explicit review and sign-off.
