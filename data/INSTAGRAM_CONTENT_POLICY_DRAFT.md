# RIO Instagram Content Policy — FOUNDER-LOCK DRAFT

Status: **DRAFT — FORMAT MIX + HOOK STRATEGY APPROVED; REMAINING ITEMS PENDING**

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
- Benefit, problem-solution, importance, or purchase/use rationale must be grounded in verified product facts or an explicitly supported use-case; AI must not invent performance, medical/safety, durability, compatibility, or outcome claims.

## 5. Affiliate disclosure
Every affiliate/product post must include a clear affiliate disclosure in the caption. Disclosure must not be hidden behind vague wording.

Current publisher wording includes an explicit commission disclosure and `#ad #affiliate`; this principle is retained, while final Founder-approved caption style remains pending.

## 6. Deduplication and evidence trail
- Confirmed posts must not be reposted as the same offer automatically.
- `data/ig_published.json` remains the confirmation record for Meta media IDs/permalinks.
- `data/instagram_run_status.json` remains the latest execution/result record.
- Real Meta/API errors must be retained in failure state for diagnosis.

## 7. FORMAT MIX — FOUNDER APPROVED
RIO uses a mixed Instagram format model. The format is selected by the content job, not randomly.

### Single-image post
Use for:
- quick deals;
- simple product highlights;
- fast product/value communication.

Primary focus: **Product + verified value/price where permitted + CTA**.

### Carousel post
Use for:
- buying guides;
- product comparisons;
- “best of” lists;
- feature/benefit explanations that require more than one frame.

Primary focus: **Value + information + save/share utility**.

### Reel
Use for:
- problem-solution content;
- demos/how-to;
- real usage/explanation;
- product/application stories where motion materially improves understanding.

Primary focus: **Engagement + reach + trust**.

### Format integrity rule
Regardless of format, RIO must preserve:
- real exact-product imagery where product-led;
- exact ASIN/product identity;
- no fake claims or fake urgency;
- required affiliate disclosure;
- value-first communication.

## 8. VISUAL HOOK / PROBLEM-SOLUTION RULE — FOUNDER APPROVED
RIO's AI engine may autonomously decide the most relevant hook/angle for each creative, based on the verified product and its supported use-case.

Allowed hook families include, where applicable:
- **problem first** — the practical problem/friction the product is meant to address;
- **why it matters** — why this product/use-case is useful or important in the target context;
- **benefit/use rationale** — what practical benefit the user can reasonably expect from the verified product function;
- **buy/use consideration** — why this product may be worth considering versus doing nothing or using a less suitable setup;
- **demo/how-to hook** — what the viewer will learn, see, or understand in a Reel/carousel.

Examples of structural hook styles (not fixed copy):
- “Struggling with ___?”
- “Why this matters in a small/rented home”
- “A simple way to solve ___”
- “Useful if you need ___ without ___”
- “Before you buy/use ___, check this”

AI chooses the hook dynamically. It is not required to use the same template repeatedly.

### Hook integrity guardrail
The hook is persuasive framing, not permission to exaggerate. It must remain consistent with verified product facts and RIO evidence standards. If the claimed problem/benefit cannot be supported, AI must select a different hook or omit it.

## 9. CURRENT IMPLEMENTATION BLOCKER
The current `scripts/publish_instagram.py` publishes `site/social/<offer_id>.png` branded cards as its Instagram image. Its own comments state that it intentionally does not use real product photos.

That implementation conflicts with the Founder-locked Product Image Policy, which requires the exact verified real product image as the primary product display and allows local RIO cards only as fallback assets.

**Required before autonomous Instagram product publishing is considered production-correct:** refactor the publisher/creative pipeline so the primary Instagram product image comes from the validated exact-product image registry or another Founder-approved exact-product image source. Until then, the branded-card implementation must not be treated as satisfying the locked product-image requirement.

## 10. FOUNDER DECISION PENDING
The following items still require explicit Founder approval before this document becomes FULLY LOCKED:

1. **Visual system** — exact layout, logo placement, typography/text overlay rules, aspect ratio beyond the approved AI hook behavior above.
2. **Caption style** — short/medium/long; Hinglish/English; practical vs editorial voice.
3. **CTA** — exact action requested from the viewer.
4. **Hashtag policy** — number/type; static vs generated.
5. **Cadence** — posts per week and preferred time windows.
6. **On-creative data** — whether price/rating/review count should appear on image/video or caption only.
7. **Approval model** — Founder approval per post/creative vs autonomous publication after policy/validator gates.
8. **Content mix** — percentage/priority between AI/design/professional content and Home & Living affiliate products.
9. **Reposting/update policy** — whether the same product may be reposted after a defined cooldown/new angle/new verified price.

## 11. Phase-2 implementation rule
Do not expand Instagram autonomous publishing until Sections 9 and 10 are resolved. Phase 2 should then implement the locked creative rules, measure outputs/results, and optimize only within the Founder-approved policy.

## Sources
- `INSTAGRAM_AUTOMATION.md`
- `PRODUCT_IMAGE_POLICY.md`
- `data/TELEGRAM_DEAL_DROP_FORMAT.md` (evidence principles only; Telegram formatting is not automatically an Instagram rule)
- `scripts/publish_instagram.py` (current implementation behavior)

## Founder decision log
- 2026-08-23: Founder approved the mixed model shown in the sample: single-image for quick deals/product highlights, carousel for guides/comparisons, Reel for demo/problem-solution content.
- 2026-08-23: Founder approved AI-selected hook/problem-solution framing. AI decides dynamically whether to emphasize why the product matters, the problem it solves, why it is useful/buy-worthy, or another applicable verified angle.
