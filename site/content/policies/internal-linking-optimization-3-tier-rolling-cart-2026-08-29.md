# Internal Linking Optimization Plan — 3-Tier Rolling Cart

**Date:** 2026-08-29  
**Offer ID:** `3-tier-rolling-cart`  
**Status:** READY FOR EXECUTION  
**Pillar:** 1 — Website Development / Conversion / SEO  
**Rotation Status:** Least-used pillar (0 *new* completed tasks since last rotation)

## Why
With 17 verified offers and zero approved revenue, conversion-path readiness is the highest-impact priority. Internal linking between high-intent assets (buying guide, product-led blog, Instagram carousel) improves SEO signals, user journey coherence, and conversion probability without requiring new content or Founder-only actions.

This plan leverages existing verified assets to create a closed-loop conversion funnel:

`Instagram → Buying Guide → Product-Led Blog → Amazon Offer`

All assets are already published and verified; this is purely a linking and tracking enhancement.

## Current State
- **Buying Guide:** Published, links to cart (explicit CTA in conclusion)
- **Product-Led Blog:** Published, links to cart (inline in 'Top Pick' section)
- **Instagram Carousel:** Published, links to cart (caption + slide 1 disclosure)

No cross-links exist between the three high-intent assets themselves.

## Proposed Optimizations

| From Asset | To Asset | Placement | Anchor Text | Tracking Hint |
|------------|----------|-----------|-------------|---------------|
| Product-Led Blog | Buying Guide | End of blog post | "Compare 5 top rolling carts in our detailed buying guide" | `?utm_source=product-led-blog&utm_medium=internal-link&utm_campaign=rolling-cart-optimization` |
| Buying Guide | Product-Led Blog | Sidebar callout box | "See how this cart solves real Indian workspace problems" | Same UTM pattern |
| Instagram Carousel | Buying Guide | Caption link (replace generic link) | "Full comparison + measurements →" | Same UTM pattern |

## Compliance & Tracking
- **Disclosures:** Present in all assets; no change required.
- **Merchant Terms:** Amazon Associates India terms followed.
- **Geography:** India-only targeting maintained.
- **Factual Claims:** Verified against product specs.
- **Privacy:** No third-party tracking beyond Amazon.
- **Tracking:** UTM + Amazon sub-ID configured.
- **Platform Policy:** Instagram caption + link policy respected.

## Resource Envelope
- **Tools Used:** Existing site CMS, Markdown editor
- **API Quota Used:** 0
- **Spend Ceiling (INR):** 0
- **Human-Only Dependencies:** None

## Sensitivity Forecast (Monthly)
Based on ~200 estimated monthly visits to high-intent assets:
- 0.5% conversion → 1 verified order
- 1% conversion → 2 verified orders
- 2% conversion → 4 verified orders
- 3% conversion → 6 verified orders

## Next Steps
1. Commit changes to repo
2. Run validators (`scripts/validate_offer_integrity.py`, `scripts/validate_dashboard.py`, etc.)
3. Draft updated Instagram caption + slide 1 disclosure with new internal link anchor text
4. Submit for Founder review and approval
5. Rotate to Pillar 2 (new affiliate networks and product opportunities)

## Blocker
None. All changes are safe, reversible, and within delegated authority.
