# RIO Product Image Policy

Status: **Founder-locked requirement**  
Confirmed by Vicky Gautam: 2026-08-22  
Amended by Founder directive: 2026-08-28

## Non-negotiable display rule

1. Every product placement must show the real image of the exact verified product or variant.
2. Clicking or tapping the image must open the matching Amazon.in ASIN directly.
3. Every Amazon destination must include the RIO tracking tag `rioaffiliate-21`.
4. Image ASIN and destination ASIN must match. No auto-substitution is allowed.
5. Local RIO branded cards are fallback assets only. They must never silently replace real product images as the primary website content.
6. New offers cannot publish until image, ASIN and affiliate URL are added to `data/product_image_registry.json` and pass validation.

## Merchant-branding amendment — 2026-08-28

7. RIO-generated promotional creatives must be product-first and RIO-branded; Amazon or other merchant/marketplace logos, wordmarks, badges, or decorative branding must not be added as default visual elements.
8. A merchant trademark or approved marketplace asset may appear only when its use is explicitly permitted by the applicable affiliate-program/trademark rules and RIO has a compliant reason to use it. RIO must not imply sponsorship, endorsement, partnership, or ownership by the merchant.
9. Merchant branding is not required merely to tell the customer where the CTA leads. The CTA may use neutral language such as `Check current price`, `View product`, or `See current offer`; the customer can see the merchant after following the verified destination.
10. Required affiliate disclosure remains mandatory and must not be removed with merchant branding. Disclosure and merchant trademark treatment are separate compliance requirements.
11. The CTA/destination must continue to resolve to the exact verified product/variant using the valid RIO affiliate link and tracking tag.
12. Creative-generation and publication logic must treat unauthorized/default merchant branding as a validation failure. A creative containing merchant branding may publish only when that asset/use has been explicitly approved under the applicable program rules.

## Repository history

- `3a628e48f79c410728d84666ffa8f6fe37cf3b6f` introduced real Amazon product photos on the redesigned homepage.
- `05c021f` linked homepage offers directly to Amazon.
- The 2026-08-22 production audit replaced Amazon-hosted images with RIO text cards because provenance was not machine-readable.
- Vicky reconfirmed that this replacement contradicted the intended customer experience. Real images were restored from repository history and protected by a registry plus validation gate.
- 2026-08-28 Founder amendment established product-first/RIO-branded creatives, prohibited default unauthorized merchant branding, preserved affiliate disclosure, and required merchant-branding validation before publication.

## Reliability

Each real product image keeps a local RIO fallback. The fallback is used only if the real image cannot load; the image click continues to use the verified direct Amazon destination.
