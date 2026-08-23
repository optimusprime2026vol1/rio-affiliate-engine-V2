# RIO Instagram Content Policy — FOUNDER-LOCK DRAFT

Status: **DRAFT — DO NOT TREAT AS FULLY LOCKED UNTIL FOUNDER RESOLVES PENDING ITEMS**

Purpose: convert existing repository-backed Instagram and product-display rules into one operational policy for Phase 2. No unsupported posting strategy is invented here.

## 1. Objective
Instagram is a distribution and trust channel supporting RIO's locked business objective. It must produce measurable traffic/engagement/conversion signals without weakening evidence, product identity, affiliate disclosure, or publishing safety.

## 2. Non-negotiable eligibility gate
An Instagram product post may publish only when all of the following are true:
- offer `publish_status=READY`;
- affiliate status is `ACTIVE`;
- product identity is `VERIFIED`;
- availability is `IN_STOCK`;
- required RIO validators pass;
- RIO kill switch is OFF;
- product verification is fresh enough under the current staleness gate;
- a valid publish creative exists;
- the offer has not already been confirmed as posted;
- required Instagram credentials are present only through secrets.

State flow remains:
`APPROVED -> POST_PENDING -> INSTAGRAM_POSTED`

A Meta/API failure becomes `FAILED_RETRY` with the real error reason. A workflow must never report success when no post was actually published.

## 3. Product image integrity — FOUNDER LOCKED
For product-led Instagram creative:
- the primary visual must use the real image of the exact verified product/variant;
- image ASIN and destination ASIN must match;
- no silent product/variant substitution;
- the associated Amazon destination must use the RIO affiliate tag `rioaffiliate-21` where an Amazon affiliate destination is used;
- `data/product_image_registry.json` must contain the image/product/affiliate mapping and validation must pass;
- a local RIO branded card is a fallback/support asset only and must not silently replace the real product image as the primary product creative.

## 4. Evidence and claims
- Never fabricate or estimate price, rating, review count, stock, scarcity, product identity, or verification status.
- Any price/rating/review count used in creative or caption must come from the latest verified record.
- Price-sensitive creative must be refreshed/rechecked before publish when the evidence is stale or materially changed.
- No fake urgency or scarcity claim.
- If the system cannot verify a claim to the required standard, omit the claim or block the post.

## 5. Affiliate disclosure
Every affiliate/product post must include a clear affiliate disclosure in the caption. Disclosure must not be hidden behind vague wording.

Current publisher wording includes an explicit commission disclosure and `#ad #affiliate`; this principle is retained, while final Founder-approved caption style remains pending.

## 6. Deduplication and evidence trail
- Confirmed posts must not be reposted as the same offer automatically.
- `data/ig_published.json` remains the confirmation record for Meta media IDs/permalinks.
- `data/instagram_run_status.json` remains the latest execution/result record.
- Real Meta/API errors must be retained in failure state for diagnosis.

## 7. CURRENT IMPLEMENTATION BLOCKER
The current `scripts/publish_instagram.py` publishes `site/social/<offer_id>.png` branded cards as its Instagram image. Its own comments state that it intentionally does not use real product photos.

That implementation conflicts with the Founder-locked Product Image Policy, which requires the exact verified real product image as the primary product display and allows local RIO cards only as fallback assets.

**Required before autonomous Instagram product publishing is considered production-correct:** refactor the publisher/creative pipeline so the primary Instagram product image comes from the validated exact-product image registry or another Founder-approved exact-product image source. Until then, the branded-card implementation must not be treated as satisfying the locked product-image requirement.

## 8. FOUNDER DECISION PENDING
Existing repository sources do not define these items. They must be explicitly resolved before this document becomes FULLY LOCKED:

1. **Format mix** — single image vs carousel vs Reel priority.
2. **Visual system** — exact layout, logo placement, typography/text overlay rules, aspect ratio.
3. **Caption style** — short/medium/long; Hinglish/English; practical vs editorial voice.
4. **CTA** — exact action requested from the viewer.
5. **Hashtag policy** — number/type; static vs generated.
6. **Cadence** — posts per week and preferred time windows.
7. **On-creative data** — whether price/rating/review count should appear on image/video or caption only.
8. **Approval model** — Founder approval per post/creative vs autonomous publication after policy/validator gates.
9. **Content mix** — percentage/priority between AI/design/professional content and Home & Living affiliate products.
10. **Reposting/update policy** — whether the same product may be reposted after a defined cooldown/new angle/new verified price.

## 9. Phase-2 implementation rule
Do not expand Instagram autonomous publishing until Sections 7 and 8 are resolved. Phase 2 should then implement the locked creative rules, measure outputs/results, and optimize only within the Founder-approved policy.

## Sources
- `INSTAGRAM_AUTOMATION.md`
- `PRODUCT_IMAGE_POLICY.md`
- `data/TELEGRAM_DEAL_DROP_FORMAT.md` (evidence principles only; Telegram formatting is not automatically an Instagram rule)
- `scripts/publish_instagram.py` (current implementation behavior)
