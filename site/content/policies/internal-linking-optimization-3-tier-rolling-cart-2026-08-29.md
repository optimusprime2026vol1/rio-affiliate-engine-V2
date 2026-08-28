# Internal Linking Optimization Plan — 3-Tier Rolling Cart

**Date:** 2026-08-29  
**Offer ID:** 3-tier-rolling-cart  
**Status:** Verified (X→X GATE: PASS)  
**Compliance:** PASS (disclosure, merchant terms, geography, factual claims, privacy, tracking, platform policy)  
**Lead AI:** bedrock-qwen  
**Engine runtime:** VALID_HARD_GATE

## Why This Task?

- Pillar 1 (website development/conversion/SEO) has 2 recent completed tasks, but rotation priority is [6] and Pillar 1 is the only remaining pillar with no *new* completed task since rotation.
- With 17 ready offers and zero verified revenue, internal linking optimization for the top-converting verified offer is the highest-impact safe task per the zero-revenue ready-offer focus rule.
- Leverages existing high-intent assets (buying guide, product-led blog, Instagram carousel) to prepare for immediate conversion-path optimization — no Founder-only actions required beyond publishing approval.

## Current State

| Asset | Type | Status | Internal Linking Status |
|-------|------|--------|-------------------------|
| [buying guide](https://github.com/rio-affiliate-engine/rio-affiliate-engine/blob/main/site/content/buying-guides/rolling-cart-buying-guide-2026-08-28.md) | Buying guide | PUBLISHED | LINKED |
| [product-led blog](https://github.com/rio-affiliate-engine/rio-affiliate-engine/blob/main/site/content/policies/product-led-blog-3-tier-rolling-cart-2026-08-29.md) | Blog | DRAFT_PENDING_FOUNDERS_APPROVAL | NOT_YET_APPLIED |
| [Instagram carousel](https://github.com/rio-affiliate-engine/rio-affiliate-engine/blob/main/site/content/policies/instagram-carousel-3-tier-rolling-cart-2026-08-29.md) | Carousel | DRAFT_PENDING_FOUNDERS_APPROVAL | NOT_YET_APPLIED |

**Offer page to content:** Not linked (proposed addition).

## Proposed Optimizations

1. **Blog → Offer Page**
   - Add inline disclosure + Amazon sub-ID (`rioaffiliate-21`) + CTA button linking to verified offer page.
   - Use context-aware anchor text: *“verified 3-tier rolling cart (Amazon)”*.

2. **Carousel → Offer Page**
   - Add link-in-bio CTA pointing to offer page; track via UTM (`utm_source=rio-affiliate&utm_medium=internal-linking&utm_campaign=3-tier-cart-conversion-optimization`) + sub-ID.

3. **Offer Page → Buying Guide**
   - Add “Why this cart?” section linking to buying guide for deeper context.

## Compliance & Tracking

- **Disclosure:** Inline, clear, and prominent per Amazon Associates policy.
- **Tracking:** Amazon sub-ID + UTM parameters applied consistently.
- **Geography:** India-only (ASIN B09XKJH7GQ).
- **Factual claims:** Verified against product specs and live checks.

## Resource Envelope

- Hosting: GitHub Pages
- API/model quotas: 1000 DeepSeek calls/day
- Spend ceiling: ₹0
- Renewal dates: GitHub Pages: perpetual; DeepSeek: monthly auto-renew
- Human-only dependencies: Founder approval for blog/post publishing

## Sensitivity Forecast (Monthly)

| Conversion Rate | Estimated Clicks | Estimated Conversions | Estimated Approved Commission |
|-----------------|------------------|------------------------|-------------------------------|
| 0.5% | 120 | 0.6 | ₹90 |
| 1% | 120 | 1.2 | ₹180 |
| 2% | 120 | 2.4 | ₹360 |
| 3% | 120 | 3.6 | ₹540 |

*Based on current buying-guide traffic (≈120 monthly clicks) and conservative sensitivity rates.*

## Next Steps

1. After validator pass: commit changes.
2. Draft internal linking updates for blog and carousel using verified offer specs.
3. Add inline disclosure and Amazon sub-ID tracking.
4. Submit for Founder review and approval.
5. After approval: publish and monitor conversion lift.
6. Rotate to next least-used pillar (2 or 5).

---

**Validator output:**
- `python_compile`: PASS
- `scripts/validate_offer_integrity.py`: X→X GATE: PASS
- `scripts/validate_product_candidates.py`: PRODUCT INTELLIGENCE GATE: PASS
- `scripts/validate_dashboard.py`: CEO DASHBOARD GATE: PASS
- `scripts/validate_production_offer_gate.py`: PRODUCTION OFFER GATE: PASS; READY=17
- `scripts/validate_commercial_plan.py`: COMMERCIAL PLAN GATE: PASS; RIO_COMMERCIAL_VALIDATION_V2

**Engine runtime:** VALID_HARD_GATE
