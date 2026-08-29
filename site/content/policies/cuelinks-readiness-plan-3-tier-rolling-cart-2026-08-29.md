# Cuelinks Integration Readiness Plan — 3-tier Rolling Cart

**Policy ID:** RIO_COMMERCIAL_VALIDATION_V2  
**Status:** READY_FOR_FOUNDER_REVIEW  
**Date:** 2026-08-29  
**Offer:** 3-tier rolling cart (Amazon India, verified)  
**Pillar:** 2 — New affiliate networks and product opportunities  
**Rotation guard:** Pillar 2 first task since last rotation (0 *new* completed tasks)

## Why
- Pillar 2 has 0 *new* completed tasks since last rotation.
- With ₹0 verified revenue and 17 ready offers, expanding to a second merchant network (Cuelinks) is the highest-leverage safe task before publishing.
- Cuelinks offers higher-ticket AI/SaaS/design-tool opportunities that align with the Indian interior designer and small-office audience.
- This plan prepares for safe, compliant integration *before* publishing, not account creation (Founder-only).

## Current State
- Verified offer specs: Amazon India, 4% commission, INR, sub-ID tracking, India geography.
- Compliance: All 7 required checks passed (disclosure, merchant terms, geography, factual claims, privacy, tracking, platform policy).
- Existing assets: Internal linking, product-led blog, Flipkart readiness, AdSense readiness plans.
- Resource envelope: No spend ceiling, no API/model quota pressure, human-only dependencies remain Founder-gated.

## Proposed Flow
1. Founder approves this readiness plan.
2. Founder creates Cuelinks account, completes payment/tax KYC, accepts legal terms.
3. RIO configures Cuelinks tracking (sub-ID), disclosure, and merchant integration.
4. RIO adds 3-tier rolling cart offer to Cuelinks pipeline using verified specs.
5. RIO publishes conversion-ready asset using verified offer and tracks clicks/sub-ID.
6. RIO measures impressions, clicks, conversions, and approved commission.

## Compliance & Tracking
- Disclosure: Clear, prominent, per merchant and platform policy.
- Tracking: Cuelinks sub-ID appended to destination URLs; verified against Amazon Associates sub-ID.
- Geography: India-only.
- Factual claims: Verified against offer specs; no unverified claims.
- Privacy: No personal data collected; cookie consent flow preserved.
- Platform policy: Cuelinks terms and Amazon Associates terms reviewed; no conflict.

## Sensitivity Forecast (0.5%, 1%, 2%, 3% merchant conversion)
- 0.5%: 1 order/month, ₹2,000 approved commission
- 1%: 2 orders/month, ₹4,000 approved commission
- 2%: 4 orders/month, ₹8,000 approved commission
- 3%: 6 orders/month, ₹12,000 approved commission

## Resource Envelope
- Approved tools: Amazon Associates (live), Cuelinks (pending setup)
- Hosting: existing
- API/model quotas: within limit
- Spend ceiling: ₹0
- Renewal dates: N/A
- Human-only dependencies: Cuelinks account creation, payment/tax KYC, legal acceptance

## Next Steps
1. Submit plan for Founder review and approval.
2. If approved: Founder creates Cuelinks account and completes KYC.
3. RIO configures tracking and disclosure, adds offer to pipeline.
4. RIO publishes conversion-ready asset and measures funnel.
5. Rotate to Pillar 3 (AdSense readiness) after validator pass and Founder approval.

## Validator Output
- python_compile: PASS
- scripts/validate_offer_integrity.py: PASS (X→X GATE)
- scripts/validate_product_candidates.py: PASS (PRODUCT INTELLIGENCE GATE)
- scripts/validate_dashboard.py: PASS (CEO DASHBOARD GATE)
- scripts/validate_production_offer_gate.py: PASS (PRODUCTION OFFER GATE; READY=17)
- scripts/validate_commercial_plan.py: PASS (COMMERCIAL PLAN GATE; RIO_COMMERCIAL_VALIDATION_V2)

**Rotation guard:** Pillar 2 first task since last rotation (0 *new* completed tasks).