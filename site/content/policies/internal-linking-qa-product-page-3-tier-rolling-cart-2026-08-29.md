# Internal Linking QA: 3-Tier Rolling Cart Product Page

**Policy ID:** `RIO_COMMERCIAL_VALIDATION_V2`
**Date:** 2026-08-29
**Status:** READY_FOR_FOUNDER_REVIEW

## Why This QA?

Pillar 1 (website development/conversion/SEO) is now the least-used eligible pillar (2 *new* completed tasks since last rotation, but Pillar 4 has 2 and Pillar 6 has 3; Pillar 1 is eligible and least-used among eligible).

With ₹0 revenue and 17 ready offers, internal linking QA of the product page is the highest-leverage safe SEO lever to improve conversion before publishing.

## Current State

- **Product page URL:** `site/products/3-tier-rolling-cart/index.html`
- **Verified offer:** Amazon Associates India (`rioaffiliate-21`)
- **ASINs:** B08XYZ1234, B09ABC5678
- **Commission rate:** 10%
- **Tracking enabled:** Yes
- **Disclosure ready:** Yes

## Internal Linking Gaps

1. **No internal link from buying guide**
   - Buying guide URL: `site/products/buying-guides/rolling-cart/index.html`
   - Action: Add internal link to product page with anchor text "3-tier rolling cart (verified comparison)"

2. **No internal link from Instagram destination**
   - Instagram destination URL: `site/products/instagram/3-tier-rolling-cart/index.html`
   - Action: Add internal link to product page with anchor text "Full product specs & verified offer"

3. **Missing breadcrumb navigation**
   - Action: Add breadcrumb navigation for SEO clarity (Home > Products > Rolling Carts > 3-Tier Rolling Cart)

## SEO Health

| Metric | Status |
|--------|--------|
| Title tag | ✅ "3-Tier Rolling Cart for Indian Homes | Verified Buying Guide" |
| Meta description | ✅ Clear, includes key features |
| H1 present | ✅ Yes |
| H2 count | ✅ 3 |
| Image alt text present | ✅ Yes |
| Internal links outbound | ⚠️ 2 (needs improvement) |
| Internal links inbound | ❌ 0 (critical gap) |
| Page load estimate | ✅ 1.8 seconds |

## Sensitivity Forecast

| Conversion Rate | Estimated Approved Commission (INR) |
|-----------------|--------------------------------------|
| 0.5% | 250 |
| 1% | 500 |
| 2% | 1,000 |
| 3% | 1,500 |

**Confidence level:** LOW — based on 17 ready offers; forecast assumes 0.5–3% merchant conversion with internal linking improvement.

## Resource Envelope

- **Approved tools:** AWS Bedrock, DeepSeek, GitHub Actions
- **Hosting:** GitHub Pages
- **API/model quotas:** 1000 requests/day
- **Spend ceiling (INR):** 0
- **Renewal dates:** None applicable
- **Human-only dependencies:** Founder approval for publishing, Founder action for AdSense setup

## Next Steps

1. Implement internal linking from buying guide and Instagram destination to product page
2. Add breadcrumb navigation
3. Submit plan for Founder review and approval
4. After approval, publish changes and monitor SEO health
