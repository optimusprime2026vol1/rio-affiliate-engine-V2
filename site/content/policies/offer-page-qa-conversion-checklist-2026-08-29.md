# Offer-Page QA and Conversion-Path Optimization Checklist

**Date:** 2026-08-29
**Pillar:** 1 (Website Development/Conversion/SEO)
**Policy:** RIO_COMMERCIAL_VALIDATION_V2 (ACTIVE_GOVERNED)

## Why This Task

With 17 verified ready offers and zero verified revenue, the highest-impact safe task is optimizing the conversion path for existing verified offers. The 3-tier rolling cart is the top verified offer with existing high-intent assets (buying guide, internal linking strategy, Instagram carousel). This QA checklist ensures the offer page is conversion-ready before driving traffic.

## Target Offer

- **Product:** 3-tier rolling cart
- **Verification Status:** VERIFIED (repository evidence present)
- **Existing Assets:**
  - Buying guide: `site/content/buying-guide-3-tier-rolling-cart.md`
  - Internal linking: `data/internal_linking_state.json`
  - Instagram carousel: `site/content/policies/instagram-carousel-3-tier-rolling-cart-2026-08-29.md`

## Compliance Gate (HARD PASS/FAIL)

All checks must pass before promotion:

1. **Disclosure** — Affiliate disclosure visible above the fold
2. **Merchant Terms** — Amazon Associates India terms respected
3. **Geography** — India-only targeting
4. **Factual Claims** — All claims verified against merchant listing
5. **Privacy** — Privacy policy present and linked
6. **Tracking** — Sub-ID tracking aligned with campaign
7. **Platform Policy** — No policy violations

## QA Checklist

### Content Integrity
- [ ] Product title matches merchant listing exactly
- [ ] Price and availability current (re-verify within 24h of publish)
- [ ] No fabricated ratings, reviews, or claims
- [ ] Images match actual product

### Conversion Path
- [ ] Affiliate link has sub-ID tracking parameter
- [ ] CTA buttons clear, above the fold, mobile-friendly
- [ ] Page loads under 3 seconds
- [ ] Mobile responsive layout confirmed
- [ ] Internal links to related high-intent content present

### SEO
- [ ] Title tag includes target keyword
- [ ] Meta description compelling and accurate
- [ ] Alt text on all images
- [ ] Schema markup for product (if applicable)

## Sensitivity Forecast (ESTIMATE ONLY — NOT VERIFIED REVENUE)

| Conversion Rate | Monthly Visitors | Monthly Commissions (INR) |
|----------------|-----------------|--------------------------|
| 0.5% | 1,000 | 500 |
| 1% | 1,000 | 1,000 |
| 2% | 1,000 | 2,000 |
| 3% | 1,000 | 3,000 |

**Note:** These are planning estimates only. No revenue is verified until approved commission settlement occurs.

## Resource Envelope

- **Approved Tools:** GitHub Actions, AWS Bedrock, Telegram webhook
- **Hosting:** GitHub Pages
- **API/Model Quotas:** Within limits
- **Spend Ceiling:** ₹0 (no paid acquisition)
- **Renewal Dates:** 2026-09-01
- **Human-Only Dependencies:** Amazon account verification, AdSense approval

## Next Steps

1. Run QA checklist on live offer page
2. Fix any QA failures immediately
3. Submit Founder request for Amazon account verification
4. Rotate to next least-used pillar

## Evidence Standards

- No merchant, product, commission, availability, or live check described as verified unless repository context contains direct evidence
- All forecasts labeled as estimates, not verified revenue
- Compliance is hard pass/fail — no commercial strength can offset compliance failure