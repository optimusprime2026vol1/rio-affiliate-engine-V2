# NEXT WORK — Instagram Review (source-grounded)

Status: **REVIEW BEFORE PHASE-2 EXECUTION**

This file consolidates only the Instagram/product-display rules currently supported by repository sources. It does not invent new posting strategy.

## 1. Existing Instagram automation flow
Source: `INSTAGRAM_AUTOMATION.md`

- State flow: `APPROVED -> POST_PENDING -> INSTAGRAM_POSTED`.
- Meta rejection becomes `FAILED_RETRY` with the real error reason.
- Missing credentials or failed validators are hard failures; a workflow must not report success when nothing posted.
- Founder approval source: `data/instagram_approval.json`.
- An offer can publish only when it is also `READY`, `ACTIVE`, `VERIFIED`, `IN_STOCK`, fresh enough, and has a public social card.
- `data/instagram_run_status.json` stores the latest attempt/reason.
- `data/ig_published.json` stores confirmed Meta media IDs/permalinks.
- Confirmed offers must not post twice.
- Instagram credentials remain secrets only (`IG_USER_ID_RIO`, `IG_ACCESS_TOKEN_RIO`).

## 2. Product-image requirements that must carry into Instagram creative review
Source: `PRODUCT_IMAGE_POLICY.md`

- Use the real image of the exact verified product/variant.
- Image ASIN and destination ASIN must match; no silent substitution.
- Amazon destination must carry `rioaffiliate-21`.
- Local RIO branded cards are fallback assets only; they must not silently replace the real product image as primary content.
- New offers cannot publish until image, ASIN and affiliate URL are present in `data/product_image_registry.json` and pass validation.
- Local fallback may be used only when the real image cannot load; the click target remains the verified Amazon destination.

## 3. Evidence/communication principles available from existing deal-drop format
Source: `data/TELEGRAM_DEAL_DROP_FORMAT.md`

These are Telegram-specific formatting rules, not automatically Instagram rules, but the underlying evidence principles are relevant for Phase-2 review:

- Only use READY verified offers.
- Price/rating/review-count must come from the latest verified record; never estimate or fabricate.
- Price-sensitive creative should be refreshed/rechecked before publish when stale/materially changed.
- No fake urgency unless the claim is actually visible and verified at post time.
- Affiliate disclosure must not be omitted where required.

## 4. Items NOT yet supported by the current source documents
The reviewed files do **not** define enough detail to lock the following without Founder input or another parked source:

- exact Instagram post visual layout/design system;
- reel vs carousel vs single-image priority;
- caption length/tone/format;
- hashtag policy;
- exact CTA wording;
- posting cadence/time-of-day for Instagram;
- whether prices/ratings should appear visually on the creative;
- approval policy for each creative vs autonomous publishing;
- content mix between professional AI/design-tool audience and Home & Living products.

These should be recovered from prior Founder instructions (if present elsewhere) or decided explicitly before Phase-2 Instagram automation is expanded.

## Phase-2 trigger
Next session/work block should resolve the unsupported items above, then encode the approved rules into a Founder-locked Instagram content policy before changing publishing behavior.
