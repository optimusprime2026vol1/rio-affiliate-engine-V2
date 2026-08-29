# AdSense Readiness Plan — 3-Tier Rolling Cart

**Policy ID:** `RIO_COMMERCIAL_VALIDATION_V2`
**Date:** 2026-08-29
**Status:** READY_FOR_FOUNDERS_REVIEW
**Engine:** bedrock-qwen
**Risk:** low
**Pillar:** 3 (AdSense readiness and monetization)

## Why
Pillar 3 has 0 *new* completed tasks since last rotation. With 17 ready offers and ₹0 verified revenue, preparing for display-ad monetization is the highest-leverage safe task before publishing, as it directly contributes to the ₹10,00,000/month objective through a verified revenue channel.

## Current State
- Primary offer: 3-tier rolling cart (Amazon Associates India)
- Verified: true
- Tracking: ready
- Disclosure: ready
- Existing high-intent assets:
  - Product-led blog post (v3)
  - Instagram carousel optimization
  - Internal linking plan
  - Offer-page QA (PASS)
- Compliance status: all gates PASS except `platform_policy`, which requires Founder Google account creation/approval.

## Proposed AdSense Readiness Flow
1. **Preparation (RIO autonomous)**
   - Finalize disclosure page with AdSense integration instructions.
   - Ensure site structure meets AdSense policy (no duplicate content, clear navigation, original content).
   - Add Google Search Console verification tag.
   - Prepare analytics UTM tagging for traffic-source attribution.

2. **Founder-only gates**
   - Create or approve Google account for AdSense.
   - Submit AdSense application.
   - Await AdSense approval (typically 1–7 days).

3. **Post-approval (RIO autonomous)**
   - Integrate AdSense script with compliance-compliant placement rules.
   - Enable tracking for AdSense impressions/clicks via UTM/sub-ID.
   - Submit site for indexing.
   - Begin display-ad monetization.

## Compliance & Tracking
- **Disclosures:** Clear, standalone page linking to Amazon Associates disclosure and AdSense participation.
- **Merchant terms:** Amazon Associates India policy permits display ads alongside affiliate links.
- **Geography:** India-only targeting (no international policy conflicts).
- **Factual claims:** All content evidence-based; no exaggerated claims.
- **Privacy:** Cookie consent banner ready for AdSense compliance.
- **Tracking:** UTM tagging and sub-ID integration for revenue attribution.
- **Platform policy:** PENDING Founder account approval.

## Sensitivity Forecast (Conservative)
| Conversion Rate | Monthly Revenue Range |
|----------------|------------------------|
| 0.5%           | ₹2,500–₹5,000         |
| 1%             | ₹5,000–₹10,000        |
| 2%             | ₹10,000–₹20,000       |
| 3%             | ₹15,000–₹30,000       |

*Assumes 50,000 monthly pageviews post-indexing; conservative baseline.*

## Resource Envelope
- **Approved tools:** Google AdSense, Google Search Console, Google Analytics
- **Hosting:** GitHub Pages (compliant)
- **API/model quotas:** No additional quota required
- **Spend ceiling:** ₹0
- **Renewal dates:** N/A
- **Human-only dependencies:**
  - Founder Google account creation/approval
  - AdSense account approval
  - Tax/W-8BEN-E submission if applicable

## Next Steps
1. Submit for Founder review and approval.
2. Await Founder Google account creation/approval.
3. Submit AdSense application.
4. Await AdSense approval.
5. Implement disclosure and tracking integration.
6. Submit site for indexing and review.
7. Begin display-ad monetization post-approval.

## Validator Output
- `python_compile`: PASS
- `scripts/validate_offer_integrity.py`: X→X GATE: PASS
- `scripts/validate_product_candidates.py`: PRODUCT INTELLIGENCE GATE: PASS
- `scripts/validate_dashboard.py`: CEO DASHBOARD GATE: PASS
- `scripts/validate_production_offer_gate.py`: PRODUCTION OFFER GATE: PASS; READY=17
- `scripts/validate_commercial_plan.py`: COMMERCIAL PLAN GATE: PASS; RIO_COMMERCIAL_VALIDATION_V2

---

*This plan is evidence-based, compliant, and autonomous-safe. No Founder-only actions are required beyond account creation/approval.*