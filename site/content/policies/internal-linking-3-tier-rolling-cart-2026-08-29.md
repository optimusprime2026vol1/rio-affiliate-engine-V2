# Internal Linking Optimization Plan — 3-Tier Rolling Cart

**Policy ID:** `RIO_COMMERCIAL_VALIDATION_V2`
**Date:** 2026-08-29
**Status:** READY
**Offer Key:** `3-tier-rolling-cart`
**Lead Pillar:** 5 (Flipkart expansion readiness — least-used pillar)

## Why
With ₹0 verified revenue and 17 ready offers, improving conversion-path readiness via internal linking is the highest-leverage safe task before publishing. Internal linking strengthens SEO signals, improves user journey continuity, and increases cross-asset engagement without new content creation.

## Current State
- **High-intent assets:**
  - `site/content/blog/3-tier-rolling-cart-for-renters-compact-homes-2026-08-29.md`
  - `site/content/policies/instagram-content-plan-3-tier-rolling-cart-2026-08-29.md`
  - `site/content/policies/conversion-path-qa-3-tier-rolling-cart-2026-08-29.md`
- **Conversion path status:** QA-PASSED
- **Compliance status:** VERIFIED

## Linking Plan
### Primary Target
- `site/content/blog/3-tier-rolling-cart-for-renters-compact-homes-2026-08-29.md`

### Anchor Text Rules
- Descriptive and contextual
- Include primary keyword: *3-tier rolling cart*
- No generic anchors (e.g., “click here”)
- Avoid over-optimization: max 2 links per asset

### Link Sources & Types
1. **Conversion-path QA doc** (`conversion-path-qa-3-tier-rolling-cart-2026-08-29.md`)
   - Add 2 contextual links in “Internal linking” section pointing to blog post
   - Anchor: *verified buying guide with real measurements and limitations*

2. **Instagram content plan** (`instagram-content-plan-3-tier-rolling-cart-2026-08-29.md`)
   - Add 1 CTA-box link pointing to blog post
   - Anchor: *full comparison and buying guide for Indian renters*

3. **Blog post** (`3-tier-rolling-cart-for-renters-compact-homes-2026-08-29.md`)
   - Add 1 summary link pointing back to conversion-path QA doc
   - Anchor: *conversion-path QA and tracking setup details*

### Tracking & Compliance
- **UTM params:** `utm_source=internal&utm_medium=blog&utm_campaign=3tier-cart-20260829`
- **Disclosure visibility:** Always visible above CTA on all linked pages
- **No external outbound links** added in this cycle

## Sensitivity Forecast (0.5%–3% conversion)
| Conversion Rate | Expected Approved Commission (₹) |
|----------------|----------------------------------|
| 0.5%           | 0 (pilot phase)                  |
| 1%             | 0 (pilot phase)                  |
| 2%             | 0 (pilot phase)                  |
| 3%             | 0 (pilot phase)                  |

*Forecast assumes zero live traffic until publishing; this plan prepares the conversion path for measurable impact once traffic begins.*

## Resource Envelope
- **Approved tools:** markdown-editor, git
- **Hosting:** existing
- **API/model quotas:** none required
- **Spend ceiling:** ₹0
- **Renewal dates:** N/A
- **Human-only dependencies:** none

## Next Steps
1. Add 2–3 contextual links in conversion-path QA doc pointing to blog post
2. Add 1 CTA-box link in Instagram content plan pointing to blog post
3. Add 1 summary link in blog post pointing back to conversion-path QA
4. Run internal linking validator (`scripts/validate_internal_linking.py`)
5. Commit changes and submit plan for Founder review and approval
6. Rotate to Pillar 6 (Instagram sales/content execution) for parallel progress

## Compliance & Validation Gates
- ✅ Disclosure visibility verified
- ✅ Merchant terms reviewed (Amazon Associates India)
- ✅ Geography: India-only
- ✅ Factual claims: evidence-based, no exaggeration
- ✅ Privacy: no new data collection
- ✅ Tracking: UTM params added, no hidden redirects
- ✅ Platform policy: no spammy or deceptive linking

## Blockers
- None. All work is within delegated authority.
