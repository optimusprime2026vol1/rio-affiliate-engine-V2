# Flipkart Integration Execution Plan — 2026-08-29

**Policy ID:** `RIO_FLIPKART_INTEGRATION_V1`
**Status:** READY FOR EXECUTION (Founder account pending)
**Phase:** Phase 2 — conversion-focused content using verified offers

## 1. Objective
Create conversion-ready content for Flipkart offers using existing verified specs, audience-fit framing, and internal linking — no new discovery or Founder-only actions required beyond future account setup.

## 2. Readiness Summary
- **Ready offers:** 17 (all Amazon Associates India, verified)
- **Target product:** 3-tier rolling cart (verified specs, audience-fit framing, internal linking candidates, Instagram carousel)
- **Compliance checks:** Disclosure, geography, factual claims, privacy = PASS; merchant terms, tracking, platform policy = PENDING_FOUNDER_ACCOUNT
- **Resource envelope:** No additional spend; uses existing site generator and verified specs
- **Conversion sensitivity forecast:** ₹2.5k–₹30k/month depending on conversion rate (0.5%–3%)

## 3. Immediate Execution Tasks
1. **Draft Flipkart-specific offer page**
   - Use verified specs from `data/verified_offers.json`
   - Apply disclosure template (`site/content/policies/disclosure-template.md`)
   - Include internal links from existing buying guide and Instagram carousel
   - Add Flipkart pixel integration note (Founder account required)

2. **Add internal linking**
   - From `site/content/buying-guides/3-tier-rolling-cart-indian-designers-2026-08-28.md`
   - From `site/content/instagram/carousels/3-tier-rolling-cart-indian-designers-2026-08-28.md`
   - Link text: "Available on Flipkart (pending account setup)"

3. **Create Flipkart offer content template**
   - Reusable structure for future Flipkart offers
   - Includes verified specs, disclosure, internal linking, pixel note

## 4. Impact & Next Steps
- **Expected impact:** High-readiness conversion content using existing assets
- **Next task after execution:** Commit changes, propose 2–3 immediate fix tasks (disclosure page draft, internal linking, Instagram carousel draft), and rotate to next least-used pillar (3 or 6).

## 5. Compliance & Gates
- **Hard pass/fail compliance checks:** Disclosure, geography, factual claims, privacy = PASS; merchant terms, tracking, platform policy = PENDING_FOUNDER_ACCOUNT
- **No Founder-only actions required for this task**
- **Two failed niche pilots trigger mandatory Dr. Victor strategy review before third niche**

## 6. Resource Envelope
- Approved tools: existing site generator, verified offer specs
- Hosting: current site infrastructure
- API/model quotas: DeepSeek/Bedrock quota available
- Spend ceiling: ₹0 additional spend required
- Renewal dates: none applicable
- Human-only dependencies: Founder Flipkart account setup, payment/tax onboarding

---
*Policy locked per RIO 3.0 Phase-2 autonomous execution pillars and Commercial Validation Policy v2.*