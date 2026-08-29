# Flipkart Integration Plan — RIO 3.0

**Policy ID:** `RIO_COMMERCIAL_VALIDATION_V2`
**Status:** DRAFT — pending Founder review and approval
**Date:** 2026-08-29
**Lead AI:** DeepSeek

## Why Flipkart?

- **Audience fit:** Flipkart is the #1 e-commerce platform for Indian interior designers, contractors, and home professionals (per 2025 industry reports).
- **Product alignment:** High-intent categories (storage, organization, office furniture) overlap directly with the 3-tier rolling cart offer.
- **Commission potential:** Verified Flipkart offers typically pay 3–8% on home/office categories, with higher ticket sizes than Amazon in some segments.
- **Diversification:** Reduces merchant concentration risk before scaling.

## Current State

- **Ready offers:** 17 (Amazon India only)
- **Verified offer:** 3-tier rolling cart (Amazon India, 4% commission, verified tracking)
- **Content assets:** 27 items; 3 high-intent assets directly support rolling-cart intent
- **Compliance status:** Disclosure, factual claims, privacy, and tracking are verified; Flipkart-specific terms and account approval are pending

## Compliance & Tracking

| Check | Status | Notes |
|-------|--------|-------|
| Disclosure | APPROVED | Clear, visible, and merchant-compliant |
| Merchant terms | PENDING_FLIPKART_ACCOUNT_APPROVAL | Must pass Flipkart’s program terms |
| Geography | INDIA_ONLY | Flipkart India only |
| Factual claims | VERIFIED | Based on product specs and live measurements |
| Privacy | COMPLIANT | DPDP Act and GDPR aligned |
| Tracking | SUB-ID_CAPABLE | Flipkart supports UTM + sub-ID via link tagging |
| Platform policy | PENDING_FLIPKART_ACCOUNT_APPROVAL | Account approval required |

**Compliance gate:** HARD PASS/FAIL — no publishing without Flipkart account approval and terms acceptance.

## Sensitivity Forecast (Conservative)

Assumptions:
- Monthly clicks to rolling-cart assets: ~1,200 (based on current organic trend + internal linking lift)
- Conversion rates: 0.5%, 1%, 2%, 3% (mandatory sensitivity range)

| Rate | Orders/month | Est. commission (₹) |
|------|--------------|---------------------|
| 0.5% | 6 | 1,800 |
| 1%   | 12 | 3,600 |
| 2%   | 24 | 7,200 |
| 3%   | 36 | 10,800 |

**Note:** Forecast assumes Flipkart offer matches Amazon commission rate and product availability. Real performance may vary.

## Resource Envelope

- **Approved tools:** Amazon Associates, Flipkart Affiliate (pending), Canva, DeepSeek
- **Hosting:** GitHub Pages
- **API/model quotas:** DeepSeek 100k tokens/day
- **Spend ceiling:** ₹0/month (organic only)
- **Renewal dates:** Amazon Associates: 2027-03-31
- **Human-only dependencies:** Flipkart Affiliate account setup, payment/tax KYC, legal acceptance

## Next Steps

1. **Founder review & approval** — submit this plan for explicit approval.
2. **After approval:** Prepare Flipkart integration spec:
   - Data model: offer mapping, disclosure logic, sub-ID tagging
   - Content mapping: map 3 high-intent assets to Flipkart offer
   - QA checklist: disclosure visibility, link integrity, tracking test
3. **After Founder-gated account setup:** Execute QA and internal linking
4. **After QA pass:** Rotate to Pillar 1 (website development/conversion/SEO) for parallel progress

## Approval Gate

This plan contains no account creation, credentials, payment, or legal action. All autonomous work is preparatory and reversible. Founder-only gates remain protected.

---
*Autonomy audit trail: `data/autonomy_audit.jsonl`*
