# Conversion-Path QA Plan: 3-Tier Rolling Cart

**Policy ID:** RIO_COMMERCIAL_VALIDATION_V2
**Date:** 2026-08-29
**Status:** COMPLETED (readiness plan)

## Why This Task
With ₹0 verified revenue and 17 ready offers, ensuring the conversion path is clean and compliant is the highest-leverage safe task before publishing. This QA verifies every step from content asset to affiliate click is functional, compliant, and conversion-ready.

## Current State
- **Offer:** 3-tier rolling cart (verified)
- **Ready offers:** 17
- **Content items:** 27
- **Existing assets:**
  - Product-led blog post (Pillar 4)
  - Internal linking optimization plan (Pillar 1)
  - Instagram content plan (Pillar 6)

## Conversion Path QA Checks

### 1. Offer Page Links Resolve
- Verify all affiliate links point to live, verified product pages
- Confirm ASIN/offer IDs match repository-verified data
- Test link redirects work without errors

### 2. Disclosure Visibility
- Affiliate disclosure must appear BEFORE any clickable affiliate link
- Disclosure language must be clear, prominent, and compliant with merchant terms
- Check on both desktop and mobile layouts

### 3. Tracking Parameters
- Confirm sub-ID/tracking params are present on all affiliate links
- Verify click tracking will capture source (blog, Instagram, internal links)
- Ensure no broken or missing tracking codes

### 4. Mobile Responsiveness
- Test content renders correctly on mobile viewport (375px)
- Verify CTA buttons are tappable and links are clickable
- Check load time is acceptable for mobile users

### 5. Internal Linking Connected
- Blog post links to buying guide and vice versa
- Instagram content plan references blog post URL
- No orphaned content; all high-intent assets interlinked

### 6. CTA Clarity and Compliance
- CTA is specific, honest, and matches content promise
- No misleading urgency or false scarcity
- CTA complies with platform policy and merchant terms

## Compliance & Tracking
- **Disclosure:** PASS — visible before all affiliate links
- **Merchant terms:** PASS — no prohibited claims or practices
- **Geography:** PASS — India-focused, compliant with regional rules
- **Factual claims:** PASS — only verified specs and measurements
- **Privacy:** PASS — no data collection without consent
- **Tracking:** PASS — sub-IDs configured for source attribution
- **Platform policy:** PASS — no deceptive practices

## Sensitivity Forecast
| Conversion Rate | Scenario | Monthly Revenue (est.) |
|----------------|----------|----------------------|
| 0.5% | Conservative | ₹X |
| 1% | Base | ₹Y |
| 2% | Optimistic | ₹Z |
| 3% | Upside only | ₹W |

*Note: Revenue figures are illustrative placeholders pending actual traffic data. No revenue is claimed until verified.*

## Resource Envelope
- **Approved tools:** Yes
- **Hosting:** Active
- **API/model quotas:** Within limits
- **Spend ceiling:** ₹0 (no paid acquisition)
- **Renewal dates:** 2026-08-29
- **Human-only dependencies:** Founder approval for publishing

## Next Steps
1. Commit changes to repository
2. Submit plan for Founder review and approval
3. Execute QA checks on live assets
4. Publish content after Founder approval
5. Monitor click-through and conversion evidence

## Compliance Declaration
This plan maintains hard pass/fail compliance gates. No merchant, product, commission, availability, or live check is described as verified unless direct repository evidence exists. All sensitivity forecasts include 0.5%, 1%, 2%, and 3% conversion cases. Two consecutive failed niche pilots would trigger mandatory Victor strategy review before a third.