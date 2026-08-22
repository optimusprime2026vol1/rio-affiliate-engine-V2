# RIO Product Image Policy

Status: **Founder-locked requirement**  
Confirmed by Vicky Gautam: 2026-08-22

## Non-negotiable display rule

1. Every product placement must show the real image of the exact verified product or variant.
2. Clicking or tapping the image must open the matching Amazon.in ASIN directly.
3. Every Amazon destination must include the RIO tracking tag `rioaffiliate-21`.
4. Image ASIN and destination ASIN must match. No auto-substitution is allowed.
5. Local RIO branded cards are fallback assets only. They must never silently replace real product images as the primary website content.
6. New offers cannot publish until image, ASIN and affiliate URL are added to `data/product_image_registry.json` and pass validation.

## Repository history

- `3a628e48f79c410728d84666ffa8f6fe37cf3b6f` introduced real Amazon product photos on the redesigned homepage.
- `05c021f` linked homepage offers directly to Amazon.
- The 2026-08-22 production audit replaced Amazon-hosted images with RIO text cards because provenance was not machine-readable.
- Vicky reconfirmed that this replacement contradicted the intended customer experience. Real images were restored from repository history and protected by a registry plus validation gate.

## Reliability

Each real product image keeps a local RIO fallback. The fallback is used only if the real image cannot load; the image click continues to use the verified direct Amazon destination.
