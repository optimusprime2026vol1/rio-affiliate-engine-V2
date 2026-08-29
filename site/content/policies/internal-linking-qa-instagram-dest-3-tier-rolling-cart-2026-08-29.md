# Internal Linking QA — Instagram Destination Page

**Policy ID:** `RIO_COMMERCIAL_VALIDATION_V2`
**Date:** 2026-08-29
**Offer:** 3-tier rolling cart (Amazon Associates India)
**Status:** READY_FOR_FOUNDER_REVIEW

## Why
Instagram posts will drive traffic to a dedicated destination page. Internal linking QA ensures the destination page is conversion-ready, SEO-optimized, and connected to existing high-traffic assets before publishing.

With ₹0 revenue and 17 ready offers, internal linking is the highest-leverage safe SEO lever to improve conversion before publishing.

## Current State
- Instagram content plan approved (2026-08-29)
- Destination page URL: `/instagram/3-tier-rolling-cart`
- Offer specs verified: Amazon Associates India, tracking ID `rioaffiliate-21`
- Commission rate: ₹800 per verified order

## Internal Linking Gaps
1. No internal link from existing high-traffic pages to Instagram destination
2. No breadcrumb navigation to Instagram destination on offer landing page
3. Instagram destination lacks canonical tag pointing to main offer page

## SEO Health
- Title tag: ✅ Present, descriptive
- Meta description: ✅ Present, includes key terms
- H1: ✅ Present
- H2 count: 3
- Internal links out: 0
- Internal links in: 0
- Canonical tag: ❌ Missing

## Sensitivity Forecast
| Conversion Rate | Estimated Approved Commission (INR) |
|-----------------|-------------------------------------|
| 0.5%            | 400                                 |
| 1%              | 800                                 |
| 2%              | 1,600                               |
| 3%              | 2,400                               |

**Confidence:** LOW — assumes Instagram traffic reaches destination page.

## Resource Envelope
- Approved tools: GitHub Actions, AWS Bedrock, DeepSeek
- Hosting: GitHub Pages
- API/model quotas: bedrock-qwen primary, deepseek-chat fallback
- Spend ceiling: ₹0
- Renewal dates: none applicable
- Human-only dependencies: Founder approval for publishing, Founder review of internal linking plan

## Next Steps
1. Commit changes after validator pass
2. Submit plan for Founder review and approval
3. After approval, add internal links from high-traffic pages to Instagram destination
4. Add canonical tag and breadcrumb navigation to Instagram destination page
5. Rotate to Pillar 6 (Instagram sales/content execution) for scheduling 3 Instagram posts (hook, problem/solution, CTA)
