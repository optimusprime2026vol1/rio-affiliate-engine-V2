# RIO X→X Offer Integrity Policy

## Non-negotiable invariant
Creative X → CTA X → tracking/campaign X → canonical destination X → exact intended product/variant X.

A near match is a failure. X-1, Z, a different size/color/model, a search-results page, an unintended bundle, or an unverified substitute must not pass as X.

## Release gate
An offer is BLOCKED unless all of the following are true:
1. Stable merchant product identifier is recorded when the merchant exposes one (ASIN/SKU/product ID).
2. Intended product name/model and promoted variant are recorded.
3. Creative product/variant exactly map to the intended landing product/variant.
4. Canonical destination has been manually or programmatically verified.
5. Availability has been checked.
6. Price-sensitive creative is refreshed at publish time; otherwise omit exact price claims.
7. Affiliate/tracking mapping is active and belongs to the same offer/campaign.
8. Claims and images describe the intended product; no fabricated testing/review claims.
9. The final CTA resolves to the verified destination, not a search/category/substitute page.

## Runtime controls
- Recheck active destinations on a schedule.
- Quarantine redirect/mismatch/unavailable offers.
- Never auto-substitute a different product into an existing creative.
- A replacement product gets a new offer identity and must pass the full gate.
- Log destination checks and identity changes.

## Attribution key
campaign_id + offer_id must travel together through click tracking. Revenue reporting must preserve the offer identity so Product X performance cannot silently merge into Product Z.
